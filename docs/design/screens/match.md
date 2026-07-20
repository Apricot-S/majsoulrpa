# MatchScreen 設計

## 目的と範囲

`MatchScreen` は、合意済みの友人戦・大会の対局画面を検出し、試合全体と現在局の状態を
decoded WebSocket message から管理する `Screen` である。

この文書では、対局開始時および途中復帰時の初期化、局をまたぐ状態遷移、callback の
ライフサイクル、再同期の共通化方針を定める。打牌、副露、和了などの個別操作 API と
結果画面の UI 操作は、対応する段階で別途詳細化する。

`references/match/` の v1-develop 実装は message の種類、action の意味、実通信で起こり得る
順序差を知るために参照する。mutable state、局ごとの Presentation 再生成、同期処理の分岐、
private API はそのまま移植しない。

## 結論

- reload / 再ログインを挟まない間は、局をまたいで 1 つの `MatchScreen` instance と 1 回の
  callback invocation を維持する。
- `ActionNewRound` では current round snapshot を置き換え、`MatchScreen` を stale にしない。
- live action と restore action は別 decoder adapter で正規化し、同じ reducer へ渡す。
- 新規開始と途中復帰は同じ bootstrapper で初期化し、public な `restore` flag は設けない。
- 対局中の `syncGame` も同じ replay 処理で現在の instance を再同期する。
- state は immutable snapshot とし、`MatchScreen` instance 内の具体的 store に保持する。
- `RoundState` は current snapshot に加えて、同じ reducer が適用した局内 event 列を保持する。
- 対応対象の protocol action 1 件を public `MatchEvent` 1 件へ直接正規化し、内部 action union は作らない。
- concrete event は `@final` な frozen dataclass、`MatchEvent` は全 event を列挙する明示的 union とする。
- 初期化 milestone で追加する公開 API は `get_state()` だけとし、状態待機や操作 API は後続で
  1 つずつ追加する。
- Match 専用 background task、decode 直後の observer、共有 Match cache は追加しない。
- Match 中も generic `Screen.reload()` を使い、成功後は callback を直ちに return する。
- reload / 再ログイン後は新しい `MatchScreen` instance を途中復帰と同じ bootstrap で復元する。

この判断は
[ADR-0006: MatchScreenを局遷移では維持しaction reducerを共有する](../../adr/0006-match-screen-lifecycle-and-reducer.md)
に記録する。

## callback のライフサイクル

v1-develop は局終了後の `ActionNewRound` ごとに Match 相当 object を作り直し、user callback へ
制御を戻していた。現在の `MatchScreen` はこの境界を採用しない。

```text
MatchScreen を画像検出
  -> before_callback() で bootstrap
  -> user callback を 1 回開始
       -> state を読む / 次の state change を待つ / 操作する
       -> ActionNewRound: 同じ MatchScreen 内で round を交換
       -> syncGame: 同じ MatchScreen 内で state を再構築
       -> reload: stale になった後、callback から直ちに return
       -> match terminal: 結果処理後に stale
  -> callback が return
  -> runtime が次の Screen を検出
```

callback 利用者は試合が active の間、callback 内の loop を継続する。active 中の早期 return を
framework が試合終了として補完しない。早期 return を検出する runtime hook は必要性が確認される
まで追加せず、Match callback の利用契約として明記する。ただし、明示的な `reload()` は recovery
境界である。呼び出し後は同じ Screen を使わず、user data を return して runtime の Screen 検出へ
制御を戻す。

## 状態の所有

### immutable snapshot

初期化 milestone の公開状態は概念的に次の immutable 型とする。名称は v1-develop の利用者向け
property を考慮しつつ、mutable list や内部 object を公開しない形へ変更する。

```python
class MatchOrigin(StrEnum):
    FRIENDLY = "friendly"
    TOURNAMENT = "tournament"


@dataclass(frozen=True, slots=True)
class MatchRank:
    id: int
    score: int


@dataclass(frozen=True, slots=True)
class MatchPlayer:
    seat: int
    account_id: int
    name: str
    level4: MatchRank
    level3: MatchRank

    @property
    def is_cpu(self) -> bool: ...


@dataclass(frozen=True, slots=True)
class MatchDapai:
    tile: str
    moqie: bool
    liqi: bool
    wliqi: bool


class MatchFuluKind(StrEnum):
    CHI = "chi"
    PENG = "peng"
    DAMINGGANG = "daminggang"
    ANGANG = "angang"
    JIAGANG = "jiagang"


@dataclass(frozen=True, slots=True)
class MatchFulu:
    kind: MatchFuluKind
    tiles: tuple[str, ...]
    from_seat: int | None


@dataclass(frozen=True, slots=True)
class RoundState:
    generation: int
    step: int
    chang: int
    ju: int
    ben: int
    liqibang: int
    dora_indicators: tuple[str, ...]
    left_tile_count: int
    scores: tuple[int, ...]
    shoupai: tuple[str, ...]
    zimopai: str | None
    he: tuple[tuple[MatchDapai, ...], ...]
    fulu: tuple[tuple[MatchFulu, ...], ...]
    num_babei: tuple[int, ...]
    liqi: tuple[bool, ...]
    wliqi: tuple[bool, ...]
    first_draw: tuple[bool, ...]
    yifa: tuple[bool, ...]
    lingshang_zimo: tuple[bool, ...]
    previous_dapai_seat: int | None
    previous_dapai_tile: str | None
    has_pending_operation: bool
    events: tuple[MatchEvent, ...]


@dataclass(frozen=True, slots=True)
class MatchState:
    version: int
    match_id: str
    origin: MatchOrigin
    origin_id: int
    self_seat: int
    players: tuple[MatchPlayer, ...]
    round: RoundState
```

human player は正の `account_id`、`name`、四麻段位 `level4`、三麻段位 `level3` を必須とする。
`MatchRank` は `AccountLevel.id` と `score` を失わず保持する。段位名への変換表を state の正本に
すると雀魂側の追加段位へ追従できず、Kanachan などの categorical feature にも再変換が必要になる
ため、protocol の数値を正本とする。表示名が必要なら別 adapter で変換する。通常の友人戦では human
player だけが response `players` に入り、CPU は `robots` に分離される。一方 VS_AI では human は
自分 1 人だけ、`robots` は空で、`seat_list` の残りの participant ID がすべて `ready_id_list` に入る。
どちらの形式でも CPU の participant ID を human account ID と同じ公開 field に保持し、CPU の name は
空文字列とする。human の name は空文字列にならないため、`MatchPlayer.is_cpu` は `name == ""` から
判定できる。

CPU の `level` / `level3` は wire 上存在しないが、画面にはどちらも初心 1 と表示される。公開 state も
画面表示に合わせ、四人麻雀 `level4=MatchRank(id=10101, score=0)`、三人麻雀
`level3=MatchRank(id=20101, score=0)` を設定する。`CPU(簡単)` / `CPU(普通)` は実際に取得可能な human
player name なので CPU の補完名には使わない。これにより `account_id`、`name`、両段位はいずれも
非 optional となり、利用者が `None` を分岐する必要をなくす。character などの cosmetic metadata は
実需要が出るまで公開しない。

`RoundState.shoupai` は自分の配牌を昇順の tuple で保持する。雀魂の `ActionNewRound.tiles` が 14 枚の
場合、その 14 枚すべてが手積み麻雀と同様の配牌である。14 枚全体を sort し、右端の 1 枚を表示上
便宜的に `zimopai` の位置へ分離し、残り 13 枚を `shoupai` とする。wire 上の最後の tile を実際の
ツモ牌と解釈して先に分離しない。13 枚の場合は全体を sort して `shoupai` とし、`zimopai=None` と
する。この処理は v1-develop の実装を維持する。

用語は雀魂 protobuf と v1-develop の domain 語彙に合わせ、`zimo`、`dapai`、`chi`、`peng`、
`gang`、`liqi` などのピンインを canonical name とする。立直の一般的なピンインは `lizhi` だが、
雀魂は `liqi`、`is_liqi`、`LiQiSuccess`、`liqibang` を一貫して使っている。ここだけ `lizhi` にすると
protocol adapter と public model の間に恒常的な別名が生じるため、API でも `liqi` を採用し、
`lizhi` alias は設けない。Mjai の `reach` など外部 protocol の語彙は、その adapter 境界で変換する。

operation の protocol data は immutable な内部 snapshot として同時に保持するが、operation type と
操作 API を設計する前に生の数値を公開しない。初期 `MatchState` では
`RoundState.has_pending_operation` だけを公開し、operation 詳細は最初の操作 API と同時に公開する。

`ActionNewRound` では match identity と player metadata を維持し、round generation を増やして
新しい `RoundState` を設定する。局の step は局ごとに 0 から始め、instance の version とは
分ける。state の collection は tuple などとし、内部 list をそのまま公開しない。

`MatchState.version` は同じ Screen instance 内で公開 snapshot を publish するたびに増加する。
fresh / recovery bootstrap が最初に publish する version は 1 とする。restore の historical action
ごとには version を公開せず、temporary store で replay がすべて成功した後に完成 snapshot を一度
だけ publish する。active 中の再同期も同様に、成功時だけ以前の version + 1 を publish する。

### 局内 event 列

`RoundState.events` は append-only な意味上の event 列である。最初の局では `StartMatchEvent` を index 0、
`NewRoundEvent` を index 1 とする。二局目以降または restore batch に `ActionMJStart` がない場合は、
`NewRoundEvent` を index 0 とする。immutable snapshot の一部なので公開型は mutable な `list` ではなく
`tuple[MatchEvent, ...]` とする。次局の `ActionNewRound` では新しい `RoundState` とともに event 列も
新しい `NewRoundEvent` から開始する。試合全体の過去局を store に蓄積し続けず、必要な AI adapter
または callback 利用者が局をまたいだ履歴を保持する。

public event は標準 library の frozen dataclass とする。concrete event は `@final`、`slots=True`、
`kw_only=True` とし、同じ module に全 concrete class を列挙した public type alias `MatchEvent` を置く。
`type` discriminator は設けず、利用者は concrete event class に対する class pattern で型を絞り込む。

field の型は annotation と静的型検査で保証する。各 class の `__post_init__()` は共通 validator を使い、
値域、tuple 要素間の関係、相互排他など、型だけでは表せない不変条件を検証する。未知 keyword は
dataclass constructor が拒否する。nested value も frozen dataclass と tuple だけで構成し、構築後に
内容を変更できないようにする。

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class _MatchEventBase:
    action_step: int

    def __post_init__(self) -> None:
        validate_action_step(self.action_step)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StartMatchEvent(_MatchEventBase):
    pass


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiqiSuccess:
    seat: int
    score: int
    liqibang: int
    failed: bool

    def __post_init__(self) -> None:
        validate_seat(self.seat)
        validate_score(self.score)
        validate_nonnegative_int("liqibang", self.liqibang)
        validate_bool("failed", self.failed)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ZimoEvent(_MatchEventBase):
    seat: int
    tile: str | None
    left_tile_count: int
    liqi_success: LiqiSuccess | None = None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        validate_seat(self.seat)
        validate_optional_tile(self.tile)
        validate_left_tile_count(self.left_tile_count)
        validate_optional_instance("liqi_success", self.liqi_success, LiqiSuccess)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiEvent(_MatchEventBase):
    seat: int
    tile: str
    moqie: bool
    liqi: bool
    wliqi: bool
    dora_indicators: tuple[str, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        validate_seat(self.seat)
        validate_tile(self.tile)
        validate_bool("moqie", self.moqie)
        validate_bool("liqi", self.liqi)
        validate_bool("wliqi", self.wliqi)
        if self.liqi and self.wliqi:
            raise ValueError("liqi and wliqi are mutually exclusive")


type MatchEvent = (
    StartMatchEvent
    | NewRoundEvent
    | ZimoEvent
    | DapaiEvent
    | ChiEvent
    | PengEvent
    | DaminggangEvent
    | AngangEvent
    | JiagangEvent
    | BabeiEvent
)


def event_name(event: MatchEvent) -> str:
    match event:
        case StartMatchEvent():
            return "start_match"
        case NewRoundEvent():
            return "new_round"
        case ZimoEvent():
            return "zimo"
        case DapaiEvent():
            return "dapai"
        case ChiEvent():
            return "chi"
        case PengEvent():
            return "peng"
        case DaminggangEvent():
            return "daminggang"
        case AngangEvent():
            return "angang"
        case JiagangEvent():
            return "jiagang"
        case BabeiEvent():
            return "babei"
    assert_never(event)
```

各 case は `return`、`raise`、loop 内の `continue` などで control flow を終え、`match` の直後に
`assert_never(event)` を置く。`MatchEvent` union に新しい concrete class を追加して利用側が未対応の
ままなら、`ty` は `assert_never()` の引数が `Never` でないことを報告する。`case _` は使わない。

上記は初期 active-round reducer の union であり、局終了 reducer と同時に `HuleEvent`、
`NoTileEvent`、`LiujuEvent` を追加する。`ActionDiscardTile` は `DapaiEvent` 1 件に変換し、立直宣言牌か
どうかを `liqi` / `wliqi` field に含める。独立した `LiqiEvent` は作らない。後続 action に埋め込まれた
`LiQiSuccess` も独立 event に分離せず、その action に対応する event の `liqi_success` field として
保持し、reducer が同じ event の適用中に点数と `liqibang` を更新する。これは雀魂の action 境界を
保ち、Kanachan の打牌 feature へ変換しやすくするためである。Mjai の `reach` / `reach_accepted` への
分離が必要な adapter は、`DapaiEvent` と後続 event の `liqi_success` から外部境界で生成する。

`ActionNewRound.tiles` が14枚の場合は全体をsortして右端を便宜上 `zimopai` に分離しているため、親の
第一打牌では `moqie == false` でも打牌が `shoupai` ではなく `zimopai` と一致する場合がある。
`DapaiEvent` reducer は、自分が親、当該 seat の第一打牌、打牌が `zimopai` と一致するという条件を
すべて満たす場合に限り、この牌を `zimopai` から除く。通常の手出しは `shoupai` から牌を除いた後、
残っている `zimopai` を手牌へ取り込んでsortする。ツモ切りは打牌と `zimopai` の一致を要求する。

Sniffer の観測時刻は transport metadata であり、public event には保持しない。live message の
`observed_at` は Sniffer 調査ログに残す。event の順序は `RoundState.events` の tuple 順を正本とし、
`action_step` で protobuf action との対応を検証できる。1 action 1 event なので別の event index は
持たせない。

### instance-local store

`MatchStateStore` は `MatchScreen` instance が所有し、normalized `MatchEvent` を immutable snapshot へ
reduce する。Room と同様に active 中は同じ callback invocation と Screen instance を維持するため、
`ScreenContext` に
共有 `MatchStateCache` は追加しない。

画面遷移を伴わない network reconnect で `syncGame` を受信した場合は、同じ store を再構築する。
`Screen.reload()` または再ログインでは現在の instance を stale にし、新しく検出した
`MatchScreen` が `syncGame` から新しい store を構築する。以前の instance の state は引き継がず、
callback 間で維持したい利用者側の情報だけを callback の user data で渡す。

store は raw message 履歴や decoded protobuf object を保持しない。一方、restore adapter も過去 action
から live と同じ public event を構築し、同じ reducer で適用して完成した `RoundState.events` に含める。
これにより途中復帰直後でも Mjai protocol adapter や Kanachan の Progression Features が局内履歴を
利用できる。restore 中に生成した transition は callback へ「新着 event」として再通知せず、完成
snapshot の履歴としてだけ公開する。履歴の再構築と通知の抑止を分け、restore 専用 reducer は作らない。

restore / active resync は現在の store を直接書き換えながら replay しない。同じ metadata から
temporary store を作り、action 列、step、state invariant の検証がすべて成功した場合だけ、完成した
snapshot と内部 operation snapshot を current store へ commit する。途中の action で失敗した場合は
以前の公開 state を変更せず、元の失敗を伝播する。

## 初期化 milestone の公開 API

最初に追加する高レベル API は次の 1 つだけとする。

```python
async def get_state(self) -> MatchState: ...
```

`before_callback()` が初期 snapshot を構築済みであることを保証する。`get_state()` は network request
や click を行わず、queue に蓄積済みの Match message を `get_nowait()` で順に reduce してから最新の
snapshot を返す。初期化後の blocking wait は別 API として次段階で追加する。state 型と public
`MatchEvent` union / event model は `majsoulrpa.screens.match` から export し、wire adapter、decoder、
store は export しない。

公開 API の info log は `screen=MatchScreen api=get_state` という構造情報だけを含め、state、match ID、
player、牌、operation を含めない。

## match metadata の decode と対象範囲

`.lq.FastTest.authGame` は outbound request / response だけを受理する。request の `account_id` は
session account ID と一致し、`game_uuid` は空でないことを要求する。token は検証対象や state に
保存せず、通常 log と例外 message に含めない。

response の `seat_list` は 3 または 4 seat とし、session account ID が一度だけ現れることを要求する。
`players` は human player だけを含み、その account ID は `seat_list` の human seat と一対一に対応
しなければならない。通常の友人戦では `robots` が CPU metadata を含み、metadata decoder は
`players` と `robots` をそれぞれ wire `account_id` で索引して seat を決める。

VS_AI では `players` が session account 1 人だけで `robots` が空になる。`seat_list` から human ID を
除いたすべての participant ID が、重複なく `ready_id_list` と完全一致する場合に限り、それらを
metadata の省略された CPU として扱う。CPU は wire の participant ID、空の name、画面表示に合わせた
既定段位を持つ `MatchPlayer` へ正規化する。この条件を満たさない未知 seat ID、human / robot 間の
ID 重複、seat に現れない余剰 metadata は不整合にする。

対象 match は合意済み友人戦または大会だけである。`game_config.meta.room_id` と `contest_uid` の
うち、友人戦では `room_id` に友人戦 ID が入り、`mode_id` と `contest_uid` は 0 になることを実通信で
確認した。この組み合わせから `MatchOrigin.FRIENDLY` と `origin_id=room_id` を構築する。大会の
組み合わせは実通信確認後に `MatchOrigin.TOURNAMENT` へ固定する。`room_id` と `contest_uid` が両方
0 の場合は、段位戦やイベント戦などのオープン対局である可能性が高い。ただし現時点では推測であり、
分類を確定せず対象外 match として `ScreenUnexpectedStateError` にする。両方が正の場合も受理しない。

初期対応は通常の三人戦 / 四人戦 action に限定する。`game_config.mode` と `detail_rule` から特殊 mode
を識別できる field は手動 spike で固定し、血戦、換三張、open hand など reducer が未対応の mode は
初期化を成功させない。有効な protocol だが対象 mode 未対応の場合は `ScreenUnexpectedStateError`、
field 型や相互関係が壊れている場合は `ScreenInconsistentMessageError` とする。

## action の正規化

Sniffer の共通 decoder は outer Liqi message の protobuf decode に留める。
`.lq.ActionPrototype.data` の復号と action message 型の decode は Match 固有 decoder が担当する。

対応対象の protobuf action は同じ意味の internal model を経由せず、public `MatchEvent` union member
へ直接正規化する。入力 adapter は encoding の違いに応じて明示的に分ける。

- live adapter: `.lq.ActionPrototype` の obfuscated `data` を unmask して decode する
- restore adapter: `syncGame.response.game_restore.actions` の plain `data` を decode する

unknown protobuf field に Match action 固有の検査は設けず、共通 protobuf parser と同様に既知 field
だけを利用する。

両 adapter は action 名をkeyとするdecoder registryからevent classmethodを選び、decoded dataを渡す。
外部入力の共通fieldはadapter、event固有のfieldと不変条件はclassmethodとdataclassが検証する。
`ActionMJStart` は `StartMatchEvent`、
`ActionNewRound` は `NewRoundEvent`、
`ActionDealTile` は `ZimoEvent`、`ActionDiscardTile` は `DapaiEvent` のように、protocol action と
event object を 1 対 1 に対応させる。`ActionChiPengGang` と `ActionAnGangAddGang` は protocol 内の
`type` に応じて具体的な `ChiEvent` / `PengEvent` / gang event class を選ぶが、1 action から生成する
event は常に 1 件である。

`StartMatchEvent` は current round より前に届くため、bootstrapper の temporary store で prelude event
として保持する。続く `NewRoundEvent` が最初の `RoundState` を生成するとき、両方を到着順のまま
`RoundState.events` に入れる。reducer 上は state を変更しない event だが、機械学習 AI が match の
BOS feature として利用できる。不要な利用者は `StartMatchEvent` を読み飛ばせばよい。

protobuf decode 後の `dict[str, JsonValue]` はログ用 action data と event class 固有の `from_dict()`
classmethod への入力に使う。classmethod が外部入力から型付き field を取り出し、値の正規化を行って
concrete constructor を呼ぶ。raw dict を constructor へそのまま展開せず、型付き API は維持する。
action に付随する現在の選択可能 operation は発生済み event ではないため、
event と重複する action model を作らず、adapter が immutable な内部 operation snapshot として
別に返す。後続の操作 API ではこれを public `MatchOperation` として別途設計する。

`restore: bool` は reducer や state model まで伝播させない。live / restore の encoding 差は action
adapter 内で解消し、同じ decoded data と event classmethod から同じ public event を生成する。

nested message type は `liqi_pb2.DESCRIPTOR` から action 名で解決する。ただし descriptor に存在する
任意の action を暗黙に受理せず、初期化時の allowlist を次に限定する。

- `ActionMJStart`
- `ActionNewRound`
- `ActionDealTile`
- `ActionDiscardTile`
- `ActionChiPengGang`
- `ActionAnGangAddGang`
- `ActionBaBei`

active `game_state` の restore batch に round terminal action が含まれるかは手動 spike で確認する。
`ActionHule`、`ActionNoTile`、`ActionLiuJu` は局遷移設計と同時に追加し、初期化だけの段階では暗黙に
無視しない。特殊 mode 専用 action、未知 action 名、壊れた data、不正 step は推測せず明示的な
失敗にする。

live の mask 解除は v1-develop で確認済みの byte algorithm を Match 固有 pure function として移植
し、synthetic protobuf bytes で固定する。restore の plain bytes に同じ解除を二重適用しない。

## 新規開始と途中復帰の共通 bootstrap

### 必要な情報

callback を開始するには次の情報が必要である。

1. `.lq.FastTest.authGame` 由来の match metadata、seat list、player metadata
2. current round を構築できる `ActionNewRound` から始まる action 列
3. 新規開始または途中復帰のどちらかを確定できる entry evidence

新規開始では 2 を live `.lq.ActionPrototype` から得る。途中復帰では `syncGame` の
`game_restore.actions` から得る。public `MatchEvent` に正規化した後は同じ reducer を使う。

友人戦の新規開始では、`.lq.Lobby.startRoom` の outbound request/response、
`.lq.NotifyRoomGameStart`、`.lq.FastTest.authGame`、`.lq.FastTest.enterGame`、
`ActionMJStart`、`ActionNewRound`、`ActionDiscardTile` の順に観測された。

fresh entry marker は実通信ログで確定する。v1-develop では `.lq.NotifyRoomGameStart` が候補だが、
友人戦の host / guest と tournament のすべてで一度だけ観測され、reload / 途中復帰では観測されない
ことを確認してから固定する。marker を Room / tournament 側が先に消費する場合は、Screen を stale
にして callback から戻る handoff point で、その decoded message を一度だけ `put_back()` する。
Match 側が marker を直接受信した場合と同じ bootstrap 処理を使う。

marker から派生する `MatchEntryHint` は `ScreenContext` に追加しない。hint を生成するにも同じ marker
判定が必要で、元 message の direction、時刻、match ID などの根拠を失うためである。単一の marker
を実通信で確定できない場合に限り、複数 message から導出する one-shot transition handoff を再検討
する。restore 用 `syncGame` は recovery entry evidence とし、public な `restore` flag は設けない。

### bootstrap accumulator

`before_callback()` はマウスカーソルを退避した後、内部 bootstrapper で既存の
`SnifferMessageSource` を到着順に読む。public な `restore` 引数は持たない。

bootstrapper は一時的に次を保持する。

- authGame 由来の metadata
- direct または `put_back()` された fresh entry marker 由来の candidate match ID
- metadata より先に到着した normalized event または restore event batch
- fresh / recovery の entry evidence

auth と action source の到着順は固定しない。action が先なら bounded な初期化用 buffer に保持し、
auth と entry kind が揃ってから apply する。candidate match ID がある場合は authGame の match ID
と一致することを検証する。entry kind が未確定の段階で、buffer 内の live `ActionNewRound` だけを
根拠に fresh 初期化を完了しない。以前の Room terminal state は reload 後も残り得るため、fresh
evidence として再利用しない。

entry kind は内部 enum `UNKNOWN` / `FRESH` / `RECOVERY` として一方向にだけ遷移させる。fresh marker
と restore 用 `syncGame` の両方を同じ bootstrap generation で観測した場合、後着側へ切り替えず
不整合にする。identical な authGame の再送は idempotent に扱えるが、match ID、seat、player、origin
が異なる再送は失敗にする。

`before_callback()` はマウス退避後、まず蓄積済み message を drain し、不足分を framework-owned な
5 秒の初期化期限内で await する。この期限は public 引数にしない。期限切れは画面検出失敗ではなく、
Match 画面に必要な authoritative state が届かなかった `ScreenInconsistentMessageError` とし、
screenshot を付ける。source failure と cancellation は変換しない。

auth 前に保持する live action、restore batch、step reorder の各件数は最大 1024 とする。これは現在の
Sniffer queue capacity と揃え、drain によって別の無制限 buffer を作らないための resource limit で
ある。上限超過は action を捨てず不整合として失敗する。

```text
decoded Sniffer message
  -> bootstrap message classifier
       -> authGame --------------------> metadata decoder
       -> live ActionPrototype --------> live event adapter ----+
       -> syncGame.game_restore.actions -> restore event adapter +-> event reducer
       -> known non-state message ------> consume / safe log
```

entry kind、metadata、active round snapshot のすべてが構築できた時点で `before_callback()` を
完了する。`finishSyncGame` だけを state 初期化条件にはしない。

| message | bootstrap での扱い |
|---|---|
| `.lq.NotifyRoomGameStart` | fresh entry marker の候補。実通信確認までは確定しない |
| `.lq.FastTest.authGame` | match metadata、self seat、players を構築する |
| `.lq.ActionPrototype` | live action 1 件へ decode する |
| `.lq.FastTest.syncGame` | recovery entry evidence と restore action batch へ decode する |
| `.lq.FastTest.finishSyncGame` | state を変更しない同期 marker とする |
| Room / tournament の既知 terminal message | entry noise として必要な範囲だけ消費する |
| heartbeat 等の既知 common message | state を変更せず安全な level でログする |
| 未知または矛盾した message | screenshot 付き不整合エラーにする |

新規開始と復帰で別々の初期化 loop を作らない。違いは action adapter と、restore batch から再構築
した event を完成 snapshot の履歴には含めるが、新着 transition として通知しないことだけに限定する。

recovery entry では `syncGame` の snapshot を authoritative とする。reload 前から queue に残って
いた live action や、restore 完了前に観測した live action を初期 snapshot の代用にしない。
restore 完了後は、snapshot の次 step 以降と検証できる live action だけを通常処理へ渡す。これに
より、reload 中に対局が進行していても `syncGame` 時点の current round から再開できる。

restore 用 `.lq.FastTest.syncGame` は outbound request / response、request `round_id == "-1"`、
`step == 1000000`、response `is_end == false`、`game_restore.game_state == 1` を要求する。
`response.step` は action 件数と一致し、action step は 0 から `response.step - 1` まで連続しなければ
ならない。これらの sentinel と `game_state` の意味は実ログで再確認してから定数化する。
`finishSyncGame` は既知 marker として消費するが、state 構築に必要な authGame と syncGame が揃った後の
必須完了条件にはしない。

## reducer と局遷移

reducer は concrete `MatchEvent` class ごとの純粋な状態遷移を担い、次の immutable state を
返す。適用した同じ event object を `RoundState.events` の末尾へ追加するため、state 更新用 action と
公開履歴を二重に model 化しない。current state と event 列の再構築に必要な event を 1 種類ずつ
TDD で追加する。

各局の action sequence は step 0 から始める。試合開始時だけ `ActionMJStart` が step 0 に入り、
最初の `ActionNewRound` が step 1 になる場合がある。sequence validator と reducer は step 0 の
`StartMatchEvent` を temporary prelude に適用し、step 1 の `NewRoundEvent` で最初の `RoundState` を作る
ときに両 event を保存する。それ以外の `ActionNewRound` は step 0 とし、match metadata を維持した
まま `RoundState` と operation を構築する。current round がある場合は round generation を増やし、
同じ `MatchScreen` を active のままにする。

live action の step が観測順と異なる可能性は v1-develop の知見として残す。round 初期化後の通常処理には
step を key とする bounded reorder buffer が必要であり、期待 step から連続して apply できる action だけを
reducer へ渡す。適用済み step、内容が異なる duplicate、別 round と矛盾する action は失敗にする。
欠けた step を推測したり飛ばしたりせず、呼び出し側 timeout または queue failure に委ねる。

一方、v1-develop には試合開始時の `ActionMJStart` と最初の `ActionNewRound` が逆順で観測された記録はなく、
同実装の初期化経路も両 action を並べ替えていない。この二つについては現時点で reorder buffer の対象に
せず、受信順に step 0、step 1 と検証する。`ActionNewRound` step 1 が先行した場合は不整合として扱い、
実際の観測結果が得られたときに対象範囲を再検討する。

restore batch は step 0 から current step までを検証する。先頭が `ActionMJStart` なら、その次の
step 1 の `ActionNewRound` とともに `StartMatchEvent` を最初の event 列へ保存する。先頭が
`ActionNewRound` なら step 0 から構築する。いずれも対応 action は同じ event adapter と reducer へ
順番に replay し、response の `step`、action 数、各 step の整合性を検証する。局終了 action だけで
current round を初期化しない。

## 対局中の再同期と reload

active callback 中の `syncGame` は途中復帰と同じ restore adapter と replay 処理を使う。既存 state を
部分補正せず、同じ match identity を確認して authoritative な restored snapshot へ置き換える。
version は単調増加させ、callback と `MatchScreen` instance は維持する。

Match 固有の `reload()` override は設けず、generic `Screen.reload()` の stale 契約に従う。callback
利用者は `await screen.reload()` の直後に user data を return し、runtime の Screen 検出へ制御を
戻す。stale になった Screen で処理を継続した場合は、次の Screen API 呼び出しで失敗する。

cookie が有効なら reload 後に `LoginScreen` を経ず、同じ対局の `MatchScreen` が直接検出される。
ただし reload 中にも対局は進むため、新しい `MatchScreen.before_callback()` は fresh entry として
扱わず、`authGame` と restore 用 `syncGame` が揃うまで待つ。`syncGame` の全 action を同じ reducer
へ replay して current state を構築した後、新しい Match callback invocation を開始する。

cookie が無効、session が切断済みなどの理由で `LoginScreen` を経る場合も、ログイン完了後に
検出された `MatchScreen` が同じ recovery bootstrap を使う。したがって、直接 Match に戻る経路と
再ログイン経路で state 復元処理を分けない。

```text
Match callback
  -> await Screen.reload()
  -> current MatchScreen が stale
  -> callback が user data を return
  -> runtime が LoginScreen または MatchScreen を検出
  -> 新しい MatchScreen.before_callback()
       -> authGame + syncGame を同じ recovery bootstrap で replay
  -> 新しい Match callback invocation
```

## message source と並行性

RoomScreen と同様、常駐 Sniffer client task が decoded message を既存 bounded queue へ蓄積し、
`MatchScreen` の API が `get()` / `get_nowait()` で読む。

Match 専用 background reducer は追加しない。background task と操作 API が同じ queue を競合して
読むと response と action の相関が複雑になり、別 mailbox が必要になるためである。callback と
Match API は逐次利用を前提とし、操作と状態待機を同じ message 順序で処理する。

callback は長時間 source を読まずに停止しない。queue overflow、payload budget 超過、publication
gap、decode error は状態を推測せず runtime 全体の失敗として伝播する。

## terminal と次の Screen

実通信で確定した match terminal message により terminal snapshot へ遷移する。結果 UI の確認と
Room / tournament / Home への遷移が完了するまでは、必要な Match API を同じ instance で処理できる
よう直ちに stale にしない。

次の Screen に属する message を先読みした場合は 1 回だけ `put_back()` し、画面遷移を確認して
から stale にする。terminal 後に新しい match の auth/action を観測しても、同じ instance を
暗黙に別試合へ転用しない。

友人戦の対局終了後に `.lq.Lobby.fetchRoom` response を観測した場合は、Room へ戻るための
authoritative な完全 snapshot として 1 回だけ `put_back()` する。runtime が新しく検出した
`RoomScreen` はこの response から instance-local store を初期化する。以前の RoomScreen instance
や terminal snapshot は引き継がない。

## 整合性と失敗モデル

少なくとも次を検証する。

- authGame、syncGame、ActionPrototype の direction と Req/Res 種別
- match ID が空でなく、同じ instance 内で変化しないこと
- self account ID が seat list に一度だけ存在すること
- player 数と seat 数が 3 または 4 で一致すること
- human player account ID が重複しないこと。robot ID は human account ID と別に扱うこと
- `seat_list` の CPU 表現と `robots` の対応が、実通信で確認した規則に一致すること
- restore batch が任意の `ActionMJStart` と `ActionNewRound` から current step まで連続すること
- current round の live step が欠落、重複、巻き戻りしないこと
- action data が schema と state 不変条件を満たすこと
- syncGame が active state と同じ match identity を表すこと

field 欠落、型不正、矛盾は screenshot 付き Match inconsistent message error とする。nested protobuf
decode、Sniffer transport、stream gap は元の infrastructure error を伝播する。未知 action を
無視したり、画面から state を推測したり、自動 reload で成功に見せたりしない。

## ログと秘密情報

- 公開 API の info log は Screen 名と API 名など秘密でない構造情報に限定する。
- Sniffer 調査ログは decoded message を Screen が選んだ level へ出す既存の例外に従う。
  `ActionPrototype` は難読化された `data` を protobuf decode 済みの辞書へ差し替えて info log に出す。
- Sniffer 調査ログを docs、fixture、sample、chat、commit へ転記しない。
- 自動テストは synthetic decoded message、synthetic nested protobuf、fake browser だけを使う。

## module 配置

初期化実装は次の責務で配置する。bootstrap loop を早期に汎用 framework へ抽象化しない。

- `screens/match/state.py`: public immutable state と invariant
- `screens/match/event/_base.py`: event 共通の action step と不変条件
- `screens/match/event/<event>.py`: concrete event ごとの final frozen dataclass と `from_dict()`
- `screens/match/event/__init__.py`: concrete event と明示的な `MatchEvent` union の export
- `screens/match/_action.py`: live unmask、restore adapter、nested decode、event decoder registry
- `screens/match/store.py`: metadata、step、round reducer、temporary replay と atomic commit
- `screens/match/screen.py`: message classifier、初期化期限、Screen error への変換、`get_state()`
- `screens/match/__init__.py`: `MatchScreen`、public state 型、public event 型だけを export

decode / transition の pure error は `ValueError` 派生の内部型とし、`screen.py` の境界で screenshot 付き
`ScreenInconsistentMessageError` または `ScreenUnexpectedStateError` へ変換する。Sniffer transport、
outer protobuf decode、queue overflow、cancellation は元の infrastructure error を伝播する。

## 実装前の手動 spike

初期化実装を始める前に、合意済みの対局で次を確認する。payload 値は文書、fixture、chat、commit へ
貼らず、API 名、field の意味、順序という設計結果だけを反映する。

1. 友人戦 host / guest と tournament の fresh 開始で共通する entry marker と message 順序。
2. cookie が残る Match reload と Login を経る途中復帰で、marker が再送されず restore 用
   `authGame` / `syncGame` が届くこと。
3. `ReqSyncGame.round_id == "-1"`、`step == 1000000`、`game_restore.game_state == 1`、
   `response.step == len(actions)` の意味。
4. 三人戦でも `seat_list`、`players`、`robots` と participant ID の関係が四人戦と同じであること。
   四人戦では `seat_list` に human / CPU の全 ID が seat 順で入り、CPU ID が `robots` と対応することを
   確認済み。
5. tournament の `game_config.meta.room_id`、`mode_id`、`contest_uid`、`category` の対応。
   友人戦の `room_id > 0`、`mode_id == 0`、`contest_uid == 0` は確認済み。両 ID が 0 の match が
   open match であるという推測も、必要なら分類 field と合わせて確認する。
6. standard mode と未対応特殊 mode を識別する `game_config.mode` / `detail_rule` field。
7. dealer / non-dealer の `ActionNewRound.tiles` が 13 / 14 枚になる条件。
   `dora` / `doras` と optional `operation` の実際の presence も確認する。
8. fresh と局途中 restore の action 名一覧。active restore batch に round terminal action が含まれるか。
9. `ActionPrototype` の局内 step、次局での reset、実際に観測順が前後する範囲。
10. fresh / direct reload / Login recovery の bootstrap 中に現れる state 非関連 API 名。v1 の common
    message allowlist を一括移植せず、観測済み message だけを分類する。

実通信ログは一時ログだけに置き、コミットしない。

## TDD と実装順

1. 実装前の手動 spike を完了し、fresh marker、origin、CPU、restore sentinel を固定する。
2. public immutable state、final frozen event dataclass、段位を含む authGame / ActionNewRound の strict decode。
3. 明示的 `MatchEvent` union、runtime validator、nested action の live / restore decoder と 1 対 1 変換。
4. standard active-round event reducer、event 列、step / round generation の不変条件。
5. temporary store への restore replay と atomic publish。
6. bootstrapper の fresh / recovery 経路。
7. `MatchScreen.before_callback()` と `get_state()` への接続。
8. 同一 instance での次局 `ActionNewRound`。
9. active 中の `syncGame` 再同期。
10. generic reload 後の Screen 再検出と recovery bootstrap。
11. 状態待機と操作 API を 1 種類ずつ追加する。

各段階で synthetic data の自動テストを完了し、高レベル API は 1 つずつ実ゲーム確認する。
実 payload はテストや文書へ保存しない。

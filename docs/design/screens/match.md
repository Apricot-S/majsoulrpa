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
    seat: Seat
    account_id: int
    name: str
    level4: MatchRank
    level3: MatchRank

    @property
    def is_cpu(self) -> bool: ...


@final
@dataclass(frozen=True, slots=True)
class Dapai:
    tile: Tile
    moqie: bool
    liqi: bool
    wliqi: bool


@final
@dataclass(frozen=True, slots=True)
class Chi:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Peng:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Daminggang:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Angang:
    consumed: tuple[Tile, Tile, Tile, Tile]


@final
@dataclass(frozen=True, slots=True)
class Jiagang:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    added: Tile


@final
@dataclass(frozen=True, slots=True)
class Babei:
    moqie: bool


type Fulu = Chi | Peng | Daminggang | Angang | Jiagang


@dataclass(frozen=True, slots=True)
class RoundState:
    generation: int
    step: int
    chang: int
    ju: Seat
    ben: int
    liqibang: int
    dora_indicators: tuple[Tile, ...]
    left_tile_count: int
    scores: tuple[int, ...]
    shoupai: tuple[Tile, ...]
    zimopai: Tile | None
    he: tuple[tuple[Dapai, ...], ...]
    fulu: tuple[tuple[Fulu, ...], ...]
    babei: tuple[tuple[Babei, ...], ...]
    liqi: tuple[bool, ...]
    wliqi: tuple[bool, ...]
    first_draw: tuple[bool, ...]
    yifa: tuple[bool, ...]
    lingshang_zimo: tuple[bool, ...]
    pending_action_target: tuple[Seat, Tile] | None
    operation_candidates: OperationCandidates | None
    events: tuple[MatchEvent, ...]


@dataclass(frozen=True, slots=True)
class MatchState:
    version: int
    match_id: str
    origin: MatchOrigin
    origin_id: int
    self_seat: Seat
    players: tuple[MatchPlayer, ...]
    round: RoundState
```

`Fulu` は kind discriminator を持たず、具体 class の Union とする。利用者は class pattern で型を
絞り込み、各副露に存在しない field を `None` として分岐する必要がない。`Chi`、`Peng`、
`Daminggang` は取得元と取得牌を、`Jiagang` はさらに元の `Peng` の取得情報と追加牌を区別して保持する。
これは Event 列の単純な複製ではなく、Event を適用して得られる現在の副露状態である。北抜きは面子の
Union には含めず、seat ごとの `tuple[Babei, ...]` として `RoundState.babei` に保持する。`Babei` は
`ActionBaBei.moqie` を保持するが、北牌は常に `4z` なので tile field は持たない。

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

match 内の seat index と牌は、それぞれ `Seat = NewType("Seat", int)`、
`Tile = NewType("Tile", str)` で意味を区別する。JSON / protobuf などの外部入力境界で
`validate_seat()` / `validate_tile()` を一度だけ通し、検証済みの戻り値を Event、State、Store、
operation へ渡す。内部処理は `Seat` / `Tile` を受け取るため、同じ値域・牌形式の検証を各 model や
reducer で繰り返さない。`NewType` 自体には runtime validation がないため、生の `int` / `str` を
直接 `Seat()` / `Tile()` で包む処理は decoder 境界に置かず、必ず共通 validator を使用する。

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

### operation 候補

operation は発生済みの event ではなく、その event を適用した直後に自家が選択できる行動候補である。
`ActionNewRound`、`ActionDealTile`、`ActionDiscardTile`、副露や槓に対応する action のいずれにも
`OptionalOperationList` が付随し得るため、event class ごとに decode せず共通 decoder で正規化する。
各 event を reduce するたびに以前の候補を置き換え、field がない場合と `operation_list` が空の場合は
どちらも `None` とする。restore replay でも action ごとに置き換えるため、完成 snapshot には最後の
action の候補だけが残る。

公開 operation は `@final`、`frozen=True`、`slots=True`、`kw_only=True` の dataclass とし、数値の
`type` discriminator は公開しない。`MatchOperation` は全 concrete class を列挙する明示的 union とし、
利用者は event と同様に class pattern で型を絞り込む。protobuf の `combination` 文字列は decoder
境界で牌 tuple へ変換し、raw string や mutable list を公開 model に保持しない。

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiOperation:
    tile: Tile
    moqie: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class ChiOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@dataclass(frozen=True, slots=True, kw_only=True)
class PengOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]


@dataclass(frozen=True, slots=True, kw_only=True)
class AngangOperation:
    consumed: tuple[Tile, Tile, Tile, Tile]


@dataclass(frozen=True, slots=True, kw_only=True)
class DaminggangOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile, Tile]


@dataclass(frozen=True, slots=True, kw_only=True)
class JiagangOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    added: Tile


@dataclass(frozen=True, slots=True, kw_only=True)
class LiqiOperation:
    tile: Tile
    moqie: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class ZimohuOperation:
    tile: Tile


@dataclass(frozen=True, slots=True, kw_only=True)
class RongOperation:
    from_seat: Seat
    tile: Tile


@dataclass(frozen=True, slots=True, kw_only=True)
class LiujuOperation: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class BabeiOperation:
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class SkipOperation: ...


type MatchOperation = (
    DapaiOperation
    | ChiOperation
    | PengOperation
    | AngangOperation
    | DaminggangOperation
    | JiagangOperation
    | LiqiOperation
    | ZimohuOperation
    | RongOperation
    | LiujuOperation
    | BabeiOperation
    | SkipOperation
)


@dataclass(frozen=True, slots=True, kw_only=True)
class OperationCandidates:
    time_fixed_ms: int
    time_add_ms: int
    operations: tuple[MatchOperation, ...]
```

live action の singular `operation` は受信者である自家用なので、`OptionalOperationList.seat` が示す
actor seat は各公開 operation model に重複して保持しない。実行主体は現在の `MatchScreen` と
`OperationCandidates` によって自家へ固定される。restore / record にある複数人分の `operations` を
扱う段階では、actor seat 付きの container を別途設計する。`OperationCandidates.operations` は非空、
時間は非負の millisecond として検証する。

一方、チー、ポン、大明槓、ロンの `from_seat` は牌の取得元となる seat を確定する値なので公開 operation に
含める。`from_seat` と `tile` は直前の Event から materializer が同時に補い、利用者が
`pending_action_target` を参照して候補を完成させる必要をなくす。これは actor の
`self_seat` とは役割が異なる。利用者が operation instance を自作した場合も、将来の operate API が
現在の候補への包含を検証することで、対象 seat または対象牌が異なる instance を拒否する。
`RoundState.operation_candidates` は候補がないときだけ `None` とし、
`has_pending_operation` は設けない。候補の有無は `operation_candidates is None` または
`operation_candidates is not None` で直接判定し、同じ状態を表す API を重複させない。

type と concrete class の対応は次のとおりとする。

| type | public class | `combination` の意味 |
|---:|---|---|
| 1 | `DapaiOperation` | 鳴き後の食い替えで禁止される打牌。通常は空配列。現在の手牌から選択可能な打牌へ展開する |
| 2 | `ChiOperation` | 手牌 2 枚を `|` で区切った組合せ。対象 seat・牌は Event から補う |
| 3 | `PengOperation` | 手牌 2 枚を `|` で区切った組合せ。対象 seat・牌は Event から補う |
| 4 | `AngangOperation` | 消費する対象牌 4 枚を `|` で区切った組合せ |
| 5 | `DaminggangOperation` | 手牌 3 枚を `|` で区切った組合せ。対象 seat・牌は Event から補う |
| 6 | `JiagangOperation` | 既存のポン牌 3 枚と加える牌 1 枚を `|` で区切った組合せ。並び順に意味は持たせない |
| 7 | `LiqiOperation` | 立直宣言牌の候補。各要素は単独の牌で、手出し／ツモ切りの選択肢へ展開する |
| 8 | `ZimohuOperation` | 空配列。和了対象のツモ牌は Event から補う |
| 9 | `RongOperation` | 空配列。和了対象 seat・牌は Event から補う |
| 10 | `LiujuOperation` | 空配列。現時点では九種九牌だけを表す |
| 11 | `BabeiOperation` | 空配列。v1-develop の対応であり実通信で再確認する |

`LiujuOperation` は画面の「流局」ボタンに対応する。現時点で type 10 が表す選択可能な流局は
九種九牌だけであり、親の配牌直後または自家ツモ直後に、`Fulu` がなく、手牌とツモ牌に
么九牌が9種類以上ある場合だけ生成する。第一ツモかどうかは operation message を提示する
サーバーと、成立後の `LiujuEvent` を適用する reducer の双方で保証する。
`operate()` は共通の行動ボタン領域から `liuju.png` を待ってクリックする。流局では牌を
消費しないため、クリック後の手牌スライド待機は行わない。自家の九種九牌を表す
`LiujuEvent` だけを操作の完了として扱い、他の流局種別では完了させない。

`BabeiOperation` は親の14枚配牌または自家ツモの直後に、手牌か表示上のツモ牌へ `4z` が存在する場合
だけ生成する。雀魂の画面では両方に北がある場合も抜く物理牌を選択できず自動的に決まるため、
Operation には `moqie` を持たせない。実際に手牌とツモ牌のどちらから抜かれたかは、後続の
`BabeiEvent.moqie` に記録する。
操作時は `button-area.toml` の search region から `babei.png` を待ってクリックする。
クリック後は手牌のスライド完了を1.5秒待ち、物理牌を選択する追加操作は行わない。

type 1 の `combination` は選択可能な牌ではなく、食い替えによる禁止牌である。Event 適用後の
`shoupai` と実際の `zimopai` から禁止牌を除いた打牌を列挙し、牌 1 種類と
`moqie` 1 値の組を `DapaiOperation` 1 instance として公開する。同じ牌が手牌とツモ牌の両方に
存在して手出しとツモ切りを選べる場合は、`moqie=False` と `moqie=True` の 2 instance にする。
同じ `tile` / `moqie` の物理牌が複数ある場合は同じ操作なので 1 instance に正規化する。

雀魂の食い替え禁止牌には赤五牌に関する欠落がある。`5m`、`5p`、`5s` のいずれかが禁止されても、
対応する `0m`、`0p`、`0s` が `combination` に含まれない場合がある。type 1 の変換時は通常五が
禁止されていれば対応する赤五も追加で禁止し、選択可能な `DapaiOperation` を生成しない。この
workaround は Kanachan の `src/annotation/annotation.cpp` に残された知見と実通信確認に基づく。

type 2〜6 の各 encoded combination は表の枚数と完全に一致させ、各要素を通常の牌表現として検証する。
protobuf の `combination` 1 要素を public operation 1 instance へ展開し、牌組の候補一覧を単一
operation の中に保持しない。したがって、複数の鳴き方を選べる場合は `ChiOperation` などが候補数分
並ぶ。チー、ポン、大明槓では `combination` から手牌側の `consumed` を生成し、候補が付随した
`DapaiEvent` の牌を `tile`、seat を `from_seat` として補う。各 instance は取得元の seat、取得する河の牌、
手牌から消費する 1 組を持ち、それ自体で副露の選択内容を完全に表す。赤牌と通常牌は別の牌として
保持し、`tile` も `DapaiEvent.tile` の表現を変更しない。`ChiOperation` は四麻で自家の上家による
`DapaiEvent` にだけ生成し、各 `consumed` が現在の `shoupai` に実在して、取得牌と合わせて順子に
なることを検証する。`PengOperation` は三麻・四麻とも任意の他家による `DapaiEvent` から生成し、
取得牌と `consumed` が同じ牌種で、各 `consumed` が現在の `shoupai` に実在することを検証する。
`DaminggangOperation` も三麻・四麻とも任意の他家による `DapaiEvent` から生成し、同じ検証を
手牌側の3枚に対して行う。赤5と黒5は同じ牌種として扱うが、各候補には wire の赤牌表現を
そのまま保持する。

暗槓は4枚すべてを `AngangOperation.consumed` とし、各 combination の牌順と候補順を wire のまま
保持する。候補は親の `ActionNewRound` または自家の `ActionDealTile` にだけ生成し、4枚すべてが
現在の `shoupai` と `zimopai` を合わせた実牌に存在することを要求する。親の14枚配牌で表示上
分離された `zimopai` も手牌として消費牌の検証に含める。

加槓候補の `combination` は、実牌譜では
既存のポンと追加牌の区別によらず赤5が先頭に正規化されており、4枚目を追加牌として扱えない。
4枚の multiset に牌構成が包含される自家の `Peng` を現在の `RoundState.fulu` から一意に特定し、その
`from_seat`、他家から取得した `tile`、手牌から使った2枚の `consumed` を `JiagangOperation` に
引き継ぐ。既存のポン3枚を multiset として差し引いた残りの1枚を `added` とし、通常牌か赤牌かを
区別する。対応する `Peng` が存在しない、一意に定まらない、または差分が1枚にならない場合は
不整合として拒否する。候補は自家の `ActionDealTile` にだけ生成し、`added` が現在の `shoupai`
または `zimopai` に実在することを要求する。4組のfuluがあっても、既存の `Peng` を置換するため
許容する。複数候補は `combination` の wire 順を維持する。
加槓成立時の `ActionAnGangAddGang` (`type == 2`) は `tiles` に追加牌
1枚を直接格納するため、Event の追加牌はこの値から取得する。調査根拠は
[`加槓候補の牌順序`](../../investigations/jiagang-combination-order.md) に記録する。

この復元に必要な既存ポンを失わないよう、store は operation 候補のmaterializerへ、候補生成時点の
`round_state.fulu[state.self_seat]` を `fulu` として渡す。`fulu` は `zimopai` の直後に置く必須引数と
し、局初期化時だけは副露が存在しないため
空tupleを渡す。副露Eventの適用と同じactionに後続operationが含まれる場合は、Eventを反映した後の
自家fuluを渡す。materializerへMatchState全体は渡さず、候補生成に必要な自家副露だけに境界を絞る。

自家fuluは加槓の復元以外の不整合検出にも利用する。新しいチー・ポン・大明槓・暗槓は、自家fuluが
すでに4組なら生成しない。ただし加槓は既存のポンを置き換えて副露数を増やさないため許容する。
立直は自家fuluが空、または暗槓だけで構成される場合に限って許容する。これらはoperationごとに
テストを追加してからmaterializerへ実装する。
type 7 は `|` で分割せず、各要素を立直宣言牌として検証する。候補牌ごとに現在の `shoupai` から
`moqie=False`、実際の `zimopai` から `moqie=True` の `LiqiOperation` を生成する。同じ牌について
両方を選べる場合は 2 instance とする。

雀魂の立直候補にも赤五牌に関する欠落がある。`0m`、`0p`、`0s` のいずれかを切って立直できる
場合、対応する `5m`、`5p`、`5s` が type 7 の `combination` に含まれないことがある。変換時は
赤五が候補なら対応する通常五も候補牌として補い、現在の `shoupai` と `zimopai` に実在する牌から
`LiqiOperation` を生成する。対応する通常五が実在しなければ候補を追加しない。通常五だけが候補の
場合に赤五を補う逆方向の推測も行わない。この workaround は Kanachan の
`src/annotation/annotation.cpp` に残された知見に基づく。

type 8 の `ZimohuOperation.tile` は候補を発生させた
`ActionDealTile` のツモ牌、または `ActionNewRound` の天和判定に使う牌から補う。
`ActionNewRound` の天和候補では、表示のため分離した `zimopai` を `ZimohuOperation.tile` として使う。
これは和了 operation の対象牌を確定するための規約であり、同じ牌の打牌 operation を
`moqie=True` に変更するものではない。type 9 の `RongOperation.tile` と `from_seat` は放銃牌と放銃者、
搶槓対象牌と槓または北抜きを行った player など、候補を発生させた `DapaiEvent`、
`AngangEvent`、`JiagangEvent`、`BabeiEvent` から補う。対象 seat が自家の場合や、自家の未解決な
ツモ牌がある場合は不整合とする。
いずれも赤牌を通常牌へ正規化しない。type 8〜11 は `combination` が空でなければ不整合とする。
未知 type は将来の候補として黙って保持せず decode error にする。`seat`、`change_tiles`、
`change_tile_states`、`gap_type` および unknown protobuf field は今回の標準 operation model には
取り込まず、既知 field の独自 whitelist 検査も追加しない。

operation 型を段階的に追加している間は、まだ public model を実装していない type も decode error に
する。対応済み type だけを部分的な `OperationCandidates` として公開してはならない。各 milestone で
decoder の対応 type と public `MatchOperation` union を同時に増やす。

operation の変換は 2 段階に分ける。action adapter は `OptionalOperationList` の decoded dict を
live / restore 共通の immutable な内部 specification へ decode する。store は Event を適用した後の
手牌状態と適用した Event を使って、その specification を public `OperationCandidates | None` へ
展開する。type 1 と type 7 は action decode 時点では選択可能な手出し／ツモ切りを確定できず、
type 2、3、5 は取得する直前の打牌とその seat を確定できないため、いずれも public operation へ直接 decode
しない。operation を event field に含めたり、同じ action を event と operation event の 2 件へ
分割したりしない。操作を送信する browser API は operation model と decoder の実装範囲に含めず、
候補を state へ接続した後に 1 API ずつ設計する。

operate API は `OperationCandidates.operations` から選んだ concrete operation instance を
引数として受け取る。各 instance は追加の候補 index や牌組引数を要求せず、それ自体で選択内容を
完全に表す。副露・ロン operation も対象 seat、取得牌または和了対象牌、消費牌を instance 内に持ち、
呼び出し側が直前の河や `RoundState.pending_action_target` を参照して補完する必要はない。API は渡された
instance が現在の候補に含まれることを確認してから画面操作へ変換する。

親の `ActionNewRound.tiles` 14 枚はすべて配牌であり、表示の都合で右端の 1 枚を `zimopai` field に
分離していても実ツモ牌ではない。`ActionNewRound` に付随する type 1 / type 7 を展開するときは
14 枚すべてを `moqie=False` の手出し候補とし、`moqie=True` へ変換しない。ツモ牌位置の click が
必要かどうかは後続の operate API が画面上の配置へ変換する責務であり、operation の意味を変更しない。

### 打牌操作 API

`await screen.operate(operation)` は呼出時点までに蓄積された message を先に reduce し、更新後の
`RoundState.operation_candidates` に渡された operation が含まれることを検証する。候補がない場合は
`ScreenInvalidOperationError`、候補に含まれない instance は `ScreenInvalidArgumentError` とする。
利用者が候補と等しい instance を自作して渡すことは許容する。最初の milestone では
`DapaiOperation` だけを実行し、対応する自家の `DapaiEvent` を適用した後の `MatchState` を返す。

`moqie=False` は現在の `shoupai` にある同種牌の先頭をクリックし、`moqie=True` は分離表示された
実際の `zimopai` をクリックする。ただし親の初打で分離表示された14枚目を選んだ場合だけ、
operation の意味を変えずにツモ牌位置のクリックへ変換する。同じ牌が残り13枚にもある場合も、
分離表示された牌を優先してよい。親の配牌演出中の誤クリックを避けるため、初打では
v1-develop と同じ待機を入れる。

通常打牌では、候補を含む `ActionPrototype` の `observed_at` から0.4秒後をUI準備時刻とする。
`operate()` はクリック直前に準備時刻までの残り時間だけ待つ。AIの思考や利用者側の処理によって
すでに0.4秒以上経過していれば追加で待たない。この観測時刻は操作タイミングのために
`MatchScreen` 内部でだけ保持し、public `MatchEvent` や `MatchState` には追加しない。UIの描画が
0.4秒より遅れた場合は、後述するクリック再試行で補う。

通常の browser `click()` が対象座標への cursor 移動と hover 待機を行うため、Screen 側では
いずれも重複して実行しない。クリック後は `MOUSE_SAFE_REGION` へ退避する。その後も Sniffer
message を通常どおり log・reduce し、自家の
`DapaiEvent` の `tile` / `moqie` が指定した operation と一致した時点で完了する。先に別の state event
が適用された場合や、自家の打牌内容が一致しない場合は authoritative state を保持したまま
`ScreenInconsistentMessageError` とする。API 自体には timeout 引数を設けず、必要なら呼出側が
`asyncio.timeout()` で期限を管理する。

#### 立直操作

`LiqiOperation` は `button-area.toml` の search region 内で `liqi.png` を検出して立直ボタンを
クリックする。operation message がUI描画より先に届くため、ボタンを検出できるか、後続の
`ActionPrototype` によって選択権の消滅を確認するまで検出を繰り返す。ボタンをクリックした後は
立直打牌候補の表示を0.4秒待ち、もう一度queueを確認してから `tile` / `moqie` に対応する牌領域を
クリックする。待機中に後続actionを先読みした場合は、そのmessageを1回だけ `put_back()` し、
古くなった牌領域をクリックしない。

牌領域の決定とクリック再試行は `DapaiOperation` と共通にする。自家の `DapaiEvent` が指定した
`tile` / `moqie` と一致し、`liqi` または `wliqi` が真であることを完了条件とする。これにより通常の
立直とダブル立直を同じ `LiqiOperation` で扱い、立直を伴わない同一打牌を成功扱いしない。

#### 自摸和・ロン操作

`ZimohuOperation` と `RongOperation` は和了ボタンを直接探さず、基準 viewport 上の
自動和了トグルをオンにする。領域は四人麻雀では
`Region(left=18, top=590, width=42, height=42)`、三人麻雀では
`Region(left=18, top=558, width=42, height=42)` とする。
和了判断を遅らせないため `warp=True` で直ちにクリックし、ボタン描画待ちや手牌スライド待機は
追加しない。その後は通常の message pipeline で、自家の `hu_tile` が指定した `tile` と一致する
`HuleEvent` まで reduce して更新後の `MatchState` を返す。ロンではダブロン・トリロンの
`hules` に自家のロンが含まれていれば完了とする。

自動和了トグルは次局へ入ると雀魂側でオフへ戻るため、和了成立後に framework から再度クリックして
オフへ戻す cleanup は行わない。

#### 打牌・立直打牌のクリック再試行

`DapaiOperation` と `LiqiOperation` は、対象牌を1回クリックしただけで入力済みとみなしてはならない。
WebSocket message がUI描画より先に届くことがあり、候補を生成したmessageを処理できた時点でも、
画面上の手牌がまだクリックに反応しない場合があるためである。v1-develop と同様に、入力の進行を
確認できるまで同じ領域のクリックを繰り返す。

再試行中も Sniffer message を別経路で消費しない。heartbeatなどの既知common messageは通常どおり
log・処理するが、その受信を理由に直ちに再clickしない。各clickから0.5秒を次のclickまでの最小間隔とし、
その間もmessageの処理を続ける。v1-developの再試行helperは、操作またはstate進行の境界となる
`.lq.FastTest.inputOperation`、`.lq.FastTest.inputChiPengGang`、`.lq.ActionPrototype` だけを先読みの
終了条件とし、取得したmessageをqueueへ `put_back()` して後続の通常pipelineに一度だけ処理させて
いた。今回も同じ所有権規則を使い、Dapai / Liqi の進行確認に関係するmessageだけを `put_back()`
する。未知messageを成功扱いで捨てたり、state eventを再試行loop内だけで消費したりしない。

#### 手牌クリック領域の根拠

1920 × 1080 の基準 viewport では、左端の牌を端まで含む領域を
`[left=224, top=922, width=89, height=149]` とし、隣の牌までの水平間隔を `94.91` とした。13枚の
各 left は次の計算結果になる。

```pycon
>>> left = 224
>>> for i in range(13):
...     print(left + i * 94.91)
...
224.0
318.90999999999997
413.82
508.73
603.64
698.55
793.46
888.37
983.28
1078.19
1173.1
1268.01
1362.92
```

牌の端では隣の牌へ触れる可能性があるため、左右をそれぞれ10%除外して中央80%を使う。上端も10%
除外し、下側はクリックの安定性を優先して30%除外するため、高さは70%とする。左端の牌に対する
計算結果は次のとおりである。

```pycon
>>> edge_region = [224, 922, 89, 149]
>>> region = [0] * 4
>>> region[0] = edge_region[0] + edge_region[2] * 0.1
>>> region[1] = edge_region[1] + edge_region[3] * 0.1
>>> region[2] = edge_region[2] * 0.8
>>> region[3] = edge_region[3] * 0.7
>>> region
[232.9, 936.9, 71.2, 104.3]
```

実装では v1-develop と同じく各計算段階で `int()` により切り捨てる。そのため基準領域は
`Region(left=232, top=936, width=71, height=104)`、index `i` の left は
`232 + int(i * 94.91)` となる。この段階的な切り捨ては、最後に `232.9 + i * 94.91` 全体を
切り捨てる計算とは一致しない場合がある。

分離表示されたツモ牌は v1-develop で使われていた、手牌枚数 1、4、7、10、13 に対する left
`348`、`633`、`918`、`1203`、`1487` を基準とする。同じ内側補正を適用した
`356`、`641`、`926`、`1211`、`1495` を `ZIMOPAI_REGIONS` の left とし、top、width、height は
手牌クリック領域と共通にする。

### チー・ポン・大明槓操作

チー・ポン・大明槓buttonは同時に提示されるoperationの組合せによって配置が変わる。`chi.png`、
`peng.png`、`gang.png` は150×38で、`button-area.toml` の `region` も左上を基準とした同じ150×38とする。
既存のtemplate matcherでは `margin` も含めた領域が探索範囲になるため、rightを670、bottomを252
として、画面上の `left=630, top=600, width=820, height=290` 全体を探索する。専用のmatcher APIは
追加せず、通常の `load_png_template_matcher()` を使用する。検出結果のregionは実際に見つかった
buttonの150×38なので、その領域をクリックする。描画が通信より遅い場合は、呼び出し側のtimeout
まで検出を繰り返す。

`ChiOperation` または `PengOperation` が1候補なら、対応するbuttonのclickだけで選択が確定する。
チーの2〜5候補、ポンの2候補では、公開候補tuple中の同種operationのwire順をUIの左からの順序として
用いる。v1-developで確認された選択領域は `top=692, width=157, height=117`、候補間隔200である。
候補数を `n`、0始まりの候補位置を `i` とし、`left = 961 - 100 * n + 200 * i` で選択領域を求める。
button clickから候補表示まで0.4秒待ち、組合せを選択した後は手牌のスライドが終わるまで1.5秒待って、
続く打牌で移動中の牌を誤ってクリックしないようにする。

`DaminggangOperation` は麻雀のルール上1候補だけなので、槓buttonのclickだけで選択を確定し、
組合せ選択領域はクリックしない。候補数が1でなければ画面配置を推測せず不整合とする。button click後は
チー・ポンと同様に手牌のスライド完了を1.5秒待つ。

完了時は自家の `ChiEvent`、`PengEvent` または `DaminggangEvent` の `from_seat`、`tile`、`consumed` が指定operationと
一致することを要求する。buttonの描画待ち中に `ActionPrototype` を先読みした場合は1回だけqueueへ
戻し、通常のevent pipelineで処理する。他家の `PengEvent` が先に成立した場合はチーが上位actionに
preemptされたものとして、operation失敗にはせず更新後のstateを返す。他家だけを和了者とする
`HuleEvent` が成立した場合は、チー・ポン・大明槓がロンにpreemptされたものとして許容する。
自家の和了を含む `HuleEvent` は、要求していない自家操作が成立した不整合としてpreempt扱いしない。
button click後に同じ競合が起きた場合も同様とする。複数候補の
表示待ち中にも組合せ領域をクリックする直前にqueueを確認し、上位actionを先読みしていれば
put-backして、すでに消えた選択UIの座標をクリックしない。上位actionを観測せずbuttonも検出できない
場合は成功扱いせず、検出を続けて呼び出し側のtimeoutに委ねる。

### operation のスキップ

チー、ポン、大明槓、ロンは、候補を選ばず待つだけではスキップできない。frameworkは対応するUIを
明示的に操作する。チー、ポン、大明槓は「鳴きなし」toggleをonにして現在の候補をスキップし、
actionの進行を確認してからoffへ戻して、将来の鳴きを再び許可する。ロンはスキップbuttonを
クリックする。

自家のツモ番に北抜き・暗槓・加槓・ツモ和了が提示された場合、立直の有無で候補の構成と操作を変える。
非立直時は `SkipOperation` を候補へ追加せず、利用者が選んだ `DapaiOperation` の打牌によって
他の候補を暗黙にキャンセルする。雀魂のUIではスキップbuttonでも候補を消せるが、その後に打牌選択が
必要になるため、frameworkの標準操作では使用しない。

立直中に加槓が提示されることはない。北抜き・暗槓・ツモ和了が提示された場合は、ツモ切りの牌を
含めて打牌を選択できないため、ツモ切りを表す `DapaiOperation` を行動候補へ含めず、frameworkが
合成する `SkipOperation` を追加する。利用者は提示された北抜き・暗槓・ツモ和了、または
`SkipOperation` のいずれかを選ぶ。`SkipOperation` を実行したときは
スキップbuttonをクリックして明示的に候補を見送る。

「鳴きなし」toggleとスキップbuttonのclickは判断の遅延を避けるため `warp=True` とし、通常clickの
cursor移動とhover待機を省略する。「鳴きなし」toggleの領域は、四人麻雀では
`(left=18, top=655, width=42, height=42)`、三人麻雀では
`(left=18, top=623, width=42, height=42)` とする。

スキップbuttonは `skip.png` と `skip.toml` で毎回検出し、通常の行動buttonより短い0.2秒間隔で
再検出する。検出に成功した領域を1回だけclickし、推定座標を連打しない。スキップbuttonの位置へ
座標clickを繰り返すと、画面遷移後に表示された自家ツモの選択buttonを誤って消すおそれがあるためで
ある。
実画面での確認結果は
[対局中のスキップボタン押下要否](../../investigations/match-skip-button.md) に記録する。

「鳴きなし」をonにした後のoffへの復帰は必須cleanupとする。通常どおりスキップが成立した場合だけで
なく、別playerの上位actionによってチー・ポン・大明槓の選択またはスキップがpreemptされた場合も、
offへの復帰を完了してからAPIを返す。onのまま処理を中断すると後続の鳴き候補まで自動的に拒否して
しまうため、preemptをoperation失敗にしないこととcleanupの省略を混同しない。offへの復帰を確認
できない場合も、正常完了したようには返さない。

副露候補は、別playerの上位actionによってUIから消えることがある。これはスキップ時だけでなく、
候補を選択した場合にも起こる。ロンはチー、ポン、大明槓より優先され、ポンと大明槓はチーより
優先される。このため、チーの選択・スキップ中に別playerのポン・大明槓・ロンが成立した場合、
およびポン・大明槓の選択・スキップ中にロンが成立した場合は、要求したoperationの失敗として
扱わない。対応する `ActionChiPengGang` または `ActionHule` を先読みした場合はqueueへ
`put_back()` し、通常のevent decode・reduceでauthoritative stateを進める。上位actionを確認できない
ままbuttonが見つからない、または消えた場合まで黙って成功扱いにはしない。

ロンのスキップは上位actionによってpreemptされない。ダブロン・トリロンが可能な状況でも、雀魂は
自家がロンまたはスキップを選ぶまで待つ。したがって、別playerの `ActionHule` を理由に自家の
ロンスキップを暗黙に成功扱いするfallbackは設けず、明示的なスキップ操作の完了を要求する。

public APIでは明示的なスキップを field のない `SkipOperation` で表す。これによりスキップも
`OperationCandidates.operations` から選択でき、他の候補と同じ `operate()` APIへ渡せる。
`SkipOperation` はprotobufのoperation typeを直接表すものではなく、画面状態と立直状態に基づいて
frameworkが追加する合成候補である。非立直時の自家ツモ番には追加せず、打牌を暗黙のキャンセルとして
利用する。

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
    seat: Seat
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
    seat: Seat
    tile: Tile | None
    left_tile_count: int
    dora_indicators: tuple[Tile, ...]
    liqi_success: LiqiSuccess | None = None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        validate_left_tile_count(self.left_tile_count)
        validate_optional_instance("liqi_success", self.liqi_success, LiqiSuccess)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiEvent(_MatchEventBase):
    seat: Seat
    tile: Tile
    moqie: bool
    liqi: bool
    wliqi: bool
    dora_indicators: tuple[Tile, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        validate_bool("moqie", self.moqie)
        validate_bool("liqi", self.liqi)
        validate_bool("wliqi", self.wliqi)
        if self.liqi and self.wliqi:
            raise ValueError("liqi and wliqi are mutually exclusive")


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ChiEvent(_MatchEventBase):
    seat: Seat
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    liqi_success: LiqiSuccess | None = None


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class PengEvent(_MatchEventBase):
    seat: Seat
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    liqi_success: LiqiSuccess | None = None


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DaminggangEvent(_MatchEventBase):
    seat: Seat
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile, Tile]
    liqi_success: LiqiSuccess | None = None


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AngangEvent(_MatchEventBase):
    seat: Seat
    consumed: tuple[Tile, Tile, Tile, Tile]
    dora_indicators: tuple[Tile, ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class JiagangEvent(_MatchEventBase):
    seat: Seat
    consumed: tuple[Tile, Tile, Tile]
    added: Tile
    dora_indicators: tuple[Tile, ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class BabeiEvent(_MatchEventBase):
    seat: Seat
    moqie: bool
    dora_indicators: tuple[Tile, ...]


class LiujuType(StrEnum):
    JIUZHONGJIUPAI = "jiuzhongjiupai"
    SIFENGLIANDA = "sifenglianda"
    SIGANGSANLE = "sigangsanle"
    SIJIALIQI = "sijialiqi"


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiujuEvent(_MatchEventBase):
    type: LiujuType
    seat: Seat | None
    liqi_success: LiqiSuccess | None = None


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTilePlayer:
    tingpai: bool
    hand: tuple[Tile, ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTileScore:
    seat: Seat | None
    old_scores: tuple[int, ...]
    delta_scores: tuple[int, ...]
    hand: tuple[Tile, ...]
    ming: tuple[str, ...]
    dora_indicators: tuple[Tile, ...]
    score: int


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NoTileEvent(_MatchEventBase):
    liujumanguan: bool
    players: tuple[NoTilePlayer, ...]
    scores: tuple[NoTileScore, ...]
    game_end: bool


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleFan:
    value: int
    id: int


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class Hule:
    hand: tuple[Tile, ...]
    ming: tuple[str, ...]
    hu_tile: Tile
    seat: Seat
    zimo: bool
    # その他に親・立直、ドラ・裏ドラ表示牌、役、符、点数内訳を保持する。


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HuleEvent(_MatchEventBase):
    hules: tuple[Hule, ...]
    old_scores: tuple[int, ...]
    delta_scores: tuple[int, ...]
    scores: tuple[int, ...]
    baopai_seat: Seat | None


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
    | LiujuEvent
    | NoTileEvent
    | HuleEvent
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
        case LiujuEvent():
            return "liuju"
        case NoTileEvent():
            return "no_tile"
        case HuleEvent():
            return "hule"
    assert_never(event)
```

各 case は `return`、`raise`、loop 内の `continue` などで control flow を終え、`match` の直後に
`assert_never(event)` を置く。`MatchEvent` union に新しい concrete class を追加して利用側が未対応の
ままなら、`ty` は `assert_never()` の引数が `Never` でないことを報告する。`case _` は使わない。

`ActionDiscardTile` は `DapaiEvent` 1 件に変換し、立直宣言牌か
どうかを `liqi` / `wliqi` field に含める。独立した `LiqiEvent` は作らない。後続 action に埋め込まれた
`LiQiSuccess` も独立 event に分離せず、その action に対応する event の `liqi_success` field として
保持し、reducer が同じ event の適用中に点数と `liqibang` を更新する。これは雀魂の action 境界を
保ち、Kanachan の打牌 feature へ変換しやすくするためである。Mjai の `reach` / `reach_accepted` への
分離が必要な adapter は、`DapaiEvent` と後続 event の `liqi_success` から外部境界で生成する。

`ActionDealTile.tile` は自家のツモだけ実牌を含み、他家のツモでは空文字列になる。`ZimoEvent.tile` は
空文字列を `None` に正規化し、reducer は自家なら実牌、他家なら `None` であることを検証する。
`doras` が非空なら現在のドラ表示牌を置き換え、空なら以前の表示牌を維持する。ツモを適用した時点で
直前の打牌または搶槓対象は解決済みとして `pending_action_target` を消去する。

`ActionBaBei` は `BabeiEvent` に変換し、seat、`moqie`、ドラ表示牌を保持する。北牌は常に `4z` なので
Event に tile field は持たない。reducer は三人戦だけで受理し、自家の `moqie=true` ではツモ牌、
`moqie=false` では手牌から `4z` を消費する。手牌から抜いた場合は別のツモ牌を手牌へ取り込む。
北抜きは河と `Fulu` を変更せず、seat ごとの `RoundState.babei` に履歴を追加し、対象 seat の
嶺上ツモと `(seat, 4z)` の搶槓対象を設定する。搶槓が成立しなければ、直後の同じ seat の
`ActionDealTile` を嶺上ツモとして受理する。

`ActionLiuJu` は `LiujuEvent` に変換し、type 1〜4 を `LiujuType` の九種九牌、四風連打、
四槓散了、四家立直へ対応させる。seat は九種九牌だけ必須とし、他の type では wire の0を
`None` に変換する。埋め込まれた `LiQiSuccess` は `liqi_success` に保持する。reducer は
Event 列へ追加して未解決の打牌・搶槓対象と operation 候補を消去し、九種九牌では対象 seat が
第一ツモ中であることを検証する。

`ActionNoTile` は通常の荒牌平局と流し満貫に共通の `NoTileEvent` に変換する。
`players` は protobuf の順序を保ち、各 player の聴牌状態と公開手牌を
`NoTilePlayer` に保持する。`tings` は通常ルールでも使用されるが、他の Action Event と同様に
待ち情報を RPA の公開型へ取り込まない。`already_hule` は通常ルールで利用しないため無視する。
流し満貫の精算情報は `NoTileScore` に変換し、seat、点数列、公開手牌・副露、
ドラ表示牌、流し満貫の獲得点を保持する。通常ルールで利用しない `taxes` / `lines` は無視する。
`NoTileScoreInfo.seat` は流し満貫達成者がいない場合も wire 上は0になるため、
`score == 0` なら `NoTileScore.seat` を `None` に正規化し、非0の場合だけ `Seat` として扱う。
`scores` は通常1要素で、流し満貫達成者が複数いる場合だけ複数要素になる。全員聴牌または
全員不聴では `delta_scores` が空になるため、空の差分は全員0点として扱う。player 数は
3人または4人とし、各 score の `old_scores` と非空の `delta_scores` は player 数と一致し、
score seat は重複しないことを要求する。
特殊 mode 用の `muyu` / `hules_history` は公開 model に取り込まないが、decoded message の
ログには残す。

reducer は Event の player 数が対局人数と一致し、残り自摸回数0の最終打牌直後であることを
要求する。各 `NoTileScore.old_scores` は現在の点数と一致させ、複数の `delta_scores` を
seat ごとに合算して更新後の点数を求める。`liujumanguan` flag は `seat` が `None` でない
score の有無と一致させる。適用後は Event 列へ追加し、未解決の行動対象と operation 候補を
消去する。

`ActionHule` は自摸和と栄和に共通の `HuleEvent` に変換する。protobuf の repeated `hules` は
message の順序を保った `tuple[Hule, ...]` とし、自摸和は1要素、ダブロン・トリロンは複数要素で
表す。`Hule` は和了者、`zimo`、`hu_tile`、公開された手牌と副露、親・立直、
`dora_indicators` / `li_dora_indicators`、役、符、
点数内訳を保持する。役名は `HuleFan.id`、和了点の区分は `Hule.title_id` から特定できるため、
実牌譜で常に空文字列の `FanInfo.name` / `HuleInfo.title` は公開 model に保持しない。
`HuleEvent` は action 全体の和了前点数、点数差分、和了後点数を保持する。
自摸和 reducer は直前の同じ seat の `ZimoEvent`、または親の配牌直後の
天和だけを受理する。自家に見えている和了牌、`qinjia`、点数遷移を検証し、Event 列へ追加して
operation 候補と未解決の打牌・搶槓対象を消去する。

ロン reducer は `pending_action_target` が存在することを要求し、その `(seat, tile)` を放銃元または
搶槓対象として使う。各 `Hule` は `zimo=False`、
`hu_tile` が対象牌と一致し、和了者が対象 seat と異なることを要求する。ダブロン・トリロンでは
message の順序を保ったまま各和了者を検証し、seat の重複を拒否する。自摸和とロンが同じ
`HuleEvent` に混在する場合も不整合とする。自摸和・ロンのいずれも、全和了者の seat が対局人数の
範囲内であり、`qinjia` が局の親と一致することを検証する。適用後は点数を更新し、operation 候補と
未解決対象を消去する。

`ActionHule.gameend` は解析 Wiki でも値が設定された牌譜が確認されておらず、飛び終了した実牌譜でも
空だったため、`HuleEvent` には取り込まない。decoded message のログには元の field が残るので、
将来値が観測された場合も postmortem は可能である。

action 直下の `ActionHule.doras` は実牌譜では空で、和了によって新しいドラ表示牌が捲られることも
ないため `HuleEvent` には保持しない。最終的なドラ・裏ドラ表示牌は各 `Hule` の
`dora_indicators` / `li_dora_indicators` に保持する。reducer は和了時に
`RoundState.dora_indicators` を更新せず、直前の打牌・嶺上ツモ・連続する槓までに確定した値を維持する。

`Hule.baopai_seats` は和了ごとの包の対象 seat を複数保持でき、ダブロン・トリロンで別々の包が
成立する場合も各 `Hule` に対応付けられる。旧 scalar の `HuleInfo.baopai` と action 直下の
`ActionHule.baopai` は通常の seat と異なり、0が包なし、1〜4がそれぞれ起家・下家・対面・上家を表す。
decoder はこの差を吸収し、0を `None`、1〜4を `Seat(0)`〜`Seat(3)` に変換して、それぞれ
`Hule.baopai_seat` と `HuleEvent.baopai_seat` に保持する。旧 scalar が現在も使われるかは未検証で
あるため、`baopai_seats` との整合条件や優先順位は設けない。

`ActionChiPengGang(type=0)` は `ChiEvent` に変換する。雀魂の `tiles` は自家から消費する2枚を先に、
直前の河から取得する牌を末尾に置く。protocol decoder で前2枚を固定長の `consumed`、末尾を `tile` に
分解し、雀魂の内部表現をそのまま公開 API へ持ち込まない。
`from_seat` は `froms[-1]` から取得する。reducer は `from_seat` と取得牌が未解決の直前打牌に一致し、
かつ四麻で鳴いた seat の上家に当たることを検証する。自家のチーでは `consumed` を `shoupai` から
除き、`Chi(from_seat=..., tile=..., consumed=...)` として追加する。他家のチーでは自家手牌を
変更しない。どちらも全員の `first_draw` / `yifa` を終了させ、未解決打牌を消去する。後続の打牌候補が
同じ action に含まれる場合は、チー適用後の自家手牌から `DapaiOperation` を生成する。

`ActionChiPengGang(type=1)` は `PengEvent` に変換する。`tiles` / `froms` の分解方法はチーと同じで、
前2枚を鳴いた player の `consumed`、末尾を `from_seat` の河から取得する `tile` とする。赤5と黒5は
同じ牌種として扱い、3枚が同種であることを decoder で検証する。reducer は取得元の方向を制限せず、
任意の他家による未解決の直前打牌と `from_seat` / `tile` が一致することを要求する。自家では
`consumed` を手牌から除いて `Peng` を追加し、他家では自家手牌を変更しない。立直成立、
`first_draw` / `yifa`、未解決打牌、同じ action に含まれる後続打牌候補の扱いはチーと共通とする。

`ActionChiPengGang(type=2)` は `DaminggangEvent` に変換する。雀魂の `tiles` / `froms` は、鳴いた
playerの手牌から消費する3枚を先に、河から取得する牌とその `from_seat` を末尾に置く。decoderは
先頭3枚を固定長の `consumed`、末尾を `tile` に分解し、赤5と黒5を同じ牌種として4枚の整合性を
検証する。reducerは任意の他家による未解決の直前打牌との一致を要求し、自家では `consumed` を
手牌から除いて `Daminggang` を追加する。他家では自家手牌を変更しない。大明槓したseatの
`lingshang_zimo` を真にし、続く嶺上牌の処理へ引き継ぐ。立直成立、`first_draw` / `yifa`、未解決
打牌の扱いはチー・ポンと共通とする。

`ActionAnGangAddGang(type=3)` は `AngangEvent` に変換する。wire の `tiles` は名前に反して暗槓する
牌種を表す単独の文字列である。公開 Event と `Angang` state は消費した4枚を固定長 `consumed` として
保持する。赤ありルールの表現へ正規化し、萬子・筒子・索子の五は wire が `0m` / `5m`、`0p` /
`5p`、`0s` / `5s` のどちらでも、それぞれ赤五を先頭に置いた1枚と黒五3枚にする。それ以外は同じ
牌4枚とする。対局ルール metadata まで RPA が解釈して赤なし表現へ切り替える複雑さは導入しない。
赤なし対局を扱う利用者は、把握している対局ルールに基づいて AI feature 等の外部境界で補正する。

reducer は自家の `shoupai` と `zimopai` から、赤五と黒五を同じ牌種として数えた4枚を消費する。
したがって赤なし対局で手牌が黒五4枚でも state 遷移は継続できる。暗槓が手牌内の4枚だけを使い、
別の `zimopai` が残る場合は、そのツモ牌を `shoupai` に取り込む。暗槓は河へ追加せず、
全員の `first_draw` / `yifa` を終了し、暗槓した seat の
`lingshang_zimo` を真にする。

`ActionAnGangAddGang(type=2)` は `JiagangEvent` に変換する。`tiles` は加えた牌1枚を表すため、
赤牌と通常牌を正規化せず `added` にそのまま保持する。`consumed` は `added` を除いた3枚を
赤あり表現へ正規化する。`added` が赤五なら黒五3枚、黒五なら赤五1枚と黒五2枚、それ以外は
同種3枚とする。この `consumed` は wire から一意に補完した正規化形であり、元のポンの取得形は
表さない。
reducer は同じ牌種の既存 `Peng` が対象 seat の `fulu` に一意に存在することを要求し、その
`from_seat`、取得した `tile`、`consumed` を引き継いだ完全な `Jiagang` へ置換する。自家の加槓では
`added` と完全一致する牌を `shoupai` または `zimopai` から消費する。手牌側の牌を加えた場合は、
別に引いていた `zimopai` を `shoupai` に取り込む。他家の手牌は観測できないため、既存ポンの
置換だけを行う。加槓した seat の `lingshang_zimo` を真にし、河は変更しない。

雀魂では暗槓・加槓・北抜きのいずれも搶槓の対象になり得るため、成立直後の対象を
`pending_action_target` の `(seat, tile)` に保持する。通常の打牌も同じ field に保持し、同時には
存在し得ない二つの optional field を設けない。ロンなら後続の和了 Event がこの値を参照し、
和了せずツモへ進んだ時点で消去する。副露は打牌だけを対象にできるため、reducer は
`events[-1]` が `DapaiEvent` であることも要求し、搶槓対象のチー・ポン・大明槓を拒否する。
`ZimoEvent` の reducer は元から直前 Event を参照して嶺上ツモを識別するため、統合によって Event 列の
追加走査は発生しない。

暗槓・加槓の operation は最大3候補を取り得る。一方、3候補時の雀魂 UI の選択座標は未確認である。
操作 API を実装する際は推測した座標でクリックせず、専用の画面状態例外で停止する。例外 message には
実例と座標調査への協力依頼を含め、利用者が任意に取得した screenshot を報告できるようにする。

暗槓操作は `gang.png` のボタンをクリックし、1候補なら追加の候補選択を行わない。2候補なら
message の候補順を画面の左から右へ対応させ、基準 viewport でそれぞれ
`Region(left=601, top=692, width=317, height=117)` と
`Region(left=961, top=692, width=317, height=117)` をクリックする。この座標は4牌を表示する
暗槓・加槓候補用であり、2牌を表示するチー・ポン候補の領域とは共用しない。3候補の場合は槓ボタンを
クリックして候補表示を待った後、座標を推測せず `ScreenNotImplementedOperationError` に表示中の
screenshot を添えて停止する。

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
action に付随する現在の選択可能 operation は発生済み event ではないため、event と重複する
action model を作らず、adapter が public `OperationCandidates | None` として別に返す。

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
- `ActionLiuJu`
- `ActionNoTile`
- `ActionHule`

active `game_state` の restore batch に round terminal action が含まれるかは手動 spike で確認する。
特殊 mode 専用 action、未知 action 名、壊れた data、不正 step は推測せず明示的な
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
- `screens/match/types.py`: 検証済みの `Seat` / `Tile` NewType と境界 validator
- `screens/match/_decode.py`: event と operation が共有する decoded JSON field getter
- `screens/match/event/_base.py`: event 共通の action step と不変条件
- `screens/match/event/<event>.py`: concrete event ごとの final frozen dataclass と `from_dict()`
- `screens/match/event/__init__.py`: concrete event と明示的な `MatchEvent` union の export
- `screens/match/operation/<operation>.py`: concrete operation ごとの final frozen dataclass
- `screens/match/operation/_decode.py`: `OptionalOperationList` の共通 wire decoder と type dispatch
- `screens/match/operation/_specification.py`: state 適用前の immutable な内部 operation specification
- `screens/match/operation/_materialize.py`: Event 適用後の手牌から public operation 候補への展開
- `screens/match/operation/__init__.py`: concrete operation、`MatchOperation`、候補 container の export
- `screens/match/_action.py`: live unmask、restore adapter、nested decode、event decoder registry
- `screens/match/store.py`: metadata、step、round reducer、temporary replay と atomic commit
- `screens/match/screen.py`: message classifier、初期化期限、Screen error への変換、`get_state()`
- `screens/match/__init__.py`: `MatchScreen`、public state、event、operation 型を通常 export

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
11. live `OptionalOperationList.seat` の意味と、三人戦で type 11 が北抜きを表すこと。

実通信ログは一時ログだけに置き、コミットしない。

## TDD と実装順

1. 実装前の手動 spike を完了し、fresh marker、origin、CPU、restore sentinel を固定する。
2. public immutable state、final frozen event dataclass、段位を含む authGame / ActionNewRound の strict decode。
3. 明示的 `MatchEvent` union、runtime validator、nested action の live / restore decoder と 1 対 1 変換。
4. public immutable operation、共通 decoder、state への接続を type 1 件ずつ追加する。
5. standard active-round event reducer、event 列、step / round generation の不変条件。
6. temporary store への restore replay と atomic publish。
7. bootstrapper の fresh / recovery 経路。
8. `MatchScreen.before_callback()` と `get_state()` への接続。
9. 同一 instance での次局 `ActionNewRound`。
10. active 中の `syncGame` 再同期。
11. generic reload 後の Screen 再検出と recovery bootstrap。
12. 状態待機と操作 API を 1 種類ずつ追加する。

各段階で synthetic data の自動テストを完了し、高レベル API は 1 つずつ実ゲーム確認する。
実 payload はテストや文書へ保存しない。

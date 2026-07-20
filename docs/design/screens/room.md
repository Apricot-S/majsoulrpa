# RoomScreen 設計

## 目的と範囲

`RoomScreen` は、合意済み友人戦の待機部屋で現在の状態を参照し、部屋からの退出、
AI の追加、対局開始、準備完了を安全に操作する `Screen` である。

この設計は待機部屋だけを対象とする。オープン対局、段位戦、未合意の対局への参加、
対局中の操作は対象にしない。WebSocket request をフレームワークから生成して送信する
API も追加しない。操作は雀魂の画面に対して行い、成否と状態変化を Sniffer が観測した
WebSocket message で確認する。

部屋 ID、account ID、プレイヤー名は、フレームワーク利用者が bot を参加・開始させるかを
判断するため、この Screen では例外的に公開する。これらを通常ログへ自動出力しない。

## 公開名

公開 class 名は `RoomScreen` とする。`FriendlyRoomScreen` は意味は明確だが、既存の
`HomeScreen.create_room()` / `join_room()` から到達する画面名として長く、今回の要件で
指定された名前とも異なるため採用しない。

## 公開データモデル

公開する状態は mutable な内部 object や protobuf object ではなく、取得時点の immutable
snapshot とする。

```python
from dataclasses import dataclass
from enum import StrEnum


class RoomStatus(StrEnum):
    WAITING = "waiting"
    MATCH_STARTED = "match_started"
    LEFT = "left"
    KICKED = "kicked"


@dataclass(frozen=True, slots=True)
class RoomPlayer:
    account_id: int
    name: str
    is_host: bool
    is_ready: bool


@dataclass(frozen=True, slots=True)
class RoomState:
    version: int
    status: RoomStatus
    room_id: int
    max_player_count: int
    players: tuple[RoomPlayer, ...]
    ai_count: int
    self_account_id: int

    @property
    def self_is_host(self) -> bool: ...

    @property
    def participant_count(self) -> int: ...

    @property
    def available_slots(self) -> int: ...
```

設計上の意味は次のとおりとする。

- `version` は RPA client 内で状態が変わるたびに増える単調増加値である。wire 上の
  `Room.seq` をそのまま公開する値ではない。
- `room_id` は protocol の正の整数をそのまま公開する。`HomeScreen.join_room()` の文字列入力
  とは型が異なる。
- `max_player_count` は通常 room の `3` / `4` に加えて、VS_AI の `1` を許す。
  VS_AI は `createRoom` だけで作られ、人間の host 1 人が Room 内の全参加者となる。
  対局開始後に残りの席へ入る CPU は Room 内の `players` / `ai_count` へ先取りして加えない。
  それ以外の値は protocol 不整合とする。
- `players` は人間のプレイヤーだけを含む。`Room.persons` / `player_list` の順序を維持し、
  seat の意味が実通信で確認できるまでは seat API を追加しない。
- AI は人間として扱わず、`robots` の要素数を `ai_count` として公開する。`robot_count` は
  AI 追加後も `0` のまま変化しないため、状態計算には使わない。これにより AI 追加の完了と
  空き枠を判定できる。
- `is_host` は snapshot の `owner_id` と account ID の一致から毎回導出する。
- `is_ready` は protocol の `ready_list` または準備通知が示す値である。ホストを便宜的に
  `True` へ書き換えない。対局開始条件を調べるときだけホストを判定対象から除外する。
- `self_account_id` は client session state で取得済みの正の値でなければならない。

terminal な `MATCH_STARTED`、`LEFT`、`KICKED` でも最後に確定できた部屋情報は snapshot に
残す。これにより `wait_for_state_change()` の待機中に起きた遷移を利用者が判定できる。
terminal 遷移後に同じ `RoomScreen` で別の操作はできない。

## 公開 API 候補

すべて async の高レベル Screen API とし、`majsoulrpa.screens.api` の info log 対象、
stale 保護対象とする。

```python
class RoomScreen(Screen):
    async def get_state(self) -> RoomState: ...

    async def wait_for_state_change(self, state: RoomState) -> RoomState: ...

    async def leave(self) -> None: ...

    async def add_ai(self) -> RoomState: ...

    async def start_match(self) -> None: ...

    async def set_ready(
        self,
        *,
        ready: bool = True,
    ) -> RoomState: ...
```

高レベル Screen API は timeout 引数を持たない。期限が必要な利用者は structured concurrency に
従い、呼び出し側で `asyncio.timeout()` を使う。

```python
async with asyncio.timeout(10.0):
    state = await screen.add_ai()
```

RoomScreen 内部の message 待機は cancellation をそのまま伝播する。呼び出し側の timeout を
通常完了や server rejection として扱わず、timeout 時に自動 retry もしない。
他の Screen API と同様に、同じ Screen instance に対する複数 API の並行呼び出しは
サポートしない。RPA runtime は callback を逐次実行するため、通常利用で操作が競合しない。

## Callback lifecycle

Room callback は room が active な間、同じ callback invocation と `RoomScreen` instance を維持する。
callback が return すると runtime は現在の instance を破棄して画面検出からやり直すが、消費済みの
完全 snapshot や途中状態を次の instance へ引き継がない。次の API が非 terminal な状態を返した後も、
callback 内で状態待機または別の操作を続ける。

- `get_state()`
- 非 terminal な state を返した `wait_for_state_change()`
- `add_ai()`
- `set_ready()`

`LEFT`、`KICKED`、`MATCH_STARTED`、RPA 停止、または失敗によって現在の RoomScreen を終了するときに
callback を return する。active 中の早期 return を runtime hook で検出する処理は、必要性が
確認されるまで追加せず、利用契約として明記する。誤って早期 return した後に RoomScreen が
再検出されても、差分 notice や過去の instance state から初期化成功を推測しない。

雀魂の友人戦では Room 内で browser を reload または再起動すると host、guest ともに退出するため、
reload を RoomScreen の recovery 境界として扱わない。一方、対局終了後に同じ友人戦へ戻る画面
遷移では `.lq.Lobby.fetchRoom` response を新しい RoomScreen の完全 snapshot として使う。
この lifecycle 判断は
[ADR-0007: Room状態をcallback invocation内で管理する](../../adr/0007-room-state-lifecycle.md)
に記録する。

`get_state()` は新しい network request を送らず、`SnifferMessageSource` に蓄積された
message をその時点まで読み進めて最新 snapshot を返す。
`wait_for_state_change()` は polling 用 sleep を利用者に書かせず、渡された snapshot の
version より新しい snapshot を待つ。snapshot の room ID と self account ID が現在の room と
一致し、version が現在より未来でないことを検証する。待機開始後の最初の更新が terminal
遷移でも、その terminal snapshot を 1 回返す。`MATCH_STARTED` の場合は `room-sign` が
画面から消えるまで待ってから Screen を stale にして返す。その後の Screen API は stale
error になる。

### `leave()`

- ホストとゲストの両方が利用できる。
- `WAITING` 以外では画面を操作しない。
- 特に、ゲストが `MATCH_STARTED` へ遷移した後は退出操作を行えない。
- 成功した `.lq.Lobby.leaveRoom` response を観測して `LEFT` にした後で Screen を stale にする。
- ホスト退出後に残った側で起きるホスト交代は、残った client の
  `.lq.NotifyRoomPlayerUpdate` から処理する。

### `add_ai()`

- 最新 snapshot で自分がホストの場合だけ利用できる。
- `participant_count < max_player_count` を事前条件とする。
- VS_AI は `participant_count == max_player_count == 1` の満員 room として扱う。画面に
  `add_ai` ボタンが存在しないため、template の探索や click を行わない。
- UI が選ぶ空き位置へ 1 体だけ追加する。位置指定 API は実需要が出るまで追加しない。
- `.lq.Lobby.addRoomRobot` の成功 response と、
  `.lq.NotifyRoomPlayerUpdate` で AI 数が 1 増えた snapshot の両方を待つ。実通信では
  notice が response より先に観測されるため、両者の到着順は問わない。
- 満員、ホストでない、または room が active でない場合は click しない。
- 自動 retry はしない。競合による server rejection は型付き例外として返す。

### `start_match()`

- 最新 snapshot で自分がホストの場合だけ利用できる。
- 人間のゲスト全員が `is_ready` でなければ click しない。
- AI を含めた Room 内の参加人数が `max_player_count` に達していることも事前条件とする。
  VS_AI では host 1 人でこの条件を満たし、対局開始後に残りの席へ CPU が入る。
- `.lq.Lobby.startRoom` の成功 response に加えて `.lq.NotifyRoomGameStart` を待つ。
- 実通信では `startRoom` の outbound request/response、game start notice の順に観測され、
  その後に `authGame` と `enterGame` が続いた。
- game start notice を観測して `MATCH_STARTED` にした後、`room-sign` が画面から消えるまで
  待ってから Screen を stale にする。ローディング画面のイラストは設定により異なるため、
  ローディング画面自体の template 検出は行わない。
- guest が `wait_for_state_change()` で `MATCH_STARTED` を観測した場合も、同じ画面消失条件を
  満たしてから terminal snapshot を返す。これにより callback 終了直後に runtime が
  `RoomScreen` を再検出しないようにする。
- 画面消失待機が呼び出し側 timeout で中断されても、通信上は terminal のため Screen は
  stale にする。

### `set_ready()`

- 最新 snapshot で自分がゲストの場合だけ利用できる。
- キーワード専用引数 `ready` で目標状態を指定する。省略時は `True` とし、
  `set_ready()` は ready、`set_ready(ready=False)` は ready 解除を行う。
- 自分の `is_ready` がすでに `ready` と一致する場合は、確認済みの最新 snapshot を返す
  idempotent な no-op とする。成功したように見せる fallback ではなく、要求された事後条件が
  すでに成立している場合である。
- `.lq.Lobby.readyPlay` request の `ready` が指定した目標状態と一致すること、および成功
  response を確認し、`.lq.NotifyRoomPlayerReady` で自分の `is_ready` が目標状態になった
  snapshot まで待つ。response と notice の到着順は実通信で確認するまで固定しない。
- ready 解除専用の `cancel()` / `cancel_ready()` は追加しない。`cancel()` は取り消す対象が
  名前から分からず、同じ状態設定操作を別 API に分ける必要もないためである。
- 操作名は `set_ready()` と `start_match()` を維持し、`ready()` / `start()` の alias は
  追加しない。前者は目標状態を設定する idempotent な操作、後者は対局開始操作であることを
  明示する。

## WebSocket 観測方式

### 結論

操作のたびに一時的な Sniffer を開始せず、`RPARuntime` と兄弟 task としてすでに常駐する
Sniffer client 受信 task が decode 済み message を `SnifferMessageSource` へ蓄積する。
`RoomScreen` は既存の protected `get()` / `get_nowait()` 操作だけでそれを読み進める。
decode 直後に room 専用 observer を呼ぶ処理、OS thread、Room 専用 background task は
追加しない。

```text
ZMQ SUB
  -> protobuf decode
  -> account ID 用 session state.observe(message)
  -> 既存の bounded Sniffer message queue
       -> RoomScreen が get() / get_nowait()
       -> room message を snapshot へ反映
```

room 状態だけ account ID と同じ decode 直後の observer に置く必要はない。RoomScreen の
callback と API は逐次実行され、`SnifferMessageSource` がその間の message を順序どおり保持
するためである。host 交代や kick は、次の `get_state()`、状態待機、または操作前 refresh で
処理できる。`wait_for_state_change()` は source の `get()` を直接 await する。

この状態管理方式の判断は
[ADR-0007: Room状態をcallback invocation内で管理する](../../adr/0007-room-state-lifecycle.md)
に記録する。以前の共有 cache 方針は
[ADR-0004](../../adr/0004-room-state-message-source-and-cache.md) で履歴として参照できる。

最新 snapshot は `RoomScreen` instance が所有する具体的な `RoomStateStore` に保持する。これは
message を常時観測する service ではなく、同じ RoomScreen が source を読んだときだけ更新する。
raw message の履歴、operation response、waiter は保持せず、`ScreenContext` や別の Screen
instance と共有しない。

`RoomScreen.before_callback()` と各公開 API の先頭は、まず `get_nowait()` でその時点の queue を
drain し、room message を instance-local store へ反映する。待機が必要な API は続けて `get()` で
到着順に読む。
Sniffer の stream gap、decode error、queue overflow は従来どおり runtime 全体の失敗とし、
Room state を推測で補完しない。長時間 callback が source を読まず queue 上限へ達した場合も、
常駐 observer を追加しても queue 自体は残るため解決しない。従来どおり黙って破棄せず
runtime error にする。

初期 snapshot を RoomScreen へ引き渡すため、`HomeScreen.create_room()` / `join_room()` は成功した
`createRoom` / `joinRoom` の完全な decoded Req/Res を source に残す。現行 `join_room()` は成功
message を消費するため、RoomScreen 実装時に response dict だけでなく元の decoded message を
保持し、成功確認後に 1 回だけ `put_back()` する。失敗 response は RoomScreen へ渡さない。

対局終了後に同じ友人戦へ戻る場合、新しい `RoomScreen` は `.lq.Lobby.fetchRoom` response の完全
snapshot から instance-local store を初期化する。`MatchScreen` がこの message を画面遷移の確認中に
先読みした場合は、次の Screen に属する decoded message として 1 回だけ `put_back()` する。
`fetchRoom` は対局から Room への再入場 evidence であり、Room 内の reload recovery や active 中の
callback 早期 return を補完する evidence として扱わない。

### 初期 snapshot と更新 message

現行 protocol から次の対応を設計の出発点とする。実装前に synthetic message で固定し、
実際の雀魂では payload を docs や fixture へ転記せず動作だけを確認する。

| message | 用途 |
|---|---|
| `.lq.Lobby.createRoom` response | ホスト側の最初の完全な `Room` snapshot |
| `.lq.Lobby.joinRoom` response | ゲスト側の最初の完全な `Room` snapshot |
| `.lq.Lobby.fetchRoom` response | 対局終了後に同じ友人戦へ戻るときの完全な `Room` snapshot |
| `.lq.NotifyRoomPlayerUpdate` | owner、人間、AI、位置情報の更新。ホスト交代もここで扱う |
| `.lq.NotifyRoomPlayerReady` | 個別プレイヤーの ready 更新 |
| `.lq.NotifyRoomGameStart` | `MATCH_STARTED` への terminal 遷移 |
| `.lq.NotifyRoomKickOut` | 自分が kick されたことによる `KICKED` への terminal 遷移 |
| `.lq.Lobby.leaveRoom` response | 自発的退出による `LEFT` への terminal 遷移 |
| `.lq.Lobby.addRoomRobot` response | AI 追加要求の server 成否 |
| `.lq.Lobby.readyPlay` response | ready 要求の server 成否 |
| `.lq.Lobby.startRoom` response | 対局開始要求の server 成否 |

`Room` の `seq` と room notice の `seq` は順序検証に使える可能性があるが、増加規則をまだ
実通信で確認していない。推測で厳密化せず、手動 spike で同値、連番、飛び値の意味を確認して
から test を追加する。PUB/SUB publication sequence の gap 検出はこの確認前でも有効である。

`NotifyRoomPlayerReady.account_list` は現行 `.proto` 上では名前に反して singular field である。
最初の実装は `account_id` と `ready` による個別更新を基準とし、`account_list` の実 payload
上の意味は手動 spike で確認する。decode 結果の形が想定と違う場合は空 list などへ変換せず、
protocol / design を更新する。

### 操作と message の相関

各操作は次の順序で行う。

1. `get_nowait()` で現在の source を空になるまで読み、room state を最新化する。
2. active room state、権限、満員・ready 条件を確認する。
3. template または確定した `Region` を使って画面を click する。
4. source の `get()` で到着 message を順に処理し、期待する outbound Req/Res と notice を待つ。
5. response を観測したら `error` を検証し、server rejection なら例外にする。
6. 状態変化を伴う操作では、必要な response と事後条件を満たす snapshot の両方が揃うまで
   読み進める。両者の順序は操作ごとの実通信結果に従う。
7. terminal 操作だけ Screen を stale にする。

click 前に source を drain し、同じ Screen の操作を並行実行しないため、click 後に得た同名
Req/Res を今回の操作へ対応付けられる。response や notice が待機開始より先に到着しても
bounded queue に残るため取り逃がさない。Req/Res の request direction、API 名、既知 request
field も確認する。必要な response または notice の片方が来ない場合は成功扱いにせず待機を
続け、呼び出し側の timeout または cancellation に委ねる。矛盾した notice を観測した場合は
message 不整合として失敗させる。

## 状態整合性

次を満たさない decoded message は、RoomScreen が source から読み取った時点で screenshot 付き
`ScreenInconsistentMessageError` とする。Sniffer transport / protobuf decode 自体の失敗は、
従来どおり background task から元の infrastructure error として伝播する。

- active snapshot の room ID、owner ID、self account ID、各人間の account ID は正である。
- `max_player_count` は通常 room の 3 / 4、または VS_AI の 1 である。
- 人間の account ID は重複しない。
- active room の owner ID と self account ID は human player list に存在する。
- ready 対象の account ID は human player list に存在する。
- 人間と AI の合計は最大人数を超えない。
- active な同じ RoomScreen instance の途中で room ID が変化しない。
- terminal 後の古い room update を新しい active state として扱わない。

terminal state になった現在の `RoomScreen` は stale とし、同じ instance で新しい room を開始しない。
新しい room へ入る場合は `HomeScreen.create_room()` / `join_room()`、対局終了後に同じ友人戦へ
戻る場合は `fetchRoom` から、新しい `RoomScreen` callback と store を開始する。active 中に別
room ID の完全 snapshot を観測した場合は暗黙に切り替えず不整合とする。

実通信では `robot_count` は AI 追加後も `0` のままで、`robots` に追加順の AI が入り、各 AI の
`account_id` は `1`、`2`、`3` と増える。`positions` は画面左から並ぶ player slot ごとに、その
slot を占める人間または AI の account ID を保持する。現時点の公開状態は座席指定を扱わず、
`ai_count = len(robots)` だけを利用する。

## ホスト交代、kick、外部からの対局開始

ホスト権限を `RoomScreen` instance の bool として cache しない。各 `RoomState` の
`owner_id` から `RoomPlayer.is_host` と `self_is_host` を再導出する。
`NotifyRoomPlayerUpdate` でホストが変われば、同じ callback 中でも次の `get_state()` または
`wait_for_state_change()` から新しい権限が見える。操作 lock 取得後にも再検証するため、
ホスト交代との race で古い権限を使って click しない。

空 payload の `NotifyRoomKickOut` は受信した client 自身の kick として `KICKED` にする。
待機中の Room API は terminal state を検知して呼び出し側の timeout より先に失敗する。
外部ホストが対局を開始した場合も `NotifyRoomGameStart` で `MATCH_STARTED` にし、その後の
Room 操作を禁止する。

## 失敗モデル

### 結論: Enum を属性に持つ例外

server error code を戻り値の Enum にする方式は採用しない。呼び出し側が戻り値を無視して
失敗を成功として進める可能性があるためである。一方、文字列だけの例外では bot が理由を
安全に分岐できない。したがって、server rejection は機械判定用 Enum と元の数値 code を
属性に持つ型付き例外として表す。

```python
class RoomOperation(StrEnum):
    LEAVE = "leave"
    ADD_AI = "add_ai"
    START_MATCH = "start_match"
    SET_READY = "set_ready"


class RoomOperationFailureReason(Enum):
    # 実通信で意味と数値を確認できた項目だけ追加する。
    UNRECOGNIZED_ERROR_CODE = -1


class RoomOperationNotAllowedReason(StrEnum):
    NOT_GUEST = "not_guest"
    NOT_HOST = "not_host"
    ROOM_FULL = "room_full"
    ROOM_NOT_FULL = "room_not_full"
    GUEST_NOT_READY = "guest_not_ready"
    ROOM_INACTIVE = "room_inactive"


class RoomOperationNotAllowedError(ScreenInvalidOperationError):
    operation: RoomOperation
    reason: RoomOperationNotAllowedReason


class RoomOperationRejectedError(ScreenError):
    operation: RoomOperation
    reason: RoomOperationFailureReason
    server_error_code: int
```

同じ数値 code の意味が操作ごとに異なることが手動確認で分かった場合は、無理に共通 Enum に
せず操作別 Enum へ分割する。既知 code を資料や他実装から推測して先に追加しない。
未対応 code は数値だけ warning log に残し、`UNRECOGNIZED_ERROR_CODE` とする。server の
`Error.message`、room ID、account ID、プレイヤー名は通常例外 message に含めない。

失敗の分類は次のとおりとする。

| 失敗 | 扱い |
|---|---|
| host 限定 API を guest が呼ぶ、guest 限定 API を host が呼ぶ | `RoomOperationNotAllowedError` + reason Enum |
| 満員、空席、guest 未 ready など事前条件不成立 | 同上。click しない |
| server の `error.code` | `RoomOperationRejectedError` |
| 未知 code | 上記例外 + `UNRECOGNIZED_ERROR_CODE`。数値 code は属性に保持 |
| response / notice が到着しない | API 内では待機を継続。呼び出し側の timeout / cancellation に委ねる |
| message field の欠落・型不正・矛盾 | `ScreenInconsistentMessageError` |
| kick 済み、対局開始済み、退出済み | `ScreenStaleError` の Room 用派生 |
| template / 操作対象が見つからない | `ScreenDetectionError` |
| browser / Sniffer / decode / stream gap | 元の infrastructure error を変換せず伝播 |
| cancellation | cleanup 後にそのまま伝播 |

server rejection、呼び出し側 timeout、kick を自動 retry しない。UI error dialog を閉じて同じ
`RoomScreen` を継続利用できることが操作ごとの手動確認で確定した場合だけ、例外送出前の
画面復旧をその API の明示的な手順として設計する。復旧に失敗した場合は元の rejection を
成功扱いにせず、cleanup failure を添えて報告する。

## 画面検出と画像資産

`RoomScreen.detection_spec()` は待機部屋に固有で、個人情報を含まない template を使う。
WebSocket state だけを Screen の画像到達判定の代用にしない。画像で RoomScreen が検出され、
`before_callback()` で対応する active room snapshot を取得できて初めて callback を実行する。
framework hook である `before_callback()` の初期化上限は public 引数にせず、実装時に runtime
側の既定期限または内部定数として固定する。画像だけ成立して snapshot がない場合は状態を
推測せず失敗させる。

実装時に必要な RoomScreen、退出、AI 追加、開始、ready、error dialog の template または
確定 `Region` は、実画面で確認後にユーザーへコミットを依頼する。エージェントが実ゲーム
由来の screenshot を生成、複製、コミットしない。

## ログと公開情報

- 高レベル API の info log は Screen 名と API 名だけとする。
- Room state の取得だけで room ID、account ID、名前を log しない。
- 成功 log に room ID や player 情報を含めない。
- rejection log は operation と failure reason 名だけを基本とし、未知 code のときだけ数値を
  warning に出す。
- Sniffer 調査ログは既存の安全性方針の例外に従う。decode 済み message を出せるが、docs、
  fixture、examples、チャット、コミットへ転記しない。
- raw payload bytes は別の debug log に出せるが、保存物をコミットしない。

## 実装前の手動 spike

実装を始める前に、次を合意済み友人戦でユーザーに確認してもらう。payload の値は文書へ
貼らず、API 名、field の意味、error code の意味、画面遷移という設計結果だけを反映する。

1. 四人部屋と三人部屋の create / join、および対局終了後の fetch snapshot。
2. `persons`、`robots`、`robot_count`、`positions` の関係。
3. ready 通知の `account_id`、`ready`、`account_list`、`seq` の意味。
4. host 退出時の player update と owner の選ばれ方。
5. host による kick を受けた client の notice と遷移。
6. AI 追加成功、満員時、guest から操作できない場合の UI と response。
7. guest 未 ready、空席あり、全員 ready の各 start 操作と response / notice 順序。
8. guest / host の退出成功と、対局開始後に退出 UI が使えないこと。
9. 各 Req/Res の既知 error code と error dialog 復旧手順。
10. Room / notice の `seq` 増加規則。

実通信ログは一時ログだけに置き、コミットしない。必要な template 画像と settings は、個人
情報が写っていないことを確認したうえでユーザーにコミットを依頼する。

## TDD と実装順

高レベル API は一度に 1 つだけ実装し、各段階で自動テスト、品質ゲート、実ゲーム確認を
完了してから次へ進む。

1. `RoomState` / `RoomPlayer` の純粋な decode と不変条件。
2. instance-local `RoomStateStore` と `SnifferMessageSource` からの snapshot 更新、terminal。
3. `RoomScreen` の画像検出と `get_state()`。
4. `wait_for_state_change()` と外部 host 交代 / kick の扱い。
5. `leave()`。
6. `add_ai()`。
7. `set_ready()`。
8. `start_match()`。

自動テストは synthetic decoded message、fake state store、fake browser operation、synthetic
screenshot だけを使う。実雀魂、実 network、ライブ payload は使わない。

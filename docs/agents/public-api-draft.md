# 公開 API 草案

この文書は v3 の最初の公開 API 候補を整理する草案です。実装時に
テストリストと照合して変更してよいですが、変更する場合は理由を残します。

## 設計判断

- callback 登録を主 API とする
- callback は `async def` のみ受け付ける
- 同じ Presentation class への callback 登録は 1 つだけ許す
- 重複登録は起動時ではなく登録時に例外にする
- callback の戻り値を次の data とする
- data はフレームワークが解釈、保存、serialize、log しない
- 未登録 Presentation は検出しても dispatch しない
- detection timeout と操作 timeout は分ける

同じ Presentation に複数 callback を登録できると、data の更新順序と例外時の
扱いが曖昧になります。v3 初期では禁止し、必要が出たらユーザー側で 1 つの
callback から複数処理を呼び出す形にします。

## 最小利用例

以下は API の形を説明するための例であり、実装済みコードではありません。

```python
from majsoulrpa import RPAApp
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import HomeScreen, LoginScreen


app = RPAApp()


@app.on(LoginScreen)
async def login(screen: LoginScreen, data: UserData) -> UserData:
    await screen.enter_email_address(data.email_address)
    code = await data.code_provider.fetch()
    await screen.enter_verification_code(code)
    return data


@app.on(HomeScreen)
async def home(screen: HomeScreen, data: UserData) -> UserData:
    await screen.stop(close_browser=True)
    return data


result = await app.run(AppConfig(), data, detection_timeout=60)
```

## `RPAApp`

責務:

- Presentation class と callback の対応を保持する
- client runtime を起動する
- 検出された Presentation を callback へ dispatch する
- data の受け渡しを行う
- timeout、cancellation、例外伝播を整理する

公開候補:

```python
class RPAApp:
    def on(self, screen_type: type[ScreenT]) -> CallbackDecorator[ScreenT]: ...

    async def run(
        self,
        config: AppConfig,
        data: Any,
        *,
        detection_timeout: float | None = None,
    ) -> Any: ...
```

`run()` は callback が明示的に停止を要求するか、例外が発生するまで loop します。
戻り値は最後の data です。

## `AppConfig`

設定は 1 つの root config にまとめ、browser host と client の設定を下位に持たせます。
TOML から読む補助 API は用意しますが、TOML 形式を内部表現にしません。

公開候補:

```python
class AppConfig:
    endpoint: EndpointConfig
    browser: BrowserConfig
    yostar_email: YostarEmailConfig | None
```

方針:

- `AppConfig()` でローカル一体構成の default を作れる
- remote browser host も同じ config で表現できる
- secret は config に直接持たせない
- Yostar login のメールアドレスや AWS 設定は optional な
  `yostar_email` 設定に置く

## browser host

browser host は CLI と Python API の両方を用意します。

CLI 候補:

```sh
majsoulrpa-browser --client-host 127.0.0.1 --viewport-height 1080 --user-data-dir ./user-data
```

Python API 候補:

```python
from majsoulrpa.browser import run_browser_host

await run_browser_host(config)
```

`run_browser_host()` は、起動に失敗した場合に例外を投げます。起動済みのように
見せる fallback は置きません。

`browser_host` と `client_host` はどちらも「自分」ではなく接続先を表します。
browser host を起動する CLI では、client からの接続先として `--client-host` を
指定します。controller / client 側は `browser_host` へ接続します。

## Presentation / Screen

公開名は `Presentation` より短い `Screen` を候補にします。v2 の概念は
維持しますが、名前互換は考慮しません。

候補:

```python
class Screen:
    @classmethod
    def detection_spec(cls) -> ScreenDetectionSpec: ...
```

画面検出の制御は runtime 側の detector に集約し、Screen は検出に必要な
記述を必ず提供します。custom screen を書くユーザーは、操作 API と
`detection_spec()` を同じ class に置けます。`Screen` は ABC とし、
`detection_spec()` が `None` を返す設計にはしません。

標準 screen 候補:

- `LoginScreen`
- `HomeScreen`
- `FriendlyRoomScreen`
- `TournamentLobbyScreen`

初期実装では `LoginScreen` の API を 1 つだけ選びます。

`LoginScreen.enter_email_address()` に入る前に、まず `LoginScreen` に到達したかを
判定するテンプレート照合を実装します。照合結果は score と `Region` を持つ
`TemplateMatchResult` とし、`Region` は将来の画面クリックや固定領域指定にも使います。
詳細は [テンプレート照合設計メモ](template-matching.md) を参照します。

## 操作 API

操作 API は、その画面で意味があるものだけに限定します。

`LoginScreen` 候補:

```python
async def enter_email_address(self, email_address: str) -> None: ...
async def enter_verification_code(self, code: str) -> None: ...
```

`HomeScreen` 候補:

```python
async def stop(self, *, close_browser: bool = False) -> None: ...
async def close_notifications(self) -> None: ...
```

`FriendlyRoomScreen` 候補:

```python
async def join_room(self, room_code: str) -> None: ...
async def create_room(self, settings: RoomSettings) -> CreatedRoom: ...
```

`TournamentLobbyScreen` 候補:

```python
async def enter_lobby(self, tournament_id: str) -> None: ...
```

これらは候補であり、一度に実装しません。高レベル API は 1 つ実装するごとに
ユーザーの実ゲーム確認を挟みます。

## Sniffer hook

WebSocket sniffer は、raw payload をユーザーが確認できる形にします。

候補:

```python
@dataclass(frozen=True)
class RawNotice:
    direction: Direction
    name: str
    payload: bytes
    observed_at: datetime


@dataclass(frozen=True)
class RawRequestResponse:
    request_direction: Direction
    name: str
    request: bytes
    response: bytes
    request_observed_at: datetime
    response_observed_at: datetime
```

方針:

- browser host で対応検証済みの Notice または Req/Res event を渡す
- wire 用の base64 publication model は公開せず、RPA client で bytes に戻す
- decode 済み event は対応する raw event を `raw` field に保持する
- raw event と decode 済み event のどちらを購読するかは hook 登録時に明示する
- user hook とファイル保存処理は RPA client 側で実行する
- raw payload はデバッグ用ログへ出してよい
- tests、examples、docs、fixtures、commits に実 payload を入れない
- synthetic payload で自動テストする
- decode 失敗を成功扱いにしない

PUB/SUB は永続配送を保証しない。client hook は sequence gap を検出して失敗できるが、
欠落 payload を再送できない。完全な保存保証が必要になった場合は browser host 側の
専用 `CaptureSink` または replay / ack 付きtransportを別途設計し、通常hookへ暗黙の
fallbackを追加しない。

Req/Res 対応検証と二段階 decode の詳細は
[WebSocket Sniffer 設計](sniffer-design.md) を参照します。

## Optional integration

Yostar login のメール取得、AWS S3、protocol decode は optional integration として扱います。

方針:

- core runtime の必須依存にしない
- secret を config repr/log に出さない
- 実メールや credential を tests/examples に入れない
- integration ごとに optional dependency を分ける

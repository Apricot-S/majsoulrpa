# 公開 API 草案

この文書は v3 の最初の公開 API 候補を整理する草案です。実装時に
テストリストと照合して変更してよいですが、変更する場合は理由を残します。

## 設計判断

- callback 登録を主 API とする
- callback は `async def` のみ受け付ける
- 同じ Presentation class への callback 登録は 1 つだけ許す
- 重複登録は起動時ではなく登録時に例外にする
- callback の戻り値を次の state とする
- state はフレームワークが解釈、保存、serialize、log しない
- 未登録 Presentation は検出しても dispatch しない
- detection timeout と操作 timeout は分ける

同じ Presentation に複数 callback を登録できると、state の更新順序と例外時の
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
async def login(screen: LoginScreen, state: State) -> State:
    await screen.enter_email_address(state.email_address)
    code = await state.code_provider.fetch()
    await screen.enter_verification_code(code)
    return state


@app.on(HomeScreen)
async def home(screen: HomeScreen, state: State) -> State:
    await screen.stop(close_browser=True)
    return state


result = await app.run(AppConfig(), state, detection_timeout=60)
```

## `RPAApp`

責務:

- Presentation class と callback の対応を保持する
- client runtime を起動する
- 検出された Presentation を callback へ dispatch する
- state の受け渡しを行う
- timeout、cancellation、例外伝播を整理する

公開候補:

```python
class RPAApp:
    def on(self, screen_type: type[ScreenT]) -> CallbackDecorator[ScreenT]: ...

    async def run(
        self,
        config: AppConfig,
        state: StateT,
        *,
        detection_timeout: float | None = None,
    ) -> StateT: ...
```

`run()` は callback が明示的に停止を要求するか、例外が発生するまで loop します。
戻り値は最後の state です。

## `AppConfig`

設定は 1 つの root config にまとめ、browser host と client の設定を下位に持たせます。
TOML から読む補助 API は用意しますが、TOML 形式を内部表現にしません。

公開候補:

```python
class AppConfig:
    endpoint: EndpointConfig
    browser: BrowserConfig
    capture: CaptureConfig
```

方針:

- `AppConfig()` でローカル一体構成の default を作れる
- remote browser host も同じ config で表現できる
- secret は config に直接持たせない
- Yostar login のメールアドレスや AWS 設定は別の optional integration に置く

## browser host

browser host は CLI と Python API の両方を用意します。

CLI 候補:

```sh
majsoulrpa-browser --viewport-height 1080 --user-data-dir ./user-data
```

Python API 候補:

```python
from majsoulrpa.browser import run_browser_host

await run_browser_host(config)
```

`run_browser_host()` は、起動に失敗した場合に例外を投げます。起動済みのように
見せる fallback は置きません。

## Presentation / Screen

公開名は `Presentation` より短い `Screen` を候補にします。v2 の概念は
維持しますが、名前互換は考慮しません。

候補:

```python
class Screen:
    @classmethod
    async def detect(cls, context: ScreenContext) -> bool: ...
```

ただし、`detect()` を public classmethod とするか、runtime 側の detector に
分離するかは実装前に再検討します。custom screen を書きやすくすることを
優先します。

標準 screen 候補:

- `LoginScreen`
- `HomeScreen`
- `FriendlyRoomScreen`
- `TournamentLobbyScreen`

初期実装では `LoginScreen` の API を 1 つだけ選びます。

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

## Capture hook

WebSocket capture は、raw payload をユーザーが確認できる形にします。

候補:

```python
class CaptureHook:
    async def on_websocket_payload(self, payload: bytes, metadata: MessageMetadata) -> None:
        ...
```

方針:

- raw payload はデバッグ用ログへ出してよい
- tests、examples、docs、fixtures、commits に実 payload を入れない
- synthetic payload で自動テストする
- decode 失敗を成功扱いにしない

## Optional integration

Yostar login のメール取得、AWS S3、protocol decode は optional integration として扱います。

方針:

- core runtime の必須依存にしない
- secret を config repr/log に出さない
- 実メールや credential を tests/examples に入れない
- integration ごとに optional dependency を分ける

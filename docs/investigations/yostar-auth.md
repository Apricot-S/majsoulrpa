# 雀魂ログイン認証コード処理の調査結果と実装方針

## 目的

`majsoulrpa` の雀魂ログイン処理において、メールで受信した6桁の認証コードを入力した後、その認証成否を Playwright から確実に検出する。

これまで Playwright のイベント監視で req/rep を捕捉できていなかったため、Chrome / Edge DevTools の Network パネルを用いて実際の通信仕様を確認した。

---

## 調査対象

雀魂の YoStar SDK フロントエンドコード:

```text
https://game.mahjongsoul.com/StreamingAssets/WebGL/YoStarSDK/index.js.txt?v=1782831990
```

認証コード入力欄は6桁の数字を受け付ける。

```text
\d{6}
```

6桁目の入力後、ログインボタンをクリックすると認証 API へのリクエストが送信される。

---

## DevTools で確認した通信仕様

### エンドポイント

```text
POST https://jp-sdk-api.yostarplat.com/yostar/get-auth
```

### Request Payload

```json
{
  "Account": "<メールアドレス>",
  "Code": "<入力した6桁の認証コード>"
}
```

### HTTP ステータス

認証成功時、認証コード誤り時のどちらも HTTP ステータスは以下だった。

```text
200 OK
```

したがって、HTTP ステータスだけでは認証成否を判定できない。

---

## 成功レスポンス

```json
{
  "Code": 200,
  "Data": {
    "UID": "<メールアドレス>",
    "Token": "<トークン文字列>",
    "Account": "<メールアドレス>"
  },
  "Msg": "OK"
}
```

### 成功判定

最低限、以下を満たす場合に認証成功と判定する。

```python
payload.get("Code") == 200
```

より厳密には、`Data.Token` が空でない文字列であることも確認する。

```python
payload.get("Code") == 200 and bool(payload.get("Data", {}).get("Token"))
```

---

## 認証失敗レスポンス

認証コードが誤っている場合、以下のレスポンスを確認した。

```json
{
  "Code": 100303,
  "Data": {},
  "Msg": "获取授权信息失败,错误代码:%!d(string=4)"
}
```

`Code == 100303` は今回の観測では認証コード誤り時に返された。

ただし、このコードが以下も包含する可能性がある。

- 認証コードの期限切れ
- 使用済みコード
- アカウントとの不一致
- その他の認証拒否

そのため、内部例外名やユーザー向けメッセージでは、単純な「コード誤り」よりも「認証拒否」として扱う方が安全である。

---

## Playwright での捕捉方法

この通信は通常の HTTP POST であり、Playwright の `response` イベントで捕捉できる。

対象ページから通信が発生している限り、以下で捕捉可能。

```python
page.on("response", callback)
```

BrowserContext 全体を監視する場合は以下でもよい。

```python
context.on("response", callback)
```

### Page と BrowserContext の使い分け

#### `page.on("response", ...)`

- 対象の `Page` に属する通信を監視する
- iframe 内の通信も通常は、その iframe を所有する `Page` のイベントとして通知される
- ログイン処理が単一ページ内で完結するなら十分

#### `context.on("response", ...)`

- 同じ BrowserContext 内のすべての Page を監視する
- popup、別タブ、別ウィンドウを含めて捕捉しやすい
- 調査段階や、通信元 Page が不明な場合に有効

今回の認証 UI が同じ雀魂ページ内で動作しているなら、`page.on("response", ...)` で捕捉できる。

ただし、認証コード入力処理の戻り値として成否を返したい場合、常設イベントリスナーよりも `expect_response()` の方が自然である。

---

## 推奨実装方針

認証コードを入力する操作と、その結果となる `get-auth` レスポンスの待機を一体化する。

### 推奨 API

```python
page.expect_response(...)
```

### 理由

`page.on("response", ...)` は継続的なイベント購読には向いているが、以下の点で認証処理には扱いにくい。

- コールバック内の例外を呼び出し元へ直接返しにくい
- 認証コード入力処理と結果判定の対応関係を別途管理する必要がある
- 一度だけ発生するレスポンスのために状態管理が必要になる
- リスナー解除漏れや重複登録のリスクがある

`expect_response()` なら、認証コード入力によって発生する1回のレスポンスを直接待機できる。

---

## 推奨コード例

```python
from typing import Any

from playwright.async_api import Page, Response

AUTH_URL = "https://jp-sdk-api.yostarplat.com/yostar/get-auth"


class AuthenticationError(Exception):
    """Base exception for authentication failures."""


class AuthenticationRejectedError(AuthenticationError):
    """The authentication API rejected the supplied authentication code."""


class AuthenticationProtocolError(AuthenticationError):
    """The authentication API returned an unexpected HTTP or JSON response."""


async def submit_authentication_code(
    page: Page,
    code_input,
    authentication_code: str,
) -> dict[str, Any]:
    async with page.expect_response(
        lambda response: (
            response.url == AUTH_URL and response.request.method == "POST"
        ),
        timeout=15_000,
    ) as response_info:
        await code_input.fill(authentication_code)

    response: Response = await response_info.value

    if response.status != 200:
        raise AuthenticationProtocolError(
            f"Authentication API returned HTTP {response.status}."
        )

    try:
        payload = await response.json()
    except Exception as exc:
        raise AuthenticationProtocolError(
            "Authentication API returned a non-JSON response."
        ) from exc

    if not isinstance(payload, dict):
        raise AuthenticationProtocolError(
            "Authentication API returned an unexpected JSON value."
        )

    code = payload.get("Code")
    data = payload.get("Data")

    if code != 200:
        raise AuthenticationRejectedError(
            "Authentication was rejected: "
            f"code={code!r}, message={payload.get('Msg')!r}"
        )

    if not isinstance(data, dict):
        raise AuthenticationProtocolError(
            "Authentication success response does not contain a Data object."
        )

    token = data.get("Token")

    if not isinstance(token, str) or not token:
        raise AuthenticationProtocolError(
            "Authentication success response does not contain a valid token."
        )

    return payload
```

---

## URL 判定方針

完全一致でも現状は問題ない。

```python
response.url == AUTH_URL
```

ただし、将来的にクエリパラメーターが付与される可能性を考慮するなら、ホスト名とパスで判定してもよい。

```python
from urllib.parse import urlparse

from playwright.async_api import Response


def is_auth_response(response: Response) -> bool:
    parsed = urlparse(response.url)

    return (
        response.request.method == "POST"
        and parsed.hostname == "jp-sdk-api.yostarplat.com"
        and parsed.path == "/yostar/get-auth"
    )
```

現時点では完全 URL 一致の方が単純で明確である。

---

## リクエスト Payload まで条件に含めるべきか

Playwright では以下も確認可能。

```python
request_payload = response.request.post_data_json
```

例:

```python
def is_auth_response(response: Response) -> bool:
    if response.url != AUTH_URL:
        return False

    if response.request.method != "POST":
        return False

    try:
        payload = response.request.post_data_json
    except Exception:
        return False

    return (
        isinstance(payload, dict)
        and isinstance(payload.get("Account"), str)
        and isinstance(payload.get("Code"), str)
        and len(payload["Code"]) == 6
        and payload["Code"].isdigit()
    )
```

ただし、通常は URL と HTTP メソッドだけで十分である。

Payload の構造まで条件に含めると、YoStar SDK 側のフィールド変更に弱くなるため、実装では避ける方がよい。

---

## イベント監視を使う場合

継続監視やデバッグ用途では、`page.on("response", ...)` でも捕捉できる。

```python
from playwright.async_api import Response

AUTH_URL = "https://jp-sdk-api.yostarplat.com/yostar/get-auth"


async def on_response(response: Response) -> None:
    if response.url != AUTH_URL:
        return

    if response.request.method != "POST":
        return

    try:
        payload = await response.json()
    except Exception:
        return

    code = payload.get("Code")

    if code == 200:
        print("Authentication succeeded.")
    else:
        print(
            "Authentication rejected:",
            code,
            payload.get("Msg"),
        )


page.on("response", on_response)
```

ただし、本番の認証フローでは `expect_response()` を優先する。

---

## 例外設計

以下の2種類は分ける。

### `AuthenticationRejectedError`

API との通信と JSON 解析には成功したが、API が認証を拒否した場合。

例:

```json
{
  "Code": 100303,
  "Data": {},
  "Msg": "..."
}
```

### `AuthenticationProtocolError`

通信またはレスポンス形式が想定外だった場合。

例:

- HTTP 200 以外
- JSON ではない
- JSON のトップレベルが object ではない
- `Code == 200` なのに `Data` が object ではない
- `Code == 200` なのに `Token` がない
- `Token` が空文字列または文字列ではない

これにより、ユーザー入力の問題と、SDK/API変更や通信異常を区別できる。

---

## タイムアウト

認証コード入力後のレスポンス待機には、明示的なタイムアウトを設定する。

```python
timeout = 15_000
```

タイムアウトは `AuthenticationProtocolError` とは別に、Playwright の `TimeoutError` をそのまま上位へ伝播させるか、認証用例外へ変換する。

例:

```python
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

try:
    async with page.expect_response(..., timeout=15_000) as response_info:
        await code_input.fill(authentication_code)
except PlaywrightTimeoutError as exc:
    raise AuthenticationProtocolError(
        "Timed out while waiting for the authentication response."
    ) from exc
```

---

## ログ出力に関する注意

以下は機密情報として扱う。

- 認証コード
- メールアドレス
- `UID`
- `Account`
- `Token`
- Request Payload 全体
- Response JSON 全体

以下のようなログは避ける。

```python
logger.debug("Authentication response: %r", payload)
```

代わりに、必要な情報だけを記録する。

```python
logger.debug(
    "Authentication response received: code=%r, has_token=%s",
    payload.get("Code"),
    bool(payload.get("Data", {}).get("Token")),
)
```

認証失敗時の `Msg` はサーバ実装由来の文字列であり、ユーザー向け表示や安定した判定条件としては使わない。

---

## 成功判定の最終条件

推奨する認証成功条件は以下。

```python
success = (
    response.status == 200
    and payload.get("Code") == 200
    and isinstance(payload.get("Data"), dict)
    and isinstance(payload["Data"].get("Token"), str)
    and bool(payload["Data"]["Token"])
)
```

`Msg == "OK"` は文言変更やローカライズの影響を受ける可能性があるため、必須条件にしない。

---

## 実装時のテスト方針

実サイトへ接続しない単体テストでは、以下をモックまたは Fake で再現する。

### 正常系

- HTTP 200
- JSON `Code == 200`
- `Data.Token` が空でない文字列

### 認証拒否

- HTTP 200
- JSON `Code == 100303`
- `Data == {}`
- `AuthenticationRejectedError` が発生する

### プロトコル異常

- HTTP 500
- JSON でない
- JSON が list
- `Code` がない
- `Code == 200` だが `Data` がない
- `Code == 200` だが `Token` がない
- `Token == ""`
- `Token` が文字列でない

### タイムアウト

- `get-auth` レスポンスが発生しない
- 認証用のタイムアウト例外へ変換される

---

## 実装時の確認事項

1. 既存のログイン画面実装を確認する。
2. 認証コード入力直前に `page.expect_response()` を設定する。
3. 以下の通信だけを対象にする。

   ```text
   POST https://jp-sdk-api.yostarplat.com/yostar/get-auth
   ```

4. 認証コード入力操作を `expect_response()` の context manager 内で実行する。
5. HTTP ステータスだけではなく、レスポンス JSON の `Code` を確認する。
6. `Code == 200` かつ非空の `Data.Token` が存在する場合のみ成功とする。
7. `Code != 200` は認証拒否用例外にする。
8. HTTP 異常、JSON 異常、レスポンス構造異常はプロトコル用例外にする。
9. 認証コード、メールアドレス、Token、レスポンス全体をログに出さない。
10. 正常系、認証拒否、レスポンス構造異常、タイムアウトのテストを追加する。
11. `page.on("response", ...)` はデバッグ用途または継続監視用途に限定し、本処理では `expect_response()` を優先する。

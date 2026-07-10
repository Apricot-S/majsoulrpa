# 認証コード後のログインフロー計画

## 目的と範囲

`LoginScreen.enter_verification_code()` の後に続く、認証コードの成否判定、
利用規約同意画面の操作、ログイン画面からの遷移を段階的に実装する。

この計画では実装を行わない。実装は高レベル API を 1 つずつ追加し、各段階で
ユーザーによる実際の雀魂での手動確認を挟む。

認証コード、メールアドレス、Cookie、token、HTTP response body、実画面の
スクリーンショットは、テスト、fixture、ログ、ドキュメント、コミットに含めない。

## 1. 認証コード誤りの判定

手動調査により、認証コード送信時に次の HTTP request が発生し、Playwright の
`response` event で観測できることを確認した。

```text
POST https://jp-sdk-api.yostarplat.com/yostar/get-auth
```

成功時と拒否時はいずれも HTTP status 200 であるため、status だけでは判定しない。
JSON response の `Code` と、成功時の `Data.Token` の存在を browser host 内で確認する。
観測内容の詳細は
[雀魂ログイン認証コード処理の調査結果](majsoulrpa_yostar_auth_investigation.md) を参照する。

### Sniffer との分離

既存の Sniffer は、長時間流れる WebSocket frame を観測し、raw payload や metadata を
ユーザー hook へ渡すための仕組みである。今回の HTTP response は次の性質が異なる。

- ログインボタンの click と 1 対 1 に対応する、一度限りの内部制御結果である。
- click より前に待機を開始しなければ response を取り逃がす可能性がある。
- response にメールアドレスと token が含まれ、raw payload を外部へ渡す必要がない。
- LoginScreen API の成否へ同期的に反映する必要がある。

このため、HTTP method を既存 Sniffer に追加しない。WebSocket Sniffer は従来の責務に
限定し、認証 HTTP は browser command の request-scoped な待機処理として実装する。
汎用 HTTP capture hook や別の常設 event transport も、この API のためには追加しない。

### browser host 側の処理

現在の browser transport は REQ/REP で command を逐次処理する。response 待機と click を
別 command にすると、待機開始前に response が返る race が生じる。そのため、次の処理を
1 つの内部 command として browser host で不可分に実行する。

1. `POST` と完全一致 URL を条件に `page.expect_response()` を開始する。
2. LoginScreen が指定した座標を click する。
3. 上限時間内に対象 response を待つ。
4. HTTP status と JSON schema を検証する。
5. secret を除いた認証結果だけを RPA client へ返す。

内部 command の候補名は `ClickAndWaitForYostarAuthCommand` とする。汎用 command に見せる
ための JSON path 指定や raw body response は導入しない。雀魂固有であることを型名に出し、
用途を認証フローに限定する。

response は次の判別可能な型に分ける。

- accepted: HTTP 200、`Code == 200`、`Data.Token` が非空文字列
- rejected: HTTP 200、`Code != 200`
- browser error: timeout、HTTP status 異常、JSON decode 失敗、schema 異常、
  `Code == 200` だが有効な token がない

accepted response に token 自体を含めず、token が有効だったという結果だけを返す。
rejected response は必要なら数値の application code を含めてよいが、`Msg`、メールアドレス、
request payload、response JSON は transport、例外、ログへ出さない。

### LoginScreen 側の扱い

`enter_verification_code()` は認証コード欄への入力と 0.5 秒待機までは現在どおり行い、
最後の login click を新しい atomic browser operation に置き換える。

- accepted は正常終了し、次の同意画面処理へ進める。
- rejected は screenshot 付き `ScreenInvalidArgumentError` に変換する。message は
  「認証コードが拒否された」ことを表し、単純な入力間違いと断定しない。
- timeout と protocol error は不正引数扱いにせず、browser operation error を伝播する。
- response を受け取れなかった場合を成功扱いにしない。

## 2. 正しい認証コード後の同意画面

認証コードが正しい場合は、利用規約同意画面へ遷移したことを確認してから
チェックボックスを操作する。固定座標だけでは遷移失敗時に別画面を操作し得るため、
同意画面固有のテンプレート照合を前提とする。

必要な資産と確認:

- チェックボックスまたは同意画面の安定した非個人情報領域をテンプレート候補として選ぶ。
- テンプレート画像と設定はユーザーにコミットを依頼して追加する。
- `LoginScreen` の class 定数として matcher を保持する。
- 認証コード送信後、同意画面 template の出現を上限時間付きで待機する。
- 検出できた checkbox の match region をクリックする。チェック済み状態を区別する必要が
  あるかは手動確認で決める。

この段階の API は、認証コード入力と checkbox 操作を混在させず、成功画面の検出が
安定してから 1 つの高レベル API として確定する。

## 3. 同意ボタンと遷移完了

checkbox と同意ボタンをクリックした後の完了判定は、画面検出を第一候補とする。
遷移先として `HomeScreen` を検出できるテンプレートが取得できれば、runtime が次の
callback を dispatch でき、ログイン固有の通信に依存しない。

認証 HTTP の accepted は認証コードの受理だけを表す。同意後の画面遷移完了には使わず、
通信成功だけで画面操作の完了扱いにはしない。

必要な資産と確認:

- 同意画面の同意ボタン用 region を、画面 template の match region または確定した
  `Region` として定義する。
- 遷移先画面の非個人情報 template と settings をユーザーにコミットしてもらう。
- 画面遷移の待機は timeout を持ち、timeout を成功扱いにしない。
- 遷移先の Screen が検出できることを、実ゲームでユーザーに確認してもらう。

## 4. stale Screen の共通管理

画面遷移が完了した `LoginScreen` は、以後その画面で意味を持つ操作を受け付けない。
この状態は `LoginScreen` 固有の一時フラグではなく、`Screen` 基底クラスで一貫して扱う。

設計:

- `Screen` に `_stale: bool`、`_mark_stale()`、`_ensure_active()` を置く。
- `_ensure_active()` は stale の場合、現在の screenshot を添えた
  `ScreenStaleError` を送出する。`ScreenStaleError` は
  `ScreenInvalidOperationError` の派生とし、既存の不正操作 catch と互換にする。
  screenshot 取得失敗は握りつぶさない。
- 基底クラスに `@requires_active` decorator を置き、public async Screen API の先頭で
  `_ensure_active()` を await する。
- `Screen` 自身の public helper と各 Screen subclass の public 操作 API に decorator を
  明示的に適用する。private helper、`detection_spec()`、constructor には適用しない。
- 画面遷移を起こす API が正常完了した時点で `_mark_stale()` を呼ぶ。現在の
  `enter_verification_code()` では、認証、checkbox 1、checkbox 2、同意ボタンの操作が
  すべて成功した直後に stale とする。途中の例外や認証拒否では stale にしない。

decorator は重複を減らすための内部実装であり、Screen の public API 契約を曖昧にしない。
新しい public 操作を追加する際に decorator の適用漏れを防ぐため、基底 helper と
`LoginScreen` の操作を対象に回帰テストを置く。

## 実装順序

1. atomic browser command と response 型を synthetic data だけで TDD 実装する。
2. Playwright executor が response 待機を click より先に開始することを fake page で固定する。
3. `LoginScreen` が rejected result を不正引数エラーへ変換する。
4. ユーザーに実際の雀魂で accepted / rejected の両方を手動確認してもらう。
5. 同意画面と遷移先画面の template 候補を選定し、必要な資産のコミットをユーザーに依頼する。
6. `Screen` の stale 共通基盤を、対象 API の実装前に TDD で追加する。
7. checkbox 操作、同意後遷移をそれぞれ別の高レベル API 単位で
   実装し、品質ゲート後に毎回手動確認する。

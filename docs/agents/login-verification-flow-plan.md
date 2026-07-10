# 認証コード後のログインフロー計画

## 目的と範囲

`LoginScreen.enter_verification_code()` の後に続く、認証コードの成否判定、
利用規約同意画面の操作、ログイン画面からの遷移を段階的に実装する。

この計画では実装を行わない。実装は高レベル API を 1 つずつ追加し、各段階で
ユーザーによる実際の雀魂での手動確認を挟む。

認証コード、メールアドレス、Cookie、token、HTTP response body、実画面の
スクリーンショットは、テスト、fixture、ログ、ドキュメント、コミットに含めない。

## 1. 認証コード誤りの判定

画面上のエラー表示は安定して検出できるか未確認である。そのため最初に
Playwright の HTTP response event で、認証コード送信に対応する response を
観測できるか spike する。

spike の判定基準:

- 認証コード送信後の候補 response を、URL、HTTP method、status、content type などの
  secret を含まない metadata で識別できる。
- response が認証コード誤りと成功を区別できる情報を持つ。
- browser host の page lifecycle とともに observer を開始・停止できる。
- fake response event だけで自動テストできる狭い境界を設計できる。
- 実 response body や認証コードを保存・出力せずに手動確認できる。

Playwright で必要な情報が得られない、または候補 request を安定して識別できない場合は、
HTTP 傍受を本実装に採用しない。その場合は画面テンプレートによる検出を再検討し、
mitmproxy の導入はこの spike の失敗だけを理由に決めない。

採用できた場合の API 方針:

- 誤りを示す response を受けたとき、`enter_verification_code()` は
  `ScreenInvalidArgumentError` を送出する。
- 例外 message、ログ、response summary に認証コード、メールアドレス、response body を
  含めない。
- observer timeout と通信失敗は認証コード誤りとして扱わず、別の明示的な失敗にする。

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

HTTP response が明確にログイン完了を表し、かつ 1 の spike で observer 境界が有効と
確認できた場合だけ、画面検出の補助として通信判定を使う。通信成功だけで画面操作の
完了扱いにはしない。

必要な資産と確認:

- 同意画面の同意ボタン用 region を、画面 template の match region または確定した
  `Region` として定義する。
- 遷移先画面の非個人情報 template と settings をユーザーにコミットしてもらう。
- 画面遷移の待機は timeout を持ち、timeout を成功扱いにしない。
- 遷移先の Screen が検出できることを、実ゲームでユーザーに確認してもらう。

## 4. stale Screen の共通管理

画面遷移が完了した `LoginScreen` は、以後その画面で意味を持つ操作を受け付けない。
この状態は `LoginScreen` 固有の一時フラグではなく、`Screen` 基底クラスで一貫して扱う。

候補設計:

- `Screen` に `_stale: bool`、`_mark_stale()`、`_ensure_active()` を置く。
- `_ensure_active()` は stale の場合、現在の screenshot を添えた
  `ScreenInvalidOperationError` を送出する。screenshot 取得失敗は握りつぶさない。
- 基底クラスに `@requires_active` decorator を置き、public async Screen API の先頭で
  `_ensure_active()` を await する。
- `Screen` 自身の public helper と各 Screen subclass の public 操作 API に decorator を
  明示的に適用する。private helper、`detection_spec()`、constructor には適用しない。
- 同意ボタン後に遷移先が確認できた時点でだけ `_mark_stale()` を呼ぶ。通信送信直後や
  timeout 時には stale にしない。

decorator は重複を減らすための内部実装であり、Screen の public API 契約を曖昧にしない。
新しい public 操作を追加する際に decorator の適用漏れを防ぐため、基底 helper と
`LoginScreen` の操作を対象に回帰テストを置く。

## 実装順序

1. HTTP response observer の fake による境界テストを書き、Playwright API で実現可能かを
   spike する。結果をこの文書へ追記する。
2. ユーザーによる手動確認で、誤り response と成功 response を metadata のみで
   区別できるか検証する。実データは保存しない。
3. 同意画面と遷移先画面の template 候補を選定し、必要な資産のコミットをユーザーに依頼する。
4. `Screen` の stale 共通基盤を、対象 API の実装前に TDD で追加する。
5. 認証コード誤りの例外化、checkbox 操作、同意後遷移をそれぞれ別の高レベル API 単位で
   実装し、品質ゲート後に毎回手動確認する。

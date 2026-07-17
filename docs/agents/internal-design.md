# 内部設計方針

## 基本姿勢

MajsoulRPA は、過剰な抽象化や定型的な「クリーンアーキテクチャ」風の層分けを避けます。
抽象化は、テスト容易性、置換可能性、ライフサイクル管理のいずれかに
明確な価値がある場合だけ導入します。

## 境界の候補

以下は概念上の境界です。パッケージ名やクラス名は実装時に改めて決めます。

- Public API: callback 登録、config、主要 Presentation
- Browser runtime: Playwright 起動、browser context、page lifecycle
- Client runtime: Presentation 検出、callback dispatch、data 受け渡し
- Presentation: 画面検出と画面操作
- Sniffer: WebSocket message の継続観測、decode、ユーザー hook
- Browser HTTP wait: 画面操作に対応する一度限りの HTTP response 待機
- Login support: Yostar login code provider などの optional 機能
- Test support: fake browser、fake screen、synthetic capture

## 採用してよい抽象化

次のような場合は抽象化してよいです。

- fake 実装に置き換えることで自動テストが大きく簡単になる
- Playwright と mitmproxy のように、実際に複数実装を比較する必要がある
- 起動、停止、異常終了、後始末を 1 箇所で管理する必要がある
- ユーザー拡張点として明確に公開する

## 避ける抽象化

次のような抽象化は避けます。

- 実装が 1 つしかなく、置換予定もない interface
- DTO と mapper だけが増える層
- 単なるファイル分割のための service / usecase / repository
- private 実装を隠すためだけの facade
- 例外や戻り値を曖昧にする wrapper

## ライフサイクル

ライフサイクルは明示的に扱います。

- browser host の起動と停止
- client runtime の開始と終了
- WebSocket capture の開始と停止
- callback dispatch 中の cancellation
- 終了時の browser close
- 異常終了時の cleanup

終了処理で失敗した場合も、失敗を見えない形にしません。複数の失敗が起きる
可能性がある箇所では、どの失敗を主例外として扱うかをテストで固定します。

## Presentation 検出

Presentation 検出は、画面状態を「できるだけ決定的に」扱います。

方針:

- 固定 sleep だけで安定化しない
- 画像認識、DOM 情報、通信情報のどれを使うかは画面ごとに判断する
- 検出 timeout と、呼び出し側の `asyncio.timeout()` で管理する操作期限を混同しない
- 未登録 Presentation は dispatch しない
- 同時に複数 Presentation が成立する場合の優先順位を明示する

## Screen の stale 状態

検出済みの `Screen` instance が画面遷移後も利用されることを防ぐため、`Screen` 基底
class が active / stale 状態を保持する。public async Screen API は共通 decorator で
実行前に状態を検証し、stale の場合は screenshot 付き `ScreenStaleError` を送出する。

`ScreenStaleError` は `ScreenInvalidOperationError` の派生とし、stale を個別に処理する
利用者と、不正操作をまとめて処理する利用者の両方を許容する。

画面遷移を起こす API は、必要な操作がすべて正常に完了した時点でだけ instance を stale
にする。操作失敗、timeout、通信拒否などの例外経路では stale にしない。stale 判定用の
screenshot 取得に失敗した場合も、その失敗を握りつぶさない。

`Screen.reload()` はbrowser reloadが正常完了した直後に現在のinstanceをstaleにする。
reload後に同じ種類の画面へ戻った場合も、runtimeが新しく検出したScreen instanceを使う。

## Client session state

account IDはmessage queueや個別Screenではなく、RPA client runtimeが所有するsession stateで
管理する。Sniffer publicationをdecodeした直後、内部queueへ投入する前にsession stateへ
messageを観測させる。これによりScreenがmessageを読む前や、後続処理がqueueを読み捨てた
場合でも取得済みaccount IDを保持できる。

初期値は`None`とし、`.lq.Lobby.oauth2Login`の`response.account_id`または
`.lq.Lobby.createRoom`の`response.room.owner_id`から正の`int`を取得する。同じ値の再観測は
許容し、異なる値はsession整合性エラーにする。`ScreenContext.account_id`はsession stateの
現在値を読み取り専用で公開する。

### Room state

`RoomScreen` 導入時も、room message は既存の `SnifferMessageSource` から Screen が逐次読む。
account ID と異なり、decode 直後かつ内部 queue 投入前の observer へ room 状態機械を追加しない。
RoomScreen の callback と API は同時実行されず、source が未処理 message を到着順に保持するため、
host 交代や kick も操作前 refresh または状態待機で処理できる。Room 専用 thread や Screen
instance ごとの background task は追加しない。

runtime は callback loop ごとに新しい Screen instance を生成するため、最新の immutable room
snapshot と room generation だけは具体的な `RoomStateCache` として `ScreenContext` 経由で共有
する。cache は RoomScreen が source を読んだときだけ更新し、raw message 履歴、operation
response、waiter を保持しない。汎用 event sourcing store や Screen state registry は作らない。
`ScreenContext` は protobuf object や ZMQ socket の具体型を `RoomScreen` へ公開しない。

初期 snapshot は `createRoom`、`joinRoom`、`fetchRoom` response、更新は room notice から得る。
host 権限は owner ID と session account ID から snapshot ごとに導出し、Screen instance へ
cache しない。詳しい状態遷移、操作との相関、失敗モデルは
[RoomScreen 設計](room-screen-design.md) に従う。

## 高レベル Screen API のログ

通常ユーザーが callback から直接利用する高レベル Screen API は、呼び出し時に
`majsoulrpa.screens.api` logger の info log を出す。Screen 名と API 名だけを記録し、
引数、戻り値、user data は記録しない。

高レベル API は共通 decorator で明示する。`ContextVar` で async task ごとの呼び出し
深度を管理し、高レベル API 内部から別の高レベル API を呼んだ場合は最外周だけを
記録する。stale や validation error で失敗する呼び出しも、呼び出された事実は記録する。

`Screen` では `screenshot`、`reload`、`goto_log`、`stop_browser_host`、`stop_rpa` を対象とする。
継承先では、callback 利用者向けに追加された一連の操作 API を対象とする。region 操作、
template 操作、framework hook、private helper は対象外とする。

## Browser 操作

ブラウザ操作は、通信層と操作 API 層を分けます。

- `BrowserClientTransport`: client から browser host への `send_command` /
  `recv_response` を担当する
- `BrowserServerTransport`: browser host が `recv_command` / `send_response` で
  request loop と接続する
- `RemoteBrowserController`: `click` や `input_text` などの操作 API を client transport 上の
  command / response に変換する
- command / response は pydantic の判別共用体で表現する
- browser host へ送る command は `Region` ではなく、click 座標や入力テキストなどの
  低レベル情報にする
- response は click result、text input result、error result を別型にする
- click result と text input result は、必要に応じて BASE64 screenshot や実際に
  クリックした座標などを持つ
- browser host 側は request を受け取り、command executor に渡して response を返す
  loop を持つ
- request/response loop は実 network transport と分離し、fake transport で自動テストする
- 実 network server は request/response loop の挙動を固定した後で追加する
- request server は `BrowserRequestServer` protocol として `bind` / `serve_forever` /
  `stop` の lifecycle を持つ
- ZeroMQ transport は REQ/REP の 1 request / 1 response とし、同じ command / response
  schema を JSON bytes として送受信する
- ZeroMQ request server は REP socket を bind し、`BrowserZmqServerTransport` を
  request handler に渡す
- endpoint host 名は自分自身ではなく接続先を表す。browser host 側は
  client からの接続を受けるため `client_host` に bind し、controller / client
  側は `browser_host` に connect する
- `ScreenContext`: 現在の Screen 実行に必要な browser controller、viewport、stop request
  を束ねる
- `Screen`: `fill_region` など、継承先の画面 API が使う共通 helper を持つ

`ScreenContext` は browser 操作層そのものではありません。runtime から Screen へ
実行時依存を渡すための context です。実際の遠隔操作プロトコルや send/recv は
browser package 側に閉じ込めます。

## Browser HTTP response 待機

画面操作の成否が HTTP response でのみ確実に判定できる場合、response 待機は
browser host の command execution に置く。RPA client から click した後に別 command で
response を待つ構成は、待機開始前に response を取り逃がすため採用しない。

Yostar 認証では `page.expect_response()` の開始、login click、response 検証を 1 command
として実行する。認証 response の raw JSON は browser host の外へ出さず、application code
と token の存在確認から得た secret を含まない結果だけを transport response にする。

この処理は WebSocket Sniffer へ追加しない。Sniffer は継続観測とユーザー hook、HTTP wait は
単一画面操作の同期的な完了確認であり、lifecycle と公開範囲が異なるためである。

## 画像・テンプレート資産

画像資産は、必要性と安全性を確認してから追加します。

必要になった場合:

- どの API に必要かを説明する
- 画像と設定を対で扱う
- ユーザーにコミットを依頼する
- 実アカウントや個人情報が写らないことを確認する

テンプレート照合は OpenCV と numpy で実装します。テストのためだけに Pillow は
追加しません。詳細は [テンプレート照合設計メモ](template-matching.md) に従います。

画面上の矩形は `Region` として表現します。`Region` はテンプレート照合結果だけでなく、
固定領域クリックや入力欄探索にも使う共通の値オブジェクトです。TOML から読む設定値は
pydantic model で検証し、実行時の値として immutable な `Region` に変換します。

## protocol 生成物

`.proto` や生成済み Python ファイルは、必要になった時点で扱います。

方針:

- 手編集しない
- 生成手順を docs に残す
- 生成物が必要なテストは synthetic payload を使う
- 実通信 payload を fixture にしない

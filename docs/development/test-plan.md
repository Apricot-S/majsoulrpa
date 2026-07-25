# 初回テストリスト

このテストリストは、実装開始前に用意する最初のリストです。
実装中に見つかった項目は追加します。TDD では、この中から 1 つだけ選んで
テストを書き、そのテストを通す最小実装を行います。

## Phase 1: 空のプロジェクト骨格

- [x] package を import できる
- [x] `majsoulrpa.__version__` の扱いを決め、テストする
- [x] README が開発状況と安全スコープを説明している
- [ ] Sphinx や古い API docs に依存しない
- [x] `pyproject.toml` の optional dependency group が解決できる
- [x] core import だけでは OpenCV と Playwright を import しない
- [x] `python -m ruff check .` が通る
- [x] `python -m ruff format --check .` が通る
- [x] `python -m ty check` が通る

## Phase 2: config

- [x] `AppConfig()` がローカル一体構成の default を持つ
- [x] TOML から `AppConfig` を作れる
- [x] TOML の未知 key をエラーにする
- [x] endpoint の host が空文字の場合にエラーにする
- [x] port が範囲外の場合にエラーにする
- [x] viewport height が許可値外の場合にエラーにする
- [x] `user_data_dir` が未指定の場合の意味が明確である
- [x] `config.example.toml` が全設定の意味とdefaultをコメントで説明する
- [x] `config.example.toml` を読むと`AppConfig()`と同じ値になる
- [ ] secret に相当する値を config repr に出さない
- [ ] secret に相当する値を validation error に出さない

## Phase 3: browser host lifecycle

- [x] `run_browser_host()` が backend を起動して request server を bind / serve する
- [x] `run_browser_host()` が backend 起動失敗時に例外を返す
- [x] backend 起動失敗を成功扱いにしない
- [x] request server 終了時に backend と server を cleanup する
- [x] cleanup 中の Playwright driver disconnect は Ctrl+C を隠さない
- [x] request loop 中の cancellation で cleanup する
- [x] shutdown 中の副次的失敗を完全には捨てない
- [x] Playwright backend が config から browser context と page を作る
- [x] Playwright backend が雀魂ページへ遷移して canvas selector を 1 分上限で待機する
- [x] Playwright command executor が click、text input、screenshot を実行する
- [x] Playwright command executor の操作失敗は error response にする
- [x] browser host が request command を executor に渡して response を返す
- [x] browser host の request loop は cancellation を伝播する
- [x] browser ZeroMQ transport が REQ/REP で command / response を送受信する
- [x] browser ZeroMQ request server が ZMQ transport で request handler を実行する

## Phase 4: callback dispatch

- [x] `RPAApp.on(Screen)` で async callback を登録できる
- [x] sync callback 登録をエラーにする
- [x] 同じ Screen への重複登録をエラーにする
- [x] 未登録 Screen は dispatch しない
- [x] 登録順に detection を試す
- [x] callback の戻り値が次の data になる
- [x] callback が例外を投げたら `run()` から伝播する
- [x] detection timeout で明示的な例外になる
- [x] Screen 未検出時は timeout まで 0.5 秒間隔で再検出する
- [x] Screen 未検出のまま timeout したら screenshot 付き検出 timeout 例外になる
- [x] callback 実行中の cancellation で cleanup する
- [x] data を log しない

## Phase 5: Screen base

- [x] fake screenshot で Screen を検出できる
- [x] Screen detection が false のとき callback されない
- [x] Screen detection が例外を投げたら隠さない
- [x] 複数 Screen が一致した場合は登録順で選ばれる
- [x] Screen から browser controller 経由で操作できる
- [x] Screen から screenshot を利用者向け API として取得できる
- [x] Screen から browser reload を利用者向け API として実行できる
- [x] reload が正常完了したら現在の Screen instance を stale にする
- [x] Screen から指定した牌譜 ID の URL へ移動できる
- [x] Screen から RPAApp の実行ループ停止を利用者向け API として要求できる
- [x] Screen から browser host の終了を利用者向け API として要求できる
- [x] Screen 検出エラーに screenshot bytes を添付できる
- [x] Screen 検出エラーの screenshot を file path または directory path へ保存できる
- [x] Screen 検出 timeout エラーは `TimeoutError` としても捕捉できる
- [x] Screen API の不正引数は `ScreenInvalidArgumentError` として表す
- [x] Screen API の不正引数エラーは `ValueError` としても捕捉できる
- [x] ScreenContext から stop 要求を出せる
- [x] 検出された Screen に ScreenContext を注入できる
- [x] ScreenContext 未設定の Screen 操作は例外になる
- [x] `Screen` の高レベル API 呼び出しを Screen 名と API 名だけで info log に出す
- [x] `LoginScreen` で追加された高レベル API 呼び出しを info log に出す
- [x] 高レベル API の引数、戻り値、user data を log に出さない
- [x] 高レベル API が内部で別の高レベル API を呼んでも最外周だけ log に出す
- [x] stale や不正引数で失敗する高レベル API 呼び出しも log に出す
- [x] region / template helper、framework hook、private helper は高レベル API log に出さない

## Phase 5.5: Browser 操作層

- [x] client transport は `send_command` と `recv_response` を分ける
- [x] browser controller は `fill_region` を command / response に変換する
- [x] browser controller は `move_mouse` を command / response に変換する
- [x] browser controller は通常 click に固定の hover delay を設定する
- [x] browser controller は `warp=True` の click に hover delay を設定しない
- [x] Screen の region click は warp 指定を browser controller へ渡す
- [x] Playwright の通常 click は move、hover wait、down、down/up wait、up の順に実行する
- [x] Playwright の warp click は速度を優先して `mouse.click()` を使う
- [x] Playwright の通常 click は down 後の cancellation でも mouse up する
- [x] browser controller は `goto_url` を command / response に変換する
- [x] browser controller は `reload` を command / response に変換する
- [x] browser controller は `stop_browser_host` を command / response に変換する
- [x] browser controller は remote error response を例外にする
- [x] browser host へ送る command は click 座標や text など低レベル情報にする
- [x] click command は mouse down/up 間の delay を持つ
- [x] text input command は等間隔の文字入力 delay を持つ
- [x] move mouse command は移動先座標を持つ
- [x] goto url command は遷移先 URL を持つ
- [x] reload command は追加パラメータを持たない
- [x] stop browser host command は response 送信後に request loop を停止する
- [x] browser controller は screenshot command の base64 response を PNG bytes として返す
- [x] response は click、text input、error を別型にする
- [x] browser 操作履歴を client / host 側の debug log に redaction 済み summary として出す

## Phase 5.6: Controller runtime wiring

目的: `RPAApp.run()` の既定経路から remote browser host に接続し、
Screen 検出と Screen 操作で同じ controller を使えるようにする。

タスク:

- [x] controller 側は `AppConfig.endpoint.browser_host` から ZMQ endpoint を作る
- [x] browser host 側は `AppConfig.endpoint.client_host` に bind する
- [x] controller 側で ZMQ context と REQ socket を作成する
- [x] `BrowserZmqClientTransport` と `RemoteBrowserController` を組み立てる
- [x] `ScreenContext` に controller、viewport、stop request を渡す
- [x] Screen 検出用 screenshot provider を controller の screenshot API につなぐ
- [x] runtime 正常終了時に socket / context を閉じる
- [x] callback 例外時に socket / context を閉じる
- [x] cancellation 時に socket / context を閉じる
- [x] remote browser error を成功扱いにしない
- [x] 自動テストでは実ブラウザ、実 ZMQ network、実雀魂にアクセスしない

### Sniffer client message queue

- [x] 全 decode 済み message を到着順に保持する
- [x] `get()` は次の message が来るまで待機して消費する
- [x] `get_nowait()` は未読 message がなければ `None` を返す
- [x] 差し戻した message は通常の未読 message より先に取得する
- [x] 複数の差し戻しは差し戻した順序を保つ
- [x] 件数上限を越えた message を黙って破棄しない
- [x] raw payload bytes 合計の上限超過を黙って破棄しない
- [x] 単一 message が byte 上限を越える場合は明示的に拒否する
- [x] capacity と byte 上限が 0 以下なら拒否する

テスト:

- [x] 既定 `RPAApp.run()` が `browser_host` から controller runtime を作る
- [x] controller endpoint は IPv4 / hostname / IPv6 literal を正しく扱う
- [x] runtime が screenshot command を使って Screen 検出を行う
- [x] 検出された Screen に controller 入りの `ScreenContext` が注入される
- [x] Screen helper から呼ばれた click / text input が remote command になる
- [x] Screen helper から呼ばれた move_region が remote command になる
- [x] detection timeout で Screen 未検出の場合も transport を cleanup する
- [x] callback が例外を投げた場合も transport を cleanup する
- [x] callback 実行中の cancellation でも transport を cleanup する
- [x] remote error response は `BrowserOperationError` として伝播する
- [x] PNG screenshot decode が必要な場合は synthetic PNG のみでテストする

## Phase 6: Login API ひとつ目

最初に実装する高レベル API は、実装直前に 1 つ選びます。
まず `LoginScreen.enter_email_address()` には入らず、画面到達判定のための
テンプレート照合を実装します。

テンプレート照合:

- [x] TOML から `TemplateMatchSettings` を読める
- [x] unknown key を reject する
- [x] region、margin、threshold の不正値を reject する
- [x] `RegionConfig.to_region()` が immutable な `Region` を返す
- [x] `Region.right` と `Region.bottom` が計算される
- [x] `Region.random_point()` が領域内の点を返す
- [x] `Region` の不正サイズは例外にする
- [x] `Region.random_point()` の不正パラメータは例外にする
- [x] 固定領域を実 viewport サイズへ scale できる
- [x] scale 後に固定領域の size が 0 以下なら例外
- [x] template size と region size が違うと例外
- [x] 1920x1080 screenshot では scale 1 で照合する
- [x] 1280x720 screenshot では template、region、margin を `2 / 3` に scale して照合する
- [x] 2560x1440 screenshot では template、region、margin を `4 / 3` に scale して照合する
- [x] アスペクト比が 16:9 でない screenshot は例外
- [x] fake `np.ndarray` screenshot の指定 region が一致したら `matches()` が true
- [x] `match()` が `score` と実 screenshot 座標系の `Region` を返す
- [x] margin 内でずれたテンプレートも match し、ずれた `Region` を返す
- [x] threshold 未満なら `matches()` が false
- [x] scale 後に template size が 0 以下なら例外
- [x] screenshot が探索領域より小さい場合は例外
- [x] `LoginScreen.detection_spec()` が template predicate を返す
- [x] `LoginScreen.detection_spec()` が PNG screenshot bytes を template matcher に渡せる
- [x] `LoginScreen.enter_email_address()` の固定領域は実 viewport サイズへ scale される
- [x] callback dispatch 前に `LoginScreen` の pre-hook でログインボタンをクリックできる
- [x] `LoginScreen.before_callback()` がログインボタン不一致時に例外を投げる
- [x] `LoginScreen.before_callback()` がログインボタンクリック後に 1.0 秒待機する
- [x] `LoginScreen.before_callback()` が Yostar ロゴ不一致時に例外を投げる
- [x] `LoginScreen.before_callback()` が開始時に 1.5 秒待機してメンテナンスダイアログを検出する
- [x] `LoginScreen.before_callback()` がメンテナンスダイアログを検出したら操作せず `ScreenUnexpectedStateError` にする
- [x] `LoginScreen` の単体テストは画面操作用の待機時間を実際には待たない

候補:

- [x] `LoginScreen.enter_email_address()` が入力欄への browser operation を記録する
- [x] `LoginScreen.enter_email_address()` の実領域をスクリーンショット確認で確定する
- [x] `EMAIL_ADDRESS_PATTERN` が RFC 上は有効でも雀魂フロントエンドでは reject される例を固定する
- [x] `LoginScreen.enter_email_address()` がフロントエンド regex を通る不正メールを `EmailStr` で reject する
- [x] `LoginScreen.enter_email_address()` がメール入力後 0.5 秒待機して送信ボタンをクリックする
- [x] `LoginScreen.enter_email_address()` が成功後 60 秒未満の再入力を不正操作として reject する
- [x] `LoginScreen.enter_verification_code()` がメールアドレス入力未完了なら不正操作エラーにする
- [x] `LoginScreen.enter_verification_code()` が半角数字 6 桁以外を不正引数エラーにする
- [x] `LoginScreen.enter_verification_code()` が認証コード欄へ `clear=True` で入力する
- [x] `LoginScreen.enter_verification_code()` が認証コード入力後 0.5 秒待機してログインボタンをクリックする
- [x] `LoginScreen.enter_verification_code()` が入力シーケンス完了後にメンテナンスダイアログを検出する
- [x] メンテナンスダイアログを `LoginScreen` の stale 化直前に検出する
- [x] メンテナンスダイアログを検出したら screenshot 付き `ScreenUnexpectedStateError` にする

認証コード後のログインフローは、まず
[認証コード後のログインフロー設計](../design/screens/login-verification.md) の spike を行い、
通信判定と画面 template の可否を確認してから実装する。

### 認証コード誤りの通信判定 spike

- [x] `POST https://jp-sdk-api.yostarplat.com/yostar/get-auth` を Playwright で観測できる
- [x] accepted / rejected の両方が HTTP status 200 であることを手動確認する
- [x] JSON `Code` と `Data.Token` の存在で accepted / rejected を区別できることを確認する
- [x] atomic browser command が response 待機を login click より先に開始する
- [x] 対象 URL と POST method が一致する response だけを待つ
- [x] accepted response は token を含まない accepted result を返す
- [x] `Code != 200` は application code だけを含む rejected result を返す
- [x] HTTP status 異常を browser operation error にする
- [ ] JSON decode 失敗と schema 異常を browser operation error にする
- [x] `Code == 200` でも token が空または文字列でなければ browser operation error にする
- [ ] response timeout を認証拒否や成功として扱わない
- [ ] command / response の log にメールアドレス、認証コード、token、raw JSON を出さない
- [ ] command / response の serialization に token、メールアドレス、raw JSON を含めない
- [x] `LoginScreen` が rejected result を screenshot 付き不正引数エラーへ変換する
- [ ] `LoginScreen` が protocol error を不正引数エラーへ変換しない
- [ ] 自動テストは synthetic response だけを使う
- [ ] 実際の雀魂で accepted / rejected の結果をユーザーが手動確認する

### 正しい認証コード後の同意画面

- [ ] 同意画面用 template の必要性と、個人情報を含まない template 候補を確認する
- [ ] template 画像と settings はユーザーがコミットする
- [ ] 認証コード成功後に同意画面 template の出現を timeout 付きで待機する
- [ ] 同意画面が検出できない timeout を成功扱いにしない
- [x] 仮の checkbox region を順番にクリックする
- [x] 720pでは規約確認用の720p実座標Regionを使用する
- [x] 1080pと1440pでは従来の1080p基準Regionをscaleして使用する
- [ ] checkbox が既に選択済みの場合の扱いを手動確認結果に基づき固定する
- [x] 正しい認証コードから checkbox 操作までをユーザーが実際の雀魂で手動確認する

### 同意後の遷移と stale Screen

- [ ] 同意ボタンの操作対象を template match region または確定した `Region` として定義する
- [ ] 遷移先画面の非個人情報 template と settings はユーザーがコミットする
- [ ] 同意ボタン後に遷移先 Screen を timeout 付きで検出する
- [ ] 通信成功だけでは同意後の画面遷移完了として扱わない
- [x] `Screen` が active / stale 状態を保持する
- [x] stale Screen の public API は screenshot 付き `ScreenStaleError` を送出する
- [x] `ScreenStaleError` は `ScreenInvalidOperationError` としても捕捉できる
- [ ] stale 判定で screenshot 取得に失敗した場合、その失敗を隠さない
- [x] 基底クラスの `@requires_active` decorator が Screen の共通 public helper を保護する
- [x] `@requires_active` decorator が `LoginScreen` の public 操作 API を保護する
- [ ] private helper、constructor、`detection_spec()` は stale 判定の対象外である
- [x] 遷移 API の全操作が正常完了した時点でのみ `LoginScreen` を stale にする
- [x] 同意ボタンのクリック後は再検出を避けるため 1.0 秒待機する
- [x] 認証拒否では `LoginScreen` を stale にしない
- [x] 遷移操作失敗では `LoginScreen` を stale にしない
- [x] stale にした `LoginScreen` ではメールアドレス、認証コード、同意操作を再実行できない
- [x] 同意後の遷移と stale 化をユーザーが実際の雀魂で手動確認する

どちらを選ぶ場合も、先に fake browser operation のテストを書きます。
実ゲーム確認が終わるまで、もう片方には進みません。

## Phase 6.1: HomeScreen 画面検出

- [x] `HomeScreen` が `Screen` を継承する
- [x] Home 画面用 template の名前を `summon` とする
- [x] `HomeScreen.detection_spec()` が summon template predicate を返す
- [x] synthetic screenshot 内の summon template で Home 画面を検出できる
- [x] threshold 未満の screenshot では Home 画面を検出しない

画像と settings はユーザーが追加する。エージェントは実ゲーム由来の画像を
生成、複製、コミットしない。

## Phase 6.2: HomeScreen 告知画面を閉じる

- [x] `notification-close` template が存在する場合は一致領域をクリックする
- [x] `notification-close` template が存在しない場合はクリックしない
- [x] 告知画面をクリックして閉じた場合は 1.0 秒待機する
- [x] 告知画面が存在しない場合は待機しない

## Phase 6.3: HomeScreen event 画面を閉じる

- [x] `event-close` template が存在する場合は一致領域をクリックする
- [x] notification の後に event が表示されても両方を閉じる
- [x] event の後に notification が表示されても両方を閉じる
- [x] 各画面をクリックして閉じるたびに 1.0 秒待機する
- [x] 1 枚の screenshot を残りの複数 template と照合する
- [x] 同じ close template が再検出されたら予期しない状態のエラーにする
- [x] 予期しない状態のエラーに再検出時の screenshot を添付する

## Phase 6.4: HomeScreen mail 画面を閉じる

- [x] `mail-close` template が存在する場合は一致領域をクリックする
- [x] notification、event、mail の表示順にかかわらずすべて閉じる
- [x] mail をクリックして閉じた場合も 1.0 秒待機する
- [x] `mail-close` が再検出されたら予期しない状態のエラーにする

## Phase 6.5: HomeScreen rewards 画面を閉じる

- [x] `rewards-sign-in` がなければ rewards 操作を行わない
- [x] `rewards-sign-in` をクリックしたら 2.0 秒待機する
- [x] 続く `rewards-confirm` をクリックして 0.5 秒待機する
- [x] sign-in 後に confirm がなければ画面検出エラーにする
- [x] confirm 不在エラーに確認時の screenshot を添付する
- [x] rewards と通常 close のどちらが先でも両方を処理する

## Phase 6.6: HomeScreen 告知処理後の確認

- [x] 告知処理後に `tournament-match` が表示されていることを確認する
- [x] 告知処理後に `friendly-match` が表示されていることを確認する
- [x] どちらかがなければ画面検出エラーにする
- [x] 両 template を告知検出に使った最後の screenshot と照合する
- [x] Home 画面検出後は最初の screenshot より前に 1.0 秒待機する

## Phase 6.7: HomeScreen 友人戦の部屋作成

- [x] `Mode` が四人戦と三人戦を表す
- [x] `Length` が一局戦、東風戦、半荘戦、CPU 戦を表す
- [x] `ThinkingTime` が選択可能な 5 種類の持ち時間を表す
- [x] `HomeScreen.create_room()` の既定値が四人戦、半荘戦、5+20 秒である
- [x] `HomeScreen.create_room()` が各列挙値を受け付け、`None` を返す
- [x] `HomeScreen.create_room()` が高レベル API としてログ記録と stale 保護を行う
- [x] `HomeScreen.create_room()` が `friendly-match` の一致領域をクリックする
- [x] `friendly-match` が見つからなければ screenshot 付き画面検出エラーにする
- [x] `create-room` template と settings を HomeScreen から利用できる
- [x] `friendly-match` のクリック後 1.0 秒待って `create-room` をクリックする
- [x] `create-room` が見つからなければ screenshot 付き画面検出エラーにする
- [x] room 作成画面の `create` template と settings を HomeScreen から利用できる
- [x] `create-room` のクリック後 1.0 秒待って `create` の存在を必須確認する
- [x] `create` が見つからなければ screenshot 付き画面検出エラーにする
- [x] `Mode` の全列挙値に仮のクリック用 `Region` を対応付ける
- [x] `Length` の全列挙値に仮のクリック用 `Region` を対応付ける
- [x] `ThinkingTime` の全列挙値に仮のクリック用 `Region` を対応付ける
- [x] `mode`、`length`、`thinking_time` の指定領域を順に 0.5 秒間隔でクリックする
- [x] 最後の設定クリックから 0.5 秒後に `create` の一致領域をクリックする
- [x] `create` のクリック成功後だけ `HomeScreen` を stale にする
- [x] 設定または `create` のクリック失敗では `HomeScreen` を stale にしない

## Phase 6.8: HomeScreen 友人戦の部屋参加

- [x] room ID の形式を `re.compile(r"\d{5}")` の完全一致で判定する
- [x] 形式が一致する room ID は暫定 no-op で `None` を返す
- [x] 形式が一致しない room ID は screenshot 付き不正引数エラーにする
- [x] `HomeScreen.join_room()` を高レベル API のログ記録と stale 保護の対象にする
- [x] `join-room` template と settings を HomeScreen から利用できる
- [x] `friendly-match` のクリック後 1.0 秒待って `join-room` をクリックする
- [x] `friendly-match` または `join-room` がなければ screenshot 付き画面検出エラーにする
- [x] room 参加ダイアログの `confirm` template と settings を HomeScreen から利用できる
- [x] `join-room` のクリック後 1.0 秒待って `confirm` の存在を必須確認する
- [x] `confirm` がなければ screenshot 付き画面検出エラーにする
- [x] confirm 確認後に room ID 領域へ `clear=False` で room ID を入力する
- [x] room ID 入力後 0.5 秒待って `confirm` の一致領域をクリックする
- [x] confirm クリック後 0.5 秒待って `.lq.Lobby.joinRoom` を走査する
- [x] `.lq.Lobby.joinRoom` より前の message を読み捨て、後続 message は残す
- [x] `.lq.Lobby.joinRoom` がなければ screenshot 付き message 不整合エラーにする
- [x] `.lq.Lobby.joinRoom` が response を持たなければ message 不整合エラーにする
- [x] response に `error` がなければ成功を info log に出して stale にする
- [x] 成功時の info log に room ID を含めない
- [x] joinRoom response の `error` 抽出と構造確認を private helper に分離する
- [x] `error` が dict でないか `code` がなければ message 不整合エラーにする
- [x] joinRoom の既知 error code を `JoinRoomFailureReason` へ変換する
- [x] 未対応 error code を framework 側の `UNRECOGNIZED_ERROR_CODE` へ変換する
- [x] 未対応 error code の数値を warning log に記録する
- [x] error code が整数でなければ message 不整合エラーにする
- [x] 参加失敗時は成功 log を出さず、`HomeScreen` を stale にしない
- [x] 参加成功時は 1.0 秒待機してから `HomeScreen` を stale にする
- [x] 参加失敗時は失敗理由名を warning log に記録する
- [x] 参加失敗から 0.5 秒待機して `error-confirm` をクリックする
- [x] `error-confirm` から 1.0 秒待機して戻る座標をクリックする
- [x] 戻る座標から 1.0 秒待機してホーム画面の対局ボタンを確認する

## Phase 6.9: HomeScreen 大会ロビー参加

- [x] `EnterTournamentFailureReason` が既知コードと framework fallback を表す
- [x] tournament ID の形式を `re.compile(r"\d{6}")` の完全一致で判定する
- [x] 形式が一致しない tournament ID は screenshot 付き不正引数エラーにする
- [x] `HomeScreen.enter_tournament()` を高レベル API のログ記録と stale 保護の対象にする
- [x] 形式が一致する tournament ID では `tournament-match` をクリックする
- [x] `tournament-match` がなければ screenshot 付き画面検出エラーにする
- [x] `tournament-match` から 1.0 秒待機して `tournament-lobby` をクリックする
- [x] `tournament-lobby` がなければ screenshot 付き画面検出エラーにする
- [x] `tournament-lobby` から 1.0 秒待機して `enter` をクリックする
- [x] `enter` から 1.0 秒待機して `confirm` の存在を必須確認する
- [x] `confirm` がなければ screenshot 付き画面検出エラーにする
- [x] `confirm` 確認後に tournament ID 領域へ `clear=False` で入力する
- [x] tournament ID 入力から 0.5 秒待機して `confirm` をクリックする
- [x] confirm 後に `.lq.Lobby.fetchCustomizedContestByContestId` の交換を 0.5 秒待つ
- [x] 対象 message または response がなければ message 不整合エラーにする
- [x] response の `error.code` を `EnterTournamentFailureReason` へ変換する
- [x] 未対応 error code を warning log に記録して framework fallback へ変換する
- [x] `error` が dict でないか `code` が整数でなければ message 不整合エラーにする
- [x] 大会取得成功時は info log 後に 1.0 秒待機して `HomeScreen` を stale にする
- [x] 大会取得失敗時は失敗理由名を warning log に記録する
- [x] 大会取得失敗から 0.5 秒待機して大会用 `error-confirm` をクリックする
- [x] 大会用 `error-confirm` から 1.0 秒待機して共通 `tournament/leave` template をクリックする
- [x] 大会用の退出ボタンから 1.0 秒待機してホーム画面の対局ボタンを確認する

## Phase 6.10: RoomScreen

詳細な設計判断は [RoomScreen 設計](../design/screens/room.md) に従う。以下は実装前の
テストリストであり、高レベル API は記載順に 1 つずつ実装・手動確認する。

### Room state model

- [x] `RoomPlayer` と `RoomState` は immutable である
- [x] `RoomState.version` は client 内の更新ごとに単調増加する
- [x] `room_id`、owner ID、self account ID、player account ID が正でなければ拒否する
- [x] `max_player_count` は通常 room の 3 / 4 に加えて VS_AI の 1 を許す
- [x] human player の account ID 重複を拒否する
- [x] active room の owner と self が human player list にいなければ拒否する
- [x] ready list に未知 account ID があれば拒否する
- [x] `ai_count` は変化しない `robot_count` ではなく `robots` の要素数から導出する
- [x] human と AI の合計が最大人数を超えたら拒否する
- [x] `RoomPlayer.is_host` を owner ID から導出する
- [x] `RoomPlayer.is_ready` を wire の ready 状態から導出し、host を暗黙に ready にしない
- [x] `self_is_host`、`self_is_ready`、`all_guests_ready`、`participant_count`、`available_slots` を snapshot から導出する
- [x] player list は protocol で観測した順序を保つ
- [x] AI を正の account ID を持つ human player として公開しない
- [x] terminal state でも最後に確定した room 情報を保持する

### Room state store / SnifferMessageSource

- [x] 成功した `.lq.Lobby.createRoom` response から host の初期 snapshot を作る
- [x] 成功した `.lq.Lobby.joinRoom` response から guest の初期 snapshot を作る
- [x] 成功した `.lq.Lobby.fetchRoom` response から対局終了後の Room snapshot を作る
- [x] error を持つ create / join / fetch response では active room を初期化しない
- [x] `.lq.NotifyRoomPlayerUpdate` で owner、human、AI を同じ version へ原子的に更新する
- [x] host 退出後の owner 更新で `self_is_host` を再導出する
- [x] `.lq.NotifyRoomPlayerReady` で対象 player の ready だけを更新する
- [x] player update / ready の同名通知が outbound なら不正な message として拒否する
- [x] `.lq.NotifyRoomGameStart` で `MATCH_STARTED` にする
- [x] `.lq.NotifyRoomKickOut` で `KICKED` にする
- [x] 成功した `.lq.Lobby.leaveRoom` response で `LEFT` にする
- [x] terminal 後の古い room notice を active state として復活させない
- [x] active 中に別 room ID の完全 snapshot が来たら不整合にする
- [x] room 状態用の decode 直後 observer や background task を追加しない
- [x] RoomScreen は `SnifferMessageSource.get_nowait()` で蓄積済み message を順番に処理する
- [x] RoomScreen は `SnifferMessageSource.get()` で新しい message を待機する
- [ ] `RoomStateStore` は `RoomScreen` instance が所有する
- [ ] `ScreenContext` と controller runtime は Room state cache を所有しない
- [ ] store は最新 snapshot 以外の raw message 履歴、operation response、waiter を保持しない
- [ ] active 中に callback が早期 return した後の再検出を、過去の state で初期化成功にしない
- [ ] `.lq.Lobby.fetchRoom` は対局終了後の Room 再入場だけに使い、Room 内の browser reload / restart
      や active 中の callback 早期 return の復元には使わない
- [x] `HomeScreen.create_room()` は成功した createRoom message を RoomScreen 用に source へ残す
- [x] `HomeScreen.join_room()` は成功確認後に元の joinRoom message を 1 回だけ差し戻す
- [x] joinRoom の失敗 message は RoomScreen 用に差し戻さない
- [x] wait は store が渡された snapshot の version より新しければ即時に返せる
- [x] wait は source の `get()` を使い sleep polling しない
- [x] wait 中の cancellation で適用済み snapshot を壊さない
- [x] Sniffer decode、stream gap、queue overflow を room state で成功扱いにしない

### RoomScreen detection / state API

- [x] `room-sign` の template と settings asset が存在する
- [x] `RoomScreen` が `Screen` を継承する
- [x] 個人情報を含まない room template の synthetic screenshot で検出できる
- [x] threshold 未満の screenshot では検出しない
- [x] `before_callback()` は active room snapshot が得られるまで framework 内部の既定期限で待つ
- [x] 画像だけ room で snapshot がなければ状態を推測せず失敗する
- [x] `before_callback()` は source の蓄積済み message を処理して store を最新化する
- [x] `get_state()` は network request や click を行わず最新 immutable snapshot を返す
- [x] RoomScreen の全高レベル API は `timeout` 引数を持たない
- [x] 呼び出し側の `asyncio.timeout()` で待機を伴う RoomScreen API を中断できる
- [x] `wait_for_state_change()` は渡された snapshot より新しい snapshot を返す
- [x] `wait_for_state_change()` は別 room、別 self account、未来 version、同一 version で内容が矛盾する snapshot を拒否する
- [x] `wait_for_state_change()` は kick / game start の terminal snapshot も 1 回返す
- [x] game start の terminal snapshot は `room-sign` が消えるまで返さず、消失後に Screen を stale にする
- [x] game start 後の画面消失待機が cancellation されても terminal snapshot を保持して Screen を stale にする
- [x] 呼び出し側 timeout による cancellation を RoomScreen が握りつぶさない
- [x] room ID、account ID、player 名を高レベル API log に含めない
- [x] RoomState 更新に失敗した message も例外送出前に Sniffer log へ出す

### Failure model

- [x] server rejection は Enum 戻り値ではなく `RoomOperationRejectedError` にする
- [x] rejection error が operation、reason Enum、元の整数 code を保持する
- [x] 未対応 code は数値を warning log に出し `UNRECOGNIZED_ERROR_CODE` にする
- [x] server の error message、room ID、account ID、player 名を例外 message に含めない
- [x] role / 満員 / 未 ready の事前条件失敗では browser operation を行わない
- [x] 事前条件失敗は operation と machine-readable な reason Enum を保持する
- [x] response 欠落と notice 欠落を server rejection に変換しない
- [x] malformed response / notice を空状態や通常失敗へ変換しない
- [x] browser / Sniffer infrastructure error を Room 用 rejection に変換しない
- [x] Room API の cancellation を cleanup 後に伝播する

### `leave()`

- [x] host と guest の `WAITING` state で退出 UI を操作できる
- [x] click 前に source を drain し、その後の outbound `.lq.Lobby.leaveRoom` を対応付ける
- [x] 過去の leaveRoom response を今回の成功に使わない
- [x] 成功 response を観測した後だけ `LEFT` にして RoomScreen を stale にし、return 前に 1.0 秒待機する
- [x] server rejection では active state と Screen を維持する
- [x] `MATCH_STARTED` の guest は退出 UI を操作できない
- [x] kick が leave 待機に割り込んだら呼び出し側 timeout より先に stale error にする
- [x] `leave()` の実ゲーム確認後まで `add_ai()` の実装へ進まない

### `add_ai()`

- [x] VS_AI は満員として扱い、存在しない AI 追加 UI を探索・操作しない
- [x] 最新 snapshot で host の場合だけ AI 追加 UI を操作する
- [x] participant が満員なら UI を操作しない
- [x] source refresh 後の最新 host / capacity を使って事前条件を検証する
- [x] click 前に source を drain し、その後の outbound `.lq.Lobby.addRoomRobot` を対応付ける
- [x] 成功 response と AI が 1 増えた player update の両方を到着順によらず待つ
- [x] AI 数が 1 以外増減した場合は今回の成功として扱わない
- [x] server rejection を自動 retry しない
- [x] response または player update の片方しかなければ成功扱いにせず呼び出し側 timeout まで待つ
- [x] 成功時は更新後の `RoomState` を返し Screen を active のままにする
- [x] `add_ai()` の実ゲーム確認後まで `set_ready()` の実装へ進まない

### `set_ready()`

- [x] 公開 API はキーワード専用の `ready: bool = True` を受け取り、ready と ready 解除を
      同じ状態設定操作として扱う
- [x] `cancel()` / `cancel_ready()` / `ready()` の alias は追加せず、`start_match()` も
      `start()` に短縮しない
- [x] 最新 snapshot で guest の場合だけ ready UI を操作する
- [x] host が呼んだ場合は目標状態によらず UI を操作せず `NOT_GUEST` の不正操作エラーにする
- [x] 自分の `is_ready` が目標状態と一致する guest は click せず同じ snapshot を返す
- [x] click 前に source を drain し、その後の outbound `.lq.Lobby.readyPlay` を対応付ける
- [x] readyPlay request の `ready` が指定した目標状態と一致しなければ不整合にする
- [x] 成功 response と自分の ready notice の両方を待ち、片方だけでは完了しない
- [x] response と notice の順序を実通信で確認するまでは特定の到着順に依存しない
- [x] 別 player の ready notice を自分の成功として扱わない
- [x] 自分の ready notice が目標状態と一致しなければ成功として扱わない
- [x] 成功時は自分の `is_ready` が目標状態の `RoomState` を返し Screen を active のままにする
- [x] `set_ready()` の実ゲーム確認後まで `start_match()` の実装へ進まない

### `start_match()`

- [x] VS_AI は host 1 人の room snapshot から start UI を操作できる
- [x] 最新 snapshot で host の場合だけ start UI を操作する
- [x] human guest が 1 人でも未 ready なら UI を操作しない
- [x] AI を含む participant が最大人数未満なら UI を操作しない
- [x] ready 判定から host を除外する
- [x] source refresh 後の最新 host、ready、満員を使って事前条件を検証する
- [x] click 前に source を drain し、その後の outbound `.lq.Lobby.startRoom` を対応付ける
- [x] 成功 response だけでは完了せず game start notice まで待つ
- [x] game start notice 後だけ `MATCH_STARTED` にして RoomScreen を stale にする
- [x] `start_match()` は `MATCH_STARTED` 後も `room-sign` が消えるまで戻らない
- [x] ローディング画面の可変イラストは検出せず、既存の `room-sign` の消失を遷移条件にする
- [x] guest が外部 host の start を観測した場合も `MATCH_STARTED` にする
- [x] server rejection では RoomScreen を stale にしない

### RoomScreen 完了確認

- [x] `get_state()`、`wait_for_state_change()`、`leave()`、`add_ai()`、`set_ready()`、
      `start_match()` を 1 API ずつ実装し、自動テスト後に実ゲームで確認する
- [x] host と guest の対局開始で、`room-sign` 消失後に callback から戻ることを実ゲームで確認する
- [x] Phase 6.10 の実装に必要な個人情報のない画像と settings をユーザーがコミットする

## RoomScreen follow-up 調査

以下は Phase 6.10 の実装完了を妨げない protocol 調査と edge-case の実ゲーム確認である。
対応する場合は、観測結果に基づいて設計とテストリストを更新する。

- [x] 四人 / 三人 room の snapshot field の意味を確認する
- [x] `persons`、`robots`、`robot_count`、`positions` の関係を確認する
- [ ] ready notice の `account_list` と `seq` の意味を確認する
- [ ] host 退出後の owner update と host 交代を確認する
- [ ] kick notice と画面遷移を確認する
- [x] AI 追加成功の UI / response を確認する
- [ ] AI 追加の満員、guest rejection の UI / response を確認する
- [x] 全 guest ready かつ満員での start 成功を確認する
- [ ] 空席または未 ready での start rejection を確認する
- [ ] host / guest の退出と対局開始後の退出不可を確認する
- [ ] room operation の既知 error code と dialog 復旧可否を確認する
- [ ] Room / room notice の `seq` 増加規則を確認する
- [ ] 実 payload を tests、fixtures、docs、chat、commit へ含めないことを継続的に監査する

## Phase 6.11: MatchScreen 画面検出

- [x] `MatchScreen` は `Screen` の具象 subclass である
- [x] 4 種類の `seat-indicator` template と共通 settings を package asset として参照できる
- [x] 各 `seat-indicator` を含む synthetic screenshot で `MatchScreen` を検出できる
- [x] いずれの `seat-indicator` もない screenshot では `MatchScreen` を検出しない
- [x] 自動テストでは synthetic screenshot だけを使う
- [x] `before_callback()` は検出直後にマウスカーソルを手牌から離す
- [x] マウスカーソルの移動先は基準座標 `(585, 790, 1000, 70)` の領域内とする

## Phase 6.12: MatchScreen 状態初期化

詳細は [MatchScreen 設計](../design/screens/match.md) に従う。

### protobuf action / MatchEvent decode

- [x] Match内のseatと牌は、検証済み値を表す`Seat` / `Tile` NewTypeとして保持する
- [x] `validate_seat()`はintの0〜3だけを`Seat`として返し、boolと範囲外を拒否する
- [x] `validate_tile()`は有効な牌文字列だけを`Tile`として返す
- [x] JSON / protobuf境界で一度変換した`Seat` / `Tile`をEvent、State、Store内で再検証しない
- [x] `Seat` / `Tile`はmajsoulrpa.screens.matchから通常exportする
- [ ] live `ActionPrototype` の obfuscated data を synthetic bytes から decode できる
- [ ] `syncGame.game_restore.actions` の plain data を同じ public `MatchEvent` へ decode できる
- [ ] live / restore adapter は同じ action data に対して同じ event を返す
- [ ] 対応対象の protobuf action 1 件から `MatchEvent` 1 件を生成し、internal action union を作らない
- [ ] event ごとの値域と相互関係を dataclass constructor で検証する
- [x] event ごとの decoded dict 変換は位置引数の `from_dict()` classmethod に置く
- [x] concrete event class は event ごとの実装 module に分ける
- [x] action名からevent classmethodへのdispatchはdecoder registryに集約する
- [ ] event constructor は未知 keyword を拒否し、collection field を tuple に限定する
- [ ] generic な mutable `data` dict を event や state に保持しない
- [ ] live adapter は inbound DecodedNotice、restore adapter は outbound syncGame response だけを受理する
- [ ] nested action type は protocol descriptor と初期化用 allowlist の両方から解決する
- [x] Sniffer の observed_at はログに残し、public MatchEvent には保持しない
- [ ] 未知 action 名、壊れた data、不正 step は明示的な decode error にする
- [x] 既知 action の unknown protobuf field は独自検査せず、既知 field だけを利用する
- [x] live ActionPrototype の info log は難読化 data を protobuf decode 済み辞書へ差し替える
- [ ] nested action decode を共通 Sniffer decoder の責務へ追加しない

### OptionalOperation / MatchOperation decode

- [x] concrete operation は `@final`、`frozen=True`、`slots=True`、`kw_only=True` の dataclass である
- [x] public `MatchOperation` type alias はすべての concrete operation class を列挙し、type discriminator を持たない
- [ ] field のない `SkipOperation` を public `MatchOperation` に含める
- [x] `OperationCandidates` は非負の millisecond 単位の fixed / add time、非空 tuple の operation を保持する
- [x] operation field の欠落と空の `operation_list` はどちらも `None` に正規化する
- [x] operation field が object でない、time / type が bool または int 以外、operation_list が list でない場合は拒否する
- [x] type 1 の `combination` を禁止牌として解釈し、禁止されていない手牌を 1 打牌 1 `DapaiOperation` に展開する
- [x] type 2 は直前の取得牌と `combination` の手牌 2 枚を持つ `ChiOperation` 1 instance へ変換する
- [x] type 2 の各 combination は `|` で区切られた2枚に限定し、wire 順の1候補1 instanceへ展開する
- [x] ChiOperation は直前の DapaiEvent から from_seat / tile を補い、赤牌表現を維持する
- [x] ChiOperation は四麻での自家の上家による直前打牌と、手牌に実在する consumed を必要とする
- [x] type 3 は直前の取得牌と `combination` の手牌 2 枚を持つ `PengOperation` 1 instance へ変換する
- [x] type 3 の各 combination は `|` で区切られた2枚に限定し、wire 順の1候補1 instanceへ展開する
- [x] PengOperation は任意の他家による直前の DapaiEvent から from_seat / tile を補い、赤牌表現を維持する
- [x] PengOperation は取得牌と consumed が同じ牌種で、consumed が手牌に実在することを必要とする
- [x] type 4 は `combination` 1 要素ごとに消費牌 4 枚を持つ `AngangOperation` 1 instance へ変換する
- [x] type 4 の各 combination は `|` で区切られた4枚に限定し、牌indexでsortせずwire順の1候補1 instanceへ展開する
- [x] AngangOperation は ActionNewRound の親配牌または自家の ActionDealTile にだけ生成する
- [x] AngangOperation の consumed は shoupai と zimopai を合わせた現在の牌に実在することを必要とする
- [x] 親の14枚配牌で presentation zimopai が暗槓牌に含まれる場合も同じ候補へ展開する
- [x] type 5 は直前の取得牌と `combination` の手牌 3 枚を持つ `DaminggangOperation` 1 instance へ変換する
- [x] type 5 の各 combination は `|` で区切られた3枚に限定し、wire 順の1候補1 instanceへ展開する
- [x] DaminggangOperation は任意の他家による直前の DapaiEvent から from_seat / tile を補い、赤牌表現を維持する
- [x] DaminggangOperation は取得牌と consumed が同じ牌種で、consumed が手牌に実在することを必要とする
- [x] `ActionAnGangAddGang(type=3)` を live / restore の両経路で同じ `AngangEvent` へ変換する
- [x] `AngangEvent` は seat、固定長4枚の consumed、非空時に置換するドラ表示牌を保持する
- [x] 暗槓する牌が 0m / 5m、0p / 5p、0s / 5s のどちらで届いても赤五1枚を先頭、黒五3枚へ正規化する
- [x] 五以外の暗槓は wire の単独牌を同じ4枚の consumed へ展開する
- [x] `ActionAnGangAddGang` の type 2 と未知 type は暗槓として受理しない
- [x] type 6 は牌順に依存せず既存の `Peng` と4枚の multiset を比較し、元の from_seat / tile / consumed と差分の added を保持する `JiagangOperation` 1 instance へ変換する
- [x] type 7 の各候補牌を 1 打牌 1 `LiqiOperation` に展開する
- [x] type 8 は空の `combination` と発生元 Event のツモ牌から `ZimohuOperation` を生成する
- [ ] type 9 は空の `combination` と発生元 Event の対象 seat・対象牌から `RongOperation` を生成する
- [x] type 10 は空の `combination` から field のない `LiujuOperation` を生成する
- [x] `LiujuOperation` は親の配牌直後または自家ツモ直後に么九牌が9種類以上ある場合だけ生成する
- [x] `LiujuOperation` は `Fulu` のない手牌だけで生成する
- [x] `LiujuOperation` は現時点では九種九牌だけを表す
- [x] type 11 は空の `combination` から field なしの `BabeiOperation` を生成する
- [x] `BabeiOperation` は三人戦の親配牌または自家ツモに北が含まれる場合だけ生成する
- [x] `BabeiOperation` は手牌・ツモ牌のどちらを抜くかを表す `moqie` を持たない
- [x] type 2〜6 の区切り後の牌数が operation ごとの枚数と異なる場合は拒否する
- [x] AngangOperation は4枚を consumed として保持する
- [x] JiagangOperation は既存の `Peng` との差分が通常牌か赤牌かを added に保持する
- [x] JiagangOperation は既存の Peng から from_seat、取得した tile、手牌から使った2枚の consumed を引き継ぐ
- [x] type 6 の赤5が先頭に正規化されていても、既存の `Peng` に含まれる赤5と added の赤5を正しく区別する
- [x] type 6 の4枚に対応する自家の Peng が一意に見つからない、または multiset の差分が1枚でない場合は拒否する
- [x] `ActionAnGangAddGang` の type 2 は単独の `tiles` を加槓の追加牌として Event へ反映する
- [x] `JiagangEvent` は追加牌の赤牌・通常牌を正規化せず区別し、非空のドラ表示牌を保持する
- [x] `JiagangEvent.consumed` は added が赤五なら黒五3枚、黒五なら赤五1枚と黒五2枚、それ以外なら同種3枚に正規化する
- [x] 加槓は既存の `Peng` を元の取得情報と追加牌を持つ `Jiagang` に置換する
- [x] 自家の加槓は `added` と一致する手牌またはツモ牌を消費し、他のツモ牌は手牌へ取り込む
- [x] 加槓は嶺上ツモと搶槓対象を設定し、河には牌を追加しない
- [x] 対応する既存の `Peng` が一意に存在しない加槓は拒否する
- [x] `ActionBaBei` を live / restore の両経路で同じ `BabeiEvent` へ変換する
- [x] `BabeiEvent` は seat、手牌からかツモ牌からかを表す moqie、非空時に置換するドラ表示牌を保持する
- [x] 北抜きは三人戦だけで受理し、seat ごとの `RoundState.babei` に `Babei(moqie=...)` を追加する
- [x] 自家の北抜きは moqie=true ならツモ牌、false なら手牌の `4z` を消費し、手牌から抜いた場合は別のツモ牌を手牌へ取り込む
- [x] 他家の北抜きは自家の手牌を変更しない
- [x] 北抜きは河と副露を変更せず、全員の first_draw / yifa を終了し、対象seatの嶺上ツモと `4z` の搶槓対象を設定する
- [x] 北抜き直後は同じ seat の `ActionDealTile` を嶺上ツモとして受理する
- [x] `ActionLiuJu` の type 1〜4 を `LiujuEvent` と `LiujuType` へ変換する
- [x] `LiujuEvent.seat` は九種九牌だけ必須とし、他の流局種別では `None` にする
- [x] `ActionLiuJu` の未知 type と、九種九牌以外で0ではない seat を拒否する
- [x] `ActionLiuJu.liqi` を `LiujuEvent.liqi_success` に保持する
- [x] `ActionLiuJu` を live / restore の両経路で同じ `LiujuEvent` へ変換する
- [x] `LiujuEvent` を Event 列へ追加し、局終了前の operation 候補を消去する
- [x] `ActionHule` を自摸和・栄和共通の `HuleEvent` に変換し、複数の和了情報を message の順序どおり保持する
- [x] `Hule` は和了者、和了方法、和了牌、公開された手牌・副露、役ID、符、点数内訳を保持し、常に空の役名・titleは保持しない
- [x] `HuleEvent` は局の和了前点数、点数差分、和了後点数、試合終了時点数を保持し、空の action 直下ドラ表示牌は保持しない
- [x] `ActionHule` を live / restore の両経路で同じ `HuleEvent` へ変換する
- [x] 自摸和は和了者の直前の `ZimoEvent`、または親の配牌を表す `NewRoundEvent` に続く場合だけ受理する
- [x] 自家の自摸和では `Hule.hu_tile` が表示中のツモ牌と一致することを検証する
- [x] 自摸和の `Hule.qinjia` が局の親と一致することを検証する
- [x] `HuleEvent` を Event 列へ追加し、和了後点数を反映して局終了前の operation 候補を消去する
- [x] ロンは未解決の直前打牌と和了牌が一致し、和了者が放銃者と異なる場合だけ受理する
- [x] 搶槓ロンは未解決の搶槓対象と和了牌が一致し、和了者が槓・北抜きした seat と異なる場合だけ受理する
- [x] ダブロン・トリロンは message の和了者順を保って受理し、全和了者の seat / qinjia / hu_tile を検証する
- [x] 自摸和とロンが混在する `HuleEvent`、重複する和了者、和了対象のないロンを拒否する
- [x] ロン適用後は点数を更新し、operation 候補と未解決の打牌・搶槓対象を消去する
- [x] `DapaiOperation` / `LiqiOperation` は tile と moqie を保持し、手出しとツモ切りを別 instance にする
- [x] 同じ tile / moqie の物理牌が複数あっても同じ打牌 operation は重複させない
- [x] 手牌と実ツモ牌の両方に同じ候補牌があれば、moqie=false / true の両 operation を生成する
- [x] type 1 で 5m / 5p / 5s が禁止されている場合、combination にない対応する 0m / 0p / 0s も禁止する
- [x] type 1 で通常五が禁止されていない場合、対応する赤五を独自に禁止しない
- [x] type 7 で 0m / 0p / 0s が立直候補で、対応する 5m / 5p / 5s も手牌またはツモ牌に実在する場合だけ通常5も候補にする
- [x] type 7 で赤5だけが実在する場合、存在しない通常5の候補を追加しない
- [x] type 7 で通常五だけが立直候補の場合、対応する赤五を独自に候補へ追加しない
- [x] 親の ActionNewRound の14枚はすべて moqie=false の DapaiOperation に展開する
- [x] 親の ActionNewRound の presentation zimopai にある立直候補も moqie=false の LiqiOperation にする
- [x] 親の初期打牌でツモ牌位置を click する必要があっても operation を moqie=true に変換しない
- [ ] type 8〜11 の `combination` が空でない場合は拒否する
- [x] operation 内の不正な牌表現を拒否する
- [x] 未知 type を無視したり generic operation として保持したりせず decode error にする
- [x] 未実装の既知 type が混在する場合も、対応済み候補だけを部分的に公開せず decode error にする
- [x] protobuf の `seat`、`change_tiles`、`change_tile_states`、`gap_type` と unknown field の存在だけでは拒否しない
- [ ] operation の並びと各 combination の並びを protobuf の順序どおり tuple に保持する
- [ ] 副露・槓 operation は候補一覧を内部に持たず、各 instance が operate API に渡せる単一の牌組を表す
- [x] Chi / Peng / Daminggang operation は from_seat、tile、consumed だけで選択内容を完全に表す
- [x] from_seat / tile は候補が付随した DapaiEvent.seat / tile と一致し、赤牌を通常牌へ正規化しない
- [x] 直前の打牌がない状態で type 2 / 3 / 5 を public operation へ展開しない
- [x] ZimohuOperation.tile は ActionDealTile のツモ牌と一致し、赤牌を通常牌へ正規化しない
- [x] ActionNewRound の天和候補は presentation zimopai を ZimohuOperation.tile に保持する
- [x] 天和の ZimohuOperation.tile を決めても、同じ牌の打牌 operation は moqie=false のままにする
- [ ] RongOperation.from_seat / tile は放銃者と放銃牌、または槓を行った player と搶槓対象牌に一致し、赤牌を通常牌へ正規化しない
- [x] 和了対象牌を特定できない Event に type 8 が付随した場合は public operation へ展開しない
- [ ] 和了対象牌を特定できない Event に type 9 が付随した場合は public operation へ展開しない
- [x] live / restore action adapter は同じ decoded operation から等しい immutable な内部 specification を返す
- [x] store は Event 適用後の手牌と内部 specification から `OperationCandidates | None` を生成する
- [x] action decoder は `MatchEvent` と operation specification を別に返し、operation event を生成しない
- [x] event 適用時に以前の operation 候補を必ず置き換え、候補がない action では `None` に戻す
- [x] operation 候補の有無は `operation_candidates is None` / `is not None` で直接判定できる
- [ ] operation の concrete class を class pattern で網羅すると ty が成功し、variant 追加時は `assert_never()` が失敗する

### MatchScreen 打牌操作 API

- [x] `operate()` は蓄積済み message を先に reduce し、最新の operation 候補を検証する
- [x] operation 候補がない場合は screenshot 付き `ScreenInvalidOperationError` にする
- [x] 現在の候補に等しくない operation は screenshot 付き `ScreenInvalidArgumentError` にする
- [x] 現在の候補と等しい自作の `DapaiOperation` instance を受け入れる
- [x] `moqie=false` は sorted shoupai にある同種牌の先頭をクリックする
- [x] `moqie=true` は分離表示された zimopai をクリックする
- [x] 手牌と zimopai が同種でも moqie に応じた異なる位置をクリックする
- [x] 親の初打で presentation zimopai を選んだ場合、moqie=false のまま分離表示位置をクリックする
- [x] 親の初打では配牌演出が終わるまで待ってからクリックする
- [x] 通常打牌は候補messageの観測から0.4秒経過するまで、残り時間だけ待ってからクリックする
- [x] 通常打牌の候補message観測から0.4秒以上経過後に `operate()` を呼んだ場合は追加で待たない
- [x] 打牌UIの準備時刻はScreen内部で管理し、public MatchEventには観測時刻を追加しない
- [x] 対象牌への cursor 移動と hover 待機は browser click に任せ、Screen 側で重複させず、クリック後に `MOUSE_SAFE_REGION` へ退避する
- [x] `operate()` は対応する自家の DapaiEvent まで message を log・reduce して更新後の MatchState を返す
- [x] 自家の DapaiEvent の tile / moqie が指定と異なる場合は `ScreenInconsistentMessageError` にする
- [x] 対応する自家の DapaiEvent より先に別の state event が来た場合は `ScreenInconsistentMessageError` にする
- [x] stale な MatchScreen では browser を操作せず `ScreenStaleError` にする
- [x] `operate()` の公開 API log は screen 名と API 名だけを出す
- [x] Dapai は入力の進行を示すmessageを受信するまで同じ牌領域のclickを繰り返す
- [x] Dapai の再試行間隔中にcommon messageを受信しても、前回clickから0.5秒未満で再clickしない
- [x] Liqi は入力の進行を示すmessageを受信するまで同じ牌領域のclickを繰り返す
- [x] Dapai の再試行中に既知common messageをlog・処理してclickを継続する
- [x] Liqi の再試行中に既知common messageをlog・処理してclickを継続する
- [x] Dapai の再試行で先読みした inputOperation / ActionPrototype を1回だけput_backする
- [x] Liqi の再試行で先読みした inputOperation / ActionPrototype を1回だけput_backする
- [x] Dapai の再試行でinputChiPengGangを終了条件にした場合も、messageを1回だけput_backする
- [ ] Dapai / Liqi の再試行中に未知messageを捨てたり成功扱いしたりしない

### MatchScreen 立直操作 API

- [x] `button-area.toml` の search region 内から `liqi.png` を検出し、検出したボタン領域をクリックする
- [x] 立直ボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] 立直ボタンをクリックしてから候補表示を0.4秒待ち、`LiqiOperation` の tile / moqie に対応する牌領域をクリックする
- [x] 牌クリックは Dapai と同じ入力進行messageの待機・再試行処理を使う
- [x] 立直ボタン後の候補表示待ち中に `ActionPrototype` を先読みした場合は、牌領域をクリックせず1回だけput_backする
- [x] `operate()` は指定した自家の通常立直またはダブル立直の `DapaiEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 自家の `DapaiEvent` の tile / moqie が指定と異なる場合や、立直宣言を伴わない場合は不整合にする
- [x] 上位actionを確認できない立直ボタン検出失敗を成功扱いしない

### MatchScreen チー操作 API

- [x] `button-area.toml` の search region 内から `chi.png` を検出し、検出したボタン領域をクリックする
- [x] チーボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] ChiOperation が1候補なら組合せ選択領域を追加クリックしない
- [x] ChiOperation が2〜5候補なら候補tuple内の位置に対応する組合せ選択領域をクリックする
- [x] チーボタンと組合せを選択した後、手牌のスライド完了を1.5秒待ってからAPIを返す
- [x] `operate()` は指定した自家の `ChiEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 自家の `ChiEvent` が指定した from_seat / tile / consumed と異なる場合は不整合にする
- [x] チーボタン待機中に上位の `ActionChiPengGang` を先読みした場合は1回だけput_backする
- [x] 別playerの `PengEvent` にpreemptされた場合はoperation失敗にせず、更新後のMatchStateを返す
- [x] 他家だけの `HuleEvent` が先に成立した場合はチー操作をpreemptする
- [x] 複数候補の表示待ち中に上位actionを受信した場合は、組合せ領域をクリックせず通常pipelineへ戻す
- [x] 上位actionを確認できないチーボタン検出失敗を成功扱いしない

### MatchScreen ポン操作 API

- [x] `button-area.toml` の search region 内から `peng.png` を検出し、検出したボタン領域をクリックする
- [x] ポンボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] PengOperation が1候補なら組合せ選択領域を追加クリックしない
- [x] PengOperation が2候補なら候補tuple内の位置に対応する組合せ選択領域をクリックする
- [x] ポンボタンと組合せを選択した後、手牌のスライド完了を1.5秒待ってからAPIを返す
- [x] `operate()` は指定した自家の `PengEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 自家の `PengEvent` が指定した from_seat / tile / consumed と異なる場合は不整合にする
- [ ] ポンボタン待機中に上位の `ActionHule` を先読みした場合は1回だけput_backする
- [x] 他家だけの `HuleEvent` が先に成立した場合はポン操作をpreemptする
- [ ] 複数候補の表示待ち中に上位actionを受信した場合は、組合せ領域をクリックせず通常pipelineへ戻す
- [x] 上位actionを確認できないポンボタン検出失敗を成功扱いしない

### MatchScreen 大明槓操作 API

- [x] `button-area.toml` の search region 内から `gang.png` を検出し、検出したボタン領域をクリックする
- [x] 槓ボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] DaminggangOperation は1候補だけを許容し、組合せ選択領域を追加クリックしない
- [x] 槓ボタンをクリックした後、手牌のスライド完了を1.5秒待ってからAPIを返す
- [x] `operate()` は指定した自家の `DaminggangEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 自家の `DaminggangEvent` が指定した from_seat / tile / consumed と異なる場合は不整合にする
- [x] 槓ボタン待機中に `ActionPrototype` を先読みした場合は1回だけput_backし、ボタンをクリックしない
- [x] 上位actionを確認できない槓ボタン検出失敗を成功扱いしない
- [x] 他家のロンが先に成立した場合は大明槓操作をpreemptする
- [x] 自家を含む `HuleEvent` はチー・ポン・大明槓操作のpreemptとして扱わない

### MatchScreen 暗槓操作 API

- [x] `button-area.toml` の search region 内から `gang.png` を検出し、検出したボタン領域をクリックする
- [x] 槓ボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] AngangOperation が1候補なら組合せ選択領域を追加クリックしない
- [x] AngangOperation が2候補なら wire 順の位置に対応する4牌の組合せ選択領域をクリックする
- [x] AngangOperation が3候補なら候補UI表示後の screenshot 付き `ScreenNotImplementedOperationError` で停止する
- [x] 槓ボタンまたは組合せをクリックした後、手牌のスライド完了を1.5秒待ってからAPIを返す
- [x] `operate()` は指定した自家の `AngangEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 赤なし対局の黒5四枚は、赤あり表現へ正規化された `AngangEvent` と牌種で照合する
- [x] 自家の `AngangEvent` が指定した consumed と異なる場合は不整合にする
- [x] 槓ボタンまたは複数候補の表示待ち中に `ActionPrototype` を先読みした場合は1回だけput_backし、次の領域をクリックしない
- [x] 上位actionを確認できない槓ボタン検出失敗を成功扱いしない

### MatchScreen 加槓操作 API

- [x] `button-area.toml` の search region 内から `gang.png` を検出し、検出したボタン領域をクリックする
- [x] 槓ボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] JiagangOperation が1候補なら組合せ選択領域を追加クリックしない
- [x] JiagangOperation が2候補なら wire 順の位置に対応する4牌の組合せ選択領域をクリックする
- [x] JiagangOperation が3候補なら候補UI表示後の screenshot 付き `ScreenNotImplementedOperationError` で停止する
- [x] 槓ボタンまたは組合せをクリックした後、手牌のスライド完了を1.5秒待ってからAPIを返す
- [x] `operate()` は指定した自家の `JiagangEvent` までmessageをreduceし、更新後のMatchStateを返す
- [x] 自家の `JiagangEvent` が指定した added と異なる場合は不整合にする
- [x] 槓ボタンまたは複数候補の表示待ち中に `ActionPrototype` を先読みした場合は1回だけput_backし、次の領域をクリックしない
- [x] 上位actionを確認できない槓ボタン検出失敗を成功扱いしない

### MatchScreen 北抜き操作 API

- [x] `button-area.toml` の search region 内から `babei.png` を検出し、検出したボタン領域をクリックする
- [x] 北抜きボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] 北抜きボタンをクリックした後、手牌のスライド完了を1.5秒待ってから API を返す
- [x] `operate()` は自家の `BabeiEvent` まで message を reduce し、更新後の `MatchState` を返す
- [x] `BabeiEvent.moqie` は雀魂の自動選択に任せ、`BabeiOperation` との照合条件にしない
- [x] 北抜きボタン待機中に `ActionPrototype` を先読みした場合は1回だけ put_back し、ボタンをクリックしない
- [x] 上位 action を確認できない北抜きボタン検出失敗を成功扱いしない

### MatchScreen 流局操作 API

- [x] `button-area.toml` の search region 内から `liuju.png` を検出し、検出したボタン領域をクリックする
- [x] 流局ボタンがまだ描画されていない場合は、呼び出し側 timeout まで検出を再試行する
- [x] 流局ボタンのクリック後に手牌スライド待機を追加しない
- [x] `operate()` は自家の九種九牌 `LiujuEvent` まで message を reduce し、更新後の `MatchState` を返す
- [x] 九種九牌以外の `LiujuEvent` を `LiujuOperation` の完了として扱わない
- [x] 流局ボタン待機中に `ActionPrototype` を先読みした場合は1回だけ put_back し、ボタンをクリックしない
- [x] 上位 action を確認できない流局ボタン検出失敗を成功扱いしない

### MatchScreen 自摸和操作 API

- [x] 自動和了トグルの領域を `warp=True` でクリックしてオンにする
- [x] 自動和了トグルのクリック後に UI 待機を追加しない
- [x] `operate()` は指定した自家の自摸和 `HuleEvent` まで message を reduce し、更新後の `MatchState` を返す
- [x] 和了後に自動和了トグルをオフへ戻さない

### MatchScreen operation のスキップ

- [ ] チー、ポン、大明槓は「鳴きなし」toggleをonにして明示的にスキップする
- [ ] 「鳴きなし」によるスキップの進行後はtoggleをoffへ戻し、将来の鳴きを再び許可する
- [ ] 「鳴きなし」をonにした後に上位actionでpreemptされても、toggleをoffへ戻してからAPIを返す
- [ ] 「鳴きなし」をoffへ戻せない場合は、preempt自体を許容しても正常完了扱いにしない
- [ ] ロンはスキップbuttonで明示的にスキップする
- [ ] 非立直時の北抜き・暗槓・加槓・ツモ和了には `SkipOperation` を追加しない
- [ ] 非立直時の北抜き・暗槓・加槓・ツモ和了は `DapaiOperation` の打牌で暗黙にキャンセルする
- [ ] 非立直時の北抜き・暗槓・加槓・ツモ和了を見送るためにスキップbuttonを押さない
- [ ] 立直中の北抜き・暗槓・加槓・ツモ和了がある場合はツモ切りの `DapaiOperation` を候補に含めない
- [ ] 立直中の北抜き・暗槓・加槓・ツモ和了がある場合は `SkipOperation` を候補に追加する
- [ ] 立直中の `SkipOperation` はスキップbuttonをクリックして実行する
- [ ] スキップ用の「鳴きなし」toggleとスキップbuttonは `warp=True` でclickする
- [ ] チーの選択・スキップ中に別playerのポン・大明槓・ロンが成立してもoperation失敗にしない
- [ ] ポン・大明槓の選択・スキップ中に別playerのロンが成立してもoperation失敗にしない
- [ ] 上位actionの ActionChiPengGang / ActionHule を先読みした場合は1回だけput_backして通常pipelineで処理する
- [ ] 上位actionを確認できないbutton検出失敗を黙ってスキップ成功にしない
- [ ] ロンのスキップはダブロン・トリロンでも自家の選択まで待たれ、別playerのActionHuleによるpreempt成功扱いをしない
- [ ] publicなスキップ表現は field のない `SkipOperation` とし、他の候補と同じ `operate()` APIへ渡す

### immutable state / reducer

- [x] MatchRank、MatchPlayer、Dapai、各 concrete Fulu、RoundState、MatchState は frozen で collection を tuple にする
- [x] `Fulu` は `Chi | Peng | Daminggang | Angang | Jiagang` を列挙した型エイリアスとし、kind discriminator を持たない
- [x] Chi / Peng / Daminggang は from_seat、取得した tile、手牌から使った固定長 consumed を保持する
- [x] Angang は手牌から使った4枚の consumed を保持し、from_seat を持たない
- [x] Jiagang は元の Peng の from_seat / tile / consumed と追加した added を区別して保持する
- [x] 北抜きは `Fulu` に含めず、seat ごとの `tuple[Babei, ...]` として `RoundState.babei` に保持する
- [x] `Babei` は `ActionBaBei.moqie` に対応する `moqie` を保持する
- [x] human player の四麻 `level4` と三麻 `level3` の AccountLevel ID / score を失わず decode する
- [x] 通常友人戦の authGame response は players が human のみ、robots が CPU のみであることを実通信で確認する
- [x] 観測した robots の account_id は 1 / 2 / 3、nickname は空文字列、level / level3 は field 自体がない
- [x] CPU seat は正の robot ID と空の name を保持し、画面表示に合わせ level4=10101 / level3=20101、score=0 を補う
- [x] 通常友人戦の seat_list は human / CPU の全 ID を seat 順に持ち、CPU ID が robots の ID と対応する
- [x] VS_AI の authGame は空の robots と ready_id_list にある CPU seat ID から player metadata を構築する
- [x] synthetic `authGame` から match identity、origin、self seat、player metadata を decode できる
- [ ] authGame request account ID と session account ID が一致し、token を state / error / 通常 log に残さない
- [x] 友人戦は meta.room_id に友人戦 ID が入り、mode_id / contest_uid は 0 であることを実通信で確認する
- [ ] tournament metadata を実通信で確認して MatchOrigin.TOURNAMENT へ decode する
- [x] room_id / contest_uid が両方 0 の match は open match の可能性を推測で確定せず対象外として拒否する
- [ ] self account が seat list にない、重複 ID、3/4 人以外は不整合にする
- [x] seat_list の participant ID を players / robots と一対一に対応させ、human / CPU とも公開 account_id に保持する
- [ ] 未対応特殊 mode は ScreenUnexpectedStateError として初期化を成功させない
- [x] `ActionNewRound` から最初の immutable `MatchState` / `RoundState` を構築できる
- [x] `ActionNewRound` を immutable `NewRoundEvent` として live / restore の両方から decode する
- [x] 14 枚の ActionNewRound.tiles は全体を sort し、右端を zimopai、残り 13 枚を shoupai にする
- [x] 13 枚の ActionNewRound.tiles は全体を shoupai にし、zimopai を None にする
- [ ] scores、seat ごとの collection、tile、chang / ju / ben、dora、left count の不変条件を検証する
- [x] `RoundState` は `OperationCandidates | None` を保持し、同じ状態を表す bool field / property を持たない
- [x] operation候補のmaterializerへ候補生成時点の自家fuluを渡す
- [x] 自家fuluが4組なら、既存ポンを置換する加槓以外の新たな副露候補を拒否する
- [x] 立直候補は自家fuluが暗槓だけで構成されている場合に限って許容する
- [x] 初回は `ActionMJStart` step 0 の有無に応じて `ActionNewRound` step 1 / step 0 を受理する
- [ ] `ActionMJStart` を state を変更しない `StartMatchEvent` として decode する
- [x] `StartMatchEvent.from_dict()` は `ActionMJStart` のstep 0制約を検証する
- [x] 最初の RoundState ができるまで StartMatchEvent を temporary prelude に保持する
- [x] 自家の暗槓は赤五と黒五を同じ牌種として shoupai / zimopai から合計4枚を消費する
- [x] 暗槓を手牌内の4枚で行った場合は、別の zimopai を shoupai へ取り込んで sort する
- [x] 赤なし対局の黒五4枚も、赤あり表現へ正規化した AngangEvent から reducer を継続できる
- [x] 他家の暗槓は自家の shoupai / zimopai を変更せず、対象 seat の fulu に Angang を追加する
- [x] 暗槓は河と previous_dapai を変更せず、全員の first_draw / yifa を終了し、対象 seat の lingshang_zimo を有効にする
- [x] 暗槓は previous_qianggang に `(seat, tile)` を設定し、後続の嶺上 ZimoEvent が消去する
- [x] previous_dapai / previous_qianggang は seat と tile を単一 tuple にまとめ、存在条件の不整合を表現できない
- [x] 暗槓の不連続 step、不正 seat、未解決打牌、自家の消費牌不足を不整合として拒否する
- [x] 未実装の画面操作用に screenshot 付き `ScreenNotImplementedOperationError` を公開する
- [x] 暗槓の3候補 UI は座標を推測せず、調査協力を求める専用例外で停止する
- [x] 加槓の3候補 UI は座標を推測せず、調査協力を求める専用例外で停止する
- [ ] match version は同じ Screen instance 内で単調増加し、round step は局ごとに 0 から始まる
- [ ] 次局の `ActionNewRound` は同じ store の round generation を増やす
- [ ] 次局へ移っても match identity、self seat、player metadata を維持する
- [ ] DealTile、DiscardTile、ChiPengGang、AnGangAddGang、BaBei を immutable state へ reduce できる
- [x] ActionDiscardTile を immutable DapaiEvent へ decode し、event 列と河へ追加する
- [x] 親の第一打牌は moqie=false でも便宜上分離した zimopai と一致すれば正しく除去する
- [x] DapaiEvent で first_draw、previous dapai、dora、version / step を更新する
- [x] ActionDealTile を immutable ZimoEvent へ live / restore の両方から decode する
- [x] ZimoEvent は自家の実牌を Tile、他家の空文字列を None として保持する
- [x] ZimoEvent は残り枚数、新ドラ表示牌、nested LiQiSuccess を保持する
- [x] ZimoEvent reducer は自家の zimopai、残り枚数、ドラ、立直成立時の点数と liqibang を更新する
- [x] ZimoEvent reducer は他家の非公開ツモ牌を None のまま扱い、直前打牌を解決済みにする
- [x] ZimoEvent reducer は action step、seat、自他と tile 公開範囲、既存 zimopai の不整合を拒否する
- [x] `ActionChiPengGang(type=0)` を immutable `ChiEvent` へ live / restore の両方から decode する
- [x] `ChiEvent` は鳴いた seat、取得元の from_seat、河から取得する tile、手牌から使う2枚の consumed、nested `LiQiSuccess` を保持する
- [x] `ActionChiPengGang` の未対応 type は別の event として誤って受理しない
- [x] `ChiEvent` reducer は自家の consumed tiles を手牌から除き、チー面子を fulu へ追加する
- [x] `ChiEvent` reducer は他家のチーでは自家手牌を変更せず、直前打牌を解決済みにする
- [x] `ChiEvent` reducer は step、seat、from_seat、直前打牌、取得牌、チー可能な上家の不整合を拒否する
- [x] `ChiEvent` reducer は全員の first_draw / yifa、立直成立時の点数と liqibang、version / step を更新する
- [x] `ActionChiPengGang(type=1)` を immutable `PengEvent` へ live / restore の両方から decode する
- [x] `PengEvent` は鳴いた seat、取得元の from_seat、河から取得する tile、手牌から使う2枚の consumed、nested `LiQiSuccess` を保持する
- [x] `PengEvent` は赤牌と黒5を同種として扱い、取得牌と consumed が同じ牌種であることを保証する
- [x] `PengEvent` reducer は自家の consumed tiles を手牌から除き、ポン面子を fulu へ追加する
- [x] `PengEvent` reducer は他家のポンでは自家手牌を変更せず、任意の他家からの直前打牌を解決済みにする
- [x] `PengEvent` reducer は step、seat、from_seat、直前打牌、取得牌、自家手牌の不整合を拒否する
- [x] `PengEvent` reducer は全員の first_draw / yifa、立直成立時の点数と liqibang、version / step を更新する
- [x] `ActionChiPengGang(type=2)` を immutable `DaminggangEvent` へ live / restore の両方から decode する
- [x] `DaminggangEvent` は鳴いた seat、取得元の from_seat、河から取得する tile、手牌から使う3枚の consumed、nested `LiQiSuccess` を保持する
- [x] `DaminggangEvent` は赤牌と黒5を同種として扱い、取得牌と consumed が同じ牌種であることを保証する
- [x] `DaminggangEvent` reducer は自家の consumed tiles を手牌から除き、大明槓面子を fulu へ追加する
- [x] `DaminggangEvent` reducer は他家の大明槓では自家手牌を変更せず、任意の他家からの直前打牌を解決済みにする
- [x] `DaminggangEvent` reducer は step、seat、from_seat、直前打牌、取得牌、自家手牌の不整合を拒否する
- [x] `DaminggangEvent` reducer は全員の first_draw / yifa、大明槓したseatの lingshang_zimo、立直成立時の点数と liqibang、version / step を更新する
- [x] 大明槓で直前打牌を解決した後も、lingshang_zimo が真のseatに続く `ZimoEvent` を受理する
- [x] 他家の `DaminggangEvent` が先に成立した場合はチー操作をpreemptする
- [ ] concrete MatchEvent は `@final`、`frozen=True`、`slots=True`、`kw_only=True` の dataclass である
- [ ] public `MatchEvent` type alias はすべての concrete event class を列挙する
- [ ] MatchEvent に type discriminator を設けない
- [ ] event の canonical class / field は zimo、dapai、chi、peng、gang、liqi の語彙を使う
- [ ] 利用者は event の具体 class を pattern matching して型を絞り込める
- [ ] 各 case を terminal にして match 後に `assert_never(event)` を置くと全 variant で ty が成功する
- [ ] MatchEvent union に未処理 variant があると `assert_never(event)` を ty が失敗にする
- [x] ActionMJStart がある最初の RoundState.events は StartMatchEvent、NewRoundEvent の順で始まる
- [x] ActionMJStart がない局の RoundState.events は NewRoundEvent から始まる
- [x] RoundState.events の tuple 順と action_step が protobuf action の順序に一致する
- [x] liqi / wliqi 宣言は DapaiEvent の field に含め、独立 event を生成しない
- [ ] 後続 action の LiQiSuccess は対応する event の nested field に含め、独立 event を生成しない
- [ ] 次局の ActionNewRound で event 列を新しい NewRoundEvent から開始する
- [ ] restore replay は temporary store で行い、成功後に version 1 の snapshot を一度だけ publish する
- [ ] restore replay も live と同じ reducer で RoundState.events を再構築する
- [ ] active resync の replay が途中で失敗した場合、以前の state と operation を変更しない
- [ ] action step の欠落、巻き戻り、内容が異なる duplicate を成功扱いにしない
- [ ] 観測順が前後した live action は bounded buffer から step 順に apply する
- [x] 初期化時の ActionMJStart / ActionNewRound は並べ替えず、step 1 の ActionNewRound が先行したら失敗する

### state API

- [x] `before_callback()` 完了時には version 1 の active MatchState が必ず存在する
- [x] `get_state()` は request / click を行わず、蓄積済み message を drain して最新 snapshot を返す
- [x] `get_state()` の info log に match ID、account ID、player、牌、operation を含めない
- [x] MatchScreen、public state 型、public MatchEvent 型を majsoulrpa.screens.match から export する
- [ ] public operation 型は lazy export を使わず majsoulrpa.screens.match から通常 export する
- [ ] state 待機 API と operation 送信 API は operation model / decoder milestone に含めない

### unified bootstrap

- [ ] host / guest / tournament の実通信ログから fresh entry marker と順序を確認する
- [ ] marker が reload / 途中復帰では fresh evidence として現れないことを確認する
- [ ] 各 entry 経路で bootstrap 中に現れる state 非関連 API 名だけを allowlist として固定する
- [ ] Room / tournament が消費した marker を Screen 遷移直前に一度だけ put_back する
- [ ] direct / put-back marker、authGame、live ActionNewRound で同じ fresh state を初期化できる
- [ ] Login / reload からは recovery entry evidence、authGame、syncGame replay で初期化できる
- [ ] authGame と action source の到着順に依存しない
- [ ] entry kind は UNKNOWN から FRESH / RECOVERY の一方向にだけ遷移する
- [ ] fresh marker と restore syncGame が同じ bootstrap generation に現れた場合は失敗する
- [ ] identical な authGame 再送は no-op、metadata が異なる再送は失敗する
- [ ] marker が match ID を持つ場合、authGame の match ID との矛盾は失敗にする
- [ ] consume 済み marker と以前の Room terminal state を reload 時に fresh evidence として再利用しない
- [ ] public な `restore` flag を使わず message から初期化経路を判定する
- [ ] restore replay は live と同じ reducer を使う
- [ ] restore replay の event は完成 snapshot に含めるが、新着 event として callback へ通知しない
- [ ] recovery entry では restore 完了前の live action を初期 snapshot の代用にしない
- [ ] reload 中に進んだ action を含む syncGame snapshot から current state を復元できる
- [ ] restore request sentinel、is_end、game_state、response.step、action 件数と連番を検証する
- [ ] entry kind、metadata、active round のすべてが揃うまで callback を開始しない
- [ ] pending live / restore / reorder action が 1024 件を超えた場合は捨てずに失敗する
- [ ] 初期化は framework-owned 5 秒で timeout し、screenshot 付き不整合エラーにする
- [ ] source failure と cancellation を初期化エラーへ変換しない
- [ ] 未知 message や矛盾した初期化 message は screenshot 付き不整合エラーにする

### single callback / resync

- [ ] `ActionNewRound` で `MatchScreen` を stale にせず同じ callback を継続する
- [ ] active 中の syncGame は同じ instance の state を authoritative replay で置き換える
- [ ] active 中の syncGame でも match version を巻き戻さない
- [ ] 別 match ID の syncGame を暗黙に受け入れない
- [ ] MatchScreen は generic `Screen.reload()` を継承し、成功後に stale になる
- [ ] Match callback は reload 後に user data を return して runtime の再検出へ戻れる
- [ ] cookie が有効な reload は Login を挟まず、新しい MatchScreen を syncGame から復元する
- [ ] Login を挟む復帰も同じ recovery bootstrap から新しい MatchScreen を復元する
- [ ] reload 後の再検出、bootstrap、timeout、cancellation 失敗を成功扱いにしない
- [ ] callback が active 中に source を読まない場合の queue overflow を隠さない
- [ ] 友人戦の対局終了後に先読みした `.lq.Lobby.fetchRoom` response を 1 回だけ put_back し、
      新しい `RoomScreen` が完全 snapshot として消費できる
- [ ] 自動テストでは synthetic decoded message と synthetic nested protobuf だけを使う

## Phase 7: WebSocket sniffer

- [x] sniffer backend の start に失敗した場合に browser を閉じる

### Envelope decode

- [x] synthetic Notice を分類し、`Wrapper` の API 名と本文を取り出す
- [x] synthetic Request を分類し、2 byte little endian の番号を取り出す
- [x] synthetic Response を分類し、2 byte little endian の番号を取り出す
- [x] Response の明示的な空 API 名 `0A 00` を decode できる
- [x] Response の `Wrapper.name` が空でない場合はエラーにする
- [x] 空 payload、不明な種別、壊れた `Wrapper` を decode error にする
- [x] text frame を対応済み binary frame として扱わない
- [x] 既知 heartbeat を除外する場合は byte 単位の条件を synthetic data で固定する
- [x] decode できない frame を heartbeat として無視しない

### Request / Response 対応

- [x] pending key が connection、request direction、2 byte 番号を含む
- [x] Request は Response 到着まで publish しない
- [x] Response 到着時に反対方向の Request と 1 event にまとめる
- [x] 同じ番号でも connection が違えば独立して対応付ける
- [x] 同じ番号でも Request の方向が違えば独立して対応付ける
- [x] 未完了 key の再利用を duplicate request error にする
- [x] 対応 Request のない Response を unmatched response error にする
- [x] Req/Res が同方向なら direction mismatch error にする
- [x] WebSocket close 時に pending Request が残れば incomplete exchange error にする
- [x] sniffer stop 時に pending Request が残れば成功終了にしない

### Publication / PUB-SUB

- [x] raw Notice publication を schema version 付き JSON にできる
- [x] 対応済み Req/Res publication を schema version 付き JSON にできる
- [x] raw payload は publication 内で base64 として round trip する
- [x] publication は Sniffer topic と JSON の 2-part ZMQ message にする
- [x] publisher は `client_host` と `sniffer_port` の endpoint に bind する
- [x] subscriber は `browser_host` と `sniffer_port` の endpoint へ connect する
- [x] publisher の bind address が IPv6 literal なら ZMQ IPv6 を有効にする
- [x] subscriber の接続先が IPv6 literal なら ZMQ IPv6 を有効にする
- [x] subscriber は Sniffer topic だけを購読する
- [x] unknown field と未対応 schema version を reject する
- [x] `stream_id` の変更を再起動として検出する
- [x] `publication_sequence` の gap と巻き戻りを検出する
- [x] 最初の sequence が 1 より大きければ途中参加として扱う
- [x] fake PUB/SUB socket だけで自動テストできる

### Playwright capture / lifecycle

- [x] fake WebSocket の sent / received binary frame を direction 付きで capture する
- [x] WebSocket ごとに異なる connection id を割り当てる
- [x] frame に capture 順の単調増加番号を付ける
- [x] Playwright callback は bounded queue への投入だけを行う
- [x] capture queue overflow で frame を黙って捨てない
- [x] WebSocket close を connection id 付きeventとしてcaptureする
- [x] WebSocket close 時にそのsocketのlistenerと保持参照を解放する
- [x] 同じWebSocketが重複通知されてもlistenerを二重登録しない
- [x] page navigation より前に PUB bind と listener 登録を完了する
- [x] sniffer worker failure を browser host から伝播する
- [x] sniffer stop でPlaywright listenerを解除する
- [x] sniffer stop でworker、PUB socket、contextをcleanupする
- [x] request server failure と cancellation でも sniffer stop が呼ばれる
- [x] 標準Playwright browser hostは既定の実Sniffer backendを起動する

### Sniffer worker

- [x] captureしたframeをenvelope decodeしてcorrelatorへ渡す
- [x] Noticeをpublisherへ即時送信する
- [x] Requestを保留し、Response到着後に対応済みeventを送信する
- [x] WebSocket closeをcorrelatorへ渡して未完了Requestを検出する
- [x] capture、decode、correlation、publishの失敗を隠さず伝播する
- [x] worker stop時にpending Requestがあれば成功扱いにしない

### Client decode / hook

- [x] wire publicationを利用者向けraw bytes eventへ変換する
- [x] decode済みeventが対応するraw bytes eventを保持する
- [x] `majsoulrpa.sniffer`のexportを利用者向けevent型に限定する
- [x] descriptor から API 名と request / response 型の map を作る
- [x] Notice / Request の本文を対応する protobuf 型へ decode する
- [x] Response を対になった Request の API 名に対応する型へ decode する
- [x] unknown API と protobuf body decode failure を明示的なエラーにする
- [x] client受信runtimeはSUB接続後のpublicationをすべてdecodeして内部queueへ入れる
- [x] decodeとqueue投入の失敗を受信loopから伝播する
- [x] connect失敗、受信失敗、cancellationでsubscriberをcleanupする
- [x] RPA main loopとSniffer受信loopのどちらかが終了したら他方を停止する
- [x] Sniffer受信loopの例外をRPA runtimeから伝播する
- [x] Sniffer受信loopの予期しない正常終了を成功扱いにしない
- [x] RPA main loopの正常終了時にSniffer受信loopをcancelする
- [x] Controller runtimeはREQとは別のSUB socket、decoder、内部queueを組み立てる
- [x] SUB接続完了後に画面検出main loopを開始する
- [x] Controller runtimeは同じ内部message queueをScreenContextへ注入する
- [x] Screen基底はmessageの待機取得、即時取得、差し戻しをprotected操作で委譲する
- [x] ScreenContext構築時にSniffer message sourceを必須にする
- [x] Screen helperは複数のAPI名のいずれかが来るまで待機できる
- [x] Screen helperは読んだmessageの破棄と全差し戻しを選択できる
- [x] 差し戻す場合は対象messageを含めて元の順序を保つ
- [x] 待機のcancellationでも退避中messageを差し戻す
- [x] 空のAPI名集合を拒否する
- [x] Screen共通helperがdecode済みmessageをraw payload bytes抜きでログ用に整形する
- [x] `HomeScreen._discard_sniffer_messages()`が破棄直前に各messageをinfo logへ出す

利用者向けraw / decoded hookは、Screen経由のpayload取得では不足する具体的な
ユースケースが出るまで追加しない。

- [ ] raw payload をデバッグ用ログに出せる
- [ ] raw payload ログのテストは synthetic payload だけを使う
- [x] RPA runtime 終了と cancellation で SUB socket / context を cleanup する

### Client session account ID

- [x] account IDの初期値は`None`にする
- [x] `.lq.Lobby.oauth2Login` responseの`account_id`を取得する
- [x] `.lq.Lobby.createRoom` responseの`room.owner_id`を取得する
- [x] decode直後かつ内部queue投入前に全messageをsession stateへ観測させる
- [x] account IDが欠けているか0なら未取得のままにする
- [x] 同じaccount IDの再観測を許容する
- [x] 同一sessionで異なるaccount IDを観測したら整合性エラーにする
- [x] ScreenContextから最新の`int | None`を読み取り専用で参照できる

### HomeScreen month ticket

- [ ] `before_callback()`先頭の月間チケット判定は全messageを元の順序で戻す
- [x] `.lq.Lobby.payMonthTicket`がなければjade処理を行わない
- [ ] Screen基底helperがtemplate検出まで0.5秒間隔でscreenshotを繰り返す
- [ ] timeoutはhelper引数ではなく呼び出し側の`asyncio.timeout()`で指定する
- [ ] 対象messageがあればjade templateを最大5秒間繰り返し検出する
- [x] jadeを検出したらクリックして0.5秒待機する
- [x] 5秒以内にjadeを検出できなければscreenshot付き検出エラーにする
- [ ] 告知・報酬クリックとHome画面確認が完了した後にqueueをすべて読み捨てる
- [x] 自動テストではsynthetic messageとsynthetic screenshotだけを使う

## examples / docs

- [x] S3 から Yostar 認証メールを取得する example が `config.toml` を読む
- [x] S3 email example は Home 到達後 2 秒待って browser host と RPA を停止する
- [x] `examples/.gitignore` が `config.toml` と `game-records/` を除外する
- [x] examples README に S3 email example の準備と実行順を記載する
- [x] `fetch_log` exampleが入力された牌譜IDのURLへ遷移する
- [x] 空入力まで複数の牌譜IDを順に取得する
- [x] clientをbrowser hostより先に起動する手順を記載する
- [x] `FetchLogScreen.before_callback()`はHomeの告知・報酬処理を省略する
- [x] `fetch_log` exampleが`.lq.Lobby.fetchGameRecord`のReq/Resを待つ
- [x] `fetch_log` exampleがraw response bytesを牌譜ID由来の安全な名前で保存する
- [ ] examples に実メールアドレスが含まれない
- [ ] examples に AWS credential が含まれない
- [ ] examples に実 log id が含まれない
- [ ] examples にライブ通信 payload が含まれない
- [ ] docs に認証コードや token の例が含まれない
- [ ] raw payload をログに出してよいことが docs に書かれている

## Optional integration: Yostar verification email

- [x] `AppConfig` で `yostar_email` 設定を省略できる
- [x] `yostar_email` でメールアドレスだけを設定し、S3 設定を省略できる
- [x] TOML の `[yostar_email.s3]` から bucket、prefix、AWS profile を読める
- [x] Yostar email 設定の空のメールアドレスと bucket 名を拒否する
- [x] Yostar email 設定の `repr` にメールアドレスを含めない
- [x] config example は実メールアドレスや実 AWS 設定を含まない
- [x] code provider は `async fetch()` の `Protocol` として差し替えられる
- [x] MIME message の送信元が Yostar JP の完全一致でなければ拒否する
- [x] 件名が既知の形式に完全一致した場合だけ 6 桁の認証コードを抽出する
- [x] 宛先が要求されたメールアドレスと一致しなければ拒否する
- [x] 受信から 30 分以上経過したメールを期限切れとして拒否する
- [x] 認証コード、メールアドレス、メール本文を例外や repr に含めない
- [x] S3 provider は prefix 以下の最新候補から有効なメールを選ぶ
- [x] S3 provider は不正な候補を無視し、有効な候補がなければ明示的に失敗する
- [x] S3 provider の `fetch()` はメール未着だけを指定間隔で再試行する
- [x] S3 provider の `fetch_nowait()` は S3 を一度だけ確認する
- [x] S3 provider は正でない polling interval を拒否する
- [x] S3 provider の AWS profile は optional とする
- [x] S3 provider は boto3 がなければ必要な extra が分かるエラーにする
- [x] 自動テストは fake S3 client と synthetic MIME message だけを使う
- [x] code provider のメール削除 option は default で無効とする
- [x] S3 provider は削除 option が有効なら読んだ認証メールを有効期限によらず削除する
- [x] S3 provider は指定宛先または認証メール件名と一致しないメールを削除しない
- [x] S3 provider の `fetch()` は polling loop の外で S3 client を 1 回だけ作成する

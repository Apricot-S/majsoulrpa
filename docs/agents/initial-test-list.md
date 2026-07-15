# 初回テストリスト

このテストリストは、v3 の実装開始前に用意する最初のリストです。
実装中に見つかった項目は追加します。TDD では、この中から 1 つだけ選んで
テストを書き、そのテストを通す最小実装を行います。

## Phase 1: 空のプロジェクト骨格

- [x] package を import できる
- [x] `majsoulrpa.__version__` の扱いを決め、テストする
- [x] README が v3 初期状態と安全スコープを説明している
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

認証コード後のログインフローは、まず
[認証コード後のログインフロー計画](login-verification-flow-plan.md) の spike を行い、
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
- [x] 大会用 `error-confirm` から 1.0 秒待機して大会用の戻る座標をクリックする
- [x] 大会用の戻る座標から 1.0 秒待機してホーム画面の対局ボタンを確認する

## Phase 6.10: RoomScreen

詳細な設計判断は [RoomScreen 設計](room-screen-design.md) に従う。以下は実装前の
テストリストであり、高レベル API は記載順に 1 つずつ実装・手動確認する。

### Room state model

- [x] `RoomPlayer` と `RoomState` は immutable である
- [ ] `RoomState.version` は client 内の更新ごとに単調増加する
- [x] `room_id`、owner ID、self account ID、player account ID が正でなければ拒否する
- [x] `max_player_count` は 3 または 4 だけを許す
- [x] human player の account ID 重複を拒否する
- [x] active room の owner と self が human player list にいなければ拒否する
- [x] ready list に未知 account ID があれば拒否する
- [x] human と AI の合計が最大人数を超えたら拒否する
- [x] `RoomPlayer.is_host` を owner ID から導出する
- [x] `RoomPlayer.is_ready` を wire の ready 状態から導出し、host を暗黙に ready にしない
- [x] `self_is_host`、`participant_count`、`available_slots` を snapshot から導出する
- [x] player list は protocol で観測した順序を保つ
- [x] AI を正の account ID を持つ human player として公開しない
- [x] terminal state でも最後に確定した room 情報を保持する

### Room state cache / SnifferMessageSource

- [ ] 成功した `.lq.Lobby.createRoom` response から host の初期 snapshot を作る
- [ ] 成功した `.lq.Lobby.joinRoom` response から guest の初期 snapshot を作る
- [ ] 成功した `.lq.Lobby.fetchRoom` response から reload 後の snapshot を作る
- [ ] error を持つ create / join / fetch response では active room を初期化しない
- [ ] `.lq.NotifyRoomPlayerUpdate` で owner、human、AI を同じ version へ原子的に更新する
- [ ] host 退出後の owner 更新で `self_is_host` を再導出する
- [ ] `.lq.NotifyRoomPlayerReady` で対象 player の ready だけを更新する
- [ ] `.lq.NotifyRoomGameStart` で `MATCH_STARTED` にする
- [ ] `.lq.NotifyRoomKickOut` で `KICKED` にする
- [ ] 成功した `.lq.Lobby.leaveRoom` response で `LEFT` にする
- [ ] terminal 後の古い room notice を active state として復活させない
- [ ] terminal 後の新しい完全 snapshot は新しい room generation を開始する
- [ ] active 中に別 room ID の完全 snapshot が来たら不整合にする
- [ ] 古い RoomScreen generation は新しい room で stale になる
- [ ] room 状態用の decode 直後 observer や background task を追加しない
- [ ] RoomScreen は `SnifferMessageSource.get_nowait()` で蓄積済み message を順番に処理する
- [ ] RoomScreen は `SnifferMessageSource.get()` で新しい message を待機する
- [ ] callback ごとに RoomScreen instance が変わっても共有 cache から最新 snapshot を得られる
- [ ] cache は最新 snapshot と room generation 以外の raw message 履歴を保持しない
- [ ] `HomeScreen.create_room()` は成功した createRoom message を RoomScreen 用に source へ残す
- [ ] `HomeScreen.join_room()` は成功確認後に元の joinRoom message を 1 回だけ差し戻す
- [ ] joinRoom の失敗 message は RoomScreen 用に差し戻さない
- [ ] wait は cache が `after_version` より新しければ即時に返せる
- [ ] wait は source の `get()` を使い sleep polling しない
- [ ] wait 中の cancellation で適用済み snapshot を壊さない
- [ ] Sniffer decode、stream gap、queue overflow を room state で成功扱いにしない

### RoomScreen detection / state API

- [ ] `RoomScreen` が `Screen` を継承する
- [ ] 個人情報を含まない room template の synthetic screenshot で検出できる
- [ ] threshold 未満の screenshot では検出しない
- [ ] `before_callback()` は active room snapshot が得られるまで framework 内部の既定期限で待つ
- [ ] 画像だけ room で snapshot がなければ状態を推測せず失敗する
- [ ] `before_callback()` は source の蓄積済み message を処理して cache を最新化する
- [ ] `get_state()` は network request や click を行わず最新 immutable snapshot を返す
- [ ] RoomScreen の全高レベル API は `timeout` 引数を持たない
- [ ] 呼び出し側の `asyncio.timeout()` で `get_state()` を中断できる
- [ ] `wait_for_state_change()` は `after_version` より新しい snapshot を返す
- [ ] `wait_for_state_change()` は kick / game start の terminal snapshot も 1 回返す
- [ ] 呼び出し側 timeout による cancellation を RoomScreen が握りつぶさない
- [ ] room ID、account ID、player 名を高レベル API log に含めない

### Failure model

- [ ] server rejection は Enum 戻り値ではなく `RoomOperationRejectedError` にする
- [ ] rejection error が operation、reason Enum、元の整数 code を保持する
- [ ] 未対応 code は数値を warning log に出し `UNRECOGNIZED_ERROR_CODE` にする
- [ ] server の error message、room ID、account ID、player 名を例外 message に含めない
- [ ] role / 満員 / 未 ready の事前条件失敗では browser operation を行わない
- [ ] 事前条件失敗は operation と machine-readable な reason Enum を保持する
- [ ] response 欠落と notice 欠落を server rejection に変換しない
- [ ] malformed response / notice を空状態や通常失敗へ変換しない
- [ ] browser / Sniffer infrastructure error を Room 用 rejection に変換しない
- [ ] Room API の cancellation を cleanup 後に伝播する

### `leave()`

- [ ] host と guest の `WAITING` state で退出 UI を操作できる
- [ ] click 前に source を drain し、その後の outbound `.lq.Lobby.leaveRoom` を対応付ける
- [ ] 過去の leaveRoom response を今回の成功に使わない
- [ ] 成功 response を観測した後だけ `LEFT` にして RoomScreen を stale にする
- [ ] server rejection では active state と Screen を維持する
- [ ] `MATCH_STARTED` の guest は退出 UI を操作できない
- [ ] kick が leave 待機に割り込んだら呼び出し側 timeout より先に stale error にする
- [ ] `leave()` の実ゲーム確認後まで `add_ai()` の実装へ進まない

### `add_ai()`

- [ ] 最新 snapshot で host の場合だけ AI 追加 UI を操作する
- [ ] participant が満員なら UI を操作しない
- [ ] source refresh 後の最新 host / capacity を使って事前条件を検証する
- [ ] click 前に source を drain し、その後の outbound `.lq.Lobby.addRoomRobot` を対応付ける
- [ ] 成功 response だけでは完了せず、後続 player update で AI が 1 増えるまで待つ
- [ ] AI 数が 1 以外増減した場合は今回の成功として扱わない
- [ ] server rejection を自動 retry しない
- [ ] response 成功後に player update がなければ成功扱いにせず呼び出し側 timeout まで待つ
- [ ] 成功時は更新後の `RoomState` を返し Screen を active のままにする
- [ ] `add_ai()` の実ゲーム確認後まで `set_ready()` の実装へ進まない

### `set_ready()`

- [ ] 最新 snapshot で guest の場合だけ ready UI を操作する
- [ ] host が呼んだ場合は UI を操作せず不正操作エラーにする
- [ ] すでに ready の guest は click せず同じ snapshot を返す
- [ ] click 前に source を drain し、その後の outbound `.lq.Lobby.readyPlay` を対応付ける
- [ ] readyPlay request の `ready` が `true` でなければ不整合にする
- [ ] 成功 response だけでは完了せず、自分の ready notice まで待つ
- [ ] 別 player の ready notice を自分の成功として扱わない
- [ ] 成功時は自分が ready の `RoomState` を返し Screen を active のままにする
- [ ] `set_ready()` の実ゲーム確認後まで `start_match()` の実装へ進まない

### `start_match()`

- [ ] 最新 snapshot で host の場合だけ start UI を操作する
- [ ] human guest が 1 人でも未 ready なら UI を操作しない
- [ ] AI を含む participant が最大人数未満なら UI を操作しない
- [ ] ready 判定から host を除外する
- [ ] source refresh 後の最新 host、ready、満員を使って事前条件を検証する
- [ ] click 前に source を drain し、その後の outbound `.lq.Lobby.startRoom` を対応付ける
- [ ] 成功 response だけでは完了せず game start notice まで待つ
- [ ] game start notice 後だけ `MATCH_STARTED` にして RoomScreen を stale にする
- [ ] guest が外部 host の start を観測した場合も `MATCH_STARTED` にする
- [ ] server rejection では RoomScreen を stale にしない

### RoomScreen 手動確認

- [ ] 四人 / 三人 room の snapshot field の意味を確認する
- [ ] `persons`、`robots`、`robot_count`、`positions` の関係を確認する
- [ ] ready notice の `account_list` と `seq` の意味を確認する
- [ ] host 退出後の owner update と host 交代を確認する
- [ ] kick notice と画面遷移を確認する
- [ ] AI 追加成功、満員、guest の UI / response を確認する
- [ ] 空席、未 ready、全 ready の start 条件を確認する
- [ ] host / guest の退出と対局開始後の退出不可を確認する
- [ ] room operation の既知 error code と dialog 復旧可否を確認する
- [ ] Room / room notice の `seq` 増加規則を確認する
- [ ] 実 payload を tests、fixtures、docs、chat、commit へ含めない
- [ ] 個人情報のない必要画像と settings はユーザーがコミットする

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

# 初回テストリスト

このテストリストは、v3 の実装開始前に用意する最初のリストです。
実装中に見つかった項目は追加します。TDD では、この中から 1 つだけ選んで
テストを書き、そのテストを通す最小実装を行います。

## Phase 1: 空のプロジェクト骨格

- [x] package を import できる
- [x] `majsoulrpa.__version__` の扱いを決め、テストする
- [x] README が v3 初期状態と安全スコープを説明している
- [ ] Sphinx や古い API docs に依存しない
- [ ] `pyproject.toml` の optional dependency group が解決できる
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
- [ ] secret に相当する値を config repr に出さない
- [ ] secret に相当する値を validation error に出さない

## Phase 3: browser host lifecycle

- [x] browser host 起動成功時に running 状態になる
- [x] browser host 起動失敗時に例外を返す
- [x] 起動失敗を成功扱いにしない
- [x] stop を 1 回呼ぶと stopped 状態になる
- [x] stop を 2 回呼んだ場合の挙動を固定する
- [x] 起動中に cancellation された場合に cleanup する
- [ ] sniffer backend の start に失敗した場合に browser を閉じる
- [x] shutdown 中の副次的失敗を完全には捨てない
- [x] Playwright backend が config から browser context と page を作る
- [x] Playwright command executor が click、text input、screenshot を実行する
- [x] Playwright command executor の操作失敗は error response にする

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
- [x] Screen 未検出のまま timeout したら現在の data を返す
- [x] callback 実行中の cancellation で cleanup する
- [x] data を log しない

## Phase 5: Screen base

- [x] fake screenshot で Screen を検出できる
- [x] Screen detection が false のとき callback されない
- [x] Screen detection が例外を投げたら隠さない
- [x] 複数 Screen が一致した場合は登録順で選ばれる
- [x] Screen から browser controller 経由で操作できる
- [x] ScreenContext から stop 要求を出せる
- [x] 検出された Screen に ScreenContext を注入できる
- [x] ScreenContext 未設定の Screen 操作は例外になる

## Phase 5.5: Browser 操作層

- [x] remote transport は command の send と response の recv を分ける
- [x] browser controller は `fill_region` を command / response に変換する
- [x] browser controller は remote error response を例外にする
- [x] browser host へ送る command は click 座標や text など低レベル情報にする
- [x] click command は mouse down/up 間の delay を持つ
- [x] text input command は等間隔の文字入力 delay を持つ
- [x] browser controller は screenshot command の base64 response を PNG bytes として返す
- [x] response は click、text input、error を別型にする

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
- [x] `LoginScreen.enter_email_address()` の固定領域は実 viewport サイズへ scale される

候補:

- [x] `LoginScreen.enter_email_address()` が入力欄への browser operation を記録する
- [ ] `LoginScreen.enter_email_address()` の実領域をスクリーンショット確認で確定する
- [ ] `LoginScreen.enter_verification_code()` が認証コード欄へ入力する

どちらを選ぶ場合も、先に fake browser operation のテストを書きます。
実ゲーム確認が終わるまで、もう片方には進みません。

## Phase 7: WebSocket sniffer

- [ ] fake sniffer backend が synthetic payload を発行できる
- [ ] raw payload を hook に渡せる
- [ ] raw payload をデバッグ用ログに出せる
- [ ] raw payload ログのテストは synthetic payload だけを使う
- [ ] decode 失敗を成功扱いにしない
- [ ] hook が例外を投げた場合の扱いを固定する
- [ ] sniffer stop が呼ばれる

## examples / docs

- [ ] examples に実メールアドレスが含まれない
- [ ] examples に AWS credential が含まれない
- [ ] examples に実 log id が含まれない
- [ ] examples にライブ通信 payload が含まれない
- [ ] docs に認証コードや token の例が含まれない
- [ ] raw payload をログに出してよいことが docs に書かれている

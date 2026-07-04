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
- [ ] TOML から `AppConfig` を作れる
- [ ] TOML の未知 key をエラーにする
- [x] endpoint の host が空文字の場合にエラーにする
- [x] port が範囲外の場合にエラーにする
- [x] viewport height が許可値外の場合にエラーにする
- [x] `user_data_dir` が未指定の場合の意味が明確である
- [ ] secret に相当する値を config repr に出さない
- [ ] secret に相当する値を validation error に出さない

## Phase 3: browser host lifecycle

- [ ] browser host 起動成功時に running 状態になる
- [ ] browser host 起動失敗時に例外を返す
- [ ] 起動失敗を成功扱いにしない
- [ ] stop を 1 回呼ぶと stopped 状態になる
- [ ] stop を 2 回呼んだ場合の挙動を固定する
- [ ] 起動中に cancellation された場合に cleanup する
- [ ] capture backend の start に失敗した場合に browser を閉じる
- [ ] shutdown 中の副次的失敗を完全には捨てない

## Phase 4: callback dispatch

- [ ] `RPAApp.on(Screen)` で async callback を登録できる
- [ ] sync callback 登録をエラーにする
- [ ] 同じ Screen への重複登録をエラーにする
- [ ] 未登録 Screen は dispatch しない
- [ ] 登録順に detection を試す
- [ ] callback の戻り値が次の state になる
- [ ] callback が例外を投げたら `run()` から伝播する
- [ ] detection timeout で明示的な例外になる
- [ ] callback 実行中の cancellation で cleanup する
- [ ] state を log しない

## Phase 5: Screen base

- [ ] fake screenshot で Screen を検出できる
- [ ] Screen detection が false のとき callback されない
- [ ] Screen detection が例外を投げたら隠さない
- [ ] 複数 Screen が一致した場合は登録順で選ばれる
- [ ] ScreenContext から browser operation を記録できる
- [ ] ScreenContext から stop 要求を出せる

## Phase 6: Login API ひとつ目

最初に実装する高レベル API は、実装直前に 1 つ選びます。

候補:

- [ ] `LoginScreen.enter_email_address()` が入力欄を探して入力する
- [ ] `LoginScreen.enter_verification_code()` が認証コード欄へ入力する

どちらを選ぶ場合も、先に fake browser operation のテストを書きます。
実ゲーム確認が終わるまで、もう片方には進みません。

## Phase 7: WebSocket capture

- [ ] fake capture backend が synthetic payload を発行できる
- [ ] raw payload を hook に渡せる
- [ ] raw payload をデバッグ用ログに出せる
- [ ] raw payload ログのテストは synthetic payload だけを使う
- [ ] decode 失敗を成功扱いにしない
- [ ] hook が例外を投げた場合の扱いを固定する
- [ ] capture stop が呼ばれる

## examples / docs

- [ ] examples に実メールアドレスが含まれない
- [ ] examples に AWS credential が含まれない
- [ ] examples に実 log id が含まれない
- [ ] examples にライブ通信 payload が含まれない
- [ ] docs に認証コードや token の例が含まれない
- [ ] raw payload をログに出してよいことが docs に書かれている

# `src/majsoulrpa` コード改善チェックリスト

## 目的

次の機能改修へ進む前に、`src/majsoulrpa/` 配下の責務、依存方向、公開 API、
失敗モデル、テスト容易性をファイルツリーごとに確認する。

この確認は動作を維持する内部リファクタリングだけに限定しない。設計上の理由があれば、
引数の渡し方、例外の型・発生条件などの公開契約も変更候補に含める。ただし、既存動作を
無条件に契約とみなすことも、改善のためという理由だけで互換性を軽視することもしない。

このリストは変更内容を先に決めるものではない。各項目を確認し、変更が必要なら先に
`docs/development/test-plan.md` へ具体的なテスト項目を追加してから、t_wada の TDD 手順で
ひとつずつ実施する。ファイルが大きいことや `Protocol` が多いことだけを理由に分割・統合しない。

## 完了の記録方法

- [ ] 各ファイルまたは資産グループについて、現状維持、変更、後続タスク化のいずれかを判断する。
- [ ] 変更する場合は、守る振る舞いと失敗経路をテストリストへ先に追加する。
- [ ] 引数、戻り値、例外などの契約を変更する場合は、理由、影響範囲、互換性の扱いを記録し、テストと公開ドキュメントを更新する。
- [ ] 公開 API、wire schema、生成物、画像資産に影響する変更は、影響範囲を明記する。
- [ ] 1 項目の変更ごとに関連テストを通し、まとまりごとに品質ゲートを通す。

## 全ファイル共通の確認観点

この節は、すでに個別確認を完了したファイルにも遡及して適用する。追加された観点は
該当サブツリーの完了までに再確認し、必要なら個別項目を再度開く。

- [ ] 責務が現在のアーキテクチャと一致し、別 component の都合を抱え込んでいない。
- [ ] 依存方向が `RPAApp -> client runtime -> Screen / browser client / Sniffer` を逆流しない。
- [ ] 抽象化は fake への置換、実装差し替え、lifecycle 管理、公開拡張点のいずれかに寄与する。
- [ ] 単なる横流し wrapper、重複 DTO、将来予測だけの interface が増えていない。
- [ ] public と private の境界、export、命名、型注釈が実際の契約と一致する。
- [ ] 関数・メソッドの各引数について positional / keyword-only の選択に明確な理由があり、特に optional 引数を慣例だけでキーワード専用にしていない。
- [ ] timeout と cancellation を握りつぶさず、cleanup の失敗も見えなくしていない。
- [ ] decode・validation・remote 操作の失敗を空値や成功へ変換していない。
- [ ] mutable state の所有者、初期化条件、不変条件、terminal / stale 遷移が明確である。
- [ ] ログ、`repr`、例外、serialization に secret、user data、個人情報が漏れない。
- [ ] 実通信 payload、実メール、実画像を test、fixture、example、docs に持ち込んでいない。
- [ ] optional dependency は必要な module まで遅延 import され、core import を重くしていない。
- [ ] 重複を除去する場合も、異なる失敗モデルや lifecycle を無理に共通化していない。
- [ ] 対応する unit / lifecycle / cancellation / failure test があり、振る舞いを説明できる。

## ルート

- [x] `__init__.py`: `AppConfig`、`RPAApp`、version だけの小さい公開 surface、および core import の軽さを確認する。
- [x] `_clock.py`: UTC aware clock とテスト用注入点の必要性・配置を確認する。
- [x] `app.py`: callback 登録、重複検出、runtime composition への委譲、data 非介入を確認する。
  - [x] async callbackだけを登録し、重複を拒否し、登録順を維持することをテストする。
  - [x] callback間でdataの型とidentityを保ったまま受け渡し、表現・log出力しないことをテストする。
  - [x] callback例外・cancellation・画面検出timeoutを伝播し、runtime cleanupを実行することをテストする。
  - [x] `detection_timeout`の検証は期限計算と直接利用を担う`RPARuntime.run()`へ置き、`RPAApp.run()`は委譲に留める。
  - [x] 注入されたruntime factoryをtruthinessで置き換えず、falsey callableでも使用することをテストする。
  - [x] callback registryは共有mappingのままruntimeへ渡す。検出対象typeはruntime loop開始時にsnapshotされ、公開APIでは既存callbackの置換・削除を許可しない。
- [x] `cli.py`: CLI 引数から config への変換、終了コード、secret 非表示、browser runner との境界を確認する。
  - [x] config fileを読み、指定されたCLI overrideだけをimmutableな`AppConfig`へ反映してrunnerへ渡すことをテストする。
  - [x] 正常終了を`0`、`KeyboardInterrupt`をtracebackなしの`130`として返すことをテストする。
  - [x] browser runnerの起動例外を成功終了へ変換せず、そのまま伝播することをテストする。
  - [x] 不正なCLI overrideではbrowser runnerを呼ばず、config validation errorを伝播することをテストする。
  - [x] `--version`がpackageの`__version__`を表示して`0`で終了することをテストする。
- [x] `config.py`: default、strict validation、immutable 性、secret の `repr` / validation error 非表示を確認する。
  - [x] `email_address` を `YostarEmailConfig` と `AppConfig` の `repr` に表示しないことをテストする。
  - [x] 型不正な `email_address` を含む validation error にメールアドレスを表示しないことをテストする。
  - [x] endpoint host が空白だけの場合を拒否し、後段へ不正な ZeroMQ endpoint を渡さないことをテストする。
  - [x] `remote_port` と `sniffer_port` が同じ場合を bind 前に拒否することをテストする。
  - [x] TOML の型誤りを拒否し、port・boolean・整数設定の契約をテストする。
- [x] `constants.py`: component 固有値がルートへ流出していないか、定数の単位と根拠を確認する。
- [x] `endpoint.py`: browser/client の接続先 semantics、IPv4・hostname・IPv6 literal の整形重複を確認する。
  - [x] browser command と Sniffer の4経路が、接続側の `browser_host`、bind側の `client_host`、対応するportを選ぶことをテストする。
  - [x] IPv4・hostnameを維持し、IPv6 literalをZeroMQのauthority用に角括弧で囲むことをテストする。
  - [x] IPv6判定を共通化し、browser REQ/REPでもsocketの `ZMQ_IPV6` をbind/connect前に有効化することをテストする。
  - [x] `make_tcp_endpoint()`の必須引数`host, port`は自然な順序と異なる型を持つため、キーワード専用を解除する。
- [x] `timing.py`: delay の範囲・単位・乱数注入、固定 sleep の代用になっていないことを確認する。
  - [x] `base_delay` と `sigma` の `NaN`・無限大を拒否し、再標本化 loop が終了不能にならないことをテストする。
  - [x] 最初の標本が 0 以下なら再標本化し、正の delay を返す分岐をテストする。
- [x] `types.py`: callback generic が公開 API を正しく表し、不要な共通型置き場になっていないことを確認する。
- [x] `viewport.py`: 対応 viewport の制約と config / template scale との責務分担を確認する。

### rootのキーワード専用引数確認

- [x] `__init__.py`、`_clock.py`、`constants.py`、`types.py`、`viewport.py`には、キーワード専用にするか判断すべき複数引数のcallableがない。
- [x] `app.py`: `RPAApp.run()`の`detection_timeout`は主要入力の`config, data`と異なるruntime policyで、同じ位置に固定せず呼び出し側で名前を読めるため、キーワード専用を維持する。
- [x] `app.py`: `RPAApp.on()`の`screen_type`、`run()`の`config, data`、runtime factoryの`callbacks, config`は主要入力または自然な順序を持つため、位置引数を維持する。`RPAApp.__init__()`のfactoryは単独引数なので位置指定も許容する。
- [x] `cli.py`: `argv`は`main()`の主要入力として位置指定を維持し、`run_browser_host`はCLI利用者向けオプションではなく注入用collaboratorなのでキーワード専用を維持する。
- [x] `config.py`: Pydantic modelのfieldは名前付き設定schemaであり、同型fieldの取り違え防止とfield追加時の安定性が必要なため、constructorのキーワード指定を維持する。validatorとTOML loaderの単独引数は位置指定を維持する。
- [x] `endpoint.py`: `make_tcp_endpoint()`の`host, port`だけはキーワード専用を強制する理由が弱いため解除する。その他のendpoint helperは単独の主要入力を位置指定のまま維持する。
- [x] `timing.py`: `base_delay`は主要入力として位置指定を維持する。`sigma`は同じfloat型の分布調整値、`rng`は注入用collaboratorなので、取り違え防止のためキーワード専用を維持する。

## `browser/`

- [ ] `browser/__init__.py`: lazy export が optional Playwright import を隔離し、不足 extra を明示することを確認する。
  - [ ] lazy import中の`ModuleNotFoundError`は不足しているmoduleがPlaywright自身の場合だけinstall案内へ変換し、Playwright module内の別のimport失敗を隠さないことをテストする。
- [ ] `browser/messages.py`: command / response の判別共用体、strict schema、secret を含まない wire 契約を確認する。
  - [ ] wire modelをstrictかつ`NaN`・無限大を拒否する設定にし、文字列から数値への型変換や非有限の座標・delayを受理しないことをテストする。
  - [ ] malformed payloadのvalidation errorに入力値を表示せず、textや認証関連値が例外経由で漏れないことをテストする。
- [x] `browser/transport.py`: client と server の最小 `Protocol` が fake と remote I/O の分離に実際に使われることを確認する。
- [x] `browser/controller.py`: Screen 向け操作 semantics、型付き request 共通処理、unexpected response の失敗を確認する。
- [x] `browser/history.py`: command / response summary の網羅性、座標以外の text・認証情報の redaction を確認する。
- [x] `browser/server.py`: 1 request / 1 response、stop response 後の停止、executor 例外の伝播を確認する。
- [ ] `browser/zmq.py`: REQ/REP 順序、bind/connect、socket lifecycle、transport error の情報量を確認する。
  - [ ] Windows向けRuntimeWarning抑制をprocess-globalなfilterとして残さず、request serverのbind処理中だけに限定する。
- [ ] `browser/playwright.py`: 操作の原子性、mouse down 後 cleanup、HTTP response 待機、raw auth response の隔離を確認する。
  - [x] headless user-agent取得を外部Googleへのnavigationに依存させず、blank pageで取得できることをテストする。
  - [x] user-agent取得中の失敗も起動failure cleanupの対象に含め、開始済みPlaywrightを停止することをテストする。
  - [x] Yostar応答の`Code`にJSON booleanを整数として受理せず、明示的なerror responseにすることをテストする。
- [ ] `browser/runner.py`: backend・server・Sniffer の開始順、逆順 cleanup、主例外と副次例外の扱いを確認する。
  - [ ] 既定ZMQ contextを作成直後からcleanup対象にし、backend start・Sniffer start・navigationの失敗でも`term()`することをテストする。
  - [ ] serverまたはSnifferの主失敗後、兄弟taskがcancellation cleanupで別の例外を出しても主失敗を失わず、副次例外も確認できることをテストする。

### `browser/`のキーワード専用引数確認

- [x] `messages.py`のPydantic fieldはwire schemaの名前付きfieldであり、同型の座標・delay・textを順序で渡さないため、constructorのキーワード指定を維持する。
- [x] `controller.py`はtransportを主要入力として位置指定し、乱数源・delay設定と`click()`の`warp`は省略可能なpolicyで取り違えやすいため、キーワード専用を維持する。
- [x] `playwright.py`の`page_ready`は起動途中へ差し込むhook、browser起動helperの各引数は同型値を含む設定群であるため、キーワード専用を維持する。Playwright互換Protocolの`delay`と`timeout`も接続先APIの署名に合わせる。
- [x] `runner.py`はconfigを主要入力として位置指定し、backend・Sniffer・factory群は通常利用から分離した注入点なので、キーワード専用を維持する。
- [x] `zmq.py`のrequest server constructorはcontext・endpoint・executor・IPv6設定をcomposition rootで明示する配線用APIなので、キーワード専用を維持する。
- [x] `__init__.py`、`transport.py`、`history.py`、`server.py`には解除を検討すべきキーワード専用引数がない。

## `client/`

- [ ] `client/__init__.py`: 空の package root を維持する必要性と、意図しない public export がないことを確認する。
- [ ] `client/runtime.py`: 登録 Screen の検出順、callback/data loop、兄弟 task、timeout・stop・cleanup を確認する。
  - [ ] `detection_timeout`を`None`または有限の正数に限定し、`NaN`・無限大・0以下で終了不能にならないことをテストする。
- [ ] `client/controller_runtime.py`: composition root として ZMQ、controller、Sniffer、session、`ScreenContext` だけを組み立てることを確認する。
- [ ] `client/session.py`: decode 後 enqueue 前の account ID 観測、正値・再観測・不一致の不変条件を確認する。

## `presentation/`

- [ ] `presentation/__init__.py`: OpenCV を core import から隔離する lazy export と公開名の一貫性を確認する。
- [ ] `presentation/region.py`: immutable value object、scale、座標境界、random point の決定可能なテストを確認する。
- [ ] `presentation/template.py`: TOML validation、PNG adapter と ndarray matcher の分離、scale・margin・threshold の不変条件を確認する。

## `screens/` 共通

- [ ] `screens/__init__.py`: 標準 Screen と共通例外の public export が設計資料と一致することを確認する。
- [ ] `screens/errors.py`: 例外階層、`TimeoutError` / `ValueError` との多重継承、screenshot 保持・保存時の情報漏洩を確認する。
- [ ] `screens/base.py`: `ScreenContext` の依存、検出 contract、stale guard、API log、Sniffer helper の責務集中を確認する。
- [ ] `screens/login.py`: 認証 sequence、request-scoped HTTP wait、stale 化の時点、email/code/token 非漏洩を確認する。
- [ ] `screens/home.py`: 前処理 loop と各高レベル遷移を区別し、巨大な条件分岐・重複 template 操作・message 先読みを確認する。

### `screens/room/`

- [ ] `screens/room/__init__.py`: state・error・Screen の export と lazy import の必要性を確認する。
- [ ] `screens/room/state.py`: frozen snapshot、derived host state、active / terminal status の表現を確認する。
- [ ] `screens/room/_decode.py`: synthetic mapping の strict decode、field error、正値・重複・人数制約の分担を確認する。
- [ ] `screens/room/store.py`: instance-local state、snapshot/update/terminal 遷移、message 履歴を保持しないことを確認する。
- [ ] `screens/room/errors.py`: operation と reason Enum、未知 server code、例外 message の個人情報非表示を確認する。
- [ ] `screens/room/screen.py`: source drain、操作 lock、Req/Res と notice の相関、terminal 後 stale、画面消失待機を確認する。

### `screens/match/` の基盤

- [ ] `screens/match/__init__.py`: public state/event/operation 型の export、lazy export の要否、union の網羅性を確認する。
- [ ] `screens/match/types.py`: `Seat` / `Tile` の型と runtime validator が全入口で一貫して使われることを確認する。
- [ ] `screens/match/_common.py`: tile 正規化・並び順・鳴き条件の共通化が domain invariant に限られることを確認する。
- [ ] `screens/match/_decode.py`: JSON field helper が strict で、欠落や型不正を default 値へ変換しないことを確認する。
- [ ] `screens/match/_metadata.py`: human / robot / seat / rank decode と match metadata の不変条件を確認する。
- [ ] `screens/match/_action.py`: live / restore adapter、deobfuscation、API 名と action 名の対応、未知 action の失敗を確認する。
- [ ] `screens/match/state.py`: immutable snapshot、四麻・三麻、round state、event 列、version の不変条件を確認する。
- [ ] `screens/match/store.py`: live と restore の同一 reducer、atomic restore、step reorder、rollback 禁止、状態更新の責務境界を確認する。
- [ ] `screens/match/screen.py`: bootstrap、fresh/recovery 判定、message buffering、callback lifecycle、画面操作が一つの責務へ混在していないか確認する。

`screen.py` と `store.py` は大きいが、行数だけでは分割しない。分割する場合は、独立した不変条件、
異なる lifecycle、または単独でテストする価値のある境界を先に示す。

### `screens/match/event/`

- [ ] `event/__init__.py`: `MatchEvent` が全 concrete event を明示列挙し、`assert_never()` による網羅性を保つことを確認する。
- [ ] `event/_base.py`: 共通 base が event の識別や DTO 層を重複させず、必要最小限であることを確認する。
- [ ] `event/_constants.py`: event 固有定数の根拠と共有範囲を確認する。
- [ ] `event/start_match.py`: BOS event の field と reducer 上の意味を確認する。
- [ ] `event/new_round.py`: initial hand、score、dora、round metadata の不変条件を確認する。
- [ ] `event/zimo.py`: draw source、lingshang、tile/seat/step の整合性を確認する。
- [ ] `event/dapai.py`: discarded tile、moqie、liqi/wliqi、nested success との整合性を確認する。
- [ ] `event/liqi_success.py`: nested value object としての点数・供託・seat 更新を確認する。
- [ ] `event/chi.py`: 上家制約、取得牌と consumed、赤牌正規化、直前打牌の解決を確認する。
- [ ] `event/peng.py`: 取得元、同種牌、手牌消費、直前打牌の解決を確認する。
- [ ] `event/daminggang.py`: 取得元、3 枚消費、lingshang 遷移、直前打牌の解決を確認する。
- [ ] `event/angang.py`: 4 枚 canonicalization、手牌消費、lingshang 遷移を確認する。
- [ ] `event/jiagang.py`: 既存 peng の更新、追加牌、qianggang 関連状態を確認する。
- [ ] `event/babei.py`: 三麻限定条件、北抜き回数、lingshang 相当の遷移を確認する。
- [ ] `event/hule.py`: 和了者ごとの score/fan/責任払い情報、複数和了、終局状態を確認する。
- [ ] `event/no_tile.py`: 聴牌/不聴、流局 score、手牌公開、終局状態を確認する。
- [ ] `event/liuju.py`: 特殊流局の closed set と未知値の扱いを確認する。

各 concrete event は `@final`、`frozen=True`、`slots=True` の方針、`kw_only=True` の必要性、
constructor の runtime invariant、live / restore 双方から同じ object が作られることをまとめて確認する。

### `screens/match/operation/`

- [ ] `operation/__init__.py`: 利用者向け operation 型だけを通常 export し、内部 specification を漏らさないことを確認する。
- [ ] `operation/models.py`: immutable operation と `MatchOperation` union、候補の排他性・順序を確認する。
- [ ] `operation/_specification.py`: protobuf decode 直後の内部表現が public model と重複するだけの層になっていないか確認する。
- [ ] `operation/_decode.py`: operation list の strict decode、組合せ順、未知 type・不正 field の失敗を確認する。
- [ ] `operation/_materialize.py`: current state/event との相関、手牌・fulu・seat 不変条件、候補重複除去を確認する。

`_materialize.py` を分割する場合は、牌操作種別ごとの見た目ではなく、共有 validation と各 operation の
独立した invariant が明確に分かれるかを基準にする。

## `sniffer/`

- [ ] `sniffer/__init__.py`: raw / decoded 利用者向け event だけを export し、wire model や backend を漏らさないことを確認する。
- [ ] `sniffer/events.py`: raw bytes と decoded JSON-compatible body、timestamp、direction の immutable 契約を確認する。
- [ ] `sniffer/playwright.py`: listener 登録解除、binary frame 限定、bounded queue、connection/capture sequence を確認する。
- [ ] `sniffer/envelope.py`: message kind、request number、Wrapper、API 名の byte-level strict decode を確認する。
- [ ] `sniffer/correlator.py`: connection/direction/number key、duplicate/unmatched/incomplete exchange の失敗を確認する。
- [ ] `sniffer/publication.py`: schema version、base64 validation、sequence metadata、unknown field rejection を確認する。
- [ ] `sniffer/event_adapter.py`: wire publication から raw event への変換境界が decoder と重複せず、bytes 復元を一元化することを確認する。
- [ ] `sniffer/decoder.py`: descriptor map、Notice/Req/Res body decode、publication/envelope API 一致、未知 API の失敗を確認する。
- [ ] `sniffer/stream.py`: restart、gap、rollback、途中参加を区別し、欠落を補完したふりをしないことを確認する。
- [ ] `sniffer/message_queue.py`: message 件数と payload byte の両上限、put-back 順序、overflow の明示失敗を確認する。
- [ ] `sniffer/worker.py`: capture -> envelope -> correlation -> publication の順序と、stop 時 pending request の失敗を確認する。
- [ ] `sniffer/runtime.py`: context・publisher・capture・worker の開始順、逆順 cleanup、失敗伝播を確認する。
- [ ] `sniffer/zmq.py`: PUB/SUB topic、bind/connect、IPv6、socket/context cleanup、multipart validation を確認する。
- [ ] `sniffer/client_runtime.py`: receive -> stream validation -> raw adapter -> protobuf decode -> observer -> queue の順序を確認する。

Sniffer の各段は異なるデータ完全性を守るため、ファイル数だけを理由に大きな service へ統合しない。
統合候補は、失敗分類と synthetic unit test の境界を維持できる場合だけ検討する。

## `yostar_email/`

- [ ] `yostar_email/__init__.py`: optional integration の公開 surface と boto3 非依存 import を確認する。
- [ ] `yostar_email/constants.py`: sender、subject、期限などの値と調査根拠を確認する。
- [ ] `yostar_email/errors.py`: 利用者が再試行可否を判断でき、secret を message に含めない例外階層を確認する。
- [ ] `yostar_email/provider.py`: `VerificationCodeProvider` が実際の公開差し替え点として最小であることを確認する。
- [ ] `yostar_email/email.py`: MIME sender/recipient/subject/date の strict validation と code/email/body 非漏洩を確認する。
- [ ] `yostar_email/s3.py`: boto3 遅延 import、候補順、polling 条件、任意削除の対象制約、client lifecycle を確認する。

## `assets/`

- [ ] `assets/__init__.py`、`assets/templates/__init__.py`: package data のためだけの初期化ファイルとして不要な API を持たないことを確認する。
- [ ] `assets/templates/login/`: `__init__.py` の loader、PNG/TOML の対、命名、viewport 設定、個人情報非包含を確認する。
- [ ] `assets/templates/home/`: root、`create_room/`、`join_room/`、`tournament_lobby/` の loader と PNG/TOML 対応を確認する。
- [ ] `assets/templates/room/`: detection / leave / add-ai / ready / start / cancel の loader、共有 PNG、variant TOML の対応を確認する。
- [ ] `assets/templates/match/`: action、seat indicator、round/match result、skip、liuju の loader と PNG/TOML 対応を確認する。
- [ ] `assets/templates/tournament/`: leave template の loader と PNG/TOML 対応を確認する。
- [ ] `assets/protocol/__init__.py`: 生成 protocol package の境界と import 経路を確認する。
- [ ] `assets/protocol/liqi.proto`: 手編集せず、更新理由、入手元、安全性、生成手順が明示されていることだけを確認する。
- [ ] `assets/protocol/liqi_pb2.py`、`liqi_pb2.pyi`: 生成物として手編集せず、`.proto` との再生成可能性と package inclusion を確認する。

画像、`.proto`、protocol 生成物の追加・更新が必要な場合はエージェントだけで行わず、目的と
安全性を明示してユーザーにコミットを依頼する。

## サブツリー完了時の品質ゲート

- [ ] 対象サブツリーの関連 pytest が成功する。
- [ ] `uv --cache-dir .uv_cache run python -m ruff check .` が成功する。
- [ ] `uv --cache-dir .uv_cache run python -m ruff format --check .` が成功する。
- [ ] `uv --cache-dir .uv_cache run python -m ty check` が成功する。
- [ ] 共有基盤、config、runtime、Screen、Sniffer を変更した場合は全 pytest が成功する。
- [ ] 公開 API と設計判断を変えた場合は Design と、必要なら新しい ADR を更新する。
- [ ] 高レベル Screen API の振る舞いを変えた場合は、次の API へ進む前に実雀魂での手動確認をユーザーへ依頼する。
- [ ] secret、実メール、Cookie、token、実 payload、個人情報入り画像が差分にないことを確認する。

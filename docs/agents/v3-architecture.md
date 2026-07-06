# v3 アーキテクチャ草案

この文書は v3 の内部構成候補です。実装前の設計メモであり、v2 の
パッケージ構造を維持するためのものではありません。

## 方針

内部構造は、次の 3 つの価値がある場合にだけ分けます。

- テストで fake に置き換えやすい
- Playwright / mitmproxy など実装差し替えの価値がある
- 起動、停止、異常終了、後始末の lifecycle を明確にできる

それ以外の層は作りません。

## 候補パッケージ構成

```text
src/majsoulrpa/
  __init__.py
  app.py
  config.py
  errors.py
  browser/
    __init__.py
    runner.py
    server.py
    playwright.py
    zmq.py
  client/
    __init__.py
    runtime.py
    dispatch.py
  screens/
    __init__.py
    base.py
    login.py
    home.py
    room.py
    tournament.py
  sniffer/
    __init__.py
    hook.py
    metadata.py
    playwright.py
    mitmproxy.py
  yostar/
    __init__.py
    code_provider.py
    s3_code_provider.py
  testing/
    __init__.py
    fake_browser.py
    fake_capture.py
    fake_screen.py
```

これは初期候補です。実装開始時に、不要な package は作りません。

## 依存方向

依存方向は単純に保ちます。

```text
RPAApp
  -> client runtime
      -> screen detection
      -> callback dispatch
      -> browser client
      -> sniffer event stream

browser host
  -> Playwright runtime
  -> sniffer backend

screens
  -> screen context
  -> browser operations
  -> sniffer queue when needed
```

`screens` は `RPAApp` に依存しません。`sniffer` は `screens` の具体 class に
依存しません。`yostar` は core runtime から独立させ、ユーザー callback から
使う optional integration にします。

## `app.py`

`RPAApp` を置きます。

責務:

- callback registry
- 重複登録の検出
- `run()` の public entrypoint
- data の受け渡し

持たせない責務:

- Playwright の詳細
- WebSocket decode
- Yostar login
- 画面ごとの操作

## `client/runtime.py`

client runtime は、登録済み screen の検出と callback 実行を担当します。

責務:

- 登録済み screen の一覧を受け取る
- screen detection を実行する
- 優先順位に従って 1 つの screen を選ぶ
- callback を実行する
- timeout と cancellation を扱う
- stop 要求を処理する

設計上の未決定:

- screen priority を class 属性にするか、登録順にするか
- detection loop の tick 間隔を config に出すか
- screen detection の失敗を即例外にするか、次候補へ進むか

初期案:

- priority は登録順とする
- tick 間隔は public config に出さず、timeout と待機 API で制御する
- detection の例外は失敗として隠さず、runtime error として伝播する

## `screens/base.py`

Screen base は、custom screen を書くための最小 surface にします。

候補:

- `ScreenContext`
- `Screen`
- `ScreenDetector`

`ScreenContext` に含める候補:

- browser 操作用 port
- screenshot 取得 API
- template match API
- sniffer queue 参照
- runtime stop 要求 API

`ScreenContext` に含めないもの:

- user data
- callback registry
- AWS / email 設定
- raw credential

## `browser/runner.py` / `browser/server.py`

browser host の起動関数と request server は browser lifecycle と
remote command の受付を担当します。

責務:

- Playwright browser の起動
- context と page の作成
- viewport、headless、user data dir の適用
- client からの操作要求の受付
- sniffer backend の開始と停止
- shutdown

browser host は「起動したふり」をしません。Playwright が起動できない場合は、
明示的に失敗させます。

## `sniffer/`

sniffer は差し替え価値があるため、狭い境界を許可します。

境界に含めるもの:

- start
- stop
- payload event の発行
- synthetic payload のテスト投入

境界に含めないもの:

- user callback dispatch
- screen 操作
- protocol 生成物の管理
- 保存先 policy

Playwright sniffer を最初に spike し、要件を満たせない場合に mitmproxy を
採用候補にします。

`SnifferConfig` は初期 config には置きません。sniffer backend の spike 後に、
ユーザーが実際に設定すべき値が明確になってから追加します。

## `testing/`

testing package は、実ブラウザや実通信なしで TDD を進めるために用意します。

候補:

- fake browser operation recorder
- fake screenshot source
- fake sniffer event stream
- fake screen
- callback dispatch helper

testing helper は public API として安定化させる必要はありません。ただし、
examples が testing helper に依存しないようにします。

## 削除前提の v2 資産

v2 の以下は削除前提です。

- 既存の `src/` 実装
- 既存の `tests/`
- 古い examples
- 古い Sphinx API docs
- 既存の screenshot template
- 既存の generated protocol files

必要になった screenshot、template、`.proto`、生成物は、その時点で目的を
明記してユーザーにコミットを依頼します。

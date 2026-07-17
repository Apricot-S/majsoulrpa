# アーキテクチャ

この文書は MajsoulRPA の現在の内部構成と依存方向を示します。パッケージ構造は、
要件、テスト容易性、ライフサイクル管理に基づいて決定します。

## 方針

内部構造は、次の 3 つの価値がある場合にだけ分けます。

- テストで fake に置き換えやすい
- Playwright / mitmproxy など実装差し替えの価値がある
- 起動、停止、異常終了、後始末の lifecycle を明確にできる

それ以外の層は作りません。

## パッケージ構成

```text
src/majsoulrpa/
  __init__.py
  app.py
  config.py
  browser/
    controller.py
    messages.py
    playwright.py
    runner.py
    server.py
    transport.py
    zmq.py
  client/
    controller_runtime.py
    runtime.py
    session.py
  presentation/
    region.py
    template.py
  screens/
    base.py
    errors.py
    login.py
    home.py
    room/
  sniffer/
    correlator.py
    decoder.py
    envelope.py
    events.py
    message_queue.py
    playwright.py
    publication.py
    runtime.py
    worker.py
    zmq.py
  yostar_email/
    email.py
    provider.py
    s3.py
```

一覧は主要な責務を示すもので、単純な補助 module と生成物は省略しています。新しい package は、
実装の差し替え、ライフサイクル管理、またはテスト容易性に明確な価値がある場合だけ追加します。

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
  -> sniffer queue when raw message consumption is needed
  -> room state view through screen context when current room state is needed
```

`screens` は `RPAApp` に依存しません。`sniffer` は `screens` の具体 class に
依存しません。`yostar_email` は core runtime から独立させ、ユーザー callback から
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

現在の方針:

- priority は登録順とする
- tick 間隔は public config に出さず、timeout と待機 API で制御する
- detection の例外は失敗として隠さず、runtime error として伝播する

## `screens/base.py`

Screen base は、custom screen を書くための最小 surface にします。

候補:

- `ScreenContext`
- `Screen`
- `ScreenDetector`

`ScreenContext` に含めるもの:

- browser controller
- screenshot 取得 API
- template match API
- sniffer queue 参照
- Sniffer message source
- room state cache
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

WebSocket frame は Playwright で capture します。browser host 内で最小 envelope decode と
Request / Response 対応検証を行ってから、pyzmq PUB/SUB で RPA client へ配信します。
具体的な protobuf 本文は client 側で decode します。詳細は
[WebSocket Sniffer 設計](network/sniffer.md) を参照してください。

## テスト構成

テスト用 fake と synthetic data は `tests/` に置き、実ブラウザや実通信なしで各境界を
検証します。

候補:

- fake browser operation recorder
- fake screenshot source
- fake sniffer event stream
- fake screen
- callback dispatch helper

テスト helper は公開 API として安定化させません。examples もテスト helper に
依存させません。

## 外部由来の資産

以下の資産は必要性と安全性を確認してから追加または更新します。

- screenshot template
- `.proto` ファイル
- generated protocol files

必要になった screenshot、template、`.proto`、生成物は、その時点で目的を明記し、
ユーザーにコミットを依頼します。

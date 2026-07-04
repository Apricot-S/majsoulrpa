# API 設計方針

## 基本方針

v3 は v2 の API 名や互換性を維持しません。ただし、v2 の README と examples
にある利用感は尊重します。公開 API はユーザーの作業量を減らし、
カスタマイズしたいユーザーには明確な差し込み口を提供します。

## v2 から拾う利用感

v2 の公開利用例では、以下が中心でした。

- browser host を CLI で起動する
- Python から browser host を起動する
- `RPAClient` 相当の object に Presentation ごとの callback を登録する
- callback は async 関数
- callback の引数には Presentation と任意の state/data が渡る
- callback の戻り値が次の state/data になる
- 登録されていない Presentation は検出対象外
- `detection_timeout` 相当の時間制限を指定できる
- Presentation を継承して画面処理を差し替えられる
- Sniffer 相当の hook で通信を保存できる

## 目標とする API の感触

以下は設計の雰囲気を示す例であり、確定 API ではありません。

```python
app = RPAApp()


@app.on(LoginScreen)
async def handle_login(screen: LoginScreen, state: State) -> State:
    await screen.enter_email_address(state.email_address)
    code = await state.code_provider.fetch()
    await screen.enter_verification_code(code)
    return state


@app.on(HomeScreen)
async def handle_home(screen: HomeScreen, state: State) -> State:
    await screen.close_notifications()
    await screen.stop(close_browser=True)
    return state


result = await app.run(config, state, detection_timeout=60)
```

守りたい点:

- callback 登録は読みやすく、通常ユーザーはこれだけで使える
- ユーザー state はフレームワークが解釈しない
- Presentation の API は async に統一する
- timeout は呼び出し側が読める位置で指定できる
- 失敗時は明示的な例外として表す

## API を増やす基準

高レベル API は、次の条件を満たす場合に追加します。

- 合意済み友人戦・大会の利用に必要である
- 画面操作の手順をユーザーに毎回書かせるより安全である
- fake driver / fake screen で自動テストできる
- 実際の雀魂でユーザーが手動確認できる単位に分けられる

次の場合は API を追加しません。

- 便利だが対象外用途にも使いやすい
- エラー時の状態を正しく表現できない
- 内部都合だけを公開 API に漏らしている
- private 実装を温存するためだけに必要になる

## callback と state

callback は v3 の主 API です。

- callback は Presentation class に紐づける
- 同じ Presentation への複数 callback を許すかは、設計時に明示する
- callback の戻り値を次の state として扱う
- state の型はユーザーが決める
- フレームワークは state を保存、serialize、log しない

## Presentation

Presentation は「現在の画面で安全に実行できる操作」を表します。

Presentation に含めるもの:

- 画面検出に必要な条件
- その画面で意味を持つ操作
- 操作前後の待機や確認
- 画面固有の例外

Presentation に含めないもの:

- browser host の起動設定
- 通信キャプチャ backend の詳細
- ユーザーの業務ロジック
- 対象外用途を可能にする導線

## 設定 API

設定は Python object と TOML の両方から扱えるようにします。

方針:

- default は安全で明示的にする
- secret は repr/log に出さない
- どの optional dependency が必要か分かるエラーにする
- browser host と client を分離できる形にする
- 一体構成も簡単に書ける形にする

## エラー設計

エラーは原因が分かる形で表します。

- 広い `except Exception` で握りつぶさない
- 操作失敗を成功扱いにしない
- retry は条件、回数、待機理由を明示する
- ユーザーに再入力や手動確認が必要な場合は、その状態を例外で表す
- secret や認証コードを例外 message に含めない

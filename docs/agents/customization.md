# カスタマイズ方針

## 目的

v3 は、標準の使い方を簡単にしつつ、必要なユーザーが安全に差し替えられる
場所を用意します。カスタマイズ性は、内部構造を公開することではなく、
安定した拡張点を小さく用意することで実現します。

## レベル 1: callback 登録

通常ユーザーは callback 登録だけで使えることを目標にします。

できること:

- Login、Home などの Presentation ごとに処理を書く
- 任意の state を受け渡す
- 処理ごとに timeout を設定する
- 必要な場面で RPA を終了する

このレベルでは、画面認識や通信 capture の内部を知る必要がない状態を目指します。

## レベル 2: custom Presentation

未対応画面や特殊な画面遷移には、Presentation の継承または合成で対応します。

できること:

- 標準の前処理をスキップする
- 追加の画面操作を定義する
- 別の画面検出条件を使う
- 特定の通信 message を待って操作完了とみなす

注意:

- private driver 属性に依存する設計にしない
- custom Presentation が必要とする低レベル操作は、公開された小さな API にする
- 対象外用途に直結する操作は標準 API として提供しない

## レベル 3: WebSocket capture hook

通信保存や解析の用途には、WebSocket capture の hook を用意します。

できること:

- message metadata を見る
- request / response の raw bytes を保存する
- decode した message 名で分岐する
- 保存処理をユーザー側に置く

禁止:

- 実通信 payload を tests や examples に入れる
- Cookie、token、個人情報を保存する example を置く
- 検出回避や規約違反を目的とした hook を用意する

## レベル 4: browser / runtime 差し替え

高度なユーザー向けに、browser 起動や capture backend の差し替えを検討します。

差し替えを許す候補:

- headless / viewport / user data dir
- remote endpoint
- Playwright capture と mitmproxy capture
- test 用 fake browser

差し替えを許すか慎重に判断する候補:

- 任意 JavaScript injection
- proxy や certificate の低レベル設定
- browser fingerprint に関わる設定

## examples の方針

examples は、ユーザーが安全に真似できる範囲に限定します。

置いてよいもの:

- placeholder の config
- callback 登録の最小例
- custom Presentation の最小例
- synthetic payload を使う capture hook の例

置かないもの:

- 実メールアドレス
- AWS credential
- 実 log id
- ライブ通信 payload
- Cookie、token、session 情報

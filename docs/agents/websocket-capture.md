# WebSocket キャプチャ方針

## 要件

v3 では、examples の牌譜バイナリ保存のように、ユーザーが通信 message を
観測して保存処理を差し込めることを目標にします。

必要な性質:

- Mahjong Soul の WebSocket frame を観測できる
- raw bytes を必要に応じてユーザー処理へ渡せる
- raw payload をデバッグ用ログへ出せる
- message 名などの metadata で分岐できる
- request / response の対応付けを扱える
- browser host と client を分離した構成でも使える
- 自動テストでは synthetic frame だけで検証できる

## HTTP response との境界

WebSocket Sniffer は、継続的な frame 観測とユーザー hook を責務とする。画面操作の
成否確認に使う、一度限りの HTTP response 待機は責務に含めない。

特に Yostar 認証 response は token やメールアドレスを含み、raw payload を hook や
RPA client へ渡す必要がない。ログインボタンの click と response 待機を browser host の
request-scoped な操作として実行し、secret を除いた結果だけを返す。これを理由に Sniffer を
HTTP 全般へ拡張したり、汎用 HTTP capture hook を公開したりしない。

将来、認証以外に複数の HTTP 観測用途が現れた場合は、共通部分が確認できた時点で
`NetworkObserver` のような上位概念を改めて検討する。今回だけを根拠に先行抽象化しない。

## Playwright 案

利点:

- 依存関係と起動プロセスが少ない
- browser lifecycle と同じ場所で管理しやすい
- proxy certificate の導入が不要
- ローカル一体構成を簡単にできる

懸念:

- raw binary frame と request / response 対応付けの扱いを実証する必要がある
- ユーザー addon を独立プロセスとして動かす用途には向かない可能性がある
- Playwright の event API で足りない場合、内部実装に寄りすぎる恐れがある

## mitmproxy 案

利点:

- WebSocket の観測と保存に向いた独立した capture 層を作りやすい
- browser 以外の通信も proxy 経由で一貫して扱える
- ユーザー addon のモデルが作りやすい
- v2 の牌譜保存 example に近い体験を維持しやすい

懸念:

- 依存関係と起動プロセスが増える
- proxy 設定と certificate 周りの運用が重い
- lifecycle 管理が複雑になる
- platform 差の検証が必要になる

## 初期方針

最初に Playwright capture の spike を行います。Playwright で要件を満たせるなら、
v3 の初期実装は Playwright を優先します。

ただし、capture は置換価値が明確な領域です。Playwright と mitmproxy を
比較する間だけ、狭い capture backend 境界を設けることは許容します。
この境界は、以下だけを責務にします。

- capture の開始と停止
- synthetic test frame の投入
- 観測した message を hook へ渡す
- cleanup と異常終了の扱い

decode、保存、ユーザー callback dispatch まで backend interface に入れません。

## spike の判定基準

Playwright 案は、次を満たせる場合に採用候補とします。

- binary frame を欠落なく取得できる
- message 名を取り出すための decode に必要な bytes を取得できる
- request / response の対応付けが実用上十分に扱える
- browser host の lifecycle と一緒に停止できる
- fake capture で自動テストできる

満たせない場合は、mitmproxy 案を採用候補にします。

## テスト方針

自動テスト:

- synthetic binary frame を使う
- fake capture backend を使う
- 実サーバー、実雀魂、実 proxy、実 certificate を使わない
- 実 payload を fixture にしない
- raw payload ログのテストには synthetic payload だけを使う

手動確認:

- 実通信確認が必要になったら、保存場所と削除方針を明示する
- 取得した payload はログに出してよいが、コミットしない
- 必要な `.proto` や生成物はユーザーにコミットを依頼する

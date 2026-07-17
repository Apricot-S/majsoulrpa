# 安全性と秘密情報

## 利用範囲

MajsoulRPA は、合意済みの友人戦・大会での利用を対象にします。

実装しないもの:

- オープン対局への自動参加
- 段位戦への自動参加
- 未合意の対局への参加
- 規約違反や検出回避を主目的とする機能

## コミットしてはいけないもの

以下は、テスト、フィクスチャ、ログ、サンプル、ドキュメント、コミットの
どこにも含めません。

- AWS credential
- メールアドレス
- 認証コード
- Cookie
- アクセストークン
- session 情報
- 実際のメール本文
- ライブネットワークキャプチャ
- 実アカウントや個人情報が写ったスクリーンショット

## サンプル値

サンプルでは placeholder だけを使います。

例:

```toml
email-address = "user@example.com"
bucket-name = "example-bucket"
key-prefix = "example-prefix/"
```

`.invalid` や `example-*` 以外の、実在しそうな値は避けます。

## ログ

ログに出してよいもの:

- component 名
- 操作名
- timeout 秒数
- synthetic test id
- secret を含まない設定値
- デバッグ用の raw WebSocket payload

ログに出してはいけないもの:

- メールアドレス
- 認証コード
- Cookie
- token
- 実メール本文

ただし Sniffer ログは、fork 元から引き継いだ API 調査用途のため例外とする。
decode 済み message は raw payload bytes を除き、認証情報を含む内容を
Screen 側で選んだ level のログへ出してよい。このログをコミット、fixture、
サンプル、ドキュメントへ転記してはいけない。

## WebSocket payload

raw WebSocket payload は、デバッグ用ログへ出してよいものとします。
加工済みの要約だけでは原因調査が難しいため、ユーザーが必要に応じて raw
payload を確認できる状態を優先します。

ただし、実通信 payload はコミットしない、fixture にしない、ドキュメントに
貼らないことを原則にします。

手動確認で一時保存が必要な場合:

- 保存先を明示する
- コミット禁止を明示する
- 確認後の削除を明示する
- payload の内容をチャットや docs に貼らない

## 画像と protocol 資産

スクリーンショット画像や `.proto` ファイルが必要になった場合は、
ユーザーにコミットを依頼します。

エージェントは、実ゲーム由来の画像や protocol 生成物を独断で追加しません。

## エラー表示

例外 message、CLI 出力、ログには秘密情報を含めません。

悪い例:

```text
Failed to login user@example.com with code 123456
```

よい例:

```text
Failed to complete Yostar login before timeout.
```

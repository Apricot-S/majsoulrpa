# AGENTS.md

MajsoulRPA は、合意済みの友人戦・大会で利用する RPA フレームワークです。
公開 API の使いやすさ、安全性、テスト容易性を優先し、内部構造は明確な設計理由が
ある場合にだけ抽象化します。

このリポジトリで作業するエージェントは、まず以下の資料を確認してください。

- [ドキュメント索引](docs/README.md)
- [プロジェクト方針](docs/project/charter.md)
- [安全性と秘密情報](docs/project/safety.md)
- [開発ロードマップ](docs/development/roadmap.md)
- [テスト計画](docs/development/test-plan.md)
- [テストと品質基準](docs/development/testing.md)
- [アーキテクチャ](docs/design/architecture.md)
- [API 設計方針](docs/design/api-guidelines.md)
- [公開 API 設計](docs/design/public-api.md)
- [内部設計方針](docs/design/internals.md)
- [カスタマイズ方針](docs/design/customization.md)
- [WebSocket キャプチャ方針](docs/design/network/websocket-capture.md)
- [WebSocket Sniffer 設計](docs/design/network/sniffer.md)
- [RoomScreen 設計](docs/design/screens/room.md)
- [ADR 一覧](docs/adr/README.md)

## Python 実行環境

このリポジトリの Python コマンドは `uv` 経由で実行します。セッションごとに
`python` の場所や Codex の bundled runtime を探索しません。managed sandbox で
ユーザー共通の uv cache にアクセスできない場合があるため、リポジトリ内の
`.uv_cache` を明示します。

```console
uv --cache-dir .uv_cache run python -m pytest
uv --cache-dir .uv_cache run python -m ruff check .
uv --cache-dir .uv_cache run python -m ruff format --check .
uv --cache-dir .uv_cache run python -m ty check
```

対象を絞る場合も、同じ prefix の後ろに pytest の path や option を指定します。
managed sandbox の実行権限で失敗した場合は、この uv command の実行承認を求め、
別の Python runtime を探すフォールバックは行いません。

## 最重要ルール

- 合意済みの友人戦・大会での利用のみを対象にします。
- オープン対局、段位戦、未合意の対局への参加を可能にする機能は追加しません。
- 認証情報、Cookie、アクセストークン、実メール、AWS credential を、
  テスト、フィクスチャ、サンプル、ドキュメント、コミットに含めません。
  通常のログにも含めません。
- Sniffer ログだけは API 調査のための例外です。decode 済み message は raw
  payload bytes を除き、認証情報を含めて Screen 側で選んだ level のログへ
  出してよいものとします。
- raw WebSocket payload はデバッグ用ログへ出してよいですが、
  テスト、フィクスチャ、サンプル、ドキュメント、コミットには含めません。
- スクリーンショット画像や `.proto` ファイルが必要になった場合は、ユーザーに
  コミットを依頼します。
- t_wada の TDD 手順に従います。まずテストリストを作り、ひとつずつ
  テストを書いて実装し、実装とテストをリファクタリングします。テストリストの
  構造化と、役目を終えた三角測量などのテストの整理までを完了工程に含めます。
  詳細は [テストと品質基準](docs/development/testing.md) に従います。
- 高レベル API は一度に複数実装しません。1 つ実装するごとに、
  ユーザーへ実際の雀魂での確認を依頼します。
- 例外を広範囲に握りつぶしたり、一見成功したように見せる
  フォールバック処理を導入しません。

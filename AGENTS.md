# AGENTS.md

MajsoulRPA v3 は、v2 の README と examples にある利用感を出発点にしつつ、
内部設計と実装を一から作り直すブランチです。既存のプライベートな実装構造は、
単に存在しているという理由では維持しません。

このリポジトリで作業するエージェントは、まず以下の資料を確認してください。

- [v3 の方針](docs/agents/v3-charter.md)
- [開発計画](docs/agents/development-plan.md)
- [API 設計方針](docs/agents/api-guidelines.md)
- [公開 API 草案](docs/agents/public-api-draft.md)
- [内部設計方針](docs/agents/internal-design.md)
- [v3 アーキテクチャ草案](docs/agents/v3-architecture.md)
- [カスタマイズ方針](docs/agents/customization.md)
- [WebSocket キャプチャ方針](docs/agents/websocket-capture.md)
- [WebSocket Sniffer 設計](docs/agents/sniffer-design.md)
- [RoomScreen 設計](docs/agents/room-screen-design.md)
- [テストと品質基準](docs/agents/testing-quality.md)
- [初回テストリスト](docs/agents/initial-test-list.md)
- [安全性と秘密情報](docs/agents/safety-secrets.md)

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
- raw WebSocket payload は v2 同様デバッグ用ログへ出してよいですが、
  テスト、フィクスチャ、サンプル、ドキュメント、コミットには含めません。
- v2 のコードや資産は一度削除する前提です。スクリーンショット画像や
  `.proto` ファイルが必要になった場合は、ユーザーにコミットを依頼します。
- t_wada の TDD 手順に従います。まずテストリストを作り、ひとつずつ
  テストを書いて実装し、必要に応じてリファクタリングします。
- 高レベル API は一度に複数実装しません。1 つ実装するごとに、
  ユーザーへ実際の雀魂での確認を依頼します。
- 例外を広範囲に握りつぶしたり、一見成功したように見せる
  フォールバック処理を導入しません。

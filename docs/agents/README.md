# docs/agents

このディレクトリは、MajsoulRPA の設計と開発に関する作業資料を置く場所です。
`AGENTS.md` は概要だけに留め、詳細な判断基準や開発順序はここに分けます。

## 資料一覧

- [プロジェクト方針](project-charter.md)
- [開発計画](development-plan.md)
- [API 設計方針](api-guidelines.md)
- [公開 API 草案](public-api-draft.md)
- [内部設計方針](internal-design.md)
- [アーキテクチャ草案](architecture.md)
- [テンプレート照合設計メモ](template-matching.md)
- [カスタマイズ方針](customization.md)
- [WebSocket キャプチャ方針](websocket-capture.md)
- [WebSocket Sniffer 設計](sniffer-design.md)
- [RoomScreen 設計](room-screen-design.md)
- [テストと品質基準](testing-quality.md)
- [初回テストリスト](initial-test-list.md)
- [安全性と秘密情報](safety-secrets.md)

## 読み方

実装作業に入る前に、少なくとも [プロジェクト方針](project-charter.md)、
[開発計画](development-plan.md)、[テストと品質基準](testing-quality.md)、
[安全性と秘密情報](safety-secrets.md) を確認してください。

API や内部構造を変更する作業では、[API 設計方針](api-guidelines.md) と
[公開 API 草案](public-api-draft.md)、[内部設計方針](internal-design.md)、
[アーキテクチャ草案](architecture.md) も確認してください。

画面到達判定や固定領域クリックを扱う作業では、
[テンプレート照合設計メモ](template-matching.md) も確認してください。

WebSocket capture、通信依存の画面状態、Sniffer hook を扱う作業では、
[WebSocket キャプチャ方針](websocket-capture.md) と
[WebSocket Sniffer 設計](sniffer-design.md) も確認してください。

友人戦待機部屋の状態や操作を扱う作業では、[RoomScreen 設計](room-screen-design.md) も
確認してください。

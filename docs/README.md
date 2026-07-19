# MajsoulRPA documentation

このディレクトリには、現在有効な設計、設計判断の履歴、開発工程、プロジェクト方針、
調査記録を役割別に置きます。コーディングエージェント向けの必須手順は
[`AGENTS.md`](../AGENTS.md) を入口とし、詳細はこの索引から参照します。

## Project

- [プロジェクト方針](project/charter.md)
- [安全性と秘密情報](project/safety.md)

## Design

- [アーキテクチャ](design/architecture.md)
- [API 設計方針](design/api-guidelines.md)
- [公開 API 設計](design/public-api.md)
- [内部設計方針](design/internals.md)
- [カスタマイズ方針](design/customization.md)
- [テンプレート照合](design/screens/template-matching.md)
- [ログイン認証フロー](design/screens/login-verification.md)
- [RoomScreen](design/screens/room.md)
- [MatchScreen](design/screens/match.md)
- [WebSocket キャプチャ方針](design/network/websocket-capture.md)
- [WebSocket Sniffer](design/network/sniffer.md)

## Architecture Decision Records

- [ADR の運用方法と一覧](adr/README.md)

ADR は採用済みの判断とその理由を固定します。現在の仕様を知る場合は Design を読み、
なぜその設計になったかを確認する場合は ADR を参照します。

## Development

- [開発ロードマップ](development/roadmap.md)
- [テスト計画](development/test-plan.md)
- [テストと品質基準](development/testing.md)

## Investigations

- [Yostar 認証通信の調査](investigations/yostar-auth.md)
- [抽象化・レイヤー構成レビュー（2026-07-13）](investigations/abstraction-review-2026-07-13.md)

調査記録は特定時点の観測結果です。現行仕様と競合する場合は、Design と ADR を優先します。

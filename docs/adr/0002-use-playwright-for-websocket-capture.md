# ADR-0002: WebSocket captureにPlaywrightを使用する

- Status: Accepted
- Date: 2026-07-18

## Context

WebSocket frame の観測には、browser lifecycle と統合できる Playwright と、独立した
proxy 層を作れる mitmproxy が候補になった。mitmproxy は保存用 addon を構成しやすい一方、
proxy、certificate、追加 process の運用と cleanup が必要になる。

## Decision

標準 browser host の WebSocket capture backend には Playwright を使用する。page の
`websocket` event と frame event を利用し、decode や publish を callback 内で実行せず、
bounded queue と worker へ渡す。mitmproxy backend は具体的な要件が生じるまで実装しない。

## Consequences

- browser と capture の起動・停止を同じ lifecycle で管理できる。
- ローカルCA証明書とproxy processが不要になる。
- frame callback をブロックせず、queue overflow を致命的エラーとして扱う必要がある。
- Playwright で満たせない capture 要件が確認された場合は、新しい ADR で backend を再検討する。

詳細は [WebSocket キャプチャ方針](../design/network/websocket-capture.md) を参照する。

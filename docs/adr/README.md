# Architecture Decision Records

このディレクトリには、複数の component や公開 API に影響する設計判断を記録します。
現在の仕様は [`docs/design/`](../design/) に置き、ADR はその仕様を選んだ理由と変更履歴を
固定します。

## 運用

- ファイル名は `NNNN-short-title.md` とする。
- Status は `Proposed`、`Accepted`、`Deprecated`、`Superseded` のいずれかとする。
- Accepted ADR の本文は判断当時の記録として変更せず、誤記とリンク切れだけを修正する。
- 判断を変更するときは新しい ADR を作り、旧 ADR を `Superseded by ADR-NNNN` とする。
- 局所的な実装詳細や、選択肢のない通常作業は ADR にしない。

## 一覧

- [ADR-0001: Screen操作の期限を呼び出し側で管理する](0001-caller-managed-screen-timeouts.md)
- [ADR-0002: WebSocket captureにPlaywrightを使用する](0002-use-playwright-for-websocket-capture.md)
- [ADR-0003: Sniffer decodeをbrowser hostとclientに分割する](0003-split-sniffer-decoding.md)
- [ADR-0004: Room状態をmessage sourceと共有cacheで管理する](0004-room-state-message-source-and-cache.md)
- [ADR-0005: Yostar認証応答をrequest-scoped browser commandで待つ](0005-request-scoped-yostar-auth-wait.md)
- [ADR-0006: MatchScreenを局遷移では維持しaction reducerを共有する](0006-match-screen-lifecycle-and-reducer.md)
- [ADR-0007: Room状態をcallback invocation内で管理する](0007-room-state-lifecycle.md)

## テンプレート

```markdown
# ADR-NNNN: タイトル

- Status: Proposed
- Date: YYYY-MM-DD

## Context

判断が必要になった背景と制約。

## Decision

採用する方針。

## Consequences

得られる利点、受け入れる制約、今後必要になる作業。
```

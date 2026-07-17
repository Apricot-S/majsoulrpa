# ADR-0001: Screen操作の期限を呼び出し側で管理する

- Status: Accepted
- Date: 2026-07-18

## Context

非同期の高レベル Screen API には、操作ごとの期限が必要になる。一方、各 API に
`timeout` 引数を追加すると、複数の内部待機を含む操作で期限の意味が曖昧になり、
cancellation と個別 timeout の変換規則も API ごとに増える。

## Decision

高レベル Screen API は `timeout` 引数を持たない。利用者は API 呼び出し全体を
`asyncio.timeout()` で囲み、structured cancellation によって期限を管理する。
framework 全体の画面検出期限は `RPAApp.run(..., detection_timeout=...)` という別の
runtime policy として扱う。

## Consequences

- API 全体に1つの期限を適用できる。
- Screen 実装は cancellation を握りつぶさず伝播しなければならない。
- timeout を通常完了、server rejection、自動 retry の契機として扱わない。
- 利用者は期限が必要な呼び出しを明示的に `asyncio.timeout()` で囲む。

詳細は [API 設計方針](../design/api-guidelines.md) を参照する。

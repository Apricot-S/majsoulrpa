# ADR-0004: Room状態をmessage sourceと共有cacheで管理する

- Status: Superseded by ADR-0007
- Date: 2026-07-18

## Context

RoomScreen はroom messageから状態を更新する必要がある。decode直後の常駐observer、専用thread、
Screenごとのbackground taskを追加する案は、既存のbounded message queueと二重の状態管理を生み、
callbackが逐次実行される現在のruntimeには過剰である。一方、Screen instanceはcallback loopごとに
作り直されるため、instanceだけにsnapshotを持たせることもできない。

## Decision

RoomScreen は既存の `SnifferMessageSource` を到着順に読み、room messageを処理する。
Screen instance間で必要な最新immutable snapshotとroom generationだけを、`ScreenContext`から
共有される具体的な `RoomStateCache` に保持する。Room専用の常駐observerやbackground taskは
追加しない。

## Consequences

- room状態更新と操作responseの相関を同じmessage順序で扱える。
- callback/APIの先頭で蓄積済みmessageをdrainし、必要な操作は後続messageを待つ必要がある。
- cacheはraw message履歴、waiter、operation responseを保持しない。
- queue overflowやstream gapでは状態を推測せずruntimeを失敗させる。

詳細は [RoomScreen 設計](../design/screens/room.md) を参照する。

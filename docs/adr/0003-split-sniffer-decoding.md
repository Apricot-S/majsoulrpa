# ADR-0003: Sniffer decodeをbrowser hostとclientに分割する

- Status: Accepted
- Date: 2026-07-18

## Context

Mahjong Soul の Response は API 名を持たず、対応する Request から具体型を決める必要がある。
すべてをclientで処理すると、PUB/SUB配送欠落とwire protocol不整合を区別できない。
すべてをbrowser hostでdecodeすると、Screenとuser hookから離れたhostへdomain知識が集中する。

## Decision

browser host は最小 envelope decode と Request / Response 対応検証を行い、対応済みの raw event を
publish する。RPA client は publication schema と sequence を検証し、具体的な protobuf 本文を
decode する。

## Consequences

- Req/Res不整合をPUB/SUB欠落と区別できる。
- client途中参加でunmatched Responseという偽のprotocol errorを作らない。
- browser hostとclientの両方がenvelope/publication schemaを理解する必要がある。
- host側のdomain知識はcorrelationに必要な範囲に限定される。

詳細は [WebSocket Sniffer 設計](../design/network/sniffer.md) を参照する。

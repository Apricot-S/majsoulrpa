# ADR-0007: Room状態をcallback invocation内で管理する

- Status: Accepted
- Date: 2026-07-20

## Context

ADR-0004 では、`RoomScreen` の callback が active な部屋に滞在したまま return することを許容し、
次の callback loop で生成される新しい Screen instance へ最新 snapshot を引き継ぐため、
`ScreenContext` 共有の `RoomStateCache` を採用した。

しかし、状態を持つ Screen は、callback が return した後に新しい instance を現在の authoritative な
情報だけから初期化できる場合に限って再検出をサポートすべきである。`LoginScreen` は認証操作の
途中、`MatchScreen` は active な対局中に callback の早期 return をサポートしない。雀魂の友人戦
では Room 内で browser を reload または再起動すると host、guest ともに退出する。対局終了後に
友人戦へ戻る場合は `.lq.Lobby.fetchRoom` response が authoritative な完全 snapshot になるが、
active な Room callback の早期 return ではこの response は発生しない。`createRoom` / `joinRoom`
response を消費した後の差分 notice だけでは、新しい RoomScreen instance を正しく初期化できない。

## Decision

`RoomScreen` の callback 利用者は、room が active な間、同じ callback invocation と Screen
instance を維持する。`get_state()`、非 terminal な `wait_for_state_change()`、`add_ai()`、
`set_ready()` の後に callback を return してはならない。`LEFT`、`KICKED`、`MATCH_STARTED`、
RPA 停止、または失敗によって現在の RoomScreen を終了するときに return する。

room state は `RoomScreen` instance が所有する具体的な store で管理する。`ScreenContext` 共有の
`RoomStateCache` と room generation は廃止する。Room 専用の decode 直後 observer、background
task、raw message 履歴は追加せず、同じ instance が既存の `SnifferMessageSource` を到着順に
読み続ける。

Room 滞在中の browser reload / restart は recovery 境界として扱わない。新しい RoomScreen を
初期化する完全 snapshot は、Home からの新規入室では `createRoom` / `joinRoom` response、対局終了後に
同じ友人戦へ戻る場合は `fetchRoom` response から得る。active 中の早期 return を runtime hook で
検出する仕組みは、必要性が確認されるまで追加せず、callback の利用契約として明記する。

## Consequences

- Room、Login、Match は、再初期化できない途中状態を callback 間で暗黙に補完しない。
- Home のように現在の画面から新しい instance を完全に初期化できる Screen は、同じ画面で
  callback が return してもよい。
- Room callback は host 交代、ready 更新、kick、外部 host による対局開始を同じ instance で待つ
  必要がある。
- 対局終了後は `fetchRoom` の完全 snapshot から、新しい RoomScreen instance と store を初期化する。
- `ScreenContext` と runtime から Room 固有 cache 依存を除去できる。
- active な Room で誤って早期 return した後に同じ画面が再検出された場合、完全 snapshot が
  なければ初期化失敗を明示し、過去の state や差分 message から成功を推測しない。
- terminal snapshot は、待機中の API へ最後の遷移を返すために現在の instance 内だけで保持する。

この ADR は [ADR-0004](0004-room-state-message-source-and-cache.md) を置き換える。

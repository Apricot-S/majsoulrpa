# MatchScreen 設計

## 目的と範囲

`MatchScreen` は、合意済みの友人戦・大会の対局画面を検出し、試合全体と現在局の状態を
decoded WebSocket message から管理する `Screen` である。

この文書では、対局開始時および途中復帰時の初期化、局をまたぐ状態遷移、callback の
ライフサイクル、再同期の共通化方針を定める。打牌、副露、和了などの個別操作 API と
結果画面の UI 操作は、対応する段階で別途詳細化する。

`references/match/` の v1-develop 実装は message の種類、action の意味、実通信で起こり得る
順序差を知るために参照する。mutable state、局ごとの Presentation 再生成、同期処理の分岐、
private API はそのまま移植しない。

## 結論

- reload / 再ログインを挟まない間は、局をまたいで 1 つの `MatchScreen` instance と 1 回の
  callback invocation を維持する。
- `ActionNewRound` では current round snapshot を置き換え、`MatchScreen` を stale にしない。
- live action と restore action は別 decoder adapter で正規化し、同じ reducer へ渡す。
- 新規開始と途中復帰は同じ bootstrapper で初期化し、public な `restore` flag は設けない。
- 対局中の `syncGame` も同じ replay 処理で現在の instance を再同期する。
- state は immutable snapshot とし、`MatchScreen` instance 内の具体的 store に保持する。
- Match 専用 background task、decode 直後の observer、共有 Match cache は追加しない。
- Match 中も generic `Screen.reload()` を使い、成功後は callback を直ちに return する。
- reload / 再ログイン後は新しい `MatchScreen` instance を途中復帰と同じ bootstrap で復元する。

この判断は
[ADR-0006: MatchScreenを局遷移では維持しaction reducerを共有する](../../adr/0006-match-screen-lifecycle-and-reducer.md)
に記録する。

## callback のライフサイクル

v1-develop は局終了後の `ActionNewRound` ごとに Match 相当 object を作り直し、user callback へ
制御を戻していた。現在の `MatchScreen` はこの境界を採用しない。

```text
MatchScreen を画像検出
  -> before_callback() で bootstrap
  -> user callback を 1 回開始
       -> state を読む / 次の state change を待つ / 操作する
       -> ActionNewRound: 同じ MatchScreen 内で round を交換
       -> syncGame: 同じ MatchScreen 内で state を再構築
       -> reload: stale になった後、callback から直ちに return
       -> match terminal: 結果処理後に stale
  -> callback が return
  -> runtime が次の Screen を検出
```

callback 利用者は試合が active の間、callback 内の loop を継続する。active 中の早期 return を
framework が試合終了として補完しない。早期 return を検出する runtime hook は必要性が確認される
まで追加せず、Match callback の利用契約として明記する。ただし、明示的な `reload()` は recovery
境界である。呼び出し後は同じ Screen を使わず、user data を return して runtime の Screen 検出へ
制御を戻す。

## 状態の所有

### immutable snapshot

公開状態は immutable な `MatchState` とし、少なくとも次の単位を区別する。

- match identity と status
- self seat と player metadata
- 同じ Screen instance 内で単調増加する version
- current round を識別する round generation
- current round の immutable `RoundState`
- 現在選択できる operation の immutable 表現

`ActionNewRound` では match identity と player metadata を維持し、round generation を増やして
新しい `RoundState` を設定する。局の step は局ごとに 0 から始め、instance の version とは
分ける。state の collection は tuple などとし、内部 list をそのまま公開しない。

### instance-local store

`MatchStateStore` は `MatchScreen` instance が所有し、normalized action を immutable snapshot へ
reduce する。Room と同様に active 中は同じ callback invocation と Screen instance を維持するため、
`ScreenContext` に
共有 `MatchStateCache` は追加しない。

画面遷移を伴わない network reconnect で `syncGame` を受信した場合は、同じ store を再構築する。
`Screen.reload()` または再ログインでは現在の instance を stale にし、新しく検出した
`MatchScreen` が `syncGame` から新しい store を構築する。以前の instance の state は引き継がず、
callback 間で維持したい利用者側の情報だけを callback の user data で渡す。

store は raw message 履歴を保持しない。restore replay の過去 action は state 構築に使うが、
callback に新着 event として再通知しない。reducer が返す transition を bootstrapper が破棄し、
restore 専用 reducer は作らない。

## action の正規化

Sniffer の共通 decoder は outer Liqi message の protobuf decode に留める。
`.lq.ActionPrototype.data` の復号と action message 型の decode は Match 固有 decoder が担当する。

内部 normalized action は概念的に次の情報を持つ。

```python
@dataclass(frozen=True, slots=True)
class MatchAction:
    step: int
    name: str
    data: dict[str, JsonValue]
    observed_at: datetime
```

入力 adapter は明示的に分ける。

- live adapter: `.lq.ActionPrototype` の obfuscated `data` を unmask して decode する
- restore adapter: `syncGame.response.game_restore.actions` の plain `data` を decode する

adapter の出力は同じ `MatchAction` とする。`restore: bool` を reducer や state model まで伝播
させない。未知 action 名、壊れた data、不正 step は推測せず明示的な失敗にする。

## 新規開始と途中復帰の共通 bootstrap

### 必要な情報

callback を開始するには次の情報が必要である。

1. `.lq.FastTest.authGame` 由来の match metadata、seat list、player metadata
2. current round を構築できる `ActionNewRound` から始まる action 列
3. 新規開始または途中復帰のどちらかを確定できる entry evidence

新規開始では 2 を live `.lq.ActionPrototype` から得る。途中復帰では `syncGame` の
`game_restore.actions` から得る。normalized action にした後は同じ reducer を使う。

fresh entry marker は実通信ログで確定する。v1-develop では `.lq.NotifyRoomGameStart` が候補だが、
友人戦の host / guest と tournament のすべてで一度だけ観測され、reload / 途中復帰では観測されない
ことを確認してから固定する。marker を Room / tournament 側が先に消費する場合は、Screen を stale
にして callback から戻る handoff point で、その decoded message を一度だけ `put_back()` する。
Match 側が marker を直接受信した場合と同じ bootstrap 処理を使う。

marker から派生する `MatchEntryHint` は `ScreenContext` に追加しない。hint を生成するにも同じ marker
判定が必要で、元 message の direction、時刻、match ID などの根拠を失うためである。単一の marker
を実通信で確定できない場合に限り、複数 message から導出する one-shot transition handoff を再検討
する。restore 用 `syncGame` は recovery entry evidence とし、public な `restore` flag は設けない。

### bootstrap accumulator

`before_callback()` はマウスカーソルを退避した後、内部 bootstrapper で既存の
`SnifferMessageSource` を到着順に読む。public な `restore` 引数は持たない。

bootstrapper は一時的に次を保持する。

- authGame 由来の metadata
- direct または `put_back()` された fresh entry marker 由来の candidate match ID
- metadata より先に到着した normalized action または restore action batch
- fresh / recovery の entry evidence

auth と action source の到着順は固定しない。action が先なら bounded な初期化用 buffer に保持し、
auth と entry kind が揃ってから apply する。candidate match ID がある場合は authGame の match ID
と一致することを検証する。entry kind が未確定の段階で、buffer 内の live `ActionNewRound` だけを
根拠に fresh 初期化を完了しない。以前の Room terminal state は reload 後も残り得るため、fresh
evidence として再利用しない。

```text
decoded Sniffer message
  -> bootstrap message classifier
       -> authGame --------------------> metadata decoder
       -> live ActionPrototype --------> live action adapter ---+
       -> syncGame.game_restore.actions -> restore adapter ------+-> action reducer
       -> known non-state message ------> consume / safe log
```

entry kind、metadata、active round snapshot のすべてが構築できた時点で `before_callback()` を
完了する。`finishSyncGame` だけを state 初期化条件にはしない。

| message | bootstrap での扱い |
|---|---|
| `.lq.NotifyRoomGameStart` | fresh entry marker の候補。実通信確認までは確定しない |
| `.lq.FastTest.authGame` | match metadata、self seat、players を構築する |
| `.lq.ActionPrototype` | live action 1 件へ decode する |
| `.lq.FastTest.syncGame` | recovery entry evidence と restore action batch へ decode する |
| `.lq.FastTest.finishSyncGame` | state を変更しない同期 marker とする |
| Room / tournament の既知 terminal message | entry noise として必要な範囲だけ消費する |
| heartbeat 等の既知 common message | state を変更せず安全な level でログする |
| 未知または矛盾した message | screenshot 付き不整合エラーにする |

新規開始と復帰で別々の初期化 loop を作らない。違いは action adapter と、restore batch を
historical event として callback に公開しないことだけに限定する。

recovery entry では `syncGame` の snapshot を authoritative とする。reload 前から queue に残って
いた live action や、restore 完了前に観測した live action を初期 snapshot の代用にしない。
restore 完了後は、snapshot の次 step 以降と検証できる live action だけを通常処理へ渡す。これに
より、reload 中に対局が進行していても `syncGame` 時点の current round から再開できる。

## reducer と局遷移

reducer は `MatchAction.name` ごとの純粋な状態遷移を担う。current state の再構築に必要な action を
1 種類ずつ TDD で追加する。

各局の action sequence は step 0 から始める。試合開始時だけ `ActionMJStart` が step 0 に入り、
最初の `ActionNewRound` が step 1 になる場合があるため、sequence validator がこの任意の prelude を
先に消費する。それ以外の `ActionNewRound` は step 0 とし、match metadata を維持したまま
`RoundState` と operation を構築する。current round がある場合は round generation を増やし、
同じ `MatchScreen` を active のままにする。

live action の step が観測順と異なる可能性は v1-develop の知見として残す。current round 内に
step を key とする bounded reorder buffer を置き、期待 step から連続して apply できる action だけを
reducer へ渡す。適用済み step、内容が異なる duplicate、別 round と矛盾する action は失敗にする。
欠けた step を推測したり飛ばしたりせず、呼び出し側 timeout または queue failure に委ねる。

restore batch は step 0 から current step までを検証する。先頭が `ActionMJStart` なら、その次の
step 1 の `ActionNewRound` から state を構築する。先頭が `ActionNewRound` なら step 0 から構築する。
いずれも state-bearing action は同じ reducer へ順番に replay し、response の `step`、action 数、
各 step の整合性を検証する。局終了 action だけで current round を初期化しない。

## 対局中の再同期と reload

active callback 中の `syncGame` は途中復帰と同じ restore adapter と replay 処理を使う。既存 state を
部分補正せず、同じ match identity を確認して authoritative な restored snapshot へ置き換える。
version は単調増加させ、callback と `MatchScreen` instance は維持する。

Match 固有の `reload()` override は設けず、generic `Screen.reload()` の stale 契約に従う。callback
利用者は `await screen.reload()` の直後に user data を return し、runtime の Screen 検出へ制御を
戻す。stale になった Screen で処理を継続した場合は、次の Screen API 呼び出しで失敗する。

cookie が有効なら reload 後に `LoginScreen` を経ず、同じ対局の `MatchScreen` が直接検出される。
ただし reload 中にも対局は進むため、新しい `MatchScreen.before_callback()` は fresh entry として
扱わず、`authGame` と restore 用 `syncGame` が揃うまで待つ。`syncGame` の全 action を同じ reducer
へ replay して current state を構築した後、新しい Match callback invocation を開始する。

cookie が無効、session が切断済みなどの理由で `LoginScreen` を経る場合も、ログイン完了後に
検出された `MatchScreen` が同じ recovery bootstrap を使う。したがって、直接 Match に戻る経路と
再ログイン経路で state 復元処理を分けない。

```text
Match callback
  -> await Screen.reload()
  -> current MatchScreen が stale
  -> callback が user data を return
  -> runtime が LoginScreen または MatchScreen を検出
  -> 新しい MatchScreen.before_callback()
       -> authGame + syncGame を同じ recovery bootstrap で replay
  -> 新しい Match callback invocation
```

## message source と並行性

RoomScreen と同様、常駐 Sniffer client task が decoded message を既存 bounded queue へ蓄積し、
`MatchScreen` の API が `get()` / `get_nowait()` で読む。

Match 専用 background reducer は追加しない。background task と操作 API が同じ queue を競合して
読むと response と action の相関が複雑になり、別 mailbox が必要になるためである。callback と
Match API は逐次利用を前提とし、操作と状態待機を同じ message 順序で処理する。

callback は長時間 source を読まずに停止しない。queue overflow、payload budget 超過、publication
gap、decode error は状態を推測せず runtime 全体の失敗として伝播する。

## terminal と次の Screen

実通信で確定した match terminal message により terminal snapshot へ遷移する。結果 UI の確認と
Room / tournament / Home への遷移が完了するまでは、必要な Match API を同じ instance で処理できる
よう直ちに stale にしない。

次の Screen に属する message を先読みした場合は 1 回だけ `put_back()` し、画面遷移を確認して
から stale にする。terminal 後に新しい match の auth/action を観測しても、同じ instance を
暗黙に別試合へ転用しない。

友人戦の対局終了後に `.lq.Lobby.fetchRoom` response を観測した場合は、Room へ戻るための
authoritative な完全 snapshot として 1 回だけ `put_back()` する。runtime が新しく検出した
`RoomScreen` はこの response から instance-local store を初期化する。以前の RoomScreen instance
や terminal snapshot は引き継がない。

## 整合性と失敗モデル

少なくとも次を検証する。

- authGame、syncGame、ActionPrototype の direction と Req/Res 種別
- match ID が空でなく、同じ instance 内で変化しないこと
- self account ID が seat list に一度だけ存在すること
- player 数と seat 数が 3 または 4 で一致すること
- player account ID が重複しないこと。CPU seat の表現は実通信確認後に固定すること
- restore batch が任意の `ActionMJStart` と `ActionNewRound` から current step まで連続すること
- current round の live step が欠落、重複、巻き戻りしないこと
- action data が schema と state 不変条件を満たすこと
- syncGame が active state と同じ match identity を表すこと

field 欠落、型不正、矛盾は screenshot 付き Match inconsistent message error とする。nested protobuf
decode、Sniffer transport、stream gap は元の infrastructure error を伝播する。未知 action を
無視したり、画面から state を推測したり、自動 reload で成功に見せたりしない。

## ログと秘密情報

- info log は Screen 名、API 名、action 名、step など秘密でない構造情報に限定する。
- match ID、account ID、player name、hand tiles、operation 内容を通常ログへ出さない。
- Sniffer 調査ログは既存の例外に従うが、docs、fixture、sample、chat、commit へ転記しない。
- 自動テストは synthetic decoded message、synthetic nested protobuf、fake browser だけを使う。

## TDD と実装順

1. nested action の live / restore decoder と normalized `MatchAction`。
2. match metadata と `ActionNewRound` の immutable state decode。
3. reducer と step / round generation の不変条件。
4. bootstrapper の新規開始経路。
5. 同じ bootstrapper の途中復帰経路と historical event 非通知。
6. `MatchScreen.before_callback()` への接続。
7. 同一 instance での次局 `ActionNewRound`。
8. active 中の `syncGame` 再同期。
9. generic reload 後の Screen 再検出と recovery bootstrap。
10. action と操作 API を 1 種類ずつ追加する。

各段階で synthetic data の自動テストを完了し、高レベル API は 1 つずつ実ゲーム確認する。
実 payload はテストや文書へ保存しない。

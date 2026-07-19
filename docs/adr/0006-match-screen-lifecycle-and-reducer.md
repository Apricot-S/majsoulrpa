# ADR-0006: MatchScreenを局遷移では維持しaction reducerを共有する

- Status: Accepted
- Date: 2026-07-19
- Updated: 2026-07-20

## Context

v1-develop の Match 実装は、局ごとに Match 相当 object を再生成して user callback へ制御を
戻していた。また、新規開始は live `ActionPrototype`、途中復帰は `syncGame` 内の action replay
という別々の初期化経路を持ち、同じ action に対する state 更新が重複していた。

現在は通常の局遷移を 1 回の callback invocation で処理し、state と操作の連続性を保ちたい。
一方、Match 中の reload は画面描画の復旧に必要となることがあり、cookie が残っていれば
`LoginScreen` を経ず同じ Match へ直接戻る。この間にも試合は進むため、直接復帰でも再ログインと
同様に `syncGame` から current state を復元する必要がある。live action data と restore action data
は wire encoding が異なるが、decode 後の意味は同じである。

## Decision

`MatchScreen` は `ActionNewRound` で再生成せず、reload / 再ログインを挟まない間は同じ instance と
callback invocation を維持する。match-level state を維持したまま immutable current round
snapshot を置き換える。

live action と restore action は encoding ごとの adapter で同じ public `MatchEvent` に変換し、
同じ reducer で state を更新する。新規開始と途中復帰は受信 message から判定する同じ
bootstrapper を使い、public な `restore` flag は設けない。active 中の `syncGame` も同じ replay
処理で現在 instance を再同期する。

対応対象の protobuf action 1 件を `MatchEvent` 1 件へ直接正規化し、同じ意味を持つ internal action
union は作らない。concrete event は `@final` な frozen dataclass、`MatchEvent` は全 concrete event を
列挙する public type alias とし、reducer が適用した同じ object を `RoundState.events` に保持する。
`type` discriminator は設けない。利用者は concrete event class の pattern matching で分岐し、各 case
を terminal にした後の `assert_never(event)` で union 追加時の未対応を型検査エラーにする。
runtime の field 型、範囲、tuple 要素、相互関係は dataclass の `__post_init__()` と共通 validator で
保証する。

Pydantic の判別共用体は採用しない。網羅性は Pydantic ではなく static union narrowing の性質であり、
adapter は protobuf action 名から構築すべき concrete class を既に決定できるため runtime discriminator
も不要である。JSON schema または汎用 deserialize が必要になった場合は public event model を変更せず
境界 adapter を追加する。

`ActionMJStart` も `StartMatchEvent` へ変換する。最初の `RoundState` を作るまで temporary prelude として
保持し、`NewRoundEvent` より前に `RoundState.events` へ保存する。state を変更しない event だが、
機械学習 AI は match の BOS feature として利用できる。

用語は雀魂 protobuf に合わせ、立直も `lizhi` ではなく `liqi` を canonical name とする。立直宣言は
独立 event にせず `DapaiEvent.liqi` / `wliqi` に含め、後続 action に埋め込まれた `LiQiSuccess` も
対応する event の nested field とする。雀魂の action 境界を保ち、1 action から複数 event を作らない。

state store は `MatchScreen` instance が所有する。Match 専用 background task、decode 直後の
observer、`ScreenContext` 共有 Match cache は追加しない。

restore / resync は temporary store へ historical action をすべて replay し、検証が完了してから
immutable snapshot と内部 operation state を current store へ atomic に commit する。replay 途中の
state は callback へ公開しない。historical action から再構築した event は完成した
`RoundState.events` には含めるが、新着 event として再通知しない。初期化 milestone の公開 API は
`get_state()` だけとし、状態待機と操作 API は後続で 1 つずつ追加する。

Match 固有の `reload()` override は設けない。generic `Screen.reload()` が current instance を stale
にした後、callback 利用者は user data を return して runtime の Screen 検出へ制御を戻す。直接
Match へ戻る場合も `LoginScreen` を経る場合も、新しい `MatchScreen.before_callback()` が同じ
recovery bootstrap で `authGame` と authoritative な `syncGame` を replay する。reload 前に queue
へ残った live action は restore snapshot の代用にしない。

fresh entry marker は host / guest / tournament の実通信ログで確定する。Room / tournament が marker
を先に消費する場合は、Screen 遷移直前に decoded message 自体を一度だけ `put_back()` する。
`ScreenContext` に `MatchEntryHint` は追加しない。marker がなく restore 用 `syncGame` を受信した
entry は recovery とし、以前の Room terminal state を fresh evidence として再利用しない。

## Consequences

- callback 利用者は通常の局遷移を一つの loop で連続して扱える。
- live、restore、reconnect の state 遷移を同じ reducer のテストで固定できる。
- 途中復帰直後でも current round の event 列を Mjai / Kanachan adapter が利用できる。
- restore replay の event は snapshot 履歴に含めつつ、新着 event として再通知しない制御が必要になる。
- internal action と public event の二重 model を同期させる必要がなくなる。
- event の JSON schema / 汎用 deserialize は提供せず、必要になった時点で境界 adapter を設計する。
- 網羅性には `MatchEvent` alias の更新と利用側の `assert_never()` が必要になる。
- Mjai adapter は `DapaiEvent` と後続 event の nested `LiQiSuccess` から reach event を分離する必要がある。
- restore replay の全 action を扱える reducer と、失敗時に既存 state を保つ atomic commit が必要になる。
- callback は active 中に Sniffer source を継続的に読む必要があり、reload 以外の早期 return を
  試合終了として framework が補完しない。
- reload は callback invocation の recovery 境界となり、user data 以外の callback local state は
  引き継がない。
- reload 直後に callback を return する利用契約と、直接 Match へ戻っても syncGame を待つことを
  ドキュメントとテストで固定する必要がある。
- action step の並べ替え、重複、欠落を扱う bounded buffer と明示的な不整合エラーが必要になる。

詳細は [MatchScreen 設計](../design/screens/match.md) を参照する。

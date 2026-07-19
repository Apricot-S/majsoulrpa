# ADR-0006: MatchScreenを局遷移では維持しaction reducerを共有する

- Status: Accepted
- Date: 2026-07-19

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

live action と restore action は encoding ごとの adapter で同じ normalized `MatchAction` に変換し、
同じ reducer で state を更新する。新規開始と途中復帰は受信 message から判定する同じ
bootstrapper を使い、public な `restore` flag は設けない。active 中の `syncGame` も同じ replay
処理で現在 instance を再同期する。

state store は `MatchScreen` instance が所有する。Match 専用 background task、decode 直後の
observer、`ScreenContext` 共有 Match cache は追加しない。

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
- restore replay の過去 action は state 構築には使うが、新着 event として再通知しない制御が必要になる。
- callback は active 中に Sniffer source を継続的に読む必要があり、reload 以外の早期 return を
  試合終了として framework が補完しない。
- reload は callback invocation の recovery 境界となり、user data 以外の callback local state は
  引き継がない。
- reload 直後に callback を return する利用契約と、直接 Match へ戻っても syncGame を待つことを
  ドキュメントとテストで固定する必要がある。
- action step の並べ替え、重複、欠落を扱う bounded buffer と明示的な不整合エラーが必要になる。

詳細は [MatchScreen 設計](../design/screens/match.md) を参照する。

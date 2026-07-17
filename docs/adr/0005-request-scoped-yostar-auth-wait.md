# ADR-0005: Yostar認証応答をrequest-scoped browser commandで待つ

- Status: Accepted
- Date: 2026-07-18

## Context

Yostar認証のHTTP responseはlogin clickと1対1に対応し、click前に待機を開始しなければ
取り逃がす可能性がある。responseにはtokenやメールアドレスが含まれ、継続観測用の
WebSocket SnifferやRPA clientへraw bodyを渡す必要はない。

## Decision

browser hostで `page.expect_response()` の開始、login click、response検証を1つの
request-scoped commandとして不可分に実行する。clientへはaccepted/rejectedまたは
secretを含まないbrowser errorだけを返す。汎用HTTP capture hookは追加しない。

## Consequences

- response待機開始前に応答を取り逃がすraceを避けられる。
- token、メールアドレス、raw JSONをbrowser hostの外へ出さない。
- 認証固有commandがbrowser wire protocolに含まれる。
- 他のHTTP観測用途が複数現れた場合は、共通化を新しい判断として検討する。

詳細は [ログイン認証フロー設計](../design/screens/login-verification.md) を参照する。

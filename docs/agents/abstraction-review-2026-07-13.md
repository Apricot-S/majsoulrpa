# 抽象化・レイヤー構成レビュー（2026-07-13）

## 結論

現時点で、削除すべき不要なアーキテクチャ層は見つからなかった。

一般的なライブラリより境界や `Protocol` は多いが、その大半は次のいずれかを
実際に担っている。

- 実ブラウザ、実 ZeroMQ network、実 WebSocket なしでの自動テスト
- Playwright、OpenCV、boto3 の遅延 import と optional dependency の隔離
- browser host と RPA client を分離する wire protocol
- capture、request server、subscriber など複数 resource の lifecycle 管理
- wire model、raw bytes event、decode 済み event の責務分離

したがって、browser、client、screens、sniffer、optional integration という現在の
大きな境界は維持してよい。一方、層を削除せずに単純化できる内部の重複を 2 点確認した。
どちらも機能上の問題ではなく、高レベル API 実装前後の通常のリファクタリング候補である。

## レビューの前提と方法

次の設計資料を判断基準とした。

- `v3-charter.md`
- `development-plan.md`
- `api-guidelines.md`
- `public-api-draft.md`
- `internal-design.md`
- `v3-architecture.md`
- `customization.md`
- `websocket-capture.md`
- `sniffer-design.md`
- `testing-quality.md`
- `initial-test-list.md`
- `safety-secrets.md`

手書きの `src/majsoulrpa` 実装、対応する tests、公開 export、optional dependency の
import 経路を確認した。生成物である `assets/protocol/liqi_pb2.py` は生成コードのため、
抽象化レビューの対象外とした。

抽象化は、設計資料の基準どおり、次の観点で評価した。

1. fake への差し替えによって実環境なしのテストが簡単になるか
2. 実装差し替え、wire 境界、または optional dependency の隔離に必要か
3. 起動、停止、異常終了、cleanup の責務を明確にするか
4. ユーザー向けの拡張点または安定した公開 surface か
5. 上記の価値を持たず、値や呼び出しを横流しするだけになっていないか

## 境界ごとの評価

| 境界 | 判定 | 根拠 |
|---|---|---|
| `RPAApp` / runtime factory / `RPARuntime` | 維持 | `RPAApp` は公開 callback registry、factory は実環境の組み立て、`RPARuntime` は検出・dispatch・兄弟 task・cleanup を担当する。factory 差し替えにより公開 API のテストが実 ZMQ から分離されている。 |
| browser controller / transport / wire message / executor | 維持 | controller は Screen 向け操作、transport は送受信、pydantic model は process 間 schema、executor は Playwright 操作を担当する。client/host 両側の fake と logging decorator でも同じ境界が使われている。 |
| request handler / request server | 維持 | handler は 1 request/1 response と stop command の規則、server は bind/serve/stop と socket lifecycle を担当する。純粋な request loop と ZMQ resource 管理を別々にテストできる。 |
| `ScreenContext` / Screen 基底 | 維持 | runtime 依存を Screen へ注入し、custom Screen と fake controller/template/message source を可能にしている。remote transport の具体型を Screen へ漏らしていない。 |
| ndarray matcher / PNG matcher | 維持 | `TemplateMatcher` は synthetic ndarray の照合、`PngTemplateMatcher` は runtime screenshot bytes の decode を担当する実際の adapter である。OpenCV import も presentation package root から隔離されている。 |
| Sniffer capture / envelope / correlation / publication | 維持 | 各段に queue overflow、wire decode、Req/Res 対応、schema/version/sequence という別々の不変条件と失敗がある。PUB/SUB 欠落と protocol 不整合を区別するためにも統合しない方がよい。 |
| publication / raw event / decoded event | 維持 | publication は host-client 間の base64 JSON schema、raw event は利用者向け bytes、decoded event は protobuf 本文の JSON-compatible 表現である。単なる同型 DTO の写し替えではない。 |
| Sniffer subscriber / decoder / observer / message queue | 維持 | transport、decode、session state 更新、bounded queue の失敗を個別に表し、decode 後かつ enqueue 前の session state 観測順序を固定している。 |
| `BrowserHostSnifferBackend` | 維持 | context、publisher、capture、worker の開始順と逆順 cleanup を 1 箇所で管理する composition/lifecycle boundary である。各 resource の失敗経路が fake でテストされている。 |
| Yostar code provider / S3 実装 | 維持 | provider はユーザーが認証コード取得元を選ぶ公開拡張点で、S3 は boto3 を遅延 import する optional integration である。 |
| package root の `__getattr__` lazy export | 維持 | core import で Playwright/OpenCV を読み込まないことと、不足 extra を明示することがテストで固定されている。今回の要件に直接対応する抽象化である。 |

## 改善候補 1: `RPARuntime.run()` への `config` 再受け渡しをやめる

優先度: 中。変更リスク: 低。公開 API への影響: なし。

現在は `RPAApp.run()` が `runtime_factory(callbacks, config)` で runtime を構築した後、
同じ `config` を `runtime.run(config, data, ...)` にもう一度渡している。

- [`app.py`](../../src/majsoulrpa/app.py) では factory と runtime の両方へ `config` を渡す。
- [`client/runtime.py`](../../src/majsoulrpa/client/runtime.py) の `RPARuntime.run()` は
  `config` を `_ = config` として明示的に捨てている。
- [`client/controller_runtime.py`](../../src/majsoulrpa/client/controller_runtime.py) では、
  endpoint、viewport、Sniffer subscriber など config が必要な組み立ては factory 内で
  すでに完了している。

これは設定の所有箇所を曖昧にする pass-through であり、現在確認できた中では最も明確に
不要な受け渡しである。

改善案:

```python
runtime = self._runtime_factory(self._callbacks, config)
return await runtime.run(data, detection_timeout=detection_timeout)
```

`RPARuntime.run()` から `config` 引数を削除し、config は composition root である
runtime factory だけが消費する。`RPAApp.run(config, ...)` の公開 API は変更しない。

期待できる効果:

- runtime loop の責務が callback 実行と lifecycle に限定される
- 将来、runtime 側でも config を使うように見える誤解を避けられる
- テスト用 `RPARuntime` の生成・実行が少し単純になる

## 改善候補 2: browser controller の型別 request helper を 1 つにまとめる

優先度: 低。変更リスク: 低から中。公開 API への影響: なし。

[`browser/controller.py`](../../src/majsoulrpa/browser/controller.py) には、command を送信し、
response を受信し、期待する response 型を確認するだけの private helper が command ごとに
並んでいる。`_request_click()` から `_request_click_and_wait_for_yostar_auth()` まで、
処理の骨格は同じである。

改善案:

- `send_command()` と `recv_response()` を行う型付き `_request()` を 1 つだけ置く
- public な `click()`、`screenshot()` などは現在どおり command の構築と戻り値の変換を担う
- `BrowserErrorResponse` と unexpected response の扱いは現在の `_response_error()` を維持する

Python の型注釈を成立させるためだけに複雑な generic hierarchy を作るなら逆効果である。
単一 helper で型が読みやすく保てる場合だけ実施し、そうでなければ現状維持でよい。

期待できる効果:

- command 追加時の定型 private method を減らせる
- send/receive/error handling の変更箇所を 1 箇所にできる
- controller / transport という有用な境界はそのまま残せる

## 変更しない方がよい箇所

### Sniffer pipeline を大きな service に統合しない

ファイル数だけを見ると Sniffer は細かく見えるが、各段は異なるデータ完全性を守っている。
特に envelope decode、Req/Res correlation、publication sequence、protobuf body decode、
bounded queue をまとめると、どの地点で欠落・破損したかが曖昧になり、現在の明示的な
エラー方針を弱める。

### browser の transport と controller を統合しない

controller は操作 semantics、transport は remote I/O であり、logging transport と fake
transport が実際に使われている。ここを統合すると、Screen の自動テストか remote host
分離のどちらかが具体実装へ引っ張られる。

### 局所的な ZMQ `Protocol` を共通の巨大 interface にまとめない

browser REQ/REP、Sniffer PUB/SUB、controller composition で必要な socket 操作は異なる。
似た `Protocol` が複数あっても、共通化すると不要な method を要求する横断的抽象化になる。
現在の module-local な最小 interface の方が意図に合う。

### lazy import を通常 import に戻さない

`browser`、`presentation`、`yostar_email.s3` の遅延 import は、通常の import を複雑にするための
装飾ではなく、optional dependency がない環境でも core を利用可能にする要件そのものである。

### `event_adapter.py` を「mapper だから」という理由だけで削除しない

wire publication の base64 JSON と利用者向け raw bytes event は表現と公開範囲が異なる。
変換境界自体には意味がある。将来も raw event 変換が decoder からしか使われず、ファイルを
またぐことの方が読みにくいと判断された場合は同居させてもよいが、責務は残すべきである。

## 今後の監視ポイント

- `ScreenContext` に新しい依存を追加するときは、複数の Screen が必要とする runtime 依存かを
  確認する。1 Screen 固有の helper や設定は Screen 側に置く。
- 新しい Screen 状態を追加するときは、汎用 state store を先に作らず、現在の `SessionState`
  と同様に具体的な保持要件が出てから抽象化する。
- command が増えて `browser/messages.py` の判別共用体が大きくなっても、用途別の別 protocol を
  先に作らない。互換性、権限、lifecycle が実際に分かれた時点で分割を検討する。
- Sniffer の利用者 hook を追加するときは、Screen 経由では不足する具体例を先に確認し、
  transport/backend の型を公開 surface に漏らさない。

## 検証結果

2026-07-13 に次を実行し、すべて成功した。

```text
python -m pytest                  381 passed
python -m ruff check .            passed
python -m ruff format --check .   99 files already formatted
python -m ty check                passed
```

このレビューでは実ブラウザ、実雀魂、実 network、AWS、実メールへ接続していない。

## 推奨する進め方

高レベル API の実装前に必須の構造変更はない。改善候補 1 は責務を明確にする小さな変更なので、
次の通常のリファクタリングで実施してよい。改善候補 2 は新しい browser command を追加する
直前または追加後に、重複が増えることを確認してから行えば十分である。

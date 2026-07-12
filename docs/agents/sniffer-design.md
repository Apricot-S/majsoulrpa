# WebSocket Sniffer 設計

## 目的と初期スコープ

今後、画像だけでは判断できない `Screen` の状態を WebSocket 通信から補うため、
browser host で Mahjong Soul の WebSocket frame を継続観測し、RPA client へ
配信する。

初期実装では次に限定する。

- capture backend は Playwright とする
- browser host から RPA client への配信は pyzmq の PUB/SUB とする
- binary frame を Notice、Request、Response に分類する
- Request と Response の対応を browser host 内で検証する
- protobuf 本文を具体的な message 型へ decode する処理は RPA client に置く
- 自動テストでは synthetic payload と fake socket だけを使う

HTTP response 待機、payload の永続化、`Screen` ごとの状態機械は今回の
Sniffer の責務に含めない。特に Yostar 認証の HTTP response は、従来どおり
browser command 内で待機し、Sniffer へ統合しない。

生成済み `liqi_pb2.py` は protobuf runtime 6.33.2 を要求している。実装時には
transitive dependency に頼らず、互換範囲を確認した `protobuf` を project の
直接依存へ追加する。host と client の両方が `Wrapper` を検証するため、Sniffer
だけを片側の optional dependency にしない。protocol asset の再生成は今回行わない。

## v2 実装から引き継ぐ知見

`references/sniffer/` の mitmdump addon から、次の wire format と処理順を
参考にする。

- `0x01`: Notice。続く protobuf `Wrapper` に API 名と本文がある
- `0x02`: Request。続く 2 byte の番号と `Wrapper` に API 名と本文がある
- `0x03`: Response。続く 2 byte の番号と、名前が空の `Wrapper` に本文がある
- Response の具体的な型と API 名は、対応する Request から決める
- Notice は単独で扱い、Request は Response が到着するまで保留する

v2 の class 構成や正規表現による header 抽出は維持しない。特に request
番号は 1 byte ではなく、wire format 上の 2 byte を little endian の符号なし
整数として読む。`Wrapper` は生成済み protobuf class で parse し、可変長の
field を正規表現で切り出さない。

## 全体構成

```text
Playwright Page
  -> PlaywrightFrameCapture
  -> CapturedFrame queue
  -> LiqiEnvelopeParser
  -> RequestResponseCorrelator
  -> SnifferPublication
  -> ZMQ PUB
       === tcp ===
  -> ZMQ SUB
  -> publication validation / gap detection
  -> LiqiMessageDecoder
  -> decoded event queue
  -> Screen state / user hook
```

責務は次のように分ける。

### `PlaywrightFrameCapture`（browser host）

- managed `Page` で生成された WebSocket を観測する
- `framesent` / `framereceived` を direction 付きの `CapturedFrame` にする
- WebSocket ごとに process 内だけで有効な `connection_id` を割り当てる
- frame の capture 順を表す単調増加 `frame_sequence` を付ける
- text frame を対応済みとして扱わず、明示的な unsupported frame error にする
- start / stop 時に event listener を確実に登録解除する

Playwright の callback 内では payload のコピーと bounded queue への投入だけを
行う。protobuf decode や ZMQ send で callback をブロックしない。queue overflow
は frame を黙って捨てず、Sniffer の致命的エラーにする。

### `LiqiEnvelopeParser`（browser host）

- 先頭 byte から Notice / Request / Response を分類する
- Request / Response の 2 byte の番号を読む
- protobuf `Wrapper` を parse する
- Notice / Request から API 名を得る
- Response の `Wrapper.name` が空であることを検証する
- protobuf 本文は raw bytes のまま保持する

これは Req/Res 対応付けに必要な最小限の envelope decode であり、具体的な
request / response message class への decode は行わない。空 payload、不明な
種別、壊れた `Wrapper`、不正な UTF-8 相当の問題を空 message へ変換しない。

既知の protocol heartbeat を除外する必要が確認できた場合は、synthetic data
で byte 単位の条件を固定し、`IgnoredControlFrame` として明示的に扱う。
「parse できない payload を heartbeat とみなす」fallback は置かない。

### `RequestResponseCorrelator`（browser host）

pending Request の key は次とする。

```text
(connection_id, request_direction, request_number)
```

`request_direction` まで key に含めるのは、同じ WebSocket 上で両方向から
同じ番号が使われても衝突させないためである。Response は自身と反対方向の
key だけに対応する。

- Notice はただちに `RawNotice` として出力する
- Request は pending table に保存し、単独では publish しない
- Response 到着時に反対方向の Request を取り出し、`RawRequestResponse` を出力する
- 同一 key の Request が未完了のまま再利用された場合はエラーにする
- 対応 Request のない Response はエラーにする
- Request と Response が同方向の場合は direction mismatch error にする
- WebSocket close または Sniffer stop 時に pending が残っていれば incomplete
  exchange error にする

初期実装では Request の wall-clock timeout を設けない。実通信で正当な最大応答
時間をまだ決められず、任意の timeout は偽陽性になるためである。番号の再利用、
connection close、Sniffer stop を検証境界とする。

### `ZmqSnifferPublisher`（browser host）

- `AppConfig.endpoint.client_host` と `sniffer_port` から作った endpoint に bind する
- topic と schema version を付けた publication を JSON bytes で送る
- ZMQ context / PUB socket の lifecycle を browser host と一緒に管理する
- raw bytes は JSON 内では base64 とする

### `ZmqSnifferSubscriber`（RPA client）

- `AppConfig.endpoint.browser_host` と `sniffer_port` から作った endpoint へ connect する
- Sniffer topic だけを subscribe する
- JSON schema と schema version を検証する
- `stream_id` と `publication_sequence` から再起動と欠落を検出する
- raw publication を client-side decoder へ渡す
- cancellation / runtime 終了時に SUB socket と context を閉じる

### `LiqiMessageDecoder`（RPA client）

- `liqi_pb2.DESCRIPTOR` から API 名と input / output class の対応表を作る
- Notice / Request の本文を request または Notice の具体型へ decode する
- Response の本文を、対になった Request の API 名から response 型へ decode する
- decode 結果を protobuf object そのものではなく、型の安定した domain event
  または JSON-compatible dict として上位へ渡す
- 未知 API、型対応の欠落、protobuf parse error を明示的な decode error にする

## decode を二段階にする理由

Req/Res 対応検証だけは browser host 側で行う。

1. Playwright が観測した直後なので frame の欠落が PUB/SUB の配送欠落と混ざらない
2. Response の API 名は Request を見なければ決められない
3. 対応済みの 1 publication として送れば client の処理が単純になる
4. SUB が途中参加しても unmatched Response という偽の protocol error を作らない

一方、具体的な protobuf 本文の decode は RPA client 側で行う。

1. decode 結果を使う Screen state と user hook が client 側にある
2. browser host の責務を capture、最小 envelope decode、対応検証に限定できる
3. raw bytes を残したまま、client 側で用途ごとの decode / hook を選べる
4. protocol class の追加が browser lifecycle に波及しにくい

したがって「すべて host で decode」「すべて client で decode」のどちらにも
しない。前者は browser host を肥大化させ、後者は PUB/SUB の欠落を protocol
不整合と区別できない。

## 内部データモデル

値 object は frozen な pydantic model または dataclass とし、少なくとも次を持つ。

### Capture 内部

```text
CapturedFrame
  connection_id
  frame_sequence
  direction: inbound | outbound
  observed_at
  payload: bytes
```

`inbound` は server から browser、`outbound` は browser から server と定義する。

### Publication

共通 field:

```text
schema_version: 1
stream_id
publication_sequence
connection_id
kind: notice | request_response
```

`RawNotice`:

```text
direction
frame_sequence
observed_at
api_name
payload_base64
```

`RawRequestResponse`:

```text
request_direction
request_number
request_frame_sequence
request_observed_at
response_frame_sequence
response_observed_at
api_name
request_payload_base64
response_payload_base64
```

raw field には envelope を含む WebSocket payload 全体を入れる。client decoder は
再検証のうえ本文を取り出す。これにより user hook とデバッグログは v2 と同様に
raw payload を利用できる。

ZMQ は 2-part message とする。

```text
frame 1: majsoulrpa.sniffer.v1
frame 2: publication JSON bytes
```

schema に未知 field がある場合は初期実装では reject する。schema version が違う
場合も暗黙に読み替えない。

## 配送保証と Screen 状態

ZeroMQ PUB/SUB は subscriber の接続前や処理遅延時の message を保証しない。
したがって Sniffer stream を durable log として扱わない。

- publisher は `stream_id` ごとに `publication_sequence` を 1 から増やす
- subscriber は同一 stream 内の sequence gap と巻き戻りをエラーにする
- 最初に受け取った sequence が 1 より大きければ途中参加として記録する
- gap または途中参加後、過去の完全性を必要とする Screen state は
  `unknown` とし、成功したように補完しない
- 特定 message を待つ API は必ず timeout / cancellation を持つ

Req/Res 対応付けは publish 前に完了しているため、publication が 1 件欠落しても
別の publication が unmatched Response になることはない。

将来、起動時からの完全な履歴が必要だと判明した場合は、PUB/SUB に疑似保証を
足すのではなく、snapshot/replay 用の request channel を別途設計する。初期実装で
XPUB handshake、永続 queue、再送 protocol は導入しない。

## lifecycle と起動順序

現行 `PlaywrightBrowserBackend.start()` は page 作成後すぐに雀魂へ遷移するため、
その後で Sniffer を start すると初期 WebSocket を取り逃がす。実装時には browser
起動を次の順に分ける。

1. Playwright、browser context、blank page を作る
2. PUB socket を bind する
3. page に WebSocket listener を登録し、worker を開始する
4. 雀魂 URL へ遷移し、canvas を待つ
5. browser command の REP server を開始する

browser backend 全体を不必要に抽象化せず、page 作成と初回 navigation の境界だけを
内部 `page_ready` hook として明示する。標準 Playwright browser host は、専用の
`zmq.asyncio.Context`、Playwright capture、PUB publisher、worker を束ねた既定の
Sniffer backend をこの hook で起動する。custom browser backend をテスト等で注入する
場合は、Sniffer backend も必要に応じて明示注入する。Sniffer start、navigation、
request server start のいずれかが失敗したら、開始済みの resource を逆順に cleanup する。

Sniffer worker の予期しない終了は background task に放置しない。browser host は
request server と Sniffer failure を同時に監視し、Sniffer failure を host の失敗として
伝播する。停止時に pending Request が残る場合も成功終了にはしない。

## エラー方針

少なくとも次を別のエラーとして識別できるようにする。

- unsupported WebSocket frame
- malformed liqi envelope
- unknown liqi message kind
- duplicate pending Request
- unmatched Response
- Request / Response direction mismatch
- incomplete exchange on connection close / stop
- publication schema mismatch
- stream gap / restart
- unknown API / protobuf body decode failure
- capture queue overflow

payload 全体を例外 message に含めない。raw payload の debug log は許可するが、
通常の info / error log では connection、direction、番号、API 名など秘密情報を
含まない metadata に限定する。

user hook の例外は Sniffer transport の decode error と混同しない。hook dispatch は
client runtime 側で行い、例外は callback と同様に RPA runtime から伝播させる。

## public surface の初期方針

最初から backend や decoder のすべてを公開 API にしない。`majsoulrpa.sniffer` の
package root は、`Direction`、raw bytes event、raw event を保持する decode 済み
eventだけを公開する。wire publication、backend、capture、parser、correlator、decoder、
transport、workerは公開しない。user hook は、対応検証済みの raw event と decode 済み
eventのどちらを受け取るかを登録時に明示する。

通常の user hook と牌譜バイナリ等のファイル保存処理は RPA client 側で実行する。
browser host は capture、対応検証、配信に限定し、remote hostへユーザーコードや保存先
policyを配置させない。PUB/SUBの欠落を許容できない保存用途が必要になった場合だけ、
browser host側の専用`CaptureSink`またはreplay / ack付きtransportを別設計する。

Screen state からは ZMQ socket や protobuf class を直接参照させず、client runtime が
保持する event stream / state store の狭い API を `ScreenContext` へ渡す。具体的な
Screen 状態機械は Sniffer transport が安定した後、1 画面ずつ設計・実装する。

client runtime の内部message queueは、API名で選別せず、受信してdecodeできたmessageを
すべて到着順に保持する。通常の未読messageにはasync queue、読み取った後の差し戻しには
`deque`を使う。`get()` / `get_nowait()`は差し戻しを優先し、取得したmessageをqueueから
消費する。複数messageを差し戻した場合は差し戻した順序を保つ。

未処理messageの件数とraw payload bytes合計には上限を設ける。上限到達時は古いmessageを
暗黙にevictせず、Sniffer runtimeの致命的errorにする。通常はframework処理がqueueを
継続的に消費するため、長時間運転でも処理済みmessageは残らない。

client受信runtimeはSUB接続後、publicationを1件ずつclient decoderへ渡し、decode済み
messageを内部queueへ投入する。transport、decode、queue overflowのいずれの失敗も
受信loopの失敗として伝播し、connect途中の失敗やcancellationを含むすべての終了経路で
subscriberをcloseする。

RPA runtimeは画面検出・callbackのmain loopとSniffer受信loopを兄弟taskとして監視する。
一方が終了したら他方をcancelしてから共通cleanupを行う。Sniffer受信loopの例外はRPA
runtimeから伝播し、例外なしで終了した場合も常駐serviceの予期しない停止としてerrorに
する。標準Controller runtimeはREQ socketとは別にSUB socket、client decoder、内部
message queueを組み立てる。SUBのconnect完了をready境界とし、その後に画面検出main
loopを開始する。同じ内部queueを`ScreenContext`へmessage source protocolとして注入し、
Screen基底は待機取得、即時取得、差し戻しのprotected操作だけを提供する。Screenから
ZMQ socket、publication、decoder、queueの具体型は参照させない。今後のScreen状態管理は
Sniffer messageを前提とするため、`ScreenContext`のmessage sourceはoptionalにせず構築時の
必須依存とする。contextが存在すればbrowser操作とmessage取得の両方が利用可能であることを
不変条件にする。

Screen基底の名前待機helperは複数API名を受け付ける。呼び出し側は、対象を見つけるまでに
読んだmessageを破棄するか、対象messageを含めてすべて差し戻すかを選ぶ。差し戻す場合は
対象が見つかるまで一時退避し、元の順序でまとめて戻す。即時に1件ずつ戻すと差し戻し
queueが優先され、同じmessageを再取得し続けるためである。cancellationや例外でも退避済み
messageを復元する。

利用者向けraw / decoded hookは初期APIへ追加しない。framework利用者はScreen経由で
decode済みmessageと対応するraw bytesを取得できるため、それでは不足する具体的な
ユースケースが確認できた時点で再設計する。

payload本文のログはSUB層では出さず、Screen APIが対象messageと意味を確定した時点で
decode済みJSONをdebugへ出す。info / warningにはpayload本文ではなく、秘密情報を含まない
状態遷移または異常の要約だけを出す。

たとえば牌譜取得は、`goto_log()`後にqueueを順に読み、
`.lq.Lobby.fetchGameRecord`のReq/Resを取得する。走査中に別のframework処理で必要なmessageを
見つけた場合は差し戻せる。ファイル保存は返された公開raw eventの`response` bytesを
RPA client側のuser callbackで行い、Screenやmessage queue自身には保存先policyを持たせない。

## 初期実装の分割

t_wada の TDD に従い、次の縦切りを一度に 1 つだけ進める。

1. synthetic payload の envelope 分類
2. Request / Response correlator
3. publication schema の encode / decode
4. fake socket を使う PUB / SUB transport
5. fake Playwright WebSocket を使う capture
6. browser host lifecycle への組み込み
7. client runtime の購読と cleanup
8. protobuf body decoder
9. raw / decoded hook
10. 最初の通信依存 Screen state

Playwright の実 frame 取得と Req/Res 対応は、該当する自動テストと品質ゲートを
通した後にユーザーへ手動確認を依頼する。取得した実 payload は一時ログだけに置き、
テスト、fixture、docs、チャット、コミットへ貼らない。

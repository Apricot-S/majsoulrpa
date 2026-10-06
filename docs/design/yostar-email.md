# Yostar 認証メールの照合条件

## コード取得元の差し替え

`majsoulrpa.yostar_email.VerificationCodeProvider` は取得元を選ぶ公開Protocolである。
利用者はこれを継承せず、同じsignatureを持つ2つのasync methodを実装して差し替えられる。

- `fetch()` はコード取得まで待機する。
- `fetch_nowait()` はpollingせず一度だけ確認する。外部I/O自体の待機はあり得る。
- 両methodはコードを `str` として返し、keyword専用の `delete_read_emails` を持つ。
  削除は省略時に無効で、明示的に `True` を渡した場合だけ行う。

取得元固有の設定やresource管理は具体的なproviderに置く。ProtocolにはS3 client、
AWS設定、汎用factory、runtimeでの型判定を追加しない。callbackがユーザーdata内の
providerを直接呼ぶため、core runtimeにproviderの登録や生成機構は不要である。
S3実装に加え、継承しない独自実装を型付きconsumerへ渡すテストを型検査・実行して
この差し替え境界を確認する。

`yostar_email/constants.py` は JP 向けのメール照合条件を保持する。

- 送信元は既存実装の `YOSTAR_EMAIL_ADDRESS` と完全一致させる。
  `From` は1 headerで、parserが構文上のdefectを報告せず、送信元が1つの場合だけ
  コード取得に使う。正常な表示名は許容する。任意削除は既存方針どおり宛先と件名で
  判定し、送信元を削除条件へ追加しない。
- `To` headerは1つだけ必要とし、その中に要求された宛先があることを確認する。
  単一header内の複数宛先は許容する。欠落・重複した場合はコード取得と任意削除の
  対象への選択を拒否する。header名の大文字小文字によらず重複を判定する。
- 件名は既存の日本語形式と完全一致させる。コード直前の空白は全角空白であり、
  コードは先頭のゼロを保持した ASCII 数字6桁とする。
  `Subject` headerは1つだけ必要とし、欠落・重複したメールはコード取得にも
  任意削除の対象にも使わない。header名の大文字小文字によらず重複を判定する。
- 有効期間は受信直後から30分未満とし、30分ちょうどと未来の受信時刻を拒否する。
  MIME parser と S3 候補の絞り込みは同じ期限定数を使用する。

## 根拠と確認範囲

[認証通信の調査](../investigations/yostar-auth.md) はコード入力欄が6桁を受け付けることを
記録している。ASCII 数字への限定は `LoginScreen.enter_verification_code()` の既存の
入力検証と揃えるための条件であり、Unicode 数字を ASCII へ変換する処理は行わない。

送信元と件名は既存実装で採用済みの値を維持する。ただし、上記調査は HTTP 認証を
対象としており、送信元・件名を観測した根拠は記録されていない。

有効期限30分の根拠は、認証メール本文の記載である。2026-10-06にユーザーから
確認結果の補足を受けた。実メール本文は保存せず、この仕様だけを記録する。
実装は受信時刻を起点に30分未満を受理する。

synthetic MIME message により件名形式と期間の境界を検証する。実サービスの値が
変わった場合は手動確認の結果として条件を見直し、実メールや実認証コードは資料や
fixture に保存しない。

## 例外と再試行

`YostarVerificationEmailError` はメール処理の共通例外であり、これを捕捉しただけでは
再試行可能とは判断しない。

- `InvalidYostarVerificationEmailError` は個々のメールが照合条件や有効期間を
  満たさないことを表す。同じメールを再処理しても有効にはならない。
  S3 provider はこの候補を除外して他の候補を調べる。
- `majsoulrpa.yostar_email.s3.VerificationEmailNotFoundError` は現在有効なメールが
  見つからないことを表す。不正メール例外とは別の共通例外の派生であり、新着メールを
  待って再取得できる。`fetch_nowait()` はこれを伝播し、`fetch()` はこの型だけを
  polling の再試行対象にする。

他のメール例外、外部処理の失敗、キャンセルは `fetch()` が再試行せず伝播する。
外部処理の失敗に対する再試行判断は呼び出し側で行う。
フレームワークが生成するメール例外のmessageにはメールアドレス・コード・本文や
S3 bucket・prefixを埋め込まない。利用者が独自に指定する例外messageや外部SDKの
例外messageをこの例外階層が自動的に除去する仕組みは設けない。

内部の `VerificationEmail` は送信元・宛先・コードを照合用に保持するが、全fieldを
dataclassのreprから除外する。`repr()` / `str()` と通常ログの `%r` / `%s` に
メール情報を含めない。本文はこのobjectへ保持しない。

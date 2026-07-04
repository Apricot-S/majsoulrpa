# 開発計画

## 原則

実装は小さな縦切りで進めます。高レベル API は一度に 1 つだけ実装し、
その API が関連テスト、Ruff、format、ty を通過したあとで、ユーザーに
実際の雀魂での確認を依頼します。

自動テストから実際の雀魂、AWS、実メール、実ブラウザネットワークへは
アクセスしません。外部接続が必要な確認は、手動確認として明示します。

## 完了条件

各実装単位の完了条件は以下です。

- テストリストが更新されている
- 追加した振る舞いに対応するテストがある
- 関連する `python -m pytest ...` が通る
- `python -m ruff check .` が通る
- `python -m ruff format --check .` が通る
- `python -m ty check` が通る
- 例外を広く握りつぶしていない
- 成功していない処理を成功のように見せるフォールバックがない
- 秘密情報、実メール、Cookie、アクセストークン、ライブ通信キャプチャが
  追加されていない

## Phase 0: 計画とリポジトリ整理

目的: v3 の判断基準を固め、実装に入る前の土台を作る。

作業:

- `AGENTS.md` を短い入口として書き直す
- `docs/agents/` に設計・開発資料を作成する
- v2 の README と examples から、残したい利用感を抽出する
- v2 のコードや資産を削除する段取りを決める
- 削除対象と残すメタ情報を確認する

この Phase では実装しません。

## Phase 1: 空のプロジェクト骨格

目的: v2 の実装を持ち込まず、最小限の Python パッケージとして再出発する。

作業:

- v2 の `src/`、`tests/`、古い examples、古い docs を削除する
- `pyproject.toml` を v3 方針に合わせて最小化する
- `src/majsoulrpa/` に公開 API の空骨格だけを置く
- `tests/` に最初のテストリストと smoke test を置く
- README は v3 の開発中であることを明示する

注意:

- スクリーンショット画像、`.proto`、実通信ログは追加しない
- 削除で判断が必要な資産が出た場合はユーザーに確認する

## Phase 2: 設定とランタイム境界

目的: 実ブラウザに触れずに、設定とライフサイクルの最小単位を固める。

候補 API:

- 設定入力を Python object と TOML から作る
- browser host と client の endpoint を表現する
- 起動、停止、異常終了の結果を明確に返す

テスト:

- TOML のデフォルト値と明示値
- 不正値のエラー
- secret を repr/log に出さないこと
- ランタイム停止が二重実行されても状態をごまかさないこと

## Phase 3: ブラウザホストの最小起動

目的: CLI と Python からブラウザホストを起動する最小 API を作る。

候補 API:

- browser host を CLI で起動する
- Python から同じ host を起動する
- headless、viewport、user data dir などを設定する

テスト:

- 実 Playwright を使わない lifecycle test
- CLI 引数から設定への変換
- 起動失敗時の例外と終了コード

手動確認:

- ここで初めて Playwright のローカル起動をユーザーに依頼する
- 実際の雀魂アクセスはまだ必須にしない

## Phase 4: Presentation 検出ループ

目的: callback 登録と Presentation 選択の利用感を作る。

候補 API:

- Presentation class ごとの async callback 登録
- 登録された Presentation だけを検出対象にする
- state/data を callback 間で受け渡す
- detection timeout を明示する

テスト:

- fake screenshot / fake detector による Presentation 選択
- callback の戻り値が次の state になること
- 未登録 Presentation が無視されること
- timeout と例外伝播

手動確認:

- 実ゲームではなく fake Presentation で examples を確認する

## Phase 5: ログイン関連の最初の高レベル API

目的: `LoginPresentation` 相当の最初の画面 API を 1 つだけ実装する。

候補 API:

- メールアドレス入力
- 認証コード入力

進め方:

- まずテストリストを作る
- 片方の API だけを実装する
- 関連テストと品質ゲートを通す
- ユーザーに実際の雀魂での確認を依頼する
- 確認後に次の API へ進む

注意:

- 実メール本文や認証コードをログに出さない
- AWS S3 連携は別 Phase として扱う

## Phase 6: Home / room / tournament API

目的: 合意済み友人戦・大会に必要な画面操作を、1 API ずつ追加する。

候補 API:

- Home 画面の安定化処理
- RPA 終了と browser close
- 友人戦 room 参加
- 友人戦 room 作成
- 大会 lobby 参加

進め方:

- API ごとにテストリストを作る
- 実装する高レベル API は常に 1 つに絞る
- 各 API ごとにユーザーへ実ゲーム確認を依頼する

対象外:

- 段位戦や不特定多数のオープン対局への参加
- 検出回避のための操作

## Phase 7: WebSocket キャプチャと保存拡張

目的: examples の牌譜バイナリ保存のような用途を、v3 の拡張点として設計する。

作業:

- Playwright と mitmproxy の spike を行う
- raw frame、decoded metadata、request/response 対応付けの可否を確認する
- ユーザーが保存処理を差し込める hook を決める
- 自動テストは synthetic frame のみで行う

手動確認:

- 実通信キャプチャが必要になった場合は、保存先、削除手順、コミット禁止を
  明示してユーザー確認を依頼する

## Phase 8: examples とドキュメント整備

目的: v3 の利用方法を、秘密情報を含まない形で説明する。

作業:

- callback 登録だけで使う最小 example
- custom Presentation example
- synthetic data を使った capture sink example
- browser host CLI example
- TOML config example

注意:

- sample email は placeholder のみ
- AWS credential、実メール、実 log id、実通信 payload は含めない

## Phase 9: リリース前確認

目的: v3 の最初の安定版に必要な品質を確認する。

作業:

- 全体テスト
- Ruff check
- Ruff format check
- ty check
- README と docs の整合性確認
- examples の import 確認
- 安全性と対象外機能の再確認

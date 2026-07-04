# テストと品質基準

## TDD 手順

v3 の実装は t_wada の TDD に従います。

1. テストリストを作る
2. ひとつテストを書く
3. テストを成功させる
4. 必要に応じてリファクタリングを行う

テストリストは、実装前に作ります。実装中に見つかったケースは、
都度テストリストへ追加します。

## テストリストの置き場所

実装が始まったら、テストリストの置き場所を決めます。

候補:

- `docs/agents/test-list.md`
- issue / task tracker
- 対象モジュール近くの design note

どれを選ぶ場合も、テストリストが実装より先に存在する状態を守ります。

## 自動テストで禁止するもの

自動テストでは以下を使いません。

- 実際の雀魂へのアクセス
- 実 AWS
- 実メール
- 実認証コード
- 実 Cookie
- 実アクセストークン
- ライブ通信キャプチャ
- 実アカウントが写ったスクリーンショット

外部依存が必要な挙動は、fake、stub、synthetic data で表現します。

## テストの種類

優先するテスト:

- config の default と validation
- callback dispatch
- Presentation 検出の優先順位
- timeout と cancellation
- lifecycle の開始、停止、異常終了
- capture hook の dispatch
- secret が repr/log/exception に出ないこと

実ブラウザが必要なテストは、自動テストではなく手動確認として扱います。

## 品質ゲート

基本コマンド:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m ty check
```

変更範囲が狭い場合は、まず関連テストだけを実行してよいです。ただし、
共有基盤、config、runtime、Presentation、capture に触れた場合は、
最終確認で全体の品質ゲートを通します。

## 例外と fallback

禁止:

- 広い例外捕捉で処理を続ける
- 失敗した操作を成功として扱う
- decode 失敗を空 message として扱う
- timeout を通常完了として扱う
- cleanup 失敗を完全に無視する

許容:

- cleanup 中の副次的な失敗を主例外に添えて報告する
- retry 条件が明確な一時失敗だけ retry する
- ユーザーが明示的に選んだ degraded mode

## 手動確認

高レベル API を 1 つ実装するごとに、ユーザーへ実際の雀魂での確認を依頼します。

確認依頼には以下を含めます。

- 確認対象 API
- 実行手順
- 期待する画面遷移
- ログや保存物に秘密情報が出ないこと
- 実通信や画像を保存する場合の削除方針

ユーザー確認が終わるまで、次の高レベル API 実装へ進みません。

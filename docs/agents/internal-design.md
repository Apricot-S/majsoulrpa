# 内部設計方針

## 基本姿勢

v3 は、過剰な抽象化や定型的な「クリーンアーキテクチャ」風の層分けを避けます。
抽象化は、テスト容易性、置換可能性、ライフサイクル管理のいずれかに
明確な価値がある場合だけ導入します。

## 境界の候補

以下は概念上の境界です。パッケージ名やクラス名は実装時に改めて決めます。

- Public API: callback 登録、config、主要 Presentation
- Browser runtime: Playwright 起動、browser context、page lifecycle
- Client runtime: Presentation 検出、callback dispatch、state 受け渡し
- Presentation: 画面検出と画面操作
- Capture: WebSocket message の観測、decode、ユーザー hook
- Login support: Yostar login code provider などの optional 機能
- Test support: fake browser、fake screen、synthetic capture

## 採用してよい抽象化

次のような場合は抽象化してよいです。

- fake 実装に置き換えることで自動テストが大きく簡単になる
- Playwright と mitmproxy のように、実際に複数実装を比較する必要がある
- 起動、停止、異常終了、後始末を 1 箇所で管理する必要がある
- ユーザー拡張点として明確に公開する

## 避ける抽象化

次のような抽象化は避けます。

- 実装が 1 つしかなく、置換予定もない interface
- DTO と mapper だけが増える層
- 単なるファイル分割のための service / usecase / repository
- private 実装を隠すためだけの facade
- 例外や戻り値を曖昧にする wrapper

## ライフサイクル

ライフサイクルは明示的に扱います。

- browser host の起動と停止
- client runtime の開始と終了
- WebSocket capture の開始と停止
- callback dispatch 中の cancellation
- 終了時の browser close
- 異常終了時の cleanup

終了処理で失敗した場合も、失敗を見えない形にしません。複数の失敗が起きる
可能性がある箇所では、どの失敗を主例外として扱うかをテストで固定します。

## Presentation 検出

Presentation 検出は、画面状態を「できるだけ決定的に」扱います。

方針:

- 固定 sleep だけで安定化しない
- 画像認識、DOM 情報、通信情報のどれを使うかは画面ごとに判断する
- 検出 timeout と操作 timeout を混同しない
- 未登録 Presentation は dispatch しない
- 同時に複数 Presentation が成立する場合の優先順位を明示する

## 画像・テンプレート資産

v3 初期状態では、v2 の画像資産を持ち込みません。

必要になった場合:

- どの API に必要かを説明する
- 画像と設定を対で扱う
- ユーザーにコミットを依頼する
- 実アカウントや個人情報が写らないことを確認する

## protocol 生成物

`.proto` や生成済み Python ファイルは、必要になった時点で扱います。

方針:

- 手編集しない
- 生成手順を docs に残す
- 生成物が必要なテストは synthetic payload を使う
- 実通信 payload を fixture にしない

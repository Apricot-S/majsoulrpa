# AGENTS.md

このファイルは、このリポジトリで作業するエージェント向けの実務メモです。

## Project Overview

MajsoulRPA は Mahjong Soul (雀魂) 向けの RPA フレームワークです。ブラウザを動かすホストと、画面認識や操作判断を行う RPA クライアントを分離できる設計です。

このプロジェクトは、合意済みの友人戦・大会でボットを参加させる用途を想定しています。オープン対局、段位戦、未合意の対局への参加を可能にする機能は追加しないでください。

## Repository Layout

- `src/majsoulrpa/`: ライブラリ本体
- `src/majsoulrpa/browser/`: リモートブラウザ制御・サーバー実装
- `src/majsoulrpa/rpa_client/`: RPA クライアント実装
- `src/majsoulrpa/presentation/`: 画面状態、領域、テンプレート照合の実装
- `src/majsoulrpa/yostar_login/`: Yostar ログイン用メール処理
- `src/majsoulrpa/config_input/`: 設定入力用の型・変換処理
- `src/majsoulrpa/sniffer/`: 通信メッセージ取得関連
- `src/majsoulrpa/_majsoul_internal/protocol/`: Mahjong Soul プロトコル由来の生成物
- `tests/`: pytest テスト
- `examples/`: 利用例
- `docs/`: Sphinx ドキュメント

## Environment

- Python は `>=3.12` を前提にしてください。
- パッケージビルドは `uv_build` を使います。
- 依存関係グループは `pyproject.toml` の `[dependency-groups]` に定義されています。
- 開発時は、必要に応じて `browser`, `client`, `email-s3` の optional dependency を確認してください。

## Common Commands

環境に依存しますが、基本的には次のコマンドで確認します。

```sh
python -m pytest
python -m ruff check .
python -m ty check
```

ドキュメントを確認する場合:

```sh
python -m sphinx -b html docs/source docs/build/html
```

ブラウザ実行環境を作る場合は、README の手順に従って Playwright の Chromium をインストールしてください。

```sh
playwright install chromium --with-deps
```

## Coding Guidelines

- 既存の `src/` レイアウトとパッケージ境界を保ってください。
- 公開 API に近い変更では、型注釈と pydantic モデルの互換性を特に確認してください。
- 非同期処理では、既存の `asyncio` ベースの設計に合わせてください。
- 画面認識や UI 操作の待機は、固定 sleep の追加だけで解決せず、既存の presentation / template / delay の仕組みを優先してください。
- `src/majsoulrpa/_majsoul_internal/protocol/` 配下の生成ファイルは、必要な生成手順が明確な場合を除いて手編集しないでください。
- テンプレート画像と `.toml` 設定は対で扱い、片方だけ変更しないようにしてください。
- `examples/` は利用者向けの参考コードなので、実装変更に追従して壊れないようにしてください。

## Testing Guidance

- 変更した領域に対応する `tests/` 配下のテストを優先して実行してください。
- 共有基盤、設定モデル、通信、presentation の挙動を変える場合は `python -m pytest` 全体を実行してください。
- ブラウザや画像認識に関わる変更では、単体テストだけでなく、サンプル設定やテンプレート資産との整合性も確認してください。
- テストで外部サービス、AWS、実ブラウザ、ネットワークが必要になる場合は、実行条件を明示してください。

## Linting and Types

- Ruff は `line-length = 79`、`select = ["ALL"]` が基本です。
- pydocstyle は Google convention です。ただし `D` はプロジェクト全体では ignore されています。
- `tests/` では assert や private member access の一部が許可されています。設定は `pyproject.toml` を参照してください。
- `src/majsoulrpa/_majsoul_internal/protocol/liqi_pb2.py` と `.pyi` は ty の override 対象です。

## Documentation

- ユーザー向けの導入・利用方法は `README.md` に合わせてください。
- API ドキュメントは `docs/source/` の Sphinx 構成に従ってください。
- README にある利用上の注意、責任範囲、対応しない用途の説明と矛盾する変更は避けてください。

## Security and Safety

- 認証情報、メールアドレス、AWS credential、セッション情報をコミットしないでください。
- `examples/config.example.toml` はサンプルとして扱い、実運用の値を入れないでください。
- Yostar ログインやメール取得周りでは、ログに認証コードや個人情報が出ないよう注意してください。
- ユーザー同意のない対局参加、規約違反を助長する機能、検出回避を目的とした変更は実装しないでください。

## Git Hygiene

- 既存の未コミット変更はユーザーの作業として扱い、勝手に戻さないでください。
- 変更は目的に必要な範囲に絞ってください。
- コミットを作る場合は、この環境の指示に従い Conventional Commits の `<type>` を付けてください。

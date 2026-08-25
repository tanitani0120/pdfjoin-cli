# pdfjoin

![CI](https://github.com/tanitani0120/pdfjoin-cli/actions/workflows/ci.yml/badge.svg)

2つのPDFファイルを連結するコマンドラインツール。

## 動作環境

Python 3.11 以上

## 現在の制限

- 連結できるのは2ファイルまでです（v0.2 で可変長に対応予定）
- パスワード保護されたPDFには対応していません

## インストール

```bash
git clone https://github.com/tanitani0120/pdfjoin-cli.git
cd pdfjoin-cli
pip install -e .
```

## 使い方

```bash
pdfjoin --prefile a.pdf --rearfile b.pdf -o out.pdf
```

```
マージしました:3ページ
```

```bash
# 処理内容を表示
pdfjoin -v --prefile a.pdf --rearfile b.pdf -o out.pdf

# 既存ファイルを上書き
pdfjoin -f --prefile a.pdf --rearfile b.pdf -o out.pdf
```

## 終了コード
| コード | 意味 |
| ---- | ---- |
| 0 | 成功 |
| 2 | 引数エラー |
| 3 | 入力ファイルが見つからない |
| 4 | PDFとして不正 |
| 5 | 出力先の衝突 |

## 設計

### core と cli の分離
将来のGUI化を見据え、`core.merge()` は `print` も `sys.exit` も持たない純粋な関数にしています。
エラーは例外として送出するだけで、それを終了コードやメッセージに変換するのは `cli` の責務です。
同じ `core` をGUIから呼べば、エラーはダイアログ表示に変わります。

### 検証と書き込みの分離
`core.merge()` は入力の検証をすべて終えてから書き込みを開始します。
「1つ読んでは1つ書く」実装だと途中失敗時に壊れたPDFが残るため、これを避けています。
この挙動はテストで固定しています。

### 引数を list[Path] にした理由
「2ファイルまで」はCLIの都合であり、PDF連結という処理自体の制約ではありません。
`core` はドメインの形に合わせて可変長のリストを受け取り、
CLIの2引数をリストに変換するのは `cli` 側の役目としています。

### pypdf を選んだ理由
PDF操作ライブラリには PyMuPDF (AGPL-3.0) などもありますが、
AGPLはリポジトリ全体に強いコピーレフトを課します。
単純な連結処理にその制約は不要と判断し、BSD-3-Clause の pypdf を採用しました。

## 開発
```bash
pip install -e ".[dev]"
ruff format src tests
ruff check src tests
mypy src
pytest
```

## 依存ライブラリ

- [pypdf](https://github.com/py-pdf/pypdf) — BSD-3-Clause

開発時のみ:

- [pytest](https://github.com/pytest-dev/pytest) — MIT
- [ruff](https://github.com/astral-sh/ruff) — MIT
- [mypy](https://github.com/python/mypy) — MIT

## ライセンス

[MIT License](LICENSE)
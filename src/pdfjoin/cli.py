import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from pdfjoin.core import merge
from pdfjoin.errors import InputNotFoundError, InvalidPdfError, OutputConflictError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdfjoin",
        description="二つのPDFファイルを一つに結合します",
    )
    parser.add_argument(
        "--prefile", required=True, type=Path, help="先頭となるPDFファイルのパスを指定します"
    )
    parser.add_argument(
        "--rearfile", required=True, type=Path, help="後尾となるPDFファイルのパスを指定します"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="連結したファイルの出力先のパスを指定します",
    )
    parser.add_argument("-f", "--force", action="store_true", help="既存ファイルを上書きします")
    parser.add_argument("-v", "--verbose", action="store_true", help="処理内容を表示します")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version('pdfjoin')}")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        pages = merge(
            [args.prefile, args.rearfile],
            args.output,
            overwrite=args.force,
        )
    except InputNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except InvalidPdfError as e:
        print(f"error: {e}", file=sys.stderr)
        return 4
    except OutputConflictError as e:
        print(f"error: {e}", file=sys.stderr)
        return 5

    print(f"マージしました:{pages}ページ")
    return 0

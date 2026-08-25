# core.py のシグネチャだけ設計しておく
from pathlib import Path


def merge(inputs: list[Path], output: Path, *, overwrite: bool = False) -> int:
    """連結してページ数を返す。argparse も print も sys.exit もここに書かない。"""

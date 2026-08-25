from pathlib import Path

import pytest
from pypdf import PdfWriter


@pytest.fixture
def make_pdf():
    """指定したページ数の空PDFを作る関数を返す。"""

    def _make(path: Path, pages: int) -> Path:
        writer = PdfWriter()
        for _ in range(pages):
            writer.add_blank_page(width=595, height=842)
        writer.write(path)
        return path

    return _make

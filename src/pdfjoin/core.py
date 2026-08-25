from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from pdfjoin.errors import InputNotFoundError, InvalidPdfError, OutputConflictError


def merge(inputs: list[Path], output: Path, *, overwrite: bool = False) -> int:
    """連結してページ数を返す。"""
    # argparse も print も sys.exit もここに書かない。
    # --- 検証フェーズ: ここでは一切書き込まない ---
    # inputが空でないか ValueError
    if not inputs:
        raise ValueError("入力ファイルが指定されていません")
    # 各inputが存在し、ファイルがあるか InputNotFoundError
    # 各入力がPDFとして開け、暗号化されていないか InvalidPdfErrror
    # outputが入力のいずれかと同一のパスでないか OutputConflictError
    for path in inputs:
        if not path.is_file():
            raise InputNotFoundError(f"ファイルが存在しません:{path}")
        try:
            reader = PdfReader(path)
        except PdfReadError as e:
            raise InvalidPdfError(f"PDFとして読み込めません:{path}") from e
        if reader.is_encrypted:
            raise InvalidPdfError(f"ファイルは暗号化されています:{path}")
        if output.resolve() == path.resolve():
            raise OutputConflictError(f"出力先が入力ファイルと同じパスです:{path}")
    # outputが既存ならoverwrite=Trueであるか OutputConflictError
    if output.is_file() and not overwrite:
        raise OutputConflictError(f"出力ファイルが既に存在しています:{output}")
    # --- 書き込みフェーズ ---
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for path in inputs:
        writer.append(path)
    writer.write(output)
    # 戻り値: 総ページ数とりあえず今は0
    return len(writer.pages)

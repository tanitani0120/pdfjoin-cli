from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from pdfjoin.errors import InputNotFoundError, InvalidPdfError, OutputConflictError


def merge(inputs: list[Path], output: Path, *, overwrite: bool = False) -> int:
    """inputs を順に連結して output に書き出し、総ページ数を返す。

    Raises:
        ValueError: inputs が空のとき
        InputNotFoundError: 入力が存在しない、またはファイルでないとき
        InvalidPdfError: PDFとして読めない、または暗号化されているとき
        OutputConflictError: 出力先が入力と同一、または既存で overwrite=False のとき
    """
    # --- 検証フェーズ: ここでは一切書き込まない ---
    if not inputs:
        raise ValueError("入力ファイルが指定されていません")
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
    if output.is_file() and not overwrite:
        raise OutputConflictError(f"出力ファイルが既に存在しています:{output}")
    # --- 書き込みフェーズ ---
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for path in inputs:
        writer.append(path)
    writer.write(output)
    return len(writer.pages)

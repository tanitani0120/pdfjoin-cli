import pytest
from pypdf import PdfReader

from pdfjoin.core import merge
from pdfjoin.errors import InputNotFoundError, InvalidPdfError, OutputConflictError


def test_merge_returns_total_pages(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    b = make_pdf(tmp_path / "b.pdf", 2)
    output = tmp_path / "out.pdf"

    pages = merge([a, b], output)

    assert pages == 3
    assert len(PdfReader(output).pages) == 3


def test_merge_raises_when_input_missing(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    missing = tmp_path / "nope.pdf"  # 作らない
    output = tmp_path / "out.pdf"

    with pytest.raises(InputNotFoundError):
        merge([a, missing], output)

    assert not output.exists()


def test_merge_raises_when_inputs_empty(tmp_path):
    output = tmp_path / "out.pdf"
    inputs = []
    with pytest.raises(ValueError):
        merge(inputs, output)

    assert not output.exists()


def test_merge_raises_when_output_exists(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    b = make_pdf(tmp_path / "b.pdf", 2)
    output = make_pdf(tmp_path / "out.pdf", 1)

    with pytest.raises(OutputConflictError):
        merge([a, b], output)

    assert len(PdfReader(output).pages) == 1


def test_merge_raises_when_output_same_as_input(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    b = make_pdf(tmp_path / "b.pdf", 2)

    with pytest.raises(OutputConflictError):
        merge([a, b], a)

    assert len(PdfReader(a).pages) == 1


def test_merge_raises_when_input_is_not_pdf(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    broken = tmp_path / "broken.pdf"
    broken.write_text("これはPDFではない", encoding="utf-8")
    output = tmp_path / "out.pdf"

    with pytest.raises(InvalidPdfError):
        merge([a, broken], output)

    assert not output.exists()


def test_merge_overwrites_when_forced(tmp_path, make_pdf):
    a = make_pdf(tmp_path / "a.pdf", 1)
    b = make_pdf(tmp_path / "b.pdf", 2)
    output = make_pdf(tmp_path / "out.pdf", 1)

    pages = merge([a, b], output, overwrite=True)

    assert pages == 3
    assert len(PdfReader(output).pages) == 3

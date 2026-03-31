# file: tests/test_curriculum_loader.py

import pytest
from unittest.mock import MagicMock

from ingestion.cv_loader import CurriculumLoader


# ---------- TESTS ----------

def test_no_input_raises():
    loader = CurriculumLoader()

    with pytest.raises(ValueError):
        loader.load()


def test_content_passthrough():
    loader = CurriculumLoader()

    result = loader.load(content="hello world")

    assert result == "hello world"


def test_pdf_loader_called(monkeypatch):
    loader = CurriculumLoader()

    mock_loader = MagicMock()
    mock_loader.load.return_value = "pdf content"

    monkeypatch.setattr(
        loader,
        "chose_loader",
        lambda _: mock_loader
    )

    result = loader.load(file_path="test.pdf")

    assert result == "pdf content"
    mock_loader.load.assert_called_once_with("test.pdf")


def test_odt_loader_called(monkeypatch):
    loader = CurriculumLoader()

    mock_loader = MagicMock()
    mock_loader.load.return_value = "odt content"

    monkeypatch.setattr(
        loader,
        "chose_loader",
        lambda _: mock_loader
    )

    result = loader.load(file_path="test.odt")

    assert result == "odt content"


def test_unsupported_file_raises(monkeypatch):
    loader = CurriculumLoader()

    monkeypatch.setattr(
        loader,
        "chose_loader",
        lambda _: None
    )

    with pytest.raises(ValueError):
        loader.load(file_path="test.xyz")


def test_chose_loader_pdf():
    loader = CurriculumLoader()

    result = loader.chose_loader("file.pdf")

    from ingestion.pdf_loader import PdfLoader
    assert isinstance(result, PdfLoader)


def test_chose_loader_odt():
    loader = CurriculumLoader()

    result = loader.chose_loader("file.odt")

    from ingestion.odt_loader import OpenDocLoader
    assert isinstance(result, OpenDocLoader)


def test_chose_loader_docx_returns_none():
    loader = CurriculumLoader()

    result = loader.chose_loader("file.docx")

    from ingestion.docx_loader import DocxLoader
    assert isinstance(result, DocxLoader)
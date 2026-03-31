import pytest
from io import BytesIO
from unittest.mock import MagicMock

from ingestion.odt_loader import OpenDocLoader


@pytest.fixture
def loader(tmp_path):
    loader = OpenDocLoader()

    file_path = tmp_path / "test.odt"
    file_path.write_text("dummy")

    return loader, str(file_path)


def make_odt_xml(paragraphs):
    content = """
    <office:document-content xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
        <office:body>
            <office:text>
                {}
            </office:text>
        </office:body>
    </office:document-content>
    """

    xml_paragraphs = "".join(
        f"<text:p>{p}</text:p>" for p in paragraphs
    )

    return content.format(xml_paragraphs).encode("utf-8")


# 🔥 FIXED MOCK
def mock_zipfile(monkeypatch, xml_bytes):
    mock_file = BytesIO(xml_bytes)

    mock_open = MagicMock()
    mock_open.__enter__.return_value = mock_file

    mock_zip = MagicMock()
    mock_zip.__enter__.return_value = mock_zip
    mock_zip.open.return_value = mock_open

    monkeypatch.setattr(
        "ingestion.odt_loader.ZipFile",
        lambda *args, **kwargs: mock_zip
    )


# ---------- TESTS ----------

def test_invalid_file():
    loader = OpenDocLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("not_existing.odt")

    with pytest.raises(FileNotFoundError):
        loader.load("file.txt")


def test_extract_text_basic(monkeypatch, loader):
    loader_obj, file_path = loader

    xml_bytes = make_odt_xml(["Hello", "World"])
    mock_zipfile(monkeypatch, xml_bytes)

    paragraphs = loader_obj._extract_text(file_path)

    assert paragraphs == ["Hello", "World"]


def test_load_combines_paragraphs(monkeypatch, loader):
    loader_obj, file_path = loader

    xml_bytes = make_odt_xml(["Line1", "Line2"])
    mock_zipfile(monkeypatch, xml_bytes)

    result = loader_obj.load(file_path)

    assert result == "Line1\nLine2"


def test_empty_paragraphs_filtered(monkeypatch, loader):
    loader_obj, file_path = loader

    xml_bytes = make_odt_xml(["", "Valid", "   "])
    mock_zipfile(monkeypatch, xml_bytes)

    result = loader_obj.load(file_path)

    assert result == "Valid"


def test_nested_text_nodes(monkeypatch, loader):
    loader_obj, file_path = loader

    xml_bytes = b"""
    <office:document-content xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
        <office:body>
            <office:text>
                <text:p>Hello <text:span>World</text:span></text:p>
            </office:text>
        </office:body>
    </office:document-content>
    """

    mock_zipfile(monkeypatch, xml_bytes)

    result = loader_obj.load(file_path)

    assert result == "Hello World"
import pytest
from types import SimpleNamespace

from ingestion.pdf_loader import PdfLoader


# ---------- HELPERS ----------

def make_text_item(text, page_no):
    return SimpleNamespace(
        text=text,
        prov=[SimpleNamespace(page_no=page_no)]
    )


def make_doc(text_items):
    return SimpleNamespace(texts=text_items)


def make_result(doc):
    return SimpleNamespace(document=doc)


# ---------- FIXTURES ----------

@pytest.fixture
def loader(monkeypatch, tmp_path):
    loader = PdfLoader()

    # Create fake pdf file
    file_path = tmp_path / "test.pdf"
    file_path.write_text("dummy")

    return loader, str(file_path)


# ---------- TESTS ----------

def test_invalid_file_raises():
    loader = PdfLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("not_existing.pdf")

    with pytest.raises(FileNotFoundError):
        loader.load("file.txt")


def test_single_page_extraction(loader, monkeypatch):
    loader_obj, file_path = loader

    fake_doc = make_doc([
        make_text_item("Hello", 1),
        make_text_item("World", 1),
    ])

    monkeypatch.setattr(
        loader_obj.converter,
        "convert",
        lambda _: make_result(fake_doc)
    )

    result = loader_obj.load(file_path)

    assert result == "Hello\nWorld"


def test_multi_page_extraction(loader, monkeypatch):
    loader_obj, file_path = loader

    fake_doc = make_doc([
        make_text_item("Page1-A", 1),
        make_text_item("Page2-A", 2),
        make_text_item("Page1-B", 1),
    ])

    monkeypatch.setattr(
        loader_obj.converter,
        "convert",
        lambda _: make_result(fake_doc)
    )

    result = loader_obj.load(file_path)

    assert "Page1-A" in result
    assert "Page1-B" in result
    assert "Page2-A" in result


def test_empty_texts_are_ignored(loader, monkeypatch):
    loader_obj, file_path = loader

    fake_doc = make_doc([
        make_text_item("", 1),
        make_text_item(None, 1),
        make_text_item("Valid", 1),
    ])

    monkeypatch.setattr(
        loader_obj.converter,
        "convert",
        lambda _: make_result(fake_doc)
    )

    result = loader_obj.load(file_path)

    assert result == "Valid"


def test_no_prov_defaults_to_page_zero(loader, monkeypatch):
    loader_obj, file_path = loader

    fake_doc = SimpleNamespace(
        texts=[
            SimpleNamespace(text="NoProv", prov=None)
        ]
    )

    monkeypatch.setattr(
        loader_obj.converter,
        "convert",
        lambda _: make_result(fake_doc)
    )

    result = loader_obj.load(file_path)

    assert result == "NoProv"
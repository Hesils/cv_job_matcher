from collections import defaultdict
from pathlib import Path

from ingestion.base_doc_loader import BaseLoader

from docling.document_converter import DocumentConverter


class PdfLoader(BaseLoader):
    def __init__(self):
        super().__init__("pdf")
        self.converter = DocumentConverter()


    def load(self, file_path: str) -> str:
        fpath = Path(file_path)
        if not fpath.exists() or not fpath.is_file() or not fpath.suffix == ".pdf":
            raise FileNotFoundError(f"{fpath} is not a pdf file")

        result = self.converter.convert(file_path)
        doc = result.document

        # --- group texts by page ---
        pages_content = defaultdict(list)

        for text_item in doc.texts:
            if not text_item.text:
                continue

            prov = text_item.prov[0] if text_item.prov else None
            page_no = prov.page_no if prov else 0

            pages_content[page_no].append(text_item.text)

        contents = []

        for page_no, texts in pages_content.items():
            content = "\n".join(texts).strip()

            if not content:
                continue  # why: avoid empty pages

            contents.append(content)

        return "\n".join(contents)
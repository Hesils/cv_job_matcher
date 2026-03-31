from pathlib import Path
from typing import Optional

from ingestion.base_doc_loader import BaseLoader
from ingestion.odt_loader import OpenDocLoader
from ingestion.pdf_loader import PdfLoader
from ingestion.docx_loader import DocxLoader


class CurriculumLoader:
    def __init__(self):
        pass

    def load(self, file_path: Optional[str] = None, content: Optional[str] = None) -> str:
        if not file_path and not content:
            raise ValueError("Either file_path or content must be provided")
        if file_path:
            loader = self.chose_loader(file_path)
            if not loader:
                raise ValueError("File type not supported")
            return loader.load(file_path)
        else:
            return content

    @staticmethod
    def chose_loader(file_path: str) -> Optional[BaseLoader]:
        suffix = Path(file_path).suffix
        if suffix == ".pdf":
            return PdfLoader()
        elif suffix == ".odt":
            return OpenDocLoader()
        elif suffix == ".docx":
            return DocxLoader()
        return None
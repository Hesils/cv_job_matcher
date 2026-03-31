from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from ingestion.base_doc_loader import BaseLoader


ODT_NAMESPACE = {
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
}


class OpenDocLoader(BaseLoader):
    def __init__(self):
        super().__init__(".odt")

    @staticmethod
    def _extract_text(file_path: str) -> list[str]:
        with ZipFile(file_path, "r") as z:
            with z.open("content.xml") as f:
                tree = ET.parse(f)

        root = tree.getroot()

        paragraphs = []
        for p in root.findall(".//text:p", ODT_NAMESPACE):
            text = "".join(p.itertext()).strip()
            if text:
                paragraphs.append(text)

        return paragraphs


    def load(self, file_path: str) -> str:
        fpath = Path(file_path)
        if not fpath.exists() or not fpath.is_file() or not fpath.suffix == ".odt":
            raise FileNotFoundError(f"{fpath} is not an odt file")
        paragraphs = self._extract_text(file_path)

        return "\n".join(paragraphs)

from typing import Optional

class JobLoader:
    def __init__(self):
        pass

    def load(self, url: Optional[str] = None, content: Optional[str] = None) -> str:
        if not url and not content:
            raise ValueError("Either file_path or content must be provided")
        if url:
            raise ValueError("url not implemented yet")
        else:
            return content
        
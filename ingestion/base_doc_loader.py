from abc import ABC, abstractmethod


class BaseLoader(ABC):

    def __init__(self, file_type: str):
        self.file_type = file_type

    @abstractmethod
    def load(self, file_path: str) -> str:
        ...
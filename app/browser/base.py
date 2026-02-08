from abc import ABC, abstractmethod
from typing import List, Any

class BaseBrowser(ABC):
    def __init__(self, headless: bool = True):
        self.headless = headless

    @abstractmethod
    def open(self, url: str) -> None:
        pass

    @abstractmethod
    def find_elements(self, selector: str) -> List[Any]:  # 🔹 corrige le type
        """Doit retourner une liste d'éléments"""
        pass

    @abstractmethod
    def get_text(self, selector: str) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

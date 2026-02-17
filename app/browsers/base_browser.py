from abc import ABC, abstractmethod


class BaseBrowser(ABC):

    @abstractmethod
    def open(self, url: str):
        pass

    @abstractmethod
    def find_elements(self, selector: str):
        pass

    @abstractmethod
    def get_text(self, element):
        pass

    @abstractmethod
    def get_attribute(self, element, attr: str):
        pass

    @abstractmethod
    def scroll_to_bottom(self):
        pass

    @abstractmethod
    def quit(self):
        pass

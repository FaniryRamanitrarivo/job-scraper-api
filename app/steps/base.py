from abc import ABC, abstractmethod

class StepHandler(ABC):

    @abstractmethod
    def execute(self, step: dict, ctx) -> None:
        """
        Exécute la logique du step sur le contexte.
        """
        pass

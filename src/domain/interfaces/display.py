from abc import ABC, abstractmethod
from src.domain.entities.event import Event

class IDisplayService(ABC):
    @abstractmethod
    def show(self, events: list[Event]) -> None:
        pass

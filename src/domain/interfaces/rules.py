from abc import ABC, abstractmethod
from src.domain.entities.event import Event

class IRule(ABC):
    @abstractmethod
    def apply(self, events: list[Event]) -> list[Event]:
        pass

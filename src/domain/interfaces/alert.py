from abc import ABC, abstractmethod
from src.domain.entities.event import Event

class IAlertService(ABC):
    @abstractmethod
    def alert(self, events: list[Event]) -> None:
        pass
from abc import ABC, abstractmethod

from ..entities.event import Event

class IAlertService(ABC):
    @abstractmethod
    def alert(self, event: Event) -> None:
        pass
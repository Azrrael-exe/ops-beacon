from abc import ABC, abstractmethod

from ..entities.event import Event

class IDisplayService(ABC):
    @abstractmethod
    def display(self, events: list[Event]) -> None:
        pass
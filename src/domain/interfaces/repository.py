from abc import ABC, abstractmethod
from src.domain.entities.event import Event

class IEventRepository(ABC):
    @abstractmethod
    def save(self, events: list[Event]) -> None:
        pass

    @abstractmethod
    def get_event_by_id(self, id: int) -> Event:
        pass

    @abstractmethod
    def get_all_events(self) -> list[Event]:
        pass

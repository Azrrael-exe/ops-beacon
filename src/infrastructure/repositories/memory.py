from src.domain.interfaces.repository import IEventRepository
from src.domain.entities.event import Event

class MemoryFastEventRepository(IEventRepository):
    def __init__(self):
        self.events_dict = {}

    def save(self, events: list[Event]) -> None:
        for event in events:
            self.events_dict[event.id] = event

    def get_event_by_id(self, id: int) -> Event:
        return self.events_dict[id]
    
    def get_all_events(self) -> list[Event]:
        return list(self.events_dict.values())
from src.domain.interfaces.alert import IAlertService
from src.domain.interfaces.display import IDisplayService
from src.domain.entities.event import Event

class DummyAlertService(IAlertService):
    def alert(self, events: list[Event]) -> None:
        print(f"Alerting {events}")

class DummyDisplayService(IDisplayService):
    def show(self, events: list[Event]) -> None:
        print(f"Displaying {events}")
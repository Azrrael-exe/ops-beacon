from datetime import timedelta
from src.domain.interfaces.rules import IRule
from src.domain.entities.event import Event, EventLevel
from datetime import datetime

class SimpleRule(IRule):
    def apply(self, events: list[Event]) -> Event | list[Event] | None:
        for event in events:
            if event.level in [EventLevel.ERROR, EventLevel.CRITICAL]:
                if event.timestamp < (datetime.now() - timedelta(minutes=10)):
                    event.set_as_alerting()
        return events

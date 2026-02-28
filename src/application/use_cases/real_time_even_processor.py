from src.domain.interfaces.repository import IEventRepository
from src.domain.interfaces.rules import IRule
from src.domain.interfaces.alert import IAlertService
from src.domain.interfaces.display import IDisplayService
from src.domain.entities.event import Event, EventLevel, EventStatus
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Any


def event_parser(payload: dict[str, Any]) -> list[Event]:
    """
    Parse a payload with structure: {"events": [{"id": ..., "source": ..., ...}, ...]}
    Returns a list of Event objects.
    """
    try:
        events_data = payload.get("events", [])
        events = []

        for event_data in events_data:
            event = Event(
                id=event_data["id"],
                source=event_data["source"],
                level=EventLevel[event_data["level"]] if isinstance(event_data["level"], str) else event_data["level"],
                timestamp=datetime.fromisoformat(event_data["timestamp"]) if isinstance(event_data["timestamp"], str) else event_data["timestamp"],
                status=EventStatus[event_data.get("status", "NEW")] if isinstance(event_data.get("status", "NEW"), str) else event_data.get("status", EventStatus.NEW),
                should_alert=event_data.get("should_alert", False),
                metadata=event_data.get("metadata", {})
            )
            events.append(event)

        return events
    except Exception as e:
        raise ValueError(f"Error parsing events: {e}")


class RealTimeEventProcessor:
    def __init__(
        self,
        event_repository: IEventRepository,
        rule: IRule,
        alert_service: IAlertService,
        display_service: IDisplayService,
    ):
        self.event_repository = event_repository
        self.rule = rule
        self.alert_service = alert_service
        self.display_service = display_service

    def process(self, events: list[Event]) -> None:
        # 1. Apply the rule
        processed_events = self.rule.apply(events)

        # 2. Save the events
        self.event_repository.save(processed_events)

        # 3. Alert the events
        alerted_events = [event for event in processed_events if event.should_alert]
        self.alert_service.alert(alerted_events)

        # 4. Display the events
        for event in processed_events:
            self.display_service.show(event)

from src.domain.interfaces.repository import IEventRepository
from src.domain.interfaces.rules import IRule
from src.domain.interfaces.alert import IAlertService
from src.domain.interfaces.display import IDisplayService
from src.domain.entities.event import Event

class RealTimeEventProcessor:
    def __init__(
        self, 
        event_repository: IEventRepository, 
        rule: IRule, 
        alert_service: IAlertService, 
        display_service: IDisplayService
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
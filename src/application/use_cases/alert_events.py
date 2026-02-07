from domain import IEventRepository, IAlertService

class AlertEventsUseCase:
    def __init__(self, event_repository: IEventRepository, alert_service: IAlertService):
        self.event_repository = event_repository
        self.alert_service = alert_service

    def execute(self) -> None:
        events = self.event_repository.get_all()
        for event in events:
            if event.needs_alert():
                self.alert_service.alert(event=event)

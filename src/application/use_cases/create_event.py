from domain import Event, IEventRepository

class CreateEventUseCase:
    def __init__(self, event_repository: IEventRepository):
        self.event_repository = event_repository

    def execute(self, event: Event) -> Event:
        self.event_repository.add(event)
        return event

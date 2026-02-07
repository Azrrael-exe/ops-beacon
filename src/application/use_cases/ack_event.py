from domain import Event, IEventRepository
from domain.exceptions.domain_exceptions import DomainException

class AckEventUseCase:
    def __init__(self, event_repository: IEventRepository):
        self.event_repository = event_repository

    def execute(self, event_id: int) -> Event:
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise DomainException(f"Event with id {event_id} not found")
        event.acknowledge()
        self.event_repository.update(event)
        return event

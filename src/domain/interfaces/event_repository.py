"""Repository interface for event persistence."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from ..entities.event import Event
from ..enums.alert_level import AlertLevel
from ..enums.event_status import EventStatus


class IEventRepository(ABC):
    """
    Abstract repository interface for event persistence.

    Defines contract that infrastructure layer must implement.
    Domain layer depends on this abstraction, not concrete implementations
    (Dependency Inversion Principle).
    """

    @abstractmethod
    def add(self, event: Event) -> None:
        """
        Add a new event to the repository.

        Args:
            event: Event to persist
        """
        pass

    @abstractmethod
    def get_by_id(self, event_id: int) -> Event | None:
        """
        Retrieve event by its unique identifier.

        Args:
            event_id: Unique identifier (integer)

        Returns:
            Event if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> Sequence[Event]:
        """
        Retrieve all events, sorted by priority.

        Events are ordered by level (ERROR > WARNING > NORMAL)
        and timestamp within each level.

        Returns:
            Sequence of events ordered by priority
        """
        pass

    @abstractmethod
    def get_by_status(self, status: EventStatus) -> Sequence[Event]:
        """
        Retrieve events filtered by status.

        Args:
            status: Status to filter by

        Returns:
            Sequence of matching events, sorted by priority
        """
        pass

    @abstractmethod
    def get_by_level(self, level: AlertLevel) -> Sequence[Event]:
        """
        Retrieve events filtered by alert level.

        Args:
            level: Alert level to filter by

        Returns:
            Sequence of matching events, sorted by timestamp
        """
        pass

    @abstractmethod
    def update(self, event: Event) -> None:
        """
        Update an existing event.

        Args:
            event: Event with updated state

        Raises:
            EventNotFoundError: If event does not exist
        """
        pass

    @abstractmethod
    def delete(self, event_id: int) -> None:
        """
        Remove an event from the repository.

        Args:
            event_id: Unique identifier (integer) of event to remove

        Raises:
            EventNotFoundError: If event does not exist
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get total number of events.

        Returns:
            Count of all events
        """
        pass

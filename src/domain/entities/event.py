"""Core event entity representing operational events."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, ClassVar

from ..enums.alert_level import AlertLevel
from ..enums.event_status import EventStatus
from ..exceptions.domain_exceptions import (
    InvalidEventStateError,
    InvalidEventTransitionError,
)


@dataclass
class Event:
    """
    Core domain entity representing an operational event.

    Events have unique identifiers and can transition from NEW to ACKNOWLEDGED.
    Priority is determined by level (ERROR > WARNING > NORMAL) and timestamp.

    Attributes:
        id: Unique event identifier (auto-incremented integer)
        source: Origin system or component
        metadata: Additional contextual information
        level: Alert severity level
        timestamp: When the event occurred (timezone-aware)
        status: Current lifecycle state (default: NEW)
    """

    # Class variable for auto-incrementing IDs
    _next_id: ClassVar[int] = 1

    id: int
    source: str
    metadata: dict[str, Any]
    level: AlertLevel
    timestamp: datetime
    status: EventStatus = field(default=EventStatus.NEW)

    def __post_init__(self) -> None:
        """
        Validate event state after initialization.

        Raises:
            InvalidEventStateError: If any validation fails
        """
        self._validate_source()
        self._validate_metadata()
        self._validate_timestamp()
        self._validate_initial_state()

    def _validate_source(self) -> None:
        """
        Ensure source is non-empty.

        Raises:
            InvalidEventStateError: If source is empty or whitespace
        """
        if not self.source or not self.source.strip():
            raise InvalidEventStateError("Event source cannot be empty")

    def _validate_metadata(self) -> None:
        """
        Ensure metadata is a dictionary.

        Raises:
            InvalidEventStateError: If metadata is not a dict
        """
        if not isinstance(self.metadata, dict):
            raise InvalidEventStateError("Event metadata must be a dictionary")

    def _validate_timestamp(self) -> None:
        """
        Ensure timestamp has timezone information.

        Raises:
            InvalidEventStateError: If timestamp is naive (no timezone)
        """
        if self.timestamp.tzinfo is None:
            raise InvalidEventStateError(
                "Event timestamp must be timezone-aware"
            )

    def _validate_initial_state(self) -> None:
        """
        Validate domain invariants.

        Rule: NORMAL events should not be created with ACKNOWLEDGED status
        (they don't require acknowledgment).

        Raises:
            InvalidEventStateError: If NORMAL event is ACKNOWLEDGED
        """
        if (
            self.level == AlertLevel.NORMAL
            and self.status == EventStatus.ACKNOWLEDGED
        ):
            raise InvalidEventStateError(
                "NORMAL events cannot be acknowledged "
                "(no acknowledgment required)"
            )

    @classmethod
    def create(
        cls,
        source: str,
        metadata: dict[str, Any],
        level: AlertLevel,
        timestamp: datetime | None = None,
    ) -> 'Event':
        """
        Factory method to create a new event with auto-generated ID.

        Args:
            source: Origin system or component
            metadata: Additional contextual information
            level: Alert severity level
            timestamp: When event occurred (defaults to now in UTC)

        Returns:
            New Event instance with NEW status and auto-incremented ID

        Raises:
            InvalidEventStateError: If validation fails
        """
        if timestamp is None:
            timestamp = datetime.now(UTC)

        event_id = cls._next_id
        cls._next_id += 1

        return cls(
            id=event_id,
            source=source,
            metadata=metadata,
            level=level,
            timestamp=timestamp,
            status=EventStatus.NEW,
        )

    @classmethod
    def reset_id_counter(cls, start_from: int = 1) -> None:
        """
        Reset the ID counter to a specific value.

        Useful for testing or when clearing all events.

        Args:
            start_from: The value to start counting from (default: 1)
        """
        cls._next_id = start_from

    def acknowledge(self) -> None:
        """
        Acknowledge this event, transitioning status from NEW to ACKNOWLEDGED.

        Domain rules:
        - Only WARNING and ERROR events can be acknowledged
        - Cannot acknowledge already acknowledged events
        - NORMAL events throw exception (they don't require acknowledgment)

        Raises:
            InvalidEventTransitionError: If acknowledgment rules violated
        """
        # Rule: Cannot acknowledge NORMAL events
        if self.level == AlertLevel.NORMAL:
            raise InvalidEventTransitionError(
                f"Cannot acknowledge NORMAL event {self.id}: "
                "NORMAL events do not require acknowledgment"
            )

        # Rule: Cannot acknowledge already acknowledged events
        if self.status == EventStatus.ACKNOWLEDGED:
            raise InvalidEventTransitionError(
                f"Event {self.id} is already acknowledged"
            )

        # Valid transition: NEW → ACKNOWLEDGED
        self.status = EventStatus.ACKNOWLEDGED

    def requires_acknowledgment(self) -> bool:
        """
        Determine if this event requires acknowledgment.

        Returns:
            True for WARNING and ERROR events, False for NORMAL
        """
        return self.level.requires_acknowledgment()

    def needs_alert(self) -> bool:
        """
        Determine if this event should trigger an alert.

        An event needs an alert if it requires acknowledgment
        and has not yet been acknowledged.

        Returns:
            True if event requires acknowledgment and is not yet acknowledged
        """
        return (
            self.requires_acknowledgment() and self.status == EventStatus.NEW
        )

    def __lt__(self, other: 'Event') -> bool:
        """
        Enable sorting by priority (level first, then timestamp).

        Sorting order:
        1. By level: ERROR < WARNING < NORMAL (for ascending sort)
        2. Within same level: earlier timestamp < later timestamp

        Args:
            other: Another Event to compare against

        Returns:
            True if this event has higher priority than other

        Raises:
            TypeError: If other is not an Event
        """
        if not isinstance(other, Event):
            return NotImplemented

        # First priority: level (ERROR > WARNING > NORMAL)
        if self.level != other.level:
            return self.level < other.level

        # Second priority: timestamp (earlier events first)
        return self.timestamp < other.timestamp

    def __hash__(self) -> int:
        """
        Hash based on immutable ID.

        Returns:
            Hash of the event ID
        """
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """
        Events are equal if they have the same ID.

        Args:
            other: Another object to compare against

        Returns:
            True if both events have the same ID
        """
        if not isinstance(other, Event):
            return NotImplemented
        return self.id == other.id

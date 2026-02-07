"""Event status enumeration for lifecycle state tracking."""

from enum import Enum, auto


class EventStatus(Enum):
    """
    Enumeration of event lifecycle states.

    Valid transition: NEW → ACKNOWLEDGED (one-way, no rollback)
    """

    NEW = auto()
    ACKNOWLEDGED = auto()

    def is_acknowledged(self) -> bool:
        """
        Check if status represents an acknowledged event.

        Returns:
            True if status is ACKNOWLEDGED, False otherwise
        """
        return self == EventStatus.ACKNOWLEDGED

    def is_new(self) -> bool:
        """
        Check if status represents a new event.

        Returns:
            True if status is NEW, False otherwise
        """
        return self == EventStatus.NEW

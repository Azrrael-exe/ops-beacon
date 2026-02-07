"""Alert level enumeration for event severity classification."""

from enum import Enum, auto


class AlertLevel(Enum):
    """
    Enumeration of alert severity levels.

    Events are prioritized in descending order:
    ERROR > WARNING > NORMAL
    """

    NORMAL = auto()
    WARNING = auto()
    ERROR = auto()

    def requires_acknowledgment(self) -> bool:
        """
        Determine if events at this level require acknowledgment.

        Returns:
            True for WARNING and ERROR levels, False for NORMAL
        """
        return self in (AlertLevel.WARNING, AlertLevel.ERROR)

    def __lt__(self, other: 'AlertLevel') -> bool:
        """
        Enable sorting by priority (ERROR > WARNING > NORMAL).

        Higher priority levels compare as "less than" for ascending sorts,
        so sorted() will place ERROR first, then WARNING, then NORMAL.

        Args:
            other: Another AlertLevel to compare against

        Returns:
            True if this level has higher priority than other

        Raises:
            TypeError: If other is not an AlertLevel
        """
        if not isinstance(other, AlertLevel):
            return NotImplemented

        # Priority order: ERROR (0) > WARNING (1) > NORMAL (2)
        priority_order = {
            AlertLevel.ERROR: 0,
            AlertLevel.WARNING: 1,
            AlertLevel.NORMAL: 2
        }
        return priority_order[self] < priority_order[other]

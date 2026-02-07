"""Domain-specific exceptions for business rule violations."""


class DomainException(Exception):
    """
    Base exception for all domain-related errors.

    All domain exceptions inherit from this class, allowing
    application layer to catch domain errors specifically.
    """

    pass


class InvalidEventStateError(DomainException):
    """
    Raised when an event is created with invalid state.

    Examples:
    - Empty source string
    - Invalid metadata type
    - Naive datetime (no timezone)
    - NORMAL event created with ACKNOWLEDGED status
    """

    pass


class InvalidEventTransitionError(DomainException):
    """
    Raised when an invalid state transition is attempted.

    Examples:
    - Attempting to acknowledge a NORMAL event
    - Attempting to re-acknowledge an already acknowledged event
    """

    pass


class EventNotFoundError(DomainException):
    """
    Raised when an event cannot be found in the repository.

    Used by repository implementations when operations
    reference non-existent events.
    """

    pass

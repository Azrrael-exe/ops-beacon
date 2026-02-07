"""Domain exceptions."""

from .domain_exceptions import (
    DomainException,
    EventNotFoundError,
    InvalidEventStateError,
    InvalidEventTransitionError,
)

__all__ = [
    'DomainException',
    'InvalidEventStateError',
    'InvalidEventTransitionError',
    'EventNotFoundError',
]

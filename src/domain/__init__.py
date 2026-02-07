"""
Domain layer - Core business logic and entities.

This layer has no external dependencies and contains:
- Entities: Core domain objects (Event with auto-incremented int IDs)
- Enums: Domain constants (AlertLevel, EventStatus)
- Interfaces: Abstract contracts (EventRepository)
- Exceptions: Domain-specific errors

This module exports the public API for the domain layer,
allowing other layers to import cleanly: `from domain import Event, AlertLevel`
"""

from .entities.event import Event
from .enums.alert_level import AlertLevel
from .enums.event_status import EventStatus
from .exceptions.domain_exceptions import (
    DomainException,
    EventNotFoundError,
    InvalidEventStateError,
    InvalidEventTransitionError,
)
from .interfaces.event_repository import IEventRepository
from .interfaces.alert_service import IAlertService

__all__ = [
    # Entities
    'Event',
    # Enums
    'AlertLevel',
    'EventStatus',
    # Interfaces
    'IEventRepository',
    'IAlertService',
    # Exceptions
    'DomainException',
    'InvalidEventStateError',
    'InvalidEventTransitionError',
    'EventNotFoundError',
]

"""Pytest fixtures for domain tests."""

from datetime import UTC, datetime

import pytest

from domain import AlertLevel, Event, EventStatus


@pytest.fixture(autouse=True)
def reset_event_id_counter():
    """
    Reset Event ID counter before each test.

    This ensures predictable and isolated test behavior.
    """
    Event.reset_id_counter()
    yield
    # Cleanup after test (optional)
    Event.reset_id_counter()


@pytest.fixture
def fixed_timestamp():
    """Provide a fixed timezone-aware timestamp for testing."""
    return datetime(2026, 2, 7, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def sample_metadata():
    """Provide sample metadata for testing."""
    return {"endpoint": "/api/users", "status_code": 500, "latency_ms": 1500}


@pytest.fixture
def error_event(fixed_timestamp):
    """Create a sample ERROR event."""
    return Event.create(
        source="api-gateway",
        metadata={"error": "Connection timeout"},
        level=AlertLevel.ERROR,
        timestamp=fixed_timestamp,
    )


@pytest.fixture
def warning_event(fixed_timestamp):
    """Create a sample WARNING event."""
    return Event.create(
        source="database",
        metadata={"latency_ms": 2000},
        level=AlertLevel.WARNING,
        timestamp=fixed_timestamp,
    )


@pytest.fixture
def normal_event(fixed_timestamp):
    """Create a sample NORMAL event."""
    return Event.create(
        source="cron-job",
        metadata={"task": "backup"},
        level=AlertLevel.NORMAL,
        timestamp=fixed_timestamp,
    )


@pytest.fixture
def acknowledged_error_event(error_event):
    """Create an acknowledged ERROR event."""
    error_event.acknowledge()
    return error_event


@pytest.fixture
def acknowledged_warning_event(warning_event):
    """Create an acknowledged WARNING event."""
    warning_event.acknowledge()
    return warning_event

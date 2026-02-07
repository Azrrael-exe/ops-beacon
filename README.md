# Ops Beacon

> A lightweight event processor and CLI alert system for server
> operators.

Ops Beacon is an event-driven monitoring tool designed to help server
administrators focus only on what truly matters.\
It processes structured events and presents them in a prioritized CLI
stream, emitting persistent alerts for critical conditions until they
are acknowledged.

This project is an academic MVP focused on **Object-Oriented Programming
(OOP)** and **Clean Architecture principles**.

------------------------------------------------------------------------

# 🎯 Motivation

Modern systems generate a large volume of operational signals.\
However, not all events require the same level of attention.

Ops Beacon exists to:

-   Filter signal from noise
-   Prioritize critical events
-   Provide persistent alerts for actionable issues
-   Maintain a clean and extensible architecture

It runs on the operator's machine and acts as a focused event monitor.

------------------------------------------------------------------------

# 🚀 MVP Features

## Event Processing

Ops Beacon processes structured domain events containing:

-   `source`
-   `metadata`
-   `level` → `Normal | Warning | Error`
-   `timestamp`
-   `status` → `New | Acknowledged`

Event ingestion is abstracted from the core logic.\
In this first stage, the focus is on processing and presentation, not on
transport mechanisms.

------------------------------------------------------------------------

## Event Behavior

  Level     Displayed   Requires ACK   Repeating Alert
  --------- ----------- -------------- -----------------
  Normal    Yes         No             No
  Warning   Yes         Yes            Yes
  Error     Yes         Yes            Yes

-   Events are stored in memory
-   Events are shown:
    -   Prioritized by level (Error \> Warning \> Normal)
    -   Ordered by arrival time within each level
-   Alerts repeat every configurable interval until acknowledged

------------------------------------------------------------------------

# ⚙️ How It Works

## 1️⃣ Event Reception

An event enters the system through an input adapter (abstracted in this
stage).\
The adapter translates external data into a valid `Event` domain object.

## 2️⃣ Domain Validation

The `Event` entity is created with:

-   Source
-   Metadata
-   Alert level
-   Timestamp
-   Initial status (`NEW`)

Domain rules enforce:

-   Normal events do not require acknowledgment
-   Warning and Error events require acknowledgment
-   Prioritization logic is deterministic and consistent

## 3️⃣ Storage

The event is persisted in a repository.

In the MVP: - The repository is in-memory - It respects the
`EventRepository` interface - It can be replaced later without affecting
business logic

## 4️⃣ Prioritization

When rendering events:

1.  Events are grouped by level:
    -   ERROR
    -   WARNING
    -   NORMAL
2.  Within each group, they are ordered by arrival time.

## 5️⃣ Alert Scheduling

If the event level is:

-   WARNING
-   ERROR

Then the alert subsystem is activated.

The alert:

-   Emits sound and/or visual signal
-   Repeats every configured interval
-   Stops only when the event is acknowledged

## 6️⃣ Operator Interaction

The operator interacts via CLI:

-   Views event stream
-   Identifies events requiring action
-   Executes `ack <event_id>` to acknowledge

Acknowledgment changes event status to `ACKNOWLEDGED`, which:

-   Stops the alert
-   Updates the display state

------------------------------------------------------------------------

# 🧠 Domain Model

## Core Entities

### Event

Represents a domain event emitted by an external system.

**Attributes:**

-   `id: int` - Auto-incremented unique identifier
-   `source: str` - Origin system or component (non-empty)
-   `metadata: dict` - Additional contextual information
-   `level: AlertLevel` - Severity level (NORMAL, WARNING, ERROR)
-   `timestamp: datetime` - When the event occurred (timezone-aware)
-   `status: EventStatus` - Lifecycle state (NEW, ACKNOWLEDGED)

**Methods:**

-   `Event.create()` - Factory method to create new events with auto-generated ID
-   `acknowledge()` - Transition event from NEW to ACKNOWLEDGED (only for WARNING/ERROR)
-   `requires_acknowledgment()` - Check if event requires acknowledgment
-   `needs_alert()` - Check if event should trigger an alert

**Example:**

```python
from domain import Event, AlertLevel

# Create an error event
event = Event.create(
    source="api-gateway",
    metadata={"endpoint": "/api/users", "error": "timeout"},
    level=AlertLevel.ERROR
)

# Check if it needs an alert
if event.needs_alert():
    print(f"Alert! Event {event.id} from {event.source}")

# Acknowledge the event
event.acknowledge()
```

### AlertLevel (Enum)

Enumeration of alert severity levels with priority ordering.

-   `NORMAL` - Informational events (no acknowledgment required)
-   `WARNING` - Issues requiring attention (acknowledgment required)
-   `ERROR` - Critical issues (acknowledgment required)

**Priority:** ERROR > WARNING > NORMAL

**Methods:**

-   `requires_acknowledgment()` - Returns True for WARNING and ERROR

### EventStatus (Enum)

Enumeration of event lifecycle states.

-   `NEW` - Initial state for all events
-   `ACKNOWLEDGED` - Event has been acknowledged by operator

**Transition:** NEW → ACKNOWLEDGED (one-way, no rollback)

**Methods:**

-   `is_new()` - Check if status is NEW
-   `is_acknowledged()` - Check if status is ACKNOWLEDGED

------------------------------------------------------------------------

# 🏗 Architecture

Ops Beacon follows **Clean Architecture** principles.

Dependencies always point inward.

presentation → application → domain ↓ infrastructure

------------------------------------------------------------------------

# 📁 Project Structure

``` bash
ops-beacon/
├── src/
│   ├── domain/                    # ✅ Implemented
│   │   ├── entities/              # Event entity
│   │   ├── enums/                 # AlertLevel, EventStatus
│   │   ├── exceptions/            # Domain exceptions
│   │   └── interfaces/            # EventRepository interface
│   ├── application/               # 🚧 TODO: Use cases
│   ├── infrastructure/            # 🚧 TODO: Repositories, adapters
│   └── presentation/              # 🚧 TODO: CLI interface
├── tests/
│   └── domain/                    # ✅ 32 tests (pytest)
│       ├── test_alert_level.py    # 10 tests
│       ├── test_event_status.py   # 6 tests
│       ├── test_event.py          # 16 tests
│       └── conftest.py
├── scripts/
│   └── test_domain.py             # Manual test script
├── pytest.ini                     # Pytest configuration
├── pyproject.toml                 # Project dependencies
└── README.md
```

------------------------------------------------------------------------

# ⚙️ Configuration

Ops Beacon uses a YAML configuration file.

Example:

``` yaml
alert:
  repeat_interval_seconds: 5
  enable_sound: true
  enable_visual: true

repository:
  type: in_memory
  max_events: 1000
```

------------------------------------------------------------------------

# 🎓 Academic Focus

This project emphasizes:

-   **Object-Oriented Programming** - Entities with behavior, not anemic models
-   **Clean Architecture** - Domain layer has zero external dependencies
-   **Repository Pattern** - Abstract persistence from business logic
-   **Dependency Inversion Principle** - Domain defines interfaces, infrastructure implements
-   **Separation of concerns** - Each layer has a single responsibility
-   **Extensibility through abstraction** - Easy to add new features
-   **Enums for domain constants** - Type-safe representation of fixed values
-   **Comprehensive testing** - 32 unit tests with pytest (focused on essential cases)

------------------------------------------------------------------------

# 🚀 Getting Started

## Prerequisites

-   Python 3.13+
-   [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ops-beacon.git
cd ops-beacon

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Running Tests

```bash
# Run all tests
pytest

# Run domain tests only
pytest tests/domain

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src/domain --cov-report=term-missing
```

## Development

```bash
# Install development dependencies
uv sync --dev

# Run manual test script
python scripts/test_domain.py
```

## Usage Example

```python
from datetime import datetime, UTC
from domain import Event, AlertLevel, EventStatus

# Create events
error_event = Event.create(
    source="database",
    metadata={"query": "SELECT * FROM users", "error": "timeout"},
    level=AlertLevel.ERROR
)

warning_event = Event.create(
    source="api-gateway",
    metadata={"latency_ms": 2000},
    level=AlertLevel.WARNING
)

# Check if events need alerts
print(f"Error event needs alert: {error_event.needs_alert()}")  # True
print(f"Error event requires ACK: {error_event.requires_acknowledgment()}")  # True

# Acknowledge events
error_event.acknowledge()
print(f"After ACK, needs alert: {error_event.needs_alert()}")  # False

# Events are sortable by priority
events = [warning_event, error_event]
sorted_events = sorted(events)  # ERROR comes first
```

------------------------------------------------------------------------

# 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.


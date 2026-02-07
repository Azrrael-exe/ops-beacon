"""Tests simplificados para Event entity - Enfoque educativo."""

from datetime import UTC, datetime, timedelta

import pytest

from domain import (
    AlertLevel,
    Event,
    EventStatus,
    InvalidEventStateError,
    InvalidEventTransitionError,
)


class TestEventBasics:
    """Tests básicos de creación y atributos de Event."""

    def test_create_event_simple(self):
        """Test más simple: crear un evento."""
        event = Event.create(
            source="api-gateway",
            metadata={"error": "timeout"},
            level=AlertLevel.ERROR,
        )

        # Verificar que se creó correctamente
        assert event.id == 1
        assert event.source == "api-gateway"
        assert event.level == AlertLevel.ERROR
        assert event.status == EventStatus.NEW

    def test_event_ids_auto_increment(self):
        """Test que los IDs se auto-incrementan."""
        event1 = Event.create("src1", {}, AlertLevel.ERROR)
        event2 = Event.create("src2", {}, AlertLevel.WARNING)
        event3 = Event.create("src3", {}, AlertLevel.NORMAL)

        assert event1.id == 1
        assert event2.id == 2
        assert event3.id == 3


class TestEventValidation:
    """Tests de validación - qué NO se puede hacer."""

    def test_source_cannot_be_empty(self):
        """Test que source no puede estar vacío."""
        with pytest.raises(InvalidEventStateError, match="source cannot be empty"):
            Event.create(
                source="",  # ❌ Vacío no válido
                metadata={},
                level=AlertLevel.ERROR,
            )

    def test_timestamp_must_have_timezone(self):
        """Test que timestamp debe tener timezone."""
        naive_time = datetime(2026, 1, 1)  # Sin timezone

        with pytest.raises(
            InvalidEventStateError, match="timestamp must be timezone-aware"
        ):
            Event.create(
                source="test",
                metadata={},
                level=AlertLevel.ERROR,
                timestamp=naive_time,  # ❌ Sin timezone
            )


class TestEventAcknowledgment:
    """Tests de acknowledgment - regla de negocio principal."""

    def test_acknowledge_error_event(self):
        """Test acknowledge de evento ERROR - caso happy path."""
        event = Event.create("api", {}, AlertLevel.ERROR)

        # Antes de acknowledge
        assert event.status == EventStatus.NEW

        # Acknowledge
        event.acknowledge()

        # Después de acknowledge
        assert event.status == EventStatus.ACKNOWLEDGED

    def test_acknowledge_warning_event(self):
        """Test acknowledge de evento WARNING."""
        event = Event.create("db", {}, AlertLevel.WARNING)

        event.acknowledge()

        assert event.status == EventStatus.ACKNOWLEDGED

    def test_cannot_acknowledge_normal_event(self):
        """Test que eventos NORMAL NO pueden ser acknowledged - regla importante."""
        event = Event.create("cron", {}, AlertLevel.NORMAL)

        with pytest.raises(
            InvalidEventTransitionError, match="Cannot acknowledge NORMAL"
        ):
            event.acknowledge()  # ❌ NORMAL no se puede acknowledge

        # Status debe seguir siendo NEW
        assert event.status == EventStatus.NEW


class TestEventAlerts:
    """Tests de lógica de alertas."""

    def test_error_event_needs_alert_when_new(self):
        """Test que evento ERROR necesita alerta cuando está NEW."""
        event = Event.create("api", {}, AlertLevel.ERROR)

        assert event.needs_alert() is True  # ✅ Debe alertar

    def test_error_event_does_not_need_alert_after_ack(self):
        """Test que evento ERROR NO necesita alerta después de acknowledge."""
        event = Event.create("api", {}, AlertLevel.ERROR)

        event.acknowledge()

        assert event.needs_alert() is False  # ✅ Ya no alerta

    def test_normal_event_never_needs_alert(self):
        """Test que eventos NORMAL nunca necesitan alerta."""
        event = Event.create("cron", {}, AlertLevel.NORMAL)

        assert event.needs_alert() is False  # ✅ NORMAL nunca alerta


class TestEventSorting:
    """Tests de ordenamiento por prioridad."""

    def test_events_sort_by_priority(self):
        """Test que eventos se ordenan: ERROR > WARNING > NORMAL."""
        # Crear eventos en orden aleatorio
        normal = Event.create("src1", {}, AlertLevel.NORMAL)
        error = Event.create("src2", {}, AlertLevel.ERROR)
        warning = Event.create("src3", {}, AlertLevel.WARNING)

        # Ordenar
        events = [normal, warning, error]
        sorted_events = sorted(events)

        # Verificar orden correcto
        assert sorted_events[0].level == AlertLevel.ERROR  # 1° ERROR
        assert sorted_events[1].level == AlertLevel.WARNING  # 2° WARNING
        assert sorted_events[2].level == AlertLevel.NORMAL  # 3° NORMAL

    def test_events_with_same_level_sort_by_time(self):
        """Test que eventos con mismo nivel se ordenan por timestamp."""
        base_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)

        # Crear 3 eventos ERROR en diferentes tiempos
        event1 = Event.create("s1", {}, AlertLevel.ERROR, base_time)
        event2 = Event.create(
            "s2", {}, AlertLevel.ERROR, base_time + timedelta(seconds=10)
        )
        event3 = Event.create(
            "s3", {}, AlertLevel.ERROR, base_time + timedelta(seconds=5)
        )

        # Ordenar
        events = [event2, event3, event1]
        sorted_events = sorted(events)

        # Más antiguo primero
        assert sorted_events[0] == event1  # 12:00:00
        assert sorted_events[1] == event3  # 12:00:05
        assert sorted_events[2] == event2  # 12:00:10


class TestEventEquality:
    """Tests de igualdad basada en ID."""

    def test_events_with_same_id_are_equal(self):
        """Test que eventos con mismo ID son iguales."""
        time = datetime.now(UTC)

        event1 = Event(
            id=1, source="src1", metadata={}, level=AlertLevel.ERROR, timestamp=time
        )
        event2 = Event(
            id=1,  # Mismo ID
            source="src2",  # Diferente source
            metadata={},
            level=AlertLevel.WARNING,  # Diferente level
            timestamp=time,
        )

        # Mismo ID = iguales
        assert event1 == event2

    def test_events_with_different_ids_are_not_equal(self):
        """Test que eventos con diferentes IDs NO son iguales."""
        time = datetime.now(UTC)

        event1 = Event(
            id=1, source="src", metadata={}, level=AlertLevel.ERROR, timestamp=time
        )
        event2 = Event(
            id=2,  # Diferente ID
            source="src",
            metadata={},
            level=AlertLevel.ERROR,
            timestamp=time,
        )

        assert event1 != event2


class TestEventUsage:
    """Tests de casos de uso reales - ejemplos prácticos."""

    def test_complete_event_lifecycle(self):
        """Test del ciclo de vida completo de un evento."""
        # 1. Sistema detecta un error
        event = Event.create(
            source="database",
            metadata={"query": "SELECT * FROM users", "error": "timeout"},
            level=AlertLevel.ERROR,
        )

        # 2. Verificar que necesita atención
        assert event.requires_acknowledgment() is True
        assert event.needs_alert() is True

        # 3. Operador ve la alerta y acknowledges
        event.acknowledge()

        # 4. Verificar que ya no necesita alerta
        assert event.status == EventStatus.ACKNOWLEDGED
        assert event.needs_alert() is False

    def test_prioritize_multiple_events(self):
        """Test de priorización de múltiples eventos - caso real."""
        # Sistema recibe varios eventos
        events = [
            Event.create("cron", {"task": "backup"}, AlertLevel.NORMAL),
            Event.create("api", {"latency": 2000}, AlertLevel.WARNING),
            Event.create("db", {"error": "connection"}, AlertLevel.ERROR),
            Event.create("cache", {"miss_rate": 0.9}, AlertLevel.WARNING),
        ]

        # Ordenar por prioridad
        prioritized = sorted(events)

        # Verificar que ERROR está primero
        assert prioritized[0].level == AlertLevel.ERROR
        assert prioritized[0].source == "db"

        # Seguido por WARNINGs
        assert prioritized[1].level == AlertLevel.WARNING
        assert prioritized[2].level == AlertLevel.WARNING

        # NORMAL al final
        assert prioritized[3].level == AlertLevel.NORMAL
        assert prioritized[3].source == "cron"

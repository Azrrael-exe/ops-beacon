"""Tests simplificados para EventStatus enum - Enfoque educativo."""

import pytest

from domain.enums.event_status import EventStatus


class TestEventStatusBasics:
    """Tests básicos de EventStatus enum."""

    def test_event_statuses_exist(self):
        """Test que ambos estados existen."""
        assert EventStatus.NEW
        assert EventStatus.ACKNOWLEDGED

    def test_statuses_are_different(self):
        """Test que cada estado es único."""
        assert EventStatus.NEW != EventStatus.ACKNOWLEDGED


class TestStatusHelpers:
    """Tests de métodos helper - is_new() y is_acknowledged()."""

    def test_new_status_is_new(self):
        """Test que NEW es identificado como new."""
        status = EventStatus.NEW

        assert status.is_new() is True
        assert status.is_acknowledged() is False

    def test_acknowledged_status_is_acknowledged(self):
        """Test que ACKNOWLEDGED es identificado como acknowledged."""
        status = EventStatus.ACKNOWLEDGED

        assert status.is_acknowledged() is True
        assert status.is_new() is False


class TestEventStatusUsage:
    """Tests de uso práctico de EventStatus."""

    def test_check_if_event_needs_processing(self):
        """Test ejemplo: verificar si evento necesita procesamiento."""
        # Simular eventos con diferentes status
        new_status = EventStatus.NEW
        ack_status = EventStatus.ACKNOWLEDGED

        # Solo procesar eventos NEW
        if new_status.is_new():
            needs_processing = True
        else:
            needs_processing = False

        assert needs_processing is True

        # Eventos acknowledged no necesitan procesamiento
        if ack_status.is_new():
            needs_processing_2 = True
        else:
            needs_processing_2 = False

        assert needs_processing_2 is False

    def test_filter_new_events(self):
        """Test ejemplo: filtrar solo eventos NEW."""
        # Lista de status mezclados
        statuses = [
            EventStatus.NEW,
            EventStatus.ACKNOWLEDGED,
            EventStatus.NEW,
            EventStatus.ACKNOWLEDGED,
            EventStatus.NEW,
        ]

        # Filtrar solo NEW
        new_statuses = [s for s in statuses if s.is_new()]

        assert len(new_statuses) == 3
        assert all(s == EventStatus.NEW for s in new_statuses)

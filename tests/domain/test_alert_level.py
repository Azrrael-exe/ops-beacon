"""Tests simplificados para AlertLevel enum - Enfoque educativo."""

import pytest

from domain.enums.alert_level import AlertLevel


class TestAlertLevelBasics:
    """Tests básicos de AlertLevel enum."""

    def test_alert_levels_exist(self):
        """Test que todos los niveles de alerta existen."""
        # Los 3 niveles deben existir
        assert AlertLevel.NORMAL
        assert AlertLevel.WARNING
        assert AlertLevel.ERROR

    def test_alert_levels_are_different(self):
        """Test que cada nivel es único."""
        assert AlertLevel.NORMAL != AlertLevel.WARNING
        assert AlertLevel.WARNING != AlertLevel.ERROR
        assert AlertLevel.ERROR != AlertLevel.NORMAL


class TestRequiresAcknowledgment:
    """Tests de la regla de negocio: ¿requiere acknowledgment?"""

    def test_normal_does_not_require_ack(self):
        """Test que NORMAL NO requiere acknowledgment."""
        assert AlertLevel.NORMAL.requires_acknowledgment() is False

    def test_warning_requires_ack(self):
        """Test que WARNING requiere acknowledgment."""
        assert AlertLevel.WARNING.requires_acknowledgment() is True

    def test_error_requires_ack(self):
        """Test que ERROR requiere acknowledgment."""
        assert AlertLevel.ERROR.requires_acknowledgment() is True


class TestAlertLevelPriority:
    """Tests de prioridad - ERROR > WARNING > NORMAL."""

    def test_error_has_higher_priority_than_warning(self):
        """Test que ERROR tiene mayor prioridad que WARNING."""
        assert AlertLevel.ERROR < AlertLevel.WARNING

    def test_warning_has_higher_priority_than_normal(self):
        """Test que WARNING tiene mayor prioridad que NORMAL."""
        assert AlertLevel.WARNING < AlertLevel.NORMAL

    def test_error_has_highest_priority(self):
        """Test que ERROR tiene la mayor prioridad de todas."""
        assert AlertLevel.ERROR < AlertLevel.WARNING
        assert AlertLevel.ERROR < AlertLevel.NORMAL

    def test_sorting_by_priority(self):
        """Test que los niveles se ordenan correctamente."""
        # Crear lista desordenada
        levels = [
            AlertLevel.NORMAL,
            AlertLevel.ERROR,
            AlertLevel.WARNING,
            AlertLevel.NORMAL,
            AlertLevel.ERROR,
        ]

        # Ordenar
        sorted_levels = sorted(levels)

        # Verificar orden: ERROR primero, luego WARNING, luego NORMAL
        assert sorted_levels[0] == AlertLevel.ERROR
        assert sorted_levels[1] == AlertLevel.ERROR
        assert sorted_levels[2] == AlertLevel.WARNING
        assert sorted_levels[3] == AlertLevel.NORMAL
        assert sorted_levels[4] == AlertLevel.NORMAL


class TestAlertLevelUsage:
    """Tests de uso práctico de AlertLevel."""

    def test_filter_events_requiring_ack(self):
        """Test ejemplo: filtrar niveles que requieren acknowledgment."""
        all_levels = [AlertLevel.NORMAL, AlertLevel.WARNING, AlertLevel.ERROR]

        # Filtrar solo los que requieren ack
        requires_ack = [
            level for level in all_levels if level.requires_acknowledgment()
        ]

        # Solo WARNING y ERROR
        assert len(requires_ack) == 2
        assert AlertLevel.WARNING in requires_ack
        assert AlertLevel.ERROR in requires_ack
        assert AlertLevel.NORMAL not in requires_ack

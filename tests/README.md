# Tests

Suite de tests para Ops Beacon usando pytest.

## Estructura

```
tests/
├── __init__.py
└── domain/
    ├── __init__.py
    ├── conftest.py              # Fixtures compartidos
    ├── test_alert_level.py      # 10 tests para AlertLevel enum
    ├── test_event_status.py     # 6 tests para EventStatus enum
    └── test_event.py            # 16 tests para Event entity
```

## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Tests de dominio solamente
```bash
pytest tests/domain
```

### Test específico
```bash
pytest tests/domain/test_event.py
```

### Con verbose output
```bash
pytest -v
```

### Con coverage
```bash
pytest --cov=src/domain --cov-report=term-missing
```

## Cobertura de Tests (32 tests total)

### AlertLevel Enum (10 tests)
- ✅ Valores del enum (NORMAL, WARNING, ERROR)
- ✅ Método `requires_acknowledgment()`
- ✅ Comparación de prioridades (`__lt__`)
- ✅ Sorting por prioridad
- ✅ Uso práctico (filtrar por ACK requerido)

### EventStatus Enum (6 tests)
- ✅ Valores del enum (NEW, ACKNOWLEDGED)
- ✅ Métodos helper (`is_new()`, `is_acknowledged()`)
- ✅ Uso práctico (filtrar eventos, verificar procesamiento)

### Event Entity (16 tests)
- ✅ Creación con factory method
- ✅ Auto-incremento de IDs
- ✅ Validaciones (source, timestamp)
- ✅ Acknowledgment (WARNING/ERROR sí, NORMAL no)
- ✅ Lógica de alertas (`needs_alert()`)
- ✅ Sorting por prioridad y timestamp
- ✅ Equality basada en ID
- ✅ Casos de uso completos

## Fixtures (conftest.py)

### Fixtures Automáticos
- `reset_event_id_counter`: Resetea el contador de IDs antes de cada test (autouse=True)

### Fixtures de Datos
- `fixed_timestamp`: Timestamp fijo para tests determinísticos
- `sample_metadata`: Metadata de ejemplo

### Fixtures de Eventos
- `error_event`: Evento ERROR sin acknowledge
- `warning_event`: Evento WARNING sin acknowledge
- `normal_event`: Evento NORMAL
- `acknowledged_error_event`: Evento ERROR acknowledged
- `acknowledged_warning_event`: Evento WARNING acknowledged

## Filosofía de Testing

Los tests están diseñados con enfoque **educativo y práctico**:

✅ **Simples y claros** - Código fácil de entender
✅ **Casos esenciales** - Cubren las reglas de negocio principales
✅ **Nombres descriptivos** - Autoexplicativos
✅ **Comentarios educativos** - Explican el "por qué"
✅ **Casos de uso reales** - Ejemplos prácticos

## Ejemplo de Test

```python
def test_acknowledge_error_event(self):
    """Test acknowledge de evento ERROR - caso happy path."""
    event = Event.create("api", {}, AlertLevel.ERROR)

    # Antes de acknowledge
    assert event.status == EventStatus.NEW

    # Acknowledge
    event.acknowledge()

    # Después de acknowledge
    assert event.status == EventStatus.ACKNOWLEDGED
```

## Organización de Tests

Los tests están organizados en clases por concepto:

```python
class TestEventBasics:
    """Tests básicos de creación y atributos."""

class TestEventValidation:
    """Tests de validación - qué NO se puede hacer."""

class TestEventAcknowledgment:
    """Tests de acknowledgment - regla de negocio principal."""
```

## Comandos Útiles

```bash
# Ejecutar por clase
pytest tests/domain/test_event.py::TestEventBasics -v

# Ejecutar test específico
pytest tests/domain/test_event.py::TestEventBasics::test_create_event_simple -v

# Buscar por keyword
pytest tests/domain -k "acknowledge" -v

# Ver colección sin ejecutar
pytest tests/domain --collect-only -q
```

## Agregar Nuevos Tests

1. Identificar el concepto a testear
2. Agregar test en la clase apropiada
3. Usar fixtures existentes cuando sea posible
4. Seguir el patrón Arrange-Act-Assert
5. Agregar docstring explicativo

```python
def test_my_new_feature(self, error_event):
    """Test de mi nueva funcionalidad."""
    # Arrange - preparar
    initial_value = error_event.some_property

    # Act - ejecutar
    error_event.do_something()

    # Assert - verificar
    assert error_event.some_property != initial_value
```

## Best Practices Implementadas

- ✅ Un concepto por test
- ✅ Tests independientes y aislados
- ✅ Usar fixtures para setup común
- ✅ Nombres descriptivos y autoexplicativos
- ✅ Probar casos happy path y error cases
- ✅ Documentar con docstrings claros

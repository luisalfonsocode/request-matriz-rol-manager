# Guía de Testing

## Framework de Testing

Usamos pytest como framework principal de testing.

## Estructura de Tests

```
tests/
├── test_gui/        # Tests de interfaz
├── test_core/       # Tests del núcleo
└── conftest.py      # Configuración común
```

## Tipos de Tests

1. **Tests Unitarios**
   - Un componente a la vez
   - Mocks para dependencias
   - Rápidos y aislados

2. **Tests de Integración**
   - Múltiples componentes
   - Verificar interacciones
   - Más lentos pero realistas

3. **Tests GUI**
   - Interfaz gráfica
   - Simulación de eventos
   - Validación de flujos

## Escribir Tests

1. **Nombrado**:
   ```python
   def test_nombre_descriptivo():
       ...
   ```

2. **Estructura AAA**:
   ```python
   def test_ejemplo():
       # Arrange
       dato = preparar_dato()

       # Act
       resultado = procesar(dato)

       # Assert
       assert resultado == esperado
   ```

3. **Fixtures**:
   ```python
   @pytest.fixture
   def setup_común():
       # Preparación
       yield objeto
       # Limpieza
   ```

## Ejecutar Tests

1. **Todos los tests**:
   ```bash
   pytest
   ```

2. **Con cobertura**:
   ```bash
   pytest --cov=src
   ```

3. **Tests específicos**:
   ```bash
   pytest tests/test_específico.py
   ```

## Buenas Prácticas

1. **Aislamiento**
   - Cada test independiente
   - Usar fixtures
   - Limpiar recursos

2. **Assertions**
   - Mensajes claros
   - Verificar casos borde
   - Usar helpers de pytest

3. **Mocks**
   - Simular externos
   - Verificar llamadas
   - No abusar

## Integración Continua

Los tests se ejecutan en:
1. Pre-commit
2. Pull Requests
3. Merge a main

## Referencias

- [Documentación pytest](https://docs.pytest.org/)
- [Guía de buenas prácticas](https://docs.pytest.org/en/stable/goodpractices.html)
- [Plugin de cobertura](https://pytest-cov.readthedocs.io/)

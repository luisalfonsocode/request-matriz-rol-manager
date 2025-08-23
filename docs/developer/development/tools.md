# Herramientas de Desarrollo

[Ver configuración detallada](../../reference/DEVELOPMENT_TOOLS.md)

## Herramientas Principales

1. **Formateo**
   - Black: Formateo automático
   - isort: Ordenamiento de imports

2. **Linting**
   - Flake8: Verificación PEP 8
   - Pylint: Análisis estático
   - Ruff: Linting rápido

3. **Testing**
   - pytest: Framework de pruebas
   - coverage: Cobertura de código

4. **Pre-commit**
   - Verificaciones automáticas
   - Hooks configurados

## Configuración Local

1. **Instalar herramientas**:
   ```bash
   pip install -r requirements/dev.txt
   ```

2. **Configurar pre-commit**:
   ```bash
   pre-commit install
   ```

3. **Verificar instalación**:
   ```bash
   black --version
   flake8 --version
   pytest --version
   ```

## Uso Diario

1. **Antes de commit**:
   ```bash
   # Formatear código
   black .

   # Verificar tipos
   mypy .

   # Ejecutar tests
   pytest
   ```

2. **Pre-commit automático**:
   - Se ejecuta en cada commit
   - Verifica formato y estilo
   - Ejecuta tests básicos

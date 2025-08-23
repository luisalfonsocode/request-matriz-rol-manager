# Herramientas de Desarrollo

Este documento describe las herramientas de desarrollo utilizadas en el proyecto y cómo se configuran.

## Herramientas de Formateo

### Black

Black es un formateador de código Python que no requiere configuración. Aplica un estilo consistente automáticamente.

```bash
# Formatear archivos
black src/ tests/

# Verificar sin cambiar
black --check src/ tests/
```

**Configuración**:
- Longitud de línea: 88 caracteres
- Python 3.9+
- Ver configuración en `pyproject.toml`

### isort

Ordena y formatea las importaciones automáticamente, siguiendo las convenciones de PEP 8.

```bash
# Ordenar importaciones
isort src/ tests/

# Verificar sin cambiar
isort --check-only src/ tests/
```

**Configuración**:
- Perfil: black (para compatibilidad)
- Longitud de línea: 88 caracteres
- Ver configuración en `pyproject.toml`

## Linters y Análisis Estático

### Flake8

Verifica el cumplimiento de PEP 8 y encuentra errores comunes.

```bash
# Ejecutar flake8
flake8 src/ tests/
```

**Plugins instalados**:
- flake8-docstrings: Verifica docstrings
- flake8-quotes: Verifica uso consistente de comillas

### Pylint

Análisis estático más completo que flake8.

```bash
# Ejecutar pylint
pylint src/ tests/
```

**Características**:
- Detecta errores de código
- Verifica convenciones de estilo
- Sugiere refactorizaciones
- Ver configuración en `setup.cfg`

### Mypy

Verifica anotaciones de tipos estáticos.

```bash
# Ejecutar mypy
mypy src/ tests/
```

**Configuración**:
- Modo estricto
- Verifica imports faltantes
- Ver configuración en `mypy.ini`

### Ruff

Linter ultra rápido que combina múltiples herramientas.

```bash
# Ejecutar ruff
ruff check src/ tests/
```

**Características**:
- Más rápido que flake8/pylint
- Incluye múltiples reglas
- Auto-fijado de problemas
- Ver configuración en `pyproject.toml`

## Pre-commit

### Configuración

Pre-commit ejecuta verificaciones automáticas antes de cada commit.

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files

# Actualizar a últimas versiones
pre-commit autoupdate
```

**Hooks configurados**:
1. black: Formateo de código
2. isort: Ordenamiento de importaciones
3. flake8: Verificación de estilo
4. mypy: Verificación de tipos

Ver configuración completa en `.pre-commit-config.yaml`

### Uso

Los hooks se ejecutan automáticamente al hacer commit:
```bash
git add .
git commit -m "mensaje"
```

Si alguna verificación falla:
1. Se muestran los errores
2. Se deben corregir los problemas
3. Añadir los cambios (`git add`)
4. Intentar el commit nuevamente

## Seguridad

### Bandit

Análisis de seguridad del código Python.

```bash
# Ejecutar bandit
bandit -r src/
```

**Verifica**:
- Vulnerabilidades conocidas
- Problemas de seguridad comunes
- Malas prácticas de seguridad

### Safety

Verifica vulnerabilidades en dependencias.

```bash
# Verificar dependencias
safety check
```

## Testing

### Pytest

Framework principal de testing.

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src

# Tests específicos
pytest tests/test_specific.py
```

**Plugins**:
- pytest-cov: Reportes de cobertura
- pytest-mock: Mocking
- pytest-asyncio: Tests asíncronos
- Ver más en `requirements/test.txt`

## Documentación

### Sphinx

Generador de documentación.

```bash
# Generar documentación
cd docs/
make html
```

### MkDocs

Alternativa a Sphinx, más moderna.

```bash
# Servidor de desarrollo
mkdocs serve

# Construir sitio
mkdocs build
```

## VS Code

### Extensiones Requeridas

Ver `docs/VSCODE_CONFIG.md` para:
- Lista de extensiones
- Configuración recomendada
- Atajos de teclado útiles

### Integración

VS Code se integra con todas las herramientas:
- Formateo al guardar (black, isort)
- Linting en tiempo real (flake8, pylint)
- Verificación de tipos (mypy)
- Debugging de tests (pytest)

## Scripts de Utilidad

### scripts/mantener.py

Script que ejecuta todas las verificaciones:

```bash
python scripts/mantener.py
```

**Ejecuta**:
1. Formateo de código
2. Linters
3. Tests
4. Verificación de seguridad

## Referencias

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Pytest Documentation](https://docs.pytest.org/)

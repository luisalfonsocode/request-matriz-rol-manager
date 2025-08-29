# Configuración de Herramientas de Desarrollo

Este directorio contiene las configuraciones completas de las herramientas de desarrollo:

## Archivos de Configuración:

### `pyproject.toml`
- Configuración de Black (formateador)
- Configuración de isort (ordenador de imports)
- Configuración de build system

### `setup.cfg`
- Configuración de flake8 (linter)
- Configuración de isort (backup)
- Configuración de coverage

### `mypy.ini`
- Configuración completa de mypy (type checker)
- Reglas de verificación de tipos
- Exclusiones y configuraciones específicas

## Uso:

Para usar estas configuraciones desde la raíz del proyecto:

```bash
# Black con configuración específica
black --config config/tools/pyproject.toml src/

# Flake8 con configuración específica
flake8 --config config/tools/setup.cfg src/

# MyPy con configuración específica
mypy --config-file config/tools/mypy.ini src/
```

## Archivos en Raíz:

Los archivos en la raíz (`pyproject.toml`, `setup.cfg`, `mypy.ini`) son versiones mínimas que permiten que las herramientas funcionen desde la raíz pero derivan la configuración completa de estos archivos.

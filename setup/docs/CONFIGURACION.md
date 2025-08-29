# ⚙️ Configuración Avanzada - Matriz de Rol

## 🎯 Descripción General

Esta guía describe configuraciones avanzadas y personalizaciones para desarrolladores y usuarios técnicos del sistema Matriz de Rol.

## 🔧 Configuración del Entorno de Desarrollo

### Variables de Entorno

El archivo `.env` contiene la configuración principal:

```bash
# Configuración del Entorno - Matriz de Rol
PROJECT_ROOT=F:\ws\utilitarios-matriz-de-rol
VENV_DIR=F:\ws\utilitarios-matriz-de-rol\venv
PYTHON_EXE=F:\ws\utilitarios-matriz-de-rol\venv\Scripts\python.exe
PYTHON_VERSION=3.11.5
SETUP_DATE=2024-01-XX XX:XX:XX
LOG_FILE=F:\ws\utilitarios-matriz-de-rol\setup\logs\setup.log
SETUP_MODE=PowerShell
```

### Configuración Personalizada

Puedes modificar estas variables según tus necesidades:

```bash
# Ejemplo de configuración personalizada
PROJECT_ROOT=C:\MiUbicacion\matriz-rol
VENV_DIR=C:\Entornos\matriz-rol-env
DEBUG_MODE=True
LOG_LEVEL=DEBUG
```

## 🐍 Configuración de Python

### Versiones Compatibles

| Versión Python | Estado        | Notas              |
| -------------- | ------------- | ------------------ |
| 3.9.x          | ✅ Soportado   | Versión mínima     |
| 3.10.x         | ✅ Recomendado | Óptimo rendimiento |
| 3.11.x         | ✅ Recomendado | Mejor performance  |
| 3.12.x         | ✅ Compatible  | Última versión     |

### Configuración de Múltiples Versiones

```bash
# Usar launcher de Python (Windows)
py -3.9 --version
py -3.10 --version
py -3.11 --version

# Crear entorno con versión específica
py -3.11 -m venv venv_311
py -3.10 -m venv venv_310

# Configurar instalador para usar versión específica
set PYTHON_VERSION_PREFERENCE=3.11
```

### Optimización del Entorno Virtual

```bash
# Activar entorno
venv\Scripts\activate

# Actualizar herramientas básicas
python -m pip install --upgrade pip setuptools wheel

# Instalar dependencias optimizadas
pip install --upgrade --prefer-binary -r requirements.txt

# Verificar instalación
pip check
```

## 📦 Gestión de Dependencias

### Archivos de Requisitos

```
requirements/
├── base.txt          # Dependencias base
├── dev.txt           # Herramientas de desarrollo
├── test.txt          # Dependencias de testing
└── optional.txt      # Dependencias opcionales
```

#### base.txt
```
# Dependencias principales
tkinter-tooltip>=2.0.0
Pillow>=9.0.0
python-dateutil>=2.8.0
```

#### dev.txt
```
-r base.txt
# Herramientas de desarrollo
black>=22.0.0
isort>=5.10.0
flake8>=4.0.0
mypy>=0.950
pytest>=7.0.0
```

#### test.txt
```
-r base.txt
# Testing
pytest>=7.0.0
pytest-cov>=3.0.0
pytest-mock>=3.7.0
coverage>=6.0.0
```

### Instalación por Perfil

```bash
# Instalación básica
pip install -r requirements/base.txt

# Instalación para desarrollo
pip install -r requirements/dev.txt

# Instalación para testing
pip install -r requirements/test.txt

# Instalación completa
pip install -r requirements/dev.txt -r requirements/test.txt
```

### Gestión de Versiones

```bash
# Generar requirements.txt actual
pip freeze > requirements_current.txt

# Comparar con requisitos base
fc requirements.txt requirements_current.txt

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Verificar compatibilidad
pip check
```

## 🛠️ Configuración de Herramientas de Desarrollo

### Black (Formateador)

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  | dist
  | .git
  | .mypy_cache
  | .tox
  | .venv
  | _build
  | buck-out
  | build
)/
'''
```

### isort (Ordenar Importaciones)

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

### Flake8 (Linter)

```ini
# setup.cfg
[flake8]
max-line-length = 88
exclude = .git,__pycache__,docs/source/conf.py,old,build,dist
ignore = E203, E266, E501, W503, F403, F401
```

### mypy (Verificación de Tipos)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### pytest (Testing)

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]
```

## 🔧 Configuración del IDE

### VS Code

`.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

`.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Matriz de Rol",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/matriz_rol/gui/aplicacion_principal.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### PyCharm

```python
# Configuración en PyCharm
# File > Settings > Project > Python Interpreter
# Seleccionar: ./venv/Scripts/python.exe

# Code Style > Python
# Scheme: Black (instalar plugin Black)

# Tools > External Tools
# Agregar herramientas: black, isort, flake8
```

## 🔄 Scripts de Automatización

### Pre-commit Hooks

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

### Script de Desarrollo

`scripts/dev.bat`:
```batch
@echo off
echo Activando entorno de desarrollo...
call venv\Scripts\activate.bat

echo Verificando código...
black src/ tests/ --check
isort src/ tests/ --check-only
flake8 src/ tests/
mypy src/

echo Ejecutando tests...
pytest tests/ -v

echo Iniciando aplicación...
python -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
```

### Script de Construcción

`scripts/build.bat`:
```batch
@echo off
call venv\Scripts\activate.bat

echo Limpiando archivos previos...
rmdir /s /q build dist *.egg-info 2>nul

echo Formateando código...
black src/ tests/
isort src/ tests/

echo Verificando código...
flake8 src/ tests/
mypy src/

echo Ejecutando tests...
pytest tests/ --cov=src --cov-report=html

echo Construyendo paquete...
python setup.py sdist bdist_wheel

echo Build completado!
```

## 📊 Logging y Monitoreo

### Configuración de Logging

```python
# src/matriz_rol/config/logging_config.py
import logging
import logging.config
from pathlib import Path

def setup_logging(log_level="INFO"):
    """Configurar sistema de logging."""

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '[%(asctime)s] %(name)s:%(levelname)s: %(message)s'
            },
            'simple': {
                'format': '%(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': log_dir / 'matriz_rol.log',
                'mode': 'a',
            },
        },
        'loggers': {
            'matriz_rol': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False,
            },
        },
        'root': {
            'level': log_level,
            'handlers': ['console'],
        },
    }

    logging.config.dictConfig(config)
```

### Uso del Logging

```python
# En cualquier módulo
import logging

logger = logging.getLogger('matriz_rol.mi_modulo')

logger.debug("Información de debug")
logger.info("Información general")
logger.warning("Advertencia")
logger.error("Error no crítico")
logger.critical("Error crítico")
```

## 🔐 Seguridad y Permisos

### Configuración de Permisos

```bash
# Verificar permisos actuales
icacls "." /T /C

# Dar permisos completos al usuario actual
icacls "." /grant "%USERNAME%:(OI)(CI)F" /T

# Restringir permisos a administradores y usuario actual
icacls "." /inheritance:r /grant:r "%USERNAME%:(OI)(CI)F" /grant:r "Administrators:(OI)(CI)F" /T
```

### Variables de Entorno Sensibles

```bash
# .env.local (no versionar)
DATABASE_PASSWORD=secret_password
API_KEY=your_api_key_here
DEBUG_MODE=True

# Cargar en aplicación
from dotenv import load_dotenv
load_dotenv('.env.local')
```

## 📈 Optimización de Rendimiento

### Configuración de Python

```bash
# Variables de optimización
set PYTHONOPTIMIZE=1
set PYTHONDONTWRITEBYTECODE=1
set PYTHONHASHSEED=0

# Usar estas en scripts de producción
```

### Optimización de Importaciones

```python
# Importaciones lazy para mejorar tiempo de inicio
import importlib

def get_heavy_module():
    """Importar módulo pesado solo cuando se necesite."""
    return importlib.import_module('heavy_module')
```

### Configuración de Memoria

```python
# Configuración de garbage collection
import gc

# Optimizar recolección de basura
gc.set_threshold(700, 10, 10)

# Configurar en aplicación principal
```

## 🔧 Configuración de Red

### Proxy Configuration

```bash
# Variables de entorno para proxy
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
set NO_PROXY=localhost,127.0.0.1,.company.com

# Configurar pip para proxy
pip config set global.proxy http://proxy.company.com:8080
```

### Configuración de Timeouts

```python
# src/matriz_rol/config/network_config.py
NETWORK_CONFIG = {
    'connection_timeout': 30,  # segundos
    'read_timeout': 60,        # segundos
    'max_retries': 3,
    'backoff_factor': 0.3,
}
```

## 📦 Distribución y Empaquetado

### PyInstaller Configuration

```python
# build.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/matriz_rol/gui/aplicacion_principal.py'],
    pathex=[],
    binaries=[],
    datas=[('src/matriz_rol/resources', 'matriz_rol/resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MatrizDeRol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico'
)
```

### Script de Empaquetado

```bash
# scripts/package.bat
@echo off
call venv\Scripts\activate.bat

echo Limpiando builds anteriores...
rmdir /s /q build dist 2>nul

echo Creando ejecutable...
pyinstaller build.spec --clean

echo Copiando recursos adicionales...
xcopy /E /I setup\docs dist\docs\
xcopy /E /I resources dist\resources\

echo Empaquetado completado!
echo Ejecutable en: dist\MatrizDeRol.exe
```

---

## 🎯 Conclusión

Esta configuración avanzada permite:

- ✅ Entorno de desarrollo optimizado
- ✅ Herramientas de calidad de código
- ✅ Testing automatizado
- ✅ Logging detallado
- ✅ Distribución simplificada

Para configuraciones específicas adicionales, consulta los archivos de configuración individuales en el proyecto.

---

*Documentación de configuración avanzada - Sistema Matriz de Rol v3.0*

# Utilitarios para Matriz de Rol

Utilidades basadas en Python para la gestión de matrices de roles.

## Características

- Gestión de roles y permisos
- Validación de matrices de roles
- Soporte para jerarquías de roles
- Importación/exportación de datos
- Interfaz de línea de comandos (CLI)

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements/dev.txt  # Para desarrollo
pip install -r requirements/test.txt  # Para testing
```

## Configuración del Entorno de Desarrollo

1. Instalar extensiones de VS Code requeridas:
   - Python
   - Pylance
   - autoDocstring

2. Configurar el entorno:
   - Ver [Configuración de VS Code](docs/VSCODE_CONFIG.md) para la configuración del editor
   - Ver [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md) para detalles de las herramientas
   - Aplicar la configuración recomendada del workspace

## Uso

```python
from matriz_rol import MatrizRoles

# Crear una matriz de roles
matriz = MatrizRoles()

# Agregar roles y permisos
matriz.agregar_rol("admin", ["leer", "escribir", "eliminar"])
matriz.agregar_rol("editor", ["leer", "escribir"])
matriz.agregar_rol("viewer", ["leer"])

# Verificar permisos
tiene_permiso = matriz.verificar_permiso("editor", "escribir")  # True
```

## Desarrollo

### Estructura del Proyecto
```
utilitarios-matriz-de-rol/
├── src/                    # Código fuente
│   └── matriz_rol/        # Paquete principal
├── tests/                 # Tests
├── docs/                  # Documentación
├── requirements/          # Requisitos
└── scripts/              # Scripts de utilidad
```

### Documentación

- [Guía de Estilo PEP 8](docs/PEP8_GUIDE.md)
- [Guía de Type Hints](docs/TYPE_HINTS.md)
- [Guía de Docstrings](docs/DOCSTRINGS_GUIDE.md)
- [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md)

### Testing
```bash
pytest              # Ejecutar tests
pytest --cov=src    # Tests con cobertura
```

### Control de Calidad

Usar pre-commit para verificaciones automáticas:
```bash
pre-commit install    # Instalar hooks
pre-commit run -a     # Verificar todos los archivos
```

Ver [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md) para más detalles sobre:
- Formateo de código (black, isort)
- Linting (flake8, pylint, ruff)
- Verificación de tipos (mypy)
- Testing (pytest)
- Documentación (sphinx, mkdocs)

## Contribuir

1. Fork el repositorio
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Autor

Luis Alfonso - [luisalfonsocode](https://github.com/luisalfonsocode)

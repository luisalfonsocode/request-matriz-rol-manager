# Configuración del Entorno de Desarrollo

## Requisitos Previos

1. Python 3.9 o superior
2. Git
3. Visual Studio Code

## Pasos de Configuración

1. **Clonar Repositorio**:
   ```bash
   git clone https://github.com/luisalfonsocode/python-base.git
   cd python-base
   ```

2. **Crear Entorno Virtual**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   ```

3. **Instalar Dependencias**:
   ```bash
   pip install -r requirements/dev.txt
   pip install -r requirements/test.txt
   ```

4. **Configurar VS Code**:
   - Instalar extensiones recomendadas
   - Aplicar configuración del workspace
   - [Ver guía detallada](../../reference/VSCODE_CONFIG.md)

5. **Configurar Pre-commit**:
   ```bash
   pre-commit install
   ```

## Estructura del Proyecto

```
python-base/
├── src/              # Código fuente
├── tests/            # Tests
├── docs/             # Documentación
├── requirements/     # Requisitos
└── scripts/         # Scripts de utilidad
```

## Verificación

Ejecutar las siguientes comprobaciones:

1. **Entorno Python**:
   ```bash
   python --version
   pip list
   ```

2. **Tests**:
   ```bash
   pytest
   ```

3. **Linting**:
   ```bash
   flake8
   mypy .
   ```

## Problemas Comunes

1. **Conflictos de Dependencias**
   - Actualizar pip
   - Reinstalar requisitos

2. **Errores de Pre-commit**
   - Limpiar caché
   - Reinstalar hooks

3. **Problemas de VS Code**
   - Seleccionar intérprete correcto
   - Recargar ventana

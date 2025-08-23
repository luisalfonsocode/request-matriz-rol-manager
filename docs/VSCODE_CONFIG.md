# Configuración de VS Code para el Proyecto

Este documento describe la configuración de VS Code utilizada en el proyecto, incluyendo extensiones recomendadas y configuraciones específicas.

## Extensiones Requeridas

Las siguientes extensiones son necesarias para el desarrollo:

1. **Python** (ms-python.python)
   - Soporte básico para Python
   - IntelliSense y autocompletado
   - Debugging integrado

2. **Pylance** (ms-python.vscode-pylance)
   - Servidor de lenguaje Python mejorado
   - Análisis de tipos en tiempo real
   - Mejor rendimiento en autocompletado

3. **autoDocstring** (njpwerner.autodocstring)
   - Generación automática de docstrings
   - Soporte para estilo Google
   - Autocompletado de parámetros

## Configuración del Workspace

El archivo `.vscode/settings.json` contiene la siguiente configuración:

```jsonc
{
    // Configuración de Python
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",

    // Configuración de autoDocstring
    "autoDocstring.docstringFormat": "google",
    "autoDocstring.startOnNewLine": true,
    "autoDocstring.includeDescription": true,
    "autoDocstring.generateDocstringOnEnter": true,

    // Formateo automático
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--line-length",
        "88"
    ],

    // Linting
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=88"
    ],

    // Ruff (linter rápido)
    "ruff.enable": true,
    "ruff.format.args": [
        "--line-length=88"
    ],

    // Auto-organización de importaciones
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },

    // Configuración de verificación de tipos
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,

    // Resaltado de errores en tiempo real
    "editor.guides.bracketPairs": true,
    "editor.guides.indentation": true
}
```

## Explicación de la Configuración

### Python Base
- `python.defaultInterpreterPath`: Configura el intérprete de Python a usar (entorno virtual)

### Docstrings
- `autoDocstring.docstringFormat`: Usa el estilo Google para docstrings
- `autoDocstring.generateDocstringOnEnter`: Genera docstrings automáticamente

### Formateo de Código
- `editor.formatOnSave`: Formatea el código al guardar
- `python.formatting.provider`: Usa Black como formateador
- `python.formatting.blackArgs`: Configura longitud de línea a 88 caracteres

### Linting y Análisis
- `python.linting.enabled`: Activa el linting
- `python.linting.pylintEnabled`: Usa Pylint como linter principal
- `ruff.enable`: Activa Ruff para linting rápido

### Verificación de Tipos
- `python.analysis.typeCheckingMode`: Modo estricto de verificación
- `python.analysis.inlayHints`: Muestra sugerencias de tipos en el editor

## Atajos de Teclado Útiles

1. **Docstrings**
   - `"""` + Enter: Genera docstring automáticamente
   - Ctrl + Shift + 2: Genera docstring para la función actual

2. **Formateo**
   - Shift + Alt + F: Formatea el documento actual
   - Ctrl + S: Formatea al guardar (con la configuración actual)

3. **Navegación**
   - F12: Ir a definición
   - Alt + F12: Peek definición
   - Shift + F12: Ver referencias

## Integración con Herramientas

La configuración actual integra:
- Black para formateo
- Pylint para linting
- Ruff para análisis rápido
- mypy para verificación de tipos
- isort para ordenar importaciones

## Mantenimiento

Para mantener la configuración:
1. Guardar cambios en `.vscode/settings.json`
2. Actualizar este documento si se agregan nuevas configuraciones
3. Asegurarse de que todos los desarrolladores tengan las extensiones requeridas

## Troubleshooting

Problemas comunes y soluciones:

1. **El formateo no funciona**
   - Verificar que Black esté instalado: `pip install black`
   - Comprobar que la extensión de Python esté activa

2. **Docstrings no se generan**
   - Reinstalar la extensión autoDocstring
   - Verificar la configuración de `autoDocstring.docstringFormat`

3. **Linting no funciona**
   - Verificar que Pylint esté instalado
   - Comprobar la configuración de Python en VS Code

# Instrucciones para Agentes IA en utilitarios-matriz-de-rol

Este documento proporciona guías esenciales para agentes de IA trabajando en este código. El proyecto es una utilidad basada en Python para la gestión de matrices de roles.

## Estructura del Proyecto

El proyecto sigue una estructura moderna de Python:

```
utilitarios-matriz-de-rol/
├── src/                    # Directorio de código fuente
│   └── matriz_rol/        # Paquete principal
├── tests/                 # Archivos de pruebas
├── docs/                  # Documentación
├── requirements/          # Archivos de requisitos
│   ├── base.txt          # Dependencias base
│   ├── dev.txt           # Dependencias de desarrollo
│   └── test.txt          # Dependencias de pruebas
└── scripts/              # Scripts de utilidad
```

## Entorno de Desarrollo

### Configuración
1. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   ```

2. Instalar dependencias de desarrollo:
   ```bash
   pip install -r requirements/dev.txt
   ```

3. Configurar VS Code:
   - Ver la [guía de configuración de VS Code](../docs/VSCODE_CONFIG.md) para la configuración completa del editor
   - Instalar las extensiones requeridas
   - Aplicar la configuración recomendada

## Organización del Código

### Patrones Clave
- Usar importaciones absolutas dentro del proyecto
- Seguir las [guías de estilo PEP 8](../docs/PEP8_GUIDE.md) (ver guía detallada)
- Implementar [type hints](../docs/TYPE_HINTS.md) para todos los parámetros de funciones y valores de retorno
- Documentar clases y funciones usando [docstrings (estilo Google)](../docs/DOCSTRINGS_GUIDE.md)

### Ejemplo de Patrón
```python
from typing import List, Optional

def procesar_matriz(datos: List[dict], categoria: Optional[str] = None) -> dict:
    """Procesa los datos de la matriz de roles.

    Args:
        datos: Lista de diccionarios conteniendo datos de roles
        categoria: Filtro opcional de categoría

    Returns:
        Datos procesados de la matriz como diccionario
    """
    pass
```

## Pruebas

- Escribir pruebas en el directorio `tests/`
- Usar pytest como framework de pruebas
- Nombrar archivos de prueba con prefijo `test_`
- Agrupar pruebas por funcionalidad

## Documentación

- Mantener el README.md actualizado con instrucciones de configuración y uso
- Documentar decisiones arquitectónicas significativas
- Usar type hints y docstrings para documentación de código

## Control de Versiones

- Seguir commits convencionales (feat:, fix:, docs:, etc.)
- Crear ramas de características desde main
- Enviar cambios mediante pull requests

## Desarrollo Futuro

Áreas clave para implementación:
1. Funcionalidad central de procesamiento de matrices
2. Validación y sanitización de datos
3. Capacidades de importación/exportación
4. Interfaz de línea de comandos (CLI)
5. Integración con sistemas comunes de gestión de roles

---

Nota: Este es un conjunto inicial de instrucciones que evolucionará a medida que el proyecto crezca. Por favor, actualiza este documento conforme surjan nuevos patrones y convenciones.

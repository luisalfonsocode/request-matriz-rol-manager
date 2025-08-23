# Módulo de Interfaz Gráfica para Matrices de Rol

Este módulo proporciona una interfaz gráfica para la gestión de solicitudes de matrices de rol.

## Características

1. **Selección de Matrices**
   - Carga matrices desde archivo de configuración YAML
   - Permite selección múltiple
   - Muestra descripción de cada matriz

2. **Gestión de Grupos de Red**
   - Entrada de múltiples grupos
   - Validación contra el dominio
   - Confirmación para grupos no existentes

3. **Validaciones**
   - Verificación de selección de matrices
   - Validación de grupos de red
   - Confirmaciones de usuario

## Uso

```python
from matriz_rol.gui.solicitud_matriz import main
main()
```

## Configuración

Las matrices disponibles se configuran en `config/matrices.yaml`:

```yaml
matrices_rol:
  - nombre: "Matriz Básica"
    id: "BASIC"
    descripcion: "Matriz de roles básicos"
  - nombre: "Matriz Avanzada"
    id: "ADVANCED"
    descripcion: "Matriz de roles avanzados"
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest tests/test_gui_solicitud.py
```

Las pruebas cubren:
- Inicialización de componentes
- Selección/deselección de matrices
- Validación de grupos de red
- Validaciones de campos requeridos
- Procesamiento de entrada de grupos

## Documentación

- Cada clase y método incluye docstrings detallados
- Se siguen las convenciones de tipo PEP 484
- La documentación incluye ejemplos de uso

## Dependencias

- tkinter: Interfaz gráfica base
- customtkinter: Widgets modernos
- pyyaml: Manejo de configuración

## Desarrollo

Para contribuir:
1. Asegurar cobertura de pruebas
2. Seguir convenciones de tipo
3. Documentar cambios
4. Mantener compatibilidad con Windows AD

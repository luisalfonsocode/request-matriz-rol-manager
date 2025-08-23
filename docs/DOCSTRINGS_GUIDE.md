# Guía de Docstrings Estilo Google en Python

Los docstrings son cadenas de documentación que describen módulos, clases, funciones o métodos. El estilo Google es una convención popular que hace que la documentación sea fácil de leer tanto en el código como en la documentación generada.

## Estructura Básica

```python
def funcion_simple(parametro: str) -> bool:
    """Breve descripción de una línea.

    Descripción más detallada que puede
    ocupar múltiples líneas.

    Args:
        parametro: Descripción del parámetro

    Returns:
        Descripción de lo que devuelve
    """
    return True
```

## Ejemplos por Tipo

### 1. Docstring de Módulo
```python
"""
Este módulo maneja la gestión de roles y permisos.

Proporciona funcionalidades para:
    - Crear y modificar roles
    - Asignar permisos a roles
    - Verificar permisos de usuarios
"""

# imports y código del módulo...
```

### 2. Docstring de Clase
```python
class GestorRoles:
    """Clase que gestiona roles y permisos en el sistema.

    Esta clase proporciona métodos para crear roles,
    asignar permisos y verificar accesos.

    Attributes:
        roles: Diccionario que mapea nombres de roles a permisos
        usuarios: Diccionario que mapea IDs de usuario a roles

    Examples:
        >>> gestor = GestorRoles()
        >>> gestor.crear_rol("admin", ["leer", "escribir"])
        True
    """
```

### 3. Docstring de Método/Función
```python
def asignar_rol(self, usuario_id: str, rol: str) -> bool:
    """Asigna un rol específico a un usuario.

    Verifica si el rol existe y luego lo asigna al usuario
    especificado. Si el usuario ya tiene un rol, lo sobrescribe.

    Args:
        usuario_id: ID único del usuario
        rol: Nombre del rol a asignar

    Returns:
        bool: True si la asignación fue exitosa, False si el rol no existe

    Raises:
        ValueError: Si el usuario_id está vacío
        KeyError: Si el rol no existe en el sistema

    Examples:
        >>> gestor.asignar_rol("user123", "admin")
        True
    """
```

### 4. Docstring con Tipos Complejos
```python
from typing import Dict, List, Optional

def procesar_matriz(
    datos: List[Dict[str, any]],
    filtros: Optional[Dict[str, str]] = None
) -> Dict[str, List[str]]:
    """Procesa una matriz de datos aplicando filtros opcionales.

    Args:
        datos: Lista de diccionarios con datos de la matriz.
            Cada diccionario debe contener las claves 'rol' y 'permisos'.
        filtros: Diccionario opcional de filtros a aplicar.
            Las claves son campos y los valores son criterios.
            Default: None.

    Returns:
        Dict[str, List[str]]: Diccionario donde:
            - Las claves son nombres de roles
            - Los valores son listas de permisos filtrados

    Examples:
        >>> datos = [{"rol": "admin", "permisos": ["leer", "escribir"]}]
        >>> procesar_matriz(datos)
        {'admin': ['leer', 'escribir']}
    """
```

## Secciones Comunes en Docstrings

1. **Args**: Para parámetros de funciones
   ```python
   """
   Args:
       param1: Descripción del primer parámetro
       param2: Descripción del segundo parámetro
   """
   ```

2. **Returns**: Para valores de retorno
   ```python
   """
   Returns:
       Descripción de lo que devuelve la función
   """
   ```

3. **Raises**: Para excepciones
   ```python
   """
   Raises:
       ValueError: Cuando ocurre un error de valor
       TypeError: Cuando hay un error de tipo
   """
   ```

4. **Examples**: Para ejemplos de uso
   ```python
   """
   Examples:
       >>> mi_funcion(123)
       'resultado'
   """
   ```

5. **Notes**: Para notas adicionales
   ```python
   """
   Notes:
       Esta función es thread-safe y puede ser
       llamada desde múltiples hilos.
   """
   ```

## Buenas Prácticas

1. **Ser Conciso pero Completo**:
   ```python
   def sumar(a: int, b: int) -> int:
       """Suma dos números enteros.

       Args:
           a: Primer número
           b: Segundo número

       Returns:
           La suma de a y b
       """
       return a + b
   ```

2. **Documentar Comportamientos Especiales**:
   ```python
   def dividir(a: float, b: float) -> float:
       """Divide dos números.

       Args:
           a: Numerador
           b: Denominador

       Returns:
           El resultado de la división

       Raises:
           ZeroDivisionError: Si b es cero
       """
       return a / b
   ```

3. **Incluir Ejemplos Relevantes**:
   ```python
   def es_palindromo(texto: str) -> bool:
       """Verifica si un texto es palíndromo.

       Args:
           texto: Cadena a verificar

       Returns:
           True si es palíndromo, False si no

       Examples:
           >>> es_palindromo("ana")
           True
           >>> es_palindromo("hola")
           False
       """
       return texto == texto[::-1]
   ```

## Herramientas de Soporte

1. **VS Code**: Autocompletado de docstrings
2. **PyCharm**: Generación automática de docstrings
3. **Sphinx**: Generación de documentación
4. **autodoc**: Plugin para generar documentación automáticamente

## Referencias
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

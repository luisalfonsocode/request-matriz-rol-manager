# Guía de Type Hints en Python

Los type hints son anotaciones que nos permiten especificar los tipos de datos esperados en nuestro código Python. Son especialmente útiles para:
- Detectar errores temprano
- Mejorar la documentación
- Facilitar el auto-completado en IDEs
- Hacer el código más mantenible

## Ejemplos Básicos

### Sin Type Hints
```python
def suma(a, b):
    return a + b
```

### Con Type Hints
```python
def suma(a: int, b: int) -> int:
    return a + b
```

## Tipos Comunes

### Tipos Básicos
```python
def procesar_datos(
    nombre: str,           # String
    edad: int,            # Entero
    altura: float,        # Decimal
    activo: bool          # Booleano
) -> str:
    return f"{nombre} tiene {edad} años y mide {altura}m"
```

### Listas y Diccionarios
```python
from typing import List, Dict

def obtener_nombres(usuarios: List[str]) -> List[str]:
    return [u.upper() for u in usuarios]

def obtener_edades(datos: Dict[str, int]) -> Dict[str, int]:
    return datos
```

### Tipos Opcionales
```python
from typing import Optional

def saludar(nombre: str, titulo: Optional[str] = None) -> str:
    if titulo:
        return f"Hola {titulo} {nombre}"
    return f"Hola {nombre}"
```

### Unión de Tipos
```python
from typing import Union

def procesar_valor(valor: Union[str, int]) -> str:
    return str(valor)
```

## Type Hints en Clases

```python
from typing import List, Optional
from datetime import datetime

class Usuario:
    def __init__(
        self,
        nombre: str,
        edad: int,
        correo: Optional[str] = None
    ) -> None:
        self.nombre = nombre
        self.edad = edad
        self.correo = correo

    def actualizar_correo(self, nuevo_correo: str) -> bool:
        if '@' in nuevo_correo:
            self.correo = nuevo_correo
            return True
        return False

    def obtener_info(self) -> Dict[str, Union[str, int]]:
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "correo": self.correo or "No especificado"
        }
```

## Beneficios de Usar Type Hints

1. **Detección de Errores Temprana**:
   ```python
   def calcular_promedio(notas: List[float]) -> float:
       return sum(notas) / len(notas)
   
   # El IDE/linter advertirá sobre este error:
   calcular_promedio(["no", "son", "números"])  # ❌ Error de tipo
   ```

2. **Mejor Documentación**:
   ```python
   def procesar_matriz(
       datos: List[Dict[str, Union[str, int]]],
       categoria: Optional[str] = None
   ) -> Dict[str, List[str]]:
       """Los type hints hacen obvio qué espera y devuelve la función"""
       pass
   ```

3. **Autocompletado Mejorado**:
   - Los IDEs pueden proporcionar mejores sugerencias
   - Menos necesidad de consultar documentación

## Herramientas

1. **mypy**: Verificador estático de tipos
   ```bash
   mypy tu_archivo.py
   ```

2. **VS Code + Pylance**:
   - Verificación en tiempo real
   - Autocompletado inteligente
   - Detección de errores mientras escribes

## Mejores Prácticas

1. Usar type hints desde el inicio del proyecto
2. Documentar tipos complejos con type aliases:
   ```python
   from typing import TypeAlias, Dict, List

   DatosUsuario: TypeAlias = Dict[str, Union[str, int]]
   ListaResultados: TypeAlias = List[DatosUsuario]
   ```

3. No mezclar código con y sin type hints
4. Usar herramientas de verificación (mypy, pyright)
5. Mantener los tipos lo más específicos posible

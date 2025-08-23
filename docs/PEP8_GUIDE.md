# Guía Detallada de Estilo PEP 8

## Índice
- [Diseño del Código](#diseño-del-código)
- [Indentación](#indentación)
- [Longitud de Líneas](#longitud-de-líneas)
- [Importaciones](#importaciones)
- [Espacios en Blanco](#espacios-en-blanco)
- [Convenciones de Nombres](#convenciones-de-nombres)
- [Comentarios](#comentarios)
- [Docstrings](#docstrings)
- [Consejos Prácticos](#consejos-prácticos)

## Diseño del Código

### Indentación
- Usar 4 espacios por nivel de indentación
- No usar tabuladores
- La indentación de continuación debe alinearse con el delimitador de apertura

```python
# Correcto
def funcion_larga(
        parametro1,
        parametro2,
        parametro3):
    return parametro1

# Incorrecto
def funcion_larga(parametro1,
    parametro2,  # mal indentado
    parametro3):
    return parametro1
```

### Longitud de Líneas
- Máximo 79 caracteres para código
- Máximo 72 caracteres para comentarios largos y docstrings
- Usar paréntesis para dividir líneas largas

```python
# Correcto
total = (primer_numero
         + segundo_numero
         + tercer_numero)

# También correcto
from mi_paquete.mi_modulo import (
    primera_clase, segunda_clase,
    tercera_clase)

# Incorrecto
total = primer_numero + segundo_numero + tercer_numero + cuarto_numero + quinto_numero + sexto_numero
```

## Importaciones

### Orden de Importaciones
1. Módulos de la biblioteca estándar
2. Módulos de terceros relacionados
3. Módulos locales/aplicación específica

```python
# Correcto
import os
import sys
from typing import List, Optional

import pandas as pd
import requests
from sqlalchemy import Column, Integer

from mi_proyecto.modulo import MiClase
from mi_proyecto.constantes import VALOR_MAXIMO

# Incorrecto
import sys
from mi_proyecto.modulo import MiClase
import os
import pandas as pd
```

### Estilo de Importaciones
- Una importación por línea
- Evitar comodines (`from module import *`)

```python
# Correcto
from mi_modulo import clase1
from mi_modulo import clase2

# Incorrecto
from mi_modulo import clase1, clase2
from mi_modulo import *
```

## Espacios en Blanco

### En Expresiones y Sentencias
- Evitar espacios extras dentro de paréntesis/corchetes
- Evitar espacios antes de coma/punto y coma
- Usar espacios alrededor de operadores

```python
# Correcto
spam(ham[1], {eggs: 2})
if x == 4:
    print(x, y)

# Incorrecto
spam( ham[ 1 ], { eggs: 2 } )
if x==4 :
    print(x , y)
```

### Líneas en Blanco
- Dos líneas en blanco antes de funciones de nivel superior y clases
- Una línea en blanco entre métodos en clases
- Líneas en blanco para separar grupos lógicos de código

```python
class ClaseUno:
    def metodo_uno(self):
        return 1

    def metodo_dos(self):
        return 2


class ClaseDos:
    def otro_metodo(self):
        return 3
```

## Convenciones de Nombres

### Variables y Funciones
- Minúsculas con guiones bajos
- Descriptivas pero no demasiado largas

```python
# Correcto
mi_variable = 1
def calcular_total():
    pass

# Incorrecto
miVariable = 1
def CalcularTotal():
    pass
```

### Clases
- CapWords/PascalCase

```python
# Correcto
class MiClase:
    pass

class ClienteHTTP:
    pass

# Incorrecto
class mi_clase:
    pass
```

### Constantes
- Mayúsculas con guiones bajos

```python
# Correcto
MAXIMO_CONEXIONES = 100
CODIGO_ERROR = "E001"

# Incorrecto
maximoConexiones = 100
```

## Comentarios

### Estilo de Comentarios
- Completos y claros
- En su propia línea
- Actualizados con el código

```python
# Correcto
# Calcula el promedio de la lista de números
promedio = sum(numeros) / len(numeros)

# Incorrecto
promedio = sum(numeros) / len(numeros) # calcula promedio
```

### Comentarios en Línea
- Usar con moderación
- Dos espacios después del código
- No obvios

```python
# Correcto
x = x + 1  # Compensa el desplazamiento del borde

# Incorrecto
x = x + 1 # Incrementa x
```

## Docstrings

### Formato
- Triple comilla doble
- Una línea para descripciones simples
- Múltiples líneas para documentación compleja

```python
def funcion_compleja(parametro1: str, parametro2: int) -> bool:
    """
    Realiza una operación compleja con los parámetros dados.

    Args:
        parametro1: Una cadena que describe el primer parámetro
        parametro2: Un entero que indica la cantidad

    Returns:
        bool: True si la operación fue exitosa, False en caso contrario

    Raises:
        ValueError: Si parametro2 es negativo
    """
    pass
```

## Consejos Prácticos

### Herramientas de Formateo
- **Black**: Formateador automático
- **isort**: Ordena importaciones
- **flake8**: Verifica cumplimiento de PEP 8
- **pylint**: Análisis estático más completo

### Configuración en VS Code
```json
{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

### Pre-commit Hooks
Configura pre-commit para verificar automáticamente el estilo antes de cada commit:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
    -   id: isort
-   repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
    -   id: flake8
```

## Referencias
- [PEP 8 Oficial](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python PEP 8 Guide](https://realpython.com/python-pep8/)

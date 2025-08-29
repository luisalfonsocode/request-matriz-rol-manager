"""
Módulo de formateo de contenido para correos individuales.

Este módulo contiene las clases responsables del formateo
y personalización del contenido de los correos electrónicos.
"""

from .plantillas_html import PlantillasHTML
from .plantillas_texto import PlantillasTexto
from .formateador_contenido import FormateadorContenido

__all__ = ["PlantillasHTML", "PlantillasTexto", "FormateadorContenido"]

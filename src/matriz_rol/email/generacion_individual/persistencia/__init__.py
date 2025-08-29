"""
Módulo de persistencia para correos individuales.

Este módulo contiene las clases responsables de la creación
y persistencia de archivos de correo electrónico.
"""

from .gestor_archivos import GestorArchivos
from .creador_msg import CreadorMSG
from .creador_eml import CreadorEML

__all__ = ["GestorArchivos", "CreadorMSG", "CreadorEML"]

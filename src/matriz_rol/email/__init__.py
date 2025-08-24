"""
Módulo de email para el proyecto utilitarios-matriz-de-rol.

Este módulo contiene las clases y funciones para:
- Generar correos de solicitud de conformidad
- Crear archivos .msg/.eml listos para enviar
- Formatear contenido profesional de correos
"""

from .generador_correos import GeneradorCorreos, generar_correo_desde_datos

__all__ = ["GeneradorCorreos", "generar_correo_desde_datos"]

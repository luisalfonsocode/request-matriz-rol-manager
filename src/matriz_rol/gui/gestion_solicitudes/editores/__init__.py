"""
Editores inline para gestión de solicitudes.

Este módulo contiene editores especializados para permitir
la edición directa de campos en la grilla de solicitudes.
"""

from .editor_estado import EditorEstado
from .editor_ticket import EditorTicket
from .editor_observaciones import EditorObservaciones

__all__ = ["EditorEstado", "EditorTicket", "EditorObservaciones"]

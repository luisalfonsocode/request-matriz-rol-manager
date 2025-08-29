"""
Manejador de eventos de la grilla de solicitudes.

Este módulo contiene la lógica para manejar eventos específicos
del TreeView de solicitudes, como doble clic y edición inline.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable
from ....data.gestor_solicitudes import GestorSolicitudes
from ..editores.editor_estado import EditorEstado
from ..editores.editor_ticket import EditorTicket
from ..editores.editor_observaciones import EditorObservaciones


class EventosGrilla:
    """Manejador de eventos específicos de la grilla de solicitudes."""

    def __init__(
        self,
        gestor_solicitudes: GestorSolicitudes,
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el manejador de eventos.

        Args:
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
            callback_actualizar: Función a llamar después de cambios
        """
        self.gestor = gestor_solicitudes
        self.callback_actualizar = callback_actualizar

        # Editores especializados
        self.editor_estado = EditorEstado(gestor_solicitudes, callback_actualizar)
        self.editor_ticket = EditorTicket(gestor_solicitudes, callback_actualizar)
        self.editor_observaciones = EditorObservaciones(
            gestor_solicitudes, callback_actualizar
        )

    def manejar_doble_clic(
        self, event: tk.Event, tree_solicitudes: ttk.Treeview
    ) -> None:
        """
        Maneja el doble clic en la grilla para edición inline.

        Args:
            event: Evento de doble clic
            tree_solicitudes: TreeView de solicitudes
        """
        try:
            # Verificar si ya hay una edición en curso
            if (
                self.editor_estado.editando
                or self.editor_ticket.editando
                or self.editor_observaciones.editando
            ):
                return

            # Obtener el elemento y columna clickeada
            item = tree_solicitudes.identify_row(event.y)
            columna = tree_solicitudes.identify_column(event.x)

            if not item:
                return

            # Obtener datos del item
            valores = tree_solicitudes.item(item, "values")
            if not valores:
                return

            id_solicitud = valores[0]

            # Obtener la solicitud completa
            solicitud = self.gestor.obtener_solicitud_por_id(id_solicitud)
            if not solicitud:
                print(f"❌ No se encontró la solicitud {id_solicitud}")
                return

            # Delegar según la columna clickeada
            if columna == "#3":  # Columna Estado
                self._editar_estado(event, tree_solicitudes, item, solicitud)
            elif columna == "#6":  # Columna Ticket
                self._editar_ticket(event, tree_solicitudes, item, solicitud)
            elif columna == "#7":  # Columna Observaciones
                self._editar_observaciones(event, tree_solicitudes, item, solicitud)
            else:
                # Si no es columna editable, podríamos mostrar detalles
                print(f"ℹ️ Columna no editable: {columna}")

        except Exception as e:
            print(f"❌ Error en doble clic: {e}")

    def _editar_estado(
        self, event: tk.Event, tree: ttk.Treeview, item: str, solicitud
    ) -> None:
        """
        Inicia la edición del estado de una solicitud.

        Args:
            event: Evento del doble clic
            tree: TreeView
            item: Item seleccionado
            solicitud: Solicitud a editar
        """
        try:
            bbox = tree.bbox(item, column="#3")
            if bbox:
                self.editor_estado.iniciar_edicion(tree, item, bbox, solicitud)
        except Exception as e:
            print(f"❌ Error editando estado: {e}")

    def _editar_ticket(
        self, event: tk.Event, tree: ttk.Treeview, item: str, solicitud
    ) -> None:
        """
        Inicia la edición del ticket de una solicitud.

        Args:
            event: Evento del doble clic
            tree: TreeView
            item: Item seleccionado
            solicitud: Solicitud a editar
        """
        try:
            bbox = tree.bbox(item, column="#6")
            if bbox:
                self.editor_ticket.iniciar_edicion(tree, item, bbox, solicitud)
        except Exception as e:
            print(f"❌ Error editando ticket: {e}")

    def _editar_observaciones(
        self, event: tk.Event, tree: ttk.Treeview, item: str, solicitud
    ) -> None:
        """
        Inicia la edición de las observaciones de una solicitud.

        Args:
            event: Evento del doble clic
            tree: TreeView
            item: Item seleccionado
            solicitud: Solicitud a editar
        """
        try:
            bbox = tree.bbox(item, column="#7")
            if bbox:
                self.editor_observaciones.iniciar_edicion(tree, item, bbox, solicitud)
        except Exception as e:
            print(f"❌ Error editando observaciones: {e}")

    def finalizar_todas_ediciones(self) -> None:
        """Finaliza todas las ediciones en curso."""
        try:
            self.editor_estado.finalizar_edicion()
            self.editor_ticket.finalizar_edicion()
            self.editor_observaciones.finalizar_edicion()
        except Exception as e:
            print(f"❌ Error finalizando ediciones: {e}")

    def hay_edicion_activa(self) -> bool:
        """
        Verifica si hay alguna edición activa.

        Returns:
            True si hay alguna edición en curso
        """
        return (
            self.editor_estado.editando
            or self.editor_ticket.editando
            or self.editor_observaciones.editando
        )

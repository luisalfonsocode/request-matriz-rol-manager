"""
Editor inline para estados de solicitud.

Permite editar el estado de una solicitud directamente en la grilla
mediante un ComboBox temporal.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from ....data.gestor_solicitudes import (
    GestorSolicitudes,
    SolicitudConformidad,
    EstadoSolicitud,
)
from ..manejadores.validadores import Validadores


class EditorEstado:
    """Editor inline para estados de solicitud."""

    def __init__(
        self,
        gestor_solicitudes: GestorSolicitudes,
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el editor de estados.

        Args:
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
            callback_actualizar: Función a llamar después de cambios
        """
        self.gestor = gestor_solicitudes
        self.callback_actualizar = callback_actualizar

        # Estado del editor
        self.editando = False
        self.combobox_editor: Optional[ttk.Combobox] = None
        self.tree_actual: Optional[ttk.Treeview] = None
        self.item_actual: Optional[str] = None
        self.solicitud_actual: Optional[SolicitudConformidad] = None

    def iniciar_edicion(
        self,
        tree: ttk.Treeview,
        item: str,
        bbox: tuple,
        solicitud: SolicitudConformidad,
    ) -> None:
        """
        Inicia la edición inline del estado.

        Args:
            tree: TreeView donde se edita
            item: Item a editar
            bbox: Coordenadas del item
            solicitud: Solicitud a editar
        """
        if self.editando:
            return

        try:
            # Obtener estados permitidos
            estados_permitidos = Validadores.obtener_estados_permitidos(
                solicitud.estado
            )

            if not estados_permitidos:
                messagebox.showinfo(
                    "Sin cambios",
                    f"El estado '{solicitud.estado.value}' no permite cambios directos.\\n"
                    "Use los botones de acción para cambiar el estado.",
                )
                return

            # Guardar referencias
            self.tree_actual = tree
            self.item_actual = item
            self.solicitud_actual = solicitud
            self.editando = True

            # Crear lista de valores para el combobox
            valores_combo = [estado.value for estado in estados_permitidos]

            # Crear el combobox temporal
            x, y, width, height = bbox
            self.combobox_editor = ttk.Combobox(
                tree, values=valores_combo, state="readonly"
            )

            # Posicionar el combobox
            self.combobox_editor.place(x=x, y=y, width=width, height=height)

            # Establecer valor actual
            self.combobox_editor.set(solicitud.estado.value)

            # Enfocar y seleccionar
            self.combobox_editor.focus()

            # Bind eventos
            self.combobox_editor.bind("<Return>", self._guardar_estado)
            self.combobox_editor.bind("<Escape>", self._cancelar_edicion)
            self.combobox_editor.bind("<FocusOut>", self._guardar_estado)
            self.combobox_editor.bind("<<ComboboxSelected>>", self._guardar_estado)

        except Exception as e:
            print(f"❌ Error iniciando edición de estado: {e}")
            self.finalizar_edicion()

    def _guardar_estado(self, event=None) -> None:
        """Guarda el nuevo estado seleccionado."""
        if not self.editando or not self.combobox_editor:
            return

        try:
            nuevo_estado_texto = self.combobox_editor.get()

            if not nuevo_estado_texto:
                self._cancelar_edicion()
                return

            # Convertir texto a EstadoSolicitud
            try:
                nuevo_estado = EstadoSolicitud(nuevo_estado_texto)
            except ValueError:
                messagebox.showerror("Error", f"Estado no válido: {nuevo_estado_texto}")
                self._cancelar_edicion()
                return

            # Validar transición
            es_valida, mensaje_error = Validadores.validar_transicion_estado(
                self.solicitud_actual.estado, nuevo_estado
            )

            if not es_valida:
                messagebox.showerror("Error", mensaje_error)
                self._cancelar_edicion()
                return

            # Si no hay cambio, cancelar
            if nuevo_estado == self.solicitud_actual.estado:
                self._cancelar_edicion()
                return

            # Actualizar en el gestor
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_actual.id_solicitud,
                nuevo_estado,
                observaciones=f"Estado cambiado a {nuevo_estado.value} via edición inline",
            ):
                # Actualizar el item en el tree
                valores = list(self.tree_actual.item(self.item_actual, "values"))
                valores[2] = nuevo_estado.value.title()  # Columna Estado
                self.tree_actual.item(self.item_actual, values=valores)

                # Actualizar color según nuevo estado
                self._actualizar_color_item(nuevo_estado)

                messagebox.showinfo(
                    "Éxito", f"✅ Estado actualizado a: {nuevo_estado.value}"
                )

                # Callback para actualizar otras partes de la UI
                self.callback_actualizar()
            else:
                messagebox.showerror("Error", "❌ Error actualizando el estado")

        except Exception as e:
            print(f"❌ Error guardando estado: {e}")
            messagebox.showerror("Error", f"❌ Error guardando estado: {e}")
        finally:
            self.finalizar_edicion()

    def _cancelar_edicion(self, event=None) -> None:
        """Cancela la edición actual."""
        self.finalizar_edicion()

    def _actualizar_color_item(self, nuevo_estado: EstadoSolicitud) -> None:
        """
        Actualiza el color del item según el nuevo estado.

        Args:
            nuevo_estado: Nuevo estado de la solicitud
        """
        if not self.tree_actual or not self.item_actual:
            return

        # Mapeo de estados a tags
        mapeo_tags = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: "en_solicitud",
            EstadoSolicitud.EN_HELPDESK: "en_helpdesk",
            EstadoSolicitud.ATENDIDO: "atendido",
            EstadoSolicitud.CERRADO: "cerrado",
        }

        tag = mapeo_tags.get(nuevo_estado, "default")
        self.tree_actual.item(self.item_actual, tags=[tag])

    def finalizar_edicion(self) -> None:
        """Finaliza la edición y limpia recursos."""
        if self.combobox_editor:
            try:
                self.combobox_editor.destroy()
            except:
                pass
            self.combobox_editor = None

        # Limpiar variables
        self.editando = False
        self.tree_actual = None
        self.item_actual = None
        self.solicitud_actual = None

    def esta_editando(self) -> bool:
        """
        Verifica si está en modo edición.

        Returns:
            True si está editando
        """
        return self.editando

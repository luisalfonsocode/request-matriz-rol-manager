"""
Editor inline para tickets de helpdesk.

Permite editar el ticket de helpdesk de una solicitud directamente
en la grilla mediante un Entry temporal.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from ....data.gestor_solicitudes import GestorSolicitudes, SolicitudConformidad
from ..manejadores.validadores import Validadores


class EditorTicket:
    """Editor inline para tickets de helpdesk."""

    def __init__(
        self,
        gestor_solicitudes: GestorSolicitudes,
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el editor de tickets.

        Args:
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
            callback_actualizar: Función a llamar después de cambios
        """
        self.gestor = gestor_solicitudes
        self.callback_actualizar = callback_actualizar

        # Estado del editor
        self.editando = False
        self.entry_editor: Optional[tk.Entry] = None
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
        Inicia la edición inline del ticket.

        Args:
            tree: TreeView donde se edita
            item: Item a editar
            bbox: Coordenadas del item
            solicitud: Solicitud a editar
        """
        if self.editando:
            return

        try:
            # Guardar referencias
            self.tree_actual = tree
            self.item_actual = item
            self.solicitud_actual = solicitud
            self.editando = True

            # Crear el entry temporal
            x, y, width, height = bbox
            self.entry_editor = tk.Entry(tree)

            # Posicionar el entry
            self.entry_editor.place(x=x, y=y, width=width, height=height)

            # Establecer valor actual
            ticket_actual = solicitud.ticket_helpdesk or ""
            self.entry_editor.insert(0, ticket_actual)

            # Seleccionar todo el texto
            self.entry_editor.select_range(0, tk.END)

            # Enfocar
            self.entry_editor.focus()

            # Bind eventos
            self.entry_editor.bind("<Return>", self._guardar_ticket)
            self.entry_editor.bind("<Escape>", self._cancelar_edicion)
            self.entry_editor.bind("<FocusOut>", self._guardar_ticket)

        except Exception as e:
            print(f"❌ Error iniciando edición de ticket: {e}")
            self.finalizar_edicion()

    def _guardar_ticket(self, event=None) -> None:
        """Guarda el nuevo ticket."""
        if not self.editando or not self.entry_editor:
            return

        try:
            nuevo_ticket = self.entry_editor.get().strip()

            # Validar ticket
            es_valido, mensaje_error = Validadores.validar_ticket_helpdesk(nuevo_ticket)

            if not es_valido and nuevo_ticket:  # Permitir vacío
                messagebox.showerror("Error", mensaje_error)
                self._cancelar_edicion()
                return

            # Si no hay cambio, cancelar
            ticket_actual = self.solicitud_actual.ticket_helpdesk or ""
            if nuevo_ticket == ticket_actual:
                self._cancelar_edicion()
                return

            # Actualizar en el gestor
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_actual.id_solicitud,
                self.solicitud_actual.estado,  # Mantener mismo estado
                nuevo_ticket,
                (
                    f"Ticket actualizado a: {nuevo_ticket}"
                    if nuevo_ticket
                    else "Ticket removido"
                ),
            ):
                # Actualizar el item en el tree
                valores = list(self.tree_actual.item(self.item_actual, "values"))
                valores[5] = nuevo_ticket  # Columna Ticket
                self.tree_actual.item(self.item_actual, values=valores)

                mensaje = (
                    f"✅ Ticket actualizado: {nuevo_ticket}"
                    if nuevo_ticket
                    else "✅ Ticket removido"
                )
                messagebox.showinfo("Éxito", mensaje)

                # Callback para actualizar otras partes de la UI
                self.callback_actualizar()
            else:
                messagebox.showerror("Error", "❌ Error actualizando el ticket")

        except Exception as e:
            print(f"❌ Error guardando ticket: {e}")
            messagebox.showerror("Error", f"❌ Error guardando ticket: {e}")
        finally:
            self.finalizar_edicion()

    def _cancelar_edicion(self, event=None) -> None:
        """Cancela la edición actual."""
        self.finalizar_edicion()

    def finalizar_edicion(self) -> None:
        """Finaliza la edición y limpia recursos."""
        if self.entry_editor:
            try:
                self.entry_editor.destroy()
            except:
                pass
            self.entry_editor = None

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

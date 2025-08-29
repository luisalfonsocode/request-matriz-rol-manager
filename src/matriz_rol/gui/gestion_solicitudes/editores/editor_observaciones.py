"""
Editor inline para observaciones de solicitud.

Permite editar las observaciones de una solicitud directamente
en la grilla mediante un Text temporal.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from ....data.gestor_solicitudes import GestorSolicitudes, SolicitudConformidad
from ..manejadores.validadores import Validadores


class EditorObservaciones:
    """Editor inline para observaciones de solicitud."""

    def __init__(
        self,
        gestor_solicitudes: GestorSolicitudes,
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el editor de observaciones.

        Args:
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
            callback_actualizar: Función a llamar después de cambios
        """
        self.gestor = gestor_solicitudes
        self.callback_actualizar = callback_actualizar

        # Estado del editor
        self.editando = False
        self.text_editor: Optional[tk.Text] = None
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
        Inicia la edición inline de observaciones.

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

            # Crear el text temporal con scrollbar
            x, y, width, height = bbox

            # Hacer el editor más alto para observaciones
            height = max(height, 80)

            # Frame contenedor
            frame_editor = tk.Frame(tree)
            frame_editor.place(x=x, y=y, width=width, height=height)

            # Text widget
            self.text_editor = tk.Text(
                frame_editor, wrap=tk.WORD, height=3, font=("Arial", 9)
            )

            # Scrollbar
            scrollbar = tk.Scrollbar(
                frame_editor, orient="vertical", command=self.text_editor.yview
            )
            self.text_editor.configure(yscrollcommand=scrollbar.set)

            # Posicionar widgets
            self.text_editor.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Establecer valor actual
            observaciones_actuales = solicitud.observaciones or ""
            self.text_editor.insert("1.0", observaciones_actuales)

            # Seleccionar todo el texto
            self.text_editor.tag_add("sel", "1.0", "end")

            # Enfocar
            self.text_editor.focus()

            # Bind eventos
            self.text_editor.bind("<Control-Return>", self._guardar_observaciones)
            self.text_editor.bind("<Escape>", self._cancelar_edicion)
            self.text_editor.bind("<FocusOut>", self._guardar_observaciones)

            # Guardar referencia al frame para poder destruirlo
            self.frame_editor = frame_editor

        except Exception as e:
            print(f"❌ Error iniciando edición de observaciones: {e}")
            self.finalizar_edicion()

    def _guardar_observaciones(self, event=None) -> None:
        """Guarda las nuevas observaciones."""
        if not self.editando or not self.text_editor:
            return

        try:
            nuevas_observaciones = self.text_editor.get("1.0", "end-1c").strip()

            # Validar observaciones
            es_valido, mensaje_error = Validadores.validar_observaciones(
                nuevas_observaciones
            )

            if not es_valido:
                messagebox.showerror("Error", mensaje_error)
                self._cancelar_edicion()
                return

            # Si no hay cambio, cancelar
            observaciones_actuales = self.solicitud_actual.observaciones or ""
            if nuevas_observaciones == observaciones_actuales:
                self._cancelar_edicion()
                return

            # Actualizar en el gestor
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_actual.id_solicitud,
                self.solicitud_actual.estado,  # Mantener mismo estado
                observaciones=nuevas_observaciones,
            ):
                # Actualizar el item en el tree (version truncada)
                observaciones_cortas = (
                    nuevas_observaciones[:50] + "..."
                    if len(nuevas_observaciones) > 50
                    else nuevas_observaciones
                )

                valores = list(self.tree_actual.item(self.item_actual, "values"))
                valores[6] = observaciones_cortas  # Columna Observaciones
                self.tree_actual.item(self.item_actual, values=valores)

                messagebox.showinfo("Éxito", "✅ Observaciones actualizadas")

                # Callback para actualizar otras partes de la UI
                self.callback_actualizar()
            else:
                messagebox.showerror("Error", "❌ Error actualizando las observaciones")

        except Exception as e:
            print(f"❌ Error guardando observaciones: {e}")
            messagebox.showerror("Error", f"❌ Error guardando observaciones: {e}")
        finally:
            self.finalizar_edicion()

    def _cancelar_edicion(self, event=None) -> None:
        """Cancela la edición actual."""
        self.finalizar_edicion()

    def finalizar_edicion(self) -> None:
        """Finaliza la edición y limpia recursos."""
        if hasattr(self, "frame_editor") and self.frame_editor:
            try:
                self.frame_editor.destroy()
            except:
                pass
            self.frame_editor = None

        if self.text_editor:
            self.text_editor = None

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

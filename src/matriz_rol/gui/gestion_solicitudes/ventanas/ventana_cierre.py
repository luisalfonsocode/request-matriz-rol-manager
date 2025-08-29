"""
Ventana para cerrar solicitudes.

Proporciona una interfaz especializada para cerrar solicitudes
con validaciones y confirmaciones apropiadas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from customtkinter import CTkFrame, CTkLabel, CTkTextbox, CTkButton
from ....data.gestor_solicitudes import SolicitudConformidad, EstadoSolicitud


class VentanaCierre(tk.Toplevel):
    """Ventana modal para cerrar solicitudes."""

    def __init__(
        self,
        parent,
        solicitud: SolicitudConformidad,
        callback_cerrar: Optional[Callable[[str, str], bool]] = None,
    ):
        """
        Inicializa la ventana de cierre.

        Args:
            parent: Ventana padre
            solicitud: Solicitud a cerrar
            callback_cerrar: Función callback para cerrar la solicitud
        """
        super().__init__(parent)

        self.solicitud = solicitud
        self.callback_cerrar = callback_cerrar

        # Configurar ventana
        self.title(f"Cerrar Solicitud - {solicitud.id_solicitud}")
        self.geometry("600x500")

        if parent:
            self.transient(parent)
            self.grab_set()  # Modal

        # Variables
        self.ticket_var = tk.StringVar(value=solicitud.ticket_helpdesk or "")
        self.observaciones_cierre = ""

        # Centrar ventana
        self._centrar_ventana()

        # Crear interfaz
        self._crear_interfaz()

    def _centrar_ventana(self) -> None:
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _crear_interfaz(self) -> None:
        """Crea la interfaz de la ventana."""
        # Frame principal
        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        titulo = CTkLabel(
            main_frame,
            text=f"🔒 Cerrar Solicitud: {self.solicitud.id_solicitud}",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

        # Información de la solicitud
        self._crear_seccion_info(main_frame)

        # Campos obligatorios
        self._crear_seccion_campos(main_frame)

        # Observaciones de cierre
        self._crear_seccion_observaciones(main_frame)

        # Botones
        self._crear_botones(main_frame)

    def _crear_seccion_info(self, parent) -> None:
        """Crea la sección de información de la solicitud."""
        frame_info = CTkFrame(parent)
        frame_info.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            frame_info,
            text="📊 Información de la Solicitud",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Grid para información
        info_grid = CTkFrame(frame_info)
        info_grid.pack(fill="x", padx=10, pady=5)

        # ID de solicitud
        CTkLabel(info_grid, text="ID Solicitud:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )

        CTkLabel(info_grid, text=self.solicitud.id_solicitud).grid(
            row=0, column=1, sticky="w", padx=5, pady=2
        )

        # Estado actual
        CTkLabel(info_grid, text="Estado Actual:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )

        CTkLabel(info_grid, text=self.solicitud.estado.value.title()).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )

        # Cantidad de grupos
        CTkLabel(info_grid, text="Grupos de Red:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )

        cantidad_grupos = (
            len(self.solicitud.grupos_red) if self.solicitud.grupos_red else 0
        )
        CTkLabel(info_grid, text=f"{cantidad_grupos} grupos").grid(
            row=2, column=1, sticky="w", padx=5, pady=2
        )

    def _crear_seccion_campos(self, parent) -> None:
        """Crea la sección de campos obligatorios."""
        frame_campos = CTkFrame(parent)
        frame_campos.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            frame_campos, text="📝 Información de Cierre", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Campo ticket
        ticket_frame = CTkFrame(frame_campos)
        ticket_frame.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            ticket_frame, text="🎫 Ticket Helpdesk*:", font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=5, pady=2)

        self.entry_ticket = tk.Entry(
            ticket_frame, textvariable=self.ticket_var, font=("Arial", 10), width=50
        )
        self.entry_ticket.pack(fill="x", padx=5, pady=2)

        # Nota sobre campos obligatorios
        nota = CTkLabel(
            frame_campos,
            text="* Campos obligatorios para cerrar la solicitud",
            font=("Arial", 9),
            text_color="orange",
        )
        nota.pack(anchor="w", padx=10, pady=2)

    def _crear_seccion_observaciones(self, parent) -> None:
        """Crea la sección de observaciones de cierre."""
        frame_obs = CTkFrame(parent)
        frame_obs.pack(fill="both", expand=True, padx=10, pady=5)

        CTkLabel(
            frame_obs, text="💬 Observaciones de Cierre", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Textbox para observaciones
        self.txt_observaciones = CTkTextbox(frame_obs, height=150)
        self.txt_observaciones.pack(fill="both", expand=True, padx=10, pady=5)

        # Placeholder text
        self.txt_observaciones.insert(
            "0.0", "Agregue observaciones sobre el cierre de la solicitud..."
        )

    def _crear_botones(self, parent) -> None:
        """Crea los botones de la ventana."""
        frame_botones = CTkFrame(parent)
        frame_botones.pack(fill="x", padx=10, pady=10)

        # Botón de cancelar
        CTkButton(
            frame_botones,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color="red",
            hover_color="darkred",
        ).pack(side="right", padx=5)

        # Botón de cerrar solicitud
        CTkButton(
            frame_botones,
            text="🔒 Cerrar Solicitud",
            command=self._cerrar_solicitud,
            fg_color="green",
            hover_color="darkgreen",
        ).pack(side="right", padx=5)

    def _cerrar_solicitud(self) -> None:
        """Procesa el cierre de la solicitud."""
        try:
            # Validar campos obligatorios
            if not self._validar_campos():
                return

            # Confirmar cierre
            if not self._confirmar_cierre():
                return

            # Obtener datos del formulario
            ticket = self.ticket_var.get().strip()
            observaciones = self.txt_observaciones.get("0.0", "end-1c").strip()

            # Ejecutar callback si existe
            if self.callback_cerrar:
                exito = self.callback_cerrar(ticket, observaciones)
                if exito:
                    messagebox.showinfo(
                        "Éxito",
                        f"Solicitud {self.solicitud.id_solicitud} cerrada correctamente",
                    )
                    self.destroy()
                else:
                    messagebox.showerror(
                        "Error", "No se pudo cerrar la solicitud. Verifique los datos."
                    )
            else:
                # Si no hay callback, mostrar mensaje de simulación
                messagebox.showinfo(
                    "Simulación",
                    f"Solicitud {self.solicitud.id_solicitud} sería cerrada con:\\n"
                    f"Ticket: {ticket}\\n"
                    f"Observaciones: {observaciones[:100]}...",
                )
                self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def _validar_campos(self) -> bool:
        """
        Valida los campos obligatorios.

        Returns:
            bool: True si todos los campos son válidos
        """
        # Validar ticket
        ticket = self.ticket_var.get().strip()
        if not ticket:
            messagebox.showerror(
                "Campo Obligatorio",
                "El ticket de Helpdesk es obligatorio para cerrar la solicitud.",
            )
            self.entry_ticket.focus()
            return False

        # Validar formato del ticket (opcional)
        if len(ticket) < 3:
            messagebox.showerror(
                "Formato Inválido", "El ticket debe tener al menos 3 caracteres."
            )
            self.entry_ticket.focus()
            return False

        return True

    def _confirmar_cierre(self) -> bool:
        """
        Muestra un diálogo de confirmación para el cierre.

        Returns:
            bool: True si el usuario confirma el cierre
        """
        resultado = messagebox.askyesno(
            "Confirmar Cierre",
            f"¿Está seguro de que desea cerrar la solicitud {self.solicitud.id_solicitud}?\\n\\n"
            "Esta acción no se puede deshacer.",
            icon="question",
        )
        return resultado

    def obtener_datos_cierre(self) -> dict:
        """
        Obtiene los datos ingresados para el cierre.

        Returns:
            dict: Diccionario con ticket y observaciones
        """
        return {
            "ticket": self.ticket_var.get().strip(),
            "observaciones": self.txt_observaciones.get("0.0", "end-1c").strip(),
        }

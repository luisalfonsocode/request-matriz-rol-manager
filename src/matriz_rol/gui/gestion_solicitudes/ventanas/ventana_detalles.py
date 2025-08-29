"""
Ventana de detalles completos de solicitud.

Muestra todos los detalles de una solicitud en una ventana modal
con la misma interfaz visual que la creación de solicitudes.
"""

import tkinter as tk
from tkinter import ttk
from customtkinter import CTkFrame, CTkLabel, CTkTextbox, CTkButton
from ....data.gestor_solicitudes import SolicitudConformidad


class VentanaDetalles(tk.Toplevel):
    """Ventana modal para mostrar detalles completos de una solicitud."""

    def __init__(self, parent, solicitud: SolicitudConformidad):
        """
        Inicializa la ventana de detalles.

        Args:
            parent: Ventana padre
            solicitud: Solicitud a mostrar
        """
        super().__init__(parent)

        self.solicitud = solicitud

        # Configurar ventana
        self.title(f"Detalles - {solicitud.id_solicitud}")
        self.geometry("1000x800")

        if parent:
            self.transient(parent)
            self.grab_set()  # Modal

        # Centrar ventana
        self._centrar_ventana()

        # Crear interfaz
        self._crear_interfaz()
        self._cargar_datos()

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
            text=f"📋 Detalles de Solicitud: {self.solicitud.id_solicitud}",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

        # Información general
        self._crear_seccion_informacion(main_frame)

        # Grupos de red
        self._crear_seccion_grupos(main_frame)

        # Autorizadores
        self._crear_seccion_autorizadores(main_frame)

        # Observaciones
        self._crear_seccion_observaciones(main_frame)

        # Botones
        self._crear_botones(main_frame)

    def _crear_seccion_informacion(self, parent) -> None:
        """Crea la sección de información general."""
        frame_info = CTkFrame(parent)
        frame_info.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            frame_info, text="📊 Información General", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Grid para información básica
        info_grid = CTkFrame(frame_info)
        info_grid.pack(fill="x", padx=10, pady=5)

        # Estado
        CTkLabel(info_grid, text="Estado:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )

        CTkLabel(info_grid, text=self.solicitud.estado.value.title()).grid(
            row=0, column=1, sticky="w", padx=5, pady=2
        )

        # Fecha de creación
        CTkLabel(info_grid, text="Fecha de Creación:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )

        fecha_str = (
            self.solicitud.fecha_creacion.split("T")[0]
            if "T" in self.solicitud.fecha_creacion
            else self.solicitud.fecha_creacion
        )
        CTkLabel(info_grid, text=fecha_str).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )

        # Ticket
        CTkLabel(info_grid, text="Ticket Helpdesk:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )

        CTkLabel(info_grid, text=self.solicitud.ticket_helpdesk or "Sin asignar").grid(
            row=2, column=1, sticky="w", padx=5, pady=2
        )

        # Fecha de cierre (si aplica)
        if self.solicitud.fecha_cierre:
            CTkLabel(
                info_grid, text="Fecha de Cierre:", font=("Arial", 10, "bold")
            ).grid(row=3, column=0, sticky="w", padx=5, pady=2)

            fecha_cierre_str = (
                self.solicitud.fecha_cierre.split("T")[0]
                if "T" in self.solicitud.fecha_cierre
                else self.solicitud.fecha_cierre
            )
            CTkLabel(info_grid, text=fecha_cierre_str).grid(
                row=3, column=1, sticky="w", padx=5, pady=2
            )

    def _crear_seccion_grupos(self, parent) -> None:
        """Crea la sección de grupos de red."""
        self.frame_grupos = CTkFrame(parent)
        self.frame_grupos.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            self.frame_grupos, text="🌐 Grupos de Red", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Textbox para mostrar grupos (solo lectura)
        self.txt_grupos = CTkTextbox(self.frame_grupos, height=100)
        self.txt_grupos.pack(fill="x", padx=10, pady=5)

    def _crear_seccion_autorizadores(self, parent) -> None:
        """Crea la sección de autorizadores."""
        self.frame_autorizadores = CTkFrame(parent)
        self.frame_autorizadores.pack(fill="both", expand=True, padx=10, pady=5)

        CTkLabel(
            self.frame_autorizadores,
            text="👥 Autorizadores Asignados",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Crear tabla de autorizadores
        self._crear_tabla_autorizadores()

    def _crear_tabla_autorizadores(self) -> None:
        """Crea la tabla de autorizadores."""
        # Frame para la tabla
        tabla_frame = CTkFrame(self.frame_autorizadores)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear treeview para autorizadores
        columnas = ("Código", "Autorizador", "Correo")
        self.tree_autorizadores = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=6
        )

        # Configurar encabezados
        self.tree_autorizadores.heading("Código", text="Código App")
        self.tree_autorizadores.heading("Autorizador", text="Nombre Autorizador")
        self.tree_autorizadores.heading("Correo", text="Correo Electrónico")

        # Configurar anchos
        self.tree_autorizadores.column("Código", width=100)
        self.tree_autorizadores.column("Autorizador", width=300)
        self.tree_autorizadores.column("Correo", width=250)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tree_autorizadores.yview
        )
        scrollbar_x = ttk.Scrollbar(
            tabla_frame, orient="horizontal", command=self.tree_autorizadores.xview
        )

        self.tree_autorizadores.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
        )

        # Posicionar elementos
        self.tree_autorizadores.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

    def _crear_seccion_observaciones(self, parent) -> None:
        """Crea la sección de observaciones."""
        self.frame_observaciones = CTkFrame(parent)
        self.frame_observaciones.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            self.frame_observaciones,
            text="📝 Observaciones",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Textbox para observaciones (solo lectura)
        self.txt_observaciones = CTkTextbox(self.frame_observaciones, height=80)
        self.txt_observaciones.pack(fill="x", padx=10, pady=5)

    def _crear_botones(self, parent) -> None:
        """Crea los botones de la ventana."""
        frame_botones = CTkFrame(parent)
        frame_botones.pack(fill="x", padx=10, pady=10)

        # Botón de cerrar
        CTkButton(frame_botones, text="✅ Cerrar", command=self.destroy).pack(
            side="right", padx=5
        )

    def _cargar_datos(self) -> None:
        """Carga los datos de la solicitud en la interfaz."""
        try:
            # Cargar grupos de red
            if self.solicitud.grupos_red:
                grupos_texto = "\\n".join(
                    f"• {grupo}" for grupo in self.solicitud.grupos_red
                )
                self.txt_grupos.insert("0.0", grupos_texto)
                self.txt_grupos.configure(state="disabled")  # Solo lectura
            else:
                self.txt_grupos.insert("0.0", "No hay grupos de red especificados")
                self.txt_grupos.configure(state="disabled")

            # Cargar autorizadores
            if self.solicitud.autorizadores:
                for auth in self.solicitud.autorizadores:
                    self.tree_autorizadores.insert(
                        "",
                        "end",
                        values=(
                            auth.get("codigo", "N/A"),
                            auth.get("autorizador", "N/A"),
                            auth.get("correo", "N/A"),
                        ),
                    )

            # Cargar observaciones
            if self.solicitud.observaciones:
                self.txt_observaciones.insert("0.0", self.solicitud.observaciones)
                self.txt_observaciones.configure(state="disabled")  # Solo lectura
            else:
                self.txt_observaciones.insert("0.0", "Sin observaciones")
                self.txt_observaciones.configure(state="disabled")

        except Exception as e:
            print(f"❌ Error cargando datos en ventana de detalles: {e}")

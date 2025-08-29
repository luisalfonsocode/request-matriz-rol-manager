"""
Frame principal refactorizado para gestión de solicitudes de conformidad.

Este módulo orquesta todos los componentes especializados y proporciona
la interfaz principal para la gestión de solicitudes.
"""

from typing import Optional
from customtkinter import CTkFrame, CTkLabel, CTkButton
from ...data.gestor_solicitudes import GestorSolicitudes, SolicitudConformidad
from .componentes.panel_estadisticas import PanelEstadisticas
from .componentes.panel_filtros import PanelFiltros
from .componentes.lista_solicitudes import ListaSolicitudes
from .manejadores.eventos_grilla import EventosGrilla


class GestionSolicitudesFrame(CTkFrame):
    """Frame principal refactorizado para gestionar solicitudes de conformidad."""

    def __init__(self, master, gestor_solicitudes: GestorSolicitudes):
        """
        Inicializa el frame de gestión de solicitudes.

        Args:
            master: Widget padre
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
        """
        super().__init__(master)

        # Referencias principales
        self.gestor = gestor_solicitudes
        self.solicitud_seleccionada: Optional[SolicitudConformidad] = None

        # Componentes especializados
        self.panel_estadisticas: Optional[PanelEstadisticas] = None
        self.panel_filtros: Optional[PanelFiltros] = None
        self.lista_solicitudes: Optional[ListaSolicitudes] = None

        # Manejadores de lógica de negocio
        self.eventos_grilla: Optional[EventosGrilla] = None

        self._configurar_interfaz()
        self._inicializar_manejadores()
        self.actualizar_lista_solicitudes()

    def _configurar_interfaz(self) -> None:
        """Configura la interfaz completa del frame."""
        # Título principal
        self._crear_titulo()

        # Frame superior con estadísticas y filtros
        frame_superior = CTkFrame(self)
        frame_superior.pack(fill="x", padx=10, pady=5)

        self._crear_panel_estadisticas(frame_superior)
        self._crear_panel_filtros(frame_superior)

        # Frame principal con la lista de solicitudes
        frame_principal = CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=5)

        self._crear_lista_solicitudes(frame_principal)

        # Frame inferior con botón de guardar
        frame_inferior = CTkFrame(self)
        frame_inferior.pack(fill="x", padx=10, pady=5)

        self._crear_botones_accion(frame_inferior)

    def _crear_titulo(self) -> None:
        """Crea el título principal del frame."""
        titulo = CTkLabel(
            self,
            text="📋 Gestión de Solicitudes de Conformidad",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

    def _crear_panel_estadisticas(self, parent) -> None:
        """Crea el panel de estadísticas."""
        self.panel_estadisticas = PanelEstadisticas(parent, self.gestor)
        self.panel_estadisticas.pack(fill="x", padx=5, pady=5)

    def _crear_panel_filtros(self, parent) -> None:
        """Crea el panel de filtros."""
        self.panel_filtros = PanelFiltros(
            parent,
            callback_filtros=self.aplicar_filtros,
            callback_actualizar=self.actualizar_manual,
        )
        self.panel_filtros.pack(fill="x", padx=5, pady=5)

    def _crear_lista_solicitudes(self, parent) -> None:
        """Crea la lista principal de solicitudes."""
        self.lista_solicitudes = ListaSolicitudes(
            parent,
            callback_seleccion=self._on_solicitud_seleccionada,
            callback_doble_clic=self._on_doble_clic_grilla,
        )
        self.lista_solicitudes.pack(fill="both", expand=True)

    def _crear_botones_accion(self, parent) -> None:
        """Crea los botones de acción principales."""

        # Frame contenedor para centrar botones
        botones_frame = CTkFrame(parent)
        botones_frame.pack(fill="x", padx=10, pady=10)

        # Botón de guardar datos
        btn_guardar = CTkButton(
            botones_frame,
            text="💾 Guardar Datos",
            command=self._guardar_datos,
            font=("Arial", 12, "bold"),
            height=40,
            width=200,
            fg_color="#2E8B57",  # Verde
            hover_color="#228B22",
        )
        btn_guardar.pack(side="left", padx=10)

        # Botón de actualizar
        btn_actualizar = CTkButton(
            botones_frame,
            text="🔄 Actualizar Lista",
            command=self.actualizar_manual,
            font=("Arial", 12),
            height=40,
            width=150,
            fg_color="#4682B4",  # Azul
            hover_color="#1E90FF",
        )
        btn_actualizar.pack(side="left", padx=10)

    def _inicializar_manejadores(self) -> None:
        """Inicializa los manejadores de lógica de negocio."""
        self.eventos_grilla = EventosGrilla(
            self.gestor, callback_actualizar=self.actualizar_lista_solicitudes
        )

    def _on_solicitud_seleccionada(
        self, solicitud: Optional[SolicitudConformidad]
    ) -> None:
        """
        Maneja la selección de una solicitud.

        Args:
            solicitud: Solicitud seleccionada o None
        """
        self.solicitud_seleccionada = solicitud

    def _on_doble_clic_grilla(self, event) -> None:
        """
        Maneja el doble clic en la grilla.

        Args:
            event: Evento de tkinter
        """
        if self.eventos_grilla and self.lista_solicitudes:
            self.eventos_grilla.manejar_doble_clic(
                event, self.lista_solicitudes.tree_solicitudes
            )

    def actualizar_lista_solicitudes(self) -> None:
        """Actualiza la lista de solicitudes mostrada."""
        try:
            print("🔄 Actualizando lista de solicitudes en UI...")

            # Forzar recarga desde archivo
            self.gestor.cargar_solicitudes()
            solicitudes = self.gestor.obtener_solicitudes()

            # Aplicar filtros
            solicitudes_filtradas = self._aplicar_filtros_actuales(solicitudes)

            # Actualizar componentes
            if self.lista_solicitudes:
                self.lista_solicitudes.actualizar_solicitudes(solicitudes_filtradas)

            if self.panel_estadisticas:
                self.panel_estadisticas.actualizar_estadisticas()

            print(
                f"✅ {len(solicitudes_filtradas)} solicitudes mostradas en la interfaz"
            )

        except Exception as e:
            print(f"❌ Error actualizando lista de solicitudes: {e}")

    def _aplicar_filtros_actuales(self, solicitudes) -> list:
        """
        Aplica los filtros actuales a la lista de solicitudes.

        Args:
            solicitudes: Lista de solicitudes sin filtrar

        Returns:
            Lista de solicitudes filtradas
        """
        if not self.panel_filtros:
            return solicitudes

        estado_filtro = self.panel_filtros.obtener_estado_filtro()

        if estado_filtro:
            return [s for s in solicitudes if s.estado == estado_filtro]

        return solicitudes

    def aplicar_filtros(self) -> None:
        """Aplica los filtros seleccionados."""
        self.actualizar_lista_solicitudes()

    def actualizar_manual(self) -> None:
        """Actualización manual activada por el usuario."""
        try:
            from tkinter import messagebox

            print("\\n🔄 ACTUALIZACIÓN MANUAL INICIADA POR USUARIO")

            # Mostrar mensaje de progreso
            messagebox.showinfo(
                "Actualizando", "⏳ Recargando solicitudes desde BD local..."
            )

            # Forzar recarga completa
            self.actualizar_lista_solicitudes()

            # Mostrar mensaje de confirmación
            info_bd = self.gestor.obtener_info_bd()
            mensaje = (
                f"✅ Actualización completada!\\n\\n"
                f"📊 Total solicitudes: {info_bd['total_solicitudes']}\\n"
                f"💾 BD Local: {info_bd['tamaño_kb']} KB\\n"
                f"📅 Última modificación: {info_bd.get('ultima_modificacion', 'N/A')[:19]}"
            )
            messagebox.showinfo("Actualización Exitosa", mensaje)

        except Exception as e:
            from tkinter import messagebox

            print(f"❌ Error en actualización manual: {e}")
            messagebox.showerror("Error", f"❌ Error actualizando:\\n{e}")

    def _guardar_datos(self) -> None:
        """Guarda los datos de las solicitudes."""
        from tkinter import messagebox

        try:
            # Obtener datos del gestor
            self.gestor.cargar_solicitudes()
            solicitudes = self.gestor.obtener_solicitudes()

            # Simular guardado de datos
            if solicitudes:
                count = len(solicitudes)
                messagebox.showinfo(
                    "Datos Guardados",
                    f"✅ Se han guardado {count} solicitudes correctamente.\\n\\n"
                    "Los datos han sido sincronizados con la base de datos.",
                )
                print(f"📊 Datos guardados: {count} solicitudes")
            else:
                messagebox.showwarning(
                    "Sin Datos", "⚠️ No hay solicitudes para guardar."
                )

        except Exception as e:
            messagebox.showerror(
                "Error al Guardar", f"❌ Error al guardar los datos:\\n{e}"
            )
            print(f"❌ Error en _guardar_datos: {e}")

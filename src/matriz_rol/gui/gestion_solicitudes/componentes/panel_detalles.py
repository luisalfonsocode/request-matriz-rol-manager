"""
Panel de detalles y acciones para gestión de solicitudes.

Muestra información de la solicitud seleccionada y proporciona botones de acción.
"""

from typing import Optional, Callable
from customtkinter import CTkFrame, CTkLabel, CTkButton
from ....data.gestor_solicitudes import SolicitudConformidad


class PanelDetalles(CTkFrame):
    """Panel que muestra detalles de la solicitud seleccionada y acciones disponibles."""

    def __init__(
        self,
        master,
        callback_enviar_helpdesk: Callable[[], None],
        callback_marcar_atendido: Callable[[], None],
        callback_cerrar_solicitud: Callable[[], None],
        callback_reabrir_solicitud: Callable[[], None],
        callback_ver_detalles: Callable[[], None],
    ):
        """
        Inicializa el panel de detalles.

        Args:
            master: Widget padre
            callback_enviar_helpdesk: Función para enviar a helpdesk
            callback_marcar_atendido: Función para marcar como atendido
            callback_cerrar_solicitud: Función para cerrar solicitud
            callback_reabrir_solicitud: Función para reabrir solicitud
            callback_ver_detalles: Función para ver detalles completos
        """
        super().__init__(master)

        # Guardar callbacks
        self.callback_enviar_helpdesk = callback_enviar_helpdesk
        self.callback_marcar_atendido = callback_marcar_atendido
        self.callback_cerrar_solicitud = callback_cerrar_solicitud
        self.callback_reabrir_solicitud = callback_reabrir_solicitud
        self.callback_ver_detalles = callback_ver_detalles

        # Variables de estado
        self.solicitud_actual: Optional[SolicitudConformidad] = None

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        """Configura la interfaz del panel de detalles."""
        # Título del panel
        titulo = CTkLabel(
            self, text="📝 Detalles y Acciones:", font=("Arial", 12, "bold")
        )
        titulo.pack(anchor="w", padx=5, pady=5)

        # Frame principal de detalles
        frame_detalles = CTkFrame(self)
        frame_detalles.pack(fill="x", padx=5, pady=5)

        # Crear secciones
        self._crear_seccion_informacion(frame_detalles)
        self._crear_seccion_acciones(frame_detalles)

    def _crear_seccion_informacion(self, parent) -> None:
        """Crea la sección de información de la solicitud."""
        # Lado izquierdo - Información
        frame_info = CTkFrame(parent)
        frame_info.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        CTkLabel(frame_info, text="ℹ️ Información Seleccionada:").pack(
            anchor="w", padx=5, pady=2
        )

        self.label_info_solicitud = CTkLabel(
            frame_info, text="Seleccione una solicitud para ver detalles"
        )
        self.label_info_solicitud.pack(anchor="w", padx=5, pady=2)

    def _crear_seccion_acciones(self, parent) -> None:
        """Crea la sección de acciones disponibles."""
        # Lado derecho - Acciones
        frame_acciones = CTkFrame(parent)
        frame_acciones.pack(side="right", padx=5, pady=5)

        CTkLabel(frame_acciones, text="⚡ Acciones:").pack(anchor="w", padx=5, pady=2)

        # Botones de acción
        self._crear_botones_accion(frame_acciones)

    def _crear_botones_accion(self, parent) -> None:
        """Crea los botones de acción."""
        botones = [
            ("🎫 Enviar a Helpdesk", self.callback_enviar_helpdesk),
            ("✅ Marcar como Atendido", self.callback_marcar_atendido),
            ("🏁 Cerrar Solicitud", self.callback_cerrar_solicitud),
            ("🔄 Reabrir Solicitud", self.callback_reabrir_solicitud),
            ("📋 Ver Detalles Completos", self.callback_ver_detalles),
        ]

        for texto, callback in botones:
            btn = CTkButton(parent, text=texto, command=callback)
            btn.pack(pady=2, padx=5)

    def actualizar_solicitud_seleccionada(
        self, solicitud: Optional[SolicitudConformidad]
    ) -> None:
        """
        Actualiza la información de la solicitud seleccionada.

        Args:
            solicitud: Solicitud seleccionada o None si no hay selección
        """
        self.solicitud_actual = solicitud

        if solicitud:
            # Formatear información de la solicitud
            info_texto = self._formatear_info_solicitud(solicitud)
            self.label_info_solicitud.configure(text=info_texto)
        else:
            self.label_info_solicitud.configure(
                text="Seleccione una solicitud para ver detalles"
            )

    def _formatear_info_solicitud(self, solicitud: SolicitudConformidad) -> str:
        """
        Formatea la información de una solicitud para mostrar.

        Args:
            solicitud: Solicitud a formatear

        Returns:
            Texto formateado con la información
        """
        fecha_formateada = (
            solicitud.fecha_creacion.split("T")[0]
            if "T" in solicitud.fecha_creacion
            else solicitud.fecha_creacion
        )

        info_partes = [
            f"📋 ID: {solicitud.id_solicitud}",
            f"📅 Fecha: {fecha_formateada}",
            f"📊 Estado: {solicitud.estado.value}",
            f"🌐 Grupos: {len(solicitud.grupos_red)} grupo(s)",
            f"👥 Autorizadores: {len(solicitud.autorizadores)}",
        ]

        if solicitud.ticket_helpdesk:
            info_partes.append(f"🎫 Ticket: {solicitud.ticket_helpdesk}")

        if solicitud.observaciones:
            obs_cortas = (
                solicitud.observaciones[:60] + "..."
                if len(solicitud.observaciones) > 60
                else solicitud.observaciones
            )
            info_partes.append(f"📝 Obs: {obs_cortas}")

        return " | ".join(info_partes)

    def obtener_solicitud_actual(self) -> Optional[SolicitudConformidad]:
        """
        Obtiene la solicitud actualmente seleccionada.

        Returns:
            Solicitud actual o None
        """
        return self.solicitud_actual

    def limpiar_seleccion(self) -> None:
        """Limpia la información de la solicitud seleccionada."""
        self.actualizar_solicitud_seleccionada(None)

"""
Panel de filtros para gestión de solicitudes.

Proporciona controles de filtrado y búsqueda para la lista de solicitudes.
"""

from typing import Callable, Optional
from customtkinter import CTkFrame, CTkLabel, CTkComboBox, CTkButton
from ....data.gestor_solicitudes import EstadoSolicitud


class PanelFiltros(CTkFrame):
    """Panel que proporciona filtros para la lista de solicitudes."""

    def __init__(
        self,
        master,
        callback_filtros: Callable[[], None],
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el panel de filtros.

        Args:
            master: Widget padre
            callback_filtros: Función a llamar cuando cambian los filtros
            callback_actualizar: Función a llamar para actualizar manualmente
        """
        super().__init__(master)
        self.callback_filtros = callback_filtros
        self.callback_actualizar = callback_actualizar

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        """Configura la interfaz del panel de filtros."""
        # Título del panel
        titulo = CTkLabel(self, text="🔍 Filtros:", font=("Arial", 12, "bold"))
        titulo.pack(anchor="w", padx=5, pady=2)

        # Frame contenedor para los controles
        frame_controles = CTkFrame(self)
        frame_controles.pack(fill="x", padx=5, pady=2)

        # Filtro por estado
        self._crear_filtro_estado(frame_controles)

        # Botón de actualizar
        self._crear_boton_actualizar(frame_controles)

    def _crear_filtro_estado(self, parent) -> None:
        """Crea el filtro por estado."""
        CTkLabel(parent, text="Estado:").pack(side="left", padx=5)

        valores_estado = [
            "Todas",
            "En solicitud de conformidades",
            "En Helpdesk",
            "Atendido",
            "Cerrado",
        ]

        self.combo_filtro_estado = CTkComboBox(
            parent, values=valores_estado, command=self._on_filtro_cambiado
        )
        self.combo_filtro_estado.pack(side="left", padx=5)
        self.combo_filtro_estado.set("Todas")

    def _crear_boton_actualizar(self, parent) -> None:
        """Crea el botón de actualización manual."""
        btn_actualizar = CTkButton(
            parent, text="🔄 Actualizar", command=self.callback_actualizar
        )
        btn_actualizar.pack(side="left", padx=10)

    def _on_filtro_cambiado(self, value: str = None) -> None:
        """
        Maneja el cambio de filtros.

        Args:
            value: Valor seleccionado (no usado, pero requerido por CTkComboBox)
        """
        self.callback_filtros()

    def obtener_estado_filtro(self) -> Optional[EstadoSolicitud]:
        """
        Obtiene el estado seleccionado en el filtro.

        Returns:
            Estado seleccionado o None si es "Todas"
        """
        valor_filtro = self.combo_filtro_estado.get()

        mapeo_estados = {
            "En solicitud de conformidades": EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
            "En Helpdesk": EstadoSolicitud.EN_HELPDESK,
            "Atendido": EstadoSolicitud.ATENDIDO,
            "Cerrado": EstadoSolicitud.CERRADO,
        }

        return mapeo_estados.get(valor_filtro)

    def restablecer_filtros(self) -> None:
        """Restablece todos los filtros a su estado inicial."""
        self.combo_filtro_estado.set("Todas")
        self.callback_filtros()

    def aplicar_filtros(self) -> None:
        """Aplica los filtros actuales."""
        self._on_filtro_cambiado()

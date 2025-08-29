"""
Panel de estadísticas para gestión de solicitudes.

Muestra contadores y métricas en tiempo real del estado de las solicitudes.
"""

from typing import Dict
from customtkinter import CTkFrame, CTkLabel
from ....data.gestor_solicitudes import GestorSolicitudes


class PanelEstadisticas(CTkFrame):
    """Panel que muestra estadísticas de solicitudes de conformidad."""

    def __init__(self, master, gestor_solicitudes: GestorSolicitudes):
        """
        Inicializa el panel de estadísticas.

        Args:
            master: Widget padre
            gestor_solicitudes: Gestor de solicitudes para obtener datos
        """
        super().__init__(master)
        self.gestor = gestor_solicitudes
        self.labels_stats: Dict[str, CTkLabel] = {}

        self._configurar_interfaz()
        self.actualizar_estadisticas()

    def _configurar_interfaz(self) -> None:
        """Configura la interfaz del panel de estadísticas."""
        # Título del panel
        titulo = CTkLabel(self, text="📊 Estadísticas:", font=("Arial", 12, "bold"))
        titulo.pack(anchor="w", padx=5, pady=2)

        # Frame contenedor para los contadores
        self.frame_contadores = CTkFrame(self)
        self.frame_contadores.pack(fill="x", padx=5, pady=2)

    def actualizar_estadisticas(self) -> None:
        """Actualiza las estadísticas mostradas."""
        try:
            stats = self.gestor.obtener_estadisticas()

            # Limpiar labels anteriores
            for widget in self.frame_contadores.winfo_children():
                widget.destroy()

            # Crear nuevos labels con las estadísticas actualizadas
            info_stats = [
                (f"📊 Total: {stats['total']}", "#2196F3"),
                (f"🔄 En solicitud: {stats['en_solicitud']}", "#4CAF50"),
                (f"🎫 En Helpdesk: {stats['en_helpdesk']}", "#FF9800"),
                (f"✅ Atendido: {stats['atendido']}", "#9C27B0"),
                (f"🏁 Cerrado: {stats['cerrado']}", "#9E9E9E"),
            ]

            for i, (texto, color) in enumerate(info_stats):
                label = CTkLabel(self.frame_contadores, text=texto, text_color=color)
                label.pack(side="left", padx=10, pady=2)

        except Exception as e:
            print(f"❌ Error actualizando estadísticas: {e}")
            # Mostrar mensaje de error en caso de fallo
            error_label = CTkLabel(
                self.frame_contadores,
                text="⚠️ Error cargando estadísticas",
                text_color="#f44336",
            )
            error_label.pack(side="left", padx=10, pady=2)

    def obtener_estadisticas(self) -> Dict[str, int]:
        """
        Obtiene las estadísticas actuales.

        Returns:
            Dict con las estadísticas de solicitudes
        """
        return self.gestor.obtener_estadisticas()

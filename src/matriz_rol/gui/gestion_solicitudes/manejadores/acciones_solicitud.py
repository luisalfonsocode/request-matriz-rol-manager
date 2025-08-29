"""
Manejador de acciones sobre solicitudes de conformidad.

Este módulo contiene la lógica de negocio para todas las acciones
que se pueden realizar sobre las solicitudes.
"""

from typing import Callable
from tkinter import messagebox, simpledialog
from ....data.gestor_solicitudes import (
    GestorSolicitudes,
    SolicitudConformidad,
    EstadoSolicitud,
)
from ..ventanas.ventana_detalles import VentanaDetalles
from ..ventanas.ventana_cierre import VentanaCierre


class AccionesSolicitud:
    """Manejador de acciones sobre solicitudes de conformidad."""

    def __init__(
        self,
        gestor_solicitudes: GestorSolicitudes,
        callback_actualizar: Callable[[], None],
    ):
        """
        Inicializa el manejador de acciones.

        Args:
            gestor_solicitudes: Gestor de solicitudes para operaciones de datos
            callback_actualizar: Función a llamar después de cada acción
        """
        self.gestor = gestor_solicitudes
        self.callback_actualizar = callback_actualizar

    def enviar_a_helpdesk(self, solicitud: SolicitudConformidad) -> None:
        """
        Envía una solicitud al helpdesk.

        Args:
            solicitud: Solicitud a enviar al helpdesk
        """
        try:
            # Validar estado
            if solicitud.estado == EstadoSolicitud.CERRADO:
                messagebox.showinfo("Información", "La solicitud ya está cerrada")
                return

            # Pedir número de ticket
            ticket = simpledialog.askstring(
                "Enviar a Helpdesk",
                f"Ingrese el número de ticket para la solicitud:\\n{solicitud.id_solicitud}",
            )

            if ticket:
                if self.gestor.actualizar_estado_solicitud(
                    solicitud.id_solicitud,
                    EstadoSolicitud.EN_HELPDESK,
                    ticket,
                    "Solicitud enviada al sistema de Helpdesk",
                ):
                    messagebox.showinfo(
                        "Éxito", f"✅ Solicitud enviada al Helpdesk\\nTicket: {ticket}"
                    )
                    self.callback_actualizar()
                else:
                    messagebox.showerror("Error", "❌ Error actualizando la solicitud")

        except Exception as e:
            print(f"❌ Error enviando a helpdesk: {e}")
            messagebox.showerror("Error", f"❌ Error enviando a helpdesk:\\n{e}")

    def marcar_atendido(self, solicitud: SolicitudConformidad) -> None:
        """
        Marca una solicitud como atendida.

        Args:
            solicitud: Solicitud a marcar como atendida
        """
        try:
            # Validar estado
            if solicitud.estado == EstadoSolicitud.CERRADO:
                messagebox.showinfo("Información", "La solicitud ya está cerrada")
                return

            # Pedir observaciones
            observaciones = simpledialog.askstring(
                "Marcar como Atendido",
                f"Observaciones para la solicitud:\\n{solicitud.id_solicitud}",
                initialvalue="Solicitud atendida correctamente",
            )

            if observaciones is not None:  # Permitir cadena vacía
                if self.gestor.actualizar_estado_solicitud(
                    solicitud.id_solicitud,
                    EstadoSolicitud.ATENDIDO,
                    observaciones=observaciones,
                ):
                    messagebox.showinfo("Éxito", "✅ Solicitud marcada como atendida")
                    self.callback_actualizar()
                else:
                    messagebox.showerror("Error", "❌ Error actualizando la solicitud")

        except Exception as e:
            print(f"❌ Error marcando como atendido: {e}")
            messagebox.showerror("Error", f"❌ Error marcando como atendido:\\n{e}")

    def cerrar_solicitud(self, solicitud: SolicitudConformidad) -> None:
        """
        Cierra una solicitud usando una ventana especializada.

        Args:
            solicitud: Solicitud a cerrar
        """
        try:
            # Validar estado
            if solicitud.estado == EstadoSolicitud.CERRADO:
                messagebox.showinfo("Información", "La solicitud ya está cerrada")
                return

            # Abrir ventana de cierre
            ventana_cierre = VentanaCierre(None, solicitud, self.gestor)

            # Si se cerró exitosamente, actualizar
            if ventana_cierre.solicitud_cerrada:
                self.callback_actualizar()

        except Exception as e:
            print(f"❌ Error cerrando solicitud: {e}")
            messagebox.showerror("Error", f"❌ Error cerrando solicitud:\\n{e}")

    def reabrir_solicitud(self, solicitud: SolicitudConformidad) -> None:
        """
        Reabre una solicitud cerrada.

        Args:
            solicitud: Solicitud a reabrir
        """
        try:
            # Validar estado
            if solicitud.estado != EstadoSolicitud.CERRADO:
                messagebox.showinfo(
                    "Información", "Solo se pueden reabrir solicitudes cerradas"
                )
                return

            # Confirmar reapertura
            confirmacion = messagebox.askyesno(
                "Reabrir Solicitud",
                f"¿Está seguro de reabrir la solicitud {solicitud.id_solicitud}?\\n\\n"
                "La solicitud volverá al estado 'En solicitud de conformidades'.",
            )

            if confirmacion:
                if self.gestor.actualizar_estado_solicitud(
                    solicitud.id_solicitud,
                    EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
                    observaciones="Solicitud reabierta",
                ):
                    messagebox.showinfo("Éxito", "✅ Solicitud reabierta exitosamente")
                    self.callback_actualizar()
                else:
                    messagebox.showerror("Error", "❌ Error reabriendo la solicitud")

        except Exception as e:
            print(f"❌ Error reabriendo solicitud: {e}")
            messagebox.showerror("Error", f"❌ Error reabriendo solicitud:\\n{e}")

    def marcar_en_proceso(self, solicitud: SolicitudConformidad) -> None:
        """
        Marca una solicitud como en proceso.

        Args:
            solicitud: Solicitud a marcar como en proceso
        """
        try:
            # Validar estado
            if solicitud.estado == EstadoSolicitud.CERRADO:
                messagebox.showinfo("Información", "La solicitud ya está cerrada")
                return

            # Confirmar cambio
            confirmacion = messagebox.askyesno(
                "Marcar en Proceso",
                f"¿Marcar solicitud {solicitud.id_solicitud} como en proceso?",
            )

            if confirmacion:
                if self.gestor.actualizar_estado_solicitud(
                    solicitud.id_solicitud,
                    EstadoSolicitud.EN_HELPDESK,
                    observaciones="Solicitud marcada como en proceso",
                ):
                    messagebox.showinfo("Éxito", "✅ Solicitud marcada como en proceso")
                    self.callback_actualizar()
                else:
                    messagebox.showerror("Error", "❌ Error actualizando la solicitud")

        except Exception as e:
            print(f"❌ Error marcando en proceso: {e}")
            messagebox.showerror("Error", f"❌ Error marcando en proceso:\\n{e}")

    def ver_detalles_solicitud(self, solicitud: SolicitudConformidad) -> None:
        """
        Muestra los detalles completos de una solicitud.

        Args:
            solicitud: Solicitud a mostrar
        """
        try:
            # Abrir ventana de detalles
            ventana_detalles = VentanaDetalles(None, solicitud)

        except Exception as e:
            print(f"❌ Error mostrando detalles: {e}")
            messagebox.showerror("Error", f"❌ Error mostrando detalles:\\n{e}")

    def actualizar_ticket_helpdesk(
        self, solicitud: SolicitudConformidad, nuevo_ticket: str
    ) -> bool:
        """
        Actualiza el ticket de helpdesk de una solicitud.

        Args:
            solicitud: Solicitud a actualizar
            nuevo_ticket: Nuevo número de ticket

        Returns:
            True si se actualizó exitosamente
        """
        try:
            if self.gestor.actualizar_estado_solicitud(
                solicitud.id_solicitud,
                solicitud.estado,  # Mantener el mismo estado
                nuevo_ticket,
                f"Ticket actualizado a: {nuevo_ticket}",
            ):
                self.callback_actualizar()
                return True
            return False

        except Exception as e:
            print(f"❌ Error actualizando ticket: {e}")
            return False

    def actualizar_observaciones(
        self, solicitud: SolicitudConformidad, nuevas_observaciones: str
    ) -> bool:
        """
        Actualiza las observaciones de una solicitud.

        Args:
            solicitud: Solicitud a actualizar
            nuevas_observaciones: Nuevas observaciones

        Returns:
            True si se actualizó exitosamente
        """
        try:
            if self.gestor.actualizar_estado_solicitud(
                solicitud.id_solicitud,
                solicitud.estado,  # Mantener el mismo estado
                observaciones=nuevas_observaciones,
            ):
                self.callback_actualizar()
                return True
            return False

        except Exception as e:
            print(f"❌ Error actualizando observaciones: {e}")
            return False

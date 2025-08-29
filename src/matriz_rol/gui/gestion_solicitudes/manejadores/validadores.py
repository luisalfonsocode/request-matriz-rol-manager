"""
Validadores para gestión de solicitudes.

Este módulo contiene validaciones de negocio para las operaciones
sobre solicitudes de conformidad.
"""

from typing import List, Optional, Tuple
from ....data.gestor_solicitudes import SolicitudConformidad, EstadoSolicitud


class Validadores:
    """Validadores de negocio para solicitudes de conformidad."""

    @staticmethod
    def validar_transicion_estado(
        estado_actual: EstadoSolicitud, estado_nuevo: EstadoSolicitud
    ) -> Tuple[bool, str]:
        """
        Valida si una transición de estado es permitida.

        Args:
            estado_actual: Estado actual de la solicitud
            estado_nuevo: Estado al que se quiere cambiar

        Returns:
            Tupla (es_valida, mensaje_error)
        """
        # Definir transiciones válidas
        transiciones_validas = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: [
                EstadoSolicitud.EN_HELPDESK,
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.EN_HELPDESK: [
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.CERRADO,
                EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,  # Para revertir
            ],
            EstadoSolicitud.ATENDIDO: [
                EstadoSolicitud.CERRADO,
                EstadoSolicitud.EN_HELPDESK,  # Para revertir
            ],
            EstadoSolicitud.CERRADO: [
                EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES  # Solo reapertura
            ],
        }

        # Si es el mismo estado, siempre es válido (para actualizaciones)
        if estado_actual == estado_nuevo:
            return True, ""

        # Verificar si la transición es válida
        estados_permitidos = transiciones_validas.get(estado_actual, [])

        if estado_nuevo in estados_permitidos:
            return True, ""
        else:
            return (
                False,
                f"No se puede cambiar de '{estado_actual.value}' a '{estado_nuevo.value}'",
            )

    @staticmethod
    def validar_ticket_helpdesk(ticket: str) -> Tuple[bool, str]:
        """
        Valida el formato de un ticket de helpdesk.

        Args:
            ticket: Número de ticket a validar

        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not ticket or not ticket.strip():
            return False, "El ticket no puede estar vacío"

        ticket = ticket.strip()

        # Validaciones básicas
        if len(ticket) < 3:
            return False, "El ticket debe tener al menos 3 caracteres"

        if len(ticket) > 50:
            return False, "El ticket no puede tener más de 50 caracteres"

        # Verificar que contenga al menos un número o letra
        if not any(c.isalnum() for c in ticket):
            return False, "El ticket debe contener al menos un número o letra"

        return True, ""

    @staticmethod
    def validar_observaciones(observaciones: str) -> Tuple[bool, str]:
        """
        Valida las observaciones de una solicitud.

        Args:
            observaciones: Observaciones a validar

        Returns:
            Tupla (es_valida, mensaje_error)
        """
        # Las observaciones pueden estar vacías
        if not observaciones:
            return True, ""

        # Validar longitud máxima
        if len(observaciones) > 1000:
            return False, "Las observaciones no pueden exceder 1000 caracteres"

        # Verificar caracteres válidos (evitar caracteres de control)
        caracteres_invalidos = [
            c for c in observaciones if ord(c) < 32 and c not in "\\n\\r\\t"
        ]
        if caracteres_invalidos:
            return False, "Las observaciones contienen caracteres no válidos"

        return True, ""

    @staticmethod
    def validar_solicitud_para_accion(
        solicitud: SolicitudConformidad, accion: str
    ) -> Tuple[bool, str]:
        """
        Valida si una solicitud puede ejecutar una acción específica.

        Args:
            solicitud: Solicitud a validar
            accion: Acción a ejecutar ('enviar_helpdesk', 'marcar_atendido', 'cerrar', 'reabrir')

        Returns:
            Tupla (es_valida, mensaje_error)
        """
        if not solicitud:
            return False, "No hay solicitud seleccionada"

        estado_actual = solicitud.estado

        if accion == "enviar_helpdesk":
            if estado_actual == EstadoSolicitud.CERRADO:
                return False, "No se puede enviar al helpdesk una solicitud cerrada"
            return True, ""

        elif accion == "marcar_atendido":
            if estado_actual == EstadoSolicitud.CERRADO:
                return False, "No se puede marcar como atendida una solicitud cerrada"
            return True, ""

        elif accion == "cerrar":
            if estado_actual == EstadoSolicitud.CERRADO:
                return False, "La solicitud ya está cerrada"
            return True, ""

        elif accion == "reabrir":
            if estado_actual != EstadoSolicitud.CERRADO:
                return False, "Solo se pueden reabrir solicitudes cerradas"
            return True, ""

        else:
            return False, f"Acción no reconocida: {accion}"

    @staticmethod
    def obtener_estados_permitidos(
        estado_actual: EstadoSolicitud,
    ) -> List[EstadoSolicitud]:
        """
        Obtiene los estados a los que se puede transicionar desde el estado actual.

        Args:
            estado_actual: Estado actual de la solicitud

        Returns:
            Lista de estados permitidos
        """
        transiciones_validas = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: [
                EstadoSolicitud.EN_HELPDESK,
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.EN_HELPDESK: [
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.ATENDIDO: [EstadoSolicitud.CERRADO],
            EstadoSolicitud.CERRADO: [EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES],
        }

        return transiciones_validas.get(estado_actual, [])

    @staticmethod
    def validar_edicion_inline(
        solicitud: SolicitudConformidad, campo: str, nuevo_valor: str
    ) -> Tuple[bool, str]:
        """
        Valida la edición inline de un campo específico.

        Args:
            solicitud: Solicitud a editar
            campo: Campo a editar ('estado', 'ticket', 'observaciones')
            nuevo_valor: Nuevo valor del campo

        Returns:
            Tupla (es_valida, mensaje_error)
        """
        if campo == "estado":
            try:
                nuevo_estado = EstadoSolicitud(nuevo_valor)
                return Validadores.validar_transicion_estado(
                    solicitud.estado, nuevo_estado
                )
            except ValueError:
                return False, f"Estado no válido: {nuevo_valor}"

        elif campo == "ticket":
            return Validadores.validar_ticket_helpdesk(nuevo_valor)

        elif campo == "observaciones":
            return Validadores.validar_observaciones(nuevo_valor)

        else:
            return False, f"Campo no editable: {campo}"

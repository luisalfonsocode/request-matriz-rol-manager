#!/usr/bin/env python3
"""
Script de prueba para validar los nuevos estados y funcionalidades.
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_solicitudes import GestorSolicitudes, EstadoSolicitud


def test_nuevos_estados():
    """Prueba los nuevos estados del sistema."""
    print("🧪 PRUEBAS DE NUEVOS ESTADOS")
    print("=" * 50)

    # Crear instancia del gestor
    gestor = GestorSolicitudes()

    # Mostrar estados disponibles
    print("\n📋 Estados disponibles:")
    for estado in EstadoSolicitud:
        print(f"  • {estado.name}: {estado.value}")

    # Obtener solicitudes existentes
    solicitudes = gestor.obtener_solicitudes()
    print(f"\n📊 Solicitudes existentes: {len(solicitudes)}")

    if solicitudes:
        solicitud = solicitudes[0]
        print(f"\n🔍 Probando con solicitud: {solicitud.id_solicitud}")
        print(f"   Estado actual: {solicitud.estado.value}")

        # Probar transición a Helpdesk
        print("\n1️⃣ Prueba: Enviar a Helpdesk")
        resultado = gestor.actualizar_estado_solicitud(
            solicitud.id_solicitud,
            EstadoSolicitud.EN_HELPDESK,
            ticket_helpdesk="TICKET-12345",
            observaciones="Enviado para revisión técnica",
        )
        print(f"   Resultado: {'✅ Éxito' if resultado else '❌ Error'}")

        # Verificar el cambio
        solicitud_actualizada = gestor.obtener_solicitud_por_id(solicitud.id_solicitud)
        if solicitud_actualizada:
            print(f"   Nuevo estado: {solicitud_actualizada.estado.value}")
            print(f"   Ticket: {solicitud_actualizada.ticket_helpdesk}")

        # Probar transición a Atendido
        print("\n2️⃣ Prueba: Marcar como Atendido")
        resultado = gestor.actualizar_estado_solicitud(
            solicitud.id_solicitud,
            EstadoSolicitud.ATENDIDO,
            observaciones="Cambios aplicados correctamente",
        )
        print(f"   Resultado: {'✅ Éxito' if resultado else '❌ Error'}")

        # Verificar el cambio
        solicitud_actualizada = gestor.obtener_solicitud_por_id(solicitud.id_solicitud)
        if solicitud_actualizada:
            print(f"   Nuevo estado: {solicitud_actualizada.estado.value}")
            print(f"   Observaciones: {solicitud_actualizada.observaciones}")

        # Probar transición a Cerrado
        print("\n3️⃣ Prueba: Cerrar solicitud")
        resultado = gestor.actualizar_estado_solicitud(
            solicitud.id_solicitud,
            EstadoSolicitud.CERRADO,
            ticket_helpdesk="TICKET-12345",
            observaciones="Solicitud completada y cerrada",
        )
        print(f"   Resultado: {'✅ Éxito' if resultado else '❌ Error'}")

        # Verificar el cambio
        solicitud_actualizada = gestor.obtener_solicitud_por_id(solicitud.id_solicitud)
        if solicitud_actualizada:
            print(f"   Nuevo estado: {solicitud_actualizada.estado.value}")
            print(f"   Fecha cierre: {solicitud_actualizada.fecha_cierre}")

        # Revertir a estado inicial para no afectar otros tests
        print("\n🔄 Revirtiendo al estado inicial...")
        gestor.actualizar_estado_solicitud(
            solicitud.id_solicitud,
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
            observaciones="Revertido para pruebas",
        )

    # Probar estadísticas
    print("\n📈 Probando estadísticas por estado:")
    estadisticas = gestor.obtener_estadisticas()
    total = estadisticas.get("total", 0)

    for estado_key, cantidad in estadisticas.items():
        if estado_key != "total":
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            print(f"   {estado_key}: {cantidad} solicitudes ({porcentaje:.1f}%)")

    print(f"   Total: {total} solicitudes")

    print("\n✅ Pruebas completadas")


if __name__ == "__main__":
    test_nuevos_estados()

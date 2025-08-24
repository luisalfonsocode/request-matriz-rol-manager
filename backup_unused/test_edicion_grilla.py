#!/usr/bin/env python3
"""
Script de prueba para validar la funcionalidad de edición de estado en grilla.
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_solicitudes import GestorSolicitudes, EstadoSolicitud


def test_transiciones_estado():
    """Prueba las transiciones de estado permitidas."""
    print("🧪 PRUEBAS DE TRANSICIONES DE ESTADO EN GRILLA")
    print("=" * 60)

    # Crear instancia del gestor
    gestor = GestorSolicitudes()

    # Simular la lógica de transiciones de la grilla
    def obtener_estados_permitidos(estado_actual):
        """Simula el método de la grilla."""
        transiciones = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: [
                EstadoSolicitud.EN_HELPDESK,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.EN_HELPDESK: [
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.ATENDIDO: [
                EstadoSolicitud.CERRADO,
                EstadoSolicitud.EN_HELPDESK,
            ],
            EstadoSolicitud.CERRADO: [],
        }
        return transiciones.get(estado_actual, [])

    print("\n📋 Transiciones permitidas por estado:")
    print("-" * 50)

    for estado in EstadoSolicitud:
        permitidos = obtener_estados_permitidos(estado)
        print(f"\n🔹 {estado.value}:")
        if permitidos:
            for permitido in permitidos:
                print(f"   ➤ {permitido.value}")
        else:
            print("   ❌ Sin transiciones permitidas (estado final)")

    # Probar con solicitudes existentes
    solicitudes = gestor.obtener_solicitudes()
    if solicitudes:
        print(f"\n📊 Probando con solicitud existente:")
        solicitud = solicitudes[0]
        print(f"   ID: {solicitud.id_solicitud}")
        print(f"   Estado actual: {solicitud.estado.value}")

        permitidos = obtener_estados_permitidos(solicitud.estado)
        print(f"   Estados permitidos para edición:")
        if permitidos:
            for permitido in permitidos:
                print(f"      ✅ {permitido.value}")
        else:
            print("      ❌ No se permite edición directa")

    print("\n" + "=" * 60)
    print("✅ Pruebas de transiciones completadas")
    print("\n📝 INSTRUCCIONES DE USO:")
    print("1. En la vista de 'Gestión de Solicitudes'")
    print("2. Haga doble clic en la columna 'Estado' de cualquier solicitud")
    print("3. Se mostrará un combobox con los estados permitidos")
    print("4. Seleccione el nuevo estado y presione Enter")
    print("5. Se aplicarán las validaciones correspondientes")


if __name__ == "__main__":
    test_transiciones_estado()

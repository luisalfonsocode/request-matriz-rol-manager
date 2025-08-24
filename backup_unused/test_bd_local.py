"""
Script de prueba para verificar la BD local de solicitudes.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_solicitudes import GestorSolicitudes


def main():
    print("🧪 PRUEBA DE BD LOCAL - SISTEMA DE SOLICITUDES")
    print("=" * 50)

    # Crear gestor
    gestor = GestorSolicitudes()

    # Mostrar información de la BD
    print("\n📊 INFORMACIÓN DE LA BD LOCAL:")
    info = gestor.obtener_info_bd()
    for clave, valor in info.items():
        print(f"   {clave}: {valor}")

    # Crear una solicitud de prueba si no hay ninguna
    if len(gestor.obtener_solicitudes()) == 0:
        print("\n➕ CREANDO SOLICITUD DE PRUEBA...")

        grupos_prueba = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]
        autorizadores_prueba = [
            {
                "codigo": "APF2",
                "autorizador": "María García",
                "correo": "maria.garcia@empresa.com",
            },
            {
                "codigo": "FCVE",
                "autorizador": "Juan Pérez",
                "correo": "juan.perez@empresa.com",
            },
        ]

        solicitud = gestor.crear_solicitud(grupos_prueba, autorizadores_prueba)
        print(f"✅ Solicitud de prueba creada: {solicitud.id_solicitud}")

    # Mostrar todas las solicitudes
    print("\n📋 SOLICITUDES EN LA BD:")
    solicitudes = gestor.obtener_solicitudes()
    for i, sol in enumerate(solicitudes, 1):
        print(f"   {i}. {sol.id_solicitud}")
        print(f"      Estado: {sol.estado.value}")
        print(f"      Grupos: {len(sol.grupos_red)}")
        print(f"      Autorizadores: {len(sol.autorizadores)}")
        print()

    print(f"✅ PRUEBA COMPLETADA - Total: {len(solicitudes)} solicitudes en BD")


if __name__ == "__main__":
    main()

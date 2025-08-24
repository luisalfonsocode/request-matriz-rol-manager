#!/usr/bin/env python3
"""
Script para probar la creación de solicitudes y verificar que aparezcan en la grilla.
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_crear_solicitud():
    """Prueba crear una solicitud y verificar que se guarde correctamente."""
    print("🧪 PRUEBA DE CREACIÓN DE SOLICITUDES")
    print("=" * 50)

    from matriz_rol.data.gestor_solicitudes import GestorSolicitudes

    # Crear gestor
    gestor = GestorSolicitudes()

    # Ver solicitudes actuales
    solicitudes_antes = gestor.obtener_solicitudes()
    print(f"📊 Solicitudes antes: {len(solicitudes_antes)}")

    # Crear datos de prueba
    grupos_red = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]
    autorizadores_prueba = [
        {
            "nombre": "Juan Carlos",
            "apellido": "González",
            "codigo": "TEST",
            "correo": "juan.gonzalez@test.com",
            "rol": "Supervisor",
        },
        {
            "nombre": "María Elena",
            "apellido": "Rodríguez",
            "codigo": "DEMO",
            "correo": "maria.rodriguez@test.com",
            "rol": "Administrador",
        },
    ]

    # Crear solicitud
    print("\n🔧 Creando nueva solicitud de prueba...")
    try:
        solicitud = gestor.crear_solicitud(grupos_red, autorizadores_prueba)
        print(f"✅ Solicitud creada: {solicitud.id_solicitud}")
        print(f"   Estado: {solicitud.estado.value}")
        print(f"   Autorizadores: {len(solicitud.autorizadores)}")

        # Verificar que se guardó
        gestor.cargar_solicitudes()
        solicitudes_despues = gestor.obtener_solicitudes()
        print(f"\n📊 Solicitudes después: {len(solicitudes_despues)}")

        if len(solicitudes_despues) > len(solicitudes_antes):
            print("✅ La solicitud se guardó correctamente!")

            # Mostrar todas las solicitudes
            print("\n📋 Lista de todas las solicitudes:")
            for i, sol in enumerate(solicitudes_despues, 1):
                print(f"   {i}. {sol.id_solicitud} - {sol.estado.value}")
        else:
            print("❌ La solicitud no se guardó correctamente")

    except Exception as e:
        print(f"❌ Error creando solicitud: {e}")

    print("\n" + "=" * 50)
    print("✅ Prueba completada")
    print("\n📝 Para verificar en la aplicación:")
    print("1. Ejecute la aplicación (ejecutar_app.py)")
    print("2. Vaya a la pestaña 'Gestión de Solicitudes'")
    print("3. Debe ver las solicitudes listadas")
    print("4. Haga doble clic en la columna 'Estado' para editarlo")


if __name__ == "__main__":
    test_crear_solicitud()

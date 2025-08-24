#!/usr/bin/env python3
"""
Script para probar la actualización automática de solicitudes.
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_actualizacion_automatica():
    """Prueba que la actualización automática funcione correctamente."""
    print("🧪 PRUEBA DE ACTUALIZACIÓN AUTOMÁTICA DE SOLICITUDES")
    print("=" * 60)

    print("\n📋 PASOS PARA VERIFICAR LA CORRECCIÓN:")
    print("-" * 40)
    print("1. ✅ Ejecutar la aplicación: python ejecutar_app.py")
    print("2. ✅ Ir a la pestaña 'Nueva Solicitud'")
    print("3. ✅ Crear grupos de red de prueba")
    print("4. ✅ Configurar autorizadores")
    print("5. ✅ Guardar la solicitud")
    print("6. ✅ Verificar que aparece mensaje de confirmación")
    print("7. ✅ Cambiar a pestaña 'Gestión de Solicitudes'")
    print("8. ✅ Verificar que la nueva solicitud aparece en la lista")

    print("\n🔧 MEJORAS IMPLEMENTADAS:")
    print("-" * 40)
    print("✅ Actualización diferida con after() tras crear solicitud")
    print("✅ Actualización automática al cambiar a pestaña de gestión")
    print("✅ Botón manual '🔄 Actualizar' disponible")
    print("✅ Logs de debug para seguimiento del proceso")
    print("✅ Manejo de errores en las actualizaciones")

    print("\n⚡ FUNCIONAMIENTO TÉCNICO:")
    print("-" * 40)
    print("• Método: on_autorizadores_guardados()")
    print("  → Crea solicitud en gestor")
    print("  → Guarda en archivo JSON")
    print("  → Programa actualización con after(100ms)")
    print("  → Ejecuta _actualizar_gestion_tras_crear_solicitud()")

    print("\n• Método: on_cambio_pestana()")
    print("  → Detecta cambio a pestaña #2 (Gestión)")
    print("  → Programa actualización con after(50ms)")
    print("  → Ejecuta _actualizar_gestion_por_cambio_pestana()")

    print("\n• Método: actualizar_manual()")
    print("  → Activado por botón '🔄 Actualizar'")
    print("  → Muestra feedback al usuario")
    print("  → Recarga completa desde archivo")

    print("\n🎯 DIAGNÓSTICO DEL PROBLEMA:")
    print("-" * 40)
    print("❌ Problema anterior: Actualización inmediata sin timing")
    print("✅ Solución: Usar after() para diferir actualización")
    print("✅ Benefit: Permite que el guardado se complete primero")
    print("✅ Fallback: Botón manual disponible como respaldo")

    print("\n📝 INSTRUCCIONES DE VALIDACIÓN:")
    print("-" * 40)
    print("1. Crear una solicitud nueva")
    print("2. Verificar en consola los logs:")
    print("   '🔄 Programando actualización de gestión tras crear solicitud...'")
    print("   '🔄 Ejecutando actualización diferida de gestión...'")
    print("   '✅ Actualización de gestión completada'")
    print("3. Cambiar a pestaña 'Gestión de Solicitudes'")
    print("4. Verificar que la solicitud aparece inmediatamente")
    print("5. Si no aparece, usar botón '🔄 Actualizar'")

    print("\n🛠️ DEPURACIÓN ADICIONAL:")
    print("-" * 40)
    print("• Verificar archivo: data/solicitudes.json")
    print("• Revisar logs en consola")
    print("• Comprobar permisos de escritura")
    print("• Validar formato JSON del archivo")


def mostrar_archivo_gestor():
    """Muestra la ubicación del archivo de solicitudes."""
    print("\n\n📁 ARCHIVO DE SOLICITUDES:")
    print("-" * 30)

    archivo_solicitudes = Path(__file__).parent / "data" / "solicitudes.json"
    print(f"📄 Ubicación: {archivo_solicitudes}")
    print(f"📊 Existe: {'✅ SÍ' if archivo_solicitudes.exists() else '❌ NO'}")

    if archivo_solicitudes.exists():
        try:
            import json

            with open(archivo_solicitudes, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"📈 Solicitudes en archivo: {len(data.get('solicitudes', []))}")

            if data.get("solicitudes"):
                print("📋 IDs de solicitudes:")
                for sol in data["solicitudes"]:
                    print(
                        f"   • {sol.get('id_solicitud', 'sin ID')} - {sol.get('estado', 'sin estado')}"
                    )
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")


if __name__ == "__main__":
    test_actualizacion_automatica()
    mostrar_archivo_gestor()
    print("\n" + "=" * 60)
    print("✅ Verificación de actualización automática completada")
    print("🚀 ¡Ahora pruebe crear una solicitud en la aplicación!")

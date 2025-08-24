#!/usr/bin/env python3
"""
Script para revisar el estado del BD local.
"""

import json
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def revisar_bd_local():
    """Revisa el estado del BD local."""
    print("🔍 REVISIÓN DEL BD LOCAL")
    print("=" * 50)

    # Ubicaciones posibles del BD
    ubicaciones_bd = [
        Path.home() / "Documents" / "MatrizRol_BD" / "solicitudes_conformidad.json",
        Path(__file__).parent / "data" / "solicitudes_conformidad.json",
        Path(__file__).parent / "temp" / "solicitudes_conformidad.json",
    ]

    for i, ubicacion in enumerate(ubicaciones_bd, 1):
        print(f"\n{i}. Ubicación: {ubicacion}")
        print(f"   Existe: {ubicacion.exists()}")

        if ubicacion.exists():
            try:
                with open(ubicacion, "r", encoding="utf-8") as file:
                    contenido = file.read()
                    if contenido.strip():
                        datos = json.loads(contenido)
                        solicitudes = datos.get("solicitudes", [])
                        print(f"   📊 Solicitudes encontradas: {len(solicitudes)}")

                        if solicitudes:
                            print("   📋 Lista de solicitudes:")
                            for sol in solicitudes:
                                print(
                                    f"      - {sol.get('id_solicitud', 'Sin ID')} ({sol.get('estado', 'Sin estado')})"
                                )
                    else:
                        print("   ⚠️ Archivo vacío")

            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")
        else:
            print("   📁 Archivo no existe")

    # Probar crear una instancia del gestor
    print(f"\n🧪 PROBANDO GESTOR DE SOLICITUDES")
    print("-" * 40)

    try:
        from matriz_rol.data.gestor_solicitudes import GestorSolicitudes

        gestor = GestorSolicitudes()
        solicitudes = gestor.obtener_solicitudes()

        print(f"✅ Gestor inicializado correctamente")
        print(f"📊 Solicitudes en memoria: {len(solicitudes)}")

        if solicitudes:
            for sol in solicitudes:
                print(f"   - {sol.id_solicitud} ({sol.estado.value})")

    except Exception as e:
        print(f"❌ Error con el gestor: {e}")


if __name__ == "__main__":
    revisar_bd_local()

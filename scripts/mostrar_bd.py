#!/usr/bin/env python3
"""
Script para mostrar la ubicación de la base de datos del proyecto.
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_solicitudes import GestorSolicitudes


def mostrar_ubicacion_bd():
    """Muestra dónde está ubicada la base de datos."""
    print("📍 UBICACIÓN DE LA BASE DE DATOS")
    print("=" * 50)

    try:
        # Crear instancia del gestor para ver dónde se ubica la BD
        gestor = GestorSolicitudes()

        print(f"\n📂 Directorio BD: {gestor.directorio_bd}")
        print(f"📄 Archivo principal: {gestor.archivo_solicitudes}")
        print(f"💾 Archivo backup: {gestor.archivo_backup}")

        print(f"\n🔍 ESTADO DE LOS ARCHIVOS:")
        print(
            f"   Archivo principal existe: {'✅ SÍ' if gestor.archivo_solicitudes.exists() else '❌ NO'}"
        )
        print(
            f"   Archivo backup existe: {'✅ SÍ' if gestor.archivo_backup.exists() else '❌ NO'}"
        )

        if gestor.archivo_solicitudes.exists():
            import json

            with open(gestor.archivo_solicitudes, "r", encoding="utf-8") as f:
                data = json.load(f)
            solicitudes_count = len(data.get("solicitudes", []))
            print(f"   Número de solicitudes: {solicitudes_count}")

        print(f"\n📏 TAMAÑOS DE ARCHIVO:")
        if gestor.archivo_solicitudes.exists():
            size_kb = gestor.archivo_solicitudes.stat().st_size / 1024
            print(f"   Archivo principal: {size_kb:.2f} KB")

        if gestor.archivo_backup.exists():
            size_kb = gestor.archivo_backup.stat().st_size / 1024
            print(f"   Archivo backup: {size_kb:.2f} KB")

        # Mostrar ubicaciones alternativas
        print(f"\n🔄 UBICACIONES ALTERNATIVAS VERIFICADAS:")

        # Documentos del usuario
        docs_path = Path.home() / "Documents" / "MatrizRol_BD"
        print(f"   📁 Documentos: {docs_path}")
        print(f"      Accesible: {'✅ SÍ' if docs_path.exists() else '❌ NO'}")

        # Proyecto local
        proyecto_path = Path(__file__).parent / "data" / "bd_local"
        print(f"   📁 Proyecto: {proyecto_path}")
        print(f"      Accesible: {'✅ SÍ' if proyecto_path.exists() else '❌ NO'}")

        # Temporal
        import tempfile

        temp_path = Path(tempfile.gettempdir()) / "MatrizRol_BD"
        print(f"   📁 Temporal: {temp_path}")
        print(f"      Accesible: {'✅ SÍ' if temp_path.exists() else '❌ NO'}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    mostrar_ubicacion_bd()

#!/usr/bin/env python3
"""
Script para migrar estados de solicitudes del formato antiguo al nuevo.

Migra:
- 'abierta' -> 'En solicitud de conformidades'
- 'cerrada' -> 'Cerrado'
- 'en_proceso' -> 'En Helpdesk'
"""

import json
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def migrar_estados_bd():
    """Migra los estados antiguos a los nuevos en el BD local."""

    # Ubicaciones del BD
    ubicaciones_bd = [
        Path.home() / "Documents" / "MatrizRol_BD" / "solicitudes_conformidad.json",
        Path(__file__).parent / "data" / "solicitudes_conformidad.json",
        Path(__file__).parent / "temp" / "solicitudes_conformidad.json",
    ]

    # Mapeo de estados antiguos a nuevos
    mapeo_estados = {
        "abierta": "En solicitud de conformidades",
        "cerrada": "Cerrado",
        "en_proceso": "En Helpdesk",
    }

    archivo_encontrado = None
    for ubicacion in ubicaciones_bd:
        if ubicacion.exists():
            archivo_encontrado = ubicacion
            break

    if not archivo_encontrado:
        print("❌ No se encontró archivo de BD para migrar")
        return False

    print(f"📂 Migrando BD desde: {archivo_encontrado}")

    try:
        # Cargar datos actuales
        with open(archivo_encontrado, "r", encoding="utf-8") as file:
            datos = json.load(file)

        migraciones_realizadas = 0

        # Migrar cada solicitud
        for solicitud_data in datos.get("solicitudes", []):
            estado_actual = solicitud_data.get("estado", "")

            # Si el estado está en formato antiguo, migrarlo
            if estado_actual in mapeo_estados:
                nuevo_estado = mapeo_estados[estado_actual]
                solicitud_data["estado"] = nuevo_estado
                migraciones_realizadas += 1
                print(
                    f"  ✅ {solicitud_data.get('id_solicitud', 'Sin ID')}: '{estado_actual}' -> '{nuevo_estado}'"
                )

        if migraciones_realizadas > 0:
            # Crear backup antes de migrar
            backup_path = (
                archivo_encontrado.parent
                / f"backup_antes_migracion_{archivo_encontrado.name}"
            )
            with open(backup_path, "w", encoding="utf-8") as backup_file:
                json.dump(datos, backup_file, indent=2, ensure_ascii=False)
            print(f"💾 Backup creado: {backup_path}")

            # Guardar datos migrados
            with open(archivo_encontrado, "w", encoding="utf-8") as file:
                json.dump(datos, file, indent=2, ensure_ascii=False)

            print(
                f"✅ Migración completada: {migraciones_realizadas} solicitudes migradas"
            )
        else:
            print("ℹ️  No hay solicitudes que migrar")

        return True

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False


if __name__ == "__main__":
    print("🔄 Iniciando migración de estados...")
    if migrar_estados_bd():
        print("✅ Migración completada exitosamente")
    else:
        print("❌ Error en la migración")

#!/usr/bin/env python3
"""
Script para migrar la base de datos desde Documents a la raíz del proyecto.
"""

import shutil
from pathlib import Path
import json


def migrar_base_datos():
    """Migra la base de datos desde Documents al directorio del proyecto."""

    print("🔄 MIGRACIÓN DE BASE DE DATOS")
    print("=" * 50)

    # Rutas
    proyecto_root = Path(__file__).parent.parent
    origen_bd = Path.home() / "Documents" / "MatrizRol_BD"
    destino_bd = proyecto_root / "data"

    print(f"📂 Origen: {origen_bd}")
    print(f"📁 Destino: {destino_bd}")

    # Crear directorio destino
    destino_bd.mkdir(parents=True, exist_ok=True)

    # Verificar si existe la BD en Documents
    if not origen_bd.exists():
        print("❌ No se encontró la base de datos en Documents")
        return False

    # Listar archivos a migrar
    archivos_bd = list(origen_bd.glob("*.json"))
    print(f"\n📋 Archivos encontrados: {len(archivos_bd)}")

    for archivo in archivos_bd:
        print(f"   📄 {archivo.name} ({archivo.stat().st_size} bytes)")

    if not archivos_bd:
        print("❌ No se encontraron archivos de base de datos")
        return False

    # Realizar migración automáticamente
    print("\n🔄 Iniciando migración automática...")

    archivos_migrados = 0
    for archivo in archivos_bd:
        try:
            destino_archivo = destino_bd / archivo.name

            # Crear backup si ya existe
            if destino_archivo.exists():
                backup_archivo = destino_bd / f"{archivo.stem}_backup_{archivo.suffix}"
                shutil.copy2(destino_archivo, backup_archivo)
                print(f"   💾 Backup creado: {backup_archivo.name}")

            # Copiar archivo
            shutil.copy2(archivo, destino_archivo)
            print(f"   ✅ Migrado: {archivo.name}")
            archivos_migrados += 1

            # Verificar integridad del JSON
            if archivo.suffix == ".json":
                try:
                    with open(destino_archivo, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    print(
                        f"      🔍 JSON válido: {len(data.get('solicitudes', []))} solicitudes"
                    )
                except json.JSONDecodeError as e:
                    print(f"      ⚠️ Advertencia JSON: {e}")

        except Exception as e:
            print(f"   ❌ Error migrando {archivo.name}: {e}")

    print(f"\n✅ Migración completada: {archivos_migrados}/{len(archivos_bd)} archivos")

    # Verificar nueva ubicación
    print("\n🔍 Verificando nueva ubicación...")
    nuevo_archivo_principal = destino_bd / "solicitudes_conformidad.json"

    if nuevo_archivo_principal.exists():
        with open(nuevo_archivo_principal, "r", encoding="utf-8") as f:
            data = json.load(f)
        solicitudes_count = len(data.get("solicitudes", []))
        print(f"   ✅ Archivo principal: {solicitudes_count} solicitudes")

        # Mostrar primera solicitud como ejemplo
        if data.get("solicitudes"):
            primera = data["solicitudes"][0]
            print(
                f"   📄 Ejemplo: {primera.get('id_solicitud', 'sin ID')} - {primera.get('estado', 'sin estado')}"
            )

    print(f"\n📍 Nueva ubicación de BD: {destino_bd}")
    print("🎯 La aplicación ahora usará esta ubicación automáticamente")

    # Conservar archivos originales como backup
    print(f"\n💾 Archivos originales conservados en {origen_bd} como backup")

    return True


if __name__ == "__main__":
    success = migrar_base_datos()

    if success:
        print("\n" + "=" * 50)
        print("✅ MIGRACIÓN EXITOSA")
        print("🚀 Reinicie la aplicación para usar la nueva ubicación")
    else:
        print("\n" + "=" * 50)
        print("❌ MIGRACIÓN FALLIDA")

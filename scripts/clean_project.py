#!/usr/bin/env python3
"""
Script de limpieza del proyecto - Elimina archivos temporales y de prueba.
"""

import os
import shutil
from pathlib import Path


def limpiar_archivos_temporales():
    """Elimina archivos temporales y de prueba del proyecto."""

    archivos_a_eliminar = [
        "test_actualizacion.py",
        "test_bd_local.py",
        "test_botones.py",
        "test_correcciones.py",
        "test_crear_solicitud.py",
        "test_edicion_grilla.py",
        "test_nuevos_estados.py",
        "cleanup.py",
        "migrar_estados.py",
        "revisar_bd.py",
    ]

    directorios_a_limpiar = [
        ".benchmarks",
        ".mypy_cache",
        ".pytest_cache",
        "backup_unused",
    ]

    proyecto_root = Path(__file__).parent

    print("🧹 LIMPIEZA DEL PROYECTO")
    print("=" * 50)

    # Eliminar archivos temporales
    print("\n📄 Eliminando archivos temporales:")
    for archivo in archivos_a_eliminar:
        archivo_path = proyecto_root / archivo
        if archivo_path.exists():
            archivo_path.unlink()
            print(f"   ✅ Eliminado: {archivo}")
        else:
            print(f"   ⚪ No existe: {archivo}")

    # Limpiar directorios cache
    print("\n📁 Limpiando directorios cache:")
    for directorio in directorios_a_limpiar:
        dir_path = proyecto_root / directorio
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   ✅ Eliminado: {directorio}")
        else:
            print(f"   ⚪ No existe: {directorio}")

    # Limpiar __pycache__ recursivamente
    print("\n🐍 Limpiando archivos __pycache__:")
    for pycache in proyecto_root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"   ✅ Eliminado: {pycache.relative_to(proyecto_root)}")

    # Limpiar archivos .pyc
    for pyc_file in proyecto_root.rglob("*.pyc"):
        pyc_file.unlink()
        print(f"   ✅ Eliminado: {pyc_file.relative_to(proyecto_root)}")

    print("\n✅ Limpieza completada!")


if __name__ == "__main__":
    limpiar_archivos_temporales()

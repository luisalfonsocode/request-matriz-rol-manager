#!/usr/bin/env python3
"""Script para limpiar archivos no utilizados del proyecto."""

import os
import shutil
from pathlib import Path


def cleanup_project():
    """Elimina archivos y directorios no utilizados."""

    project_root = Path(__file__).parent

    # Archivos específicos a eliminar
    files_to_remove = [
        project_root / "src" / "matriz_rol" / "gui" / "autorizadores.py",
        project_root / "src" / "matriz_rol" / "gui" / "autorizadores_clean.py",
    ]

    # Directorios a eliminar
    dirs_to_remove = [
        project_root / "demo_treeview",
        project_root / "examples",
        project_root / "typings",
    ]

    # Patrones de cache a eliminar
    cache_patterns = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        ".mypy_cache",
    ]

    print("🧹 Iniciando limpieza del proyecto...")

    # Eliminar archivos específicos
    for file_path in files_to_remove:
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"✅ Eliminado: {file_path}")
            except Exception as e:
                print(f"❌ Error eliminando {file_path}: {e}")
        else:
            print(f"⚠️  No encontrado: {file_path}")

    # Eliminar directorios
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Eliminado directorio: {dir_path}")
            except Exception as e:
                print(f"❌ Error eliminando directorio {dir_path}: {e}")
        else:
            print(f"⚠️  Directorio no encontrado: {dir_path}")

    # Eliminar cache de Python recursivamente
    for root, dirs, files in os.walk(project_root):
        # Eliminar directorios __pycache__
        if "__pycache__" in dirs:
            pycache_path = Path(root) / "__pycache__"
            try:
                shutil.rmtree(pycache_path)
                print(f"✅ Eliminado cache: {pycache_path}")
            except Exception as e:
                print(f"❌ Error eliminando cache {pycache_path}: {e}")

        # Eliminar archivos .pyc
        for file in files:
            if file.endswith(".pyc"):
                pyc_path = Path(root) / file
                try:
                    pyc_path.unlink()
                    print(f"✅ Eliminado .pyc: {pyc_path}")
                except Exception as e:
                    print(f"❌ Error eliminando .pyc {pyc_path}: {e}")

    print("✨ Limpieza completada!")


if __name__ == "__main__":
    cleanup_project()

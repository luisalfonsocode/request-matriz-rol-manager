"""
Script para probar la nueva aplicación completa con 3 pestañas.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
proyecto_root = Path(__file__).parent.parent
src_path = proyecto_root / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.gui.aplicacion_principal import main

if __name__ == "__main__":
    print("🚀 Iniciando aplicación completa de Gestión de Matrices de Rol...")
    print("📋 Pestañas disponibles:")
    print("  1. Nueva Solicitud - Crear nuevas solicitudes")
    print("  2. Editar Autorizadores - Completar datos y generar correos")
    print("  3. Gestión de Solicitudes - Hacer seguimiento y control")
    print("\n▶️ Abriendo aplicación...")

    try:
        main()
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        import traceback

        traceback.print_exc()

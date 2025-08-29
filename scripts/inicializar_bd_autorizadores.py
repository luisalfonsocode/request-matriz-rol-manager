"""
Script para inicializar la base de datos de autorizadores.
Ejecutar una vez para crear la BD inicial.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path para las importaciones
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_autorizadores import GestorAutorizadores


def main():
    """Inicializa la base de datos de autorizadores."""
    print("🔄 Inicializando base de datos de autorizadores...")

    gestor = GestorAutorizadores()

    # La BD se crea automáticamente al instanciar el gestor
    info = gestor.obtener_info_bd()

    print(f"✅ BD de autorizadores inicializada:")
    print(f"   📁 Ubicación: {info['ruta']}")
    print(f"   📊 Total aplicaciones: {info['total_aplicaciones']}")
    print(f"   📋 Aplicaciones: {', '.join(info['aplicaciones'])}")
    print(f"   ✅ Autorizadores activos: {info['activos']}")


if __name__ == "__main__":
    main()

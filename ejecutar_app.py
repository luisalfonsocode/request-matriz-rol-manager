#!/usr/bin/env python3
"""
Script de entrada para ejecutar la aplicación de matriz de roles.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path para las importaciones
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Importar y ejecutar la aplicación
from matriz_rol.gui.aplicacion_principal import main

if __name__ == "__main__":
    main()

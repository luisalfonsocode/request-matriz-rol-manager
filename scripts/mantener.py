"""Script para ejecutar las operaciones de mantenimiento."""

import subprocess
import sys
from pathlib import Path


def main():
    """Ejecuta todas las operaciones de mantenimiento."""
    # Obtener la ruta del proyecto
    proyecto_path = Path(__file__).parent.parent

    print("🔄 Ejecutando operaciones de mantenimiento...")

    try:
        # Formatear código
        print("\n📝 Formateando código...")
        subprocess.run(["black", "src", "tests"], check=True)
        subprocess.run(["isort", "src", "tests"], check=True)

        # Ejecutar linters
        print("\n🔍 Ejecutando linters...")
        subprocess.run(["flake8", "src", "tests"], check=True)
        subprocess.run(["pylint", "src", "tests"], check=True)
        subprocess.run(["mypy", "src", "tests"], check=True)
        subprocess.run(["ruff", "check", "src", "tests"], check=True)

        # Ejecutar tests con cobertura
        print("\n🧪 Ejecutando tests...")
        subprocess.run(["pytest", "--cov=src", "--cov-report=term-missing"], check=True)

        # Verificar seguridad
        print("\n🔒 Verificando seguridad...")
        subprocess.run(["bandit", "-r", "src"], check=True)
        subprocess.run(["safety", "check"], check=True)

        print("\n✅ Todas las operaciones completadas exitosamente!")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error en la operación: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Script para mostrar ejemplos de nombres de archivos MSG generados.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar el directorio src al path
proyecto_root = Path(__file__).parent.parent
src_path = proyecto_root / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.email.generador_correos_individuales import GeneradorCorreosIndividuales


def main():
    """Muestra ejemplos de nombres de archivos que se generarían."""
    print("📁 EJEMPLOS DE NOMBRES DE ARCHIVOS MSG GENERADOS")
    print("=" * 55)

    # Datos de ejemplo
    datos_autorizadores = [
        {
            "codigo": "APF2",
            "autorizador": "Daniela Fernanda Ortiz",
            "correo": "daniela.ortiz@empresa.com",
        },
        {
            "codigo": "QASD",
            "autorizador": "Sebastián Eduardo Martín",
            "correo": "sebastian.martin@corp.co",
        },
        {
            "codigo": "SSSS",
            "autorizador": "Ricardo Antonio Jiménez",
            "correo": "ricardo.jimenez@global.org",
        },
        {
            "codigo": "CASD",
            "autorizador": "Isabella Camila Rojas",
            "correo": "isabella.rojas@tech.net",
        },
        {
            "codigo": "FCVE",
            "autorizador": "Paola Carolina Díaz",
            "correo": "paola.diaz@solutions.com",
        },
        {
            "codigo": "ATLA",
            "autorizador": "Laura Cristina Torres",
            "correo": "laura.torres@innovate.co",
        },
        {
            "codigo": "FIEC",
            "autorizador": "Fernando Gabriel Ruiz",
            "correo": "fernando.ruiz@business.org",
        },
    ]

    # Crear instancia del generador
    generador = GeneradorCorreosIndividuales()
    fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M")

    print(f"🕐 Fecha/Hora de generación: {fecha_archivo}")
    print(f"📂 Ubicación: {generador.directorio_salida}")
    print("\n📧 Archivos que se generarían:")
    print("-" * 55)

    for i, autorizador in enumerate(datos_autorizadores, 1):
        # Simular el nombre que se generaría
        nombre_limpio = generador._limpiar_nombre_archivo(autorizador["autorizador"])
        codigo = autorizador["codigo"]
        nombre_archivo = (
            f"{i:02d}_Conformidad_{codigo}_{nombre_limpio}_{fecha_archivo}.msg"
        )

        print(f"  {i}. {nombre_archivo}")
        print(f"     📤 Para: {autorizador['autorizador']} ({autorizador['correo']})")
        print(
            f"     📋 Asunto: 🔐 Solicitud de Conformidad [{codigo}] - Matriz de Roles - ACCIÓN REQUERIDA"
        )
        print()

    print("✨ VENTAJAS DE ESTA NOMENCLATURA:")
    print("  ✅ Numeración secuencial para orden")
    print("  ✅ 'Conformidad' identifica el tipo de solicitud")
    print("  ✅ Código de aplicación para identificación rápida")
    print("  ✅ Nombre del autorizador para contacto")
    print("  ✅ Fecha y hora de generación")
    print("\n🎯 ¡Fácil de organizar y buscar en cualquier carpeta!")


if __name__ == "__main__":
    main()

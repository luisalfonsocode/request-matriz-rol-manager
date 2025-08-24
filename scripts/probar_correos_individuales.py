"""
Script para probar la generación de correos MSG individuales.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
proyecto_root = Path(__file__).parent.parent
src_path = proyecto_root / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.email.generador_correos_individuales import GeneradorCorreosIndividuales


def main():
    """Prueba la generación de correos individuales."""
    print("🧪 Probando generación de correos MSG individuales...")

    # Datos de prueba
    datos_autorizadores = [
        {
            "codigo": "APF2",
            "autorizador": "Daniela Fernanda Ortiz",
            "correo": "daniela.ortiz@empresa.com",
        },
        {
            "codigo": "QASD",
            "autorizador": "Sebastián Eduardo Martín",
            "correo": "sebastian.martin@corporacion.co",
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
    ]

    grupos_red = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]

    # Generar correos
    generador = GeneradorCorreosIndividuales()

    try:
        archivos_generados = generador.generar_correos_individuales(
            datos_autorizadores, grupos_red
        )

        print(f"\n✅ ¡Proceso completado exitosamente!")
        print(f"📧 {len(archivos_generados)} correos generados")
        print(f"📁 Ubicación: {generador.directorio_salida}")
        print("\n📋 Archivos generados:")
        for i, archivo in enumerate(archivos_generados, 1):
            print(f"  {i}. {os.path.basename(archivo)}")

        # Abrir carpeta de destino
        print(f"\n🔗 Abriendo carpeta: {generador.directorio_salida}")
        os.startfile(str(generador.directorio_salida))

    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

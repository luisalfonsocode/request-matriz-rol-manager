"""
Script para generar un correo de ejemplo y mostrar el formato.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from matriz_rol.email import generar_correo_desde_datos


def mostrar_formato_correo():
    """Genera un correo de ejemplo para mostrar el formato."""

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
            "correo": "sebastian.martin@corporacion.co",
        },
        {
            "codigo": "SSSS",
            "autorizador": "Ricardo Antonio Jiménez",
            "correo": "ricardo.jimenez@global.org",
        },
    ]

    grupos_red = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]

    try:
        archivo_correo = generar_correo_desde_datos(datos_autorizadores, grupos_red)
        print(f"✅ Correo de ejemplo generado en: {archivo_correo}")

        # Leer y mostrar el contenido
        with open(archivo_correo, "r", encoding="utf-8") as file:
            contenido = file.read()

        print("\n" + "=" * 80)
        print("📧 FORMATO DEL CORREO GENERADO:")
        print("=" * 80)
        print(contenido)
        print("=" * 80)

        return archivo_correo

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    mostrar_formato_correo()

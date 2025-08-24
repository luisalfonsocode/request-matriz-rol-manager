"""
Script para sobreescribir con datos ficticios completos.
"""

import json
from pathlib import Path


def crear_datos_completos():
    """Crea un conjunto completo de datos ficticios."""

    datos_completos = {
        "APF2": {
            "autorizador": "Daniela Fernanda Ortiz",
            "correo": "daniela.ortiz@empresa.com",
        },
        "QASD": {
            "autorizador": "Sebastián Eduardo Martín",
            "correo": "sebastian.martin@corporacion.co",
        },
        "SSSS": {
            "autorizador": "Ricardo Antonio Jiménez",
            "correo": "ricardo.jimenez@global.org",
        },
        "CASD": {
            "autorizador": "Isabella Camila Rojas",
            "correo": "isabella.rojas@tech.net",
        },
        "FCVE": {
            "autorizador": "Paola Carolina Díaz",
            "correo": "paola.diaz@solutions.com",
        },
        "ATLA": {
            "autorizador": "Laura Cristina Torres",
            "correo": "laura.torres@innovate.co",
        },
        "FIEC": {
            "autorizador": "Fernando Gabriel Ruiz",
            "correo": "fernando.ruiz@business.org",
        },
    }

    return datos_completos


def main():
    # Ruta del archivo
    archivo_datos = (
        Path(__file__).parent.parent
        / "src"
        / "matriz_rol"
        / "data"
        / "autorizadores_datos.json"
    )

    # Crear directorio si no existe
    archivo_datos.parent.mkdir(parents=True, exist_ok=True)

    # Generar y guardar datos
    datos = crear_datos_completos()

    with open(archivo_datos, "w", encoding="utf-8") as file:
        json.dump(datos, file, indent=2, ensure_ascii=False)

    print("✅ Datos ficticios completos guardados!")
    print(f"📁 Archivo: {archivo_datos}")
    print("\n📋 Datos guardados:")

    for codigo, info in datos.items():
        print(f"  {codigo}: {info['autorizador']} - {info['correo']}")


if __name__ == "__main__":
    main()

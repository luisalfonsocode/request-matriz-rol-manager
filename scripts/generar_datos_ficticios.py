"""
Script para generar datos ficticios de autorizadores.

Este script crea nombres y correos electrónicos ficticios para los códigos
de aplicación y los guarda en el archivo de persistencia.
"""

import json
import random
from pathlib import Path


def generar_datos_ficticios():
    """Genera datos ficticios de autorizadores."""

    # Nombres ficticios
    nombres = [
        "Juan Carlos Pérez",
        "María Elena González",
        "Carlos Roberto Silva",
        "Ana Patricia López",
        "Diego Fernando Morales",
        "Laura Cristina Torres",
        "Ricardo Antonio Jiménez",
        "Sofía Alejandra Vargas",
        "Andrés Felipe Castro",
        "Isabella Camila Rojas",
        "Miguel Ángel Herrera",
        "Valentina Lucía Santos",
        "Santiago David Mendoza",
        "Camila Andrea Restrepo",
        "Alejandro José Ramírez",
        "Natalia Esperanza Gómez",
        "Sebastián Eduardo Martín",
        "Paola Carolina Díaz",
        "Fernando Gabriel Ruiz",
        "Daniela Fernanda Ortiz",
        "Luis Alberto Guerrero",
        "Mariana Isabel Campos",
        "Javier Esteban Moreno",
        "Carolina Victoria Cruz",
        "Emilio Rafael Vásquez",
        "Gabriela Antonia Núñez",
        "Nicolás Alejandro Peña",
        "Adriana Catalina Soto",
        "Rodrigo Mauricio Aguilar",
        "Lucía Esperanza Molina",
    ]

    # Dominios de correo empresariales ficticios
    dominios = [
        "empresa.com",
        "corporacion.co",
        "global.org",
        "tech.net",
        "solutions.com",
        "innovate.co",
        "business.org",
        "systems.net",
        "consulting.com",
        "group.co",
    ]

    # Códigos de aplicación (basados en los grupos predefinidos)
    codigos_aplicacion = ["APF2", "QASD", "SSSS", "CASD", "FCVE", "ATLA", "FIEC"]

    # Generar datos para cada código
    datos_autorizadores = {}

    for codigo in codigos_aplicacion:
        # Seleccionar nombre aleatorio
        nombre = random.choice(nombres)
        nombres.remove(nombre)  # Evitar duplicados

        # Generar correo basado en el nombre
        partes_nombre = nombre.lower().split()
        primer_nombre = partes_nombre[0]
        apellido = partes_nombre[-1]
        dominio = random.choice(dominios)

        # Formato de correo: nombre.apellido@dominio
        correo = f"{primer_nombre}.{apellido}@{dominio}"

        datos_autorizadores[codigo] = {"autorizador": nombre, "correo": correo}

    return datos_autorizadores


def guardar_datos_ficticios():
    """Guarda los datos ficticios en el archivo de persistencia."""

    # Ruta del archivo de datos
    directorio_datos = Path(__file__).parent.parent / "matriz_rol" / "data"
    archivo_datos = directorio_datos / "autorizadores_datos.json"

    # Asegurar que el directorio existe
    directorio_datos.mkdir(parents=True, exist_ok=True)

    # Generar datos
    datos = generar_datos_ficticios()

    try:
        # Guardar en archivo JSON
        with open(archivo_datos, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)

        print("✅ Datos ficticios generados exitosamente!")
        print(f"📁 Archivo guardado en: {archivo_datos}")
        print("\n📋 Datos generados:")
        print("-" * 50)

        for codigo, info in datos.items():
            print(f"Código: {codigo}")
            print(f"  Autorizador: {info['autorizador']}")
            print(f"  Correo: {info['correo']}")
            print()

        return True

    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Generando datos ficticios de autorizadores...")
    print()

    if guardar_datos_ficticios():
        print(
            "✨ ¡Listo! Ahora puedes abrir la aplicación y verás los datos precargados."
        )
        print(
            "💡 Tip: Puedes usar el botón 'Limpiar Datos Guardados' para empezar de nuevo."
        )
    else:
        print("💥 Algo salió mal. Revisa los errores arriba.")

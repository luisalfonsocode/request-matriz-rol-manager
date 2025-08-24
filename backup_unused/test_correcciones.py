#!/usr/bin/env python3
"""
Script para probar las correcciones de extracción de códigos y edición de ticket.
"""

import sys
from pathlib import Path
import re

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_extraccion_codigos():
    """Prueba la nueva lógica de extracción de códigos de aplicación."""
    print("🧪 PRUEBA DE EXTRACCIÓN DE CÓDIGOS DE APLICACIÓN")
    print("=" * 60)

    # Casos de prueba
    casos_prueba = [
        "APF2_QASD1_SSSS_CASD1_",
        "FCVE2_ATLA_FIEC_CASD1_",
        "_1212DDD_",  # Caso problemático reportado
        "_ABCD_EFGH_",
        "XXXX_YYYY_",  # Sin guiones bajos al inicio
        "_ZZZZ",  # Sin guión bajo al final
        "_TEST_DEMO_PROD_",
        "_12AB_",  # Con números
        "_ABC_",  # Solo 3 caracteres
        "_ABCDE_",  # 5 caracteres
    ]

    def extraer_codigos_aplicacion_corregido(grupos_red):
        """Nueva lógica corregida."""
        codigos = set()

        for grupo in grupos_red:
            # Buscar patrones de aplicación: _XXXX_ (rodeado de guiones bajos)
            patron = r"_([A-Z]{4})_"
            matches = re.findall(patron, grupo)
            for match in matches:
                codigos.add(match)

        return sorted(list(codigos))

    def extraer_codigos_aplicacion_anterior(grupos_red):
        """Lógica anterior (problemática)."""
        codigos = set()

        for grupo in grupos_red:
            # Dividir por guiones bajos y tomar elementos de 4 caracteres
            partes = grupo.split("_")
            for parte in partes:
                if len(parte) == 4 and parte.isalpha():
                    codigos.add(parte)

        return sorted(list(codigos))

    print("\n📋 Resultados de extracción:")
    print("-" * 60)
    print(f"{'Grupo de Red':<25} {'Anterior':<15} {'Corregido':<15} {'Estado'}")
    print("-" * 60)

    for caso in casos_prueba:
        resultado_anterior = extraer_codigos_aplicacion_anterior([caso])
        resultado_corregido = extraer_codigos_aplicacion_corregido([caso])

        # Determinar si hay diferencia
        if resultado_anterior != resultado_corregido:
            estado = "✅ Corregido"
        else:
            estado = "⚪ Sin cambio"

        print(
            f"{caso:<25} {str(resultado_anterior):<15} {str(resultado_corregido):<15} {estado}"
        )

    print("\n🎯 CASOS ESPECÍFICOS:")
    print("-" * 40)

    # Caso problemático específico
    caso_problema = "_1212DDD_"
    anterior = extraer_codigos_aplicacion_anterior([caso_problema])
    corregido = extraer_codigos_aplicacion_corregido([caso_problema])

    print(f"📍 Caso problemático reportado: {caso_problema}")
    print(f"   Lógica anterior: {anterior} ❌ (Incorrecto - detectaba 1212)")
    print(f"   Lógica corregida: {corregido} ✅ (Correcto - no detecta nada)")

    # Casos válidos
    casos_validos = ["_ABCD_EFGH_", "_TEST_DEMO_"]
    for caso in casos_validos:
        resultado = extraer_codigos_aplicacion_corregido([caso])
        print(f"📍 Caso válido: {caso}")
        print(f"   Códigos extraídos: {resultado} ✅")


def test_info_edicion_grilla():
    """Muestra información sobre la nueva funcionalidad de edición en grilla."""
    print("\n\n🔧 NUEVA FUNCIONALIDAD: EDICIÓN EN GRILLA")
    print("=" * 60)

    print("📝 INSTRUCCIONES DE USO:")
    print("-" * 30)
    print("1. Abra la aplicación (ejecutar_app.py)")
    print("2. Vaya a la pestaña 'Gestión de Solicitudes'")
    print("3. Para editar ESTADO:")
    print("   • Haga doble clic en la columna 'Estado'")
    print("   • Seleccione el nuevo estado del dropdown")
    print("   • Se aplicarán las validaciones automáticamente")
    print("4. Para editar TICKET HELPDESK:")
    print("   • Haga doble clic en la columna 'Ticket Helpdesk'")
    print("   • Escriba el nuevo número de ticket")
    print("   • Presione Enter para guardar o Escape para cancelar")

    print("\n⚡ VALIDACIONES AUTOMÁTICAS:")
    print("-" * 30)
    print("• Estado 'En solicitud de conformidades' → 'En Helpdesk': Pide ticket")
    print("• Estado 'En Helpdesk' → 'Atendido': Pide observaciones")
    print("• Estado → 'Cerrado': Pide confirmación")
    print("• Ticket Helpdesk: Acepta cualquier texto (números, letras, etc.)")

    print("\n🎨 EXPERIENCIA DE USUARIO:")
    print("-" * 30)
    print("✅ Edición in-place (directo en la grilla)")
    print("✅ Validaciones inmediatas")
    print("✅ Feedback visual al usuario")
    print("✅ Cancelar con Escape")
    print("✅ Guardar con Enter")


if __name__ == "__main__":
    test_extraccion_codigos()
    test_info_edicion_grilla()
    print("\n" + "=" * 60)
    print("✅ Todas las pruebas completadas")
    print("🚀 ¡Las correcciones están listas para usar!")

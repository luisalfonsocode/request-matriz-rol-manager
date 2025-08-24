"""
Script de prueba para verificar la base de datos de autorizadores.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path para las importaciones
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_autorizadores import GestorAutorizadores


def test_autorizadores():
    """Prueba la funcionalidad de la BD de autorizadores."""
    print("🧪 Probando base de datos de autorizadores...")

    gestor = GestorAutorizadores()

    # Obtener información general
    print("\n📊 Información de la BD:")
    info = gestor.obtener_info_bd()
    for clave, valor in info.items():
        print(f"   {clave}: {valor}")

    # Probar consulta por códigos específicos (como en solicitud)
    print("\n🔍 Consultando autorizadores para códigos de solicitud:")
    codigos_prueba = ["APF2", "FCVE", "QASD", "ATLA"]
    autorizadores = gestor.obtener_autorizadores_por_codigos(codigos_prueba)

    for auth in autorizadores:
        print(f"   ✅ {auth['codigo']}: {auth['autorizador']} ({auth['correo']})")

    # Simular consulta como si fuera para una solicitud específica
    print(f"\n📋 Total autorizadores para esta solicitud: {len(autorizadores)}")

    # Probar un código que no existe
    print("\n❓ Probando código inexistente:")
    auth_no_existe = gestor.obtener_autorizador_por_codigo("ZZZZ")
    print(f"   Resultado: {auth_no_existe}")


if __name__ == "__main__":
    test_autorizadores()

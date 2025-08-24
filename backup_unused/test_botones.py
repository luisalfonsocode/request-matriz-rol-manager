"""
Script de prueba para verificar funcionalidad de botones.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from matriz_rol.data.gestor_solicitudes import GestorSolicitudes


def probar_botones():
    print("🧪 PROBANDO FUNCIONALIDAD DE BOTONES")
    print("=" * 50)

    gestor = GestorSolicitudes()

    # Probar método de obtener info BD (usado por botón actualizar)
    print("\n🔄 PROBANDO FUNCIONALIDAD DEL BOTÓN ACTUALIZAR:")
    info = gestor.obtener_info_bd()
    for clave, valor in info.items():
        print(f"   {clave}: {valor}")

    # Probar método de exportar CSV (usado por botón exportar)
    print("\n📁 PROBANDO FUNCIONALIDAD DEL BOTÓN EXPORTAR:")
    archivo_prueba = Path("test_export.csv")

    if gestor.obtener_solicitudes():
        exito = gestor.exportar_solicitudes_csv(archivo_prueba)
        if exito and archivo_prueba.exists():
            print(f"   ✅ Exportación exitosa: {archivo_prueba}")
            print(f"   📄 Tamaño del archivo: {archivo_prueba.stat().st_size} bytes")

            # Leer las primeras líneas para verificar
            with open(archivo_prueba, "r", encoding="utf-8") as f:
                lineas = f.readlines()[:3]
                print(f"   📋 Primeras líneas del CSV:")
                for i, linea in enumerate(lineas):
                    print(f"      {i+1}: {linea.strip()}")

            # Limpiar archivo de prueba
            archivo_prueba.unlink()
        else:
            print("   ❌ Error en exportación")
    else:
        print("   ⚠️ No hay solicitudes para exportar")

    print("\n✅ PRUEBA DE BOTONES COMPLETADA")


if __name__ == "__main__":
    probar_botones()

"""Modulo de ejemplo para demostrar type hints."""

from typing import Dict, List, Optional, Union


def procesar_datos(
    nombre: str,
    edad: int,
    notas: List[float],
    metadata: Optional[Dict[str, str]] = None,
) -> Union[float, None]:
    """Procesa datos de un estudiante.

    Args:
        nombre: Nombre del estudiante
        edad: Edad del estudiante
        notas: Lista de calificaciones
        metadata: Informacion adicional opcional

    Returns:
        El promedio de las notas o None si no hay notas
    """
    if not notas:
        return None

    # VS Code verificará todos estos tipos
    promedio: float = sum(notas) / len(notas)

    if metadata:
        print(f"Información adicional para {nombre}: {metadata}")

    # VS Code verificará que la edad sea usada como int
    if edad < 18:
        print("Estudiante menor de edad")

    return promedio


# Ejemplos de uso con verificación de tipos
estudiante_notas: List[float] = [8.5, 9.0, 7.5]
info_adicional: Dict[str, str] = {"grupo": "A", "turno": "manana"}

# VS Code verificará que los tipos coincidan
resultado = procesar_datos(
    nombre="Ana", edad=20, notas=estudiante_notas, metadata=info_adicional
)

# VS Code reconocerá que resultado puede ser float o None
if resultado is not None:
    print(f"Promedio: {resultado:.2f}")

"""Utilidades para la matriz de roles."""

import os
import json
from typing import Dict, List, Optional, Union
from pathlib import Path

def cargar_matriz_desde_json(ruta: Union[str, Path]) -> Dict[str, List[str]]:
    """Carga una matriz de roles desde un archivo JSON.

    Args:
        ruta: Ruta al archivo JSON que contiene la matriz

    Returns:
        Dict[str, List[str]]: Diccionario con la matriz de roles

    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el archivo no es JSON válido
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def guardar_matriz_en_json(
    matriz: Dict[str, List[str]],
    ruta: Union[str, Path]
) -> None:
    """Guarda una matriz de roles en un archivo JSON.

    Args:
        matriz: Diccionario con la matriz de roles
        ruta: Ruta donde guardar el archivo JSON

    Raises:
        IOError: Si hay un error al escribir el archivo
    """
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(matriz, f, indent=4)


def validar_matriz(matriz: Dict[str, List[str]]) -> bool:
    """Valida la estructura de una matriz de roles.

    Verifica que:
    - Todas las claves sean strings
    - Todos los valores sean listas de strings
    - No haya permisos duplicados
    - No haya roles vacíos

    Args:
        matriz: Diccionario con la matriz de roles a validar

    Returns:
        bool: True si la matriz es válida, False en caso contrario
    """
    if not matriz:
        return False
        
    for rol, permisos in matriz.items():
        # Validar tipos
        if not isinstance(rol, str) or not isinstance(permisos, list):
            return False
        
        # Validar permisos
        if not permisos:  # No permitir roles sin permisos
            return False
            
        # Validar que todos los permisos sean strings
        if not all(isinstance(p, str) for p in permisos):
            return False
            
        # Validar duplicados
        if len(permisos) != len(set(permisos)):
            return False
            
    return True

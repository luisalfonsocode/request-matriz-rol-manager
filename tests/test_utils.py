"""Tests para las utilidades de E/S."""

import json
import pytest
from pathlib import Path
from matriz_rol.utils.io import (
    cargar_matriz_desde_json,
    guardar_matriz_en_json,
    validar_matriz
)


def test_validar_matriz():
    """Prueba la validación de matrices."""
    # Matriz válida
    matriz_valida = {
        "admin": ["leer", "escribir"],
        "editor": ["leer"]
    }
    assert validar_matriz(matriz_valida) is True
    
    # Matriz vacía
    assert validar_matriz({}) is False
    
    # Rol sin permisos
    matriz_invalida = {
        "admin": []
    }
    assert validar_matriz(matriz_invalida) is False
    
    # Permisos duplicados
    matriz_duplicados = {
        "admin": ["leer", "leer"]
    }
    assert validar_matriz(matriz_duplicados) is False


def test_guardar_cargar_matriz(tmp_path):
    """Prueba guardar y cargar matrices desde JSON."""
    matriz_original = {
        "admin": ["leer", "escribir", "eliminar"],
        "editor": ["leer", "escribir"],
        "viewer": ["leer"]
    }
    
    # Crear ruta temporal para el archivo
    ruta_json = tmp_path / "matriz.json"
    
    # Guardar matriz
    guardar_matriz_en_json(matriz_original, ruta_json)
    assert ruta_json.exists()
    
    # Cargar matriz y comparar
    matriz_cargada = cargar_matriz_desde_json(ruta_json)
    assert matriz_cargada == matriz_original


def test_cargar_matriz_errores():
    """Prueba el manejo de errores al cargar matrices."""
    # Archivo no existente
    with pytest.raises(FileNotFoundError):
        cargar_matriz_desde_json("no_existe.json")
    
    # JSON inválido
    ruta_invalida = Path("test_invalido.json")
    ruta_invalida.write_text("{rol: [}")
    
    with pytest.raises(json.JSONDecodeError):
        cargar_matriz_desde_json(ruta_invalida)
    
    # Limpiar archivo de prueba
    ruta_invalida.unlink()


def test_guardar_matriz_errores(tmp_path):
    """Prueba el manejo de errores al guardar matrices."""
    matriz = {"admin": ["leer"]}
    ruta_protegida = tmp_path / "protegido" / "matriz.json"
    
    # Intentar guardar en directorio sin permisos
    with pytest.raises(IOError):
        # Crear directorio con permisos de solo lectura
        ruta_protegida.parent.mkdir()
        ruta_protegida.parent.chmod(0o444)  # Solo lectura
        guardar_matriz_en_json(matriz, ruta_protegida)
    
    # Limpiar permisos para permitir eliminación
    ruta_protegida.parent.chmod(0o777)

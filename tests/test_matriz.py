"""Tests de la clase MatrizRoles."""

from datetime import datetime

import pytest

from matriz_rol.matriz import MatrizRoles


def test_crear_matriz():
    """Prueba la creación de una matriz de roles."""
    matriz = MatrizRoles()
    assert isinstance(matriz.roles, dict)
    assert isinstance(matriz.jerarquia, dict)
    assert isinstance(matriz.ultima_modificacion, datetime)


def test_agregar_rol():
    """Prueba la adición de roles a la matriz."""
    matriz = MatrizRoles()

    # Rol básico
    assert matriz.agregar_rol("admin", ["leer", "escribir"]) is True
    assert "admin" in matriz.roles
    assert matriz.roles["admin"] == ["leer", "escribir"]

    # Rol con herencia
    matriz.agregar_rol("editor", ["leer", "escribir"])
    assert matriz.agregar_rol("viewer", ["leer"], "editor") is True
    assert "viewer" in matriz.roles
    assert "viewer" in matriz.jerarquia


def test_validaciones_rol():
    """Prueba las validaciones al agregar roles."""
    matriz = MatrizRoles()

    # Validar nombre vacío
    with pytest.raises(ValueError):
        matriz.agregar_rol("", ["leer"])

    # Validar permisos vacíos
    with pytest.raises(ValueError):
        matriz.agregar_rol("admin", [])

    # Validar rol padre no existente
    with pytest.raises(KeyError):
        matriz.agregar_rol("viewer", ["leer"], "no_existe")


def test_verificar_permiso():
    """Prueba la verificación de permisos."""
    matriz = MatrizRoles()

    # Configurar roles
    matriz.agregar_rol("admin", ["leer", "escribir", "eliminar"])
    matriz.agregar_rol("editor", ["leer", "escribir"])
    matriz.agregar_rol("viewer", ["leer"], "editor")

    # Verificar permisos directos
    assert matriz.verificar_permiso("admin", "eliminar") is True
    assert matriz.verificar_permiso("editor", "escribir") is True
    assert matriz.verificar_permiso("editor", "eliminar") is False

    # Verificar permisos heredados
    assert matriz.verificar_permiso("viewer", "leer") is True

    # Verificar rol no existente
    assert matriz.verificar_permiso("no_existe", "leer") is False


def test_herencia_roles():
    """Prueba la herencia de roles y permisos."""
    matriz = MatrizRoles()

    # Configurar jerarquía de roles
    matriz.agregar_rol("super_admin", ["leer", "escribir", "eliminar", "admin"])
    matriz.agregar_rol("admin", ["leer", "escribir", "eliminar"], "super_admin")
    matriz.agregar_rol("editor", ["leer", "escribir"], "admin")
    matriz.agregar_rol("viewer", ["leer"], "editor")

    # Verificar permisos en cada nivel
    assert matriz.verificar_permiso("super_admin", "admin") is True
    assert matriz.verificar_permiso("admin", "eliminar") is True
    assert matriz.verificar_permiso("editor", "escribir") is True
    assert matriz.verificar_permiso("viewer", "leer") is True

    # Verificar límites de permisos
    assert matriz.verificar_permiso("editor", "eliminar") is False
    assert matriz.verificar_permiso("viewer", "escribir") is False

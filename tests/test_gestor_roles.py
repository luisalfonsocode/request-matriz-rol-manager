"""Tests del gestor de roles."""

import pytest

from matriz_rol.gestor_roles import GestorRoles


def test_agregar_rol():
    """Prueba la creación de roles."""
    gestor = GestorRoles()
    assert gestor.agregar_rol("admin", ["leer", "escribir"]) is True
    assert gestor.agregar_rol("admin", ["leer"]) is False  # Rol duplicado


def test_asignar_rol_usuario():
    """Prueba la asignación de roles a usuarios."""
    gestor = GestorRoles()
    gestor.agregar_rol("editor", ["leer", "escribir"])

    # Asignación exitosa
    resultado = gestor.asignar_rol_usuario("user1", "editor")
    assert resultado == "Rol editor asignado a usuario user1"

    # Rol no existente
    assert gestor.asignar_rol_usuario("user2", "admin") is None


def test_verificar_permiso():
    """Prueba la verificación de permisos."""
    gestor = GestorRoles()
    gestor.agregar_rol("admin", ["leer", "escribir", "eliminar"])
    gestor.asignar_rol_usuario("user1", "admin")

    # Usuario con permiso
    assert gestor.verificar_permiso("user1", "escribir") is True

    # Usuario sin permiso
    assert gestor.verificar_permiso("user1", "ejecutar") is False

    # Usuario no existente
    assert gestor.verificar_permiso("user2", "leer") is False


def test_roles_multiples():
    """Prueba la gestión de múltiples roles y usuarios."""
    gestor = GestorRoles()

    # Crear roles
    gestor.agregar_rol("admin", ["leer", "escribir", "eliminar"])
    gestor.agregar_rol("editor", ["leer", "escribir"])
    gestor.agregar_rol("viewer", ["leer"])

    # Asignar roles
    gestor.asignar_rol_usuario("user1", "admin")
    gestor.asignar_rol_usuario("user2", "editor")
    gestor.asignar_rol_usuario("user3", "viewer")

    # Verificar permisos por rol
    assert gestor.verificar_permiso("user1", "eliminar") is True
    assert gestor.verificar_permiso("user2", "escribir") is True
    assert gestor.verificar_permiso("user2", "eliminar") is False
    assert gestor.verificar_permiso("user3", "leer") is True
    assert gestor.verificar_permiso("user3", "escribir") is False

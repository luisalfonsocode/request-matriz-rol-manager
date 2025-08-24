"""Módulo para gestionar roles y permisos."""

from typing import Dict, List, Optional, Union


class GestorRoles:
    """Clase para gestionar roles y sus permisos asociados."""

    def __init__(self) -> None:
        """Inicializa el gestor de roles."""
        self.roles: Dict[str, List[str]] = {}
        self.usuarios: Dict[str, str] = {}

    def agregar_rol(self, nombre: str, permisos: List[str]) -> bool:
        """Agrega un nuevo rol con sus permisos.

        Args:
            nombre: El nombre del rol a crear
            permisos: Lista de permisos asociados al rol

        Returns:
            bool: True si el rol se creó correctamente, False si ya existía
        """
        if nombre in self.roles:
            return False

        self.roles[nombre] = permisos
        return True

    def asignar_rol_usuario(self, usuario_id: str, rol: str) -> Optional[str]:
        """Asigna un rol a un usuario.

        Args:
            usuario_id: Identificador único del usuario
            rol: Nombre del rol a asignar

        Returns:
            Optional[str]: Mensaje de éxito o None si hubo error
        """
        if rol not in self.roles:
            return None

        self.usuarios[usuario_id] = rol
        return f"Rol {rol} asignado a usuario {usuario_id}"

    def verificar_permiso(self, usuario_id: str, permiso: str) -> bool:
        """Verifica si un usuario tiene un permiso específico.

        Args:
            usuario_id: Identificador del usuario
            permiso: Permiso a verificar

        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario
        """
        if usuario_id not in self.usuarios:
            return False

        rol_usuario = self.usuarios[usuario_id]
        return permiso in self.roles[rol_usuario]

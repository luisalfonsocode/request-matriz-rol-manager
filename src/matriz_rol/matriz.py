"""
Este módulo proporciona funcionalidades para procesar y validar matrices de roles.

El módulo incluye clases y funciones para:
    - Validar estructuras de matrices de roles
    - Procesar y transformar datos de roles
    - Verificar consistencia de permisos
"""

from typing import Dict, List, Optional, Union
from datetime import datetime


class MatrizRoles:
    """Clase para gestionar y procesar matrices de roles.
    
    Esta clase proporciona funcionalidades para crear, validar y
    manipular matrices de roles, asegurando la consistencia de
    los datos y las relaciones entre roles y permisos.

    Attributes:
        roles: Diccionario que mapea nombres de roles a sus permisos
        jerarquia: Diccionario que define las relaciones entre roles
        ultima_modificacion: Fecha y hora de la última modificación

    Examples:
        >>> matriz = MatrizRoles()
        >>> matriz.agregar_rol("admin", ["leer", "escribir"])
        True
        >>> matriz.verificar_permiso("admin", "leer")
        True
    """

    def __init__(self) -> None:
        """Inicializa una nueva instancia de MatrizRoles."""
        self.roles: Dict[str, List[str]] = {}
        self.jerarquia: Dict[str, List[str]] = {}
        self.ultima_modificacion: datetime = datetime.now()

    def agregar_rol(
        self,
        nombre: str,
        permisos: List[str],
        rol_padre: Optional[str] = None
    ) -> bool:
        """Agrega un nuevo rol a la matriz.

        Args:
            nombre: Nombre único del rol
            permisos: Lista de permisos asociados al rol
            rol_padre: Rol del cual hereda permisos (opcional)

        Returns:
            bool: True si el rol se agregó correctamente,
                  False si el rol ya existe

        Raises:
            ValueError: Si el nombre está vacío o los permisos están vacíos
            KeyError: Si el rol_padre especificado no existe

        Examples:
            >>> matriz = MatrizRoles()
            >>> matriz.agregar_rol("editor", ["leer", "escribir"])
            True
            >>> matriz.agregar_rol("viewer", ["leer"], "editor")
            True
        """
        if not nombre or not permisos:
            raise ValueError("El nombre y los permisos no pueden estar vacíos")

        if rol_padre and rol_padre not in self.roles:
            raise KeyError(f"El rol padre '{rol_padre}' no existe")

        if nombre in self.roles:
            return False

        self.roles[nombre] = permisos
        if rol_padre:
            self.jerarquia[nombre] = self.roles[rol_padre]
        
        self.ultima_modificacion = datetime.now()
        return True

    def verificar_permiso(self, rol: str, permiso: str) -> bool:
        """Verifica si un rol tiene un permiso específico.

        Comprueba si el rol tiene el permiso directamente o
        lo hereda de su rol padre en la jerarquía.

        Args:
            rol: Nombre del rol a verificar
            permiso: Permiso que se quiere verificar

        Returns:
            bool: True si el rol tiene el permiso, False en caso contrario

        Examples:
            >>> matriz = MatrizRoles()
            >>> matriz.agregar_rol("admin", ["leer", "escribir"])
            >>> matriz.verificar_permiso("admin", "leer")
            True
        """
        if rol not in self.roles:
            return False

        # Verifica permisos directos
        if permiso in self.roles[rol]:
            return True

        # Verifica permisos heredados
        if rol in self.jerarquia:
            return permiso in self.jerarquia[rol]

        return False

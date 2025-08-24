"""
Módulo para manejar la persistencia de datos de autorizadores.

Este módulo proporciona funcionalidades para:
- Guardar y cargar datos de autorizadores desde archivo JSON
- Mantener configuraciones entre sesiones
- Actualizar automáticamente los datos guardados
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class GestorPersistencia:
    """Gestor para la persistencia de datos de autorizadores."""

    def __init__(self, archivo_datos: str = "autorizadores_datos.json"):
        """
        Inicializa el gestor de persistencia.

        Args:
            archivo_datos: Nombre del archivo donde guardar los datos
        """
        self.directorio_datos = Path(__file__).parent
        self.archivo_datos = self.directorio_datos / archivo_datos
        self._asegurar_directorio()

    def _asegurar_directorio(self) -> None:
        """Asegura que el directorio de datos exista."""
        self.directorio_datos.mkdir(parents=True, exist_ok=True)

    def cargar_autorizadores(self) -> Dict[str, Dict[str, str]]:
        """
        Carga los datos de autorizadores desde el archivo.

        Returns:
            Diccionario con códigos de aplicación como claves y datos de autorizadores como valores
        """
        try:
            if self.archivo_datos.exists():
                with open(self.archivo_datos, "r", encoding="utf-8") as file:
                    return json.load(file)
            else:
                return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar autorizadores: {e}")
            return {}

    def guardar_autorizadores(self, datos_autorizadores: List[Dict[str, str]]) -> bool:
        """
        Guarda los datos de autorizadores en el archivo.

        Args:
            datos_autorizadores: Lista de diccionarios con datos de autorizadores

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            # Convertir lista a diccionario usando código como clave
            datos_dict = {}
            for dato in datos_autorizadores:
                codigo = dato.get("codigo", "")
                if codigo:
                    datos_dict[codigo] = {
                        "autorizador": dato.get("autorizador", ""),
                        "correo": dato.get("correo", ""),
                    }

            with open(self.archivo_datos, "w", encoding="utf-8") as file:
                json.dump(datos_dict, file, indent=2, ensure_ascii=False)

            print(f"Datos guardados en: {self.archivo_datos}")
            return True

        except IOError as e:
            print(f"Error al guardar autorizadores: {e}")
            return False

    def obtener_autorizador_por_codigo(self, codigo: str) -> Optional[Dict[str, str]]:
        """
        Obtiene los datos de un autorizador por código.

        Args:
            codigo: Código de la aplicación

        Returns:
            Datos del autorizador o None si no existe
        """
        datos = self.cargar_autorizadores()
        return datos.get(codigo)

    def actualizar_autorizador(
        self, codigo: str, autorizador: str, correo: str
    ) -> bool:
        """
        Actualiza los datos de un autorizador específico.

        Args:
            codigo: Código de la aplicación
            autorizador: Nombre del autorizador
            correo: Correo del autorizador

        Returns:
            True si se actualizó correctamente
        """
        datos = self.cargar_autorizadores()
        datos[codigo] = {"autorizador": autorizador, "correo": correo}

        # Convertir de vuelta a lista para guardar
        datos_lista = []
        for cod, info in datos.items():
            datos_lista.append(
                {
                    "codigo": cod,
                    "autorizador": info["autorizador"],
                    "correo": info["correo"],
                }
            )

        return self.guardar_autorizadores(datos_lista)

    def limpiar_datos(self) -> bool:
        """
        Limpia todos los datos guardados.

        Returns:
            True si se limpió correctamente
        """
        try:
            if self.archivo_datos.exists():
                self.archivo_datos.unlink()
            return True
        except IOError as e:
            print(f"Error al limpiar datos: {e}")
            return False

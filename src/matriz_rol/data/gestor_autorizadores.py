"""
Gestor de base de datos de autorizadores.

Maneja el almacenamiento y consulta de información de autorizadores
para todas las aplicaciones del sistema.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class GestorAutorizadores:
    """Gestor para la base de datos de autorizadores."""

    def __init__(self):
        """Inicializa el gestor de autorizadores."""
        self.ruta_bd = self._obtener_ruta_bd()
        self.autorizadores_bd: Dict[str, Dict] = {}
        self.cargar_autorizadores()

    def _obtener_ruta_bd(self) -> Path:
        """Obtiene la ruta del archivo de base de datos de autorizadores."""
        # Buscar primero en la raíz del proyecto
        ruta_proyecto = Path(__file__).parents[3] / "data" / "autorizadores_bd.json"
        if ruta_proyecto.parent.exists():
            return ruta_proyecto

        # Fallback a ubicación por defecto
        ruta_proyecto.parent.mkdir(parents=True, exist_ok=True)
        return ruta_proyecto

    def cargar_autorizadores(self) -> bool:
        """Carga la base de datos de autorizadores desde archivo."""
        try:
            if self.ruta_bd.exists():
                with open(self.ruta_bd, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.autorizadores_bd = data.get("autorizadores", {})
                print(
                    f"📂 BD Autorizadores cargada: {len(self.autorizadores_bd)} aplicaciones"
                )
                return True
            else:
                print("📂 BD Autorizadores no existe, creando nueva...")
                self._crear_bd_inicial()
                return True
        except Exception as e:
            print(f"❌ Error cargando BD autorizadores: {e}")
            self.autorizadores_bd = {}
            return False

    def _crear_bd_inicial(self):
        """Crea la base de datos inicial con datos de ejemplo."""
        self.autorizadores_bd = {
            "APF2": {
                "codigo": "APF2",
                "nombre_aplicacion": "Sistema APF2",
                "autorizador": "Daniela Fernanda Ortiz",
                "correo": "daniela.ortiz@empresa.com",
                "telefono": "+57 300 123 4567",
                "area": "Tecnología",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "QASD": {
                "codigo": "QASD",
                "nombre_aplicacion": "Sistema QASD",
                "autorizador": "Sebastián Eduardo Martín",
                "correo": "sebastian.martin@corporacion.co",
                "telefono": "+57 301 234 5678",
                "area": "Calidad",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "SSSS": {
                "codigo": "SSSS",
                "nombre_aplicacion": "Sistema SSSS",
                "autorizador": "Ricardo Antonio Jiménez",
                "correo": "ricardo.jimenez@global.org",
                "telefono": "+57 302 345 6789",
                "area": "Seguridad",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "CASD": {
                "codigo": "CASD",
                "nombre_aplicacion": "Sistema CASD",
                "autorizador": "Isabella Camila Rojas",
                "correo": "isabella.rojas@tech.net",
                "telefono": "+57 303 456 7890",
                "area": "Desarrollo",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "FCVE": {
                "codigo": "FCVE",
                "nombre_aplicacion": "Sistema FCVE",
                "autorizador": "Paola Carolina Díaz",
                "correo": "paola.diaz@solutions.com",
                "telefono": "+57 304 567 8901",
                "area": "Finanzas",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "ATLA": {
                "codigo": "ATLA",
                "nombre_aplicacion": "Sistema ATLA",
                "autorizador": "Laura Cristina Torres",
                "correo": "laura.torres@innovate.co",
                "telefono": "+57 305 678 9012",
                "area": "Operaciones",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
            "FIEC": {
                "codigo": "FIEC",
                "nombre_aplicacion": "Sistema FIEC",
                "autorizador": "Fernando Gabriel Ruiz",
                "correo": "fernando.ruiz@business.org",
                "telefono": "+57 306 789 0123",
                "area": "Estrategia",
                "activo": True,
                "fecha_actualizacion": datetime.now().isoformat(),
            },
        }
        self.guardar_autorizadores()

    def guardar_autorizadores(self) -> bool:
        """Guarda la base de datos de autorizadores en archivo."""
        try:
            data = {
                "metadata": {
                    "version": "1.0",
                    "ultima_actualizacion": datetime.now().isoformat(),
                    "total_aplicaciones": len(self.autorizadores_bd),
                },
                "autorizadores": self.autorizadores_bd,
            }

            with open(self.ruta_bd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"💾 BD Autorizadores guardada: {self.ruta_bd}")
            return True
        except Exception as e:
            print(f"❌ Error guardando BD autorizadores: {e}")
            return False

    def obtener_autorizador_por_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtiene un autorizador específico por código de aplicación."""
        return self.autorizadores_bd.get(codigo.upper())

    def obtener_autorizadores_por_codigos(self, codigos: List[str]) -> List[Dict]:
        """Obtiene múltiples autorizadores por lista de códigos."""
        autorizadores = []
        for codigo in codigos:
            auth = self.obtener_autorizador_por_codigo(codigo)
            if auth:
                autorizadores.append(auth)
            else:
                print(f"⚠️ Autorizador no encontrado para código: {codigo}")
        return autorizadores

    def obtener_todos_los_autorizadores(self) -> List[Dict]:
        """Obtiene todos los autorizadores de la base de datos."""
        return list(self.autorizadores_bd.values())

    def obtener_codigos_aplicacion(self) -> List[str]:
        """Obtiene todos los códigos de aplicación disponibles."""
        return sorted(list(self.autorizadores_bd.keys()))

    def agregar_autorizador(self, codigo: str, datos_autorizador: Dict) -> bool:
        """Agrega un nuevo autorizador a la base de datos."""
        try:
            codigo = codigo.upper()
            datos_autorizador["codigo"] = codigo
            datos_autorizador["fecha_actualizacion"] = datetime.now().isoformat()

            self.autorizadores_bd[codigo] = datos_autorizador
            self.guardar_autorizadores()
            print(f"✅ Autorizador agregado: {codigo}")
            return True
        except Exception as e:
            print(f"❌ Error agregando autorizador: {e}")
            return False

    def actualizar_autorizador(self, codigo: str, datos_autorizador: Dict) -> bool:
        """Actualiza un autorizador existente."""
        try:
            codigo = codigo.upper()
            if codigo in self.autorizadores_bd:
                datos_autorizador["codigo"] = codigo
                datos_autorizador["fecha_actualizacion"] = datetime.now().isoformat()

                self.autorizadores_bd[codigo] = datos_autorizador
                self.guardar_autorizadores()
                print(f"✅ Autorizador actualizado: {codigo}")
                return True
            else:
                print(f"❌ Autorizador no encontrado: {codigo}")
                return False
        except Exception as e:
            print(f"❌ Error actualizando autorizador: {e}")
            return False

    def eliminar_autorizador(self, codigo: str) -> bool:
        """Elimina un autorizador de la base de datos."""
        try:
            codigo = codigo.upper()
            if codigo in self.autorizadores_bd:
                del self.autorizadores_bd[codigo]
                self.guardar_autorizadores()
                print(f"✅ Autorizador eliminado: {codigo}")
                return True
            else:
                print(f"❌ Autorizador no encontrado: {codigo}")
                return False
        except Exception as e:
            print(f"❌ Error eliminando autorizador: {e}")
            return False

    def obtener_info_bd(self) -> Dict:
        """Obtiene información general de la base de datos."""
        return {
            "ruta": str(self.ruta_bd),
            "total_aplicaciones": len(self.autorizadores_bd),
            "aplicaciones": list(self.autorizadores_bd.keys()),
            "activos": len(
                [a for a in self.autorizadores_bd.values() if a.get("activo", True)]
            ),
        }

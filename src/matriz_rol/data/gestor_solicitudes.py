"""
Modelo de datos para gestionar solicitudes de conformidad.

Maneja el ciclo completo: creación, seguimiento, y cierre de solicitudes.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from enum import Enum


class EstadoSolicitud(Enum):
    """Estados posibles de una solicitud según el proceso real."""

    EN_SOLICITUD_CONFORMIDADES = "En solicitud de conformidades"
    EN_HELPDESK = "En Helpdesk"
    ATENDIDO = "Atendido"
    CERRADO = "Cerrado"


class SolicitudConformidad:
    """Representa una solicitud de conformidad."""

    def __init__(
        self,
        id_solicitud: str,
        fecha_creacion: str,
        grupos_red: List[str],
        autorizadores: List[Dict[str, str]],
        estado: EstadoSolicitud = EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
        ticket_helpdesk: Optional[str] = None,
        fecha_cierre: Optional[str] = None,
        observaciones: Optional[str] = None,
    ):
        """
        Inicializa una solicitud de conformidad.

        Args:
            id_solicitud: Identificador único de la solicitud
            fecha_creacion: Fecha de creación en formato ISO
            grupos_red: Lista de grupos de red solicitados
            autorizadores: Lista de autorizadores con sus datos
            estado: Estado actual de la solicitud
            ticket_helpdesk: Número de ticket del helpdesk
            fecha_cierre: Fecha de cierre (si está cerrada)
            observaciones: Observaciones adicionales
        """
        self.id_solicitud = id_solicitud
        self.fecha_creacion = fecha_creacion
        self.grupos_red = grupos_red
        self.autorizadores = autorizadores
        self.estado = estado
        self.ticket_helpdesk = ticket_helpdesk
        self.fecha_cierre = fecha_cierre
        self.observaciones = observaciones

    def to_dict(self) -> Dict:
        """Convierte la solicitud a diccionario para persistencia."""
        return {
            "id_solicitud": self.id_solicitud,
            "fecha_creacion": self.fecha_creacion,
            "grupos_red": self.grupos_red,
            "autorizadores": self.autorizadores,
            "estado": self.estado.value,
            "ticket_helpdesk": self.ticket_helpdesk,
            "fecha_cierre": self.fecha_cierre,
            "observaciones": self.observaciones,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "SolicitudConformidad":
        """Crea una solicitud desde un diccionario."""
        return cls(
            id_solicitud=data["id_solicitud"],
            fecha_creacion=data["fecha_creacion"],
            grupos_red=data["grupos_red"],
            autorizadores=data["autorizadores"],
            estado=EstadoSolicitud(data["estado"]),
            ticket_helpdesk=data.get("ticket_helpdesk"),
            fecha_cierre=data.get("fecha_cierre"),
            observaciones=data.get("observaciones"),
        )

    def cerrar_solicitud(self, ticket_helpdesk: str, observaciones: str = ""):
        """Cierra la solicitud con el ticket del helpdesk."""
        self.estado = EstadoSolicitud.CERRADO
        self.ticket_helpdesk = ticket_helpdesk
        self.fecha_cierre = datetime.now().isoformat()
        self.observaciones = observaciones

    def reabrir_solicitud(self, motivo: str = ""):
        """Reabre una solicitud cerrada."""
        self.estado = EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES
        self.fecha_cierre = None
        self.observaciones = f"Reabierta: {motivo}"

    def marcar_en_helpdesk(self, ticket_helpdesk: str, observaciones: str = ""):
        """Marca la solicitud como enviada al helpdesk."""
        self.estado = EstadoSolicitud.EN_HELPDESK
        self.ticket_helpdesk = ticket_helpdesk
        self.observaciones = observaciones

    def marcar_atendido(self, observaciones: str = ""):
        """Marca la solicitud como atendida."""
        self.estado = EstadoSolicitud.ATENDIDO
        self.observaciones = observaciones


class GestorSolicitudes:
    """Gestor para manejar todas las solicitudes de conformidad."""

    def __init__(self):
        """Inicializa el gestor de solicitudes con BD local robusta."""
        # Estrategia de ubicación múltiple para BD local
        self.directorio_bd = self._obtener_directorio_bd()
        self.directorio_bd.mkdir(parents=True, exist_ok=True)

        self.archivo_solicitudes = self.directorio_bd / "solicitudes_conformidad.json"
        self.archivo_backup = (
            self.directorio_bd
            / f"backup_solicitudes_{datetime.now().strftime('%Y%m%d')}.json"
        )

        self.solicitudes: List[SolicitudConformidad] = []

        print(f"�️  BD LOCAL INICIALIZADA")
        print(f"📂 Ubicación: {self.archivo_solicitudes}")
        print(f"💾 Backup diario: {self.archivo_backup}")

        self.cargar_solicitudes()
        self._crear_backup_si_necesario()

    def _obtener_directorio_bd(self) -> Path:
        """Obtiene el directorio óptimo para la BD local."""
        # Opción 1: Raíz del proyecto (más accesible para desarrollo)
        try:
            proyecto_root = Path(__file__).parent.parent.parent.parent
            bd_proyecto = proyecto_root / "data"
            bd_proyecto.mkdir(parents=True, exist_ok=True)

            # Verificar que podemos escribir en el directorio
            test_file = bd_proyecto / ".test_write"
            test_file.write_text("test")
            test_file.unlink()

            return bd_proyecto
        except Exception as e:
            print(f"⚠️ No se puede usar directorio del proyecto: {e}")

        # Opción 2: Documentos del usuario (fallback)
        try:
            bd_documentos = Path.home() / "Documents" / "MatrizRol_BD"
            bd_documentos.mkdir(parents=True, exist_ok=True)
            return bd_documentos
        except Exception as e:
            print(f"⚠️ No se puede usar directorio de documentos: {e}")

        # Opción 3: Carpeta temporal (último recurso)
        import tempfile

        bd_temp = Path(tempfile.gettempdir()) / "MatrizRol_BD"
        bd_temp.mkdir(parents=True, exist_ok=True)
        return bd_temp

    def generar_id_solicitud(self) -> str:
        """Genera un ID único para una nueva solicitud."""
        fecha_actual = datetime.now()
        timestamp = fecha_actual.strftime("%Y%m%d_%H%M%S")
        numero_solicitud = len(self.solicitudes) + 1
        return f"SOL_{timestamp}_{numero_solicitud:03d}"

    def crear_solicitud(
        self, grupos_red: List[str], autorizadores: List[Dict[str, str]]
    ) -> SolicitudConformidad:
        """
        Crea una nueva solicitud de conformidad.

        Args:
            grupos_red: Lista de grupos de red solicitados
            autorizadores: Lista de autorizadores

        Returns:
            La solicitud creada
        """
        print(f"🔧 Creando nueva solicitud...")
        print(f"   Grupos de red: {grupos_red}")
        print(f"   Autorizadores: {len(autorizadores)}")

        id_solicitud = self.generar_id_solicitud()
        fecha_creacion = datetime.now().isoformat()

        solicitud = SolicitudConformidad(
            id_solicitud=id_solicitud,
            fecha_creacion=fecha_creacion,
            grupos_red=grupos_red,
            autorizadores=autorizadores,
        )

        print(f"   ID generado: {id_solicitud}")
        print(f"   Solicitudes antes de agregar: {len(self.solicitudes)}")

        self.solicitudes.append(solicitud)

        print(f"   Solicitudes después de agregar: {len(self.solicitudes)}")

        self.guardar_solicitudes()

        print(f"✅ Solicitud creada y guardada: {id_solicitud}")

        return solicitud

    def _crear_backup_si_necesario(self):
        """Crea un backup diario si no existe."""
        if self.archivo_solicitudes.exists() and not self.archivo_backup.exists():
            try:
                import shutil

                shutil.copy2(self.archivo_solicitudes, self.archivo_backup)
                print(f"💾 Backup diario creado: {self.archivo_backup.name}")
            except Exception as e:
                print(f"⚠️ No se pudo crear backup: {e}")

    def obtener_info_bd(self) -> dict:
        """Obtiene información detallada de la BD local."""
        info = {
            "ubicacion": str(self.archivo_solicitudes),
            "existe": self.archivo_solicitudes.exists(),
            "tamaño_kb": 0,
            "total_solicitudes": len(self.solicitudes),
            "ultima_modificacion": None,
            "backup_diario": self.archivo_backup.exists(),
        }

        if self.archivo_solicitudes.exists():
            try:
                stat = self.archivo_solicitudes.stat()
                info["tamaño_kb"] = round(stat.st_size / 1024, 2)
                info["ultima_modificacion"] = datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            except:
                pass

        return info

    def obtener_solicitudes(self) -> List[SolicitudConformidad]:
        """Obtiene todas las solicitudes."""
        return self.solicitudes

    def obtener_solicitud_por_id(
        self, id_solicitud: str
    ) -> Optional[SolicitudConformidad]:
        """Obtiene una solicitud específica por su ID."""
        for solicitud in self.solicitudes:
            if solicitud.id_solicitud == id_solicitud:
                return solicitud
        return None

    def actualizar_estado_solicitud(
        self,
        id_solicitud: str,
        nuevo_estado: EstadoSolicitud,
        ticket_helpdesk: Optional[str] = None,
        observaciones: str = "",
    ) -> bool:
        """
        Actualiza el estado de una solicitud.

        Args:
            id_solicitud: ID de la solicitud
            nuevo_estado: Nuevo estado
            ticket_helpdesk: Número de ticket (opcional)
            observaciones: Observaciones adicionales

        Returns:
            True si se actualizó correctamente
        """
        solicitud = self.obtener_solicitud_por_id(id_solicitud)
        if not solicitud:
            return False

        if nuevo_estado == EstadoSolicitud.CERRADO:
            if ticket_helpdesk:
                solicitud.cerrar_solicitud(ticket_helpdesk, observaciones)
        else:
            solicitud.estado = nuevo_estado
            if observaciones:
                solicitud.observaciones = observaciones

        self.guardar_solicitudes()
        return True

    def filtrar_solicitudes_por_estado(
        self, estado: EstadoSolicitud
    ) -> List[SolicitudConformidad]:
        """Filtra solicitudes por estado."""
        return [s for s in self.solicitudes if s.estado == estado]

    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas de las solicitudes."""
        total = len(self.solicitudes)
        en_solicitud = len(
            self.filtrar_solicitudes_por_estado(
                EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES
            )
        )
        en_helpdesk = len(
            self.filtrar_solicitudes_por_estado(EstadoSolicitud.EN_HELPDESK)
        )
        atendido = len(self.filtrar_solicitudes_por_estado(EstadoSolicitud.ATENDIDO))
        cerrado = len(self.filtrar_solicitudes_por_estado(EstadoSolicitud.CERRADO))

        return {
            "total": total,
            "en_solicitud": en_solicitud,
            "en_helpdesk": en_helpdesk,
            "atendido": atendido,
            "cerrado": cerrado,
        }

    def verificar_bd_local(self) -> Dict[str, any]:
        """Verifica el estado de la BD local."""
        info = {
            "archivo_existe": self.archivo_solicitudes.exists(),
            "ruta_archivo": str(self.archivo_solicitudes),
            "total_solicitudes": len(self.solicitudes),
            "es_legible": False,
            "tamaño_archivo": 0,
        }

        if info["archivo_existe"]:
            try:
                info["tamaño_archivo"] = self.archivo_solicitudes.stat().st_size
                with open(self.archivo_solicitudes, "r", encoding="utf-8") as f:
                    json.load(f)
                info["es_legible"] = True
            except:
                info["es_legible"] = False

        return info

    def cargar_solicitudes(self):
        """Carga las solicitudes desde el archivo JSON."""
        print(f"📂 Cargando solicitudes desde: {self.archivo_solicitudes}")

        if self.archivo_solicitudes.exists():
            try:
                with open(self.archivo_solicitudes, "r", encoding="utf-8") as file:
                    datos = json.load(file)
                    self.solicitudes = [
                        SolicitudConformidad.from_dict(solicitud_data)
                        for solicitud_data in datos.get("solicitudes", [])
                    ]
                print(f"✅ {len(self.solicitudes)} solicitudes cargadas exitosamente")
            except Exception as e:
                print(f"❌ Error cargando solicitudes: {e}")
                self.solicitudes = []
        else:
            print(
                f"📁 Archivo no existe, creando BD vacía en: {self.archivo_solicitudes}"
            )
            self.solicitudes = []
            # Crear archivo inicial vacío
            self.guardar_solicitudes()

    def guardar_solicitudes(self):
        """Guarda las solicitudes en el archivo JSON."""
        try:
            print(f"💾 Guardando {len(self.solicitudes)} solicitudes en BD local...")

            # Crear directorio si no existe
            self.archivo_solicitudes.parent.mkdir(parents=True, exist_ok=True)

            datos = {
                "metadata": {
                    "version": "1.0",
                    "ultima_actualizacion": datetime.now().isoformat(),
                    "total_solicitudes": len(self.solicitudes),
                },
                "solicitudes": [solicitud.to_dict() for solicitud in self.solicitudes],
            }

            with open(self.archivo_solicitudes, "w", encoding="utf-8") as file:
                json.dump(datos, file, indent=2, ensure_ascii=False)

            print(f"✅ BD local actualizada: {self.archivo_solicitudes}")

        except Exception as e:
            print(f"❌ Error guardando solicitudes: {e}")

    def exportar_solicitudes_csv(self, archivo_destino: Path) -> bool:
        """Exporta las solicitudes a un archivo CSV."""
        try:
            import csv

            with open(archivo_destino, "w", newline="", encoding="utf-8") as csvfile:
                campos = [
                    "ID Solicitud",
                    "Fecha Creación",
                    "Estado",
                    "Grupos Red",
                    "Cantidad Autorizadores",
                    "Ticket Helpdesk",
                    "Fecha Cierre",
                    "Observaciones",
                ]

                writer = csv.DictWriter(csvfile, fieldnames=campos)
                writer.writeheader()

                for solicitud in self.solicitudes:
                    writer.writerow(
                        {
                            "ID Solicitud": solicitud.id_solicitud,
                            "Fecha Creación": solicitud.fecha_creacion,
                            "Estado": solicitud.estado.value,
                            "Grupos Red": "; ".join(solicitud.grupos_red),
                            "Cantidad Autorizadores": len(solicitud.autorizadores),
                            "Ticket Helpdesk": solicitud.ticket_helpdesk or "",
                            "Fecha Cierre": solicitud.fecha_cierre or "",
                            "Observaciones": solicitud.observaciones or "",
                        }
                    )

            return True
        except Exception as e:
            print(f"Error exportando a CSV: {e}")
            return False

#!/usr/bin/env python3
"""
Sistema de Verificación Previa - Matriz de Rol
==============================================

Script de verificación del sistema antes de la instalación.
Ubicación: setup/scripts/verificar_sistema.py

Verifica:
- Versión de Python
- Espacio en disco
- Permisos de escritura
- Estructura del proyecto
- Dependencias del sistema

Autor: Sistema de Configuración Automática
Versión: 3.0
"""

import sys
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Colors:
    """Códigos de color para la terminal."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"


class VerificadorSistema:
    """Clase principal para verificación del sistema."""

    def __init__(self):
        """Inicializar el verificador."""
        self.script_dir = Path(__file__).parent
        self.setup_dir = self.script_dir.parent
        self.project_root = self.setup_dir.parent
        self.log_file = self.setup_dir / "logs" / "verificacion.log"
        self.errores = []
        self.advertencias = []

        # Crear directorio de logs
        self.log_file.parent.mkdir(exist_ok=True)

        # Inicializar log
        self._escribir_log("=" * 80)
        self._escribir_log(f"INICIO DE VERIFICACIÓN - {self._timestamp()}")
        self._escribir_log("=" * 80)

    def _timestamp(self) -> str:
        """Obtener timestamp actual."""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _escribir_log(self, mensaje: str, nivel: str = "INFO") -> None:
        """Escribir mensaje al log."""
        timestamp = self._timestamp()
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{nivel}] {mensaje}\n")

    def _imprimir_con_color(self, mensaje: str, color: str = Colors.WHITE) -> None:
        """Imprimir mensaje con color."""
        print(f"{color}{mensaje}{Colors.END}")
        self._escribir_log(
            mensaje.replace("✅", "").replace("❌", "").replace("⚠️", "").strip()
        )

    def _imprimir_exito(self, mensaje: str) -> None:
        """Imprimir mensaje de éxito."""
        self._imprimir_con_color(f"✅ {mensaje}", Colors.GREEN)

    def _imprimir_error(self, mensaje: str) -> None:
        """Imprimir mensaje de error."""
        self._imprimir_con_color(f"❌ {mensaje}", Colors.RED)
        self.errores.append(mensaje)

    def _imprimir_advertencia(self, mensaje: str) -> None:
        """Imprimir mensaje de advertencia."""
        self._imprimir_con_color(f"⚠️  {mensaje}", Colors.YELLOW)
        self.advertencias.append(mensaje)

    def _imprimir_info(self, mensaje: str) -> None:
        """Imprimir mensaje informativo."""
        self._imprimir_con_color(f"ℹ️  {mensaje}", Colors.CYAN)

    def _imprimir_header(self, titulo: str) -> None:
        """Imprimir header de sección."""
        print()
        self._imprimir_con_color("=" * 80, Colors.CYAN)
        self._imprimir_con_color(f"  {titulo}", Colors.YELLOW + Colors.BOLD)
        self._imprimir_con_color("=" * 80, Colors.CYAN)
        print()

    def verificar_python(self) -> bool:
        """Verificar versión y configuración de Python."""
        self._imprimir_header("VERIFICACIÓN DE PYTHON")

        try:
            # Verificar versión
            version = sys.version_info
            version_str = f"{version.major}.{version.minor}.{version.micro}"

            self._imprimir_info(f"Versión de Python: {version_str}")
            self._imprimir_info(f"Ejecutable: {sys.executable}")
            self._imprimir_info(f"Plataforma: {platform.platform()}")

            # Verificar compatibilidad
            if version.major < 3 or (version.major == 3 and version.minor < 9):
                self._imprimir_error(
                    f"Se requiere Python 3.9+. Versión actual: {version_str}"
                )
                return False

            self._imprimir_exito(f"Python {version_str} es compatible")

            # Verificar pip
            try:
                import pip

                pip_version = pip.__version__
                self._imprimir_exito(f"pip disponible: versión {pip_version}")
            except ImportError:
                self._imprimir_error("pip no está disponible")
                return False

            # Verificar venv
            try:
                import venv

                self._imprimir_exito("Módulo venv disponible")
            except ImportError:
                self._imprimir_error("Módulo venv no disponible")
                return False

            # Verificar tkinter
            try:
                import tkinter

                self._imprimir_exito("tkinter disponible para GUI")
            except ImportError:
                self._imprimir_error("tkinter no disponible (requerido para GUI)")
                return False

            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando Python: {e}")
            return False

    def verificar_espacio_disco(self) -> bool:
        """Verificar espacio disponible en disco."""
        self._imprimir_header("VERIFICACIÓN DE ESPACIO EN DISCO")

        try:
            # Obtener espacio disponible
            if platform.system() == "Windows":
                import ctypes

                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(str(self.project_root)),
                    ctypes.pointer(free_bytes),
                    None,
                    None,
                )
                espacio_libre = free_bytes.value
            else:
                stat = shutil.disk_usage(self.project_root)
                espacio_libre = stat.free

            # Convertir a MB
            espacio_mb = espacio_libre / (1024 * 1024)
            espacio_requerido = 500  # MB mínimos requeridos

            self._imprimir_info(f"Espacio disponible: {espacio_mb:.1f} MB")
            self._imprimir_info(f"Espacio requerido: {espacio_requerido} MB")

            if espacio_mb < espacio_requerido:
                self._imprimir_error(
                    f"Espacio insuficiente. Se requieren {espacio_requerido} MB"
                )
                return False

            self._imprimir_exito("Espacio en disco suficiente")
            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando espacio en disco: {e}")
            return False

    def verificar_permisos(self) -> bool:
        """Verificar permisos de escritura."""
        self._imprimir_header("VERIFICACIÓN DE PERMISOS")

        try:
            # Verificar permisos en directorio del proyecto
            if not os.access(self.project_root, os.W_OK):
                self._imprimir_error(
                    "Sin permisos de escritura en directorio del proyecto"
                )
                return False

            self._imprimir_exito("Permisos de escritura en directorio del proyecto")

            # Verificar capacidad de crear archivos
            archivo_prueba = self.project_root / "test_permissions.tmp"
            try:
                with open(archivo_prueba, "w") as f:
                    f.write("test")
                archivo_prueba.unlink()
                self._imprimir_exito("Capacidad de crear archivos verificada")
            except Exception:
                self._imprimir_error("No se pueden crear archivos en el directorio")
                return False

            # Verificar permisos para crear directorios
            directorio_prueba = self.project_root / "test_dir"
            try:
                directorio_prueba.mkdir(exist_ok=True)
                directorio_prueba.rmdir()
                self._imprimir_exito("Capacidad de crear directorios verificada")
            except Exception:
                self._imprimir_error("No se pueden crear directorios")
                return False

            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando permisos: {e}")
            return False

    def verificar_estructura_proyecto(self) -> bool:
        """Verificar estructura del proyecto."""
        self._imprimir_header("VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")

        # Archivos y directorios requeridos
        elementos_requeridos = [
            ("src/", "directorio"),
            ("src/matriz_rol/", "directorio"),
            ("src/matriz_rol/__init__.py", "archivo"),
            ("src/matriz_rol/gui/", "directorio"),
            ("src/matriz_rol/gui/aplicacion_principal.py", "archivo"),
            ("src/matriz_rol/gui/gestion_solicitudes.py", "archivo"),
            ("setup.py", "archivo"),
            ("requirements.txt", "archivo"),
            ("README.md", "archivo"),
        ]

        elementos_opcionales = [
            ("tests/", "directorio"),
            ("docs/", "directorio"),
            ("pyproject.toml", "archivo"),
        ]

        try:
            errores_estructura = 0

            # Verificar elementos requeridos
            for elemento, tipo in elementos_requeridos:
                ruta = self.project_root / elemento
                if tipo == "directorio":
                    if ruta.is_dir():
                        self._imprimir_exito(f"Directorio encontrado: {elemento}")
                    else:
                        self._imprimir_error(f"Directorio faltante: {elemento}")
                        errores_estructura += 1
                else:  # archivo
                    if ruta.is_file():
                        self._imprimir_exito(f"Archivo encontrado: {elemento}")
                    else:
                        self._imprimir_error(f"Archivo faltante: {elemento}")
                        errores_estructura += 1

            # Verificar elementos opcionales
            for elemento, tipo in elementos_opcionales:
                ruta = self.project_root / elemento
                if tipo == "directorio":
                    if ruta.is_dir():
                        self._imprimir_info(
                            f"Directorio opcional encontrado: {elemento}"
                        )
                    else:
                        self._imprimir_advertencia(
                            f"Directorio opcional no encontrado: {elemento}"
                        )
                else:  # archivo
                    if ruta.is_file():
                        self._imprimir_info(f"Archivo opcional encontrado: {elemento}")
                    else:
                        self._imprimir_advertencia(
                            f"Archivo opcional no encontrado: {elemento}"
                        )

            if errores_estructura > 0:
                self._imprimir_error(
                    f"Estructura del proyecto incompleta ({errores_estructura} elementos faltantes)"
                )
                return False

            self._imprimir_exito("Estructura del proyecto correcta")
            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando estructura: {e}")
            return False

    def verificar_dependencias_sistema(self) -> bool:
        """Verificar dependencias del sistema."""
        self._imprimir_header("VERIFICACIÓN DE DEPENDENCIAS DEL SISTEMA")

        try:
            # Verificar Git (opcional)
            try:
                resultado = subprocess.run(
                    ["git", "--version"], capture_output=True, text=True, timeout=10
                )
                if resultado.returncode == 0:
                    version_git = resultado.stdout.strip()
                    self._imprimir_info(f"Git disponible: {version_git}")
                else:
                    self._imprimir_advertencia("Git no disponible (opcional)")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self._imprimir_advertencia("Git no disponible (opcional)")

            # Verificar capacidad de instalación de paquetes
            try:
                # Intentar listar paquetes instalados
                resultado = subprocess.run(
                    [sys.executable, "-m", "pip", "list"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if resultado.returncode == 0:
                    self._imprimir_exito("pip funciona correctamente")
                else:
                    self._imprimir_error("pip no funciona correctamente")
                    return False
            except subprocess.TimeoutExpired:
                self._imprimir_error("pip no responde (timeout)")
                return False

            # Verificar conectividad a PyPI (opcional)
            try:
                import urllib.request

                urllib.request.urlopen("https://pypi.org", timeout=10)
                self._imprimir_info("Conectividad a PyPI disponible")
            except Exception:
                self._imprimir_advertencia(
                    "Sin conectividad a PyPI (se usará caché local)"
                )

            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando dependencias del sistema: {e}")
            return False

    def verificar_configuracion_setup(self) -> bool:
        """Verificar configuración del setup."""
        self._imprimir_header("VERIFICACIÓN DE CONFIGURACIÓN DE SETUP")

        try:
            # Verificar setup.py
            setup_py = self.project_root / "setup.py"
            if setup_py.exists():
                self._imprimir_exito("setup.py encontrado")

                # Verificar contenido básico
                contenido = setup_py.read_text(encoding="utf-8")
                if "name=" in contenido and "version=" in contenido:
                    self._imprimir_exito("setup.py contiene configuración básica")
                else:
                    self._imprimir_advertencia("setup.py puede estar incompleto")
            else:
                self._imprimir_error("setup.py no encontrado")
                return False

            # Verificar requirements.txt
            requirements = self.project_root / "requirements.txt"
            if requirements.exists():
                self._imprimir_exito("requirements.txt encontrado")

                # Contar líneas
                lineas = requirements.read_text(encoding="utf-8").strip().split("\n")
                lineas_no_vacias = [
                    l for l in lineas if l.strip() and not l.strip().startswith("#")
                ]
                self._imprimir_info(f"Dependencias listadas: {len(lineas_no_vacias)}")
            else:
                self._imprimir_advertencia("requirements.txt no encontrado")

            # Verificar directorio setup
            setup_dir = self.project_root / "setup"
            if setup_dir.exists():
                self._imprimir_info("Directorio setup encontrado")
            else:
                self._imprimir_advertencia("Directorio setup no encontrado")

            return True

        except Exception as e:
            self._imprimir_error(f"Error verificando configuración de setup: {e}")
            return False

    def generar_reporte(self) -> Dict:
        """Generar reporte de verificación."""
        self._imprimir_header("REPORTE DE VERIFICACIÓN")

        reporte = {
            "timestamp": self._timestamp(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.platform(),
            "project_root": str(self.project_root),
            "errores": self.errores,
            "advertencias": self.advertencias,
            "log_file": str(self.log_file),
        }

        # Guardar reporte detallado
        reporte_file = self.setup_dir / "logs" / "reporte_verificacion.txt"
        with open(reporte_file, "w", encoding="utf-8") as f:
            f.write("REPORTE DE VERIFICACIÓN DEL SISTEMA\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fecha y hora: {reporte['timestamp']}\n")
            f.write(f"Python: {reporte['python_version']}\n")
            f.write(f"Plataforma: {reporte['platform']}\n")
            f.write(f"Directorio del proyecto: {reporte['project_root']}\n\n")

            if self.errores:
                f.write("ERRORES ENCONTRADOS:\n")
                for i, error in enumerate(self.errores, 1):
                    f.write(f"{i}. {error}\n")
                f.write("\n")

            if self.advertencias:
                f.write("ADVERTENCIAS:\n")
                for i, advertencia in enumerate(self.advertencias, 1):
                    f.write(f"{i}. {advertencia}\n")
                f.write("\n")

            if not self.errores and not self.advertencias:
                f.write("✅ SISTEMA LISTO PARA INSTALACIÓN\n")

        self._imprimir_info(f"Reporte guardado en: {reporte_file}")

        return reporte

    def ejecutar_verificacion_completa(self) -> bool:
        """Ejecutar verificación completa del sistema."""
        print(Colors.CYAN + Colors.BOLD)
        print("█" * 80)
        print(
            "██                                                                          ██"
        )
        print(
            "██    🔍 VERIFICADOR DE SISTEMA - MATRIZ DE ROL v3.0                      ██"
        )
        print(
            "██    Verificación previa a la instalación                               ██"
        )
        print(
            "██                                                                          ██"
        )
        print("█" * 80)
        print(Colors.END)

        self._imprimir_info(f"📂 Directorio del proyecto: {self.project_root}")
        self._imprimir_info(f"📋 Log de verificación: {self.log_file}")

        verificaciones = [
            ("Python", self.verificar_python),
            ("Espacio en disco", self.verificar_espacio_disco),
            ("Permisos", self.verificar_permisos),
            ("Estructura del proyecto", self.verificar_estructura_proyecto),
            ("Dependencias del sistema", self.verificar_dependencias_sistema),
            ("Configuración de setup", self.verificar_configuracion_setup),
        ]

        todas_exitosas = True

        for nombre, verificacion in verificaciones:
            try:
                if not verificacion():
                    todas_exitosas = False
            except Exception as e:
                self._imprimir_error(f"Error durante verificación de {nombre}: {e}")
                todas_exitosas = False

        # Generar reporte
        reporte = self.generar_reporte()

        # Mostrar resumen final
        self._imprimir_header("RESUMEN FINAL")

        if todas_exitosas and len(self.errores) == 0:
            self._imprimir_con_color(
                "🎉 SISTEMA LISTO PARA INSTALACIÓN", Colors.GREEN + Colors.BOLD
            )
            self._imprimir_info("Puedes proceder con la instalación usando:")
            self._imprimir_info("  • setup/scripts/configurar_ambiente.bat")
            self._imprimir_info("  • setup/scripts/configurar_ambiente.ps1")
        else:
            self._imprimir_con_color("❌ SISTEMA NO LISTO", Colors.RED + Colors.BOLD)
            self._imprimir_error(f"Se encontraron {len(self.errores)} errores críticos")

            if self.errores:
                self._imprimir_info("Errores que deben resolverse:")
                for i, error in enumerate(self.errores, 1):
                    self._imprimir_con_color(f"  {i}. {error}", Colors.RED)

        if self.advertencias:
            self._imprimir_info(
                f"Se encontraron {len(self.advertencias)} advertencias (no críticas)"
            )

        self._escribir_log("Verificación completada")
        self._escribir_log("=" * 80)

        return todas_exitosas and len(self.errores) == 0


def main():
    """Función principal."""
    verificador = VerificadorSistema()

    try:
        exito = verificador.ejecutar_verificacion_completa()
        return 0 if exito else 1
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada por el usuario")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error inesperado durante la verificación: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

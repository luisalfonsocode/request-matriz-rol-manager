"""Interfaz gráfica para la solicitud de matrices de rol.

Este módulo proporciona una interfaz gráfica para:
1. Seleccionar múltiples matrices de rol desde un archivo de configuración
2. Ingresar múltiples grupos de red
3. Validar la existencia de los grupos de red en el dominio
4. Confirmar y procesar la solicitud

Clases:
    SolicitudMatrizFrame: Frame principal que contiene todos los elementos de la interfaz

Ejemplo:
    >>> from matriz_rol.gui.solicitud_matriz import main
    >>> main()
"""

import re
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Dict, List, Optional, Tuple, Any

import yaml
from customtkinter import CTkCheckBox, CTkFrame, CTkTextbox, CTkButton


class SolicitudMatrizFrame(CTkFrame):
    """Frame principal para la solicitud de matrices de rol.

    Esta clase maneja la interfaz de usuario para la selección de matrices
    y grupos de red, incluyendo todas las validaciones necesarias.

    Atributos:
        matrices_seleccionadas (List[str]): IDs de las matrices seleccionadas
        grupos_red (List[str]): Nombres de los grupos de red ingresados
        frame_matrices (ttk.LabelFrame): Contenedor para las matrices
        frame_grupos (ttk.LabelFrame): Contenedor para grupos de red
        txt_grupos (CTkTextbox): Campo para ingresar grupos
        btn_confirmar (CTkButton): Botón de confirmación
    """

    # Grupos predefinidos que siempre deben estar disponibles
    GRUPOS_PREDEFINIDOS = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]

    def __init__(self, master=None, callback_autorizadores=None):
        """Inicializa el frame de solicitud.

        Args:
            master: Widget padre (ventana principal)
            callback_autorizadores: Función callback para cuando se guardan autorizadores
        """
        super().__init__(master)
        self.callback_autorizadores = callback_autorizadores
        self.matrices_seleccionadas = []
        self.grupos_red = []

        # Callback para cuando se confirma la selección
        self.callback_confirmacion = None

        self.setup_ui()
        self.cargar_matrices()
        self.precargar_grupos_temporales()

    def setup_ui(self):
        """Configura los elementos de la interfaz."""
        # Frame para matrices
        self.frame_matrices = ttk.LabelFrame(self, text="Matrices de Rol Disponibles")
        self.frame_matrices.pack(pady=10, padx=10, fill="x")

        # Frame para grupos de red
        self.frame_grupos = ttk.LabelFrame(self, text="Grupos de Red")
        self.frame_grupos.pack(pady=10, padx=10, fill="x")

        # Campo de texto para grupos
        self.txt_grupos = CTkTextbox(self.frame_grupos, height=100)
        self.txt_grupos.pack(pady=5, padx=5, fill="x")
        ttk.Label(self.frame_grupos, text="Ingrese un grupo por línea").pack(pady=5)

        # Botón de confirmación
        self.btn_confirmar = CTkButton(
            self, text="Confirmar Selección", command=self.confirmar_seleccion
        )
        self.btn_confirmar.pack(pady=10)

    def cargar_matrices(self):
        """Carga las matrices desde el archivo de configuración."""
        try:
            config_path = Path(__file__).parents[3] / "config" / "matrices.yaml"
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            for matriz in config["matrices_rol"]:
                cb = CTkCheckBox(
                    self.frame_matrices,
                    text=f"{matriz['nombre']} ({matriz['id']})",
                    command=lambda m=matriz: self.toggle_matriz(m),
                )
                cb.pack(pady=2, padx=5, anchor="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matrices: {str(e)}")

    def toggle_matriz(self, matriz):
        """Maneja la selección/deselección de una matriz.

        Args:
            matriz: Diccionario con la información de la matriz
        """
        if matriz["id"] in self.matrices_seleccionadas:
            self.matrices_seleccionadas.remove(matriz["id"])
        else:
            self.matrices_seleccionadas.append(matriz["id"])

    def validar_grupos_red(self):
        """Valida la existencia de los grupos de red ingresados.

        Returns:
            tuple: (grupos_validos, grupos_invalidos)
        """
        grupos_validos = []
        grupos_invalidos = []

        for grupo in self.grupos_red:
            if not grupo.strip():
                continue

            try:
                # Ejecutar comando net group
                result = subprocess.run(
                    ["net", "group", grupo, "/domain"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    grupos_validos.append(grupo)
                else:
                    grupos_invalidos.append(grupo)

            except Exception:
                grupos_invalidos.append(grupo)

        return grupos_validos, grupos_invalidos

    def extraer_codigos_aplicacion(self, grupos_red: List[str]) -> List[str]:
        """Extrae códigos de aplicación de los grupos de red.

        Busca patrones de 4 dígitos alfanuméricos en los nombres de grupos.

        Args:
            grupos_red: Lista de nombres de grupos de red

        Returns:
            Lista de códigos de aplicación únicos encontrados
        """
        codigos = []
        patron = re.compile(r"[A-Z0-9]{4}")  # 4 caracteres alfanuméricos

        for grupo in grupos_red:
            # Encontrar todos los patrones de 4 caracteres alfanuméricos
            matches = patron.findall(grupo.upper())
            for match in matches:
                if match not in codigos:
                    codigos.append(match)

        return codigos

    def confirmar_seleccion(self):
        """Valida y confirma la selección de matrices y grupos."""
        # Validar que haya matrices seleccionadas
        if not self.matrices_seleccionadas:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar al menos una matriz"
            )
            return

        # Obtener grupos de red
        self.grupos_red = [
            g.strip()
            for g in self.txt_grupos.get("1.0", "end").split("\n")
            if g.strip()
        ]

        if not self.grupos_red:
            messagebox.showwarning(
                "Advertencia", "Debe ingresar al menos un grupo de red"
            )
            return

        # Extraer códigos de aplicación
        codigos_aplicacion = self.extraer_codigos_aplicacion(self.grupos_red)

        if not codigos_aplicacion:
            messagebox.showwarning(
                "Advertencia",
                "No se encontraron códigos de aplicación válidos en los grupos.\n"
                "Los códigos deben ser de 4 caracteres alfanuméricos.",
            )
            return

        # Abrir ventana de autorizadores
        self.abrir_ventana_autorizadores(codigos_aplicacion)

    def abrir_ventana_autorizadores(self, codigos_aplicacion: List[str]):
        """Abre una nueva ventana para gestionar autorizadores."""
        ventana_autorizadores = tk.Toplevel(self.master)
        ventana_autorizadores.title("Gestión de Autorizadores")
        ventana_autorizadores.geometry("800x600")

        # Crear el frame de autorizadores
        from .autorizadores_editor import AutorizadoresEditorFrame

        editor_frame = AutorizadoresEditorFrame(
            ventana_autorizadores,
            codigos_aplicacion=codigos_aplicacion,
            grupos_red=self.grupos_red,
        )

        # ⭐ ASIGNAR EL CALLBACK PARA CREAR SOLICITUDES ⭐
        if self.callback_autorizadores:
            print(
                "🔗 DEBUG MATRIZ: Asignando callback al editor desde solicitud_matriz"
            )
            editor_frame.callback_guardado = self.callback_autorizadores
            print(
                f"🔗 DEBUG MATRIZ: Callback asignado: {editor_frame.callback_guardado is not None}"
            )
        else:
            print("⚠️ DEBUG MATRIZ: callback_autorizadores no está definido!")

        editor_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def validar_grupos(self):
        """Valida los grupos de red y muestra resultados."""
        grupos_validos, grupos_invalidos = self.validar_grupos_red()

        mensaje = "Resultado de la validación:\n\n"

        if grupos_validos:
            mensaje += "Grupos válidos:\n"
            for grupo in grupos_validos:
                mensaje += f"✓ {grupo}\n"

        if grupos_invalidos:
            mensaje += "\nGrupos no encontrados:\n"
            for grupo in grupos_invalidos:
                mensaje += f"✗ {grupo}\n"

            continuar = messagebox.askyesno(
                "Grupos No Encontrados", f"{mensaje}\n¿Desea continuar de todas formas?"
            )

            if continuar:
                self.procesar_solicitud()
        else:
            self.procesar_solicitud()

    def procesar_solicitud(self):
        """Procesa la solicitud final."""
        # Aquí iría la lógica para procesar la solicitud
        messagebox.showinfo("Éxito", "Solicitud procesada correctamente")

    def precargar_grupos_temporales(self):
        """Precarga grupos de red temporales predefinidos."""
        # Insertar los grupos en el campo de texto
        grupos_texto = "\n".join(self.GRUPOS_PREDEFINIDOS)
        self.txt_grupos.delete("1.0", "end")
        self.txt_grupos.insert("1.0", grupos_texto)

        # Mostrar mensaje informativo
        messagebox.showinfo(
            "Grupos Temporales",
            "Se han precargado grupos temporales para pruebas.\n"
            "Puede agregar, modificar o eliminar según sea necesario.",
        )


def main():
    """Función principal para ejecutar la interfaz."""
    root = tk.Tk()
    root.title("Solicitud de Matrices de Rol")
    root.geometry("600x400")

    app = SolicitudMatrizFrame(root)
    app.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

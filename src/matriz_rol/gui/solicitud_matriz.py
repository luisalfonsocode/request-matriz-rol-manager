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

    def __init__(self, master=None):
        """Inicializa el frame de solicitud.

        Args:
            master: Widget padre (ventana principal)
        """
        super().__init__(master)
        self.matrices_seleccionadas = []
        self.grupos_red = []
        self.setup_ui()
        self.cargar_matrices()

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

        # Mostrar resumen
        resumen = "RESUMEN DE SOLICITUD\n\n"
        resumen += "Matrices seleccionadas:\n"
        for matriz_id in self.matrices_seleccionadas:
            resumen += f"- {matriz_id}\n"

        resumen += "\nGrupos de red:\n"
        for grupo in self.grupos_red:
            resumen += f"- {grupo}\n"

        continuar = messagebox.askyesno("Confirmar", f"{resumen}\n¿Desea continuar?")

        if continuar:
            self.validar_grupos()

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

# -*- coding: utf-8 -*-
"""Implementación del widget de autorizadores."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, TypedDict
import tkinter as tk
from tkinter import ttk, messagebox

from matriz_rol.gui.widgets import TabNotebook

logger = logging.getLogger(__name__)


class AutorizadorData(TypedDict, total=False):
    """Datos de un autorizador."""

    nombre: str
    correo: str
    rol: str


class MatrizData(TypedDict, total=False):
    """Datos de una matriz."""

    id: str
    nombre: str
    autorizadores: Dict[str, AutorizadorData]


class AutorizadoresTreeview(ttk.Treeview):
    """Treeview para mostrar matrices de autorización."""

    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        """Inicializa el Treeview de matrices.

        Args:
            parent: Widget padre.
            **kwargs: Argumentos adicionales para el Treeview.
        """
        super().__init__(parent, selectmode="browse", **kwargs)

        # Callback para selección
        self._selection_callback: Optional[callable] = None

        # Configurar columnas
        self["columns"] = ("nombre",)
        self.heading("#0", text="ID")
        self.heading("nombre", text="Nombre")
        self.column("#0", width=100)
        self.column("nombre", width=200)

        # Bind eventos
        self.bind("<<TreeviewSelect>>", self._on_selection)

    def set_selection_callback(self, callback: callable) -> None:
        """Establece el callback para cuando se selecciona una matriz.

        Args:
            callback: Función a llamar con el ID de la matriz seleccionada.
        """
        self._selection_callback = callback

    def _on_selection(self, event: tk.Event) -> None:
        """Maneja la selección de una matriz."""
        if not self._selection_callback:
            return

        selection = self.selection()
        if selection:
            matriz_id = selection[0]
            self._selection_callback(matriz_id)

    def clear(self) -> None:
        """Limpia todos los elementos del treeview."""
        for item in self.get_children():
            self.delete(item)

    def add_matriz(self, matriz_id: str, nombre: str) -> None:
        """Agrega una matriz al treeview.

        Args:
            matriz_id: ID único de la matriz.
            nombre: Nombre de la matriz.
        """
        self.insert("", "end", iid=matriz_id, text=matriz_id, values=(nombre,))


class AutorizadorEditFrame(ttk.Frame):
    """Frame para editar datos de un autorizador."""

    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        """Inicializa el frame de edición.

        Args:
            parent: Widget padre.
            **kwargs: Argumentos adicionales para el Frame.
        """
        super().__init__(parent, **kwargs)

        self._current_data: Optional[AutorizadorData] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario."""
        # Campo nombre
        ttk.Label(self, text="Nombre:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_nombre = ttk.Entry(self, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Campo correo
        ttk.Label(self, text="Correo:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_correo = ttk.Entry(self, width=30)
        self.entry_correo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Campo rol
        ttk.Label(self, text="Rol:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_rol = ttk.Combobox(
            self,
            values=["Administrador", "Editor", "Visualizador"],
            state="readonly",
            width=27,
        )
        self.combo_rol.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Guardar", command=self._save_changes).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Cancelar", command=self._cancel_changes).pack(
            side="left", padx=5
        )

        # Configurar expansión
        self.columnconfigure(1, weight=1)

    def load_autorizador(self, data: AutorizadorData) -> None:
        """Carga los datos de un autorizador en el formulario.

        Args:
            data: Datos del autorizador a editar.
        """
        self._current_data = data.copy()

        # Limpiar campos
        self.entry_nombre.delete(0, "end")
        self.entry_correo.delete(0, "end")
        self.combo_rol.set("")

        # Cargar datos
        self.entry_nombre.insert(0, data.get("nombre", ""))
        self.entry_correo.insert(0, data.get("correo", ""))
        self.combo_rol.set(data.get("rol", ""))

    def get_current_data(self) -> AutorizadorData:
        """Obtiene los datos actuales del formulario.

        Returns:
            Datos del autorizador desde el formulario.
        """
        return AutorizadorData(
            nombre=self.entry_nombre.get().strip(),
            correo=self.entry_correo.get().strip(),
            rol=self.combo_rol.get(),
        )

    def _save_changes(self) -> None:
        """Guarda los cambios realizados."""
        data = self.get_current_data()

        # Validar datos
        if not data.get("nombre"):
            messagebox.showerror("Error", "El nombre es requerido")
            return
        if not data.get("correo"):
            messagebox.showerror("Error", "El correo es requerido")
            return
        if "@" not in data.get("correo", ""):
            messagebox.showerror("Error", "El correo debe ser válido")
            return
        if not data.get("rol"):
            messagebox.showerror("Error", "Debe seleccionar un rol")
            return

        # Aquí iría la lógica para guardar en base de datos
        messagebox.showinfo("Éxito", "Autorizador guardado correctamente")
        logger.info(f"Autorizador guardado: {data}")

    def _cancel_changes(self) -> None:
        """Cancela los cambios y restaura los datos originales."""
        if self._current_data:
            self.load_autorizador(self._current_data)


class AutorizadoresMainFrame(ttk.Frame):
    """Frame principal con notebook para gestión de autorizadores."""

    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        """Inicializa el frame principal.

        Args:
            parent: Widget padre.
            **kwargs: Argumentos adicionales para el Frame.
        """
        super().__init__(parent, **kwargs)

        self._current_matriz: Optional[str] = None
        self._matrices_data: Dict[str, MatrizData] = {}

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario."""
        # Crear notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Selección de matriz
        self.frame_selection = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_selection, text="Seleccionar Matriz")

        # Configurar frame de selección
        ttk.Label(
            self.frame_selection,
            text="Seleccione una matriz para editar sus autorizadores:",
            font=("Arial", 10, "bold"),
        ).pack(pady=10)

        # Crear treeview con scrollbar
        tree_frame = ttk.Frame(self.frame_selection)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_matrices = AutorizadoresTreeview(tree_frame)
        self.tree_matrices.set_selection_callback(self._on_matriz_selected)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree_matrices.yview
        )
        self.tree_matrices.configure(yscrollcommand=scrollbar.set)

        self.tree_matrices.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tab 2: Edición de autorizador
        self.frame_edit = AutorizadorEditFrame(self.notebook)
        self.notebook.add(self.frame_edit, text="Editar Autorizador")

        # Inicialmente deshabilitar el segundo tab
        self.notebook.tab(1, state="disabled")

    def _on_matriz_selected(self, matriz_id: str) -> None:
        """Maneja la selección de una matriz.

        Args:
            matriz_id: ID de la matriz seleccionada.
        """
        self._current_matriz = matriz_id
        logger.info(f"Matriz seleccionada: {matriz_id}")

        # Buscar datos de la matriz
        matriz_data = self._matrices_data.get(matriz_id)
        if not matriz_data:
            messagebox.showerror(
                "Error", f"No se encontraron datos para la matriz {matriz_id}"
            )
            return

        # Simular datos de autorizador (en implementación real vendría de BD)
        autorizador_data = AutorizadorData(
            nombre=f"Autorizador para {matriz_data.get('nombre', matriz_id)}",
            correo=f"autorizador.{matriz_id.lower()}@empresa.com",
            rol="Administrador",
        )

        # Cargar datos en el frame de edición
        self.frame_edit.load_autorizador(autorizador_data)

        # Habilitar y cambiar al tab de edición
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)

        logger.info(f"Cambiado al tab de edición para matriz: {matriz_id}")

    def load_matrices(self, matrices: Dict[str, MatrizData]) -> None:
        """Carga las matrices disponibles.

        Args:
            matrices: Diccionario con las matrices disponibles.
        """
        self._matrices_data = matrices.copy()

        # Limpiar treeview
        self.tree_matrices.clear()

        # Agregar matrices ordenadas por nombre
        sorted_matrices = sorted(
            matrices.items(), key=lambda x: x[1].get("nombre", x[0])
        )

        for matriz_id, matriz_data in sorted_matrices:
            self.tree_matrices.add_matriz(
                matriz_id=matriz_id, nombre=matriz_data.get("nombre", matriz_id)
            )

        logger.info(f"Cargadas {len(matrices)} matrices")

    def get_current_matriz(self) -> Optional[str]:
        """Obtiene la matriz actualmente seleccionada.

        Returns:
            ID de la matriz actual o None si no hay selección.
        """
        return self._current_matriz

    def actualizar_aplicaciones(self, grupos: List[str]) -> None:
        """Actualiza las matrices basándose en los grupos proporcionados.

        Args:
            grupos: Lista de grupos de red para generar matrices.
        """
        logger.info(f"Actualizando aplicaciones con {len(grupos)} grupos")

        # Generar matrices basadas en los grupos
        matrices_generadas: Dict[str, MatrizData] = {}

        for i, grupo in enumerate(grupos, 1):
            matriz_id = f"MAT{i:03d}"
            matrices_generadas[matriz_id] = MatrizData(
                id=matriz_id, nombre=f"Matriz para {grupo}", autorizadores={}
            )

        # Cargar las matrices generadas
        self.load_matrices(matrices_generadas)

        logger.info(f"Generadas {len(matrices_generadas)} matrices para los grupos")


# Función de ejemplo para usar el widget
def main() -> None:
    """Función principal de ejemplo."""
    root = tk.Tk()
    root.title("Gestión de Autorizadores")
    root.geometry("800x600")

    # Crear frame principal
    main_frame = AutorizadoresMainFrame(root)
    main_frame.pack(fill="both", expand=True)

    # Datos de ejemplo
    matrices_ejemplo = {
        "MAT001": MatrizData(
            id="MAT001", nombre="Matriz de Administración", autorizadores={}
        ),
        "MAT002": MatrizData(
            id="MAT002", nombre="Matriz de Operaciones", autorizadores={}
        ),
        "MAT003": MatrizData(
            id="MAT003", nombre="Matriz de Finanzas", autorizadores={}
        ),
    }

    # Cargar matrices de ejemplo
    main_frame.load_matrices(matrices_ejemplo)

    root.mainloop()


if __name__ == "__main__":
    main()

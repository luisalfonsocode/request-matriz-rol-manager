"""
Lista principal de solicitudes de conformidad.

Proporciona el TreeView principal y la lógica de visualización de solicitudes.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from customtkinter import CTkFrame, CTkLabel
from ....data.gestor_solicitudes import SolicitudConformidad, EstadoSolicitud


class ListaSolicitudes(CTkFrame):
    """TreeView principal para mostrar la lista de solicitudes."""

    def __init__(
        self,
        master,
        callback_seleccion: Callable[[Optional[SolicitudConformidad]], None],
        callback_doble_clic: Callable[[tk.Event], None],
    ):
        """
        Inicializa la lista de solicitudes.

        Args:
            master: Widget padre
            callback_seleccion: Función a llamar cuando se selecciona una solicitud
            callback_doble_clic: Función a llamar en doble clic
        """
        super().__init__(master)
        self.callback_seleccion = callback_seleccion
        self.callback_doble_clic = callback_doble_clic

        # Variables de control
        self.editando = False
        self.combobox_editor = None
        self.solicitudes_actuales: List[SolicitudConformidad] = []

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        """Configura la interfaz de la lista de solicitudes."""
        # Título del panel
        titulo = CTkLabel(
            self, text="📋 Lista de Solicitudes:", font=("Arial", 12, "bold")
        )
        titulo.pack(anchor="w", padx=5, pady=5)

        # Frame para el TreeView
        frame_tree = CTkFrame(self)
        frame_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame interno para tkinter TreeView
        self.tree_frame = tk.Frame(frame_tree)
        self.tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self._crear_treeview()
        self._configurar_scrollbars()
        self._bind_eventos()

    def _crear_treeview(self) -> None:
        """Crea y configura el TreeView."""
        # Definir columnas
        columnas = (
            "ID",
            "Fecha",
            "Estado",
            "Grupos",
            "Autorizadores",
            "Ticket",
            "Observaciones",
        )

        self.tree_solicitudes = ttk.Treeview(
            self.tree_frame, columns=columnas, show="headings", height=10
        )

        # Configurar encabezados
        self._configurar_encabezados()

        # Configurar anchos de columna
        self._configurar_columnas()

    def _configurar_encabezados(self) -> None:
        """Configura los encabezados del TreeView."""
        encabezados = {
            "ID": "ID Solicitud",
            "Fecha": "Fecha Creación",
            "Estado": "Estado",
            "Grupos": "Grupos Red",
            "Autorizadores": "# Autorizadores",
            "Ticket": "Ticket Helpdesk",
            "Observaciones": "Observaciones",
        }

        for col, texto in encabezados.items():
            self.tree_solicitudes.heading(col, text=texto)

    def _configurar_columnas(self) -> None:
        """Configura los anchos de las columnas."""
        anchos = {
            "ID": 150,
            "Fecha": 120,
            "Estado": 80,
            "Grupos": 100,
            "Autorizadores": 80,
            "Ticket": 100,
            "Observaciones": 200,
        }

        for col, ancho in anchos.items():
            self.tree_solicitudes.column(col, width=ancho)

    def _configurar_scrollbars(self) -> None:
        """Configura las barras de desplazamiento."""
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(
            self.tree_frame, orient="vertical", command=self.tree_solicitudes.yview
        )

        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(
            self.tree_frame, orient="horizontal", command=self.tree_solicitudes.xview
        )

        self.tree_solicitudes.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
        )

        # Posicionar elementos
        self.tree_solicitudes.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

    def _bind_eventos(self) -> None:
        """Vincula los eventos del TreeView."""
        self.tree_solicitudes.bind("<<TreeviewSelect>>", self._on_seleccion)
        self.tree_solicitudes.bind("<Double-1>", self._on_doble_clic)

    def _on_seleccion(self, event: tk.Event) -> None:
        """Maneja la selección de una solicitud."""
        seleccion = self.tree_solicitudes.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree_solicitudes.item(item, "values")
            if valores:
                id_solicitud = valores[0]
                solicitud = self._buscar_solicitud_por_id(id_solicitud)
                self.callback_seleccion(solicitud)
        else:
            self.callback_seleccion(None)

    def _on_doble_clic(self, event: tk.Event) -> None:
        """Maneja el doble clic en el TreeView."""
        self.callback_doble_clic(event)

    def _buscar_solicitud_por_id(
        self, id_solicitud: str
    ) -> Optional[SolicitudConformidad]:
        """
        Busca una solicitud por su ID.

        Args:
            id_solicitud: ID de la solicitud a buscar

        Returns:
            Solicitud encontrada o None
        """
        for solicitud in self.solicitudes_actuales:
            if solicitud.id_solicitud == id_solicitud:
                return solicitud
        return None

    def actualizar_solicitudes(self, solicitudes: List[SolicitudConformidad]) -> None:
        """
        Actualiza la lista de solicitudes mostrada.

        Args:
            solicitudes: Lista de solicitudes a mostrar
        """
        # Guardar referencia a las solicitudes
        self.solicitudes_actuales = solicitudes

        # Limpiar lista actual
        for item in self.tree_solicitudes.get_children():
            self.tree_solicitudes.delete(item)

        # Agregar solicitudes ordenadas por fecha
        solicitudes_ordenadas = sorted(
            solicitudes, key=lambda x: x.fecha_creacion, reverse=True
        )

        for solicitud in solicitudes_ordenadas:
            self._agregar_solicitud_a_tree(solicitud)

        # Configurar colores por estado
        self._configurar_colores_estado()

    def _agregar_solicitud_a_tree(self, solicitud: SolicitudConformidad) -> None:
        """Agrega una solicitud al TreeView."""
        fecha_corta = (
            solicitud.fecha_creacion.split("T")[0]
            if "T" in solicitud.fecha_creacion
            else solicitud.fecha_creacion
        )

        grupos_texto = f"{len(solicitud.grupos_red)} grupo(s)"

        observaciones_cortas = (
            (solicitud.observaciones or "")[:50] + "..."
            if len(solicitud.observaciones or "") > 50
            else (solicitud.observaciones or "")
        )

        # Determinar tags para colores
        tags = [self._obtener_tag_estado(solicitud.estado)]

        self.tree_solicitudes.insert(
            "",
            "end",
            values=(
                solicitud.id_solicitud,
                fecha_corta,
                solicitud.estado.value.title(),
                grupos_texto,
                len(solicitud.autorizadores),
                solicitud.ticket_helpdesk or "",
                observaciones_cortas,
            ),
            tags=tags,
        )

    def _obtener_tag_estado(self, estado: EstadoSolicitud) -> str:
        """Obtiene el tag de color para un estado."""
        mapeo_tags = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: "en_solicitud",
            EstadoSolicitud.EN_HELPDESK: "en_helpdesk",
            EstadoSolicitud.ATENDIDO: "atendido",
            EstadoSolicitud.CERRADO: "cerrado",
        }
        return mapeo_tags.get(estado, "default")

    def _configurar_colores_estado(self) -> None:
        """Configura los colores por estado en el TreeView."""
        self.tree_solicitudes.tag_configure("en_solicitud", background="#E8F5E8")
        self.tree_solicitudes.tag_configure("en_helpdesk", background="#FFF3E0")
        self.tree_solicitudes.tag_configure("atendido", background="#F3E5F5")
        self.tree_solicitudes.tag_configure("cerrado", background="#F5F5F5")

    def obtener_solicitud_seleccionada(self) -> Optional[SolicitudConformidad]:
        """
        Obtiene la solicitud actualmente seleccionada.

        Returns:
            Solicitud seleccionada o None
        """
        seleccion = self.tree_solicitudes.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree_solicitudes.item(item, "values")
            if valores:
                return self._buscar_solicitud_por_id(valores[0])
        return None

    def limpiar_seleccion(self) -> None:
        """Limpia la selección actual."""
        self.tree_solicitudes.selection_remove(self.tree_solicitudes.selection())

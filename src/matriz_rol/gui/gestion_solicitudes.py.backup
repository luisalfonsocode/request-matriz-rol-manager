"""
Frame para gestionar y hacer seguimiento de solicitudes de conformidad.

Permite ver, filtrar y actualizar el estado de todas las solicitudes.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict, Optional
from customtkinter import (
    CTkFrame,
    CTkButton,
    CTkLabel,
    CTkComboBox,
    CTkEntry,
    CTkTextbox,
)
from datetime import datetime
from ..data.gestor_solicitudes import (
    GestorSolicitudes,
    SolicitudConformidad,
    EstadoSolicitud,
)
from ..data.gestor_autorizadores import GestorAutorizadores


class GestionSolicitudesFrame(CTkFrame):
    """Frame para gestionar solicitudes de conformidad."""

    def __init__(self, master, gestor_solicitudes: GestorSolicitudes):
        """Inicializa el frame de gestión de solicitudes."""
        super().__init__(master)

        self.gestor = gestor_solicitudes  # Usar el gestor pasado como parámetro
        self.solicitud_seleccionada: Optional[SolicitudConformidad] = None

        self.configurar_interfaz()
        self.actualizar_lista_solicitudes()

    def configurar_interfaz(self):
        """Configura la interfaz del frame."""
        # Título
        titulo = CTkLabel(
            self,
            text="📋 Gestión de Solicitudes de Conformidad",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

        # Frame superior con estadísticas y filtros
        frame_superior = CTkFrame(self)
        frame_superior.pack(fill="x", padx=10, pady=5)

        self.configurar_estadisticas(frame_superior)
        self.configurar_filtros(frame_superior)

        # Frame principal con la lista de solicitudes
        frame_principal = CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=5)

        self.configurar_lista_solicitudes(frame_principal)

        # Frame inferior con detalles y acciones
        frame_inferior = CTkFrame(self)
        frame_inferior.pack(fill="x", padx=10, pady=5)

        self.configurar_panel_detalles(frame_inferior)

    def configurar_estadisticas(self, parent):
        """Configura el panel de estadísticas."""
        frame_stats = CTkFrame(parent)
        frame_stats.pack(fill="x", padx=5, pady=5)

        CTkLabel(frame_stats, text="📊 Estadísticas:", font=("Arial", 12, "bold")).pack(
            anchor="w", padx=5, pady=2
        )

        self.frame_contadores = CTkFrame(frame_stats)
        self.frame_contadores.pack(fill="x", padx=5, pady=2)

        # Los labels de estadísticas se crearán dinámicamente
        self.labels_stats = {}

    def configurar_filtros(self, parent):
        """Configura los filtros de solicitudes."""
        frame_filtros = CTkFrame(parent)
        frame_filtros.pack(fill="x", padx=5, pady=5)

        CTkLabel(frame_filtros, text="🔍 Filtros:", font=("Arial", 12, "bold")).pack(
            anchor="w", padx=5, pady=2
        )

        frame_controles = CTkFrame(frame_filtros)
        frame_controles.pack(fill="x", padx=5, pady=2)

        # Filtro por estado
        CTkLabel(frame_controles, text="Estado:").pack(side="left", padx=5)
        self.combo_filtro_estado = CTkComboBox(
            frame_controles,
            values=[
                "Todas",
                "En solicitud de conformidades",
                "En Helpdesk",
                "Atendido",
                "Cerrado",
            ],
            command=self.aplicar_filtros,
        )
        self.combo_filtro_estado.pack(side="left", padx=5)
        self.combo_filtro_estado.set("Todas")

        # Botón de actualizar
        btn_actualizar = CTkButton(
            frame_controles, text="🔄 Actualizar", command=self.actualizar_manual
        )
        btn_actualizar.pack(side="left", padx=10)

    def configurar_lista_solicitudes(self, parent):
        """Configura la lista de solicitudes."""
        CTkLabel(
            parent, text="📋 Lista de Solicitudes:", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=5, pady=5)

        # Frame para el treeview
        frame_tree = CTkFrame(parent)
        frame_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear treeview con scrollbars
        self.tree_frame = tk.Frame(frame_tree)
        self.tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

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
        self.tree_solicitudes.heading("ID", text="ID Solicitud")
        self.tree_solicitudes.heading("Fecha", text="Fecha Creación")
        self.tree_solicitudes.heading("Estado", text="Estado")
        self.tree_solicitudes.heading("Grupos", text="Grupos Red")
        self.tree_solicitudes.heading("Autorizadores", text="# Autorizadores")
        self.tree_solicitudes.heading("Ticket", text="Ticket Helpdesk")
        self.tree_solicitudes.heading("Observaciones", text="Observaciones")

        # Configurar anchos de columna
        self.tree_solicitudes.column("ID", width=150)
        self.tree_solicitudes.column("Fecha", width=120)
        self.tree_solicitudes.column("Estado", width=80)
        self.tree_solicitudes.column("Grupos", width=100)
        self.tree_solicitudes.column("Autorizadores", width=80)
        self.tree_solicitudes.column("Ticket", width=100)
        self.tree_solicitudes.column("Observaciones", width=200)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(
            self.tree_frame, orient="vertical", command=self.tree_solicitudes.yview
        )
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

        # Evento de selección
        self.tree_solicitudes.bind("<<TreeviewSelect>>", self.on_solicitud_seleccionada)
        self.tree_solicitudes.bind("<Double-1>", self.on_doble_clic_grilla)

        # Variable para controlar la edición
        self.editando = False
        self.combobox_editor = None

    def configurar_panel_detalles(self, parent):
        """Configura el panel de detalles y acciones."""
        CTkLabel(
            parent, text="📝 Detalles y Acciones:", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=5, pady=5)

        # Frame principal de detalles
        frame_detalles = CTkFrame(parent)
        frame_detalles.pack(fill="x", padx=5, pady=5)

        # Lado izquierdo - Información
        frame_info = CTkFrame(frame_detalles)
        frame_info.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        CTkLabel(frame_info, text="ℹ️ Información Seleccionada:").pack(
            anchor="w", padx=5, pady=2
        )
        self.label_info_solicitud = CTkLabel(
            frame_info, text="Seleccione una solicitud para ver detalles"
        )
        self.label_info_solicitud.pack(anchor="w", padx=5, pady=2)

        # Lado derecho - Acciones
        frame_acciones = CTkFrame(frame_detalles)
        frame_acciones.pack(side="right", padx=5, pady=5)

        CTkLabel(frame_acciones, text="⚡ Acciones:").pack(anchor="w", padx=5, pady=2)

        # Botones de estado actualizados
        CTkButton(
            frame_acciones, text="🎫 Enviar a Helpdesk", command=self.enviar_a_helpdesk
        ).pack(pady=2, padx=5)
        CTkButton(
            frame_acciones, text="✅ Marcar como Atendido", command=self.marcar_atendido
        ).pack(pady=2, padx=5)
        CTkButton(
            frame_acciones, text="🏁 Cerrar Solicitud", command=self.cerrar_solicitud
        ).pack(pady=2, padx=5)
        CTkButton(
            frame_acciones, text="� Reabrir Solicitud", command=self.reabrir_solicitud
        ).pack(pady=2, padx=5)
        CTkButton(
            frame_acciones,
            text="📋 Ver Detalles Completos",
            command=self.ver_detalles_solicitud,
        ).pack(pady=2, padx=5)

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas."""
        stats = self.gestor.obtener_estadisticas()

        # Limpiar labels anteriores
        for widget in self.frame_contadores.winfo_children():
            widget.destroy()

        # Crear nuevos labels con los estados actualizados
        info_stats = [
            (f"📊 Total: {stats['total']}", "#2196F3"),
            (f"� En solicitud: {stats['en_solicitud']}", "#4CAF50"),
            (f"🎫 En Helpdesk: {stats['en_helpdesk']}", "#FF9800"),
            (f"✅ Atendido: {stats['atendido']}", "#9C27B0"),
            (f"🏁 Cerrado: {stats['cerrado']}", "#9E9E9E"),
        ]

        for i, (texto, color) in enumerate(info_stats):
            label = CTkLabel(self.frame_contadores, text=texto, text_color=color)
            label.pack(side="left", padx=10, pady=2)

    def actualizar_lista_solicitudes(self):
        """Actualiza la lista de solicitudes mostrada."""
        print("🔄 Actualizando lista de solicitudes en UI...")

        # Limpiar lista actual
        for item in self.tree_solicitudes.get_children():
            self.tree_solicitudes.delete(item)

        # Forzar recarga desde archivo
        print(f"🔄 Forzando recarga desde archivo...")
        self.gestor.cargar_solicitudes()
        solicitudes = self.gestor.obtener_solicitudes()

        print(f"📊 {len(solicitudes)} solicitudes obtenidas del gestor")
        if solicitudes:
            print(f"📋 Solicitudes encontradas:")
            for sol in solicitudes:
                print(f"   - {sol.id_solicitud} ({sol.estado.value})")

        # Aplicar filtro actual
        filtro_estado = self.combo_filtro_estado.get()
        if filtro_estado != "Todas":
            estado_filtro = {
                "En solicitud de conformidades": EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,
                "En Helpdesk": EstadoSolicitud.EN_HELPDESK,
                "Atendido": EstadoSolicitud.ATENDIDO,
                "Cerrado": EstadoSolicitud.CERRADO,
            }.get(filtro_estado)

            if estado_filtro:
                solicitudes = [s for s in solicitudes if s.estado == estado_filtro]

        print(f"📈 {len(solicitudes)} solicitudes después de aplicar filtros")

        # Agregar solicitudes a la lista
        for i, solicitud in enumerate(
            sorted(solicitudes, key=lambda x: x.fecha_creacion, reverse=True)
        ):
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

            # Definir colores por estado
            tags = []
            if solicitud.estado == EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES:
                tags = ["en_solicitud"]
            elif solicitud.estado == EstadoSolicitud.EN_HELPDESK:
                tags = ["en_helpdesk"]
            elif solicitud.estado == EstadoSolicitud.ATENDIDO:
                tags = ["atendido"]
            elif solicitud.estado == EstadoSolicitud.CERRADO:
                tags = ["cerrado"]

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

            print(f"  ➤ Insertada: {solicitud.id_solicitud}")

        print(f"✅ {len(solicitudes)} solicitudes mostradas en la interfaz")

        # Configurar colores por estado
        self.tree_solicitudes.tag_configure(
            "en_solicitud", background="#E8F5E8"
        )  # Verde claro
        self.tree_solicitudes.tag_configure(
            "en_helpdesk", background="#FFF3E0"
        )  # Naranja claro
        self.tree_solicitudes.tag_configure(
            "atendido", background="#F3E5F5"
        )  # Violeta claro
        self.tree_solicitudes.tag_configure(
            "cerrado", background="#F5F5F5"
        )  # Gris claro

        # Actualizar estadísticas
        self.actualizar_estadisticas()

    def enviar_a_helpdesk(self):
        """Envía la solicitud seleccionada al helpdesk."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        if self.solicitud_seleccionada.estado == EstadoSolicitud.CERRADO:
            messagebox.showinfo("Información", "La solicitud ya está cerrada")
            return

        # Pedir número de ticket
        from tkinter import simpledialog

        ticket = simpledialog.askstring(
            "Enviar a Helpdesk",
            f"Ingrese el número de ticket para la solicitud:\n{self.solicitud_seleccionada.id_solicitud}",
        )

        if ticket:
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_seleccionada.id_solicitud,
                EstadoSolicitud.EN_HELPDESK,
                ticket,
                "Solicitud enviada al sistema de Helpdesk",
            ):
                messagebox.showinfo(
                    "Éxito", f"✅ Solicitud enviada al Helpdesk\nTicket: {ticket}"
                )
                self.actualizar_lista_solicitudes()
                self.actualizar_info_seleccionada()

    def marcar_atendido(self):
        """Marca la solicitud como atendida."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        if self.solicitud_seleccionada.estado == EstadoSolicitud.CERRADO:
            messagebox.showinfo("Información", "La solicitud ya está cerrada")
            return

        # Pedir observaciones
        from tkinter import simpledialog

        observaciones = simpledialog.askstring(
            "Marcar como Atendido",
            f"Observaciones para la solicitud:\n{self.solicitud_seleccionada.id_solicitud}",
            initialvalue="Solicitud atendida correctamente",
        )

        if observaciones is not None:  # Permitir cadena vacía
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_seleccionada.id_solicitud,
                EstadoSolicitud.ATENDIDO,
                observaciones=observaciones,
            ):
                messagebox.showinfo("Éxito", "✅ Solicitud marcada como atendida")
                self.actualizar_lista_solicitudes()
                self.actualizar_info_seleccionada()

    def actualizar_manual(self):
        """Actualización manual activada por el usuario con feedback."""
        print("\n🔄 ACTUALIZACIÓN MANUAL INICIADA POR USUARIO")

        try:
            # Mostrar mensaje de progreso
            messagebox.showinfo(
                "Actualizando", "⏳ Recargando solicitudes desde BD local..."
            )

            # Forzar recarga completa
            self.gestor.cargar_solicitudes()
            self.actualizar_lista_solicitudes()

            # Mostrar mensaje de confirmación
            info_bd = self.gestor.obtener_info_bd()
            mensaje = (
                f"✅ Actualización completada!\n\n"
                f"📊 Total solicitudes: {info_bd['total_solicitudes']}\n"
                f"💾 BD Local: {info_bd['tamaño_kb']} KB\n"
                f"📅 Última modificación: {info_bd.get('ultima_modificacion', 'N/A')[:19]}"
            )
            messagebox.showinfo("Actualización Exitosa", mensaje)

        except Exception as e:
            print(f"❌ Error en actualización manual: {e}")
            messagebox.showerror("Error", f"❌ Error actualizando:\n{e}")

    def aplicar_filtros(self, event=None):
        """Aplica los filtros seleccionados."""
        self.actualizar_lista_solicitudes()

    def on_doble_clic_grilla(self, event):
        """Maneja el doble clic en la grilla para editar estado, ticket u observaciones."""
        if self.editando:
            return

        # Obtener el elemento y columna clickeada
        item = self.tree_solicitudes.identify_row(event.y)
        columna = self.tree_solicitudes.identify_column(event.x)

        # Permitir edición en columna de Estado (#3), Ticket (#6) u Observaciones (#7)
        if item and columna == "#3":
            self.editar_estado_en_grilla(item, event)
        elif item and columna == "#6":
            self.editar_ticket_en_grilla(item, event)
        elif item and columna == "#7":
            self.editar_observaciones_en_grilla(item, event)
        else:
            # Si no es columna editable, mostrar detalles
            self.ver_detalles_solicitud(event)

    def editar_estado_en_grilla(self, item, event):
        """Permite editar el estado directamente en la grilla."""
        # Obtener datos del item
        valores = self.tree_solicitudes.item(item, "values")
        if not valores:
            return

        id_solicitud = valores[0]
        estado_actual = valores[2]

        # Verificar que la solicitud existe
        solicitud = self.gestor.obtener_solicitud_por_id(id_solicitud)
        if not solicitud:
            messagebox.showerror("Error", "No se encontró la solicitud")
            return

        # Obtener posición y tamaño de la celda
        bbox = self.tree_solicitudes.bbox(item, column="#3")
        if not bbox:
            return

        x, y, width, height = bbox

        # Crear combobox para editar
        # Lista de estados permitidos con transiciones lógicas
        estados_permitidos = self.obtener_estados_permitidos(solicitud.estado)

        if not estados_permitidos:
            messagebox.showinfo(
                "Sin cambios",
                f"El estado '{estado_actual}' no permite cambios directos.\n"
                "Use los botones de acción para cambiar el estado.",
            )
            return

        # Crear el combobox temporal
        self.editando = True
        self.combobox_editor = ttk.Combobox(
            self.tree_solicitudes,
            values=[estado.value for estado in estados_permitidos],
            state="readonly",
        )

        # Posicionar el combobox sobre la celda
        self.combobox_editor.place(x=x, y=y, width=width, height=height)
        self.combobox_editor.set(estado_actual)
        self.combobox_editor.focus_set()

        # Eventos para guardar o cancelar
        def guardar_estado(event=None):
            nuevo_estado_texto = self.combobox_editor.get()
            self.finalizar_edicion()

            # Buscar el enum correspondiente
            nuevo_estado = None
            for estado in EstadoSolicitud:
                if estado.value == nuevo_estado_texto:
                    nuevo_estado = estado
                    break

            if nuevo_estado and nuevo_estado != solicitud.estado:
                self.cambiar_estado_solicitud(id_solicitud, nuevo_estado)

        def cancelar_edicion(event=None):
            self.finalizar_edicion()

        # Bind eventos
        self.combobox_editor.bind("<<ComboboxSelected>>", guardar_estado)
        self.combobox_editor.bind("<Return>", guardar_estado)
        self.combobox_editor.bind("<Escape>", cancelar_edicion)
        self.combobox_editor.bind("<FocusOut>", cancelar_edicion)

    def obtener_estados_permitidos(self, estado_actual):
        """Obtiene los estados permitidos para transición desde el estado actual."""
        transiciones = {
            EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES: [
                EstadoSolicitud.EN_HELPDESK,
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.EN_HELPDESK: [
                EstadoSolicitud.ATENDIDO,
                EstadoSolicitud.EN_SOLICITUD_CONFORMIDADES,  # Retroceso si es necesario
                EstadoSolicitud.CERRADO,
            ],
            EstadoSolicitud.ATENDIDO: [
                EstadoSolicitud.CERRADO,
                EstadoSolicitud.EN_HELPDESK,  # Retroceso si es necesario
            ],
            EstadoSolicitud.CERRADO: [
                # Estado final, no se permite cambio directo
            ],
        }

        return transiciones.get(estado_actual, [])

    def finalizar_edicion(self):
        """Finaliza la edición del combobox."""
        if self.combobox_editor:
            self.combobox_editor.destroy()
            self.combobox_editor = None
        self.editando = False

    def cambiar_estado_solicitud(self, id_solicitud, nuevo_estado):
        """Cambia el estado de una solicitud con validaciones."""
        # Obtener la solicitud
        solicitud = self.gestor.obtener_solicitud_por_id(id_solicitud)
        if not solicitud:
            return

        # Validaciones especiales según el nuevo estado
        if nuevo_estado == EstadoSolicitud.EN_HELPDESK:
            # Pedir número de ticket
            from tkinter import simpledialog

            ticket = simpledialog.askstring(
                "Enviar a Helpdesk",
                f"Ingrese el número de ticket para:\n{id_solicitud}",
                initialvalue=solicitud.ticket_helpdesk or "",
            )
            if ticket is None:  # Usuario canceló
                return

            if self.gestor.actualizar_estado_solicitud(
                id_solicitud, nuevo_estado, ticket, "Estado actualizado desde grilla"
            ):
                messagebox.showinfo(
                    "Éxito", f"✅ Solicitud enviada al Helpdesk\nTicket: {ticket}"
                )
                self.actualizar_lista_solicitudes()

        elif nuevo_estado == EstadoSolicitud.ATENDIDO:
            # Pedir observaciones
            from tkinter import simpledialog

            observaciones = simpledialog.askstring(
                "Marcar como Atendido",
                f"Observaciones para:\n{id_solicitud}",
                initialvalue="Solicitud atendida correctamente",
            )
            if observaciones is None:  # Usuario canceló
                return

            if self.gestor.actualizar_estado_solicitud(
                id_solicitud, nuevo_estado, observaciones=observaciones
            ):
                messagebox.showinfo("Éxito", "✅ Solicitud marcada como atendida")
                self.actualizar_lista_solicitudes()

        elif nuevo_estado == EstadoSolicitud.CERRADO:
            # Confirmar cierre
            respuesta = messagebox.askyesno(
                "Cerrar Solicitud",
                f"¿Está seguro de cerrar la solicitud?\n{id_solicitud}\n\n"
                "Esta acción marcará la solicitud como completada.",
            )
            if respuesta:
                if self.gestor.actualizar_estado_solicitud(
                    id_solicitud, nuevo_estado, observaciones="Cerrada desde grilla"
                ):
                    messagebox.showinfo("Éxito", "✅ Solicitud cerrada")
                    self.actualizar_lista_solicitudes()

        else:
            # Cambio simple sin validaciones adicionales
            if self.gestor.actualizar_estado_solicitud(
                id_solicitud,
                nuevo_estado,
                observaciones="Estado actualizado desde grilla",
            ):
                messagebox.showinfo(
                    "Éxito", f"✅ Estado actualizado a: {nuevo_estado.value}"
                )
                self.actualizar_lista_solicitudes()

    def editar_ticket_en_grilla(self, item, event):
        """Permite editar el número de ticket directamente en la grilla."""
        # Obtener datos del item
        valores = self.tree_solicitudes.item(item, "values")
        if not valores:
            return

        id_solicitud = valores[0]
        ticket_actual = valores[5]  # Columna de ticket

        # Verificar que la solicitud existe
        solicitud = self.gestor.obtener_solicitud_por_id(id_solicitud)
        if not solicitud:
            messagebox.showerror("Error", "No se encontró la solicitud")
            return

        # Obtener posición y tamaño de la celda
        bbox = self.tree_solicitudes.bbox(item, column="#6")
        if not bbox:
            return

        x, y, width, height = bbox

        # Crear entry para editar
        self.editando = True
        self.entry_editor = tk.Entry(self.tree_solicitudes)

        # Posicionar el entry sobre la celda
        self.entry_editor.place(x=x, y=y, width=width, height=height)
        self.entry_editor.insert(0, ticket_actual or "")
        self.entry_editor.focus_set()
        self.entry_editor.select_range(0, tk.END)

        # Eventos para guardar o cancelar
        def guardar_ticket(event=None):
            nuevo_ticket = self.entry_editor.get().strip()
            self.finalizar_edicion_entry()

            # Actualizar ticket en la solicitud
            if self.gestor.actualizar_estado_solicitud(
                id_solicitud,
                solicitud.estado,  # Mantener el mismo estado
                ticket_helpdesk=nuevo_ticket if nuevo_ticket else None,
                observaciones=f"Ticket actualizado desde grilla: {nuevo_ticket or 'Sin ticket'}",
            ):
                messagebox.showinfo(
                    "Éxito", f"✅ Ticket actualizado: {nuevo_ticket or 'Sin ticket'}"
                )
                self.actualizar_lista_solicitudes()

        def cancelar_edicion_entry(event=None):
            self.finalizar_edicion_entry()

        # Bind eventos
        self.entry_editor.bind("<Return>", guardar_ticket)
        self.entry_editor.bind("<Escape>", cancelar_edicion_entry)
        self.entry_editor.bind("<FocusOut>", cancelar_edicion_entry)

    def finalizar_edicion_entry(self):
        """Finaliza la edición del entry."""
        if hasattr(self, "entry_editor") and self.entry_editor:
            self.entry_editor.destroy()
            self.entry_editor = None
        self.editando = False

    def editar_observaciones_en_grilla(self, item, event):
        """Permite editar las observaciones directamente en la grilla."""
        # Obtener datos del item
        valores = self.tree_solicitudes.item(item, "values")
        if not valores:
            return

        id_solicitud = valores[0]
        observaciones_actuales = (
            valores[6] if len(valores) > 6 else ""
        )  # Columna de observaciones

        # Verificar que la solicitud existe
        solicitud = self.gestor.obtener_solicitud_por_id(id_solicitud)
        if not solicitud:
            messagebox.showerror("Error", "No se encontró la solicitud")
            return

        # Obtener posición y tamaño de la celda
        bbox = self.tree_solicitudes.bbox(item, column="#7")
        if not bbox:
            return

        x, y, width, height = bbox

        # Crear text widget para editar (permite texto multilinea)
        self.editando = True
        self.text_editor = tk.Text(
            self.tree_solicitudes,
            wrap=tk.WORD,
            height=3,  # Altura de 3 líneas para observaciones más largas
            width=int(width / 8),  # Aproximar caracteres basado en el ancho
        )

        # Posicionar el text widget sobre la celda
        self.text_editor.place(
            x=x, y=y, width=width, height=max(height, 60)
        )  # Mínimo 60px de altura
        self.text_editor.insert("1.0", observaciones_actuales or "")
        self.text_editor.focus_set()

        # Eventos para guardar o cancelar
        def guardar_observaciones(event=None):
            # Ctrl+Enter para guardar cuando estamos en un Text widget
            if (
                event and event.keysym == "Return" and not (event.state & 0x4)
            ):  # No Ctrl presionado
                return "break"  # Permitir nueva línea con Enter normal

            nuevas_observaciones = self.text_editor.get("1.0", "end-1c").strip()
            self.finalizar_edicion_text()

            # Actualizar observaciones en la solicitud
            if self.gestor.actualizar_estado_solicitud(
                id_solicitud,
                solicitud.estado,  # Mantener el mismo estado
                ticket_helpdesk=solicitud.ticket_helpdesk,  # Mantener ticket actual
                observaciones=nuevas_observaciones if nuevas_observaciones else None,
            ):
                messagebox.showinfo("Éxito", f"✅ Observaciones actualizadas")
                self.actualizar_lista_solicitudes()

        def cancelar_edicion_text(event=None):
            self.finalizar_edicion_text()

        # Bind eventos
        self.text_editor.bind(
            "<Control-Return>", guardar_observaciones
        )  # Ctrl+Enter para guardar
        self.text_editor.bind("<Escape>", cancelar_edicion_text)
        self.text_editor.bind("<FocusOut>", cancelar_edicion_text)

        # Agregar un label informativo
        info_label = tk.Label(
            self.tree_solicitudes,
            text="Ctrl+Enter: Guardar | Esc: Cancelar | Enter: Nueva línea",
            font=("Arial", 8),
            bg="lightyellow",
            relief="solid",
            borderwidth=1,
        )
        info_label.place(x=x, y=y - 20, width=min(width, 300))

        # Guardar referencia al label para limpiarlo después
        self.info_label = info_label

    def finalizar_edicion_text(self):
        """Finaliza la edición del text widget."""
        if hasattr(self, "text_editor") and self.text_editor:
            self.text_editor.destroy()
            self.text_editor = None
        if hasattr(self, "info_label") and self.info_label:
            self.info_label.destroy()
            self.info_label = None
        self.editando = False

    def on_solicitud_seleccionada(self, event):
        """Maneja la selección de una solicitud."""
        seleccion = self.tree_solicitudes.selection()
        if seleccion:
            item = self.tree_solicitudes.item(seleccion[0])
            id_solicitud = item["values"][0]

            self.solicitud_seleccionada = self.gestor.obtener_solicitud_por_id(
                id_solicitud
            )
            if self.solicitud_seleccionada:
                self.actualizar_info_seleccionada()

    def actualizar_info_seleccionada(self):
        """Actualiza la información de la solicitud seleccionada."""
        if not self.solicitud_seleccionada:
            self.label_info_solicitud.configure(
                text="Seleccione una solicitud para ver detalles"
            )
            return

        s = self.solicitud_seleccionada
        fecha_creacion = (
            s.fecha_creacion.split("T")[0]
            if "T" in s.fecha_creacion
            else s.fecha_creacion
        )

        info_texto = (
            f"ID: {s.id_solicitud}\n"
            f"Estado: {s.estado.value.title()}\n"
            f"Fecha: {fecha_creacion}\n"
            f"Grupos: {len(s.grupos_red)} grupo(s) de red\n"
            f"Autorizadores: {len(s.autorizadores)} persona(s)\n"
            f"Ticket: {s.ticket_helpdesk or 'Sin asignar'}"
        )

        self.label_info_solicitud.configure(text=info_texto)

    def cerrar_solicitud(self):
        """Cierra la solicitud seleccionada."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        if self.solicitud_seleccionada.estado == EstadoSolicitud.CERRADA:
            messagebox.showinfo("Información", "La solicitud ya está cerrada")
            return

        # Ventana para ingresar datos de cierre
        self.ventana_cierre_solicitud()

    def ventana_cierre_solicitud(self):
        """Abre ventana para cerrar solicitud."""
        ventana = tk.Toplevel(self)
        ventana.title("Cerrar Solicitud")
        ventana.geometry("400x300")
        ventana.transient(self)
        ventana.grab_set()

        # Título
        CTkLabel(
            ventana,
            text=f"Cerrar Solicitud: {self.solicitud_seleccionada.id_solicitud}",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        # Campo para ticket
        CTkLabel(ventana, text="Número de Ticket Helpdesk:").pack(
            anchor="w", padx=20, pady=5
        )
        entry_ticket = CTkEntry(ventana, placeholder_text="Ej: HD-2025-001234")
        entry_ticket.pack(fill="x", padx=20, pady=5)

        # Campo para observaciones
        CTkLabel(ventana, text="Observaciones:").pack(anchor="w", padx=20, pady=5)
        text_observaciones = CTkTextbox(ventana, height=100)
        text_observaciones.pack(fill="both", expand=True, padx=20, pady=5)

        # Botones
        frame_botones = CTkFrame(ventana)
        frame_botones.pack(fill="x", padx=20, pady=10)

        def confirmar_cierre():
            ticket = entry_ticket.get().strip()
            if not ticket:
                messagebox.showerror("Error", "Debe ingresar el número de ticket")
                return

            observaciones = text_observaciones.get("1.0", "end-1c").strip()

            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_seleccionada.id_solicitud,
                EstadoSolicitud.CERRADA,
                ticket,
                observaciones,
            ):
                messagebox.showinfo("Éxito", "Solicitud cerrada correctamente")
                ventana.destroy()
                self.actualizar_lista_solicitudes()
                self.solicitud_seleccionada = None
                self.actualizar_info_seleccionada()
            else:
                messagebox.showerror("Error", "No se pudo cerrar la solicitud")

        CTkButton(
            frame_botones, text="✅ Cerrar Solicitud", command=confirmar_cierre
        ).pack(side="left", padx=5)
        CTkButton(frame_botones, text="❌ Cancelar", command=ventana.destroy).pack(
            side="right", padx=5
        )

    def marcar_en_proceso(self):
        """Marca la solicitud como en proceso."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        if self.gestor.actualizar_estado_solicitud(
            self.solicitud_seleccionada.id_solicitud,
            EstadoSolicitud.EN_PROCESO,
            observaciones="Marcada como en proceso",
        ):
            messagebox.showinfo("Éxito", "Solicitud marcada como en proceso")
            self.actualizar_lista_solicitudes()
            self.actualizar_info_seleccionada()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado")

    def reabrir_solicitud(self):
        """Reabre una solicitud cerrada."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        if self.solicitud_seleccionada.estado != EstadoSolicitud.CERRADA:
            messagebox.showinfo(
                "Información", "Solo se pueden reabrir solicitudes cerradas"
            )
            return

        motivo = tk.simpledialog.askstring(
            "Reabrir Solicitud", "Motivo para reabrir la solicitud:"
        )
        if motivo:
            if self.gestor.actualizar_estado_solicitud(
                self.solicitud_seleccionada.id_solicitud,
                EstadoSolicitud.ABIERTA,
                observaciones=f"Reabierta: {motivo}",
            ):
                messagebox.showinfo("Éxito", "Solicitud reabierta correctamente")
                self.actualizar_lista_solicitudes()
                self.actualizar_info_seleccionada()
            else:
                messagebox.showerror("Error", "No se pudo reabrir la solicitud")

    def ver_detalles_solicitud(self, event=None):
        """Muestra los detalles completos de la solicitud usando la interfaz visual de creación."""
        if not self.solicitud_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una solicitud primero")
            return

        # Ventana de detalles
        ventana = tk.Toplevel(self)
        ventana.title(f"Detalles - {self.solicitud_seleccionada.id_solicitud}")
        ventana.geometry("1000x800")  # Aumentado de 800x600 a 1000x800
        ventana.transient(self)
        ventana.grab_set()  # Modal

        # Crear el frame de detalles con la misma estructura visual
        detalle_frame = DetallesSolicitudFrame(ventana, self.solicitud_seleccionada)
        detalle_frame.pack(fill="both", expand=True, padx=10, pady=10)


class DetallesSolicitudFrame(CTkFrame):
    """Frame para mostrar detalles de solicitud usando la misma interfaz visual de creación."""

    def __init__(self, master, solicitud: SolicitudConformidad):
        """Inicializa el frame de detalles.

        Args:
            master: Widget padre
            solicitud: Solicitud a mostrar
        """
        super().__init__(master)
        self.solicitud = solicitud
        self.setup_ui()
        self.cargar_datos()

    def setup_ui(self):
        """Configura la interfaz visual similar a la de creación."""
        # Título
        titulo = CTkLabel(
            self,
            text=f"📋 Detalles de Solicitud: {self.solicitud.id_solicitud}",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

        # Frame de información general
        frame_info = CTkFrame(self)
        frame_info.pack(fill="x", padx=10, pady=5)

        CTkLabel(
            frame_info, text="📊 Información General", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Grid para información básica
        info_grid = CTkFrame(frame_info)
        info_grid.pack(fill="x", padx=10, pady=5)

        # Estado
        CTkLabel(info_grid, text="Estado:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        estado_label = CTkLabel(info_grid, text=self.solicitud.estado.value.title())
        estado_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Fecha de creación
        CTkLabel(info_grid, text="Fecha de Creación:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        fecha_str = (
            self.solicitud.fecha_creacion.split("T")[0]
            if "T" in self.solicitud.fecha_creacion
            else self.solicitud.fecha_creacion
        )
        CTkLabel(info_grid, text=fecha_str).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )

        # Ticket
        CTkLabel(info_grid, text="Ticket Helpdesk:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        CTkLabel(info_grid, text=self.solicitud.ticket_helpdesk or "Sin asignar").grid(
            row=2, column=1, sticky="w", padx=5, pady=2
        )

        # Frame para matrices (simuladas - solo visual)
        self.frame_matrices = CTkFrame(self)
        self.frame_matrices.pack(fill="x", padx=10, pady=10)
        CTkLabel(
            self.frame_matrices,
            text="📑 Matrices de Rol Solicitadas",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Frame para grupos de red
        self.frame_grupos = CTkFrame(self)
        self.frame_grupos.pack(fill="both", expand=True, padx=10, pady=10)
        CTkLabel(
            self.frame_grupos, text="🌐 Grupos de Red", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # Textbox para mostrar grupos (solo lectura)
        self.txt_grupos = CTkTextbox(self.frame_grupos, height=100)
        self.txt_grupos.pack(fill="x", padx=10, pady=5)

        # Frame para autorizadores
        self.frame_autorizadores = CTkFrame(self)
        self.frame_autorizadores.pack(fill="both", expand=True, padx=10, pady=10)
        CTkLabel(
            self.frame_autorizadores,
            text="👥 Autorizadores Asignados",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Tabla de autorizadores
        self.crear_tabla_autorizadores()

        # Frame para observaciones
        self.frame_observaciones = CTkFrame(self)
        self.frame_observaciones.pack(fill="x", padx=10, pady=10)
        CTkLabel(
            self.frame_observaciones,
            text="📝 Observaciones",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        # Textbox para observaciones (solo lectura)
        self.txt_observaciones = CTkTextbox(self.frame_observaciones, height=60)
        self.txt_observaciones.pack(fill="x", padx=10, pady=5)

        # Botón de cerrar
        CTkButton(self, text="✅ Cerrar", command=self.master.destroy).pack(pady=10)

    def crear_tabla_autorizadores(self):
        """Crea la tabla de autorizadores."""
        # Frame para la tabla
        tabla_frame = CTkFrame(self.frame_autorizadores)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear treeview para autorizadores
        columnas = ("Código", "Autorizador", "Correo")
        self.tree_autorizadores = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=6
        )

        # Configurar encabezados
        self.tree_autorizadores.heading("Código", text="Código App")
        self.tree_autorizadores.heading("Autorizador", text="Nombre Autorizador")
        self.tree_autorizadores.heading("Correo", text="Correo Electrónico")

        # Configurar anchos
        self.tree_autorizadores.column("Código", width=100)
        self.tree_autorizadores.column("Autorizador", width=200)
        self.tree_autorizadores.column("Correo", width=250)

        # Scrollbar
        scrollbar_auth = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tree_autorizadores.yview
        )
        self.tree_autorizadores.configure(yscrollcommand=scrollbar_auth.set)

        # Pack
        self.tree_autorizadores.pack(side="left", fill="both", expand=True)
        scrollbar_auth.pack(side="right", fill="y")

    def cargar_datos(self):
        """Carga los datos de la solicitud en la interfaz."""
        # Cargar grupos de red
        grupos_texto = "\n".join(self.solicitud.grupos_red)
        self.txt_grupos.insert("1.0", grupos_texto)
        self.txt_grupos.configure(state="disabled")  # Solo lectura

        # Cargar autorizadores en la tabla
        for auth in self.solicitud.autorizadores:
            codigo = auth.get("codigo", "N/A")
            nombre = auth.get("autorizador", "N/A")
            correo = auth.get("correo", "N/A")
            self.tree_autorizadores.insert("", "end", values=(codigo, nombre, correo))

        # Cargar observaciones
        observaciones = self.solicitud.observaciones or "Sin observaciones"
        self.txt_observaciones.insert("1.0", observaciones)
        self.txt_observaciones.configure(state="disabled")  # Solo lectura

        # Agregar indicación visual de matrices (simulado)
        matriz_info = CTkLabel(
            self.frame_matrices,
            text=f"✅ Matrices procesadas para {len(self.solicitud.grupos_red)} grupos de red",
            font=("Arial", 10),
        )
        matriz_info.pack(anchor="w", padx=10, pady=2)

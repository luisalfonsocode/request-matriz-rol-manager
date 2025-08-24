"""Editor de autorizadores con grilla editable."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
from customtkinter import CTkFrame, CTkButton
from ..data import GestorPersistencia
from ..data.gestor_autorizadores import GestorAutorizadores
from ..email.generador_correos_individuales import GeneradorCorreosIndividuales
import os


class AutorizadoresEditorFrame(CTkFrame):
    """Frame para editar autorizadores en formato de grilla.

    Permite editar códigos de aplicación, autorizadores y correos
    en una tabla editable similar a Excel.
    """

    def __init__(
        self,
        master,
        codigos_aplicacion: List[str],
        grupos_red: Optional[List[str]] = None,
    ):
        """Inicializa el editor de autorizadores.

        Args:
            master: Widget padre
            codigos_aplicacion: Lista de códigos de aplicación extraídos
            grupos_red: Lista de grupos de red seleccionados (opcional)
        """
        super().__init__(master)
        self.codigos_aplicacion = codigos_aplicacion
        self.grupos_red = grupos_red or []
        self.datos_autorizadores = []
        self.gestor_persistencia = GestorPersistencia()
        self.gestor_autorizadores = GestorAutorizadores()  # Nueva BD de autorizadores

        # Callback para cuando se guardan los datos
        self.callback_guardado = None

        # Variable para edición en línea
        self.editing_item = None
        self.editing_column = None

        self.setup_ui()
        self.cargar_datos_iniciales()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Título
        titulo = ttk.Label(
            self, text="Gestión de Autorizadores", font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        # Instrucciones
        instrucciones = ttk.Label(
            self,
            text="INSTRUCCIONES:\n"
            "• Haga doble clic en las celdas de 'Autorizador' y 'Correo' para editarlas\n"
            "• Presione Enter para guardar los cambios o Escape para cancelar\n"
            "• Los datos se guardan automáticamente al editarlos\n"
            "• Al abrir la aplicación nuevamente, los datos previos se cargarán automáticamente\n"
            "• Los códigos de aplicación no se pueden editar",
            font=("Arial", 9),
            foreground="blue",
            justify="left",
        )
        instrucciones.pack(pady=5)

        # Frame para la tabla
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Crear Treeview con scrollbars
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("codigo", "autorizador", "correo"),
            show="headings",
            height=15,
        )

        # Configurar columnas
        self.tree.heading("codigo", text="Código de Aplicación")
        self.tree.heading("autorizador", text="Autorizador")
        self.tree.heading("correo", text="Correo del Autorizador")

        self.tree.column("codigo", width=200, anchor="center")
        self.tree.column("autorizador", width=250, anchor="w")
        self.tree.column("correo", width=300, anchor="w")

        # Configurar tags para resaltado visual
        self.tree.tag_configure("error", background="#ffcccc", foreground="#000000")
        self.tree.tag_configure("normal", background="#ffffff", foreground="#000000")
        self.tree.tag_configure("readonly", background="#f0f0f0", foreground="#000000")

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(
            frame_tabla, orient="vertical", command=self.tree.yview
        )
        scrollbar_h = ttk.Scrollbar(
            frame_tabla, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set
        )

        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Configurar grid
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Bind para edición
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.on_enter_key)
        self.tree.bind("<Button-1>", self.on_single_click)

        # Frame para botón
        frame_boton = ttk.Frame(self)
        frame_boton.pack(pady=20)

        # Botón principal de continuar
        CTkButton(
            frame_boton,
            text="Guardar y Continuar",
            command=self.guardar_continuar,
            width=200,
            height=40,
            font=("Arial", 12, "bold"),
        ).pack()

        # Variable para edición en línea
        self.editing_item = None
        self.editing_column = None

    def cargar_datos_iniciales(self):
        """Carga los códigos de aplicación usando la BD central de autorizadores."""
        print(f"🔄 Cargando autorizadores para códigos: {self.codigos_aplicacion}")

        for codigo in self.codigos_aplicacion:
            # Buscar en la BD central de autorizadores
            autorizador_bd = self.gestor_autorizadores.obtener_autorizador_por_codigo(
                codigo
            )

            if autorizador_bd:
                # Usar datos de la BD central
                autorizador = autorizador_bd.get("autorizador", "")
                correo = autorizador_bd.get("correo", "")
                print(f"✅ Autorizador encontrado en BD: {codigo} -> {autorizador}")
            else:
                # Fallback a datos guardados localmente
                datos_guardados = self.gestor_persistencia.cargar_autorizadores()
                datos_previos = datos_guardados.get(codigo, {})
                autorizador = datos_previos.get("autorizador", "")
                correo = datos_previos.get("correo", "")
                print(
                    f"⚠️ Autorizador no encontrado en BD central, usando datos locales: {codigo}"
                )

            # Determinar el tag inicial basado en si tiene datos completos
            tag_inicial = (
                ("normal",)
                if (autorizador and correo and "@" in correo)
                else ("error",)
            )

            item_id = self.tree.insert(
                "", "end", values=(codigo, autorizador, correo), tags=tag_inicial
            )
            self.datos_autorizadores.append(
                {
                    "codigo": codigo,
                    "autorizador": autorizador,
                    "correo": correo,
                    "item_id": item_id,
                }
            )

    def actualizar_resaltado_celda(self, item):
        """Actualiza el resaltado visual de una fila según si está completa."""
        values = self.tree.item(item, "values")
        autorizador = values[1] if len(values) > 1 else ""
        correo = values[2] if len(values) > 2 else ""

        # Verificar si todos los campos están completos y válidos
        autorizador_completo = autorizador.strip() != ""
        correo_completo = correo.strip() != "" and "@" in correo.strip()

        # Si ambos campos están completos, usar tag normal (sin rojo)
        if autorizador_completo and correo_completo:
            self.tree.item(item, tags=("normal",))
        else:
            # Si faltan campos, usar tag de error (rojo)
            self.tree.item(item, tags=("error",))

    def on_double_click(self, event):
        """Maneja el doble clic para editar celdas."""
        # Identificar el item que fue clickeado
        item = self.tree.identify_row(event.y)
        if not item:
            return

        # Determinar columna
        column = self.tree.identify_column(event.x)
        if not column:
            return

        column_index = int(column.replace("#", "")) - 1
        if column_index < 0 or column_index >= len(self.tree["columns"]):
            return

        column_name = self.tree["columns"][column_index]

        # No permitir editar el código de aplicación
        if column_name == "codigo":
            messagebox.showinfo(
                "Información", "El código de aplicación no se puede editar."
            )
            return

        self.editar_celda(item, column_name)

    def on_enter_key(self, event):
        """Maneja la tecla Enter para iniciar edición."""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            # Editar la primera columna editable (autorizador)
            self.editar_celda(item, "autorizador")

    def on_single_click(self, event):
        """Maneja el clic simple para seleccionar filas."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tree.focus(item)

    def editar_celda(self, item, column):
        """Abre un editor en línea para la celda."""
        try:
            # Obtener la posición de la celda
            bbox = self.tree.bbox(item, column)
            if not bbox:
                return

            x, y, width, height = bbox

            # Obtener valor actual
            values = self.tree.item(item, "values")
            column_index = self.tree["columns"].index(column)
            current_value = values[column_index] if column_index < len(values) else ""

            # Crear entry para edición
            entry = tk.Entry(self.tree, font=("Arial", 10))
            entry.insert(0, current_value)
            entry.select_range(0, tk.END)
            entry.place(x=x, y=y, width=width, height=height)
            entry.focus()

            def save_edit(event=None):
                new_value = entry.get()
                entry.destroy()
                self.actualizar_valor(item, column, new_value)

            def cancel_edit(event=None):
                entry.destroy()

            entry.bind("<Return>", save_edit)
            entry.bind("<Escape>", cancel_edit)
            entry.bind("<FocusOut>", save_edit)

        except Exception as e:
            print(f"Error al editar celda: {e}")
            messagebox.showerror("Error", f"No se pudo editar la celda: {str(e)}")

    def actualizar_valor(self, item, column, new_value):
        """Actualiza el valor en la tabla y en los datos."""
        # Actualizar en el tree
        values = list(self.tree.item(item, "values"))
        column_index = self.tree["columns"].index(column)
        values[column_index] = new_value
        self.tree.item(item, values=values)

        # Actualizar en datos internos
        for dato in self.datos_autorizadores:
            if dato["item_id"] == item:
                dato[column] = new_value

                # Guardar automáticamente los cambios en el archivo
                self.gestor_persistencia.actualizar_autorizador(
                    dato["codigo"], dato["autorizador"], dato["correo"]
                )
                break

        # Actualizar resaltado visual de la fila
        self.actualizar_resaltado_celda(item)

    def guardar_continuar(self):
        """Valida y guarda los datos."""
        campos_incompletos = False

        # Actualizar el resaltado de todas las filas y verificar si hay campos incompletos
        for dato in self.datos_autorizadores:
            item_id = dato["item_id"]
            self.actualizar_resaltado_celda(item_id)

            # Verificar si hay campos incompletos
            autorizador_completo = dato["autorizador"].strip() != ""
            correo_completo = dato["correo"].strip() != "" and "@" in dato["correo"]

            if not autorizador_completo or not correo_completo:
                campos_incompletos = True

        if campos_incompletos:
            messagebox.showwarning(
                "Campos Incompletos",
                "Complete todos los campos resaltados en rojo.\n\n"
                "• Las celdas en rojo indican campos requeridos\n"
                "• Todos los autorizadores deben tener nombre y correo válido",
            )
            return

        # Mostrar resumen y confirmar
        resumen = "RESUMEN DE AUTORIZADORES\n\n"
        for dato in self.datos_autorizadores:
            resumen += f"Código: {dato['codigo']}\n"
            resumen += f"Autorizador: {dato['autorizador']}\n"
            resumen += f"Correo: {dato['correo']}\n\n"

        if messagebox.askyesno(
            "Confirmar", f"{resumen}¿Desea continuar con estos datos?"
        ):
            try:
                # Guardar datos en persistencia
                self.gestor_persistencia.guardar_autorizadores(self.datos_autorizadores)

                # Llamar al callback si existe (para crear solicitud)
                print(
                    f"🔍 DEBUG: callback_guardado definido: {self.callback_guardado is not None}"
                )
                print(f"🔍 DEBUG: callback_guardado valor: {self.callback_guardado}")
                if self.callback_guardado:
                    print("🔔 DEBUG: Ejecutando callback_guardado...")
                    self.callback_guardado(self.datos_autorizadores)
                    print("✅ DEBUG: Callback ejecutado completamente")
                else:
                    print("❌ DEBUG: callback_guardado no está definido!")

                # Generar archivos de correo individuales
                generador = GeneradorCorreosIndividuales()
                archivos_correos = generador.generar_correos_individuales(
                    self.datos_autorizadores, self.grupos_red
                )

                # Mostrar mensaje de éxito con la cantidad de archivos generados
                mensaje_exito = (
                    "✅ Datos guardados correctamente.\n\n"
                    f"📧 {len(archivos_correos)} correos individuales generados\n"
                    f"📁 Ubicación: {generador.directorio_salida}\n\n"
                    "🔔 Los archivos están listos para revisar y enviar desde Outlook."
                )
                messagebox.showinfo("Éxito", mensaje_exito)

                # Abrir la carpeta donde se guardaron los correos
                os.startfile(str(generador.directorio_salida))

            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el correo: {str(e)}")

            # Cerrar ventana
            self.master.destroy()

"""
Aplicación principal con pestañas para la gestión completa de matrices de rol.

Incluye:
1. Solicitud de nuevas matrices (pestaña 1)
2. Editor de autorizadores (pestaña 2)
3. Gestión de solicitudes (pestaña 3)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from .solicitud_matriz import SolicitudMatrizFrame
from .autorizadores_editor import AutorizadoresEditorFrame
from .gestion_solicitudes import GestionSolicitudesFrame
from ..data.gestor_solicitudes import GestorSolicitudes


class AplicacionMatrizRol(ctk.CTk):
    """Aplicación principal con sistema de pestañas."""

    def __init__(self):
        """Inicializa la aplicación principal."""
        super().__init__()

        # Configuración de la ventana
        self.title("🔐 Sistema de Gestión de Matrices de Rol")
        self.geometry("1000x700")

        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Inicializar gestor de solicitudes
        self.gestor_solicitudes = GestorSolicitudes()

        # Variables compartidas
        self.grupos_red_actuales = []
        self.datos_autorizadores_actuales = []

        # Grupos predefinidos del sistema original
        self.grupos_predefinidos = ["APF2_QASD1_SSSS_CASD1_", "FCVE2_ATLA_FIEC_CASD1_"]

        self.configurar_interfaz()

    def configurar_interfaz(self):
        """Configura la interfaz con pestañas."""
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña 1: Solicitud de Matriz
        self.frame_solicitud = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.frame_solicitud, text="📝 Nueva Solicitud")

        # Pestaña 2: Editor de Autorizadores - OCULTA (no se usa)
        # self.frame_autorizadores = ctk.CTkFrame(self.notebook)
        # self.notebook.add(self.frame_autorizadores, text="👥 Editar Autorizadores")

        # Pestaña 3: Gestión de Solicitudes (ahora será la pestaña 2)
        self.frame_gestion = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.frame_gestion, text="📋 Gestión de Solicitudes")

        self.configurar_pestana_solicitud()
        # self.configurar_pestana_autorizadores()  # No se usa
        self.configurar_pestana_gestion()

        # Eventos para actualizar datos entre pestañas
        self.notebook.bind("<<NotebookTabChanged>>", self.on_cambio_pestana)

    def configurar_pestana_solicitud(self):
        """Configura la primera pestaña de solicitud."""
        # Usar el frame original de solicitud
        print(
            f"🔄 DEBUG: Creando SolicitudMatrizFrame con callback: {self.on_autorizadores_guardados}"
        )
        self.solicitud_frame = SolicitudMatrizFrame(
            self.frame_solicitud, callback_autorizadores=self.on_autorizadores_guardados
        )
        self.solicitud_frame.pack(fill="both", expand=True)

        # Conectar el callback para cuando se confirme la selección
        self.solicitud_frame.callback_confirmacion = self.on_solicitud_confirmada

    def configurar_pestana_autorizadores(self):
        """Configura la segunda pestaña de autorizadores - DESHABILITADA."""
        # Esta pestaña ha sido ocultada ya que no se usa
        # El editor de autorizadores se maneja desde la pestaña de solicitud
        pass

    def configurar_pestana_gestion(self):
        """Configura la tercera pestaña de gestión."""
        # Crear el frame de gestión de solicitudes pasando el gestor compartido
        self.gestion_solicitudes = GestionSolicitudesFrame(
            self.frame_gestion, self.gestor_solicitudes
        )
        self.gestion_solicitudes.pack(fill="both", expand=True)

    def ir_a_autorizadores(self):
        """Cambia a la pestaña de autorizadores y configura los datos."""
        # Extraer códigos de aplicación de los grupos
        codigos = self.extraer_codigos_aplicacion()

        if not codigos:
            messagebox.showerror(
                "Error", "No se pudieron extraer códigos de aplicación"
            )
            return

        # Configurar el editor de autorizadores
        self.configurar_editor_autorizadores(codigos)

        # No cambiar a pestaña de autorizadores (está oculta)
        # self.notebook.select(1)

    def on_solicitud_confirmada(self, matrices_seleccionadas, grupos_red):
        """Maneja la confirmación de la solicitud desde el primer tab."""
        # Actualizar las variables compartidas
        self.grupos_red_actuales = grupos_red

        # Extraer códigos de aplicación
        codigos = self.extraer_codigos_aplicacion_de_grupos(grupos_red)

        if codigos:
            # Configurar el editor de autorizadores
            self.configurar_editor_autorizadores(codigos)
            # No cambiar a pestaña de autorizadores (está oculta)
            # self.notebook.select(1)
        else:
            messagebox.showerror(
                "Error", "No se pudieron extraer códigos de aplicación de los grupos"
            )

    def extraer_codigos_aplicacion_de_grupos(self, grupos_red):
        """Extrae códigos de aplicación de una lista de grupos específica."""
        codigos = set()

        for grupo in grupos_red:
            # Buscar patrones de aplicación: _XXXX_ (rodeado de guiones bajos)
            import re

            # Buscar códigos de 4 letras rodeados por guiones bajos
            patron = r"_([A-Z]{4})_"
            matches = re.findall(patron, grupo)
            for match in matches:
                codigos.add(match)

        return sorted(list(codigos))

    def extraer_codigos_aplicacion(self):
        """Extrae códigos de aplicación únicos de los grupos de red."""
        codigos = set()

        for grupo in self.grupos_predefinidos:
            # Dividir por guiones bajos y tomar elementos de 4 caracteres
            partes = grupo.split("_")
            for parte in partes:
                if len(parte) == 4 and parte.isalpha():
                    codigos.add(parte)

        return sorted(list(codigos))

    def configurar_editor_autorizadores(self, codigos_aplicacion):
        """Configura el editor de autorizadores con los códigos extraídos - ADAPTADO."""
        print(
            f"🔄 DEBUG: configurar_editor_autorizadores llamado con {len(codigos_aplicacion)} códigos"
        )

        # La pestaña de autorizadores ha sido removida, pero mantenemos la lógica
        # para crear el editor cuando se necesite desde la solicitud

        # Nota: El editor se crea dinámicamente desde solicitud_matriz.py
        # Este método ahora solo mantiene la compatibilidad
        self.editor_autorizadores = None

        print(f"🔗 DEBUG: Configuración adaptada - editor será creado dinámicamente")

    def on_autorizadores_guardados(self, datos_autorizadores):
        """Maneja el evento cuando se guardan los autorizadores."""
        print("\n🔔 CALLBACK: on_autorizadores_guardados ejecutándose...")
        print(f"📊 Datos autorizadores recibidos: {len(datos_autorizadores)} elementos")

        # Crear la solicitud en el gestor
        try:
            # Obtener grupos actuales del editor en lugar de usar predefinidos
            grupos_actuales = []
            if hasattr(self, "editor_autorizadores") and hasattr(
                self.editor_autorizadores, "grupos_red"
            ):
                grupos_actuales = self.editor_autorizadores.grupos_red
                print(f"📂 Grupos del editor: {grupos_actuales}")
            else:
                # Fallback a grupos predefinidos
                grupos_actuales = self.grupos_predefinidos
                print(f"📂 Usando grupos predefinidos: {grupos_actuales}")

            # Verificar que tenemos grupos
            if not grupos_actuales:
                print("❌ Error: No hay grupos de red definidos")
                messagebox.showerror(
                    "Error",
                    "No se han definido grupos de red. Por favor, configure los grupos primero.",
                )
                return

            print("🔧 Creando solicitud en el gestor...")
            solicitud = self.gestor_solicitudes.crear_solicitud(
                grupos_actuales, datos_autorizadores
            )
            print(f"✅ Solicitud creada: {solicitud.id_solicitud}")

            # Forzar guardado y recarga
            print("💾 Guardando solicitudes...")
            self.gestor_solicitudes.guardar_solicitudes()
            print("✅ Solicitudes guardadas")

            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Solicitud Creada",
                f"✅ Solicitud creada exitosamente!\n\n"
                f"ID: {solicitud.id_solicitud}\n"
                f"Estado: {solicitud.estado.value.title()}\n\n"
                f"Puede hacer seguimiento en la pestaña 'Gestión de Solicitudes'",
            )

            # Forzar actualización de la pestaña de gestión en el siguiente ciclo
            if hasattr(self, "gestion_solicitudes"):
                print("🔄 Programando actualización de gestión tras crear solicitud...")
                # Usar after() para asegurar que la actualización se ejecute
                # después de que todo el guardado esté completo
                self.after(100, self._actualizar_gestion_tras_crear_solicitud)
            else:
                print("⚠️ Warning: gestion_solicitudes no está disponible")

        except Exception as e:
            print(f"❌ Error en callback: {e}")
            import traceback

            traceback.print_exc()
            messagebox.showerror("Error", f"Error creando solicitud: {e}")

    def _actualizar_gestion_tras_crear_solicitud(self):
        """Actualiza la gestión de solicitudes después de crear una nueva."""
        try:
            print("🔄 Ejecutando actualización diferida de gestión...")
            # Forzar recarga completa
            self.gestor_solicitudes.cargar_solicitudes()
            # Actualizar la interfaz
            self.gestion_solicitudes.actualizar_lista_solicitudes()
            print("✅ Actualización de gestión completada")
        except Exception as e:
            print(f"❌ Error en actualización diferida: {e}")

    def on_cambio_pestana(self, event):
        """Maneja el cambio entre pestañas."""
        pestaña_seleccionada = self.notebook.index(self.notebook.select())

        # Si cambia a gestión de solicitudes (ahora es índice 1), forzar actualización
        if pestaña_seleccionada == 1 and hasattr(self, "gestion_solicitudes"):
            print("🔄 Cambio a pestaña de Gestión - Programando actualización...")
            # Usar after() para asegurar que la actualización se ejecute
            # en el siguiente ciclo del event loop
            self.after(50, self._actualizar_gestion_por_cambio_pestana)

    def _actualizar_gestion_por_cambio_pestana(self):
        """Actualiza la gestión cuando se cambia a la pestaña."""
        try:
            print("🔄 Ejecutando actualización por cambio de pestaña...")
            # Forzar recarga del gestor desde archivo
            self.gestor_solicitudes.cargar_solicitudes()
            # Actualizar la interfaz
            self.gestion_solicitudes.actualizar_lista_solicitudes()
            print("✅ Actualización por cambio de pestaña completada")
        except Exception as e:
            print(f"❌ Error en actualización por cambio de pestaña: {e}")


def main():
    """Función principal para ejecutar la aplicación."""
    app = AplicacionMatrizRol()
    app.mainloop()


if __name__ == "__main__":
    main()

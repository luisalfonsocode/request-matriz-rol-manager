"""
Módulo para generar correos MSG individuales de solicitud de conformidad.

Este módulo crea archivos .msg de Outlook separados para cada autorizador
con la solicitud de conformidad personalizada.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import win32com.client
    import pythoncom

    OUTLOOK_DISPONIBLE = True
except ImportError:
    OUTLOOK_DISPONIBLE = False
    print(
        "⚠️ Advertencia: pywin32 no está disponible. Se crearán archivos EML en lugar de MSG."
    )


class GeneradorCorreosIndividuales:
    """Generador de correos MSG individuales para cada autorizador."""

    def __init__(self):
        """Inicializa el generador de correos individuales."""
        # Buscar la raíz del proyecto (donde está ejecutar_app.py)
        current_path = Path(__file__).resolve()
        while current_path.parent != current_path:
            if (current_path / "ejecutar_app.py").exists():
                break
            current_path = current_path.parent

        self.directorio_salida = current_path / "output" / "correos_individuales"
        self.directorio_salida.mkdir(parents=True, exist_ok=True)

    def generar_correos_individuales(
        self, datos_autorizadores: List[Dict[str, str]], grupos_red: List[str]
    ) -> List[str]:
        """
        Genera un archivo MSG separado para cada autorizador.

        Args:
            datos_autorizadores: Lista con datos de autorizadores
            grupos_red: Lista de grupos de red seleccionados

        Returns:
            Lista de rutas de archivos MSG generados
        """
        archivos_generados = []
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M")

        # Crear carpeta específica para esta solicitud
        carpeta_solicitud = self._crear_carpeta_solicitud(fecha_archivo, grupos_red)

        print(
            f"📧 Generando correos individuales para {len(datos_autorizadores)} autorizadores..."
        )
        print(f"📁 Carpeta de solicitud: {carpeta_solicitud}")

        for i, autorizador in enumerate(datos_autorizadores, 1):
            if autorizador.get("autorizador") and autorizador.get("correo"):
                try:
                    archivo_path = self._crear_correo_individual(
                        autorizador,
                        datos_autorizadores,
                        grupos_red,
                        fecha_actual,
                        fecha_archivo,
                        i,
                        carpeta_solicitud,
                    )
                    archivos_generados.append(archivo_path)
                    print(
                        f"✅ {i}/{len(datos_autorizadores)} - Correo para {autorizador['autorizador']}"
                    )
                except Exception as e:
                    print(
                        f"❌ Error generando correo para {autorizador['autorizador']}: {e}"
                    )

        # Crear archivo resumen de la solicitud
        self._crear_resumen_solicitud(
            carpeta_solicitud, datos_autorizadores, grupos_red, fecha_actual
        )

        print(f"\n📁 Correos generados en: {carpeta_solicitud}")
        print(f"📊 Total exitosos: {len(archivos_generados)}")

        return archivos_generados

    def _crear_correo_individual(
        self,
        autorizador_principal: Dict[str, str],
        todos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha_actual: str,
        fecha_archivo: str,
        numero: int,
        carpeta_solicitud: Path,
    ) -> str:
        """Crea un archivo MSG individual para un autorizador específico."""

        # Generar contenido personalizado para este autorizador
        contenido_html = self._generar_contenido_html_individual(
            autorizador_principal, todos_autorizadores, grupos_red, fecha_actual
        )
        contenido_texto = self._generar_contenido_texto_individual(
            autorizador_principal, todos_autorizadores, grupos_red, fecha_actual
        )

        # Nombre del archivo
        nombre_limpio = self._limpiar_nombre_archivo(
            autorizador_principal["autorizador"]
        )
        codigo = autorizador_principal["codigo"]
        archivo_nombre = (
            f"{numero:02d}_Conformidad_{codigo}_{nombre_limpio}_{fecha_archivo}.msg"
        )
        archivo_path = carpeta_solicitud / archivo_nombre

        if OUTLOOK_DISPONIBLE:
            self._crear_archivo_msg_outlook(
                archivo_path, autorizador_principal, contenido_html, contenido_texto
            )
        else:
            # Crear archivo EML como alternativa
            archivo_eml = archivo_path.with_suffix(".eml")
            self._crear_archivo_eml_individual(
                archivo_eml, autorizador_principal, contenido_html, contenido_texto
            )
            archivo_path = archivo_eml

        return str(archivo_path)

    def _crear_carpeta_solicitud(
        self, fecha_archivo: str, grupos_red: List[str]
    ) -> Path:
        """Crea una carpeta específica para esta solicitud."""
        # Generar nombre de carpeta único
        timestamp = fecha_archivo
        grupos_cortos = "_".join(
            [g[:4] for g in grupos_red[:2]]
        )  # Primeros 4 chars de primeros 2 grupos

        nombre_carpeta = f"Solicitud_{timestamp}_{grupos_cortos}"
        carpeta_solicitud = self.directorio_salida / nombre_carpeta

        # Crear la carpeta
        carpeta_solicitud.mkdir(parents=True, exist_ok=True)

        return carpeta_solicitud

    def _crear_resumen_solicitud(
        self,
        carpeta_solicitud: Path,
        datos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha_actual: str,
    ):
        """Crea un archivo resumen de la solicitud."""
        resumen_path = carpeta_solicitud / "RESUMEN_SOLICITUD.txt"

        contenido_resumen = f"""RESUMEN DE SOLICITUD DE CONFORMIDAD
=====================================

📅 Fecha de Generación: {fecha_actual}
📁 Carpeta: {carpeta_solicitud.name}

🌐 GRUPOS DE RED SOLICITADOS ({len(grupos_red)}):
{chr(10).join(f"  • {grupo}" for grupo in grupos_red)}

👥 AUTORIZADORES ({len(datos_autorizadores)}):
{chr(10).join(f"  • {auth['codigo']} - {auth['autorizador']} ({auth['correo']})" for auth in datos_autorizadores)}

📧 ARCHIVOS GENERADOS:
{chr(10).join(f"  • {i:02d}_Conformidad_{auth['codigo']}_{self._limpiar_nombre_archivo(auth['autorizador'])}_{carpeta_solicitud.name.split('_')[1]}.msg" for i, auth in enumerate(datos_autorizadores, 1))}

📋 INSTRUCCIONES:
1. Revisar cada archivo MSG individual
2. Abrir desde Outlook para enviar
3. Hacer seguimiento de respuestas
4. Actualizar estado en el sistema de gestión

---
Generado automáticamente por el Sistema de Gestión de Matriz de Roles
"""

        try:
            with open(resumen_path, "w", encoding="utf-8") as file:
                file.write(contenido_resumen)
            print(f"📄 Resumen creado: {resumen_path.name}")
        except Exception as e:
            print(f"⚠️ Error creando resumen: {e}")

    def _crear_archivo_msg_outlook(
        self,
        archivo_path: Path,
        autorizador: Dict[str, str],
        contenido_html: str,
        contenido_texto: str,
    ):
        """Crea un archivo MSG usando Outlook COM."""
        try:
            # Inicializar COM
            pythoncom.CoInitialize()

            # Crear aplicación Outlook
            outlook = win32com.client.Dispatch("Outlook.Application")

            # Crear nuevo elemento de correo
            mail = outlook.CreateItem(0)  # 0 = olMailItem

            # Configurar correo con código de aplicación en el asunto
            mail.To = f"{autorizador['autorizador']} <{autorizador['correo']}>"
            mail.Subject = f"🔐 Solicitud de Conformidad [{autorizador['codigo']}] - Matriz de Roles - ACCIÓN REQUERIDA"
            mail.HTMLBody = contenido_html
            mail.Body = contenido_texto

            # Guardar como archivo MSG
            mail.SaveAs(str(archivo_path), 3)  # 3 = olMSG

            print(f"📧 Archivo MSG creado: {archivo_path.name}")

        except Exception as e:
            print(f"❌ Error creando MSG: {e}")
            # Crear EML como fallback
            archivo_eml = archivo_path.with_suffix(".eml")
            self._crear_archivo_eml_individual(
                archivo_eml, autorizador, contenido_html, contenido_texto
            )
        finally:
            try:
                pythoncom.CoUninitialize()
            except:
                pass

    def _crear_archivo_eml_individual(
        self,
        archivo_path: Path,
        autorizador: Dict[str, str],
        contenido_html: str,
        contenido_texto: str,
    ):
        """Crea un archivo EML como alternativa al MSG."""

        # Codificar asunto con código de aplicación
        asunto_codificado = f"🔐 Solicitud de Conformidad [{autorizador['codigo']}] - Matriz de Roles - ACCIÓN REQUERIDA"

        eml_content = f"""From: Gestión de Accesos <gestion.accesos@empresa.com>
To: {autorizador['autorizador']} <{autorizador['correo']}>
Subject: {asunto_codificado}
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit

{contenido_texto}

--boundary123
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: 8bit

{contenido_html}

--boundary123--
"""

        with open(archivo_path, "w", encoding="utf-8") as file:
            file.write(eml_content)

        print(f"📧 Archivo EML creado: {archivo_path.name}")

    def _limpiar_nombre_archivo(self, nombre: str) -> str:
        """Limpia el nombre para usarlo en archivo."""
        # Tomar solo los primeros nombres/apellidos
        palabras = nombre.split()[:2]  # Máximo 2 palabras
        nombre_limpio = "_".join(palabras)

        # Eliminar caracteres especiales
        caracteres_invalidos = '<>:"/\\|?*'
        for char in caracteres_invalidos:
            nombre_limpio = nombre_limpio.replace(char, "")

        return nombre_limpio

    def _generar_contenido_html_individual(
        self,
        autorizador_principal: Dict[str, str],
        todos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha: str,
    ) -> str:
        """Genera contenido HTML personalizado para un autorizador específico."""

        # Destacar el rol del autorizador principal
        tabla_autorizadores = ""
        for dato in todos_autorizadores:
            estilo_fila = ""
            if dato["codigo"] == autorizador_principal["codigo"]:
                estilo_fila = 'style="background-color: #fff2cc; font-weight: bold;"'

            tabla_autorizadores += f"""
                <tr {estilo_fila}>
                    <td style="padding: 8px; border: 1px solid #ddd;">{dato['codigo']}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{dato['autorizador']}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{dato['correo']}</td>
                </tr>"""

        lista_grupos = "".join([f"<li>{grupo}</li>" for grupo in grupos_red])

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Solicitud de Conformidad</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 20px; color: #333;">
    <div style="border: 2px solid #007acc; border-radius: 8px; padding: 20px; background-color: #f8f9fa;">
        <h2 style="color: #007acc; margin-top: 0;">🔐 Solicitud de Conformidad - Código {autorizador_principal['codigo']}</h2>
        <p style="color: #666; margin: 5px 0;"><strong>Fecha:</strong> {fecha}</p>
        <p style="color: #007acc; font-weight: bold;">Autorizador responsable: {autorizador_principal['autorizador']}</p>
    </div>

    <p>Estimado(a) <strong>{autorizador_principal['autorizador']}</strong>,</p>

    <p>Esperamos que se encuentre bien. Le escribimos para solicitar su <strong style="color: #d63384;">CONFORMIDAD</strong> respecto a la asignación de roles y permisos en los siguientes sistemas:</p>

    <div style="background-color: #e7f3ff; padding: 15px; border-left: 4px solid #007acc; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #007acc;">📋 Grupos de Red Solicitados:</h3>
        <ul style="margin: 10px 0;">
            {lista_grupos}
        </ul>
    </div>

    <h3 style="color: #333;">👥 Matriz de Autorizadores:</h3>
    <p><em>Su código de aplicación aparece destacado en amarillo:</em></p>

    <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
        <thead>
            <tr style="background-color: #007acc; color: white;">
                <th style="padding: 10px; border: 1px solid #ddd;">Código Aplicación</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Autorizador Responsable</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Correo Electrónico</th>
            </tr>
        </thead>
        <tbody>
            {tabla_autorizadores}
        </tbody>
    </table>

    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 20px; margin: 20px 0;">
        <h3 style="color: #856404; margin-top: 0;">📝 ACCIÓN REQUERIDA PARA EL CÓDIGO {autorizador_principal['codigo']}:</h3>
        <p>Por favor, revise la información anterior y confirme específicamente para su código de aplicación <strong style="background-color: #fff2cc; padding: 2px 6px; border-radius: 3px;">{autorizador_principal['codigo']}</strong>:</p>
        <ul style="color: #856404;">
            <li>✅ <strong>APRUEBO</strong> - La asignación de roles es correcta</li>
            <li>❌ <strong>RECHAZO</strong> - Se requieren modificaciones (especificar motivo)</li>
        </ul>
        <p style="color: #856404;"><strong>Plazo de respuesta:</strong> 3 días hábiles a partir de la fecha de este correo.</p>
    </div>

    <div style="border-top: 1px solid #ddd; padding-top: 20px; margin-top: 30px;">
        <h4 style="color: #007acc;">📞 Información de Contacto:</h4>
        <p>
            • <strong>Equipo de Gestión de Accesos</strong><br>
            • Email: <a href="mailto:gestion.accesos@empresa.com">gestion.accesos@empresa.com</a><br>
            • Teléfono: +1 (555) 123-4567
        </p>

        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 12px; color: #666;">
            Este correo ha sido generado automáticamente por el Sistema de Gestión de Matriz de Roles.<br>
            Por favor, no responda directamente a este correo. Utilice los datos de contacto proporcionados.
        </p>
    </div>
</body>
</html>"""

    def _generar_contenido_texto_individual(
        self,
        autorizador_principal: Dict[str, str],
        todos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha: str,
    ) -> str:
        """Genera contenido de texto plano personalizado para un autorizador específico."""

        lista_grupos = "\n".join([f"  • {grupo}" for grupo in grupos_red])

        lista_autorizadores = ""
        for dato in todos_autorizadores:
            marcador = (
                " *** SU CÓDIGO ***"
                if dato["codigo"] == autorizador_principal["codigo"]
                else ""
            )
            lista_autorizadores += f"  • {dato['codigo']} - {dato['autorizador']} ({dato['correo']}){marcador}\n"

        return f"""SOLICITUD DE CONFORMIDAD - CÓDIGO {autorizador_principal['codigo']}
=========================================================

Fecha: {fecha}
Autorizador responsable: {autorizador_principal['autorizador']}

Estimado(a) {autorizador_principal['autorizador']},

Esperamos que se encuentre bien. Le escribimos para solicitar su CONFORMIDAD respecto a la asignación de roles y permisos en los siguientes sistemas:

GRUPOS DE RED SOLICITADOS:
{lista_grupos}

MATRIZ DE AUTORIZADORES:
(Su código {autorizador_principal['codigo']} aparece marcado con ***)
{lista_autorizadores}

ACCIÓN REQUERIDA ESPECÍFICAMENTE PARA EL CÓDIGO {autorizador_principal['codigo']}:
================================================================
Por favor, revise la información anterior y confirme:
  ✅ APRUEBO - La asignación de roles es correcta
  ❌ RECHAZO - Se requieren modificaciones (especificar motivo)

Plazo de respuesta: 3 días hábiles a partir de la fecha de este correo.

INFORMACIÓN DE CONTACTO:
========================
  • Equipo de Gestión de Accesos
  • Email: gestion.accesos@empresa.com
  • Teléfono: +1 (555) 123-4567

---
Este correo ha sido generado automáticamente por el Sistema de Gestión de Matriz de Roles.
Por favor, no responda directamente a este correo. Utilice los datos de contacto proporcionados.
"""

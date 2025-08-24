"""
Módulo para generar correos de solicitud de conformidad a autorizadores.

Este módulo crea archivos .msg de Outlook individuales para cada autorizador
con la solicitud de conformidad para los autorizadores de roles.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import win32com.client
    import pythoncom

    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False
    print(
        "Advertencia: pywin32 no está disponible. Se crearán archivos EML en lugar de MSG."
    )


class GeneradorCorreos:
    """Generador de correos de solicitud de conformidad."""

    def __init__(self):
        """Inicializa el generador de correos."""
        self.directorio_salida = Path(__file__).parent.parent / "output" / "correos"
        self.directorio_salida.mkdir(parents=True, exist_ok=True)

    def generar_correo_conformidad(
        self, datos_autorizadores: List[Dict[str, str]], grupos_red: List[str]
    ) -> str:
        """
        Genera un archivo de correo para solicitar conformidad.

        Args:
            datos_autorizadores: Lista con datos de autorizadores
            grupos_red: Lista de grupos de red seleccionados

        Returns:
            Ruta del archivo de correo generado
        """
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generar contenido del correo
        contenido_html = self._generar_contenido_html(
            datos_autorizadores, grupos_red, fecha_actual
        )
        contenido_texto = self._generar_contenido_texto(
            datos_autorizadores, grupos_red, fecha_actual
        )

        # Crear archivo .msg (simulado como .eml para compatibilidad)
        archivo_nombre = f"Solicitud_Conformidad_Matriz_Roles_{fecha_archivo}.eml"
        archivo_path = self.directorio_salida / archivo_nombre

        # Generar correo en formato EML (compatible con Outlook)
        correo_eml = self._crear_archivo_eml(
            contenido_html, contenido_texto, datos_autorizadores
        )

        with open(archivo_path, "w", encoding="utf-8") as file:
            file.write(correo_eml)

        return str(archivo_path)

    def _generar_contenido_html(
        self,
        datos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha: str,
    ) -> str:
        """Genera el contenido HTML del correo."""

        # Construir tabla de autorizadores
        tabla_autorizadores = ""
        for dato in datos_autorizadores:
            tabla_autorizadores += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{dato['codigo']}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{dato['autorizador']}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{dato['correo']}</td>
                </tr>"""

        # Construir lista de grupos de red
        lista_grupos = ""
        for grupo in grupos_red:
            lista_grupos += f"<li>{grupo}</li>"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .content {{ margin-bottom: 20px; }}
                .table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                .table th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: left; }}
                .table td {{ border: 1px solid #ddd; padding: 8px; }}
                .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🔐 Solicitud de Conformidad - Matriz de Roles</h2>
                <p><strong>Fecha:</strong> {fecha}</p>
            </div>

            <div class="content">
                <p>Estimado(a) Autorizador(a),</p>

                <p>Esperamos que se encuentre bien. Le escribimos para solicitar su <strong>conformidad</strong>
                respecto a la asignación de roles y permisos en los siguientes sistemas:</p>

                <h3>📋 Grupos de Red Solicitados:</h3>
                <ul>
                    {lista_grupos}
                </ul>

                <h3>👥 Matriz de Autorizadores:</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Código de Aplicación</th>
                            <th>Autorizador Responsable</th>
                            <th>Correo Electrónico</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tabla_autorizadores}
                    </tbody>
                </table>

                <div class="highlight">
                    <h3>📝 Acción Requerida:</h3>
                    <p>Por favor, revise la información anterior y confirme:</p>
                    <ul>
                        <li>✅ <strong>APRUEBO</strong> - La asignación de roles es correcta</li>
                        <li>❌ <strong>RECHAZO</strong> - Se requieren modificaciones (especificar motivo)</li>
                    </ul>
                    <p><strong>Plazo de respuesta:</strong> 3 días hábiles a partir de la fecha de este correo.</p>
                </div>

                <h3>📞 Información de Contacto:</h3>
                <p>Si tiene alguna consulta o requiere información adicional, no dude en contactarnos:</p>
                <ul>
                    <li><strong>Equipo de Gestión de Accesos</strong></li>
                    <li><strong>Email:</strong> gestion.accesos@empresa.com</li>
                    <li><strong>Teléfono:</strong> +1 (555) 123-4567</li>
                </ul>
            </div>

            <div class="footer">
                <p>Este correo ha sido generado automáticamente por el Sistema de Gestión de Matriz de Roles.</p>
                <p>Por favor, no responda directamente a este correo. Utilice los datos de contacto proporcionados.</p>
            </div>
        </body>
        </html>
        """

        return html_content

    def _generar_contenido_texto(
        self,
        datos_autorizadores: List[Dict[str, str]],
        grupos_red: List[str],
        fecha: str,
    ) -> str:
        """Genera el contenido en texto plano del correo."""

        # Construir lista de autorizadores
        lista_autorizadores = ""
        for dato in datos_autorizadores:
            lista_autorizadores += (
                f"  • {dato['codigo']} - {dato['autorizador']} ({dato['correo']})\n"
            )

        # Construir lista de grupos
        lista_grupos = ""
        for grupo in grupos_red:
            lista_grupos += f"  • {grupo}\n"

        texto_content = f"""
SOLICITUD DE CONFORMIDAD - MATRIZ DE ROLES
==========================================

Fecha: {fecha}

Estimado(a) Autorizador(a),

Esperamos que se encuentre bien. Le escribimos para solicitar su CONFORMIDAD
respecto a la asignación de roles y permisos en los siguientes sistemas:

GRUPOS DE RED SOLICITADOS:
{lista_grupos}

MATRIZ DE AUTORIZADORES:
{lista_autorizadores}

ACCIÓN REQUERIDA:
Por favor, revise la información anterior y confirme:
  ✅ APRUEBO - La asignación de roles es correcta
  ❌ RECHAZO - Se requieren modificaciones (especificar motivo)

Plazo de respuesta: 3 días hábiles a partir de la fecha de este correo.

INFORMACIÓN DE CONTACTO:
  • Equipo de Gestión de Accesos
  • Email: gestion.accesos@empresa.com
  • Teléfono: +1 (555) 123-4567

---
Este correo ha sido generado automáticamente por el Sistema de Gestión de Matriz de Roles.
Por favor, no responda directamente a este correo. Utilice los datos de contacto proporcionados.
        """

        return texto_content

    def _crear_archivo_eml(
        self,
        contenido_html: str,
        contenido_texto: str,
        datos_autorizadores: List[Dict[str, str]],
    ) -> str:
        """Crea el contenido del archivo EML."""

        # Obtener lista de destinatarios
        destinatarios = []
        for dato in datos_autorizadores:
            if dato["correo"]:
                destinatarios.append(f"{dato['autorizador']} <{dato['correo']}>")

        destinatarios_str = "; ".join(destinatarios)
        fecha_rfc = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

        eml_content = f"""From: Gestión de Accesos <gestion.accesos@empresa.com>
To: {destinatarios_str}
Subject: 🔐 Solicitud de Conformidad - Matriz de Roles - ACCIÓN REQUERIDA
Date: {fecha_rfc}
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

        return eml_content


def generar_correo_desde_datos(
    datos_autorizadores: List[Dict[str, str]], grupos_red: List[str]
) -> str:
    """
    Función de conveniencia para generar un correo de conformidad.

    Args:
        datos_autorizadores: Lista con datos de autorizadores
        grupos_red: Lista de grupos de red

    Returns:
        Ruta del archivo de correo generado
    """
    generador = GeneradorCorreos()
    return generador.generar_correo_conformidad(datos_autorizadores, grupos_red)

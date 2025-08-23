"""Tests para la interfaz gráfica de solicitud de matrices."""

import os
import tkinter as tk
from unittest import TestCase, main, mock
from pathlib import Path

import yaml

from matriz_rol.gui.solicitud_matriz import SolicitudMatrizFrame


class TestSolicitudMatrizFrame(TestCase):
    """Pruebas para la interfaz de solicitud de matrices."""

    def setUp(self):
        """Configura el ambiente de prueba."""
        self.root = tk.Tk()
        self.frame = SolicitudMatrizFrame(self.root)

        # Crear archivo de configuración temporal para pruebas
        self.config_test = {
            "matrices_rol": [
                {
                    "nombre": "Test Matriz 1",
                    "id": "TEST1",
                    "descripcion": "Matriz de prueba 1",
                },
                {
                    "nombre": "Test Matriz 2",
                    "id": "TEST2",
                    "descripcion": "Matriz de prueba 2",
                },
            ]
        }

        self.config_path = Path("test_matrices.yaml")
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config_test, f)

    def tearDown(self):
        """Limpia el ambiente después de las pruebas."""
        self.root.destroy()
        if self.config_path.exists():
            self.config_path.unlink()

    def test_inicializacion(self):
        """Prueba la inicialización correcta del frame."""
        self.assertIsNotNone(self.frame.frame_matrices)
        self.assertIsNotNone(self.frame.frame_grupos)
        self.assertIsNotNone(self.frame.txt_grupos)
        self.assertIsNotNone(self.frame.btn_confirmar)
        self.assertEqual(len(self.frame.matrices_seleccionadas), 0)
        self.assertEqual(len(self.frame.grupos_red), 0)

    def test_toggle_matriz(self):
        """Prueba la selección/deselección de matrices."""
        matriz = {"id": "TEST1", "nombre": "Test Matriz"}

        # Probar selección
        self.frame.toggle_matriz(matriz)
        self.assertIn("TEST1", self.frame.matrices_seleccionadas)

        # Probar deselección
        self.frame.toggle_matriz(matriz)
        self.assertNotIn("TEST1", self.frame.matrices_seleccionadas)

    @mock.patch("subprocess.run")
    def test_validar_grupos_red(self, mock_run):
        """Prueba la validación de grupos de red."""
        # Simular grupo válido
        mock_run.return_value.returncode = 0
        self.frame.grupos_red = ["grupo_valido"]
        validos, invalidos = self.frame.validar_grupos_red()
        self.assertEqual(validos, ["grupo_valido"])
        self.assertEqual(invalidos, [])

        # Simular grupo inválido
        mock_run.return_value.returncode = 1
        self.frame.grupos_red = ["grupo_invalido"]
        validos, invalidos = self.frame.validar_grupos_red()
        self.assertEqual(validos, [])
        self.assertEqual(invalidos, ["grupo_invalido"])

    @mock.patch("tkinter.messagebox.showwarning")
    def test_validacion_campos_requeridos(self, mock_showwarning):
        """Prueba la validación de campos requeridos."""
        # Probar sin matrices seleccionadas
        self.frame.matrices_seleccionadas = []
        self.frame.confirmar_seleccion()
        mock_showwarning.assert_called_with(
            "Advertencia", "Debe seleccionar al menos una matriz"
        )

        # Probar sin grupos de red
        self.frame.matrices_seleccionadas = ["TEST1"]
        self.frame.txt_grupos.delete("1.0", "end")
        self.frame.confirmar_seleccion()
        mock_showwarning.assert_called_with(
            "Advertencia", "Debe ingresar al menos un grupo de red"
        )

    def test_procesamiento_grupos_red(self):
        """Prueba el procesamiento de grupos de red ingresados."""
        grupos_texto = "grupo1\ngrupo2\n\ngrupo3"
        self.frame.txt_grupos.insert("1.0", grupos_texto)

        # Simular confirmación
        self.frame.matrices_seleccionadas = ["TEST1"]
        with mock.patch("tkinter.messagebox.askyesno", return_value=False):
            self.frame.confirmar_seleccion()

        # Verificar que se procesaron correctamente los grupos
        self.assertEqual(self.frame.grupos_red, ["grupo1", "grupo2", "grupo3"])


if __name__ == "__main__":
    main()

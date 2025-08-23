"""Tests para el CLI de matriz-rol."""

import json

from click.testing import CliRunner

from matriz_rol.cli import cli, convertir, crear, validar


def test_validar_matriz_valida(tmp_path):
    """Prueba la validación de una matriz válida."""
    # Crear archivo de prueba
    matriz = {"admin": ["leer", "escribir"], "editor": ["leer"]}
    archivo = tmp_path / "matriz.json"
    archivo.write_text(json.dumps(matriz))

    runner = CliRunner()
    result = runner.invoke(validar, [str(archivo)])

    assert result.exit_code == 0
    assert "✅ Matriz válida" in result.output
    assert "admin" in result.output
    assert "editor" in result.output


def test_validar_matriz_invalida(tmp_path):
    """Prueba la validación de una matriz inválida."""
    # Crear archivo con JSON inválido
    archivo = tmp_path / "invalido.json"
    archivo.write_text("{rol: [}")

    runner = CliRunner()
    result = runner.invoke(validar, [str(archivo)])

    assert result.exit_code == 0
    assert "❌ Error" in result.output


def test_convertir_matriz(tmp_path):
    """Prueba la conversión de una matriz."""
    # Crear archivo de origen
    matriz = {"admin": ["leer", "escribir"], "editor": ["leer"]}
    origen = tmp_path / "origen.json"
    origen.write_text(json.dumps(matriz))

    destino = tmp_path / "destino.json"

    runner = CliRunner()
    result = runner.invoke(convertir, [str(origen), str(destino)])

    assert result.exit_code == 0
    assert "✅ Matriz convertida" in result.output
    assert destino.exists()

    # Verificar contenido del archivo destino
    matriz_convertida = json.loads(destino.read_text())
    assert matriz_convertida == matriz


def test_crear_matriz(tmp_path):
    """Prueba la creación interactiva de una matriz."""
    archivo = tmp_path / "nueva.json"

    runner = CliRunner()
    result = runner.invoke(
        crear, [str(archivo)], input="admin\nleer\nescribir\n\nviewer\nleer\n\n\n"
    )

    assert result.exit_code == 0
    assert "✅ Matriz creada" in result.output
    assert archivo.exists()

    # Verificar contenido del archivo creado
    matriz = json.loads(archivo.read_text())
    assert matriz == {"admin": ["leer", "escribir"], "viewer": ["leer"]}

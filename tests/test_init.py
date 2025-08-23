"""
Tests de configuración inicial.
"""

def test_version():
    """Verifica que la versión del paquete esté definida."""
    from matriz_rol import __version__
    assert __version__ == '0.1.0'

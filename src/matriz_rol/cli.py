"""
Script CLI para la gestión de matrices de roles.
"""

import click
from matriz_rol import MatrizRoles
from matriz_rol.utils.io import cargar_matriz_desde_json, guardar_matriz_en_json


@click.group()
def cli():
    """Herramienta CLI para gestión de matrices de roles."""
    pass


@cli.command()
@click.argument('archivo', type=click.Path(exists=True))
def validar(archivo):
    """Valida una matriz de roles desde un archivo JSON."""
    try:
        matriz = cargar_matriz_desde_json(archivo)
        click.echo(f"✅ Matriz válida: {len(matriz)} roles encontrados")
        for rol, permisos in matriz.items():
            click.echo(f"  - {rol}: {', '.join(permisos)}")
    except Exception as e:
        click.echo(f"❌ Error al validar matriz: {str(e)}", err=True)


@cli.command()
@click.argument('archivo_origen', type=click.Path(exists=True))
@click.argument('archivo_destino', type=click.Path())
def convertir(archivo_origen, archivo_destino):
    """Convierte una matriz de roles entre formatos."""
    try:
        matriz = cargar_matriz_desde_json(archivo_origen)
        guardar_matriz_en_json(matriz, archivo_destino)
        click.echo(f"✅ Matriz convertida y guardada en {archivo_destino}")
    except Exception as e:
        click.echo(f"❌ Error al convertir matriz: {str(e)}", err=True)


@cli.command()
@click.argument('archivo', type=click.Path())
def crear(archivo):
    """Crea una nueva matriz de roles interactivamente."""
    matriz = {}
    
    while True:
        rol = click.prompt("Nombre del rol (o enter para terminar)", default='', show_default=False)
        if not rol:
            break
            
        permisos = []
        while True:
            permiso = click.prompt("Agregar permiso (o enter para terminar)", default='', show_default=False)
            if not permiso:
                break
            permisos.append(permiso)
            
        matriz[rol] = permisos
        
    try:
        guardar_matriz_en_json(matriz, archivo)
        click.echo(f"✅ Matriz creada y guardada en {archivo}")
    except Exception as e:
        click.echo(f"❌ Error al guardar matriz: {str(e)}", err=True)


def main():
    """Punto de entrada principal."""
    cli()

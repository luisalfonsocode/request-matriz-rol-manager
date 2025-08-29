#!/usr/bin/env python3
"""Script de instalación para el paquete matriz-rol."""

from setuptools import setup, find_packages


def parse_requirements(filename):
    """Lee dependencias desde archivo requirements."""
    with open(filename, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("-r")
        ]


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="matriz-rol",
    version="0.1.0",
    description="Utilidades para gestión de matrices de roles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Alfonso",
    author_email="luisalfonsocode@example.com",
    url="https://github.com/luisalfonsocode/utilitarios-matriz-de-rol",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=parse_requirements("requirements/base.txt"),
    extras_require={
        "dev": parse_requirements("requirements/dev.txt"),
        "test": parse_requirements("requirements/test.txt"),
    },
    entry_points={
        "console_scripts": [
            "matriz-rol=matriz_rol.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
    ],
    keywords="roles, permisos, matriz, seguridad",
)

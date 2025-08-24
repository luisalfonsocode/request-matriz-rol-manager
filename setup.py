#!/usr/bin/env python3
"""Script de instalación para el paquete matriz-rol."""

from setuptools import setup, find_packages

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
    install_requires=[
        "PyYAML>=6.0.0",
        "customtkinter>=5.2.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
        ],
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

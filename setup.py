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
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "typing-extensions>=4.0.0",
        "dataclasses>=0.8",
        "PyYAML>=6.0.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "tqdm>=4.65.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.0.0",
            "autopep8>=2.0.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
            "ruff>=0.1.0",
            "flake8>=6.0.0",
            "bandit>=1.7.0",
            "pre-commit>=3.0.0",
            "safety>=2.3.0",
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.1.0",
            "ipython>=8.0.0",
            "jupyter>=1.0.0",
            "rich>=13.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-asyncio>=0.21.0",
            "pytest-bdd>=6.1.0",
            "pytest-benchmark>=4.0.0",
            "Faker>=18.0.0",
            "hypothesis>=6.75.0",
            "coverage>=7.2.0",
            "requests>=2.31.0",
            "requests-mock>=1.11.0",
            "WebTest>=3.0.0",
            "pytest-postgresql>=4.1.1",
            "pytest-mongodb>=2.2.0",
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

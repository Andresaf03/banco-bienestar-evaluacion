"""Rutas del proyecto y lectura de configuración.

Todas las rutas se resuelven desde la raíz del repo (carpeta que contiene `pyproject.toml`),
para que los módulos funcionen igual desde `make`, `uv run` o un notebook.
"""

from __future__ import annotations

import os
from functools import cache, lru_cache
from pathlib import Path

import yaml


@lru_cache(maxsize=1)
def raiz() -> Path:
    """Devuelve la raíz del repositorio (donde vive `pyproject.toml`)."""
    actual = Path(__file__).resolve()
    for padre in actual.parents:
        if (padre / "pyproject.toml").exists():
            return padre
    raise RuntimeError("No se encontró pyproject.toml hacia arriba de " + str(actual))


def ruta(*partes: str) -> Path:
    """Ruta absoluta relativa a la raíz del repo."""
    return raiz().joinpath(*partes)


RAW = ruta("data", "raw")
MANUAL = ruta("data", "manual")
INTERIM = ruta("data", "interim")
PROCESSED = ruta("data", "processed")
DOCS = ruta("docs")
DICCIONARIOS = ruta("docs", "diccionarios")
LITERATURA = ruta("literatura")
# `PROYECTO_SALIDAS` redirige tablas y figuras (lo mismo hace analisis/00_utils.R): las pruebas de
# humo corren el mismo código sin pisar los resultados vigentes de outputs/.
SALIDAS = Path(os.environ.get("PROYECTO_SALIDAS", ruta("outputs")))
FIGURAS = SALIDAS / "figuras"
TABLAS = SALIDAS / "tablas"
CONFIG = ruta("config")


@cache
def cargar_yaml(nombre: str) -> dict:
    """Carga `config/<nombre>.yaml` como diccionario."""
    with open(CONFIG / f"{nombre}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fuentes() -> dict:
    return cargar_yaml("fuentes")


def parametros() -> dict:
    return cargar_yaml("parametros")

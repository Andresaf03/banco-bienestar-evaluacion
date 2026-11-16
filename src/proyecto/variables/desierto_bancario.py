"""Bandera de desierto bancario: municipio sin sucursal de banca múltiple en 2019T1. **Esqueleto.**

Entrada: `cnbv_bdif.parquet` (sector `banca_multiple`, variable `sucursales`, periodo
`parametros.periodo.inicio`). Según la auditoría (P10) son 1,516 de 2,463 municipios (62%).

Salida: `data/interim/desierto_bancario.parquet` con `cve_mun, desierto_bancario (0/1),
sin_ninguna_sucursal (0/1: tampoco SOCAP ni SOFIPO ni banca de desarrollo), suc_bm_2019q1`.

Variantes pendientes: (a) definir el desierto con banca múltiple + EACP (sin ningún punto de
acceso privado), (b) usar corresponsales (no recomendado por cambios metodológicos), (c) escalar
la variable como intensidad (sucursales por 10 mil adultos en 2019T1).
"""

from __future__ import annotations

from pathlib import Path

from proyecto.utils.io import INTERIM

SALIDA = INTERIM / "desierto_bancario.parquet"


def calcular(inicio: str = "2019Q1") -> Path:
    raise NotImplementedError("Fase de análisis: pendiente. Ver docstring del módulo.")

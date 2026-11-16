"""ENOE por municipio y trimestre -> `data/interim/enoe_municipio.parquet` (fase 2).

Junta las sumas ponderadas de `descarga/enoe.py`, colapsa municipios nuevos (P-7) sumando y calcula
los indicadores preregistrados (2026-10-07), en porcentaje salvo el ingreso:

- `pct_negocio`: empleadores + cuenta propia / ocupados con posición especificada;
- `pct_informal`: ocupados en el sector informal (`tue2 = 5`) / ocupados;
- `pct_ocupacion`: ocupados / población de 15 a 98 años;
- `log_ingreso`: media ponderada de log(ingreso mensual > 0) de los ocupados;
- `n_registros`: personas del universo en la muestra (sin ponderar).
"""

from __future__ import annotations

import logging

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM

log = logging.getLogger(__name__)

PARTES = INTERIM / "enoe" / "partes"
SALIDA = INTERIM / "enoe_municipio.parquet"


def limpiar() -> None:
    s = pd.concat([pd.read_parquet(a) for a in sorted(PARTES.glob("*.parquet"))], ignore_index=True)
    s["cve_mun"] = s["cve_mun"].map(mapa_crosswalk()).fillna(s["cve_mun"])
    sumas = [c for c in s.columns if c not in ("cve_mun", "periodo")]
    s = s.groupby(["cve_mun", "periodo"], as_index=False)[sumas].sum()
    d = s[["cve_mun", "periodo", "n_registros"]].copy()
    d["pct_negocio"] = 100 * s["negocio"] / s["pos_validos"].where(s["pos_validos"] > 0)
    d["pct_informal"] = 100 * s["informal"] / s["ocupados"].where(s["ocupados"] > 0)
    d["pct_ocupacion"] = 100 * s["ocupados"] / s["pob15"].where(s["pob15"] > 0)
    d["log_ingreso"] = s["ing_log_suma"] / s["ing_validos"].where(s["ing_validos"] > 0)
    d.to_parquet(SALIDA, index=False)
    log.info(
        "ENOE municipal: %d filas, %d trimestres; municipios por trimestre: mín %d, máx %d",
        len(d),
        d["periodo"].nunique(),
        d.groupby("periodo")["cve_mun"].nunique().min(),
        d.groupby("periodo")["cve_mun"].nunique().max(),
    )

"""Consolida las partes del DENUE (una por versión × sector) en las tablas del proyecto.

`proyecto.descarga.denue` deja en `data/interim/denue/partes/` tres parquet por archivo procesado
(`loc_`, `mun_`, `pts_`). Aquí se suman las partes de cada versión y se añade el índice de
semestre, para obtener:

- `denue_localidad.parquet`: `cve_loc, cve_mun, version, semestre, s, bloque, clase, n_estab,
  n_micro, empleo_est`
- `denue_municipio.parquet`: lo mismo agregado a municipio
- `denue_cobertura.parquet`: control de calidad por versión (establecimientos, localidades,
  municipios y sectores procesados)

Los bloques **no son excluyentes**: una farmacia cuenta en `consumo` y en `salud`, y todos los
establecimientos cuentan en `emprendimiento` (ver `denue_clasificacion.py`).
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path

import pandas as pd

from proyecto.descarga.denue import catalogo
from proyecto.utils.io import INTERIM
from proyecto.utils.periodos import semestre_a_s

log = logging.getLogger(__name__)

PARTES = INTERIM / "denue" / "partes"
SALIDA_LOC = INTERIM / "denue_localidad.parquet"
SALIDA_MUN = INTERIM / "denue_municipio.parquet"
SALIDA_COB = INTERIM / "denue_cobertura.parquet"
_RE_PARTE = re.compile(r"^(loc|mun|pts)_(\d{4}_\d{2})_(.+)\.parquet$")


def partes(prefijo: str) -> dict[str, list[Path]]:
    """`version -> [rutas]` de las partes con ese prefijo."""
    salida: dict[str, list[Path]] = {}
    for ruta in sorted(PARTES.glob(f"{prefijo}_*.parquet")):
        m = _RE_PARTE.match(ruta.name)
        if m:
            salida.setdefault(m.group(2), []).append(ruta)
    return salida


def _consolidar(prefijo: str, llaves: list[str]) -> pd.DataFrame:
    por_version = partes(prefijo)
    if not por_version:
        raise FileNotFoundError(
            f"no hay partes `{prefijo}_*` en {PARTES}; corre `make descargar-denue`"
        )
    marcos = []
    for version, rutas in sorted(por_version.items()):
        d = pd.concat([pd.read_parquet(r) for r in rutas], ignore_index=True)
        d = (
            d.groupby(llaves, observed=True)[["n_estab", "n_micro", "empleo_est"]]
            .sum()
            .reset_index()
        )
        marcos.append(d)
        log.debug("%s %s: %d filas de %d sectores", prefijo, version, len(d), len(rutas))
    out = pd.concat(marcos, ignore_index=True)
    out["s"] = out["semestre"].map(semestre_a_s)
    out["n_estab"] = out["n_estab"].astype("int32")
    out["n_micro"] = out["n_micro"].astype("int32")
    out["empleo_est"] = out["empleo_est"].astype("float32")
    return out


def limpiar() -> Path:
    loc = _consolidar("loc", ["cve_loc", "cve_mun", "version", "semestre", "bloque", "clase"])
    mun = _consolidar("mun", ["cve_mun", "version", "semestre", "bloque", "clase"])
    loc.to_parquet(SALIDA_LOC, index=False, compression="zstd")
    mun.to_parquet(SALIDA_MUN, index=False, compression="zstd")

    emp = loc[loc["bloque"] == "emprendimiento"]
    cobertura = (
        emp.groupby(["version", "semestre", "s"], observed=True)
        .agg(
            establecimientos=("n_estab", "sum"),
            micronegocios=("n_micro", "sum"),
            empleo_est=("empleo_est", "sum"),
            localidades=("cve_loc", "nunique"),
            municipios=("cve_mun", "nunique"),
        )
        .reset_index()
        .sort_values("s")
    )
    cobertura["sectores_procesados"] = cobertura["version"].map(
        {v: len(r) for v, r in partes("loc").items()}
    )
    # Una versión con menos sectores de los que publica el INEGI está incompleta: usarla en el
    # panel produciría caídas artificiales de establecimientos.
    esperados = Counter(m["version"] for m in catalogo())
    cobertura["sectores_esperados"] = cobertura["version"].map(esperados)
    cobertura["completa"] = cobertura["sectores_procesados"] == cobertura["sectores_esperados"]
    incompletas = cobertura.loc[~cobertura["completa"], "version"].tolist()
    if incompletas:
        log.warning(
            "versiones DENUE incompletas (no usar en el panel hasta terminar la descarga): %s",
            ", ".join(incompletas),
        )
    cobertura.to_parquet(SALIDA_COB, index=False)
    log.info(
        "DENUE: %d versiones, %d filas por localidad, %d por municipio; "
        "establecimientos por versión: mínimo %s, máximo %s",
        loc["version"].nunique(),
        len(loc),
        len(mun),
        f"{cobertura['establecimientos'].min():,}",
        f"{cobertura['establecimientos'].max():,}",
    )
    return SALIDA_LOC


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    limpiar()

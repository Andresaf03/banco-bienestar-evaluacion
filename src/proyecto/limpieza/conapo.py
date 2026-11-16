"""CONAPO: índices de marginación municipal (2010, 2015, 2020) y proyecciones de población.

Salidas:
- `data/interim/conapo_marginacion.parquet`: formato largo por año: `cve_mun, anio, <indicadores>,
  im (índice), gm (grado), imn (índice normalizado)`. Se conservan todas las variables; los
  nombres se pasan a snake_case sin acentos (`PL.5000` -> `pl_5000`).
- `data/interim/conapo_proyecciones_quinq.parquet`: población a mitad de año por municipio, sexo,
  año (1990–2040) y grupo quinquenal; agrega `pob_15_mas`, `pob_18_mas_aprox` (18+ aproximado
  como 3/5 del grupo 15–19 más 20+; el grupo exacto 18+ no existe en la fuente) y `pob_total`.
- `data/interim/conapo_proyecciones_inddemo.parquet`: indicadores demográficos municipales.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path

import pandas as pd

from proyecto.utils.claves import normalizar_serie
from proyecto.utils.io import INTERIM, MANUAL

log = logging.getLogger(__name__)

MARG = MANUAL / "conapo_marginacion"
PROY = MANUAL / "conapo_proyecciones"
SALIDA_MARG = INTERIM / "conapo_marginacion.parquet"
SALIDA_QUINQ = INTERIM / "conapo_proyecciones_quinq.parquet"
SALIDA_INDDEMO = INTERIM / "conapo_proyecciones_inddemo.parquet"
ARCHIVOS_MARG = {2020: "imm_2020.csv", 2015: "imm_dp2_2015.csv", 2010: "imm_dp2_2010.csv"}
FRACCION_18_EN_15_19 = 2 / 5  # edades 18 y 19 de las cinco del grupo 15–19 (aproximación uniforme)


def _snake(nombre: str) -> str:
    t = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return t


def limpiar_marginacion() -> Path:
    partes = []
    for anio, nombre in ARCHIVOS_MARG.items():
        df = pd.read_csv(MARG / nombre, dtype=str, encoding="utf-8-sig", keep_default_na=False)
        df.columns = [_snake(c) for c in df.columns]
        df = df.rename(columns={f"im_{anio}": "im", f"gm_{anio}": "gm", f"imn_{anio}": "imn"})
        df["cve_mun"] = normalizar_serie(df["cve_mun"])
        df["cve_ent"] = df["cve_mun"].str[:2]
        df["anio"] = anio
        for c in df.columns:
            if c in (
                "cve_mun",
                "cve_ent",
                "nom_ent",
                "nom_mun",
                "gm",
                "entidad",
                "nom_ent_etq",
                "anio",
            ):
                continue
            df[c] = pd.to_numeric(df[c], errors="coerce")
        partes.append(df.drop(columns=[c for c in ("entidad", "nom_ent_etq") if c in df.columns]))
    out = pd.concat(partes, ignore_index=True)
    cols = ["cve_mun", "cve_ent", "nom_ent", "nom_mun", "anio", "pob_tot", "im", "gm", "imn"]
    out = out[[*cols, *[c for c in out.columns if c not in cols]]]
    out.to_parquet(SALIDA_MARG, index=False)
    log.info("CONAPO marginación: %s", out.groupby("anio").size().to_dict())
    return SALIDA_MARG


def limpiar_proyecciones() -> tuple[Path, Path]:
    q = pd.read_csv(
        PROY / "pobproy_quinq1.csv", dtype=str, encoding="utf-8-sig", keep_default_na=False
    )
    q.columns = [_snake(c) for c in q.columns]
    q["cve_mun"] = normalizar_serie(q["clave"])
    q["anio"] = pd.to_numeric(q["ano"], errors="coerce").astype("Int64")
    grupos = [c for c in q.columns if c.startswith("pob_") and c != "pob_total"]
    for c in [*grupos, "pob_total"]:
        q[c] = pd.to_numeric(q[c], errors="coerce")
    mayores_15 = [c for c in grupos if c not in ("pob_00_04", "pob_05_09", "pob_010_014")]
    q["pob_15_mas"] = q[mayores_15].sum(axis=1)
    q["pob_18_mas_aprox"] = q["pob_15_mas"] - (1 - FRACCION_18_EN_15_19) * q["pob_015_019"]
    q = q.drop(columns=["clave", "ano", "fecha", "etiqueta_estado"], errors="ignore").rename(
        columns={"clave_ent": "cve_ent"}
    )
    q["cve_ent"] = q["cve_mun"].str[:2]
    q = q[
        [
            "cve_mun",
            "cve_ent",
            "nom_ent",
            "nom_mun",
            "sexo",
            "anio",
            "pob_total",
            "pob_15_mas",
            "pob_18_mas_aprox",
            *grupos,
        ]
    ]
    q.to_parquet(SALIDA_QUINQ, index=False)

    d = pd.read_csv(
        PROY / "pobproy_inddemo.csv", dtype=str, encoding="utf-8-sig", keep_default_na=False
    )
    d.columns = [_snake(c) for c in d.columns]
    d["cve_mun"] = normalizar_serie(d["clave"])
    d["anio"] = pd.to_numeric(d["ano"], errors="coerce").astype("Int64")
    for c in d.columns:
        if c not in (
            "cve_mun",
            "clave",
            "clave_ent",
            "nom_ent",
            "nom_mun",
            "ano",
            "anio",
            "fecha",
            "n",
        ):
            d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.drop(columns=["clave", "ano", "fecha", "n"], errors="ignore").rename(
        columns={"clave_ent": "cve_ent"}
    )
    d["cve_ent"] = d["cve_mun"].str[:2]
    d.to_parquet(SALIDA_INDDEMO, index=False)
    log.info(
        "CONAPO proyecciones: %d filas quinquenales, %d municipios, años %s–%s",
        len(q),
        q["cve_mun"].nunique(),
        q["anio"].min(),
        q["anio"].max(),
    )
    return SALIDA_QUINQ, SALIDA_INDDEMO


def limpiar() -> Path:
    limpiar_marginacion()
    limpiar_proyecciones()
    return SALIDA_MARG

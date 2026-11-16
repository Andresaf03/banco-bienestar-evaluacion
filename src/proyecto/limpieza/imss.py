"""IMSS por municipio -> `data/interim/imss_municipio.parquet` (clave INEGI, trimestral).

Consolida las partes que deja `descarga.imss` (una por cierre de trimestre) y cruza el municipio
del catálogo IMSS a la clave INEGI con `utils.cruce_nombres` (excepción controlada a la regla 6).
Varias claves IMSS pueden ir al mismo municipio (el IMSS parte algunas ciudades en sectores) y se
suman. Lo que no se cruza se reporta con su peso en puestos: nunca se descarta en silencio.
"""

from __future__ import annotations

import logging

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.cruce_nombres import cruzar, manuales, resumen_md
from proyecto.utils.io import DICCIONARIOS, INTERIM, RAW

log = logging.getLogger(__name__)
PARTES = INTERIM / "imss" / "partes"
SALIDA = INTERIM / "imss_municipio.parquet"
CRUCE = INTERIM / "cruce_municipios_imss.parquet"
MEDIDAS = ["asegurados", "ta", "masa_sal_ta", "ta_micro", "ta_pequena"]
# Tamaño del registro patronal (catálogo IMSS): S1 = 1 puesto, S2 = 2–5, S3 = 6–50.
MICRO = {"S1", "S2"}
PEQUENA = {"S3"}


def catalogo_imss() -> pd.DataFrame:
    d = pd.read_excel(
        RAW / "imss" / "diccionario_de_datos_1.xlsx",
        sheet_name="entidad-municipio",
        header=1,
        dtype=str,
    )
    d = d.rename(columns={"descripción municipio": "municipio", "descripción entidad": "entidad"})
    d["cve_ent"] = d["cve_entidad"].str.zfill(2)
    return d[["cve_municipio", "cve_ent", "entidad", "municipio"]].drop_duplicates("cve_municipio")


def limpiar() -> None:
    cruce = cruzar(catalogo_imss(), "cve_municipio", "cve_ent", "municipio", manuales("imss"))
    cruce.to_parquet(CRUCE, index=False)
    (DICCIONARIOS / "cruce_municipios_imss.md").write_text(
        resumen_md(cruce, "IMSS", "cve_municipio", "municipio"), encoding="utf-8"
    )
    partes = sorted(PARTES.glob("asg_*.parquet"))
    if not partes:
        raise FileNotFoundError("sin partes del IMSS: corre `make descargar-imss`")
    d = pd.concat([pd.read_parquet(p) for p in partes], ignore_index=True)
    if "tamano_patron" not in d.columns:
        raise ValueError("partes del IMSS sin desglose por tamaño: vuelve a bajarlas con FORCE=1")
    d = d.assign(
        ta_micro=d["ta"].where(d["tamano_patron"].isin(MICRO), 0),
        ta_pequena=d["ta"].where(d["tamano_patron"].isin(PEQUENA), 0),
    )
    d = d.merge(cruce[["cve_municipio", "cve_mun"]], on="cve_municipio", how="left")
    sin = d["cve_mun"].isna()
    # La CDMX viene sin clave de municipio (todas sus alcaldías juntas): no se puede asignar y de
    # todos modos sus alcaldías están ya tratadas al inicio.
    log.info(
        "IMSS: %d de %d claves sin cruzar (incluye la CDMX sin municipio); %.2f%% de los puestos "
        "afiliados quedan fuera",
        d.loc[sin, "cve_municipio"].nunique(),
        d["cve_municipio"].nunique(),
        100 * d.loc[sin, "ta"].sum() / d["ta"].sum(),
    )
    d = d[~sin]
    d["cve_mun"] = d["cve_mun"].map(mapa_crosswalk()).fillna(d["cve_mun"])
    salida = d.groupby(["cve_mun", "periodo"], as_index=False)[MEDIDAS].sum()
    salida.to_parquet(SALIDA, index=False)
    log.info(
        "IMSS municipal: %d filas, %d municipios, %d trimestres",
        len(salida),
        salida["cve_mun"].nunique(),
        salida["periodo"].nunique(),
    )

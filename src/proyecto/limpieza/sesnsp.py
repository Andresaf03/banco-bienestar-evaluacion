"""SESNSP, incidencia delictiva municipal -> `data/interim/sesnsp_municipio_trim.parquet` (fase 3).

Del zip manual (`data/manual/sesnsp/`) se lee el CSV consolidado 2015–2025 (latin-1, un mes por
columna) y, para cada resultado preregistrado (`parametros.fase3.delitos.resultados`: tipo de
delito y, si aplica, subtipos), se suman las carpetas de investigación por municipio y trimestre.

- La clave del SESNSP es la del INEGI sin el cero inicial (`1001` = `01001`): no se une por nombre.
- Las claves terminadas en 998/999 ("No especificado", "Otros municipios") salen y se reporta su
  peso.
- Meses -> trimestres con `sum(min_count=1)`: un municipio que no aparece en un año (2015–2016
  cubren solo 1,931) queda NaN, no cero. Los municipios creados después de 2010 se colapsan en su
  municipio de origen (P-7) con la misma regla.
"""

from __future__ import annotations

import logging
import zipfile

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM, MANUAL, fuentes, parametros

log = logging.getLogger(__name__)

SALIDA = INTERIM / "sesnsp_municipio_trim.parquet"
MESES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]
CLAVES_NO_MUNICIPALES = ("998", "999")


def leer_csv() -> pd.DataFrame:
    cfg = fuentes()["sesnsp"]
    ruta = MANUAL / "sesnsp" / cfg["archivo"]
    nombre = cfg["archivo"].removesuffix(".zip") + ".csv"
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        d = pd.read_csv(
            f,
            encoding="latin-1",
            usecols=["Año", "Cve. Municipio", "Tipo de delito", "Subtipo de delito", *MESES],
            dtype={
                "Cve. Municipio": str,
                "Tipo de delito": "category",
                "Subtipo de delito": "category",
            },
        )
    return d.rename(
        columns={
            "Año": "anio",
            "Cve. Municipio": "cve_mun",
            "Tipo de delito": "tipo",
            "Subtipo de delito": "subtipo",
        }
    )


def colapsar_trimestres(mensual: pd.DataFrame, valor: str) -> pd.DataFrame:
    """`cve_mun, anio, mes, <valor>` -> `cve_mun, periodo (YYYYQn), <valor>`.

    Suma los tres meses con `min_count=1`: un trimestre sin ningún mes con dato queda NaN.
    """
    trimestre = (mensual["mes"] - 1) // 3 + 1
    periodo = mensual["anio"].astype(int).astype(str) + "Q" + trimestre.astype(str)
    return (
        mensual.assign(periodo=periodo)
        .groupby(["cve_mun", "periodo"], as_index=False)[valor]
        .sum(min_count=1)
    )


def _seleccion(d: pd.DataFrame, tipo: str, subtipos: list[str]) -> pd.Series:
    mascara = d["tipo"] == tipo
    if subtipos:
        mascara &= d["subtipo"].isin(subtipos)
    return mascara


def _verificar_catalogo(d: pd.DataFrame, cfg: dict) -> None:
    """Cada tipo y subtipo preregistrado debe existir tal cual en el archivo."""
    tipos = set(d["tipo"].astype(str))
    subtipos = set(d["subtipo"].astype(str))
    for nombre, r in cfg["resultados"].items():
        faltan = [r["tipo"]] if r["tipo"] not in tipos else []
        faltan += [s for s in r["subtipos"] if s not in subtipos]
        if faltan:
            raise ValueError(f"{nombre}: el archivo del SESNSP no trae {faltan}")


def por_resultado(d: pd.DataFrame, nombre: str, tipo: str, subtipos: list[str]) -> pd.DataFrame:
    """Carpetas del resultado por municipio y trimestre (`delitos_<nombre>`)."""
    sub = d[_seleccion(d, tipo, subtipos)]
    anual = sub.groupby(["cve_mun", "anio"], as_index=False)[MESES].sum(min_count=1)
    mensual = anual.melt(id_vars=["cve_mun", "anio"], value_vars=MESES, var_name="mes")
    mensual["mes"] = mensual["mes"].map({m: i for i, m in enumerate(MESES, start=1)})
    return colapsar_trimestres(mensual, "value").rename(columns={"value": f"delitos_{nombre}"})


def limpiar() -> None:
    cfg = parametros()["fase3"]["delitos"]
    d = leer_csv()
    _verificar_catalogo(d, cfg)
    d["cve_mun"] = d["cve_mun"].str.strip().str.zfill(5)
    no_mun = d["cve_mun"].str.endswith(CLAVES_NO_MUNICIPALES)
    total = d[MESES].sum().sum()
    log.info(
        "SESNSP: %d renglones; claves no municipales (998/999): %.2f%% de las carpetas",
        len(d),
        100 * d.loc[no_mun, MESES].sum().sum() / total,
    )
    d = d[~no_mun]
    salida = None
    for nombre, r in cfg["resultados"].items():
        parte = por_resultado(d, nombre, r["tipo"], r["subtipos"])
        salida = (
            parte if salida is None else salida.merge(parte, on=["cve_mun", "periodo"], how="outer")
        )
    columnas = [c for c in salida.columns if c.startswith("delitos_")]
    validos = set(pd.read_parquet(INTERIM / "municipios.parquet", columns=["cve_mun"])["cve_mun"])
    mapa = mapa_crosswalk()
    desconocidas = sorted(set(salida["cve_mun"]) - validos - set(mapa))
    if desconocidas:
        log.warning("claves del SESNSP fuera del catálogo INEGI (salen): %s", desconocidas)
        salida = salida[~salida["cve_mun"].isin(desconocidas)]
    salida["cve_mun"] = salida["cve_mun"].map(mapa).fillna(salida["cve_mun"])
    salida = salida.groupby(["cve_mun", "periodo"], as_index=False)[columnas].sum(min_count=1)
    salida.to_parquet(SALIDA, index=False)
    por_anio = salida.assign(anio=salida["periodo"].str[:4]).groupby("anio")
    log.info(
        "SESNSP municipal: %d filas, %d municipios; municipios con dato por año %s",
        len(salida),
        salida["cve_mun"].nunique(),
        por_anio.apply(
            lambda g: g.dropna(subset=columnas, how="all")["cve_mun"].nunique()
        ).to_dict(),
    )

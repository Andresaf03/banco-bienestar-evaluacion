"""Remesas por municipio (Banxico CE166) -> `data/interim/remesas_municipio.parquet`.

El CSV exportado del SIE trae una fila de títulos (`Ingresos por Remesas, Distribución por
Municipio, <Entidad>, <Municipio>`), otra con las claves de serie y los datos trimestrales en
millones de dólares desde 2013. El nombre de la entidad se separa en la **primera** coma después
del prefijo (hay municipios con coma en el nombre). Entidad y municipio se cruzan a la clave INEGI
con `utils.cruce_nombres` (excepción controlada a la regla 6). Las series "No identificado" y los
totales estatales no entran.
"""

from __future__ import annotations

import csv
import io
import logging

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.cruce_nombres import cruzar, manuales, normalizar, resumen_md
from proyecto.utils.io import DICCIONARIOS, INTERIM, RAW, fuentes
from proyecto.utils.periodos import yyyymm_a_periodo

log = logging.getLogger(__name__)
SALIDA = INTERIM / "remesas_municipio.parquet"
CRUCE = INTERIM / "cruce_municipios_banxico.parquet"
PREFIJO = "Ingresos por Remesas, Distribución por Municipio, "
MESES_INICIO_TRIMESTRE = {"01": "03", "04": "06", "07": "09", "10": "12"}


def _leer() -> tuple[pd.DataFrame, pd.DataFrame]:
    ruta = RAW / "banxico_remesas" / fuentes()["banxico_remesas"]["archivo"]
    filas = list(csv.reader(io.StringIO(ruta.read_text(encoding="latin-1"))))
    titulos = next(f for f in filas if f and f[0] == "Título")[1:]
    claves = next(f for f in filas if f and f[0] == "Fecha")[1:]
    inicio = next(i for i, f in enumerate(filas) if f and f[0] == "Fecha") + 1
    series = []
    for clave, titulo in zip(claves, titulos, strict=True):
        if titulo.startswith(PREFIJO):
            entidad, municipio = titulo[len(PREFIJO) :].split(", ", 1)
            series.append((clave, entidad, municipio))
    series = pd.DataFrame(series, columns=["serie", "entidad", "municipio"])
    datos = pd.DataFrame(filas[inicio:], columns=["fecha", *claves]).dropna(subset=["fecha"])
    datos = datos[datos["fecha"].str.match(r"\d{2}/\d{2}/\d{4}")]
    return series, datos


def _clave_entidad(series: pd.DataFrame) -> pd.Series:
    """Entidad (nombre) -> cve_ent INEGI: exacto normalizado o contención única (p. ej.
    "Coahuila" / "Coahuila de Zaragoza")."""
    ent = pd.read_parquet(INTERIM / "municipios.parquet", columns=["cve_ent", "nom_ent"])
    ent = ent.dropna().drop_duplicates("cve_ent").assign(n=lambda x: x["nom_ent"].map(normalizar))
    mapa = {}
    for nombre in series["entidad"].unique():
        n = normalizar(nombre)
        hits = ent[(ent["n"] == n)]
        if len(hits) != 1:
            hits = ent[ent["n"].str.contains(rf"(?:^| ){n}(?: |$)", regex=True)]
        if len(hits) != 1:
            raise ValueError(f"entidad sin cruce único: {nombre}")
        mapa[nombre] = hits["cve_ent"].iloc[0]
    return series["entidad"].map(mapa)


def limpiar() -> None:
    series, datos = _leer()
    series = series[series["municipio"] != "No identificado"].assign(
        cve_ent=lambda x: _clave_entidad(x)
    )
    cruce = cruzar(series, "serie", "cve_ent", "municipio", manuales("banxico"))
    duplicados = cruce.dropna(subset=["cve_mun"])["cve_mun"].duplicated(keep=False)
    if duplicados.any():
        raise ValueError(f"remesas: {int(duplicados.sum())} series van al mismo municipio")
    cruce.to_parquet(CRUCE, index=False)
    (DICCIONARIOS / "cruce_municipios_banxico.md").write_text(
        resumen_md(cruce, "Banxico remesas (CE166)", "serie", "municipio"), encoding="utf-8"
    )
    largo = datos.melt(id_vars="fecha", var_name="serie", value_name="remesas_musd")
    largo = largo.merge(cruce[["serie", "cve_mun"]], on="serie", how="inner")
    largo["remesas_musd"] = pd.to_numeric(largo["remesas_musd"], errors="coerce")
    dia, mes, anio = largo["fecha"].str.split("/", expand=True).T.values
    largo["periodo"] = [
        yyyymm_a_periodo(a + MESES_INICIO_TRIMESTRE[m]) for a, m in zip(anio, mes, strict=True)
    ]
    sin = largo["cve_mun"].isna()
    log.info(
        "remesas: %d series sin cruzar (%.2f%% del monto)",
        largo.loc[sin, "serie"].nunique(),
        100 * largo.loc[sin, "remesas_musd"].sum() / largo["remesas_musd"].sum(),
    )
    largo = largo[~sin]
    largo["cve_mun"] = largo["cve_mun"].map(mapa_crosswalk()).fillna(largo["cve_mun"])
    salida = largo.groupby(["cve_mun", "periodo"], as_index=False)["remesas_musd"].sum(min_count=1)
    salida.to_parquet(SALIDA, index=False)
    log.info(
        "remesas municipales: %d filas, %d municipios, %s–%s",
        len(salida),
        salida["cve_mun"].nunique(),
        salida["periodo"].min(),
        salida["periodo"].max(),
    )

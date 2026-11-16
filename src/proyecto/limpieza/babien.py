"""Banco del Bienestar, directorio de sucursales: asignación espacial de `cve_mun`.

Entrada: `data/manual/babien/sucursalesbabien_1ertrim2026.csv` (foto del 1er trimestre de 2026,
sin fechas de apertura). Salida: `data/interim/babien.parquet` con una fila por sucursal:
- `cve_mun_espacial`: municipio del polígono 2024 que contiene el punto (lat/lon).
- `cve_mun_declarado`: municipio que se infiere de los campos `municipio_alcaldia` + `entidad`
  por nombre normalizado contra el catálogo (solo para comparar; **no** se usa como clave).
- `coincide`: True si ambos coinciden; `sin_coordenadas`: True si no hay lat/lon válidas.
Reporta cuántas no coinciden y cuántas no tienen coordenadas (insumo de la auditoría).
"""

from __future__ import annotations

import logging
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd

from proyecto.limpieza.municipios import poligonos_2024
from proyecto.utils.io import INTERIM, MANUAL

log = logging.getLogger(__name__)

ENTRADA = MANUAL / "babien" / "sucursalesbabien_1ertrim2026.csv"
SALIDA = INTERIM / "babien.parquet"
# México continental aprox.; fuera de esto la coordenada se considera inválida.
LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = -118.6, -86.5, 14.3, 32.8


def _norm(s: str) -> str:
    t = (
        unicodedata.normalize("NFKD", str(s or ""))
        .encode("ascii", "ignore")
        .decode()
        .lower()
        .strip()
    )
    return " ".join(t.split())


def _cve_por_nombre(df: pd.DataFrame, catalogo: pd.DataFrame) -> pd.Series:
    """Cruce por (entidad, municipio) normalizados. Solo para validar, nunca para unir bases."""
    cat = catalogo.assign(
        k_ent=catalogo["nom_ent"].map(_norm), k_mun=catalogo["nom_mun"].map(_norm)
    )
    idx = cat.drop_duplicates(["k_ent", "k_mun"]).set_index(["k_ent", "k_mun"])["cve_mun"]
    claves = pd.MultiIndex.from_arrays(
        [df["entidad"].map(_norm), df["municipio_alcaldia"].map(_norm)]
    )
    return pd.Series(idx.reindex(claves).to_numpy(), index=df.index, dtype="string")


def limpiar() -> Path:
    df = pd.read_csv(ENTRADA, dtype=str, keep_default_na=False)
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    valida = df["latitud"].between(LAT_MIN, LAT_MAX) & df["longitud"].between(LON_MIN, LON_MAX)
    df["sin_coordenadas"] = ~valida

    pol = poligonos_2024()
    pts = gpd.GeoDataFrame(
        df[valida],
        geometry=gpd.points_from_xy(df.loc[valida, "longitud"], df.loc[valida, "latitud"]),
        crs="EPSG:4326",
    ).to_crs(pol.crs)
    cruce = gpd.sjoin(pts, pol[["cve_mun", "geometry"]], how="left", predicate="within")
    cruce = cruce[~cruce.index.duplicated(keep="first")]
    df["cve_mun_espacial"] = pd.Series(cruce["cve_mun"], index=cruce.index, dtype="string").reindex(
        df.index
    )

    catalogo = pd.read_parquet(
        INTERIM / "municipios.parquet", columns=["cve_mun", "nom_mun", "nom_ent"]
    )
    df["cve_mun_declarado"] = _cve_por_nombre(df, catalogo)
    df["coincide"] = (df["cve_mun_espacial"] == df["cve_mun_declarado"]).fillna(False)
    df["id_sucursal"] = range(1, len(df) + 1)
    cols = [
        "id_sucursal",
        "nombre_institucion",
        "nombre_sucursal",
        "domicilio",
        "localidad",
        "municipio_alcaldia",
        "entidad",
        "horario_publico",
        "latitud",
        "longitud",
        "sin_coordenadas",
        "cve_mun_espacial",
        "cve_mun_declarado",
        "coincide",
    ]
    df = df[cols]
    df.to_parquet(SALIDA, index=False)
    log.info(
        "BABIEN: %d sucursales; sin coordenadas válidas: %d; sin polígono: %d; sin clave por nombre: %d; no coinciden (ambas presentes): %d",
        len(df),
        df["sin_coordenadas"].sum(),
        (valida & df["cve_mun_espacial"].isna()).sum(),
        df["cve_mun_declarado"].isna().sum(),
        (
            (~df["coincide"]) & df["cve_mun_espacial"].notna() & df["cve_mun_declarado"].notna()
        ).sum(),
    )
    return SALIDA

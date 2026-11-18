"""B1 de la fase 6: distancia de la población a la sucursal del Banco del Bienestar más cercana.

Descriptivo (preregistro del 2026-11-17, `docs/decisiones.md`). Para cada fecha de corte se toma
el conjunto de localidades con sucursal **abierta** y se mide, para cada localidad del ITER 2020,
la distancia haversine al punto de la localidad con sucursal más cercana (0 si tiene una propia).

Fechas de apertura por localidad con sucursal (`tratamiento_localidad.parquet`):
- heredadas de Bansefi (`ya_tratado_inicio`) sin ambigüedad: abiertas desde 2019T1;
- con fecha propia (`G_trimestre`, no ambigua): esa fecha;
- **ambiguas** (municipios con 2+ sucursales, la BDIF solo fecha la primera), tres versiones:
  - **central** (la que se reporta): las localidades del municipio abren en orden de población,
    cada una cuando el conteo de sucursales del municipio en la BDIF (`sucursales_bienestar`, neto
    de Banjército) alcanza las sucursales de las más pobladas más la suya; si el conteo no llega,
    en 2024T4;
  - optimista (cota): todas abren en la primera apertura del municipio;
  - pesimista (cota): solo la localidad más poblada abre en esa fecha; las demás, en 2024T4 (la
    red de 2024T4 coincide con el directorio de 2026T1).
  Corrección de la revisión del 2026-11-18: la optimista abría desde 2019T1 todas las sucursales
  de los municipios heredados de Bansefi, lo que exageraba el acceso de 2019.

La población de 65 años o más (`POB65_MAS`) viene del ITER; donde está reservada por
confidencialidad se imputa con la proporción municipal del Censo 2020.

Salida: `fase6_accesibilidad.csv` en `outputs/tablas/` (respeta `PROYECTO_SALIDAS`).
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.limpieza.inegi_censo import FALTANTES, ZIPS
from proyecto.utils.claves import combinar, combinar_localidad
from proyecto.utils.io import INTERIM, PROCESSED, TABLAS

log = logging.getLogger(__name__)

RADIO_TIERRA_KM = 6371.0
CORTES = ["2019Q1", "2021Q4", "2022Q4", "2023Q4", "2024Q4"]
UMBRALES_KM = (5, 10, 20)
TAMANOS = [
    (0, 2_500, "menos de 2,500"),
    (2_500, 15_000, "2,500 a 15 mil"),
    (15_000, np.inf, "15 mil o más"),
]
SALIDA = "fase6_accesibilidad.csv"


def localidades_iter() -> pd.DataFrame:
    """Localidades del ITER 2020 con coordenadas, población total y de 65+."""
    ruta, nombre = ZIPS[2020]
    with zipfile.ZipFile(ruta) as z:
        miembro = next(m for m in z.namelist() if m.endswith(nombre))
        with z.open(miembro) as f:
            df = pd.read_csv(
                f,
                dtype=str,
                encoding="utf-8-sig",
                keep_default_na=False,
                usecols=["ENTIDAD", "MUN", "LOC", "POBTOT", "POB65_MAS"],
            )
    df.columns = [c.lower() for c in df.columns]
    df = df[(df["mun"] != "000") & ~df["loc"].isin(["0000", "9998", "9999"])].copy()
    df["cve_mun"] = combinar(df["entidad"], df["mun"])
    df["cve_loc"] = combinar_localidad(df["cve_mun"], df["loc"])
    for c in ("pobtot", "pob65_mas"):
        df[c] = pd.to_numeric(df[c].where(~df[c].isin(FALTANTES)), errors="coerce")
    coords = pd.read_parquet(
        INTERIM / "inegi_censo_localidades_2020.parquet", columns=["cve_loc", "lat", "lon"]
    )
    df = df.merge(coords, on="cve_loc", how="inner").dropna(subset=["lat", "lon", "pobtot"])
    censo = pd.read_parquet(
        INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot", "pob65_mas"]
    )
    prop = (censo["pob65_mas"] / censo["pobtot"]).set_axis(censo["cve_mun"])
    imputar = df["pob65_mas"].isna()
    df.loc[imputar, "pob65_mas"] = df.loc[imputar, "pobtot"] * df.loc[imputar, "cve_mun"].map(prop)
    log.info("ITER: %d localidades; 65+ imputado en %d", len(df), int(imputar.sum()))
    return df[["cve_loc", "cve_mun", "lat", "lon", "pobtot", "pob65_mas"]]


def cotas_apertura(trat: pd.DataFrame, g_mun: pd.Series) -> pd.DataFrame:
    """Trimestre de apertura de cada localidad con sucursal en las dos cotas.

    `trat` trae `cve_mun_estable, G_trimestre, ya_tratado_inicio, fecha_ambigua, pobtot`; `g_mun`
    es la primera apertura del municipio, alineada con `trat`. Devuelve `optimista` y `pesimista`.
    """
    heredada = trat["ya_tratado_inicio"].fillna(False).astype(bool)
    ambigua = trat["fecha_ambigua"].fillna(False).astype(bool)
    propia = trat["G_trimestre"].where(~ambigua)
    propia = propia.where(~(heredada & ~ambigua), "2019Q1")
    optimista = propia.fillna(g_mun)
    # Pesimista: entre las ambiguas de cada municipio, solo la más poblada abre con el municipio.
    pob_ambigua = trat["pobtot"].where(ambigua)
    maxima = pob_ambigua.groupby(trat["cve_mun_estable"]).transform("max")
    principal = ambigua & (pob_ambigua == maxima)
    pesimista = propia.fillna(g_mun.where(principal | ~ambigua, "2024Q4"))
    return pd.DataFrame({"optimista": optimista, "pesimista": pesimista}, index=trat.index)


def apertura_central(trat: pd.DataFrame, conteo: pd.DataFrame) -> pd.Series:
    """Trimestre de apertura de cada localidad ambigua según el conteo municipal de la BDIF.

    `trat` trae `cve_mun, cve_loc, fecha_ambigua, n_sucursales_loc, pobtot`; `conteo` trae
    `cve_mun, periodo, suc_bienestar` (mismas claves). Las localidades de cada municipio se ordenan
    por población (de mayor a menor) y la de lugar r abre en el primer trimestre en que el conteo
    alcanza las sucursales de las r − 1 anteriores más una. Devuelve NaN en las no ambiguas.
    """
    ambiguas = trat[trat["fecha_ambigua"].fillna(False).astype(bool)].sort_values(
        ["cve_mun", "pobtot", "cve_loc"], ascending=[True, False, True]
    )
    previas = (
        ambiguas.groupby("cve_mun")["n_sucursales_loc"].cumsum() - ambiguas["n_sucursales_loc"]
    )
    necesarias = previas + 1
    series = {m: d.sort_values("periodo") for m, d in conteo.groupby("cve_mun")}
    fechas = {}
    for i, m in ambiguas["cve_mun"].items():
        s = series.get(m)
        alcanza = s[s["suc_bienestar"] >= necesarias[i]] if s is not None else None
        fechas[i] = alcanza["periodo"].iloc[0] if alcanza is not None and len(alcanza) else "2024Q4"
    return pd.Series(fechas, dtype="object").reindex(trat.index)


def fechas_apertura() -> pd.DataFrame:
    """Localidades con sucursal y su trimestre de apertura en las cotas optimista y pesimista."""
    trat = pd.read_parquet(INTERIM / "tratamiento_localidad.parquet")
    mun = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "G_trimestre"]
    ).drop_duplicates("cve_mun")
    trat["cve_mun_estable"] = trat["cve_mun"].map(mapa_crosswalk()).fillna(trat["cve_mun"])
    g_mun = trat["cve_mun_estable"].map(mun.set_index("cve_mun")["G_trimestre"])
    salida = pd.concat([trat[["cve_loc", "lat", "lon"]], cotas_apertura(trat, g_mun)], axis=1)
    conteo = pd.read_parquet(
        INTERIM / "sucursales_bienestar.parquet", columns=["cve_mun", "periodo", "suc_bienestar"]
    )
    central = apertura_central(trat, conteo)
    # Las no ambiguas tienen la misma fecha en todas las versiones.
    salida["central"] = central.fillna(salida["pesimista"].where(central.isna()))
    sin_fecha = int(salida["optimista"].isna().sum())
    if sin_fecha:
        log.warning("%d localidades con sucursal sin fecha municipal: se omiten", sin_fecha)
    return salida.dropna(subset=["optimista"])


def distancia_minima(origen: pd.DataFrame, destino: pd.DataFrame) -> np.ndarray:
    """Km de cada punto de `origen` al punto más cercano de `destino` (haversine, BallTree)."""
    from sklearn.neighbors import BallTree

    arbol = BallTree(np.radians(destino[["lat", "lon"]].to_numpy(float)), metric="haversine")
    d, _ = arbol.query(np.radians(origen[["lat", "lon"]].to_numpy(float)), k=1)
    return d[:, 0] * RADIO_TIERRA_KM


def _resumen(d: pd.DataFrame, peso: str) -> dict[str, float]:
    w = d[peso].to_numpy(float)
    km = d["km"].to_numpy(float)
    fila = {"poblacion": w.sum(), "km_media": float(np.average(km, weights=w))}
    for u in UMBRALES_KM:
        fila[f"pct_a_{u}km"] = 100 * w[km <= u].sum() / w.sum()
    return fila


def accesibilidad() -> pd.DataFrame:
    locs = localidades_iter()
    marg = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "grado_marginacion_2020"]
    ).drop_duplicates("cve_mun")
    estable = locs["cve_mun"].map(mapa_crosswalk()).fillna(locs["cve_mun"])
    locs["marginacion"] = estable.map(marg.set_index("cve_mun")["grado_marginacion_2020"])
    locs["tamano"] = pd.cut(
        locs["pobtot"],
        bins=[t[0] for t in TAMANOS] + [np.inf],
        labels=[t[2] for t in TAMANOS],
        right=False,
    ).astype(str)
    suc = fechas_apertura()
    filas = []
    for cota in ("central", "optimista", "pesimista"):
        for corte in CORTES:
            abiertas = suc[suc[cota] <= corte]
            locs["km"] = distancia_minima(locs, abiertas)
            for peso, nombre in (("pobtot", "total"), ("pob65_mas", "65 y más")):
                cortes = [("nacional", "todas", locs)]
                cortes += [("marginacion", g, d) for g, d in locs.groupby("marginacion")]
                cortes += [("tamano", g, d) for g, d in locs.groupby("tamano")]
                for tipo, grupo, d in cortes:
                    filas.append(
                        {
                            "cota": cota,
                            "corte": corte,
                            "sucursales_localidades": len(abiertas),
                            "poblacion_tipo": nombre,
                            "grupo_tipo": tipo,
                            "grupo": grupo,
                            **_resumen(d, peso),
                        }
                    )
    return pd.DataFrame(filas)


def generar() -> Path:
    tabla = accesibilidad()
    TABLAS.mkdir(parents=True, exist_ok=True)
    ruta = TABLAS / SALIDA
    tabla.round(3).to_csv(ruta, index=False)
    nac = tabla[(tabla["grupo_tipo"] == "nacional") & (tabla["poblacion_tipo"] == "65 y más")][
        ["cota", "corte", "km_media", "pct_a_5km", "pct_a_10km"]
    ]
    log.info("accesibilidad de los 65+:\n%s", nac.round(1).to_string(index=False))
    return ruta


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

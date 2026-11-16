"""Tratamiento a nivel localidad: qué localidad recibió sucursal del Banco del Bienestar y cuándo.

El problema: la BDIF fecha las aperturas a nivel **municipio**, y el directorio del Banco del
Bienestar georreferencia las sucursales pero **no trae fecha**. La combinación las identifica:

1. Cada sucursal del directorio se asigna a la localidad del ITER 2020 más cercana **dentro del
   mismo municipio** (las localidades del ITER son puntos, no polígonos; la cabecera suele quedar
   a pocos cientos de metros).
2. La fecha de apertura sale de `sucursales_bienestar.parquet` (serie municipal neta de
   Banjército, ver `docs/data_audit.md` P2):
   - municipio con **una sola** sucursal en el directorio (1,270 de 1,482 cohortes): la fecha
     municipal es, sin ambigüedad, la de esa localidad;
   - municipio con **2 o más**: la primera apertura municipal se asigna a la localidad de mayor
     población y se marca `fecha_ambigua = True`; las demás localidades reciben las aperturas
     posteriores en orden de población, también marcadas. Salen de la especificación principal.

Salida `data/interim/tratamiento_localidad.parquet`, una fila por localidad con sucursal:
`cve_loc, cve_mun, nom_loc, pobtot, lat, lon, n_sucursales_loc, n_sucursales_mun, G_trimestre,
G_semestre, g_s, fecha_ambigua, sospechoso_banjercito, dist_sucursal_km`.

`dist_sucursal_km` es la distancia entre la sucursal y el punto de la localidad asignada: sirve
para detectar asignaciones dudosas (sucursales lejos de cualquier localidad censada).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.utils.io import INTERIM, parametros
from proyecto.utils.periodos import periodo_a_semestre, semestre_a_s

log = logging.getLogger(__name__)

SALIDA = INTERIM / "tratamiento_localidad.parquet"
RADIO_TIERRA_KM = 6371.0


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia en km entre pares de coordenadas en grados (vectorizada)."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * RADIO_TIERRA_KM * np.arcsin(np.sqrt(a))


def asignar_localidad(sucursales: pd.DataFrame, localidades: pd.DataFrame) -> pd.DataFrame:
    """Para cada sucursal, la localidad más cercana dentro de su propio municipio."""
    locs = {
        cve: g[["cve_loc", "lat", "lon", "pobtot", "nom_loc"]].to_numpy(dtype=object)
        for cve, g in localidades.groupby("cve_mun")
    }
    filas = []
    for r in sucursales.itertuples():
        candidatas = locs.get(r.cve_mun_espacial)
        if candidatas is None:
            filas.append((r.id_sucursal, r.cve_mun_espacial, None, None, np.nan))
            continue
        lat = candidatas[:, 1].astype(float)
        lon = candidatas[:, 2].astype(float)
        d = haversine_km(r.latitud, r.longitud, lat, lon)
        k = int(np.argmin(d))
        filas.append(
            (r.id_sucursal, r.cve_mun_espacial, candidatas[k, 0], candidatas[k, 4], float(d[k]))
        )
    return pd.DataFrame(
        filas, columns=["id_sucursal", "cve_mun", "cve_loc", "nom_loc", "dist_sucursal_km"]
    )


def construir() -> Path:
    p = parametros()
    localidades = pd.read_parquet(INTERIM / "inegi_censo_localidades_2020.parquet")
    sucursales = pd.read_parquet(INTERIM / "babien.parquet")
    sucursales = sucursales[sucursales["cve_mun_espacial"].notna() & ~sucursales["sin_coordenadas"]]

    asignadas = asignar_localidad(sucursales, localidades)
    asignadas = asignadas[asignadas["cve_loc"].notna()]

    # Sucursales por localidad y por municipio.
    por_loc = asignadas.groupby(["cve_mun", "cve_loc", "nom_loc"], as_index=False).agg(
        n_sucursales_loc=("id_sucursal", "size"), dist_sucursal_km=("dist_sucursal_km", "max")
    )
    por_loc["n_sucursales_mun"] = por_loc.groupby("cve_mun")["n_sucursales_loc"].transform("sum")

    # Fechas municipales de apertura (serie neta de Banjército).
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    inicio, fin = p["periodo"]["inicio"], p["periodo"]["fin"]
    ventana = sb[(sb["periodo"] >= inicio) & (sb["periodo"] <= fin)]
    piv = ventana.pivot(index="cve_mun", columns="periodo", values="suc_bienestar")
    tratado = piv.fillna(0) >= p["tratamiento"]["umbral"]
    primer = tratado.idxmax(axis=1).where(tratado.any(axis=1))
    ya_tratado = tratado[inicio]
    sospechoso = sb.groupby("cve_mun")["sospechoso_banjercito_nuevo"].first()

    por_loc = por_loc.merge(
        pd.DataFrame(
            {
                "G_trimestre": primer,
                "ya_tratado_inicio": ya_tratado,
                "sospechoso_banjercito": sospechoso,
            }
        ),
        left_on="cve_mun",
        right_index=True,
        how="left",
    )

    # Localidades de un municipio con varias sucursales: orden por población para repartir las
    # aperturas; la mayor se queda con la primera fecha. Todas quedan marcadas como ambiguas.
    pob = localidades.set_index("cve_loc")["pobtot"]
    por_loc["pobtot"] = por_loc["cve_loc"].map(pob)
    por_loc = por_loc.sort_values(["cve_mun", "pobtot"], ascending=[True, False])
    por_loc["orden_en_municipio"] = por_loc.groupby("cve_mun").cumcount()
    por_loc["fecha_ambigua"] = por_loc["n_sucursales_mun"] > 1
    # Las localidades secundarias no tienen fecha propia observable: se dejan sin G.
    por_loc.loc[por_loc["orden_en_municipio"] > 0, "G_trimestre"] = pd.NA

    por_loc["G_semestre"] = por_loc["G_trimestre"].map(
        lambda q: periodo_a_semestre(q) if isinstance(q, str) else pd.NA
    )
    por_loc["g_s"] = por_loc["G_semestre"].map(
        lambda sem: semestre_a_s(sem) if isinstance(sem, str) else 0
    )
    por_loc = por_loc.merge(localidades[["cve_loc", "lat", "lon"]], on="cve_loc", how="left").drop(
        columns="orden_en_municipio"
    )

    por_loc.to_parquet(SALIDA, index=False)
    log.info(
        "tratamiento_localidad: %d localidades con sucursal en %d municipios; "
        "%d con fecha propia (no ambigua), %d ambiguas, %d ya tratadas al inicio, %d sospechosas de Banjército; "
        "distancia sucursal-localidad: mediana %.2f km, p95 %.2f km, máx %.1f km",
        len(por_loc),
        por_loc["cve_mun"].nunique(),
        int((~por_loc["fecha_ambigua"] & por_loc["G_trimestre"].notna()).sum()),
        int(por_loc["fecha_ambigua"].sum()),
        int(por_loc["ya_tratado_inicio"].fillna(False).sum()),
        int(por_loc["sospechoso_banjercito"].fillna(False).sum()),
        por_loc["dist_sucursal_km"].median(),
        por_loc["dist_sucursal_km"].quantile(0.95),
        por_loc["dist_sucursal_km"].max(),
    )
    return SALIDA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    construir()

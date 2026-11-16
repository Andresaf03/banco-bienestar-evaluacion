"""Distancia del centroide de cada municipio al municipio más cercano con banca múltiple en 2019T1.

Fase 4 (preregistro 2026-10-14): covariable previa de H2 y moderador continuo de E1.

Entradas: polígonos del MG 2024 disueltos por municipio estable (`variables.vecinos`), en EPSG:6372
(proyección métrica), y `banca_mun_2019` de `panel_municipio_trim` (1 si el municipio tenía una
sucursal de banca múltiple en `periodo.inicio`, BDIF).

Salida: `data/interim/distancia_bm.parquet` con `cve_mun, dist_bm_km, cve_mun_bm_mas_cercano`.
- Municipios **con** banca múltiple en 2019T1: distancia 0 (y ellos mismos como el más cercano).
- Los demás: distancia euclidiana, en km, entre su centroide y el del municipio con banca múltiple
  más cercano. No hay coordenadas de las sucursales de banca múltiple en la BDIF; la de centroides
  es la aproximación disponible.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from proyecto.utils.io import INTERIM, PROCESSED
from proyecto.variables.vecinos import poligonos_estables

log = logging.getLogger(__name__)

SALIDA = INTERIM / "distancia_bm.parquet"
CRS_METRICO = 6372


def distancia_a_banca(centroides: pd.DataFrame, con_banca: pd.Series) -> pd.DataFrame:
    """`centroides`: `cve_mun, x, y` en metros; `con_banca`: booleano indexado por `cve_mun`."""
    c = centroides.assign(banca=centroides["cve_mun"].map(con_banca).fillna(False).astype(bool))
    destinos = c[c["banca"]].reset_index(drop=True)
    if destinos.empty:
        raise ValueError("ningún municipio con banca múltiple: no hay a qué medir la distancia")
    nn = NearestNeighbors(n_neighbors=1).fit(destinos[["x", "y"]].to_numpy())
    dist, idx = nn.kneighbors(c[["x", "y"]].to_numpy())
    salida = pd.DataFrame(
        {
            "cve_mun": c["cve_mun"],
            "dist_bm_km": np.where(c["banca"], 0.0, dist[:, 0] / 1000),
            "cve_mun_bm_mas_cercano": np.where(
                c["banca"], c["cve_mun"], destinos["cve_mun"].to_numpy()[idx[:, 0]]
            ),
        }
    )
    return salida.reset_index(drop=True)


def calcular() -> Path:
    g = poligonos_estables().to_crs(CRS_METRICO)
    centro = g.geometry.centroid
    centroides = pd.DataFrame({"cve_mun": g["cve_mun"], "x": centro.x, "y": centro.y})
    panel = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "banca_mun_2019"]
    ).drop_duplicates("cve_mun")
    con_banca = panel.set_index("cve_mun")["banca_mun_2019"].astype(bool)
    salida = distancia_a_banca(centroides, con_banca)
    log.info(
        "distancia a la banca múltiple 2019T1: %d municipios; sin banca: mediana %.1f km, p90 %.1f km",
        len(salida),
        salida.loc[salida["dist_bm_km"] > 0, "dist_bm_km"].median(),
        salida.loc[salida["dist_bm_km"] > 0, "dist_bm_km"].quantile(0.9),
    )
    salida.to_parquet(SALIDA, index=False, compression="zstd")
    return SALIDA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    calcular()

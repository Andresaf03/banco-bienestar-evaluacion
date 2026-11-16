"""Contigüidad municipal y fecha de la primera apertura vecina (fase 4, preregistro 2026-10-14).

Entradas: polígonos `00mun.shp` (MG 2024, `limpieza.municipios.poligonos_2024`), colapsados por
municipio estable (P-7: los municipios creados después de 2010 se disuelven en su padre), y el
`G_trimestre` de `panel_municipio_trim`.

Salidas:
- `data/interim/vecinos.parquet`: pares `(cve_mun, cve_mun_vecino)` con contigüidad tipo *queen*
  (comparten al menos un punto de frontera), simétricos y sin el propio municipio.
- `vecino_de_tratado()`: por municipio, el primer trimestre en que abre una sucursal **nueva**
  (después del inicio del panel) en algún vecino, y si tiene un vecino con sucursal heredada.

Uso: derrames (A1), controles sin vecino tratado (H1e) y traslado de cuentas (B2).
"""

from __future__ import annotations

import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

from proyecto.construccion.panel import P, mapa_crosswalk
from proyecto.limpieza.municipios import poligonos_2024
from proyecto.utils.io import INTERIM

log = logging.getLogger(__name__)

SALIDA = INTERIM / "vecinos.parquet"


def poligonos_estables() -> gpd.GeoDataFrame:
    """Polígonos del MG 2024 disueltos por municipio estable (P-7)."""
    g = poligonos_2024()
    g["cve_mun"] = g["cve_mun"].map(mapa_crosswalk()).fillna(g["cve_mun"])
    return g.dissolve(by="cve_mun", as_index=False)[["cve_mun", "geometry"]]


def pares_contiguos(g: gpd.GeoDataFrame) -> pd.DataFrame:
    """Pares de municipios que comparten frontera (queen), simétricos y sin autopares.

    `intersects` y no `touches`: con fronteras digitalizadas por separado, dos polígonos vecinos
    pueden traslaparse por centímetros y `touches` los dejaría fuera.
    """
    pares = gpd.sjoin(g, g, how="inner", predicate="intersects", lsuffix="a", rsuffix="b")
    pares = pares[pares["cve_mun_a"] != pares["cve_mun_b"]]
    pares = pares.rename(columns={"cve_mun_a": "cve_mun", "cve_mun_b": "cve_mun_vecino"})
    pares = pares[["cve_mun", "cve_mun_vecino"]].drop_duplicates()
    return pares.sort_values(["cve_mun", "cve_mun_vecino"]).reset_index(drop=True)


def contiguidad() -> Path:
    g = poligonos_estables()
    pares = pares_contiguos(g)
    sin_vecinos = sorted(set(g["cve_mun"]) - set(pares["cve_mun"]))
    log.info(
        "contigüidad: %d municipios, %d pares; sin vecinos: %s",
        g["cve_mun"].nunique(),
        len(pares),
        ", ".join(sin_vecinos) or "ninguno",
    )
    pares.to_parquet(SALIDA, index=False, compression="zstd")
    return SALIDA


def vecino_de_tratado(
    g_trimestre: pd.Series, inicio: str | None = None, pares: pd.DataFrame | None = None
) -> pd.DataFrame:
    """Primera apertura **nueva** entre los vecinos de cada municipio.

    `g_trimestre`: serie indexada por `cve_mun` con el periodo (`YYYYQn`) de la primera sucursal
    del Banco del Bienestar (NaN si nunca abre). Las aperturas en o antes de `inicio` (2019T1) son
    sucursales heredadas.

    Devuelve, por `cve_mun`: `G_trimestre_vecino` (primer trimestre con apertura nueva en un
    vecino; NaN si no hay), `vecino_heredado` (algún vecino con sucursal heredada) y `n_vecinos`.
    """
    inicio = inicio or P["periodo"]["inicio"]
    pares = (pd.read_parquet(SALIDA) if pares is None else pares).copy()
    pares["g_vecino"] = pares["cve_mun_vecino"].map(g_trimestre)
    nueva = pares["g_vecino"].notna() & (pares["g_vecino"] > inicio)
    heredada = pares["g_vecino"].notna() & (pares["g_vecino"] <= inicio)
    salida = pd.DataFrame(
        {
            "G_trimestre_vecino": pares[nueva].groupby("cve_mun")["g_vecino"].min(),
            "vecino_heredado": heredada.groupby(pares["cve_mun"]).any(),
            "n_vecinos": pares.groupby("cve_mun").size(),
        }
    )
    salida["vecino_heredado"] = salida["vecino_heredado"].fillna(False).astype(bool)
    return salida.rename_axis("cve_mun").reset_index()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    contiguidad()

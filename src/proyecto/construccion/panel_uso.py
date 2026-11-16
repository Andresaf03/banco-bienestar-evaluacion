"""Panel de la fase 5 (exploratoria, no preregistrada): ¿se usan las cuentas del banco?

La fase 4 mostró que el banco abre cuentas y emite tarjetas donde llega. Esta fase pregunta qué
tipo de cuentas son y si vienen con crédito. Módulo aparte para no tocar los paneles anteriores.

Parte de `panel_municipio_trim_f4` (mismas unidades, tratamiento, banderas, covariables y series
del Banco del Bienestar del Portafolio) y le agrega, desde 2022T4, las series de la **banca de
desarrollo** de la BDIF. En la BDIF la banca de desarrollo es el Banco del Bienestar más Banjército
(adenda de la fase 4), así que `con_banjercito` marca los municipios donde Banjército tuvo sucursal:
fuera de ellos, la banca de desarrollo es solo el banco.

| columna | qué es |
|---|---|
| `capt_n1_bd` … `capt_n4_bd` | contratos de captación por nivel de cuenta (N1 y N2: bajo monto) |
| `capt_total_bd`, `cred_total_bd` | contratos de captación y de crédito |
| `capt_ahorro_bd`, `capt_plazo_bd` | contratos de cuentas de ahorro y de depósitos a plazo |
| `cuentas_celular_bd` | cuentas asociadas a un celular (banca móvil) |
| `transacciones_cajeros_bd` | transacciones en los cajeros de la banca de desarrollo |
| `cred_personal_bd`, `cred_nomina_bd`, `cred_grupal_bd` | crédito por tipo (los que el banco ofrece) |
| `tarjetas_credito_bd` | tarjetas de crédito |
| `*_pc` | por diez mil adultos, con el denominador fijo de 2022T4 |
| `con_banjercito` | Banjército tuvo sucursal en el municipio (2016–2026) |

Uso:
    uv run python -m proyecto.construccion.panel_uso
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import P, mapa_crosswalk
from proyecto.construccion.panel_fase4 import _bdif, _con_ceros
from proyecto.utils.io import INTERIM, PROCESSED

log = logging.getLogger(__name__)

SALIDA = PROCESSED / "panel_municipio_uso.parquet"
BASE = PROCESSED / "panel_municipio_trim_f4.parquet"

# (columna nueva, variable de la BDIF), todas del sector banca de desarrollo.
SERIES_BD = [
    ("capt_n1_bd", "capt_n1"),
    ("capt_n2_bd", "capt_n2"),
    ("capt_n3_bd", "capt_n3"),
    ("capt_n4_bd", "capt_n4"),
    ("capt_ahorro_bd", "capt_ahorro"),
    ("capt_plazo_bd", "capt_plazo"),
    ("cuentas_celular_bd", "cuentas_celular"),
    ("transacciones_cajeros_bd", "transacciones_cajeros"),
    ("cred_total_bd", "cred_total"),
    ("cred_personal_bd", "cred_personal"),
    ("cred_nomina_bd", "cred_nomina"),
    ("cred_grupal_bd", "cred_grupal"),
    ("tarjetas_credito_bd", "tarjetas_credito"),
]
INSTITUCION_BANJERCITO = "037019"
TIPO_SUCURSALES = "31"


def municipios_con_banjercito() -> set[str]:
    """Claves estables con alguna sucursal de Banjército: Portafolio operativo 2016–2021
    (`sucursales_bienestar`) y modelo Power Pivot 2022–2026."""
    sb = pd.read_parquet(
        INTERIM / "sucursales_bienestar.parquet", columns=["cve_mun", "suc_banjercito"]
    )
    cruce = mapa_crosswalk()
    con_bj = sb.loc[sb["suc_banjercito"].fillna(0) > 0, "cve_mun"]
    con = set(con_bj.map(cruce).fillna(con_bj))
    modelo = pd.read_parquet(
        INTERIM / "cnbv_portafolio_modelo.parquet",
        columns=["cve_mun", "institucion", "tipo", "valor"],
    )
    bj = modelo[
        (modelo["institucion"] == INSTITUCION_BANJERCITO)
        & (modelo["tipo"].astype(str) == TIPO_SUCURSALES)
        & (modelo["valor"] > 0)
    ]
    con |= set(bj["cve_mun"].map(cruce).fillna(bj["cve_mun"]))
    return con


def panel_municipio_uso() -> Path:
    if not BASE.exists():
        raise FileNotFoundError(f"falta {BASE}: corre `make panel-fase4` primero")
    panel = pd.read_parquet(BASE)
    for nombre, variable in SERIES_BD:
        panel = _con_ceros(panel, _bdif(variable, ["banca_desarrollo"], nombre), nombre)
    por_cada = P["resultados"]["por_cada_municipio"]
    base = panel["poblacion_adulta_fija"].replace(0, np.nan)
    for nombre, _ in SERIES_BD:
        panel[f"{nombre}_pc"] = panel[nombre] / base * por_cada
    con = municipios_con_banjercito()
    panel["con_banjercito"] = panel["cve_mun"].isin(con)
    panel = panel.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    panel.to_parquet(SALIDA, index=False, compression="zstd")
    log.info(
        "panel de uso: %d municipios × %d trimestres; %d con Banjército -> %s",
        panel["cve_mun"].nunique(),
        panel["t"].nunique(),
        len(con),
        SALIDA,
    )
    return SALIDA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    panel_municipio_uso()

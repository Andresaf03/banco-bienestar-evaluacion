"""Serie municipal de sucursales del Banco del Bienestar sin Banjército (insumo del tratamiento).

La BDIF municipal suma Banco del Bienestar + Banjército en "banca de desarrollo". El Portafolio
de Información de la CNBV (`cnbv_portafolio_operativa.parquet`) separa ambas instituciones por
municipio de 2016-01 a 2021-12. Esta tabla combina las dos fuentes para cada
municipio-trimestre 2016T1–2025T4:

- `suc_bd_bdif`: sucursales de banca de desarrollo según la BDIF (observado).
- `suc_banjercito`: sucursales de Banjército. Observado en los meses de cierre de trimestre que
  publica el Portafolio (2016T1–2021T4). Fuera de esa ventana se **extrapola** la red observada más
  cercana (la de 2021-12 hacia adelante, 2022T1+), acotada por `suc_bd_bdif`. Supuesto: la red de
  Banjército es estable (65 municipios en 2016-01, 75 en 2021-12; 91–95 sucursales nacionales en
  2023–2025 según `BD Banca`).
- `suc_bienestar`: `max(suc_bd_bdif - suc_banjercito, 0)`. Es la serie que debe definir G.
- `fuente_banjercito`: "portafolio" (observado) | "extrapolado_2021-12" (2022T1+).
- `sospechoso_banjercito_nuevo`: True si el municipio entra al tratamiento después de 2021T4 y el
  directorio del Banco del Bienestar (2026) no tiene sucursal ahí o tiene menos que
  `suc_bienestar` en 2025T4: candidatos a sucursal nueva de Banjército (83 → 95 sucursales
  nacionales entre 2021 y 2025) que la extrapolación no captura.

Salida: `data/interim/sucursales_bienestar.parquet`.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from proyecto.utils.io import INTERIM
from proyecto.utils.periodos import yyyymm_a_periodo

log = logging.getLogger(__name__)

SALIDA = INTERIM / "sucursales_bienestar.parquet"


def limpiar() -> Path:
    bdif = pd.read_parquet(
        INTERIM / "cnbv_bdif.parquet",
        columns=["cve_mun", "periodo", "t", "sector", "variable", "valor"],
    )
    bd = bdif[(bdif["variable"] == "sucursales") & (bdif["sector"] == "banca_desarrollo")]
    bd = bd[["cve_mun", "periodo", "t", "valor"]].rename(columns={"valor": "suc_bd_bdif"})

    op = pd.read_parquet(INTERIM / "cnbv_portafolio_operativa.parquet")
    banj = op[(op["producto"] == "Número de Sucursales") & (op["institucion"] == "Banjército")]
    banj_mes = banj.groupby(["cve_mun", "yyyymm"])["valor"].sum()
    banj_trim = (
        banj[banj["periodo"].notna()]
        .groupby(["cve_mun", "periodo"])["valor"]
        .sum()
        .rename("suc_banjercito_obs")
    )
    # Ventana observada: del primer al último mes de cierre de trimestre con datos del Portafolio.
    meses_cierre = sorted(m for m in banj["yyyymm"].unique() if m[4:] in ("03", "06", "09", "12"))
    mes_inicio, mes_fin = meses_cierre[0], meses_cierre[-1]
    red_ini = banj_mes.xs(mes_inicio, level="yyyymm").rename("banj_ini")
    red_fin = banj_mes.xs(mes_fin, level="yyyymm").rename("banj_fin")

    df = bd.merge(banj_trim.reset_index(), on=["cve_mun", "periodo"], how="left")
    df = df.merge(red_ini.reset_index(), on="cve_mun", how="left").merge(
        red_fin.reset_index(), on="cve_mun", how="left"
    )
    df[["banj_ini", "banj_fin"]] = df[["banj_ini", "banj_fin"]].fillna(0)
    per_ini, per_fin = yyyymm_a_periodo(mes_inicio), yyyymm_a_periodo(mes_fin)
    df["suc_banjercito"] = df["suc_banjercito_obs"].fillna(0)
    df["fuente_banjercito"] = "portafolio"
    antes = df["periodo"] < per_ini
    despues = df["periodo"] > per_fin
    df.loc[antes, "suc_banjercito"] = df.loc[antes, "banj_ini"]
    df.loc[antes, "fuente_banjercito"] = f"extrapolado_{mes_inicio[:4]}-{mes_inicio[4:]}"
    df.loc[despues, "suc_banjercito"] = df.loc[despues, "banj_fin"]
    df.loc[despues, "fuente_banjercito"] = f"extrapolado_{mes_fin[:4]}-{mes_fin[4:]}"
    # La extrapolación no puede exceder lo observado en la BDIF.
    df["suc_banjercito"] = df[["suc_banjercito", "suc_bd_bdif"]].min(axis=1)
    df["suc_bienestar"] = (df["suc_bd_bdif"] - df["suc_banjercito"]).clip(lower=0)

    # Sospechosos: entran después de 2021T4 y el directorio 2026 no respalda la sucursal.
    babien = (
        pd.read_parquet(INTERIM / "babien.parquet")
        .groupby("cve_mun_espacial")
        .size()
        .rename("n_babien")
    )
    piv = df.pivot(index="cve_mun", columns="periodo", values="suc_bienestar")
    tr = piv.fillna(0) >= 1
    primera = tr.idxmax(axis=1).where(tr.any(axis=1))
    # Se compara la serie ya neta de Banjército (2021-12) contra el directorio 2026: un exceso
    # residual o la ausencia total en el directorio apuntan a una sucursal nueva de Banjército.
    ult = df[df["periodo"] == df["periodo"].max()].set_index("cve_mun")["suc_bienestar"]
    chk = (
        pd.DataFrame({"G_periodo": primera, "bienestar_ult": ult})
        .join(babien, how="left")
        .fillna({"n_babien": 0})
    )
    sospechoso = (chk["G_periodo"] > per_fin) & (
        (chk["n_babien"] == 0) | (chk["bienestar_ult"] > chk["n_babien"])
    )
    df = df.merge(
        sospechoso.rename("sospechoso_banjercito_nuevo").reset_index(), on="cve_mun", how="left"
    )
    df["sospechoso_banjercito_nuevo"] = df["sospechoso_banjercito_nuevo"].fillna(False).astype(bool)

    df = df[
        [
            "cve_mun",
            "periodo",
            "t",
            "suc_bd_bdif",
            "suc_banjercito",
            "suc_bienestar",
            "fuente_banjercito",
            "sospechoso_banjercito_nuevo",
        ]
    ]
    df = df.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    df.to_parquet(SALIDA, index=False)
    log.info(
        "sucursales_bienestar: %d filas; %d municipios con Banjército extrapolado; %d sospechosos de Banjército nuevo",
        len(df),
        int((df.groupby("cve_mun")["suc_banjercito"].max() > 0).sum()),
        int(df.groupby("cve_mun")["sospechoso_banjercito_nuevo"].first().sum()),
    )
    return SALIDA

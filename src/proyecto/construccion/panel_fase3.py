"""Paneles de la fase 3 (preregistro en `docs/decisiones.md`, 2026-10-11).

Módulo aparte para no tocar `panel.py` ni `panel_fase2.py`: reutiliza sus funciones y escribe
paneles nuevos en `data/processed/` con la estructura de siempre (`id, t, G, banderas, resultados,
covariables`), para que `analisis/11_fase3.R` los lea con `leer_panel()`.

| panel | unidad | periodos | tratamiento |
|---|---|---|---|
| `panel_municipio_delitos` | municipio | 2019T1–2025T4 | G de `panel_municipio_trim` |
| `panel_municipio_delitos_largo` | municipio | 2016T1–2025T4 (se estima desde 2017T1) | G de `panel_municipio_trim_largo` |
| `panel_municipio_delitos_obs` | municipio | 2019T1–2025T4 | G observado (fase 2, P-8) |
| `panel_municipio_elecciones` | municipio | 2015, 2018, 2021, 2024 | una cohorte, G = 4 |
| `panel_municipio_elecciones_todos` | municipio | ídem, sin el filtro de lista nominal | ídem |
| `panel_municipio_elecciones_obs` | municipio | ídem | G observado |

Elecciones: las aperturas fuera de la ventana entre elecciones se marcan en `apertura_posterior_ce`
(la columna que `leer_panel()` ya filtra) y la dosis en `exposicion_ce`, como la EIC de la fase 2.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import P, _agregar_tamano_cohorte, _tratamiento_trimestral
from proyecto.construccion.panel_fase2 import _covariables_municipales
from proyecto.utils.io import INTERIM, PROCESSED

log = logging.getLogger(__name__)

F3 = P["fase3"]
SALIDAS = {
    "municipio_delitos": PROCESSED / "panel_municipio_delitos.parquet",
    "municipio_delitos_largo": PROCESSED / "panel_municipio_delitos_largo.parquet",
    "municipio_delitos_obs": PROCESSED / "panel_municipio_delitos_obs.parquet",
    "municipio_elecciones": PROCESSED / "panel_municipio_elecciones.parquet",
    "municipio_elecciones_todos": PROCESSED / "panel_municipio_elecciones_todos.parquet",
    "municipio_elecciones_obs": PROCESSED / "panel_municipio_elecciones_obs.parquet",
}
# Columnas del panel trimestral que viajan al panel de delitos (tratamiento, banderas, covariables).
BASE_TRIM = [
    "cve_mun",
    "periodo",
    "t",
    "G_trimestre",
    "G",
    "tratado",
    "ya_tratado_inicio",
    "sospechoso_banjercito",
    "indice_marginacion_2020",
    "grado_marginacion_2020",
    "poblacion_2020",
    "log_poblacion_2020",
    "banca_mun_2019",
    "desierto_bancario",
]
# Cambio de lista nominal entre elecciones consecutivas, respecto de la mediana de su estado, a
# partir del cual el municipio se considera con geografía electoral inestable (adenda del
# 2026-10-11, fijada con la lista nominal y antes de estimar).
SALTO_LISTA_NOMINAL = 0.25


def _guardar_fase3(panel: pd.DataFrame, nombre: str, id_col: str) -> Path:
    """Como `panel_fase2._guardar`, con las rutas de la fase 3."""
    panel = _agregar_tamano_cohorte(panel, id_col)
    panel = panel.sort_values([id_col, "t"]).reset_index(drop=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(SALIDAS[nombre], index=False, compression="zstd")
    unidades = panel.drop_duplicates(id_col)
    log.info(
        "panel %s: %d filas, %d unidades × %d periodos; G > 0 %d, G = 0 %d",
        nombre,
        len(panel),
        len(unidades),
        panel["t"].nunique(),
        int((unidades["G"] > 0).sum()),
        int((unidades["G"] == 0).sum()),
    )
    return SALIDAS[nombre]


# --------------------------------------------------------------------------- A. delitos
def tasas_delitos(panel: pd.DataFrame, por: float) -> pd.DataFrame:
    """`delitos_<x>` -> `tasa_<x>` por `por` habitantes con la población fija del Censo 2020."""
    base = panel["pobtot"].where(panel["pobtot"] > 0)
    nuevas = {
        "tasa_" + c.removeprefix("delitos_"): por * panel[c] / base
        for c in panel.columns
        if c.startswith("delitos_")
    }
    return panel.assign(**nuevas)


def panel_delitos(base: str, nombre: str) -> Path:
    """El panel trimestral `base` (mismo G, banderas y covariables) con los delitos del SESNSP."""
    cfg = F3["delitos"]
    trim = pd.read_parquet(PROCESSED / f"{base}.parquet")
    trim = trim[[c for c in BASE_TRIM if c in trim.columns]]
    delitos = pd.read_parquet(INTERIM / "sesnsp_municipio_trim.parquet")
    panel = trim.merge(delitos, on=["cve_mun", "periodo"], how="left")
    panel["pobtot"] = panel["poblacion_2020"]
    panel = tasas_delitos(panel, cfg["por_habitantes"])
    # Municipio de registro ≠ de ocurrencia: robustez solo con municipios con algún robo en 2019.
    robos_2019 = (
        panel[panel["periodo"].str.startswith("2019")]
        .groupby("cve_mun")["delitos_robo_total"]
        .sum()
    )
    panel["con_registro_2019"] = panel["cve_mun"].map(robos_2019.gt(0)).fillna(False)
    return _guardar_fase3(panel, nombre, "cve_mun")


# --------------------------------------------------------------------------- B. elecciones
def cohorte_electoral(g_trimestre: pd.Series, cfg: dict, inicio_panel: str) -> pd.DataFrame:
    """G (4 o 0), exclusión por exposición y dosis a partir del primer trimestre con sucursal.

    - Tratada: primera sucursal entre `inicio_tratamiento` y `fin_tratamiento` (entre la elección
      de 2021 y la de 2024) -> G = 4.
    - Fuera por exposición (`apertura_posterior_ce`): aperturas después de `inicio_panel` y antes
      de `inicio_tratamiento` (expuestas en una elección previa) y los trimestres ambiguos.
    - Control: sin sucursal o con la primera después de la elección de 2024.
    """
    ini, fin = cfg["inicio_tratamiento"], cfg["fin_tratamiento"]
    tratada = g_trimestre.between(ini, fin)
    previa = g_trimestre.gt(inicio_panel) & g_trimestre.lt(ini)
    ambigua = g_trimestre.isin(cfg["trimestres_ambiguos"])
    exposicion = np.select(
        [~tratada, g_trimestre.le(cfg["fin_exposicion_temprana"])],
        ["control", "temprana"],
        "tardía",
    )
    return pd.DataFrame(
        {
            "G": np.where(tratada, len(cfg["anios"]), 0).astype(int),
            "apertura_posterior_ce": (previa | ambigua).fillna(False).astype(bool).to_numpy(),
            "exposicion_ce": exposicion,
        },
        index=g_trimestre.index,
    )


def porcentajes_electorales(e: pd.DataFrame) -> pd.DataFrame:
    """Participación, bloque, Morena y nulos (%) desde los conteos municipales."""
    validos = e["votos_validos"].where(e["votos_validos"] > 0)
    return e.assign(
        pct_participacion=100 * e["total_votos"] / e["lista_nominal"].where(e["lista_nominal"] > 0),
        pct_bloque_gobierno=100 * e["votos_bloque"] / validos,
        pct_morena=100 * e["votos_morena"] / validos,
        pct_nulos=100 * e["votos_nulos"] / e["total_votos"].where(e["total_votos"] > 0),
    )


def geografia_inestable(e: pd.DataFrame, umbral: float = SALTO_LISTA_NOMINAL) -> pd.Series:
    """Municipios cuya lista nominal cambia entre elecciones consecutivas más de `umbral` (en log)
    respecto de la mediana de su estado: secciones que el INE asignó a otro municipio en alguna
    elección (en 2015 aún no separaba varios municipios) o casillas no instaladas."""
    ln = e.pivot_table(index="cve_mun", columns="anio", values="lista_nominal", aggfunc="sum")
    cambio = np.log(ln).diff(axis=1).iloc[:, 1:]
    mediana = cambio.groupby(ln.index.str[:2]).transform("median")
    return (cambio - mediana).abs().gt(np.log1p(umbral)).any(axis=1)


def _netos_y_niveles(panel: pd.DataFrame, resultados: list[str]) -> pd.DataFrame:
    """`<r>_neto` (menos la media estado × elección) y `<r>_2015` (nivel previo como covariable)."""
    cve_ent = panel["cve_mun"].str[:2]
    nuevas = {}
    for r in resultados:
        nuevas[f"{r}_neto"] = panel[r] - panel.groupby([cve_ent, "anio"])[r].transform("mean")
        nivel = panel.loc[panel["anio"] == F3["elecciones"]["anios"][0]].set_index("cve_mun")[r]
        nuevas[f"{r}_2015"] = panel["cve_mun"].map(nivel)
    return panel.assign(**nuevas, cve_ent=cve_ent)


def panel_elecciones(
    nombre: str, serie: str = "sucursales_bienestar", filtrar: bool = True
) -> Path:
    cfg = F3["elecciones"]
    anios = cfg["anios"]
    e = porcentajes_electorales(pd.read_parquet(INTERIM / "ine_diputados_municipio.parquet"))
    completos = e.groupby("cve_mun")["anio"].nunique().eq(len(anios))
    e = e[e["cve_mun"].isin(completos[completos].index)]
    inestable = geografia_inestable(e)
    log.info(
        "elecciones: %d municipios en las 4 elecciones (%d sin alguna); %d con geografía inestable",
        int(completos.sum()),
        int((~completos).sum()),
        int(inestable.sum()),
    )
    if filtrar:
        e = e[~e["cve_mun"].isin(inestable[inestable].index)]
    panel = e.assign(t=e["anio"].map({a: i for i, a in enumerate(anios, start=1)}))

    sb = pd.read_parquet(INTERIM / f"{serie}.parquet")
    if serie == "sucursales_bienestar_obs":
        sb = sb.assign(suc_bienestar=sb["suc_bienestar_obs"], sospechoso_banjercito_nuevo=False)
    primer, ya, sospechoso = _tratamiento_trimestral(sb, P["periodo"]["fin_trimestral"])
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    cohorte = cohorte_electoral(panel["G_trimestre"], cfg, P["periodo"]["inicio"])
    panel = panel.assign(**{c: cohorte[c] for c in cohorte.columns})
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)
    panel = _covariables_municipales(panel)
    panel = _netos_y_niveles(panel, cfg["familia_rw"] + cfg["secundarios"])
    u = panel.drop_duplicates("cve_mun")
    muestra = u[~u["ya_tratado_inicio"] & ~u["apertura_posterior_ce"] & ~u["sospechoso_banjercito"]]
    log.info(
        "%s: tratadas %d (temprana %d, tardía %d), controles %d; fuera por exposición %d",
        nombre,
        int((muestra["G"] > 0).sum()),
        int((muestra["exposicion_ce"] == "temprana").sum()),
        int((muestra["exposicion_ce"] == "tardía").sum()),
        int((muestra["G"] == 0).sum()),
        int(u["apertura_posterior_ce"].sum()),
    )
    return _guardar_fase3(panel, nombre, "cve_mun")


def construir_todos() -> dict[str, Path]:
    salidas: dict[str, Path] = {}
    if (INTERIM / "sesnsp_municipio_trim.parquet").exists():
        salidas["municipio_delitos"] = panel_delitos("panel_municipio_trim", "municipio_delitos")
        salidas["municipio_delitos_largo"] = panel_delitos(
            "panel_municipio_trim_largo", "municipio_delitos_largo"
        )
        if (PROCESSED / "panel_municipio_trim_obs.parquet").exists():
            salidas["municipio_delitos_obs"] = panel_delitos(
                "panel_municipio_trim_obs", "municipio_delitos_obs"
            )
    else:
        log.warning("sin sesnsp_municipio_trim.parquet: no se construyen los paneles de delitos")
    if (INTERIM / "ine_diputados_municipio.parquet").exists():
        salidas["municipio_elecciones"] = panel_elecciones("municipio_elecciones")
        salidas["municipio_elecciones_todos"] = panel_elecciones(
            "municipio_elecciones_todos", filtrar=False
        )
        if (INTERIM / "sucursales_bienestar_obs.parquet").exists():
            salidas["municipio_elecciones_obs"] = panel_elecciones(
                "municipio_elecciones_obs", serie="sucursales_bienestar_obs"
            )
    else:
        log.warning("sin ine_diputados_municipio.parquet: no se construyen los paneles electorales")
    return salidas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    construir_todos()

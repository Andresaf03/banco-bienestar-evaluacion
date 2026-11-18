"""Paneles de la fase 6 (preregistro y adenda en `docs/decisiones.md`, 2026-11-17).

Módulo aparte para no tocar `panel.py`, que reproduce la corrida final.

| salida | unidad | qué agrega |
|---|---|---|
| `panel_localidad_f6` | localidad × semestre | `panel_localidad` + establecimientos por sector (C1, C2), la fecha de la primera apertura del municipio (C3) y la proporción de 65+ del municipio (C4) |
| `pub_municipio_f6` | municipio | foto de octubre de 2026 del padrón de Bienestar con tratamiento y covariables (A-foto, B2) |

Sectores (SCIAN a 2 dígitos, bloque `emprendimiento` del DENUE):
- `s46` comercio al por menor; `s72` alimentos y hospedaje; `s81` otros servicios;
  `s3133` manufactura (31, 32 y 33);
- `consumo_amplio` = 46 + 72 + 81; `resto` = todo lo demás (incluye manufactura);
- `sin_52_93` = todos menos servicios financieros (52) y gobierno (93).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import P, _g_efectivo, aplicar_crosswalk, mapa_crosswalk
from proyecto.utils.io import INTERIM, PROCESSED
from proyecto.utils.periodos import periodo_a_t, semestre_a_s

log = logging.getLogger(__name__)

SALIDAS = {
    "localidad_f6": PROCESSED / "panel_localidad_f6.parquet",
    "municipio_pub": PROCESSED / "pub_municipio_f6.parquet",
}
SECTORES: dict[str, tuple[str, ...]] = {
    "s46": ("46",),
    "s72": ("72",),
    "s81": ("81",),
    "s3133": ("31", "32", "33"),
}
CONSUMO_AMPLIO = ("46", "72", "81")
COHORTES_PRINCIPALES = ("2022Q1", "2024Q1")
EXCLUIDOS_C2 = ("52", "93")


def sectores_denue(loc: pd.DataFrame) -> pd.DataFrame:
    """Establecimientos por sector a partir del bloque `emprendimiento` en formato largo.

    `loc` trae `cve_loc, semestre, bloque, clase, n_estab`; la clase del bloque `emprendimiento`
    es el SCIAN a 2 dígitos. Devuelve una fila por `cve_loc × semestre` con `estab_<sector>`.
    """
    emp = loc.loc[loc["bloque"] == "emprendimiento", ["cve_loc", "semestre", "clase", "n_estab"]]
    ancho = emp.pivot_table(
        index=["cve_loc", "semestre"], columns="clase", values="n_estab", aggfunc="sum"
    ).fillna(0)

    def suma(codigos: tuple[str, ...]) -> pd.Series:
        presentes = [c for c in codigos if c in ancho.columns]
        return ancho[presentes].sum(axis=1) if presentes else pd.Series(0.0, index=ancho.index)

    total = ancho.sum(axis=1)
    salida = pd.DataFrame(index=ancho.index)
    for nombre, codigos in SECTORES.items():
        salida[f"estab_{nombre}"] = suma(codigos)
    salida["estab_consumo_amplio"] = suma(CONSUMO_AMPLIO)
    salida["estab_resto"] = total - salida["estab_consumo_amplio"]
    salida["estab_sin_52_93"] = total - suma(EXCLUIDOS_C2)
    salida["estab_total_sectores"] = total
    return salida.reset_index()


def _g_municipal_semestral(periodos: list[str]) -> pd.DataFrame:
    """Semestre efectivo de la primera apertura de cada municipio (clave estable) y si ya tenía."""
    mun = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet",
        columns=["cve_mun", "G_trimestre", "ya_tratado_inicio"],
    ).drop_duplicates("cve_mun")
    semestre = mun["G_trimestre"].map(
        lambda g: f"{g[:4]}S{1 if int(g[-1]) <= 2 else 2}" if isinstance(g, str) else None
    )
    mun["G_mun"] = _g_efectivo(semestre, periodos, semestre_a_s)
    mun["mun_ya_tratado"] = mun["ya_tratado_inicio"].fillna(False).astype(bool)
    return mun[["cve_mun", "G_mun", "mun_ya_tratado"]]


def _censo_municipal() -> pd.DataFrame:
    """Población total y de 65+ del Censo 2020 con la clave estable del crosswalk."""
    censo = pd.read_parquet(
        INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot", "pob65_mas"]
    )
    censo = aplicar_crosswalk(censo, ["pobtot", "pob65_mas"], ["cve_mun"])
    censo["prop_65_mas"] = censo["pob65_mas"] / censo["pobtot"]
    return censo


def panel_localidad_f6() -> Path:
    base = pd.read_parquet(PROCESSED / "panel_localidad.parquet")
    periodos = sorted(base["semestre"].unique())
    loc = pd.read_parquet(
        INTERIM / "denue_localidad.parquet",
        columns=["cve_loc", "semestre", "bloque", "clase", "n_estab"],
    )
    loc = loc[loc["semestre"].isin(periodos) & loc["cve_loc"].isin(base["cve_loc"].unique())]
    sec = sectores_denue(loc)
    panel = base.merge(sec, on=["cve_loc", "semestre"], how="left")
    nuevas = [c for c in sec.columns if c.startswith("estab_")]
    panel[nuevas] = panel[nuevas].fillna(0)
    descuadre = (panel["estab_total_sectores"] - panel["estab_emprendimiento"]).abs().max()
    if descuadre > 0:
        raise ValueError(
            f"los sectores no suman el total del DENUE (diferencia máxima {descuadre})"
        )
    panel = panel.drop(columns="estab_total_sectores")
    por_cada = P["resultados"]["por_cada_localidad"]
    base_pob = panel["pobtot"].where(panel["pobtot"] > 0)
    for c in [c for c in nuevas if c != "estab_total_sectores"]:
        panel[f"{c}_pc"] = panel[c] / base_pob * por_cada

    estable = panel["cve_mun"].map(mapa_crosswalk()).fillna(panel["cve_mun"])
    g_mun = _g_municipal_semestral(periodos).set_index("cve_mun")
    panel["G_mun"] = estable.map(g_mun["G_mun"]).fillna(0).astype(int)
    panel["mun_ya_tratado"] = estable.map(g_mun["mun_ya_tratado"]).fillna(False).astype(bool)
    censo = _censo_municipal().set_index("cve_mun")
    panel["prop_65_mas"] = estable.map(censo["prop_65_mas"])
    faltan = panel.loc[panel["prop_65_mas"].isna(), "cve_mun"].nunique()
    if faltan:
        log.warning("%d municipios sin proporción de 65+ del Censo 2020", faltan)

    panel.to_parquet(SALIDAS["localidad_f6"], index=False, compression="zstd")
    log.info(
        "panel localidad_f6: %d filas, %d localidades; columnas nuevas: %s",
        len(panel),
        panel["cve_loc"].nunique(),
        ", ".join(c for c in nuevas if c != "estab_total_sectores"),
    )
    return SALIDAS["localidad_f6"]


def pub_municipio_f6() -> Path:
    """Foto del padrón (oct-2026) con el tratamiento y las covariables del panel financiero."""
    mun = pd.read_parquet(PROCESSED / "panel_municipio_trim.parquet")
    columnas = [
        "cve_mun",
        "G_trimestre",
        "G",
        "ya_tratado_inicio",
        "sospechoso_banjercito",
        "log_poblacion_2020",
        "indice_marginacion_2020",
        "banca_mun_2019",
        "desierto_bancario",
        "poblacion_adulta_fija",
    ]
    mun = mun.drop_duplicates("cve_mun")[columnas]
    pub = pd.read_parquet(INTERIM / "pub_municipio.parquet")
    pub = aplicar_crosswalk(
        pub[["cve_mun", "beneficiarios_unicos", "monto"]],
        ["beneficiarios_unicos", "monto"],
        ["cve_mun"],
    )
    salida = mun.merge(pub, on="cve_mun", how="left").merge(
        _censo_municipal(), on="cve_mun", how="left"
    )
    sin_pub = int(salida["beneficiarios_unicos"].isna().sum())
    if sin_pub:
        log.warning("%d municipios del panel sin dato en el padrón", sin_pub)
    salida["benef_100hab"] = 100 * salida["beneficiarios_unicos"] / salida["pobtot"]
    salida["monto_pc"] = salida["monto"] / salida["pobtot"]
    salida["cve_ent"] = salida["cve_mun"].str[:2]
    # Mismas cohortes que la muestra financiera (2022T1–2024T1); las demás aperturas aparte.
    t_inicio, t_fin = (periodo_a_t(p) for p in COHORTES_PRINCIPALES)
    ya = salida["ya_tratado_inicio"].fillna(False).astype(bool)
    principal = salida["G"].between(t_inicio, t_fin) & ~salida["sospechoso_banjercito"].fillna(
        False
    )
    salida["grupo"] = np.select(
        [ya, principal, salida["G"] > 0, salida["G"] == 0],
        ["ya_tratado", "tratado_2022_2024", "otras_aperturas", "sin_apertura"],
        default="otras_aperturas",
    )
    salida.to_parquet(SALIDAS["municipio_pub"], index=False)
    log.info("pub_municipio_f6: %s", salida["grupo"].value_counts().to_dict())
    return SALIDAS["municipio_pub"]


def construir_todos() -> dict[str, Path]:
    return {"localidad_f6": panel_localidad_f6(), "municipio_pub": pub_municipio_f6()}


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if len(sys.argv) > 1:
        globals()[sys.argv[1]]()
    else:
        construir_todos()

"""Paneles de la fase 2 (preregistro en `docs/decisiones.md`, 2026-10-07).

Módulo aparte para no tocar `panel.py`, que reproduce la corrida final: reutiliza sus funciones
(tratamiento trimestral, G efectivo, crosswalk, covariables) y escribe paneles nuevos en
`data/processed/` con la misma estructura (`id, t, G, banderas, resultados, covariables`), para que
`analisis/10_fase2.R` los lea con `leer_panel()`.

| panel | unidad | periodos | resultados |
|---|---|---|---|
| `panel_municipio_trim_obs` | municipio | 2019T1–2025T4 | BDIF, con G del Banco del Bienestar **observado** 2022+ |
| `panel_municipio_eic` | municipio | 2015, 2020, 2025 | EIC/Censo: emprendimiento, programas, remesas… |
| `panel_localidad_viirs` | localidad | 2016–2024 (anual) | luz nocturna a 1 km y en el anillo 1–3 km |
| `panel_municipio_efipem` | municipio | 2016–2024 (anual) | impuestos, predial y derechos por habitante |
| `panel_municipio_enoe` | municipio | 2019T1–2025T4 sin 2020T2 | ENOE: negocio propio, informalidad, ingreso |

Convención para los paneles de una sola cohorte (EIC): las unidades fuera de la muestra por
exposición parcial se marcan en `apertura_posterior_ce`, el nombre que `leer_panel()` ya filtra
desde la fase 1 (Censos Económicos), y la dosis en `exposicion_ce` (control / temprana / tardía).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import (
    P,
    _agregar_tamano_cohorte,
    _banca_multiple_inicio,
    _covariables_en_logaritmos,
    _g_efectivo,
    _tratamiento_trimestral,
    aplicar_crosswalk,
)
from proyecto.utils.io import INTERIM, PROCESSED
from proyecto.utils.periodos import descomponer, periodo_a_t, rango

log = logging.getLogger(__name__)

F2 = P["fase2"]
SALIDAS = {
    "municipio_trim_obs": PROCESSED / "panel_municipio_trim_obs.parquet",
    "municipio_eic": PROCESSED / "panel_municipio_eic.parquet",
    "localidad_viirs": PROCESSED / "panel_localidad_viirs.parquet",
    "municipio_efipem": PROCESSED / "panel_municipio_efipem.parquet",
    "municipio_enoe": PROCESSED / "panel_municipio_enoe.parquet",
}


# --------------------------------------------------------------------------- utilidades
def anio_de_apertura(periodo: object, fmt: str) -> float:
    """Año calendario en que la apertura cuenta para un resultado **anual** (regla preregistrada).

    Un compuesto o un registro anual promedia los 12 meses: una apertura en la primera mitad del año
    (semestre 1, trimestres 1–2) ya cuenta ese año; en la segunda mitad, cuenta el año siguiente.
    `fmt` es "semestre" (`2022S2`) o "trimestre" (`2022Q3`). Devuelve NaN si no hay apertura.
    """
    if not isinstance(periodo, str):
        return np.nan
    anio = int(periodo[:4])
    if fmt == "semestre":
        segunda_mitad = periodo[-1] == "2"
    else:
        segunda_mitad = descomponer(periodo)[1] >= 3
    return float(anio + 1 if segunda_mitad else anio)


def _g_anual(g_periodo: pd.Series, anios: list[int], fmt: str) -> pd.Series:
    """G anual en la escala t (primer año = 1); 0 si nunca o si cae después del último año."""
    anio = g_periodo.map(lambda p: anio_de_apertura(p, fmt))
    t = anio - (anios[0] - 1)
    return t.where(anio.le(anios[-1]), 0).fillna(0).astype(int)


def _covariables_municipales(panel: pd.DataFrame) -> pd.DataFrame:
    """Marginación 2020, población 2020 (Censo, colapsada P-7), banca múltiple 2019T1 y desierto."""
    marg = pd.read_parquet(INTERIM / "conapo_marginacion.parquet")
    marg = marg[marg["anio"] == 2020].set_index("cve_mun")
    panel["indice_marginacion_2020"] = panel["cve_mun"].map(marg["im"])
    panel["grado_marginacion_2020"] = panel["cve_mun"].map(marg["gm"])
    pobm = pd.read_parquet(INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot"])
    pobm = aplicar_crosswalk(pobm.assign(llave=1), ["pobtot"], ["cve_mun", "llave"])
    panel["pobtot"] = panel["cve_mun"].map(pobm.set_index("cve_mun")["pobtot"])
    panel["poblacion_2020"] = panel["pobtot"]
    banca = panel["cve_mun"].map(_banca_multiple_inicio(estable=True)).fillna(0).astype(int)
    panel["banca_mun_2019"] = banca
    panel["desierto_bancario"] = 1 - banca
    return _covariables_en_logaritmos(panel, "poblacion_2020", None)


def _guardar(panel: pd.DataFrame, nombre: str, id_col: str) -> Path:
    panel = _agregar_tamano_cohorte(panel, id_col)
    panel = panel.sort_values([id_col, "t"]).reset_index(drop=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(SALIDAS[nombre], index=False, compression="zstd")
    unidades = panel.drop_duplicates(id_col)
    log.info(
        "panel %s: %d filas, %d unidades × %d periodos; tratadas %d, G = 0 %d",
        nombre,
        len(panel),
        len(unidades),
        panel["t"].nunique(),
        int((unidades["G"] > 0).sum()),
        int((unidades["G"] == 0).sum()),
    )
    return SALIDAS[nombre]


# --------------------------------------------------------------------------- 1. tratamiento observado
def panel_municipio_trim_obs() -> Path:
    """El panel trimestral de siempre con G recalculado sobre el Banco del Bienestar observado.

    Hasta 2021T4 la serie es la misma; desde 2022T1 sale del modelo Power Pivot del Portafolio CNBV
    (`limpieza/cnbv_portafolio_modelo.py`) en vez de la BDIF menos el Banjército extrapolado. Como
    Banjército ya se observa, nadie queda como sospechoso. `G_base` y `G_trimestre_base` guardan
    el tratamiento de la corrida final para comparar.
    """
    base = pd.read_parquet(PROCESSED / "panel_municipio_trim.parquet")
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar_obs.parquet")
    sb = sb.assign(suc_bienestar=sb["suc_bienestar_obs"], sospechoso_banjercito_nuevo=False)
    inicio, fin = P["periodo"]["inicio"], P["periodo"]["fin_trimestral"]
    primer, ya, _ = _tratamiento_trimestral(sb, fin)

    def indice(periodo: str) -> int:
        return periodo_a_t(periodo, base=inicio, valor_base=1)

    panel = base.drop(columns=["n_cohorte"], errors="ignore").copy()
    panel["G_base"] = panel["G"]
    panel["G_trimestre_base"] = panel["G_trimestre"]
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    panel["G"] = _g_efectivo(panel["G_trimestre"], rango(inicio, fin), indice)
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = False

    u = panel.drop_duplicates("cve_mun")
    cambio = u[u["G"] != u["G_base"]]
    log.info(
        "G observado contra G de la corrida final: %d municipios cambian (%d entran, %d salen, %d "
        "cambian de cohorte); antes sospechosos de Banjército: %d",
        len(cambio),
        int(((cambio["G_base"] == 0) & (cambio["G"] > 0)).sum()),
        int(((cambio["G_base"] > 0) & (cambio["G"] == 0)).sum()),
        int(((cambio["G_base"] > 0) & (cambio["G"] > 0)).sum()),
        int(base.drop_duplicates("cve_mun")["sospechoso_banjercito"].sum()),
    )
    return _guardar(panel, "municipio_trim_obs", "cve_mun")


# --------------------------------------------------------------------------- 2. EIC / Censo
def panel_municipio_eic() -> Path:
    """Municipio × {2015, 2020, 2025}: una cohorte (G = 3) con las aperturas de la ventana."""
    cfg = F2["eic"]
    e = pd.read_parquet(INTERIM / "inegi_eic_municipio.parquet")
    anios = sorted(e["anio"].unique())
    if anios != [2015, 2020, 2025]:
        raise ValueError(f"cortes inesperados: {anios}")
    marco = pd.DataFrame({"cve_mun": sorted(e["cve_mun"].unique())})
    panel = marco.merge(pd.DataFrame({"anio": anios}), how="cross")
    panel = panel.merge(e, on=["cve_mun", "anio"], how="left")
    panel["t"] = panel["anio"].map({a: i for i, a in enumerate(anios, start=1)})

    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    primer, ya, sospechoso = _tratamiento_trimestral(sb, P["periodo"]["fin_trimestral"])
    g_q = panel["cve_mun"].map(primer)
    panel["G_trimestre"] = g_q
    tratada = g_q.between(cfg["inicio_tratamiento"], cfg["fin_tratamiento"])
    panel["G"] = np.where(tratada, len(anios), 0).astype(int)
    # Fuera de la muestra por exposición: abrieron antes del Censo 2020 (pero después de 2019T1) o
    # después del levantamiento de la EIC 2025. Columna con el nombre que `leer_panel()` filtra.
    previa = g_q.gt(P["periodo"]["inicio"]) & g_q.lt(cfg["inicio_tratamiento"])
    posterior = g_q.gt(cfg["fin_tratamiento"])
    panel["apertura_posterior_ce"] = (previa | posterior).fillna(False).astype(bool)
    panel["exposicion_ce"] = np.select(
        [~tratada, g_q.le(cfg["fin_exposicion_temprana"])], ["control", "temprana"], "tardía"
    )
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)
    panel = _covariables_municipales(panel)
    log.info(
        "EIC: fuera por exposición %d municipios (antes del Censo 2020 %d, después de la EIC %d)",
        int(panel.drop_duplicates("cve_mun")["apertura_posterior_ce"].sum()),
        int(previa[panel["t"] == 1].sum()),
        int(posterior[panel["t"] == 1].sum()),
    )
    return _guardar(panel, "municipio_eic", "cve_mun")


# --------------------------------------------------------------------------- 3. VIIRS
def _g_semestre_vecina(marco: pd.DataFrame, trat: pd.DataFrame, bloque: int = 2000) -> pd.DataFrame:
    """G semestral (texto) de la localidad con sucursal más cercana distinta de la propia.

    Misma regla que `panel._exposicion_espacial` (fechable: no ambigua, no heredada de Bansefi, no
    sospechosa) pero devuelve el semestre de apertura en texto, para pasarlo a años.
    """
    from proyecto.construccion.tratamiento_localidad import haversine_km

    suc = trat.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    fechable = (
        suc["G_semestre"].notna()
        & ~suc["fecha_ambigua"].fillna(False).astype(bool)
        & ~suc["ya_tratado_inicio"].fillna(False).astype(bool)
        & ~suc["sospechoso_banjercito"].fillna(False).astype(bool)
    )
    g_suc = suc["G_semestre"].where(fechable).to_numpy(dtype=object)
    lat_s, lon_s = suc["lat"].to_numpy(float), suc["lon"].to_numpy(float)
    cve_s = suc["cve_loc"].to_numpy()
    lat_l, lon_l = marco["lat"].to_numpy(float), marco["lon"].to_numpy(float)
    cve_l = marco["cve_loc"].to_numpy()
    dist = np.empty(len(marco))
    cercana = np.empty(len(marco), dtype=int)
    for i in range(0, len(marco), bloque):
        j = slice(i, i + bloque)
        d = haversine_km(lat_l[j, None], lon_l[j, None], lat_s[None, :], lon_s[None, :])
        d[cve_l[j, None] == cve_s[None, :]] = np.inf
        k = d.argmin(axis=1)
        cercana[j] = k
        dist[j] = d[np.arange(len(k)), k]
    return pd.DataFrame(
        {"cve_loc": cve_l, "dist_vecina_km": dist, "G_semestre_vecina": g_suc[cercana]}
    )


def panel_localidad_viirs() -> Path:
    """Localidad × año 2016–2024 con la luz nocturna y el marco del panel de localidades."""
    anios = F2["viirs"]["anios"]
    base = pd.read_parquet(PROCESSED / "panel_localidad.parquet")
    fijas = [
        "cve_loc",
        "cve_mun",
        "nom_loc",
        "lat",
        "lon",
        "pobtot",
        "G_semestre",
        "fecha_ambigua",
        "ya_tratado_inicio",
        "sospechoso_banjercito",
        "n_sucursales_loc",
        "dist_bb_km",
        "mun_con_apertura",
        "es_cabecera",
        "con_actividad",
        "estab_previos",
        "banca_mun_2019",
        "desierto_bancario",
        "indice_marginacion_2020",
        "grado_marginacion_2020",
        "poblacion_2020",
        "log_poblacion_2020",
        "log1p_estab_previos",
    ]
    un = base.drop_duplicates("cve_loc")[fijas].reset_index(drop=True)
    trat = pd.read_parquet(INTERIM / "tratamiento_localidad.parquet")
    vec = _g_semestre_vecina(un, trat)
    un = un.merge(vec, on="cve_loc", how="left")
    dif = (un["dist_vecina_km"] - un["dist_bb_km"]).abs()
    if (dif > 1e-6).any():
        raise ValueError(
            f"la distancia recalculada no coincide con dist_bb_km en {int((dif > 1e-6).sum())} localidades"
        )
    un["G"] = _g_anual(un["G_semestre"], anios, "semestre")
    un["G_vecina"] = _g_anual(un["G_semestre_vecina"], anios, "semestre")

    v = pd.read_parquet(INTERIM / "viirs_localidad.parquet")
    v = v[v["anio"].isin(anios)]
    panel = un.merge(pd.DataFrame({"anio": anios}), how="cross")
    panel = panel.merge(v, on=["cve_loc", "anio"], how="left")
    faltan = panel["luz_1km"].isna().sum()
    if faltan:
        raise ValueError(f"{faltan} localidad-años sin luz: ¿cambió el marco de localidades?")
    panel["t"] = panel["anio"] - (anios[0] - 1)
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["log1p_luz_1km"] = np.log1p(panel["luz_1km"])
    panel["luz_1km_pos"] = (panel["luz_1km"] > 0).astype(int)
    panel["log1p_luz_anillo"] = np.log1p(panel["luz_anillo"])
    return _guardar(panel, "localidad_viirs", "cve_loc")


# --------------------------------------------------------------------------- 4. EFIPEM
def panel_municipio_efipem() -> Path:
    """Municipio × año 2016–2024: ingresos propios por habitante; solo municipios que reportan todo."""
    anios = F2["efipem"]["anios"]
    f = pd.read_parquet(INTERIM / "efipem_municipio.parquet")
    f = f[f["anio"].isin(anios)]
    marco = pd.DataFrame({"cve_mun": sorted(f["cve_mun"].unique())})
    panel = marco.merge(pd.DataFrame({"anio": anios}), how="cross")
    panel = panel.merge(f, on=["cve_mun", "anio"], how="left")
    panel["t"] = panel["anio"] - (anios[0] - 1)
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    primer, ya, sospechoso = _tratamiento_trimestral(sb, P["periodo"]["fin_trimestral"])
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    panel["G"] = _g_anual(panel["G_trimestre"], anios, "trimestre")
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)
    panel = _covariables_municipales(panel)
    base = panel["pobtot"].where(panel["pobtot"] > 0)
    for c in ("impuestos", "predial", "derechos"):
        pc = panel[c] / base
        panel[f"log_{c}_pc"] = np.log(pc.where(pc > 0))
    return _guardar(panel, "municipio_efipem", "cve_mun")


# --------------------------------------------------------------------------- 5. ENOE
def panel_municipio_enoe() -> Path:
    """Municipio × trimestre 2019T1–2025T4 sin 2020T2; solo los municipios en todos los trimestres.

    `t` cuenta trimestres calendario desde 2019T1 (2020T2 queda como hueco común, como 2023S1 en el
    DENUE) y G es el primer trimestre **observado** con sucursal.
    """
    cfg = F2["enoe"]
    e = pd.read_parquet(INTERIM / "enoe_municipio.parquet")
    periodos = [p for p in rango(cfg["inicio"], cfg["fin"]) if p not in set(cfg["excluir"])]
    e = e[e["periodo"].isin(periodos) & (e["n_registros"] > 0)]
    completos = e.groupby("cve_mun")["periodo"].nunique()
    completos = completos[completos == len(periodos)].index
    panel = e[e["cve_mun"].isin(completos)].copy()
    inicio = P["periodo"]["inicio"]

    def indice(periodo: str) -> int:
        return periodo_a_t(periodo, base=inicio, valor_base=1)

    panel["t"] = panel["periodo"].map(indice)
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    primer, ya, sospechoso = _tratamiento_trimestral(sb, P["periodo"]["fin_trimestral"])
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    panel["G"] = _g_efectivo(panel["G_trimestre"], periodos, indice)
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)
    panel = _covariables_municipales(panel)
    log.info(
        "ENOE: %d municipios en los %d trimestres (de %d con algún dato)",
        len(completos),
        len(periodos),
        e["cve_mun"].nunique(),
    )
    return _guardar(panel, "municipio_enoe", "cve_mun")


def construir_todos() -> dict[str, Path]:
    salidas = {}
    for nombre, f, insumo in [
        ("municipio_trim_obs", panel_municipio_trim_obs, "sucursales_bienestar_obs.parquet"),
        ("municipio_eic", panel_municipio_eic, "inegi_eic_municipio.parquet"),
        ("localidad_viirs", panel_localidad_viirs, "viirs_localidad.parquet"),
        ("municipio_efipem", panel_municipio_efipem, "efipem_municipio.parquet"),
        ("municipio_enoe", panel_municipio_enoe, "enoe_municipio.parquet"),
    ]:
        if (INTERIM / insumo).exists():
            salidas[nombre] = f()
        else:
            log.warning("sin %s: no se construye el panel %s", insumo, nombre)
    return salidas


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if len(sys.argv) > 1:
        globals()[f"panel_{sys.argv[1]}"]()
    else:
        construir_todos()

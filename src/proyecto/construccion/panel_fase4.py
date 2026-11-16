"""Paneles de la fase 4 (preregistro en `docs/decisiones.md`, 2026-10-14).

Módulo aparte para no tocar `panel.py` ni los de las fases 2 y 3. Parte de `panel_municipio_trim`
(mismas unidades, tratamiento, banderas y covariables) y le agrega:

| bloque | columnas |
|---|---|
| B y C1: Banco del Bienestar (Portafolio CNBV) | `tarjetas_debito_bb`, `transacciones_cajero_bb` y sus `_pc` |
| C3 y C4: series privadas largas | `tarjetas_credito_bm`, `establecimientos_tpv_privado` y sus `_pc` = BDIF − banco − Banjército |
| A1, H1(e) y B2: vecinos | `G_vecino_mun` (primera apertura **nueva** en un vecino, en `t`), `vecino_heredado`, `n_vecinos` |
| H2 y E1: covariables nuevas | `dist_bm_km`, `log1p_dist_bm`, `region`, `tendencia_{privado,bm,eacp}` (2017T2–2018T4) |

| panel | periodos | G |
|---|---|---|
| `panel_municipio_trim_f4` | 2019T1–2025T4 | el de `panel_municipio_trim` |
| `panel_municipio_placebo_f4` | 2017T2–2021T4 | **falsa** = real − 8 trimestres (A2) |

Además escribe la adenda de datos preregistrada en `outputs/tablas/fase4_adenda_*.csv`: la
concentración de los saltos del Portafolio, los controles que quedan sin vecinos tratados y la
validación de las series privadas reconstruidas contra la BDIF de 2022T4 en adelante.
"""

from __future__ import annotations

import logging
from functools import cache
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import P, _agregar_tamano_cohorte, mapa_crosswalk
from proyecto.utils.io import INTERIM, PROCESSED, TABLAS
from proyecto.utils.periodos import periodo_a_t, rango, t_a_periodo
from proyecto.variables import distancia, vecinos

log = logging.getLogger(__name__)

F4 = P["fase4"]
SALIDAS = {
    "municipio_trim_f4": PROCESSED / "panel_municipio_trim_f4.parquet",
    "municipio_placebo_f4": PROCESSED / "panel_municipio_placebo_f4.parquet",
    "municipio_enigh": PROCESSED / "panel_municipio_enigh.parquet",
    "municipio_enigh_pagos": PROCESSED / "panel_municipio_enigh_pagos.parquet",
    "hogar_enigh": PROCESSED / "panel_hogar_enigh.parquet",
}
# ENIGH (adenda del 2026-10-14): la forma de pago solo es comparable desde 2020.
OLAS_ENIGH = [2016, 2018, 2020, 2022, 2024]
OLAS_PAGOS = [2020, 2022, 2024]
PAGOS = ["pct_gasto_electronico", "pct_hog_pago_electronico"]
CONCENTRADO_ENIGH = ["pct_hog_deposito", "pct_hog_bene_gob", "log_ing_cor_pc", "log_gasto_mon_pc"]
COVARIABLES_MUN = [
    "cve_mun",
    "G_trimestre",
    "ya_tratado_inicio",
    "sospechoso_banjercito",
    "log_poblacion_2020",
    "indice_marginacion_2020",
    "banca_mun_2019",
    "poblacion_2020",
    "desierto_bancario",
]
POR_CADA = P["resultados"]["por_cada_municipio"]


# ----------------------------------------------------------------------------- Portafolio CNBV
def mes_a_trimestre(yyyymm: str) -> str:
    """`202205` -> `2022Q2` (cualquier mes, no solo los de cierre)."""
    return f"{yyyymm[:4]}Q{(int(yyyymm[4:6]) - 1) // 3 + 1}"


def _portafolio_mensual(serie: str, institucion: str) -> pd.DataFrame:
    """Serie mensual (`cve_mun` estable, `yyyymm`, `valor`) del Portafolio, operativa + modelo."""
    cfg = F4["portafolio"]["series"][serie]
    inst = F4["portafolio"][institucion]
    o = pd.read_parquet(
        INTERIM / "cnbv_portafolio_operativa.parquet",
        columns=["yyyymm", "cve_mun", "institucion", "producto", "valor"],
    )
    o = o[(o["institucion"] == inst["operativa"]) & o["producto"].isin(cfg["operativa"])]
    m = pd.read_parquet(
        INTERIM / "cnbv_portafolio_modelo.parquet",
        columns=["yyyymm", "cve_mun", "institucion", "descripcion_tipo", "valor"],
    )
    m = m[(m["institucion"] == inst["modelo"]) & m["descripcion_tipo"].isin(cfg["modelo"])]
    # El modelo empieza donde termina la operativa (2022-01); si se traslaparan, manda el modelo.
    o = o[o["yyyymm"] < m["yyyymm"].min()] if not m.empty else o
    d = pd.concat([o[["yyyymm", "cve_mun", "valor"]], m[["yyyymm", "cve_mun", "valor"]]])
    d["cve_mun"] = d["cve_mun"].map(mapa_crosswalk()).fillna(d["cve_mun"])
    return d.groupby(["cve_mun", "yyyymm"], as_index=False)["valor"].sum()


@cache
def periodos_portafolio() -> frozenset[str]:
    """Trimestres completos (tres meses) que el Portafolio publica, operativa más modelo. Una
    institución sin el producto en esos trimestres tiene cero, no un faltante."""
    meses = pd.concat(
        [
            pd.read_parquet(INTERIM / f"cnbv_portafolio_{f}.parquet", columns=["yyyymm"])["yyyymm"]
            for f in ("operativa", "modelo")
        ]
    ).drop_duplicates()
    por_trimestre = meses.map(mes_a_trimestre).value_counts()
    return frozenset(por_trimestre[por_trimestre == 3].index)


def a_trimestres(mensual: pd.DataFrame, flujo: bool) -> pd.DataFrame:
    """`cve_mun, yyyymm, valor` mensual → `cve_mun, periodo, valor` trimestral.

    Saldo: el valor del mes de cierre (03, 06, 09, 12). Flujo: la suma de los tres meses, y fuera
    los trimestres que la fuente no publica completos (las transacciones siguen el pago bimestral
    de programas: el último mes no representa al trimestre).
    """
    d = mensual.assign(periodo=mensual["yyyymm"].map(mes_a_trimestre))
    if flujo:
        meses = d.groupby("periodo")["yyyymm"].nunique()
        d = d[d["periodo"].isin(meses[meses == 3].index)]
    else:
        d = d[d["yyyymm"].str[-2:].isin(["03", "06", "09", "12"])]
    return d.groupby(["cve_mun", "periodo"], as_index=False)["valor"].sum()


def portafolio_trimestral(serie: str, institucion: str) -> pd.DataFrame:
    """`cve_mun, periodo, <serie>` del Portafolio (ver `a_trimestres`)."""
    flujo = F4["portafolio"]["series"][serie]["flujo"]
    out = a_trimestres(_portafolio_mensual(serie, institucion), flujo)
    return out.rename(columns={"valor": serie})


def _con_ceros(
    panel: pd.DataFrame, serie: pd.DataFrame, columna: str, publicados: frozenset[str] | None = None
) -> pd.DataFrame:
    """Une la serie y rellena con 0 los municipios ausentes, solo en los periodos que la fuente
    publica (regla 10: antes de su primer periodo queda NaN). `publicados` = los periodos de la
    fuente; por defecto, los que aparecen en la serie."""
    panel = panel.merge(serie, on=["cve_mun", "periodo"], how="left")
    publicados = publicados if publicados is not None else frozenset(serie["periodo"])
    publicado = panel["periodo"].isin(publicados)
    panel.loc[publicado, columna] = panel.loc[publicado, columna].fillna(0)
    return panel


# ----------------------------------------------------------------------------- BDIF
@cache
def _bdif_crudo() -> pd.DataFrame:
    return pd.read_parquet(
        INTERIM / "cnbv_bdif.parquet", columns=["cve_mun", "periodo", "variable", "sector", "valor"]
    )


def _bdif(variable: str, sectores: list[str], nombre: str) -> pd.DataFrame:
    b = _bdif_crudo()
    b = b[(b["variable"] == variable) & b["sector"].isin(sectores)].copy()
    b["cve_mun"] = b["cve_mun"].map(mapa_crosswalk()).fillna(b["cve_mun"])
    return (
        b.groupby(["cve_mun", "periodo"], as_index=False)["valor"]
        .sum()
        .rename(columns={"valor": nombre})
    )


def restar(total: pd.Series, *partes: pd.Series) -> pd.Series:
    """Total menos las partes públicas. Un resultado negativo es una inconsistencia entre fuentes
    (no una cantidad): queda en NaN y se reporta."""
    resto = total.copy()
    for parte in partes:
        resto = resto - parte
    negativos = resto < 0
    if negativos.any():
        log.warning(
            "%s: %d municipio-trimestres negativos (mínimo %.0f); quedan en NaN",
            resto.name,
            int(negativos.sum()),
            resto[negativos].min(),
        )
    return resto.mask(negativos)


def series_privadas(panel: pd.DataFrame) -> pd.DataFrame:
    """Tarjetas de crédito de banca múltiple y comercios con TPV privados, 2016–2025.

    La BDIF publica "banca" (múltiple + desarrollo) y "todos" sin hueco; la banca de desarrollo
    de la BDIF es exactamente Banco del Bienestar + Banjército del Portafolio (verificado
    2022T4–2023T4). Restando ambos queda lo privado.
    """
    for nombre, variable, sectores in [
        ("tarjetas_credito_banca", "tarjetas_credito", ["banca"]),
        ("establecimientos_tpv_todos", "establecimientos_tpv", ["todos"]),
    ]:
        panel = _con_ceros(panel, _bdif(variable, sectores, nombre), nombre)
    for serie in ("tarjetas_credito", "establecimientos_tpv"):
        for inst, sufijo in (("banco", "bb"), ("banjercito", "bj")):
            col = f"{serie}_{sufijo}"
            trimestral = portafolio_trimestral(serie, inst).rename(columns={serie: col})
            panel = _con_ceros(panel, trimestral, col, periodos_portafolio())
    panel["tarjetas_credito_bm"] = restar(
        panel["tarjetas_credito_banca"], panel["tarjetas_credito_bb"], panel["tarjetas_credito_bj"]
    ).rename(None)
    panel["establecimientos_tpv_privado"] = restar(
        panel["establecimientos_tpv_todos"],
        panel["establecimientos_tpv_bb"],
        panel["establecimientos_tpv_bj"],
    ).rename(None)
    return panel


def validar_series_privadas(panel: pd.DataFrame) -> pd.DataFrame:
    """Reconstrucción contra lo que la BDIF publica por sector desde 2022T4."""
    directas = [
        ("tarjetas_credito_bm", _bdif("tarjetas_credito", ["banca_multiple"], "directa")),
        (
            "establecimientos_tpv_privado",
            _bdif("establecimientos_tpv", ["banca_multiple", "socap", "sofipo"], "directa"),
        ),
    ]
    filas = []
    for col, directa in directas:
        d = panel[["cve_mun", "periodo", col]].merge(
            directa, on=["cve_mun", "periodo"], how="inner"
        )
        d["directa"] = d["directa"].fillna(0)
        for periodo, g in d.groupby("periodo"):
            filas.append(
                {
                    "serie": col,
                    "periodo": periodo,
                    "total_reconstruido": g[col].sum(),
                    "total_bdif_sector": g["directa"].sum(),
                    "correlacion_municipal": g[col].corr(g["directa"]),
                    "municipios_distintos": int((g[col].round() != g["directa"].round()).sum()),
                }
            )
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------- covariables
def _region(cve_mun: pd.Series) -> pd.Series:
    mapa = {ent: reg for reg, ents in F4["regiones_banxico"].items() for ent in ents}
    return cve_mun.str[:2].map(mapa)


def _modulos_compartamos() -> pd.DataFrame:
    return _bdif("modulos_compartamos", ["banca_multiple"], "modulos_compartamos")


def tendencias_previas(largo: pd.DataFrame) -> pd.DataFrame:
    """Pendiente lineal por trimestre de las sucursales por adulto en 2017T2–2018T4 (H2).

    Banca múltiple sin los módulos de Compartamos (P-11): la BDIF los publica en ese tramo y dejan
    de contarse en 2019T1.
    """
    cfg = F4["tendencia_previa"]
    periodos = rango(cfg["inicio"], cfg["fin"])
    d = largo[largo["periodo"].isin(periodos)][
        ["cve_mun", "periodo", "sucursales_bm", "sucursales_eacp", "poblacion_adulta_fija"]
    ].merge(_modulos_compartamos(), on=["cve_mun", "periodo"], how="left")
    d["sucursales_bm"] = (d["sucursales_bm"] - d["modulos_compartamos"].fillna(0)).clip(lower=0)
    d["sucursales_privado"] = d["sucursales_bm"] + d["sucursales_eacp"]
    base = d["poblacion_adulta_fija"].replace(0, np.nan)
    d["x"] = d["periodo"].map(lambda p: periodo_a_t(p, base=cfg["inicio"], valor_base=0))
    salida = {}
    for corto in ("privado", "bm", "eacp"):
        d["y"] = d[f"sucursales_{corto}"] / base * POR_CADA
        g = d.dropna(subset=["y"]).groupby("cve_mun")
        cov = g.apply(lambda s: np.cov(s["x"], s["y"], bias=True)[0, 1], include_groups=False)
        var = g["x"].var(ddof=0)
        salida[f"tendencia_{corto}"] = cov / var
    return pd.DataFrame(salida).rename_axis("cve_mun").reset_index()


def _agregar_vecinos(panel: pd.DataFrame, inicio: str) -> pd.DataFrame:
    if not vecinos.SALIDA.exists():
        vecinos.contiguidad()
    g_trim = panel.drop_duplicates("cve_mun").set_index("cve_mun")["G_trimestre"]
    v = vecinos.vecino_de_tratado(g_trim, inicio=P["periodo"]["inicio"])
    panel = panel.merge(v, on="cve_mun", how="left")
    fin = panel["periodo"].max()

    def a_t(p: object) -> int:
        if not isinstance(p, str) or p > fin:
            return 0
        return periodo_a_t(p, base=inicio, valor_base=1)

    panel["G_vecino_mun"] = panel["G_trimestre_vecino"].map(a_t).astype(int)
    panel["vecino_heredado"] = panel["vecino_heredado"].fillna(False).astype(bool)
    panel["n_vecinos"] = panel["n_vecinos"].fillna(0).astype(int)
    return panel


def _agregar_covariables(panel: pd.DataFrame) -> pd.DataFrame:
    if not distancia.SALIDA.exists():
        distancia.calcular()
    dist = pd.read_parquet(distancia.SALIDA, columns=["cve_mun", "dist_bm_km"])
    panel = panel.merge(dist, on="cve_mun", how="left")
    panel["log1p_dist_bm"] = np.log1p(panel["dist_bm_km"])
    panel["region"] = _region(panel["cve_mun"])
    largo = pd.read_parquet(PROCESSED / "panel_municipio_trim_largo.parquet")
    return panel.merge(tendencias_previas(largo), on="cve_mun", how="left")


# ----------------------------------------------------------------------------- paneles
def panel_municipio_trim_f4() -> Path:
    panel = pd.read_parquet(PROCESSED / "panel_municipio_trim.parquet")
    inicio = panel["periodo"].min()
    for serie in ("tarjetas_debito", "transacciones_cajero"):
        col = f"{serie}_bb"
        trimestral = portafolio_trimestral(serie, "banco").rename(columns={serie: col})
        panel = _con_ceros(panel, trimestral, col, periodos_portafolio())
    panel = series_privadas(panel)
    base = panel["poblacion_adulta_fija"].replace(0, np.nan)
    for c in (
        "tarjetas_debito_bb",
        "transacciones_cajero_bb",
        "tarjetas_credito_bm",
        "establecimientos_tpv_privado",
    ):
        panel[f"{c}_pc"] = panel[c] / base * POR_CADA
    panel = _agregar_vecinos(panel, inicio)
    panel = _agregar_covariables(panel)
    panel = panel.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    panel.to_parquet(SALIDAS["municipio_trim_f4"], index=False, compression="zstd")
    log.info(
        "panel_municipio_trim_f4: %d filas, %d municipios, %d columnas nuevas",
        len(panel),
        panel["cve_mun"].nunique(),
        len(panel.columns) - 72,
    )
    return SALIDAS["municipio_trim_f4"]


def panel_municipio_placebo_f4() -> Path:
    """A2: 2017T2–2021T4 con G falsa = G real − 8 para las cohortes 2022T1–2024T1."""
    cfg = F4["placebo"]
    largo = pd.read_parquet(PROCESSED / "panel_municipio_trim_largo.parquet")
    periodos = rango(cfg["inicio"], cfg["fin"])
    d = largo[largo["periodo"].isin(periodos)].copy()
    d = d.merge(_modulos_compartamos(), on=["cve_mun", "periodo"], how="left")
    d["sucursales_bm"] = (d["sucursales_bm"] - d["modulos_compartamos"].fillna(0)).clip(lower=0)
    d["sucursales_privado"] = d["sucursales_bm"] + d["sucursales_eacp"]
    base = d["poblacion_adulta_fija"].replace(0, np.nan)
    for c in ("sucursales_privado", "sucursales_bm", "sucursales_eacp"):
        d[f"{c}_pc"] = d[c] / base * POR_CADA

    g_real = d["G_trimestre"]
    # Fuera: aperturas reales dentro de la ventana (2019T2–2021T4) y sucursales heredadas.
    dentro = g_real.notna() & (g_real > P["periodo"]["inicio"]) & (g_real <= cfg["fin"])
    d = d[~dentro & ~d["ya_tratado_inicio"]].copy()
    cohortes = d["G_trimestre"].notna() & d["G_trimestre"].between("2022Q1", "2024Q1")

    def falsa(p: str) -> int:
        t_real = periodo_a_t(p, base=cfg["inicio"], valor_base=1)
        return t_real - cfg["adelanto"]

    d["t"] = d["periodo"].map(lambda p: periodo_a_t(p, base=cfg["inicio"], valor_base=1))
    d["G"] = 0
    d.loc[cohortes, "G"] = d.loc[cohortes, "G_trimestre"].map(falsa)
    d.loc[d["G"] > d["t"].max(), "G"] = 0
    d["tratado"] = ((d["G"] > 0) & (d["t"] >= d["G"])).astype(int)
    d = _agregar_tamano_cohorte(d, "cve_mun")
    d = d.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    d.to_parquet(SALIDAS["municipio_placebo_f4"], index=False, compression="zstd")
    u = d.drop_duplicates("cve_mun")
    log.info(
        "panel_municipio_placebo_f4: %d municipios × %d trimestres; con G falsa %d, G = 0 %d",
        len(u),
        d["t"].nunique(),
        int((u["G"] > 0).sum()),
        int((u["G"] == 0).sum()),
    )
    return SALIDAS["municipio_placebo_f4"]


# ----------------------------------------------------------------------------- adenda de datos
def adenda_saltos(panel: pd.DataFrame) -> pd.DataFrame:
    """B1: qué parte de los saltos nacionales de tarjetas del banco (sep-2021 y feb-2022) cae en
    municipios que abren dentro de ±1 trimestre del salto."""
    d = _portafolio_mensual("tarjetas_debito", "banco")
    g_trim = panel.drop_duplicates("cve_mun").set_index("cve_mun")["G_trimestre"]
    filas = []
    for antes, despues, trimestre in [
        ("202108", "202109", "2021Q3"),
        ("202201", "202202", "2022Q1"),
    ]:
        a = d[d["yyyymm"] == antes].set_index("cve_mun")["valor"]
        b = d[d["yyyymm"] == despues].set_index("cve_mun")["valor"]
        todos = a.index.union(b.index)
        cambio = b.reindex(todos, fill_value=0) - a.reindex(todos, fill_value=0)
        alrededor = set(rango(_mover(trimestre, -1), _mover(trimestre, 1)))
        cerca = cambio.index.to_series().map(g_trim).isin(alrededor).to_numpy()
        filas.append(
            {
                "salto": f"{antes}->{despues}",
                "cambio_nacional": cambio.sum(),
                "cambio_en_aperturas_±1t": cambio[cerca].sum(),
                "proporcion": cambio[cerca].sum() / cambio.sum() if cambio.sum() else np.nan,
                "cambio_absoluto_en_aperturas_±1t": cambio[cerca].abs().sum() / cambio.abs().sum(),
                "municipios_con_cambio": int((cambio != 0).sum()),
            }
        )
    return pd.DataFrame(filas)


def _mover(periodo: str, k: int) -> str:
    return t_a_periodo(periodo_a_t(periodo) + k)


def adenda_controles_vecinos(panel: pd.DataFrame) -> pd.DataFrame:
    """H1(e): controles limpios por pila con y sin la condición de vecinos (regla de los 100)."""
    k_pre, k_post = F4["apilado"]["k_pre"], F4["apilado"]["k_post"]
    u = panel.drop_duplicates("cve_mun")
    u = u[~u["ya_tratado_inicio"] & ~u["sospechoso_banjercito"]]
    pares = pd.read_parquet(vecinos.SALIDA)
    g_todos = panel.drop_duplicates("cve_mun").set_index("cve_mun")["G"]
    pares["g_vecino"] = pares["cve_mun_vecino"].map(g_todos)
    t_max, t_min = int(panel["t"].max()), int(panel["t"].min())
    filas = []
    for g in sorted(c for c in u["G"].unique() if c > 0):
        if g - k_pre < t_min or g + k_post > t_max:
            continue
        limpio = u[(u["G"] == 0) | (u["G"] > g + k_post)]["cve_mun"]
        fin = g + k_post
        con_vecino = pares[(pares["g_vecino"] > 0) & (pares["g_vecino"] <= fin)]
        con_vecino_nuevo = con_vecino[con_vecino["g_vecino"] > 1]
        filas.append(
            {
                "pila_G": int(g),
                "tratadas": int((u["G"] == g).sum()),
                "controles_limpios": len(limpio),
                "sin_vecino_con_sucursal": int((~limpio.isin(con_vecino["cve_mun"])).sum()),
                "sin_vecino_apertura_nueva": int((~limpio.isin(con_vecino_nuevo["cve_mun"])).sum()),
            }
        )
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------- ENIGH
def ola_de_apertura(g_trimestre: object, olas: list[int]) -> tuple[int, bool]:
    """(G, ambigua) en la escala de olas (1 = la primera). El levantamiento va del 21 de agosto
    al 28 de noviembre: una apertura hasta el segundo trimestre del año de una ola cuenta en esa
    ola; en el tercero es ambigua; en el cuarto, cuenta en la siguiente. G = 0 si no abre antes
    de la última ola."""
    if not isinstance(g_trimestre, str):
        return 0, False
    anio, trimestre = int(g_trimestre[:4]), int(g_trimestre[-1])
    for k, ola in enumerate(olas, start=1):
        if ola > anio or (ola == anio and trimestre <= 2):
            return k, False
        if ola == anio and trimestre == 3:
            return k, True
    return 0, False


def _tratamiento_enigh(d: pd.DataFrame, olas: list[int]) -> pd.DataFrame:
    cov = pd.read_parquet(PROCESSED / "panel_municipio_trim.parquet", columns=COVARIABLES_MUN)
    cov = cov.drop_duplicates("cve_mun")
    d = d.merge(cov, on="cve_mun", how="inner")
    g = d["G_trimestre"].map(lambda x: ola_de_apertura(x, olas))
    d["G"] = g.str[0].astype(int)
    d["fecha_ambigua"] = g.str[1].astype(bool)
    d["t"] = d["anio"].map({a: k for k, a in enumerate(olas, start=1)}).astype(int)
    d["tratado"] = ((d["G"] > 0) & (d["t"] >= d["G"])).astype(int)
    return d


def panel_municipio_enigh(olas: list[int], resultados: list[str], nombre: str) -> Path:
    """Municipio × ola, solo municipios presentes en todas las olas (panel balanceado)."""
    m = pd.read_parquet(INTERIM / "enigh_municipio.parquet")
    m = m[m["anio"].isin(olas)]
    completos = m.groupby("cve_mun")["anio"].nunique()
    m = m[m["cve_mun"].isin(completos[completos == len(olas)].index)]
    m = m[["cve_mun", "anio", "n_hogares", *resultados]]
    panel = _agregar_tamano_cohorte(_tratamiento_enigh(m, olas), "cve_mun")
    panel = panel.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    panel.to_parquet(SALIDAS[nombre], index=False, compression="zstd")
    u = panel.drop_duplicates("cve_mun")
    u = u[~u["ya_tratado_inicio"] & ~u["fecha_ambigua"]]
    log.info(
        "%s: %d municipios × %d olas; sin heredados ni ambiguos: %s",
        nombre,
        panel["cve_mun"].nunique(),
        len(olas),
        u["G"].value_counts().sort_index().to_dict(),
    )
    return SALIDAS[nombre]


def panel_hogar_enigh() -> Path:
    """Hogar × ola con el tratamiento de su municipio (robustez del TWFE extendido). Los
    resultados de forma de pago quedan en NaN antes de 2020."""
    h = pd.read_parquet(INTERIM / "enigh_hogar.parquet")
    integ = h["tot_integ"].where(h["tot_integ"] > 0)
    d = pd.DataFrame(
        {
            "cve_mun": h["cve_mun"],
            "anio": h["anio"],
            "factor": h["factor"],
            "pct_gasto_electronico": 100
            * h["gasto_electronico"]
            / h["gasto_forma"].where(h["gasto_forma"] > 0),
            "pct_hog_pago_electronico": 100 * h["pago_electronico"].astype(float),
            "pct_hog_deposito": 100 * (h["deposito"] > 0).astype(float),
            "pct_hog_bene_gob": 100 * (h["bene_gob"] > 0).astype(float),
            "log_ing_cor_pc": np.log((h["ing_cor"] / integ).where(h["ing_cor"] > 0)),
            "log_gasto_mon_pc": np.log((h["gasto_mon"] / integ).where(h["gasto_mon"] > 0)),
        }
    )
    d.loc[d["anio"] < OLAS_PAGOS[0], PAGOS] = np.nan
    d = _agregar_tamano_cohorte(_tratamiento_enigh(d, OLAS_ENIGH), "cve_mun")
    d.to_parquet(SALIDAS["hogar_enigh"], index=False, compression="zstd")
    log.info("panel_hogar_enigh: %d hogares, %d municipios", len(d), d["cve_mun"].nunique())
    return SALIDAS["hogar_enigh"]


def construir_enigh() -> dict[str, Path]:
    return {
        "municipio_enigh": panel_municipio_enigh(OLAS_ENIGH, CONCENTRADO_ENIGH, "municipio_enigh"),
        "municipio_enigh_pagos": panel_municipio_enigh(OLAS_PAGOS, PAGOS, "municipio_enigh_pagos"),
        "hogar_enigh": panel_hogar_enigh(),
    }


def construir_todos() -> dict[str, Path]:
    salidas = {
        "municipio_trim_f4": panel_municipio_trim_f4(),
        "municipio_placebo_f4": panel_municipio_placebo_f4(),
    }
    if (INTERIM / "enigh_municipio.parquet").exists():
        salidas.update(construir_enigh())
    panel = pd.read_parquet(SALIDAS["municipio_trim_f4"])
    TABLAS.mkdir(parents=True, exist_ok=True)
    adendas = {
        "fase4_adenda_saltos_portafolio": adenda_saltos(panel),
        "fase4_adenda_controles_vecinos": adenda_controles_vecinos(panel),
        "fase4_adenda_series_privadas": validar_series_privadas(panel),
    }
    for nombre, tabla in adendas.items():
        tabla.to_csv(TABLAS / f"{nombre}.csv", index=False)
        log.info("%s:\n%s", nombre, tabla.to_string(index=False))
    return salidas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    construir_todos()

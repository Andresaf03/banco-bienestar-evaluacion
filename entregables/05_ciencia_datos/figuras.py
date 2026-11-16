"""Figuras y cifras de la presentación de Ciencia de Datos Aplicada II.

Uso:
    uv run python entregables/05_ciencia_datos/figuras.py

No estima nada: lee las salidas de la batería (`outputs/tablas/`), el panel municipal y el Marco
Geoestadístico, y escribe
  - `outputs/figuras/cdaii_*.png`: mapa de aperturas, dos estudios de evento, resumen de efectos
    financieros y la ecuación del estimador, en la paleta del deck (blanco y azul, sin título: el
    título va en la lámina);
  - `entregables/05_ciencia_datos/cifras.json`: las cifras que `presentacion.js` pone en las
    láminas y en las notas, ya formateadas, para no copiarlas a mano.

Las figuras usan Source Sans 3 si está instalada (la fuente del cuerpo del deck).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import geopandas as gpd
import matplotlib
import pandas as pd
from matplotlib import font_manager
from matplotlib.patches import Patch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from proyecto.utils.entregables import _num, _pct  # noqa: E402
from proyecto.utils.io import (  # noqa: E402
    FIGURAS,
    INTERIM,
    PROCESSED,
    RAW,
    TABLAS,
    parametros,
    ruta,
)

log = logging.getLogger(__name__)

DESTINO_CIFRAS = ruta("entregables", "05_ciencia_datos", "cifras.json")
SHP_MUNICIPIOS = RAW / "inegi_mg" / "mg_2024_integrado" / "conjunto_de_datos" / "00mun.shp"

# Paleta del deck (muestreada de la propuesta de Inferencia Causal).
FONDO = "#FAFAFA"
AZUL = "#0B5FFF"
AZUL_BANDA = "#D6E3FF"
TINTA = "#000000"
TINTA_2 = "#404040"
REJILLA = "#E3E3E3"
# Mapa: secuencial de un solo tono, de lo más antiguo (oscuro) a lo más reciente (claro).
MAPA = {
    "Ya tenía (Bansefi)": "#0A2A66",
    "2019–2022": AZUL,
    "2023": "#6F9BFF",
    "2024": "#A9C4FF",
    "Sin sucursal": "#ECEEF2",
}
DPI = 200

# Resultados financieros del resumen (mismos que `analisis/09_figuras_entregables.R`).
RESUMEN = [
    ("principal", "sucursales_privado_pc", "Sucursales privadas"),
    ("principal", "sucursales_bm_pc", "Sucursales de banca múltiple"),
    ("principal", "sucursales_eacp_pc", "Sucursales de EACP"),
    ("panel_corto", "captacion_privado_pc", "Captación privada (2022T4+)"),
    ("panel_corto", "credito_privado_pc", "Crédito privado (2022T4+)"),
    ("eacp", "capt_ahorro_eacp_pc", "Captación de ahorro de EACP"),
    ("eacp", "cred_consumo_eacp_pc", "Crédito al consumo de EACP †"),
]
EVENTO = {
    "primera_etapa_sucursales_total_pc": "cdaii_evento_primera_etapa",
    "sucursales_privado_pc": "cdaii_evento_privadas",
}
VENTANA_EVENTO = (-12, 11)


def _estilo() -> None:
    """Fuente y tinta comunes; Source Sans 3 si está en ~/Library/Fonts."""
    for ttf in (Path.home() / "Library" / "Fonts").glob("SourceSans3-*.ttf"):
        font_manager.fontManager.addfont(str(ttf))
    familia = "Source Sans 3"
    try:
        font_manager.findfont(familia, fallback_to_default=False)
    except ValueError:
        log.warning("Source Sans 3 no está instalada: las figuras usan la fuente por omisión")
        familia = "sans-serif"
    plt.rcParams.update(
        {
            "font.family": familia,
            "font.size": 13,
            "text.color": TINTA,
            "axes.labelcolor": TINTA,
            "axes.edgecolor": REJILLA,
            "xtick.color": TINTA_2,
            "ytick.color": TINTA_2,
            "axes.facecolor": FONDO,
            "figure.facecolor": FONDO,
            "savefig.facecolor": FONDO,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def _guardar(fig: plt.Figure, nombre: str) -> Path:
    FIGURAS.mkdir(parents=True, exist_ok=True)
    destino = FIGURAS / f"{nombre}.png"
    fig.savefig(destino, dpi=DPI, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    log.info("figura %s", destino)
    return destino


def _leer(nombre: str) -> pd.DataFrame:
    ruta_csv = TABLAS / f"{nombre}.csv"
    if not ruta_csv.exists():
        raise FileNotFoundError(f"falta {ruta_csv}: corre la batería antes de la presentación")
    return pd.read_csv(ruta_csv)


def _fila(t: pd.DataFrame, **filtro: str) -> pd.Series:
    sel = t
    for col, val in filtro.items():
        sel = sel[sel[col] == val]
    if len(sel) != 1:
        raise ValueError(f"se esperaba una fila para {filtro}, hay {len(sel)}")
    return sel.iloc[0]


# --- Mapa ---------------------------------------------------------------------------------------


def _categoria(g: int) -> str:
    """Categoría del mapa según G (trimestre de la primera sucursal, 2019T1 = 1, 0 = nunca)."""
    if g == 1:
        return "Ya tenía (Bansefi)"
    if 2 <= g <= 16:
        return "2019–2022"
    if 17 <= g <= 20:
        return "2023"
    if 21 <= g <= 24:
        return "2024"
    return "Sin sucursal"


def fig_mapa() -> dict[str, int]:
    panel = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "G"]
    ).drop_duplicates("cve_mun")
    cruce = pd.read_parquet(
        INTERIM / "crosswalk_municipios.parquet", columns=["cve_mun", "cve_estable"]
    )
    mun = gpd.read_file(SHP_MUNICIPIOS, columns=["CVEGEO", "CVE_ENT"])
    mun["geometry"] = mun.geometry.simplify(1500)
    # Los municipios nuevos (hijos) toman la fecha del municipio estable al que se agregan.
    mun = mun.merge(cruce, left_on="CVEGEO", right_on="cve_mun", how="left")
    mun["cve_estable"] = mun["cve_estable"].fillna(mun["CVEGEO"])
    mun = mun.merge(panel.rename(columns={"cve_mun": "cve_estable"}), on="cve_estable", how="left")
    if mun["G"].isna().any():
        log.warning("%d polígonos sin G en el panel: van como sin sucursal", mun["G"].isna().sum())
    mun["categoria"] = mun["G"].fillna(0).astype(int).map(_categoria)
    estados = mun.dissolve(by="CVE_ENT")

    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    for cat, color in MAPA.items():
        mun[mun["categoria"] == cat].plot(ax=ax, color=color, edgecolor=FONDO, linewidth=0.08)
    estados.boundary.plot(ax=ax, color="#8A8F99", linewidth=0.35)
    xmin, _, xmax, _ = mun.total_bounds
    ax.set_xlim(xmin - 0.2 * (xmax - xmin), xmax)
    ax.set_axis_off()
    # Conteos en unidades del panel (municipios con límites constantes), no en polígonos.
    conteo = panel["G"].map(_categoria).value_counts()
    leyenda = [
        Patch(
            facecolor=c,
            edgecolor="#8A8F99",
            linewidth=0.4,
            label=f"{cat}  ({conteo.get(cat, 0):,})",
        )
        for cat, c in MAPA.items()
    ]
    ax.legend(
        handles=leyenda,
        loc="lower left",
        title="Primera sucursal",
        title_fontsize=11,
        alignment="left",
        frameon=False,
        fontsize=11,
        handlelength=1.2,
        borderaxespad=0.2,
    )
    _guardar(fig, "cdaii_mapa_aperturas")
    return {cat: int(conteo.get(cat, 0)) for cat in MAPA}


# --- Estudios de evento ------------------------------------------------------------------------


def fig_evento(
    resultado: str, nombre: str, banda: float | None = None, etiqueta_banda: str = ""
) -> None:
    d = _leer(f"cs_agg_municipio_trim_esc_{resultado}")
    d = d[d["tipo"] == "dynamic"].copy()
    d["e"] = d["termino"].astype(int)
    d = d[d["e"].between(*VENTANA_EVENTO)].sort_values("e")

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    if banda is not None:
        ax.axhspan(-banda, banda, color=AZUL_BANDA, alpha=0.6, linewidth=0, zorder=0)
    ax.axhline(0, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.axvline(-0.5, color=TINTA_2, linewidth=0.8, linestyle=":", zorder=1)
    # Previos y posteriores por separado: la banda no se une a través de la apertura.
    for tramo in (d[d["e"] < 0], d[d["e"] >= 0]):
        ax.fill_between(
            tramo["e"],
            tramo["ic_bajo"],
            tramo["ic_alto"],
            color=AZUL,
            alpha=0.16,
            linewidth=0,
            zorder=2,
        )
    ax.plot(d["e"], d["valor"], "o", color=AZUL, markersize=5, zorder=3)
    if banda is not None:
        ax.text(
            VENTANA_EVENTO[0],
            banda,
            etiqueta_banda,
            va="bottom",
            fontsize=11,
            color=TINTA_2,
        )
    ax.set_xlabel("Trimestres desde la primera sucursal")
    ax.set_ylabel("Sucursales por 10 mil adultos")
    ax.grid(axis="y", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, nombre)


# --- Resumen de efectos financieros ------------------------------------------------------------


def fig_efectos(t: pd.DataFrame, sesoi: float) -> None:
    filas = []
    for variante, resultado, nombre in RESUMEN:
        r = _fila(t, variante=variante, panel="municipio_trim", resultado=resultado)
        escala = abs(r["media_base"])
        filas.append(
            (nombre, r["efecto_pct"], 100 * r["ic90_bajo"] / escala, 100 * r["ic90_alto"] / escala)
        )
    d = pd.DataFrame(filas, columns=["nombre", "pct", "bajo", "alto"]).iloc[::-1]
    y = range(len(d))

    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    ax.axvspan(-sesoi, sesoi, color=AZUL_BANDA, alpha=0.6, linewidth=0, zorder=0)
    ax.axvline(0, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.hlines(y, d["bajo"], d["alto"], color=TINTA, linewidth=1.6, zorder=2)
    ax.plot(
        d["pct"],
        y,
        "o",
        color=AZUL,
        markersize=8,
        markeredgecolor=FONDO,
        markeredgewidth=1.2,
        zorder=3,
    )
    ax.set_yticks(list(y), d["nombre"], fontsize=13, color=TINTA)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-9, 9)
    ax.set_xlabel("Efecto (% de la media previa), IC al 90%")
    ax.text(
        sesoi, len(d) - 0.35, f"±{sesoi:g}%", ha="right", va="bottom", fontsize=11, color=TINTA_2
    )
    ax.grid(axis="x", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, "cdaii_efectos_financieros")


# --- Ecuación ----------------------------------------------------------------------------------


def fig_ecuacion() -> None:
    lineas = [
        r"$ATT(g,t)=\mathbb{E}\,[\,Y_{it}(g)-Y_{it}(0)\mid G_i=g\,]$",
        r"$\widehat{ATT}(g,t)=\mathbb{E}\,\left[\,(w^{G}_{i}-w^{C}_{i})"
        r"\,(Y_{it}-Y_{i,g-1}-m_{g,t}(X_i))\,\right]$",
        r"$\theta=\sum_{g}\,\Pr(G=g\mid G\leq\mathcal{T})\,\frac{1}{\mathcal{T}-g+1}"
        r"\sum_{t\geq g}ATT(g,t)$",
    ]
    with plt.rc_context({"mathtext.fontset": "cm"}):
        fig = plt.figure(figsize=(7.6, 2.3))
        for i, linea in enumerate(lineas):
            fig.text(0.0, 0.84 - 0.36 * i, linea, fontsize=19, color=TINTA, va="center")
        _guardar(fig, "cdaii_ecuacion")


# --- Cifras ------------------------------------------------------------------------------------


def cifras(t: pd.DataFrame, mapa: dict[str, int], sesoi: float) -> dict:
    def principal(resultado: str, variante: str = "principal") -> pd.Series:
        return _fila(t, variante=variante, panel="municipio_trim", resultado=resultado)

    priv, bm, eacp = (
        principal(r) for r in ("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
    )
    pe = _fila(t, panel="municipio_trim", resultado="sucursales_total_pc", variante="primera_etapa")
    cred = principal("cred_consumo_eacp_pc", "eacp")

    suc = (
        pd.read_parquet(
            INTERIM / "sucursales_bienestar.parquet", columns=["periodo", "suc_bienestar"]
        )
        .groupby("periodo")["suc_bienestar"]
        .sum()
    )
    m19 = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "periodo", "sucursales_bm"]
    ).query("periodo == '2019Q1'")

    banc = _leer("fase4_bancarizacion")
    tarjetas = _fila(banc, resultado="tarjetas_debito_bb_pc", estimador="Callaway y Sant'Anna")
    perm = _fila(_leer("fase4_permutacion"), resultado="sucursales_privado_pc")
    etwfe = _fila(
        _leer("fase4_efectos_fijos"), etiqueta="municipio_trim_f4_esc_etwfe_sucursales_privado_pc"
    )
    denue = _fila(t, panel="localidad", variante="principal", resultado="estab_emprendimiento_pc")
    est = _leer("fase4_estimadores")
    bm_twfe = _fila(est, estimador="TWFE estático", resultado="sucursales_bm_pc")
    bm_bjs = _fila(est, estimador="Borusyak et al.", resultado="sucursales_bm_pc")
    directorio = pd.read_parquet(INTERIM / "babien.parquet", columns=["id_sucursal"])
    etwfe_abren = _fila(
        est,
        estimador="TWFE extendido con covariables, solo municipios que abren",
        resultado="sucursales_privado_pc",
    )

    def cota(r: pd.Series) -> str:
        return f"±{r['cota_equivalencia_pct']:.1f}%"

    return {
        "sucursales_2019": _num(suc.loc["2019Q1"], 0),
        "sucursales_2024": _num(suc.loc["2024Q4"], 0),
        "sucursales_directorio": _num(directorio["id_sucursal"].nunique(), 0),
        "pct_sin_bm_2019": f"{100 * (m19['sucursales_bm'] == 0).mean():.0f}%",
        "n_municipios": _num(m19["cve_mun"].nunique(), 0),
        "n_tratadas": _num(priv["n_tratadas"], 0),
        "n_controles": _num(priv["n_controles"], 0),
        "mapa": mapa,
        "pe_att": _num(pe["valor"], 2),
        "pe_ee": _num(pe["ee"], 2),
        "pe_wald_p": f"{pe['pre_wald_p']:.2f}",
        "tarjetas": _num(tarjetas["valor"], 0),
        "priv_att": _num(priv["valor"], 3),
        "priv_ee": _num(priv["ee"], 3),
        "priv_pct": _pct(priv["efecto_pct"]),
        "priv_cota": cota(priv),
        "priv_wald_p": f"{priv['pre_wald_p']:.2f}",
        "priv_rw": f"{priv['p_rw']:.2f}",
        "bm_pct": _pct(bm["efecto_pct"]),
        "bm_cota": cota(bm),
        "eacp_pct": _pct(eacp["efecto_pct"]),
        "eacp_cota": cota(eacp),
        "bm_twfe_pct": _pct(bm_twfe["efecto_pct"]),
        "bm_bjs_pct": _pct(bm_bjs["efecto_pct"]),
        "sesoi": f"±{sesoi:g}%",
        "sesoi_nivel": _num(sesoi / 100 * priv["media_base"], 3),
        "media_previa_priv": _num(priv["media_base"], 2),
        "perm_p": f"{perm['p_permutacion']:.2f}",
        "cred_eacp_pct": _pct(cred["efecto_pct"]),
        "etwfe_cov_pct": _pct(100 * etwfe["valor"] / etwfe["media_base"]),
        "etwfe_abren_pct": _pct(etwfe_abren["efecto_pct"]),
        "denue_pct": _pct(denue["efecto_pct"]),
    }


def generar() -> Path:
    _estilo()
    sesoi = float(parametros()["estimacion"]["sesoi_pct"])
    t = _leer("tabla_final")
    mapa = fig_mapa()
    priv = _fila(t, variante="principal", panel="municipio_trim", resultado="sucursales_privado_pc")
    fig_evento("primera_etapa_sucursales_total_pc", EVENTO["primera_etapa_sucursales_total_pc"])
    fig_evento(
        "sucursales_privado_pc",
        EVENTO["sucursales_privado_pc"],
        banda=sesoi / 100 * priv["media_base"],
        etiqueta_banda=f"±{sesoi:g}% de la media previa",
    )
    fig_efectos(t, sesoi)
    fig_ecuacion()
    datos = cifras(t, mapa, sesoi)
    DESTINO_CIFRAS.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log.info("cifras en %s", DESTINO_CIFRAS)
    return DESTINO_CIFRAS


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

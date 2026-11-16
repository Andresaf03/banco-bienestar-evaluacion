"""Figuras y cifras de la presentación de Tópicos de Política Pública II.

Uso:
    uv run python entregables/06_politica_publica/figuras.py

No estima nada: lee las salidas de la batería (`outputs/tablas/`), el panel municipal, el Marco
Geoestadístico y el resumen de uso de la app (`app/public/datos/uso.json`), y escribe
  - `outputs/figuras/ppii_*.png`: figuras en la paleta del deck de CDA II (blanco y azul, sin
    título: el título va en la lámina), con `figsize` igual al ancho que ocupan en la lámina para
    que el texto quede a tamaño real;
  - `entregables/06_politica_publica/cifras.json`: las cifras que `presentacion.js` pone en las
    láminas y en las notas, ya formateadas.

Reutiliza el estilo y los lectores de `entregables/05_ciencia_datos/figuras.py` (se carga como
módulo, sin modificarlo). Las pocas cifras que no están en `outputs/tablas/` se escriben abajo, en
`EXTERNAS`, cada una con su fuente.
"""

from __future__ import annotations

import importlib.util
import json
import logging
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from proyecto.utils.entregables import _num, _pct  # noqa: E402
from proyecto.utils.io import INTERIM, PROCESSED, parametros, ruta  # noqa: E402

log = logging.getLogger(__name__)


def _cargar_cdaii():
    """Módulo de figuras de CDA II (estilo, paleta, lectores y mapa), sin tocar su carpeta."""
    archivo = ruta("entregables", "05_ciencia_datos", "figuras.py")
    spec = importlib.util.spec_from_file_location("figuras_cdaii", archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


cdaii = _cargar_cdaii()
_leer, _fila, _guardar = cdaii._leer, cdaii._fila, cdaii._guardar
FONDO, AZUL, AZUL_BANDA = cdaii.FONDO, cdaii.AZUL, cdaii.AZUL_BANDA
TINTA, TINTA_2, REJILLA = cdaii.TINTA, cdaii.TINTA_2, cdaii.REJILLA
MARINO = "#0A2A66"  # acento oscuro del tema (accent2)
GRIS = "#8A8F99"  # neutro de comparación

DESTINO_CIFRAS = ruta("entregables", "06_politica_publica", "cifras.json")
USO_APP = ruta("app", "public", "datos", "uso.json")
Z90 = 1.645

# Cifras que no están en outputs/tablas/ (no se estiman aquí; se citan).
EXTERNAS = {
    # ASF (2023), auditoría 2022-2-06HJO-21-0018-2023: meta de sucursales nuevas construidas por
    # la SEDENA y su avance al cierre de 2022.
    "meta_sedena": 2744,
    "terminadas_2022": 1873,
    "operando_2022": 922,
    # Bruhn y Love (2014): 815 sucursales de Banco Azteca en 2002; +7.6% dueños de negocio
    # informal (ver la sección de literatura de entregables/04_final/trabajo_final.qmd).
    "azteca_sucursales": 815,
    "azteca_pct": "+7.6%",
    # Fonseca y Matray (2024): empresas y empleo suben alrededor de 10% en Brasil.
    "brasil_pct": "≈+10%",
}


def _estilo() -> None:
    cdaii._estilo()
    plt.rcParams.update({"font.size": 14, "xtick.labelsize": 13, "ytick.labelsize": 13})


def _pct_ic(valor: float, ee: float, media: float) -> tuple[float, float, float]:
    """Efecto e IC al 90% en % de la media previa."""
    escala = 100 / abs(media)
    return valor * escala, (valor - Z90 * ee) * escala, (valor + Z90 * ee) * escala


def _periodo(t: int) -> str:
    """Trimestre en la escala del panel (2019T1 = 1) como texto, p. ej. 13 -> 2022T1."""
    return f"{2019 + (t - 1) // 4}T{(t - 1) % 4 + 1}"


# --- Forest genérico ----------------------------------------------------------------------------


def _forest(
    filas: pd.DataFrame,
    nombre: str,
    tamano: tuple[float, float],
    xlim: tuple[float, float],
    banda: float | None = None,
) -> None:
    """Puntos con IC al 90% en % de la media; `filas` trae nombre, pct, bajo, alto y destacado."""
    d = filas.iloc[::-1].reset_index(drop=True)
    y = list(range(len(d)))
    fig, ax = plt.subplots(figsize=tamano)
    if banda is not None:
        ax.axvspan(-banda, banda, color=AZUL_BANDA, alpha=0.6, linewidth=0, zorder=0)
        ax.text(
            banda,
            len(d) - 0.45,
            f"±{banda:g}%",
            ha="right",
            va="bottom",
            fontsize=12,
            color=TINTA_2,
        )
    ax.axvline(0, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.hlines(y, d["bajo"], d["alto"], color=TINTA, linewidth=1.6, zorder=2)
    for destacado, marca, color in ((False, "o", AZUL), (True, "D", MARINO)):
        sel = d[d["destacado"] == destacado]
        ax.plot(
            sel["pct"],
            sel.index,
            marca,
            color=color,
            markersize=8,
            markeredgecolor=FONDO,
            markeredgewidth=1.2,
            zorder=3,
        )
    ax.set_yticks(y, d["nombre"], color=TINTA)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, len(d) + 0.05 if banda is not None else len(d) - 0.4)
    ax.set_xlabel("Efecto (% de la media previa), IC al 90%")
    ax.grid(axis="x", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, nombre)


# --- Planteamiento --------------------------------------------------------------------------------


def _sucursales_por_trimestre() -> pd.Series:
    suc = pd.read_parquet(
        INTERIM / "sucursales_bienestar.parquet", columns=["periodo", "suc_bienestar"]
    )
    serie = suc.groupby("periodo")["suc_bienestar"].sum().sort_index()
    return serie.loc["2019Q1":"2024Q4"]


def fig_sucursales(serie: pd.Series) -> None:
    """Sucursales del Banco del Bienestar (sin Banjército) por trimestre, 2019T1–2024T4."""
    x = list(range(len(serie)))
    fig, ax = plt.subplots(figsize=(5.9, 3.7))
    ax.plot(x, serie.values, color=AZUL, linewidth=2.2, zorder=3)
    ax.plot(
        [x[0], x[-1]],
        [serie.iloc[0], serie.iloc[-1]],
        "o",
        color=AZUL,
        markersize=8,
        markeredgecolor=FONDO,
        markeredgewidth=1.2,
        zorder=4,
    )
    ax.annotate(
        _num(serie.iloc[0], 0),
        (x[0], serie.iloc[0]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="left",
        fontsize=14,
        color=TINTA,
    )
    ax.annotate(
        _num(serie.iloc[-1], 0),
        (x[-1], serie.iloc[-1]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="right",
        fontsize=14,
        color=TINTA,
    )
    ax.set_xticks(
        [i for i, p in enumerate(serie.index) if p.endswith("Q1")],
        [p[:4] for p in serie.index if p.endswith("Q1")],
    )
    ax.set_ylim(0, serie.max() * 1.18)
    ax.set_ylabel("Sucursales en operación")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, "ppii_sucursales")


def fig_mapa() -> dict[str, int]:
    """Mapa de aperturas de CDA II, a tamaño de lámina y con la leyenda en 13 pt."""
    gpd = cdaii.gpd
    panel = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "G"]
    ).drop_duplicates("cve_mun")
    cruce = pd.read_parquet(
        INTERIM / "crosswalk_municipios.parquet", columns=["cve_mun", "cve_estable"]
    )
    mun = gpd.read_file(cdaii.SHP_MUNICIPIOS, columns=["CVEGEO", "CVE_ENT"])
    mun["geometry"] = mun.geometry.simplify(1500)
    mun = mun.merge(cruce, left_on="CVEGEO", right_on="cve_mun", how="left")
    mun["cve_estable"] = mun["cve_estable"].fillna(mun["CVEGEO"])
    mun = mun.merge(panel.rename(columns={"cve_mun": "cve_estable"}), on="cve_estable", how="left")
    mun["categoria"] = mun["G"].fillna(0).astype(int).map(cdaii._categoria)
    estados = mun.dissolve(by="CVE_ENT")

    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    for cat, color in cdaii.MAPA.items():
        mun[mun["categoria"] == cat].plot(ax=ax, color=color, edgecolor=FONDO, linewidth=0.08)
    estados.boundary.plot(ax=ax, color=GRIS, linewidth=0.35)
    xmin, _, xmax, _ = mun.total_bounds
    ax.set_xlim(xmin - 0.25 * (xmax - xmin), xmax)
    ax.set_axis_off()
    conteo = panel["G"].map(cdaii._categoria).value_counts()
    leyenda = [
        cdaii.Patch(
            facecolor=c, edgecolor=GRIS, linewidth=0.4, label=f"{cat}  ({conteo.get(cat, 0):,})"
        )
        for cat, c in cdaii.MAPA.items()
    ]
    ax.legend(
        handles=leyenda,
        loc="lower left",
        title="Primera sucursal",
        title_fontsize=13,
        alignment="left",
        frameon=False,
        fontsize=13,
        handlelength=1.2,
        borderaxespad=0.1,
    )
    _guardar(fig, "ppii_mapa_aperturas")
    return {cat: int(conteo.get(cat, 0)) for cat in cdaii.MAPA}


def fig_ecuacion() -> None:
    lineas = [
        r"$ATT(g,t)=\mathbb{E}\,[\,Y_{it}(g)-Y_{it}(0)\mid G_i=g\,]$",
        r"$\widehat{ATT}(g,t)=\mathbb{E}\,\left[\,(w^{G}_{i}-w^{C}_{i})"
        r"\,(Y_{it}-Y_{i,g-1}-m_{g,t}(X_i))\,\right]$",
    ]
    with plt.rc_context({"mathtext.fontset": "cm"}):
        fig = plt.figure(figsize=(6.0, 1.45))
        for i, linea in enumerate(lineas):
            fig.text(0.0, 0.78 - 0.56 * i, linea, fontsize=19, color=TINTA, va="center")
        _guardar(fig, "ppii_ecuacion")


# --- Resultados financieros ---------------------------------------------------------------------


def fig_evento(
    resultado: str, nombre: str, banda: float | None = None, etiqueta_banda: str = ""
) -> None:
    """Estudio de evento de CS (como en CDA II) a tamaño de lámina."""
    d = _leer(f"cs_agg_municipio_trim_esc_{resultado}")
    d = d[d["tipo"] == "dynamic"].copy()
    d["e"] = d["termino"].astype(int)
    d = d[d["e"].between(*cdaii.VENTANA_EVENTO)].sort_values("e")

    fig, ax = plt.subplots(figsize=(5.7, 3.6))
    if banda is not None:
        ax.axhspan(-banda, banda, color=AZUL_BANDA, alpha=0.6, linewidth=0, zorder=0)
        ax.text(
            cdaii.VENTANA_EVENTO[0], banda, etiqueta_banda, va="bottom", fontsize=12, color=TINTA_2
        )
    ax.axhline(0, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.axvline(-0.5, color=TINTA_2, linewidth=0.8, linestyle=":", zorder=1)
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
    ax.plot(d["e"], d["valor"], "o", color=AZUL, markersize=5.5, zorder=3)
    ax.set_xlabel("Trimestres desde la primera sucursal")
    ax.set_ylabel("Sucursales por 10 mil adultos")
    ax.grid(axis="y", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, nombre)


def _filas_financieras(t: pd.DataFrame) -> pd.DataFrame:
    def de_tabla(variante: str, resultado: str, nombre: str) -> dict:
        r = _fila(t, variante=variante, panel="municipio_trim", resultado=resultado)
        escala = 100 / abs(r["media_base"])
        return {
            "nombre": nombre,
            "pct": r["efecto_pct"],
            "bajo": r["ic90_bajo"] * escala,
            "alto": r["ic90_alto"] * escala,
            "destacado": False,
        }

    tc = _fila(_leer("fase4_uso"), resultado="tarjetas_credito_bm_pc", variante="C4")
    pct, bajo, alto = _pct_ic(tc["valor"], tc["ee"], tc["media_base"])
    return pd.DataFrame(
        [
            de_tabla("principal", "sucursales_privado_pc", "Sucursales privadas"),
            de_tabla("principal", "sucursales_bm_pc", "Sucursales de banca múltiple"),
            de_tabla("principal", "sucursales_eacp_pc", "Sucursales de EACP"),
            de_tabla("panel_corto", "captacion_privado_pc", "Captación privada (2022T4+)"),
            de_tabla("panel_corto", "credito_privado_pc", "Crédito privado (2022T4+)"),
            {
                "nombre": "Tarjetas de crédito, banca múltiple",
                "pct": pct,
                "bajo": bajo,
                "alto": alto,
                "destacado": False,
            },
            de_tabla("eacp", "capt_ahorro_eacp_pc", "Captación de ahorro de EACP"),
            de_tabla("eacp", "cred_consumo_eacp_pc", "Crédito al consumo de EACP †"),
        ]
    )


def _filas_estimadores() -> pd.DataFrame:
    """Sucursales privadas con todos los estimadores de la fase 4 (respaldo de efectos fijos)."""
    est = _leer("fase4_estimadores").query("resultado == 'sucursales_privado_pc'")
    nombres = {
        "Callaway y Sant'Anna": ("Callaway y Sant'Anna (base)", False),
        "Sun y Abraham": ("Sun y Abraham", False),
        "Borusyak et al.": ("Borusyak et al.", False),
        "TWFE estático": ("TWFE estático", False),
        "TWFE estudio de evento (promedio e = 0…8)": ("Estudio de evento TWFE", False),
        "DiD apilado, id^pila + e": ("DiD apilado", False),
        "DiD apilado, id^pila + e^cve_ent^pila": ("DiD apilado, estado × evento", False),
        "TWFE extendido (Wooldridge) sin covariables": ("TWFE extendido sin covariables", False),
        "TWFE extendido (Wooldridge)": ("TWFE extendido con covariables", True),
        "TWFE extendido con covariables, solo municipios que abren": (
            "… solo municipios que abren",
            False,
        ),
    }
    filas = []
    for clave, (nombre, destacado) in nombres.items():
        r = _fila(est, estimador=clave)
        filas.append(
            {
                "nombre": nombre,
                "pct": r["efecto_pct"],
                "bajo": r["ic90_bajo"],
                "alto": r["ic90_alto"],
                "destacado": destacado,
            }
        )
    soporte = _fila(
        _leer("fase4_diagnostico_etwfe"),
        resultado="sucursales_privado_pc",
        muestra="soporte común (0.1 ≤ PS ≤ 0.9)",
        covariables=True,
    )
    reg = _fila(
        _leer("fase4_diagnostico_cs_metodo"), resultado="sucursales_privado_pc", metodo="reg"
    )
    for nombre, r, valor, destacado in (
        ("… con soporte común", soporte, "att", True),
        ("Callaway y Sant'Anna, ajuste lineal", reg, "att", False),
    ):
        pct, bajo, alto = _pct_ic(r[valor], r["ee"], r["media_base"])
        filas.append(
            {"nombre": nombre, "pct": pct, "bajo": bajo, "alto": alto, "destacado": destacado}
        )
    orden = [
        "Callaway y Sant'Anna (base)",
        "Sun y Abraham",
        "Borusyak et al.",
        "TWFE estático",
        "Estudio de evento TWFE",
        "DiD apilado",
        "DiD apilado, estado × evento",
        "TWFE extendido sin covariables",
        "Callaway y Sant'Anna, ajuste lineal",
        "TWFE extendido con covariables",
        "… con soporte común",
        "… solo municipios que abren",
    ]
    return pd.DataFrame(filas).set_index("nombre").loc[orden].reset_index()


# --- Uso, actividad y respaldo ------------------------------------------------------------------


def _creditos_por_100_cuentas() -> dict[str, float]:
    """Créditos por cada 100 cuentas de captación en 2025T4 (BDIF), del resumen de la app.

    Es la razón descriptiva de `docs/decisiones.md`, fase 5 (0.5 en la banca de desarrollo sin
    Banjército contra 61 en la banca múltiple de los mismos municipios), que calcula
    `app/datos/temas.py` (`make app-datos`). Aquí solo se divide.
    """
    if not USO_APP.exists():
        raise FileNotFoundError(f"falta {USO_APP}: corre `make app-datos`")
    uso = json.loads(USO_APP.read_text(encoding="utf-8"))
    ultimo = uso["banca_desarrollo"][-1]
    if ultimo["periodo"] != "2025Q4":
        log.warning("el último periodo de uso.json es %s, no 2025Q4", ultimo["periodo"])
    return {
        "periodo": ultimo["periodo"],
        "banco": 100 * ultimo["cred"] / ultimo["capt"],
        "banca_multiple": 100 * ultimo["cred_bm"] / ultimo["capt_bm"],
        "cajeros": uso["portafolio"]["cajeros"],
        "cajeros_solo_retiro": uso["portafolio"]["cajeros_solo_retiros"],
    }


def fig_uso(razon: dict[str, float]) -> None:
    """Barras horizontales: créditos por cada 100 cuentas, banco contra banca múltiple."""
    etiquetas = ["Banca múltiple", "Banco del Bienestar"]
    valores = [razon["banca_multiple"], razon["banco"]]
    colores = [GRIS, AZUL]
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.barh([1, 0], valores, height=0.55, color=colores, zorder=2)
    for y, v in zip([1, 0], valores, strict=True):
        ax.text(
            v + 1.2,
            y,
            f"{v:.1f}" if v < 10 else f"{v:.0f}",
            va="center",
            fontsize=16,
            fontweight="bold",
            color=TINTA,
        )
    ax.set_yticks([1, 0], etiquetas, color=TINTA, fontsize=14)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, max(valores) * 1.18)
    ax.set_xlabel(f"Créditos por cada 100 cuentas, {razon['periodo'].replace('Q', 'T')}")
    ax.grid(axis="x", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, "ppii_uso_creditos")


def _decaimiento() -> pd.DataFrame:
    d = _leer("decaimiento_estab_emprendimiento_pc")
    d = d[d["banda"].notna()].copy()
    d[["pct", "bajo", "alto"]] = d.apply(
        lambda r: pd.Series(_pct_ic(r["att"], r["ee"], r["media_base"])), axis=1
    )
    d["falla"] = d["pre_wald_p"] < 0.05
    return d


def fig_decaimiento(d: pd.DataFrame) -> None:
    """DENUE: efecto en la actualización de 2024 por distancia a la sucursal (IC al 90%)."""
    x = list(range(len(d)))
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.axhline(0, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.vlines(x, d["bajo"], d["alto"], color=TINTA, linewidth=1.6, zorder=2)
    ax.plot(
        x,
        d["pct"],
        "o",
        color=AZUL,
        markersize=9,
        markeredgecolor=FONDO,
        markeredgewidth=1.2,
        zorder=3,
    )
    for xi, (_, r) in zip(x, d.iterrows(), strict=True):
        ax.text(
            xi + 0.12, r["pct"], _pct(r["pct"]), va="center", ha="left", fontsize=13, color=TINTA
        )
    etiquetas = [b + (" †" if f else "") for b, f in zip(d["banda"], d["falla"], strict=True)]
    etiquetas = [e.replace("sucursal propia", "Con sucursal") for e in etiquetas]
    ax.set_xticks(x, etiquetas)
    ax.set_xlim(-0.4, len(d) - 0.4)
    ax.set_ylabel("Efecto (% de la media previa)")
    ax.grid(axis="y", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, "ppii_decaimiento")


def fig_balance(sop: pd.DataFrame) -> None:
    """Diferencia estandarizada máxima por cohorte antes y después de reponderar (DR)."""
    d = sop[sop["cohorte"].notna()].copy()
    d["etiqueta"] = d["cohorte"].astype(int).map(_periodo)
    x = list(range(len(d)))
    fig, ax = plt.subplots(figsize=(5.7, 3.5))
    ax.axhline(0.1, color=TINTA_2, linewidth=0.8, linestyle="--", zorder=1)
    ax.text(len(d) - 0.6, 0.1, "0.1", va="bottom", ha="right", fontsize=12, color=TINTA_2)
    ax.vlines(x, d["dif_max_ponderada"], d["dif_max_bruta"], color=REJILLA, linewidth=2, zorder=2)
    ax.plot(x, d["dif_max_bruta"], "o", color=GRIS, markersize=8, zorder=3)
    ax.plot(
        x,
        d["dif_max_ponderada"],
        "o",
        color=AZUL,
        markersize=8,
        markeredgecolor=FONDO,
        markeredgewidth=1.2,
        zorder=4,
    )
    ax.set_xticks(x, d["etiqueta"], rotation=45, ha="right", fontsize=12)
    ax.set_ylabel("Diferencia estandarizada máx.")
    ax.legend(
        handles=[
            Line2D([], [], marker="o", linestyle="", color=GRIS, markersize=8, label="Antes"),
            Line2D(
                [],
                [],
                marker="o",
                linestyle="",
                color=AZUL,
                markersize=8,
                label="Después de reponderar",
            ),
        ],
        loc="upper left",
        frameon=False,
        fontsize=13,
    )
    ax.grid(axis="y", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    _guardar(fig, "ppii_balance")


def _filas_heterogeneidad(het: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for resultado, panel, nombre in (
        ("sucursales_privado_pc", "municipio_trim", "Privadas"),
        ("estab_emprendimiento_pc", "localidad", "DENUE"),
    ):
        for grupo, sufijo in (("0", "con banca"), ("1", "desierto")):
            r = _fila(
                het.astype({"grupo": str}),
                dimension="desierto_bancario",
                panel=panel,
                resultado=resultado,
                grupo=grupo,
            )
            pct, bajo, alto = _pct_ic(r["att"], r["ee"], r["media_base"])
            filas.append(
                {
                    "nombre": f"{nombre}, {sufijo}",
                    "pct": pct,
                    "bajo": bajo,
                    "alto": alto,
                    "destacado": grupo == "1",
                }
            )
    return pd.DataFrame(filas)


# --- Cifras -------------------------------------------------------------------------------------


def _cota(r: pd.Series) -> str:
    return f"±{r['cota_equivalencia_pct']:.1f}%"


def _p(v: float) -> str:
    return "<0.001" if v < 0.001 else f"{v:.2f}"


def _cifras_planteamiento(t: pd.DataFrame, suc: pd.Series, mapa: dict, razon: dict) -> dict:
    m19 = pd.read_parquet(
        PROCESSED / "panel_municipio_trim.parquet", columns=["cve_mun", "periodo", "sucursales_bm"]
    ).query("periodo == '2019Q1'")
    priv = _fila(t, variante="principal", panel="municipio_trim", resultado="sucursales_privado_pc")
    return {
        "sucursales_2019": _num(suc.loc["2019Q1"], 0),
        "sucursales_2024": _num(suc.loc["2024Q4"], 0),
        "meta_sedena": _num(EXTERNAS["meta_sedena"], 0),
        "terminadas_2022": _num(EXTERNAS["terminadas_2022"], 0),
        "operando_2022": _num(EXTERNAS["operando_2022"], 0),
        "pct_sin_bm_2019": f"{100 * (m19['sucursales_bm'] == 0).mean():.0f}%",
        "n_municipios": _num(m19["cve_mun"].nunique(), 0),
        "n_tratadas": _num(priv["n_tratadas"], 0),
        "n_controles": _num(priv["n_controles"], 0),
        "mapa": mapa,
        "azteca_sucursales": _num(EXTERNAS["azteca_sucursales"], 0),
        "azteca_pct": EXTERNAS["azteca_pct"],
        "brasil_pct": EXTERNAS["brasil_pct"],
        "creditos_100_banco": f"{razon['banco']:.1f}",
        "creditos_100_bm": f"{razon['banca_multiple']:.0f}",
        "periodo_razon": razon["periodo"].replace("Q", "T"),
        "cajeros_banco": _num(razon["cajeros"], 0),
        "cajeros_solo_retiro": _num(razon["cajeros_solo_retiro"], 0),
    }


def _cifras_financieras(t: pd.DataFrame, sesoi: float) -> dict:
    def fila(variante: str, resultado: str) -> pd.Series:
        return _fila(t, variante=variante, panel="municipio_trim", resultado=resultado)

    priv, bm, eacp = (fila("principal", f"sucursales_{s}_pc") for s in ("privado", "bm", "eacp"))
    pe = fila("primera_etapa", "sucursales_total_pc")
    capt, cred = (fila("panel_corto", f"{s}_privado_pc") for s in ("captacion", "credito"))
    cred_eacp = fila("eacp", "cred_consumo_eacp_pc")
    banc = _fila(
        _leer("fase4_bancarizacion"),
        resultado="tarjetas_debito_bb_pc",
        estimador="Callaway y Sant'Anna",
    )
    # Uso del banco con los dos efectos estimados, no con la razón descriptiva de la fase 4.
    tx = _fila(
        _leer("fase4_bancarizacion"),
        resultado="transacciones_cajero_bb_pc",
        estimador="Callaway y Sant'Anna",
    )
    tc = _fila(_leer("fase4_uso"), resultado="tarjetas_credito_bm_pc", variante="C4")
    tc_pct, tc_bajo, tc_alto = _pct_ic(tc["valor"], tc["ee"], tc["media_base"])
    apilado = _fila(
        _leer("apilado_resumen"),
        resultado="cred_consumo_eacp_pc",
        controles="limpios (nunca + aún no tratados)",
    )
    sop = _leer("desc_soporte_comun")
    umbral = sop[sop["cohorte"].isna()].iloc[0]
    return {
        "pe_att": _num(pe["valor"], 2),
        "pe_ee": _num(pe["ee"], 2),
        "pe_wald_p": _p(pe["pre_wald_p"]),
        "tarjetas": _num(banc["valor"], 0),
        "tarjetas_ee": _num(banc["ee"], 0),
        "tarjetas_wald_p": _p(banc["pre_wald_p"]),
        "transacciones": _num(tx["valor"], 0),
        "transacciones_wald_p": _p(tx["pre_wald_p"]),
        "transacciones_por_tarjeta": f"{tx['valor'] / banc['valor']:.1f}",
        "priv_att": _num(priv["valor"], 3),
        "priv_ee": _num(priv["ee"], 3),
        "priv_pct": _pct(priv["efecto_pct"]),
        "priv_cota": _cota(priv),
        "priv_wald_p": _p(priv["pre_wald_p"]),
        "priv_rw": _p(priv["p_rw"]),
        "media_previa_priv": _num(priv["media_base"], 2),
        "bm_pct": _pct(bm["efecto_pct"]),
        "bm_cota": _cota(bm),
        "eacp_pct": _pct(eacp["efecto_pct"]),
        "eacp_cota": _cota(eacp),
        "capt_pct": _pct(capt["efecto_pct"]),
        "capt_cota": _cota(capt),
        "cred_pct": _pct(cred["efecto_pct"]),
        "cred_cota": _cota(cred),
        "corto_tratadas": _num(capt["n_tratadas"], 0),
        "corto_controles": _num(capt["n_controles"], 0),
        "tc_pct": _pct(tc_pct),
        "tc_cota": f"±{max(abs(tc_bajo), abs(tc_alto)):.1f}%",
        "cred_eacp_pct": _pct(cred_eacp["efecto_pct"]),
        "cred_eacp_apilado_wald_p": _p(apilado["pre_wald_p"]),
        "sesoi": f"±{sesoi:g}%",
        "sesoi_nivel": _num(umbral["umbral_por_10mil"], 3),
        "sesoi_sucursales": _num(umbral["umbral_sucursales_total"], 0),
    }


def _cifras_validez(t: pd.DataFrame) -> dict:
    est = _leer("fase4_estimadores").query("resultado == 'sucursales_privado_pc'")
    otros = est[
        est["estimador"].isin(
            [
                "TWFE estático",
                "Sun y Abraham",
                "Borusyak et al.",
                "DiD apilado, id^pila + e",
                "DiD apilado, id^pila + e^cve_ent^pila",
                "TWFE extendido (Wooldridge) sin covariables",
                "TWFE estudio de evento (promedio e = 0…8)",
            ]
        )
    ]
    placebo = _fila(
        _leer("fase4_validez"), resultado="sucursales_privado_pc", variante="A2_placebo"
    )
    honest = _fila(
        _leer("fase4_honest_sd").astype({"M": str}), resultado="sucursales_privado_pc", M="0.0"
    )
    rm = _leer("rob_honest_municipio_trim_esc_sucursales_privado_pc")
    rm = rm[rm["Mbar"].astype(str) == "0.25"].iloc[0]
    priv = _fila(t, variante="principal", panel="municipio_trim", resultado="sucursales_privado_pc")
    vecinos = _fila(_leer("fase4_validez"), resultado="sucursales_privado_pc", variante="A1b")
    diag = _leer("fase4_diagnostico_etwfe").query("resultado == 'sucursales_privado_pc'")
    etwfe = _fila(diag, muestra="completa", covariables=True)
    # Banca múltiple: los tres estimadores de efectos fijos que dan un efecto negativo.
    bm_fe = _leer("fase4_estimadores").query("resultado == 'sucursales_bm_pc'")
    bm_fe = bm_fe[
        bm_fe["estimador"].isin(
            [
                "TWFE estático",
                "Borusyak et al.",
                "TWFE extendido (Wooldridge) sin covariables",
            ]
        )
    ]
    return {
        "est_n": str(len(otros)),
        "est_min": _pct(otros["efecto_pct"].min()),
        "est_max": _pct(otros["efecto_pct"].max()),
        "placebo_pct": _pct(100 * placebo["valor"] / placebo["media_base"]),
        "perm_p": f"{_fila(_leer('fase4_permutacion'), resultado='sucursales_privado_pc')['p_permutacion']:.2f}",
        "honest_sd_bajo": _pct(honest["lb_pct"]),
        "honest_sd_alto": _pct(honest["ub_pct"]),
        "honest_rm025": f"±{100 * max(abs(rm['lb']), abs(rm['ub'])) / priv['media_base']:.0f}%",
        "vecinos_pct": _pct(100 * vecinos["valor"] / vecinos["media_base"]),
        "etwfe_cov_pct": _pct(etwfe["efecto_pct"]),
        "etwfe_cov_ee_pct": f"{100 * etwfe['ee'] / etwfe['media_base']:.1f}%",
        "etwfe_abren_pct": _pct(
            _fila(
                diag,
                muestra="solo municipios que alguna vez abren (hasta 2023T4)",
                covariables=True,
            )["efecto_pct"]
        ),
        "etwfe_soporte_pct": _pct(
            _fila(diag, muestra="soporte común (0.1 ≤ PS ≤ 0.9)", covariables=True)["efecto_pct"]
        ),
        "cs_reg_pct": _pct(
            _fila(
                _leer("fase4_diagnostico_cs_metodo"),
                resultado="sucursales_privado_pc",
                metodo="reg",
            )["efecto_pct"]
        ),
        "bm_fe_min": _pct(bm_fe["efecto_pct"].min()),
        "bm_fe_max": _pct(bm_fe["efecto_pct"].max()),
    }


def _cifras_poder() -> dict:
    """Efecto inyectado (exploratorio; `analisis/15_poder_inyectado.R`, `docs/decisiones.md`)."""
    diag = _leer("poder_inyectado_diagnostico").set_index("diseno")
    abren = diag.loc["barajadas_solo_abren"]
    detecta = _leer("poder_inyectado_calibrado").set_index("pct")["detecta"]

    def entero(v: float) -> str:
        return f"{int(100 * v + 1e-9)}%"

    return {
        "solo_abren_pct": _pct(abren["real_pct"]),
        "solo_abren_bajo": _pct(abren["real_pct"] - Z90 * abren["real_ee_pct"]),
        "solo_abren_alto": _pct(abren["real_pct"] + Z90 * abren["real_ee_pct"]),
        "solo_abren_p": f"{abren['p_randomizacion']:.2f}",
        "centro_nunca": _pct(diag.loc["barajadas_entre_tratadas", "centro_pct"]),
        "detecta_5_min": entero(detecta.loc[5].min()),
        "detecta_5_max": entero(detecta.loc[5].max()),
        "detecta_28_min": entero(detecta.loc[2.8].min()),
        "detecta_28_max": entero(detecta.loc[2.8].max()),
    }


def _cifras_uso() -> dict:
    uso = _leer("uso_resumen").set_index("resultado")
    capt, cred, tarj = (
        uso.loc[r] for r in ("capt_total_bd_pc", "cred_total_bd_pc", "tarjetas_debito_bd_pc")
    )
    return {
        "uso_capt": _num(capt["valor"], 0),
        "uso_capt_ee": _num(capt["ee"], 0),
        "uso_tarjetas": _num(tarj["valor"], 0),
        "uso_cred": _num(cred["valor"], 1),
        "uso_cred_ee": _num(cred["ee"], 1),
        "uso_cred_wald_p": _p(cred["pre_wald_p"]),
        "uso_tratadas": _num(capt["n_tratadas"], 0),
        "uso_controles": _num(capt["n_controles"], 0),
    }


def _cifras_actividad(t: pd.DataFrame, dec: pd.DataFrame, het: pd.DataFrame) -> dict:
    denue = _fila(t, panel="localidad", variante="principal", resultado="estab_emprendimiento_pc")
    ce = _fila(t, panel="municipio_ce", variante="ce", resultado="ue_pc")
    banda = dec.set_index("banda")
    contraste = _leer("decaimiento_estab_emprendimiento_pc").set_index("contraste")
    expo = het.query("dimension == 'exposicion' and resultado == 'estab_emprendimiento_pc'")
    expo = expo.assign(pct=100 * expo["att"] / expo["media_base"]).set_index("grupo")
    eic = _fila(_leer("fase2_resumen"), panel="municipio_eic", resultado="pct_negocio")
    return {
        "denue_pct": _pct(denue["efecto_pct"]),
        "denue_tratadas": _num(denue["n_tratadas"], 0),
        "denue_controles": _num(denue["n_controles"], 0),
        "dec_0_2": _pct(banda.loc["0–2 km", "pct"]),
        "dec_2_5": _pct(banda.loc["2–5 km", "pct"]),
        "dec_5_10": _pct(banda.loc["5–10 km", "pct"]),
        "dec_p_propia_0_2": _p(contraste.loc["sucursal propia − 0–2 km", "p_dif"]),
        "expo_temprana": _pct(expo.loc["temprana (hasta 2022S2)", "pct"]),
        "expo_tardia": _pct(expo.loc["tardía (2023S1–2024S1)", "pct"]),
        "expo_p": _p(expo.loc["temprana (hasta 2022S2)", "p_dif"]),
        "ce_pct": _pct(ce["efecto_pct"]),
        "ce_cota": _cota(ce),
        "ce_tratadas": _num(ce["n_tratadas"], 0),
        "eic_negocio": _num(eic["valor"], 1),
        "eic_alto": _pct(_pct_ic(eic["valor"], eic["ee"], eic["media_base"])[2]),
    }


def _cifras_respaldo(het: pd.DataFrame) -> dict:
    ctrl = _leer("fase4_controles").query("resultado == 'sucursales_privado_pc'")
    emp = ctrl[ctrl["variante"].str.startswith("H1d")].iloc[0]
    emp_pct, emp_bajo, emp_alto = _pct_ic(emp["att"], emp["ee"], emp["media_base"])
    rob = _leer("rob_localidad_act_estab_emprendimiento_pc")
    loc = rob[rob["variante"].str.startswith("muestra emparejada")].iloc[0]
    smd = _leer("balance_localidad_estab_emprendimiento_pc")["dif_est_despues"].abs().max()
    sop = _leer("desc_soporte_comun")
    coh = sop[sop["cohorte"].notna()].set_index(sop["cohorte"].dropna().astype(int))
    sin = _fila(
        _leer("desc_soporte_robustez"),
        resultado="sucursales_privado_pc",
        variante="sin las cohortes 20 y 21",
    )
    het_d = het.astype({"grupo": str}).query("dimension == 'desierto_bancario' and grupo == '1'")
    q_fin = het_d[het_d["panel"] == "municipio_trim"]
    q_fin = q_fin[q_fin["resultado"].str.startswith("sucursales_")]["q_dif"].min()
    q_denue = _fila(het_d, panel="localidad", resultado="estab_emprendimiento_pc")["q_dif"]
    f3 = _leer("fase3_resumen").set_index("resultado")
    delitos = f3[f3["panel"] == "municipio_delitos"]
    cotas = 100 * (delitos["valor"].abs() + Z90 * delitos["ee"]) / delitos["media_base"]
    # VIIRS: la comparación por calendario entre localidades con sucursal, la única que pasa la
    # pre-prueba (docs/decisiones.md, 2026-10-07); la de controles lejanos la reprueba.
    viirs = _leer("fase2_rob_extra_viirs_log1p_luz_1km")
    viirs = viirs[viirs["variante"] == "controles: solo con sucursal"].iloc[0]
    return {
        "emp_fin_pct": _pct(emp_pct),
        "emp_fin_cota": f"±{max(abs(emp_bajo), abs(emp_alto)):.1f}%",
        "emp_fin_n": _num(emp["tratadas"], 0),
        "emp_denue_pct": _pct(100 * loc["att"] / loc["media_base"]),
        "emp_denue_tratadas": _num(loc["tratadas"], 0),
        "emp_denue_controles": _num(loc["controles"], 0),
        "emp_denue_wald_p": _p(loc["pre_wald_p"]),
        "emp_denue_smd": f"{smd:.2f}",
        "balance_max_hasta_19": f"{coh.loc[13:19, 'dif_max_ponderada'].max():.2f}",
        "balance_20": f"{coh.loc[20, 'dif_max_ponderada']:.2f}",
        "balance_21": f"{coh.loc[21, 'dif_max_ponderada']:.2f}",
        "sin_desbalanceadas_pct": _pct(sin["efecto_pct"]),
        "sin_desbalanceadas_cota": f"±{sin['cota_ic90_pct']:.1f}%",
        "het_q_fin_min": f"{q_fin:.2f}",
        "het_q_denue": f"{q_denue:.2f}",
        "viirs": f"{100 * viirs['att']:+.2f}".replace("-", "−"),
        "viirs_ee": _num(100 * viirs["ee"], 2),
        "viirs_wald_p": _p(viirs["pre_wald_p"]),
        "robo_transeunte_pct": _pct(
            100
            * f3.loc["tasa_robo_transeunte", "valor"]
            / f3.loc["tasa_robo_transeunte", "media_base"]
        ),
        "homicidio_pct": _pct(
            100
            * f3.loc["tasa_homicidio_doloso", "valor"]
            / f3.loc["tasa_homicidio_doloso", "media_base"]
        ),
        "delitos_cota_min": f"{cotas.min():.0f}%",
        "delitos_cota_max": f"{cotas.max():.0f}%",
        "participacion": _num(f3.loc["pct_participacion", "valor"], 1),
        "participacion_wald_p": _p(f3.loc["pct_participacion", "pre_wald_p"]),
    }


def _het_pct(het: pd.DataFrame) -> dict:
    """Efecto por grupo de desierto bancario en % de la media de cada grupo."""
    filas = _filas_heterogeneidad(het).set_index("nombre")["pct"]
    return {
        "het_priv_con": _pct(filas["Privadas, con banca"]),
        "het_priv_sin": _pct(filas["Privadas, desierto"]),
        "het_denue_con": _pct(filas["DENUE, con banca"]),
        "het_denue_sin": _pct(filas["DENUE, desierto"]),
    }


# --- Generación ---------------------------------------------------------------------------------


def generar() -> Path:
    _estilo()
    sesoi = float(parametros()["estimacion"]["sesoi_pct"])
    t = _leer("tabla_final")
    het = _leer("het_q")
    priv = _fila(t, variante="principal", panel="municipio_trim", resultado="sucursales_privado_pc")

    suc = _sucursales_por_trimestre()
    fig_sucursales(suc)
    mapa = fig_mapa()
    fig_ecuacion()
    fig_evento("primera_etapa_sucursales_total_pc", "ppii_evento_primera_etapa")
    fig_evento(
        "sucursales_privado_pc",
        "ppii_evento_privadas",
        banda=sesoi / 100 * priv["media_base"],
        etiqueta_banda=f"±{sesoi:g}% de la media previa",
    )
    _forest(_filas_financieras(t), "ppii_efectos_financieros", (4.7, 3.85), (-9, 9), banda=sesoi)
    razon = _creditos_por_100_cuentas()
    fig_uso(razon)
    dec = _decaimiento()
    fig_decaimiento(dec)
    fig_balance(_leer("desc_soporte_comun"))
    _forest(_filas_estimadores(), "ppii_estimadores", (4.75, 4.0), (-6, 15), banda=sesoi)
    _forest(_filas_heterogeneidad(het), "ppii_heterogeneidad", (4.9, 3.6), (-12, 20))

    datos = {
        **_cifras_planteamiento(t, suc, mapa, razon),
        **_cifras_financieras(t, sesoi),
        **_cifras_validez(t),
        **_cifras_poder(),
        **_cifras_uso(),
        **_cifras_actividad(t, dec, het),
        **_cifras_respaldo(het),
        **_het_pct(het),
    }
    DESTINO_CIFRAS.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log.info("cifras en %s", DESTINO_CIFRAS)
    return DESTINO_CIFRAS


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

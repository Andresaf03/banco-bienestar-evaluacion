"""Paneles balanceados para diferencias en diferencias escalonadas.

Se construyen cuatro paneles con la misma estructura (`id, periodo, t, G, tratado, resultados,
covariables`) para poder correr el mismo código de estimación sobre los tres niveles de agregación
que pidió el asesor y comparar:

| panel | unidad | periodicidad | resultados |
|---|---|---|---|
| `panel_localidad`      | localidad (9 dígitos) | semestral  | DENUE: 4 bloques |
| `panel_municipio`      | municipio (5 dígitos) | semestral  | DENUE: 4 bloques |
| `panel_anillo`         | localidad × radio     | semestral  | DENUE dentro de 1/2/5/10 km |
| `panel_municipio_trim` | municipio             | trimestral | BDIF: financieras |

Definición del tratamiento (igual en los tres): `G` es el primer periodo con sucursal del Banco
del Bienestar en operación, **neta de Banjército**. A nivel localidad viene de
`tratamiento_localidad.parquet`; a nivel municipio, de `sucursales_bienestar.parquet`. `G = 0`
marca a los nunca tratados dentro de la ventana, como exige el paquete `did`.

Dos detalles que cambian los resultados y quedan explícitos:

1. **2023S1 no existe en el DENUE** (el INEGI no publicó versión). Las unidades cuya apertura cae
   en ese semestre se asignan al **primer periodo observado posterior** (2023S2): con datos
   semestrales no se puede distinguir el efecto dentro del hueco, y dejar `G` en un periodo que
   nadie observa rompe `att_gt`.
2. **Los ya tratados al inicio** (herencia Bansefi) se excluyen de la muestra principal, pero se
   conservan marcados (`ya_tratado_inicio`) para la especificación alterna tipo Fonseca y Matray.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.utils.io import INTERIM, PROCESSED, parametros
from proyecto.utils.periodos import periodo_a_t, rango, semestre_a_s

log = logging.getLogger(__name__)

P = parametros()
SALIDAS = {
    "localidad": PROCESSED / "panel_localidad.parquet",
    "municipio": PROCESSED / "panel_municipio.parquet",
    "anillo": PROCESSED / "panel_anillo.parquet",
    "municipio_trim": PROCESSED / "panel_municipio_trim.parquet",
    "municipio_trim_largo": PROCESSED / "panel_municipio_trim_largo.parquet",
    "municipio_ce": PROCESSED / "panel_municipio_ce.parquet",
}


# --------------------------------------------------------------------------- utilidades
def mapa_crosswalk() -> pd.Series:
    """`cve_mun` -> `cve_estable`: colapsa los 22 municipios creados después de 2010 en el
    municipio del que se desprendieron, para que la unidad sea comparable en todo el panel
    (decisión P-7). Sin esto, los municipios nuevos entran con periodos vacíos y `did` los
    descarta o, peor, los cuenta como controles con población desconocida."""
    cw = pd.read_parquet(
        INTERIM / "crosswalk_municipios.parquet", columns=["cve_mun", "cve_estable"]
    )
    return cw.set_index("cve_mun")["cve_estable"]


def aplicar_crosswalk(d: pd.DataFrame, columnas_suma: list[str], llaves: list[str]) -> pd.DataFrame:
    """Reemplaza `cve_mun` por la clave estable y suma los conteos de los municipios colapsados."""
    mapa = mapa_crosswalk()
    d = d.copy()
    d["cve_mun"] = d["cve_mun"].map(mapa).fillna(d["cve_mun"])
    columnas_suma = [c for c in columnas_suma if c in d.columns]
    otras = [c for c in d.columns if c not in columnas_suma + llaves]
    # `min_count=1` conserva el faltante cuando **todos** los valores del grupo son NaN: sin esto,
    # una variable que la BDIF no publica en un trimestre (captación y crédito por sector antes de
    # 2022T4) se convertiría en cero y produciría un salto artificial que el estimador leería como
    # efecto del tratamiento.
    agregado = d.groupby(llaves, observed=True)[columnas_suma].sum(min_count=1).reset_index()
    if otras:
        primeras = d.groupby(llaves, observed=True)[otras].first().reset_index()
        agregado = agregado.merge(primeras, on=llaves, how="left")
    return agregado


def semestres_observados() -> list[str]:
    """Semestres con versión del DENUE, en orden (sin el hueco de 2023S1)."""
    cob = pd.read_parquet(INTERIM / "denue_cobertura.parquet")
    completas = cob[cob["completa"]] if "completa" in cob.columns else cob
    if len(completas) < len(cob):
        log.warning(
            "se omiten %d versiones DENUE incompletas: %s",
            len(cob) - len(completas),
            ", ".join(cob.loc[~cob["completa"], "version"]),
        )
    return completas.sort_values("s")["semestre"].tolist()


def _g_efectivo(g_periodo: pd.Series, periodos: list[str], indice) -> pd.Series:
    """Lleva `G` al primer periodo **observado** que sea >= G; 0 si nunca o si cae fuera.

    Necesario por el hueco de 2023S1 en el DENUE y porque las aperturas posteriores al último
    periodo del panel equivalen a "no tratado dentro de la ventana".
    """

    def mapear(g):
        if not isinstance(g, str):
            return 0
        candidatos = [p for p in periodos if p >= g]
        return indice(candidatos[0]) if candidatos else 0

    return g_periodo.map(mapear).astype(int)


def _pivotar_denue(d: pd.DataFrame, llave: str) -> pd.DataFrame:
    """De formato largo (bloque, clase) a columnas `estab_<bloque>`, `micro_<bloque>`, etc."""
    por_bloque = (
        d.groupby([llave, "semestre", "bloque"], observed=True)[
            ["n_estab", "n_micro", "empleo_est"]
        ]
        .sum()
        .reset_index()
    )
    ancho = por_bloque.pivot(index=[llave, "semestre"], columns="bloque")
    ancho.columns = [f"{a}_{b}" for a, b in ancho.columns]
    ancho = ancho.rename(
        columns=lambda c: c.replace("n_estab_", "estab_").replace("n_micro_", "micro_")
    )
    # Clases finas de interés directo para los bloques de consumo y salud.
    clases = {
        "farmacia": "estab_farmacia",
        "restaurantes": "estab_restaurantes",
        "abarrotes_alimentos": "estab_abarrotes",
        "consultorios": "estab_consultorios",
        "banca_multiple": "estab_banca",
        "cajas_ahorro": "estab_cajas",
    }
    for clase, nombre in clases.items():
        serie = (
            d[d["clase"] == clase]
            .groupby([llave, "semestre"], observed=True)["n_estab"]
            .sum()
            .rename(nombre)
        )
        ancho = ancho.join(serie, how="left")
    return ancho.reset_index()


def _tasas(panel: pd.DataFrame, poblacion: str, por_cada: int) -> pd.DataFrame:
    """Añade `<variable>_pc`: conteo por cada `por_cada` habitantes."""
    base = panel[poblacion].replace(0, np.nan)
    columnas = [c for c in panel.columns if c.startswith(("estab_", "micro_", "empleo_"))]
    for c in columnas:
        panel[f"{c}_pc"] = panel[c] / base * por_cada
    return panel


# --------------------------------------------------------------------------- paneles
def panel_localidad() -> Path:
    periodos = semestres_observados()
    loc = pd.read_parquet(INTERIM / "denue_localidad.parquet")
    loc = loc[loc["semestre"].isin(periodos)]
    censo = pd.read_parquet(INTERIM / "inegi_censo_localidades_2020.parquet")
    trat = pd.read_parquet(INTERIM / "tratamiento_localidad.parquet")

    # El piso de población aplica a **todas** las localidades, con sucursal o sin ella. Exentar a las
    # tratadas metía localidades de 1 a 7 habitantes cuya tasa por mil es apalancamiento puro, y
    # volvía asimétrica cualquier robustez "sin piso": los controles bajo el piso nunca entraban al
    # marco, así que quitar el filtro en R solo reincorporaba tratadas diminutas.
    minimo = P["unidades"]["localidad_pob_minima"]
    marco = censo[censo["pobtot"] >= minimo]
    fuera = int((~trat["cve_loc"].isin(marco["cve_loc"])).sum())
    log.info("piso de %d habitantes: %d localidades con sucursal quedan fuera", minimo, fuera)
    marco = marco[["cve_loc", "cve_mun", "nom_loc", "lat", "lon", "pobtot"]]
    if P["unidades"]["localidad_requiere_denue"]:
        con_denue = set(loc["cve_loc"].unique())
        marco = marco[marco["cve_loc"].isin(con_denue)]

    esqueleto = marco.merge(pd.DataFrame({"semestre": periodos}), how="cross")
    ancho = _pivotar_denue(loc, "cve_loc")
    panel = esqueleto.merge(ancho, on=["cve_loc", "semestre"], how="left")
    cols_conteo = [c for c in panel.columns if c.startswith(("estab_", "micro_", "empleo_"))]
    panel[cols_conteo] = panel[cols_conteo].fillna(0)

    panel["s"] = panel["semestre"].map(semestre_a_s)
    t = trat.set_index("cve_loc")
    panel["G_semestre"] = panel["cve_loc"].map(t["G_semestre"])
    panel["G"] = _g_efectivo(panel["G_semestre"], periodos, semestre_a_s)
    panel["tratado"] = ((panel["G"] > 0) & (panel["s"] >= panel["G"])).astype(int)
    for bandera in ("fecha_ambigua", "ya_tratado_inicio", "sospechoso_banjercito"):
        panel[bandera] = panel["cve_loc"].map(t[bandera]).fillna(False).astype(bool)
    panel["n_sucursales_loc"] = panel["cve_loc"].map(t["n_sucursales_loc"]).fillna(0).astype(int)
    panel = panel.merge(_exposicion_espacial(marco, trat, periodos), on="cve_loc", how="left")

    # 8 de cada 10 localidades del marco no tienen ningún establecimiento en el DENUE (son
    # rancherías). Se conservan porque el cero es un dato válido y son controles legítimos, pero
    # se marca cuáles tuvieron actividad alguna vez para poder restringir la muestra en robustez.
    con_actividad = panel.groupby("cve_loc")["estab_emprendimiento"].transform("max") > 0
    panel["con_actividad"] = con_actividad.astype(bool)
    panel = _tasas(panel, "pobtot", P["resultados"]["por_cada_localidad"])
    panel = _agregar_covariables_localidad(panel, periodos)
    panel = _agregar_tamano_cohorte(panel, "cve_loc")
    panel = panel.sort_values(["cve_loc", "s"]).reset_index(drop=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(SALIDAS["localidad"], index=False, compression="zstd")
    _log_panel("localidad", panel, "cve_loc")
    return SALIDAS["localidad"]


def _exposicion_espacial(
    marco: pd.DataFrame, trat: pd.DataFrame, periodos: list[str], bloque: int = 2000
) -> pd.DataFrame:
    """Exposición de cada localidad a una sucursal del Banco del Bienestar que **no** es la suya.

    La fecha de tratamiento es municipal y la localidad tratada es la que tiene la sucursal, así que
    las localidades vecinas quedaban como "nunca tratadas" aunque la sucursal les quede a pocos
    kilómetros: el 91% de los controles estaba en un municipio que abrió una sucursal. Estas columnas
    permiten definir controles limpios (`leer_panel(controles = ...)` en R) y estimar el derrame:

    - `dist_bb_km`: km a la localidad con sucursal más cercana distinta de la propia. Se usa el punto
      de la localidad asignada a cada sucursal (mediana de 0.41 km a la sucursal real).
    - `G_vecina`: G semestral de esa localidad vecina si su fecha es identificable (no ambigua, no
      heredada de Bansefi, no sospechosa de Banjército); 0 si no lo es.
    - `mun_con_apertura`: el municipio abrió al menos una sucursal entre `periodo.inicio` y
      `periodo.fin` (serie municipal neta de Banjército).
    - `es_cabecera`: cabecera municipal (clave de localidad terminada en 0001).
    """
    from proyecto.construccion.tratamiento_localidad import haversine_km

    suc = trat.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    fechable = (
        suc["G_semestre"].notna()
        & ~suc["fecha_ambigua"].fillna(False).astype(bool)
        & ~suc["ya_tratado_inicio"].fillna(False).astype(bool)
        & ~suc["sospechoso_banjercito"].fillna(False).astype(bool)
    )
    g_suc = _g_efectivo(suc["G_semestre"].where(fechable), periodos, semestre_a_s).to_numpy()
    lat_s, lon_s = suc["lat"].to_numpy(float), suc["lon"].to_numpy(float)
    cve_s = suc["cve_loc"].to_numpy()

    locs = marco.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    lat_l, lon_l = locs["lat"].to_numpy(float), locs["lon"].to_numpy(float)
    cve_l = locs["cve_loc"].to_numpy()
    dist = np.empty(len(locs))
    cercana = np.empty(len(locs), dtype=int)
    for i in range(0, len(locs), bloque):
        j = slice(i, i + bloque)
        d = haversine_km(lat_l[j, None], lon_l[j, None], lat_s[None, :], lon_s[None, :])
        d[cve_l[j, None] == cve_s[None, :]] = np.inf  # la sucursal propia no cuenta
        k = d.argmin(axis=1)
        cercana[j] = k
        dist[j] = d[np.arange(len(k)), k]

    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    inicio, fin = P["periodo"]["inicio"], P["periodo"]["fin"]
    sb = sb[(sb["periodo"] >= inicio) & (sb["periodo"] <= fin)]
    piv = sb.pivot_table(
        index="cve_mun", columns="periodo", values="suc_bienestar", aggfunc="sum"
    ).fillna(0)
    con_apertura = set(piv.index[(piv.diff(axis=1) > 0).any(axis=1)])

    salida = pd.DataFrame(
        {
            "cve_loc": cve_l,
            "dist_bb_km": dist,
            "G_vecina": g_suc[cercana].astype(int),
        }
    )
    salida = marco[["cve_loc", "cve_mun"]].merge(salida, on="cve_loc", how="left")
    salida["G_vecina"] = salida["G_vecina"].fillna(0).astype(int)
    salida["mun_con_apertura"] = salida["cve_mun"].isin(con_apertura)
    salida["es_cabecera"] = salida["cve_loc"].str.endswith("0001")
    log.info(
        "exposición: dist_bb_km mediana %.1f km; localidades a >=10 km %d de %d; municipios con "
        "apertura %d",
        np.nanmedian(salida["dist_bb_km"]),
        int((salida["dist_bb_km"] >= 10).sum()),
        len(salida),
        len(con_apertura),
    )
    return salida.drop(columns="cve_mun")


def _banca_multiple_inicio(estable: bool) -> pd.Series:
    """`cve_mun` -> 1 si el municipio tenía sucursal de banca múltiple en `periodo.inicio` (BDIF).

    Sale de la BDIF y no del DENUE: el SCIAN 52 del DENUE tiene rupturas de cobertura de hasta +41%
    (2018S1), así que "sin banca" en el DENUE de 2016 mezclaba desiertos reales con subregistro.
    `estable=True` colapsa los municipios nuevos en su municipio de origen (paneles municipales).
    """
    inicio = P["periodo"]["inicio"]
    b = pd.read_parquet(
        INTERIM / "cnbv_bdif.parquet", columns=["cve_mun", "periodo", "sector", "variable", "valor"]
    )
    b = b[
        (b["periodo"] == inicio)
        & (b["variable"] == "sucursales")
        & (b["sector"] == "banca_multiple")
    ]
    if estable:
        b = b.assign(cve_mun=b["cve_mun"].map(mapa_crosswalk()).fillna(b["cve_mun"]))
    return (b.groupby("cve_mun")["valor"].sum() > 0).astype(int)


def _covariables_en_logaritmos(
    panel: pd.DataFrame, poblacion: str, previos: str | None
) -> pd.DataFrame:
    """Transformaciones para el modelo de propensión y de resultado del estimador DR.

    En escala cruda la población llega a cientos de miles y los establecimientos previos a miles,
    frente a controles casi todos en cero: el logit del PS se vuelve extremo y el error estándar de
    CS se multiplicaba por cuatro. En logaritmos el ajuste es estable y la interpretación, la misma.
    """
    panel["log_poblacion_2020"] = np.log(panel[poblacion].where(panel[poblacion] > 0))
    if previos is not None:
        panel["log1p_estab_previos"] = np.log1p(panel[previos])
    return panel


def _agregar_covariables_localidad(panel: pd.DataFrame, periodos: list[str]) -> pd.DataFrame:
    """Covariables previas al tratamiento, fijas por unidad (medidas en el primer periodo)."""
    base = panel[panel["semestre"] == periodos[0]].set_index("cve_loc")
    previas = pd.DataFrame(index=base.index)
    previas["estab_previos"] = base.get("estab_emprendimiento", 0)
    banca = base["cve_mun"].map(_banca_multiple_inicio(estable=False)).fillna(0).astype(int)
    previas["banca_mun_2019"] = banca
    previas["desierto_bancario"] = 1 - banca
    marg = pd.read_parquet(INTERIM / "conapo_marginacion.parquet")
    marg = marg[marg["anio"] == 2020].set_index("cve_mun")
    previas["indice_marginacion_2020"] = base["cve_mun"].map(marg["im"])
    previas["grado_marginacion_2020"] = base["cve_mun"].map(marg["gm"])
    previas["poblacion_2020"] = base["pobtot"]
    previas = _covariables_en_logaritmos(previas, "poblacion_2020", "estab_previos")
    return panel.merge(previas.reset_index(), on="cve_loc", how="left")


def panel_municipio() -> Path:
    periodos = semestres_observados()
    mun = pd.read_parquet(INTERIM / "denue_municipio.parquet")
    mun = mun[mun["semestre"].isin(periodos)]
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    pobm = pd.read_parquet(
        INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot"]
    ).set_index("cve_mun")["pobtot"]

    marco = pd.DataFrame({"cve_mun": sorted(mun["cve_mun"].unique())})
    esqueleto = marco.merge(pd.DataFrame({"semestre": periodos}), how="cross")
    ancho = _pivotar_denue(mun, "cve_mun")
    panel = esqueleto.merge(ancho, on=["cve_mun", "semestre"], how="left")
    cols_conteo = [c for c in panel.columns if c.startswith(("estab_", "micro_", "empleo_"))]
    panel[cols_conteo] = panel[cols_conteo].fillna(0)
    panel = aplicar_crosswalk(panel, cols_conteo, ["cve_mun", "semestre"])
    panel["s"] = panel["semestre"].map(semestre_a_s)
    panel["pobtot"] = panel["cve_mun"].map(pobm)

    g_mun, ya, sosp = _tratamiento_municipal(sb)
    panel["G_semestre"] = panel["cve_mun"].map(g_mun)
    panel["G"] = _g_efectivo(panel["G_semestre"], periodos, semestre_a_s)
    panel["tratado"] = ((panel["G"] > 0) & (panel["s"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sosp).fillna(False).astype(bool)

    panel = _tasas(panel, "pobtot", P["resultados"]["por_cada_municipio"])
    marg = pd.read_parquet(INTERIM / "conapo_marginacion.parquet")
    marg = marg[marg["anio"] == 2020].set_index("cve_mun")
    panel["indice_marginacion_2020"] = panel["cve_mun"].map(marg["im"])
    panel["grado_marginacion_2020"] = panel["cve_mun"].map(marg["gm"])
    panel["poblacion_2020"] = panel["pobtot"]
    # Mismas covariables previas que en el panel de localidades, medidas en el primer semestre.
    previos = panel.loc[panel["semestre"] == periodos[0]].set_index("cve_mun")[
        "estab_emprendimiento"
    ]
    panel["estab_previos"] = panel["cve_mun"].map(previos)
    banca = panel["cve_mun"].map(_banca_multiple_inicio(estable=True)).fillna(0).astype(int)
    panel["banca_mun_2019"] = banca
    panel["desierto_bancario"] = 1 - banca
    panel = _covariables_en_logaritmos(panel, "poblacion_2020", "estab_previos")
    panel = _agregar_tamano_cohorte(panel, "cve_mun")
    panel = panel.sort_values(["cve_mun", "s"]).reset_index(drop=True)
    panel.to_parquet(SALIDAS["municipio"], index=False, compression="zstd")
    _log_panel("municipio", panel, "cve_mun")
    return SALIDAS["municipio"]


def _tratamiento_trimestral(sb: pd.DataFrame, fin: str | None = None):
    """Primer trimestre con sucursal, `ya_tratado_inicio` y `sospechoso` por municipio.

    Serie neta de Banjército, con los municipios nuevos colapsados en su municipio de origen. Es la
    única definición del tratamiento municipal: la usan el panel semestral y el trimestral. `fin`
    extiende la ventana de fechado (el panel trimestral llega a `periodo.fin_trimestral`).
    """
    inicio_q, fin_q = P["periodo"]["inicio"], fin or P["periodo"]["fin"]
    ventana = sb[(sb["periodo"] >= inicio_q) & (sb["periodo"] <= fin_q)].copy()
    ventana["cve_mun"] = ventana["cve_mun"].map(mapa_crosswalk()).fillna(ventana["cve_mun"])
    piv = ventana.groupby(["cve_mun", "periodo"])["suc_bienestar"].sum().unstack("periodo")
    tratado = piv.fillna(0) >= P["tratamiento"]["umbral"]
    primer_q = tratado.idxmax(axis=1).where(tratado.any(axis=1))
    sospechoso = sb.groupby("cve_mun")["sospechoso_banjercito_nuevo"].first()
    return primer_q, tratado[inicio_q], sospechoso


def _tratamiento_municipal(sb: pd.DataFrame):
    """`G` en semestres, `ya_tratado_inicio` y `sospechoso` por municipio (serie neta de Banjército)."""
    from proyecto.utils.periodos import periodo_a_semestre

    primer_q, ya, sospechoso = _tratamiento_trimestral(sb)
    g_sem = primer_q.map(lambda q: periodo_a_semestre(q) if isinstance(q, str) else pd.NA)
    return g_sem, ya, sospechoso


def panel_anillo() -> Path:
    periodos = semestres_observados()
    anillos = pd.read_parquet(INTERIM / "anillos.parquet")
    cob = pd.read_parquet(INTERIM / "denue_cobertura.parquet").set_index("version")
    anillos["semestre"] = anillos["version"].map(cob["semestre"])
    anillos = anillos[anillos["semestre"].isin(periodos)]

    ancho = anillos.pivot_table(
        index=["cve_loc", "radio_km", "semestre"],
        columns="bloque",
        values=["n_estab", "n_micro"],
        aggfunc="sum",
    )
    ancho.columns = [f"{'estab' if a == 'n_estab' else 'micro'}_{b}" for a, b in ancho.columns]
    panel = ancho.reset_index()
    panel["s"] = panel["semestre"].map(semestre_a_s)

    trat = pd.read_parquet(INTERIM / "tratamiento_localidad.parquet").set_index("cve_loc")
    censo = pd.read_parquet(INTERIM / "inegi_censo_localidades_2020.parquet").set_index("cve_loc")
    panel["G_semestre"] = panel["cve_loc"].map(trat["G_semestre"])
    panel["G"] = _g_efectivo(panel["G_semestre"], periodos, semestre_a_s)
    panel["tratado"] = ((panel["G"] > 0) & (panel["s"] >= panel["G"])).astype(int)
    for bandera in ("fecha_ambigua", "ya_tratado_inicio", "sospechoso_banjercito"):
        panel[bandera] = panel["cve_loc"].map(trat[bandera]).fillna(False).astype(bool)
    panel["cve_mun"] = panel["cve_loc"].str[:5]
    panel["pobtot"] = panel["cve_loc"].map(censo["pobtot"])
    panel = _tasas(panel, "pobtot", P["resultados"]["por_cada_localidad"])
    panel = _agregar_tamano_cohorte(panel, "cve_loc")
    panel = panel.sort_values(["cve_loc", "radio_km", "s"]).reset_index(drop=True)
    panel.to_parquet(SALIDAS["anillo"], index=False, compression="zstd")
    log.info(
        "panel anillo: %d filas, %d localidades × %d radios × %d semestres; tratadas %d",
        len(panel),
        panel["cve_loc"].nunique(),
        panel["radio_km"].nunique(),
        panel["semestre"].nunique(),
        int(panel.loc[panel["s"] == panel["s"].min(), "G"].gt(0).sum()),
    )
    return SALIDAS["anillo"]


def panel_municipio_trim(largo: bool = False) -> Path:
    """Panel trimestral con los resultados financieros de la BDIF (`resultados.series_bdif`).

    Va de `periodo.inicio` (2019T1) a `periodo.fin_trimestral` (2025T4). Con `largo=True` arranca
    en `periodo.robustez_inicio` (2016T1), para la robustez con pre-periodo extendido: `t` y `G` se
    cuentan desde ese trimestre (t = 1 en 2016T1), mientras que el tratamiento, los ya tratados y
    las covariables siguen definidos en 2019T1.
    """
    inicio, fin = P["periodo"]["inicio"], P["periodo"]["fin_trimestral"]
    arranque = P["periodo"]["robustez_inicio"] if largo else inicio
    periodos = rango(arranque, fin)
    b = pd.read_parquet(INTERIM / "cnbv_bdif.parquet")
    b = b[b["periodo"].isin(periodos)]
    series = P["resultados"]["series_bdif"]
    nombres = [s["nombre"] for s in series]

    def suma(serie: dict) -> pd.DataFrame:
        d = b[(b["variable"] == serie["variable"]) & (b["sector"].isin(serie["sectores"]))]
        return (
            d.groupby(["cve_mun", "periodo"], observed=True)["valor"]
            .sum()
            .rename(serie["nombre"])
            .reset_index()
        )

    piezas = [suma(s) for s in series]
    vacias = [s["nombre"] for s, p_ in zip(series, piezas, strict=True) if p_.empty]
    if vacias:
        raise ValueError(f"series de la BDIF sin datos: {', '.join(vacias)}")
    # Esqueleto balanceado: todos los municipios observados × todos los trimestres. Sin esto,
    # `did` descarta unidades con periodos faltantes (municipios de creación reciente).
    municipios = sorted(set().union(*(set(p_["cve_mun"]) for p_ in piezas)))
    panel = pd.DataFrame({"cve_mun": municipios}).merge(
        pd.DataFrame({"periodo": periodos}), how="cross"
    )
    for p_ in piezas:
        panel = panel.merge(p_, on=["cve_mun", "periodo"], how="left")
    # Un municipio ausente en un trimestre que la BDIF sí publica es un cero real (no tiene esa
    # infraestructura). Antes del primer trimestre en que la variable se publica con esta
    # desagregación queda NaN: cajeros, TPV, transacciones, captación y crédito por sector solo
    # existen desde 2022T4. Rellenar cajeros y TPV con cero desde 2019 producía un salto nacional de 0
    # a 62 mil cajeros en 2022T4 que el estimador leía como efecto del tratamiento.
    for p_ in piezas:
        c = p_.columns[-1]
        desde = p_["periodo"].min()
        publicado = panel["periodo"] >= desde
        panel.loc[publicado, c] = panel.loc[publicado, c].fillna(0)

    pob = pd.read_parquet(
        INTERIM / "cnbv_bdif_poblacion.parquet", columns=["cve_mun", "periodo", "poblacion_adulta"]
    )
    panel = panel.merge(pob, on=["cve_mun", "periodo"], how="left")
    # Municipios creados después de 2010: se colapsan en su municipio de origen (decisión P-7).
    panel = aplicar_crosswalk(panel, [*nombres, "poblacion_adulta"], ["cve_mun", "periodo"])

    def indice(periodo: str) -> int:
        return periodo_a_t(periodo, base=arranque, valor_base=1)

    panel["t"] = panel["periodo"].map(indice)
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    primer, ya, sospechoso = _tratamiento_trimestral(sb, fin)
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    panel["G"] = _g_efectivo(panel["G_trimestre"], periodos, indice)
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)

    # Covariables previas para el estimador doblemente robusto y para el emparejamiento.
    marg = pd.read_parquet(INTERIM / "conapo_marginacion.parquet")
    marg = marg[marg["anio"] == 2020].set_index("cve_mun")
    panel["indice_marginacion_2020"] = panel["cve_mun"].map(marg["im"])
    panel["grado_marginacion_2020"] = panel["cve_mun"].map(marg["gm"])
    pobc = pd.read_parquet(INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot"])
    panel["poblacion_2020"] = panel["cve_mun"].map(pobc.set_index("cve_mun")["pobtot"])
    base_inicio = panel[panel["periodo"] == inicio].set_index("cve_mun")
    panel["banca_mun_2019"] = (
        panel["cve_mun"].map(base_inicio["sucursales_bm"] > 0).fillna(False).astype(int)
    )
    panel["desierto_bancario"] = 1 - panel["banca_mun_2019"]
    panel = _covariables_en_logaritmos(panel, "poblacion_2020", None)

    # Denominador **fijo** por municipio: la población adulta de la BDIF cambia de fuente dentro del
    # panel (proyección CONAPO hasta 2020T3, Censo 2020 desde 2020T4), con saltos municipales de −20%
    # a +13% en 2020T4. Con un denominador que se mueve, la tasa salta aunque el conteo no cambie, y
    # ese escalón cae en el pre-periodo. Fijarlo en el trimestre de config (base Censo 2020) hace de
    # la tasa un reescalamiento por unidad que no altera la dinámica.
    por_cada = P["resultados"]["por_cada_municipio"]
    fijo = P["resultados"]["denominador_municipio_periodo"]
    pob_fija = panel.loc[panel["periodo"] == fijo].set_index("cve_mun")["poblacion_adulta"]
    panel["poblacion_adulta_fija"] = panel["cve_mun"].map(pob_fija)
    base = panel["poblacion_adulta_fija"].replace(0, np.nan)
    for c in nombres:
        panel[f"{c}_pc"] = panel[c] / base * por_cada
    panel = _agregar_imss_y_remesas(panel, por_cada)
    panel = _agregar_tamano_cohorte(panel, "cve_mun")
    panel = panel.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    salida = SALIDAS["municipio_trim_largo" if largo else "municipio_trim"]
    panel.to_parquet(salida, index=False, compression="zstd")
    _log_panel(
        "municipio trimestral" + (" largo" if largo else ""), panel, "cve_mun", periodo="periodo"
    )
    return salida


def _agregar_imss_y_remesas(panel: pd.DataFrame, por_cada: int) -> pd.DataFrame:
    """Resultados de la fase 1 medidos cada trimestre: empleo formal (IMSS) y remesas (Banxico).

    - IMSS: puestos afiliados, en micro (1–5 puestos) y pequeños (6–50) registros patronales, por
      diez mil adultos con el mismo denominador fijo; salario diario promedio en logaritmo (la masa
      salarial entre los puestos). Un municipio ausente en un trimestre del IMSS no tiene puestos
      afiliados: cero, solo en los trimestres que el IMSS publica.
    - Remesas: dólares por adulto. Sin serie de Banxico el municipio queda en NaN (no se inventa
      un cero).
    Si los archivos intermedios no existen todavía, el panel se construye sin estas columnas.
    """
    base = panel["poblacion_adulta_fija"].replace(0, np.nan)
    ruta_imss = INTERIM / "imss_municipio.parquet"
    if ruta_imss.exists():
        imss = pd.read_parquet(ruta_imss)
        panel = panel.merge(imss, on=["cve_mun", "periodo"], how="left")
        publicado = panel["periodo"].isin(set(imss["periodo"]))
        for c in ["asegurados", "ta", "masa_sal_ta", "ta_micro", "ta_pequena"]:
            panel.loc[publicado, c] = panel.loc[publicado, c].fillna(0)
        for c in ["ta", "ta_micro", "ta_pequena"]:
            panel[f"{c}_pc"] = panel[c] / base * por_cada
        panel["log_salario_diario"] = np.log(
            (panel["masa_sal_ta"] / panel["ta"]).where(panel["ta"] > 0)
        )
    else:
        log.warning("sin imss_municipio.parquet: el panel no trae empleo formal")
    ruta_remesas = INTERIM / "remesas_municipio.parquet"
    if ruta_remesas.exists():
        remesas = pd.read_parquet(ruta_remesas)
        panel = panel.merge(remesas, on=["cve_mun", "periodo"], how="left")
        panel["remesas_usd_adulto"] = panel["remesas_musd"] * 1e6 / base
    else:
        log.warning("sin remesas_municipio.parquet: el panel no trae remesas")
    return panel


def panel_municipio_ce() -> Path:
    """Panel municipal de los Censos Económicos 2004–2024 (fase 1), un corte por censo.

    Diseño de una sola cohorte, como el del DENUE entre actualizaciones, pero con el censo mismo:
    tratadas = primera sucursal entre `ce.inicio_tratamiento` y `ce.fin_exposicion` (expuestas
    durante el año de referencia del CE 2024), fechadas en el último corte (G = 5); las aperturas
    posteriores quedan marcadas (`apertura_posterior_ce`) y fuera de la muestra principal, porque
    su exposición es parcial. Los cortes 2004→2009→2014→2019 dan tres placebos. Unidades por mil
    habitantes (Censo 2020, fijo) y montos en logaritmo (los efectos fijos de censo absorben la
    inflación común).
    """
    cfg = P["ce"]
    ce = pd.read_parquet(INTERIM / "inegi_ce_municipio.parquet")
    anios = sorted(ce["anio_censo"].unique())
    marco = pd.DataFrame({"cve_mun": sorted(ce["cve_mun"].unique())})
    panel = marco.merge(pd.DataFrame({"anio_censo": anios}), how="cross")
    panel = panel.merge(ce, on=["cve_mun", "anio_censo"], how="left")
    panel["t"] = panel["anio_censo"].map({a: i for i, a in enumerate(anios, start=1)})

    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    primer, ya, sospechoso = _tratamiento_trimestral(sb, P["periodo"]["fin_trimestral"])
    panel["G_trimestre"] = panel["cve_mun"].map(primer)
    tratada = panel["G_trimestre"].between(cfg["inicio_tratamiento"], cfg["fin_exposicion"])
    panel["G"] = np.where(tratada, len(anios), 0).astype(int)
    panel["apertura_posterior_ce"] = panel["G_trimestre"].gt(cfg["fin_exposicion"]).fillna(False)
    panel["exposicion_ce"] = np.select(
        [~tratada, panel["G_trimestre"].le(cfg["fin_exposicion_temprana"])],
        ["control", "temprana"],
        "tardía",
    )
    panel["tratado"] = ((panel["G"] > 0) & (panel["t"] >= panel["G"])).astype(int)
    panel["ya_tratado_inicio"] = panel["cve_mun"].map(ya).fillna(False).astype(bool)
    panel["sospechoso_banjercito"] = panel["cve_mun"].map(sospechoso).fillna(False).astype(bool)

    pobm = pd.read_parquet(INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun", "pobtot"])
    pobm = aplicar_crosswalk(pobm.assign(llave=1), ["pobtot"], ["cve_mun", "llave"])
    panel["pobtot"] = panel["cve_mun"].map(pobm.set_index("cve_mun")["pobtot"])
    por_cada = cfg["por_cada"]
    base = panel["pobtot"].replace(0, np.nan)
    for c in ["ue", "personal_ocupado"]:
        panel[f"{c}_pc"] = panel[c] / base * por_cada
    for c in ["remuneraciones", "vacb", "produccion_bruta"]:
        panel[f"log_{c}"] = np.log(panel[c].where(panel[c] > 0))

    marg = pd.read_parquet(INTERIM / "conapo_marginacion.parquet")
    marg = marg[marg["anio"] == 2020].set_index("cve_mun")
    panel["indice_marginacion_2020"] = panel["cve_mun"].map(marg["im"])
    panel["grado_marginacion_2020"] = panel["cve_mun"].map(marg["gm"])
    panel["poblacion_2020"] = panel["pobtot"]
    banca = panel["cve_mun"].map(_banca_multiple_inicio(estable=True)).fillna(0).astype(int)
    panel["banca_mun_2019"] = banca
    panel["desierto_bancario"] = 1 - banca
    panel = _covariables_en_logaritmos(panel, "poblacion_2020", None)
    panel = _agregar_tamano_cohorte(panel, "cve_mun")
    panel = panel.sort_values(["cve_mun", "t"]).reset_index(drop=True)
    panel.to_parquet(SALIDAS["municipio_ce"], index=False, compression="zstd")
    log.info(
        "panel CE: %d municipios × %d censos; tratadas %d, controles %d, aperturas posteriores %d",
        panel["cve_mun"].nunique(),
        len(anios),
        int(panel.drop_duplicates("cve_mun")["G"].gt(0).sum()),
        int(panel.drop_duplicates("cve_mun").eval("G == 0 and not apertura_posterior_ce").sum()),
        int(panel.drop_duplicates("cve_mun")["apertura_posterior_ce"].sum()),
    )
    return SALIDAS["municipio_ce"]


def _agregar_tamano_cohorte(panel: pd.DataFrame, id_col: str) -> pd.DataFrame:
    """`n_cohorte`: unidades que comparten el mismo G. Las cohortes de una o dos unidades
    producen ATT(g,t) sin varianza utilizable y dominan los rezagos largos del event study."""
    tamanos = panel.drop_duplicates(id_col).groupby("G")[id_col].size()
    panel["n_cohorte"] = panel["G"].map(tamanos).fillna(0).astype(int)
    return panel


def _log_panel(nombre: str, panel: pd.DataFrame, id_col: str, periodo: str = "semestre") -> None:
    base = panel[panel[periodo] == panel[periodo].min()]
    log.info(
        "panel %s: %d filas, %d unidades × %d periodos; tratadas %d, nunca tratadas %d, "
        "ya tratadas al inicio %d",
        nombre,
        len(panel),
        panel[id_col].nunique(),
        panel[periodo].nunique(),
        int((base["G"] > 0).sum()),
        int((base["G"] == 0).sum()),
        int(base.get("ya_tratado_inicio", pd.Series(dtype=bool)).sum()),
    )


def construir_todos() -> dict[str, Path]:
    salidas = {
        "localidad": panel_localidad(),
        "municipio": panel_municipio(),
        "municipio_trim": panel_municipio_trim(),
        "municipio_trim_largo": panel_municipio_trim(largo=True),
    }
    if (INTERIM / "inegi_ce_municipio.parquet").exists():
        salidas["municipio_ce"] = panel_municipio_ce()
    if (INTERIM / "anillos.parquet").exists():
        salidas["anillo"] = panel_anillo()
    else:
        log.warning("sin anillos.parquet: corre `python -m proyecto.variables.anillos`")
    return salidas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    construir_todos()

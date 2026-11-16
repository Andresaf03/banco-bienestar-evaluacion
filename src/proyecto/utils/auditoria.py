"""Auditoría de datos: responde las 12 preguntas de `docs/data_audit.md` con evidencia.

Se ejecuta con `make auditar` (`python -m proyecto.utils.auditoria`). Lee `data/interim/*` y escribe:
- `docs/data_audit.md` (reporte),
- `outputs/figuras/cohortes.png`,
- `outputs/tablas/auditoria_*.csv` (tablas de apoyo).

No estima efectos: solo conteos, cruces y descriptivos.
"""

from __future__ import annotations

import logging
import re
from datetime import date

import matplotlib
import numpy as np
import openpyxl
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from proyecto.utils.io import DOCS, FIGURAS, INTERIM, RAW, TABLAS, parametros  # noqa: E402
from proyecto.utils.periodos import periodo_a_t, rango  # noqa: E402

log = logging.getLogger(__name__)

P = parametros()
INICIO, FIN = P["periodo"]["inicio"], P["periodo"]["fin"]
PERIODOS_PANEL = rango(INICIO, FIN)
ROJO = "🔴"
AMARILLO = "🟡"
VERDE = "🟢"


# ----------------------------------------------------------------------------- carga
def cargar() -> dict[str, pd.DataFrame]:
    b = pd.read_parquet(INTERIM / "cnbv_bdif.parquet")
    pob = pd.read_parquet(INTERIM / "cnbv_bdif_poblacion.parquet")
    suc = (
        b[b["variable"] == "sucursales"]
        .pivot_table(
            index=["cve_mun", "periodo", "t"], columns="sector", values="valor", aggfunc="first"
        )
        .reset_index()
    )
    return {
        "bdif": b,
        "pob": pob,
        "suc": suc,
        "bd": suc.pivot(index="cve_mun", columns="periodo", values="banca_desarrollo"),
        "bm": suc.pivot(index="cve_mun", columns="periodo", values="banca_multiple"),
        "mun": pd.read_parquet(INTERIM / "municipios.parquet"),
        "cw": pd.read_parquet(INTERIM / "crosswalk_municipios.parquet"),
        "babien": pd.read_parquet(INTERIM / "babien.parquet"),
        "marg": pd.read_parquet(INTERIM / "conapo_marginacion.parquet"),
        "censo": pd.read_parquet(
            INTERIM / "inegi_censo_2020.parquet",
            columns=["cve_mun", "pobtot", "p_15ymas", "p_18ymas"],
        ),
        "proy": pd.read_parquet(
            INTERIM / "conapo_proyecciones_quinq.parquet",
            columns=["cve_mun", "sexo", "anio", "pob_total", "pob_15_mas", "pob_18_mas_aprox"],
        ),
    }


def _md(df: pd.DataFrame, index: bool = False, floatfmt: str = ".1f") -> str:
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else format(v, floatfmt))
    if index:
        d = d.reset_index()
    cols = [str(c) for c in d.columns]
    filas = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in d.itertuples(index=False):
        filas.append(
            "| "
            + " | ".join(
                "" if (isinstance(v, float) and np.isnan(v)) or v is None else str(v) for v in r
            )
            + " |"
        )
    return "\n".join(filas)


def _guardar(df: pd.DataFrame, nombre: str) -> str:
    TABLAS.mkdir(parents=True, exist_ok=True)
    ruta = TABLAS / f"auditoria_{nombre}.csv"
    df.to_csv(ruta, index=False)
    return f"`outputs/tablas/{ruta.name}`"


# ----------------------------------------------------------------------------- P1
def p1_separacion(d: dict) -> str:
    b = d["bdif"]
    cob = (
        b[["periodo", "sector", "variable"]]
        .drop_duplicates()
        .groupby(["variable", "sector"])["periodo"]
        .agg(["min", "max", "nunique"])
        .reset_index()
    )
    resultados = {
        "sucursales": "sucursales",
        "cajeros": "cajeros",
        "tpv": "TPV",
        "establecimientos_tpv": "establecimientos con TPV",
        "corresponsales": "corresponsales",
        "cuentas_celular": "cuentas/contratos banca móvil",
        "transacciones_cajeros": "transacciones en cajeros",
        "transacciones_tpv": "transacciones en TPV",
        "capt_ahorro": "contratos de captación (ahorro)",
        "capt_n1": "contratos de captación (transaccionales N1)",
        "capt_total": "contratos de captación (total)",
        "tarjetas_debito": "tarjetas de débito",
        "cred_personal": "contratos de crédito (personal)",
        "cred_hipotecario": "contratos de crédito (hipotecario)",
        "tarjetas_credito": "tarjetas de crédito",
        "cred_total": "contratos de crédito (total)",
    }
    filas = []
    for var, etiqueta in resultados.items():
        c = cob[cob["variable"] == var].set_index("sector")

        def rango_de(s, c=c):
            return (
                f"{c.loc[s, 'min']}–{c.loc[s, 'max']} ({c.loc[s, 'nunique']})"
                if s in c.index
                else "—"
            )

        bd, bm, banca = rango_de("banca_desarrollo"), rango_de("banca_multiple"), rango_de("banca")
        if "banca_desarrollo" in c.index and c.loc["banca_desarrollo", "min"] <= INICIO:
            estado = f"{VERDE} separable todo el panel"
        elif "banca_desarrollo" in c.index:
            estado = f"{ROJO} separable solo desde {c.loc['banca_desarrollo', 'min']}; antes solo 'banca' = múltiple + desarrollo"
        else:
            estado = f"{ROJO} nunca separable por sector (solo total)"
        filas.append(
            {
                "variable de resultado": etiqueta,
                "canónica": f"`{var}`",
                "banca_desarrollo": bd,
                "banca_multiple": bm,
                "banca (combinada)": banca,
                "veredicto": estado,
            }
        )
    tabla = pd.DataFrame(filas)
    ref = _guardar(cob, "p1_cobertura_sector_variable")
    return f"""**Respuesta corta.** Sí para **sucursales** en los 40 trimestres (2016T1–2025T4): la BDIF trae `Sucursales banca de desarrollo` y `Sucursales banca comercial` (múltiple) como columnas separadas en todas las eras de layout. {ROJO} **No** para el resto de las variables de resultado antes de 2022T4: cajeros, TPV, transacciones, cuentas de banca móvil y **todos los contratos de captación y de crédito** vienen para "Banca (comercial y de desarrollo)" combinada en 2016T1–2022T3 y solo se separan por sector (banca múltiple / banca de desarrollo / SOCAP / SOFIPO) a partir de **2022T4** (13 trimestres, 2022T4–2025T4). Los **corresponsales** nunca se separan (solo total de todos los sectores).

Implicación: el **tratamiento** (primera sucursal de banca de desarrollo) se puede fechar en todo el panel; los **resultados "solo banca múltiple y EACP"** solo se observan directamente en 2022T4–2024T4 (9 trimestres del panel propuesto). Para 2019T1–2022T3 el dato disponible es banca total (múltiple + desarrollo), que incluye al Banco del Bienestar (efecto mecánico). Ver alternativas en la sección final.

Cobertura por variable y sector (primer–último trimestre y número de trimestres con dato):

{_md(tabla)}

Tabla completa (todas las variables × sectores): {ref}. Evidencia de nombres de columna por era: `docs/diccionarios/cnbv_bdif.md`, sección "Encabezados originales por variable canónica"."""


# ----------------------------------------------------------------------------- P2
def _banca_por_institucion() -> pd.DataFrame:
    """Sucursales por institución (nivel nacional) de la hoja `BD Banca`, disponible desde 2023T3."""
    filas = []
    for ruta in sorted((RAW / "cnbv_bdif").glob("Base_de_Datos_de_Inclusion_Financiera_*.xlsx")):
        yyyymm = re.search(r"_(\d{6})\.", ruta.name).group(1)
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        if "BD Banca" not in wb.sheetnames:
            continue
        ws = wb["BD Banca"]
        for row in ws.iter_rows(min_row=13, values_only=True):
            vals = list(row)
            if len(vals) > 5 and vals[1] == "Banca de desarrollo":
                filas.append(
                    {
                        "yyyymm": yyyymm,
                        "institucion": vals[3],
                        "clave": vals[2],
                        "sucursales": vals[5],
                        "cajeros": vals[6],
                        "capt_total": vals[19] if len(vals) > 19 else None,
                    }
                )
        wb.close()
    return pd.DataFrame(filas)


def _grupos(piv: pd.DataFrame) -> tuple[int, int, int, pd.Series]:
    """(ya tratados en INICIO, cohortes, nunca, cohortes por periodo) a partir de una matriz cve×periodo."""
    obs = piv[PERIODOS_PANEL].dropna(how="all")
    tr = obs.fillna(0) >= 1
    ya = tr[INICIO]
    primera = tr.idxmax(axis=1).where(tr.any(axis=1))
    coh = primera[~ya & tr.any(axis=1)]
    return int(ya.sum()), int(len(coh)), int((~tr.any(axis=1)).sum()), coh


def p2_banjercito(d: dict) -> str:
    inst = _banca_por_institucion()
    ref = _guardar(inst, "p2_banca_desarrollo_por_institucion_nacional")
    piv_nac = inst.pivot(index="yyyymm", columns="institucion", values="sucursales")
    sb = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    op = pd.read_parquet(INTERIM / "cnbv_portafolio_operativa.parquet")
    banj = pd.read_parquet(INTERIM / "banjercito_municipios.parquet")
    mun = d["mun"].set_index("cve_mun")[["nom_mun", "nom_ent"]]
    suc = op[(op["producto"] == "Número de Sucursales") & op["en_bdif"]]
    por_mes = (
        suc.pivot_table(index="yyyymm", columns="institucion", values="valor", aggfunc="sum")
        .fillna(0)
        .astype(int)
    )
    por_mes["municipios_banjercito"] = (
        suc[suc["institucion"] == "Banjército"].groupby("yyyymm")["cve_mun"].nunique()
    )
    # cuadre con BDIF por trimestre
    pf_trim = suc[suc["periodo"].notna()].groupby("periodo")["valor"].sum()
    cuadre = (
        pd.DataFrame(
            {"bdif_banca_desarrollo": d["bd"].sum(), "portafolio_bienestar+banjercito": pf_trim}
        )
        .dropna()
        .astype(int)
    )
    # grupos con y sin Banjército
    piv_bd = sb.pivot(index="cve_mun", columns="periodo", values="suc_bd_bdif")
    piv_bien = sb.pivot(index="cve_mun", columns="periodo", values="suc_bienestar")
    ya_bd, coh_bd, nunca_bd, cbd = _grupos(piv_bd)
    ya_b, coh_b, nunca_b, cb = _grupos(piv_bien)
    comp = pd.DataFrame(
        {
            "serie": [
                "BDIF banca de desarrollo (Bienestar + Banjército)",
                "Bienestar sin Banjército (corregida)",
            ],
            f"ya tratados {INICIO}": [ya_bd, ya_b],
            "cohortes": [coh_bd, coh_b],
            "nunca tratados": [nunca_bd, nunca_b],
        }
    )
    # casos concretos
    solo = banj[banj["solo_banjercito_202112"]].set_index("cve_mun").join(mun)
    cambian_g = pd.DataFrame({"G_bdif": cbd, "G_bienestar": cb.reindex(cbd.index)})
    cambian_g = cambian_g[cambian_g["G_bdif"] != cambian_g["G_bienestar"]].join(mun)
    cambian_g["G_bienestar"] = cambian_g["G_bienestar"].fillna(f"nunca (hasta {FIN})")
    sosp = (
        sb[sb["sospechoso_banjercito_nuevo"]]
        .groupby("cve_mun")
        .agg(bd_ult=("suc_bd_bdif", "last"), bienestar_ult=("suc_bienestar", "last"))
        .join(mun)
    )
    ref_sosp = _guardar(sosp.reset_index(), "p2_sospechosos_banjercito_nuevo")
    ref_solo = _guardar(solo.reset_index(), "p2_solo_banjercito_202112")
    return f"""**Respuesta corta.** En la BDIF municipal **no**: el sector "Banca de desarrollo" suma Banco del Bienestar y Banjército sin columna de institución (nota 1 de los reportes CNBV). **Pero sí se puede separar con otra fuente de la propia CNBV**: el Portafolio de Información publica `BD_Operativa_YYYYMM.xlsx` con sucursales **por institución y localidad INEGI** para 2016-01 a 2021-12 (`data/raw/cnbv_portafolio/`, 72 meses; la CNBV etiqueta al banco como "Bansefi" hasta 2021-07). El total Bienestar + Banjército del Portafolio **cuadra exactamente** con la banca de desarrollo de la BDIF en cada trimestre (2020T2 difiere por una revisión posterior de la CNBV) y municipio por municipio (0 diferencias en 2016T1–2020T1; 2 municipios en 2020T3–2021T4 por cambios de clave, p. ej. Villa Corzo/El Parral):

{_md(cuadre.reset_index())}

Banjército por trimestre (sucursales y municipios, Portafolio; meses de cierre):

{_md(por_mes.reset_index()[["yyyymm", "Banco del Bienestar", "Banjército", "municipios_banjercito"]][por_mes.reset_index()["yyyymm"].str[4:].isin(["03", "06", "09", "12"]).values])}

Nacional desde 2023T3 (hoja `BD Banca` de la BDIF):

{_md(piv_nac.reset_index())}

**Corrección aplicada** (`data/interim/sucursales_bienestar.parquet`, módulo `limpieza/banjercito.py`): `suc_bienestar = suc_bd_bdif − suc_banjercito`, con Banjército **observado** en 2016T1–2021T4 (meses de cierre del Portafolio) y **extrapolado** solo hacia 2022T1+ con la red de 2021-12, acotado por la BDIF. Supuesto: la red de Banjército es estable después de 2021 (59 municipios en 2016, 61 en 2019T1, 69 en 2019T2, 75 en 2021T4; 83 → 95 sucursales nacionales 2021–2025). Efecto sobre los grupos del panel:

{_md(comp)}

- **{len(solo)} municipios "solo Banjército"** en 2021-12 (sucursal de banca de desarrollo sin Bienestar): {", ".join(f"{r.Index} {r.nom_mun}" for r in solo.itertuples())}. {ya_bd - ya_b} municipios dejan de contar como "ya tratados en {INICIO}" (su única sucursal de banca de desarrollo era de Banjército) y pasan a cohortes o a nunca tratados según cuándo llega el Bienestar. Lista: {ref_solo}.
- **{len(cambian_g)} cohortes cambian de G** al quitar Banjército (su primera sucursal de banca de desarrollo era de Banjército):

{_md(cambian_g.reset_index())}

- {AMARILLO} **Residual no observable**: Banjército abrió ~12 sucursales entre 2022 y 2025 (83 → 95) que la extrapolación no ve. Cruce contra el directorio del Banco del Bienestar (2026): **{len(sosp)} municipios sospechosos** (entran después de 2021T4 y el directorio no respalda la sucursal): {ref_sosp}. Se marcan con `sospechoso_banjercito_nuevo` para excluirlos en robustez.
- El archivo `BD_Operativa_202606.xlsx` (más reciente) es un modelo Power Pivot sin hoja plana; no se puede leer con herramientas abiertas. Si la CNBV publica de nuevo hojas planas mensuales 2022+, el residual desaparece.
- **Actualización del 2026-10-07 (fase 2):** sí se puede leer. `xl/model/item.data` es un respaldo de Analysis Services sin la compresión de los .pbix y `pbixray` lo decodifica (`limpieza/cnbv_portafolio_modelo.py`). Con Banjército observado 2022+ cambian 9 municipios y los resultados no se mueven: P-8 cerrada (`docs/decisiones.md`).

Tabla nacional: {ref}."""


# ----------------------------------------------------------------------------- P3
def p3_eacp(d: dict) -> str:
    b = d["bdif"]
    cob = b[["periodo", "sector", "variable"]].drop_duplicates()

    def vars_de(s, desde=None):
        x = cob[cob["sector"] == s]
        if desde:
            x = x[x["periodo"] >= desde]
        return sorted(x["variable"].unique())

    filas = []
    for s in ["banca_multiple", "banca", "socap", "sofipo", "eacp"]:
        filas.append(
            {
                "sector": s,
                "variables (todo el periodo)": ", ".join(vars_de(s)),
                "n_variables": len(vars_de(s)),
            }
        )
    tabla = pd.DataFrame(filas)

    # cobertura municipal: municipios con sucursales >0 y con contratos >0 por sector en 2024Q4 y 2019Q1
    def mun_con(s, var, per):
        x = b[(b["sector"] == s) & (b["variable"] == var) & (b["periodo"] == per)]
        return int((x["valor"] > 0).sum()), int(x["valor"].notna().sum())

    cobm = []
    for per in ["2019Q1", "2024Q4"]:
        for s in ["banca_multiple", "banca_desarrollo", "socap", "sofipo"]:
            n, obs = mun_con(s, "sucursales", per)
            cobm.append(
                {
                    "periodo": per,
                    "sector": s,
                    "variable": "sucursales",
                    "municipios con >0": n,
                    "municipios con dato": obs,
                }
            )
        for s, var in [
            ("banca", "capt_ahorro"),
            ("eacp", "capt_ahorro"),
            ("banca_multiple", "capt_total"),
            ("socap", "capt_total"),
            ("sofipo", "capt_total"),
        ]:
            n, obs = mun_con(s, var, per)
            if obs:
                cobm.append(
                    {
                        "periodo": per,
                        "sector": s,
                        "variable": var,
                        "municipios con >0": n,
                        "municipios con dato": obs,
                    }
                )
    return f"""**Respuesta corta.** Cobertura municipal: sí, las hojas de EACP tienen las mismas filas (todos los municipios) que las de banca en todos los trimestres. Variables: **no son las mismas**. {AMARILLO}
- **Sucursales**: SOCAP y SOFIPO separadas en los 40 trimestres (igual que banca múltiple y desarrollo).
- **Captación**: la banca reporta ahorro, plazo, transaccionales N1–N4 (N4 = "tradicionales" hasta 2022T3) y tarjetas de débito; las EACP reportan ahorro, **a la vista**, plazo y tarjetas de débito. Los productos no son homologables uno a uno; sí lo es el **total de contratos de captación**, pero ese total solo viene desde 2022T4.
- **Crédito**: la banca reporta tarjeta de crédito, personal, nómina, ABCD, grupal, hipotecario, automotriz; las EACP reportan **consumo, vivienda** y (desde 2022T4) comercial y tarjeta de crédito. Comparable solo el total (desde 2022T4).
- **Separación SOCAP vs SOFIPO** en captación/crédito/transacciones: solo desde **2022T4**; antes viene "EACP" combinada. Usuarios (socios/clientes) por sexo sí vienen separados desde 2018T3.
- Cajeros/TPV/transacciones por sector EACP: solo desde 2022T4.

Variables por sector en la tabla larga:

{_md(tabla)}

Municipios con dato y con valor > 0 (2019T1 y 2024T4):

{_md(pd.DataFrame(cobm))}"""


# ----------------------------------------------------------------------------- P4
def p4_denominador(d: dict) -> str:
    pob, censo, proy = d["pob"], d["censo"], d["proy"]
    p = pob[pob["periodo"].isin(["2019Q1", "2022Q3", "2022Q4", "2024Q4", "2025Q1"])]
    resumen = (
        p.groupby("periodo")
        .agg(
            municipios=("cve_mun", "size"),
            pob_adulta_nacional=("poblacion_adulta", "sum"),
            pob_total_nacional=("poblacion", "sum"),
            enteros=("poblacion_adulta", lambda s: float((s.dropna() % 1 == 0).mean())),
        )
        .reset_index()
    )
    # comparación 2022Q4 vs Censo 2020
    c = pob[pob["periodo"] == "2022Q4"].merge(censo, on="cve_mun", how="inner")
    dif15 = (c["poblacion_adulta"] - c["p_15ymas"]).abs()
    dif18 = (c["poblacion_adulta"] - c["p_18ymas"]).abs()
    # comparación 2019Q1 vs CONAPO 2019
    py = (
        proy[proy["anio"] == 2019]
        .groupby("cve_mun")[["pob_total", "pob_15_mas", "pob_18_mas_aprox"]]
        .sum()
    )
    c19 = pob[pob["periodo"] == "2019Q1"].merge(py, on="cve_mun", how="inner")
    r15 = (c19["poblacion_adulta"] / c19["pob_15_mas"]).describe()
    r18 = (c19["poblacion_adulta"] / c19["pob_18_mas_aprox"]).describe()
    rt = (c19["poblacion"] / c19["pob_total"]).describe()
    return f"""**Respuesta corta.** Sí. Todas las bases traen `Población` y `Población adulta` por municipio (y desde 2018T1 población adulta por sexo). **Definición de edad: 15 años o más.** Cita del Reporte Trimestral BDIF (2019T1 y 2024T4, `data/raw/cnbv_bdif/reportes/`): "población adulta incluye a las personas de 15 años o más, debido a recomendaciones internacionales de la OCDE". {AMARILLO} No es 18+.

**Fuente de la población (evidencia empírica, la CNBV no la declara en la hoja):**
- 2016T1–2022T3: valores con decimales (interpolación de proyecciones CONAPO). En 2019T1, población adulta BDIF / CONAPO 15+ (proyección 2019, `pobproy_quinq1`): mediana {r15["50%"]:.3f} (p5 {r15["min"]:.3f}, p95 {r15["max"]:.3f}); contra 18+ aproximado: mediana {r18["50%"]:.3f}. Población total BDIF / CONAPO total: mediana {rt["50%"]:.3f}. → consistente con **CONAPO 15+** (la razón no es exactamente 1 porque la CNBV usa la vintage anterior de proyecciones y/o interpola al trimestre).
- 2022T4–2025T4: enteros iguales al **Censo 2020**: en 2022T4, |pob. adulta BDIF − P_15YMAS Censo| tiene mediana {dif15.median():.0f} y máximo {dif15.max():.0f} (vs. mediana {dif18.median():.0f} contra P_18YMAS). Población total coincide con POBTOT del ITER 2020.

{ROJO} **Salto de denominador en 2022T4**: la serie pasa de proyección CONAPO (vintage vieja) a Censo 2020 fijo, lo que introduce un escalón en cualquier tasa "por 10 mil adultos" justo cuando cambia el layout. El Censo 2020 queda **fijo** de 2022T4 a 2024T4 (no crece con el tiempo) y en **2025T1** la CNBV vuelve a cambiar la fuente (población nacional pasa de 126.0 a 133.4 millones: nueva vintage de proyecciones CONAPO), otro escalón fuera del panel base pero dentro de la extensión a 2025.

{_md(resumen, floatfmt=".2f")}

Alternativa disponible: `data/interim/conapo_proyecciones_quinq.parquet` (población a mitad de año por municipio, sexo y grupo quinquenal 1990–2040): permite construir un denominador **propio y consistente** para todo el panel, con 15+ exacto o 18+ aproximado (el grupo 15–19 no se puede partir en la fuente; `pob_18_mas_aprox` supone 2/5 del grupo). Decisión pendiente."""


# ----------------------------------------------------------------------------- P5-P8
def _matriz_panel(d: dict) -> pd.DataFrame:
    bd = d["bd"][PERIODOS_PANEL]
    return bd


def p5_ya_tratados(d: dict) -> str:
    bd = _matriz_panel(d)
    x = bd[INICIO]
    n = int((x >= 1).sum())
    faltan = int(x.isna().sum())
    dist = (x[x >= 1]).describe()
    mun = d["mun"].set_index("cve_mun")
    top = (
        x[x >= 1]
        .sort_values(ascending=False)
        .head(10)
        .to_frame("sucursales_bd_2019q1")
        .join(mun[["nom_mun", "nom_ent"]])
        .reset_index()
    )
    # 2016Q1 también
    n16 = int((d["bd"]["2016Q1"] >= 1).sum())
    return f"""**Respuesta corta.** **{n} municipios** tienen al menos una sucursal de banca de desarrollo en {INICIO} (de {int(x.notna().sum())} con dato; {faltan} sin dato). Es la herencia Bansefi + Banjercito. En 2016T1 eran {n16}; la serie es casi plana (484–501) hasta 2021T3 y despega en **2022T1** (680) — coincide con la ASF: 14 sucursales operando en 2021 y 908 en 2022.

Sucursales de banca de desarrollo entre los ya tratados en {INICIO}: media {dist["mean"]:.2f}, mediana {dist["50%"]:.0f}, máximo {dist["max"]:.0f}. Los 10 municipios con más sucursales:

{_md(top)}

Bajo Callaway y Sant'Anna estos {n} municipios se **descartan** como tratados (ya tratados en el primer periodo). Decisión pendiente: excluirlos o usarlos como control tipo Fonseca y Matray."""


def p6_nunca_tratados(d: dict) -> str:
    bd = _matriz_panel(d)
    obs = bd.dropna(how="all")
    nunca = obs[(obs.fillna(0) < 1).all(axis=1)].index
    alguna = obs[(obs >= 1).any(axis=1)].index
    ya = obs[obs[INICIO] >= 1].index
    nuevos = alguna.difference(ya)
    incompletos = int(bd.isna().any(axis=1).sum())
    pob = d["pob"][d["pob"]["periodo"] == INICIO].set_index("cve_mun")
    bm = d["bm"][INICIO]
    marg = d["marg"][d["marg"]["anio"] == 2020].set_index("cve_mun")
    grupos = {
        "nunca tratados": nunca,
        "tratados 2019T2–2024T4 (cohortes)": nuevos,
        "ya tratados en 2019T1": ya,
    }
    filas = []
    for nombre, idx in grupos.items():
        idx = idx.intersection(pob.index)
        gm = marg["gm"].reindex(idx)
        filas.append(
            {
                "grupo": nombre,
                "n": len(idx),
                "pob. adulta 2019T1 (mediana)": pob.loc[idx, "poblacion_adulta"].median(),
                "pob. adulta (media)": pob.loc[idx, "poblacion_adulta"].mean(),
                "% con banca múltiple 2019T1": 100 * (bm.reindex(idx) >= 1).mean(),
                "índice marg. 2020 (media)": marg["im"].reindex(idx).mean(),
                "% marg. alta/muy alta": 100 * gm.isin(["Alto", "Muy alto"]).mean(),
                "% rural (tipo CNBV)": 100 * (pob.loc[idx, "tipo_poblacion"] == "Rural").mean(),
            }
        )
    tabla = pd.DataFrame(filas)
    _guardar(pd.DataFrame({"cve_mun": nunca}), "p6_nunca_tratados")
    return f"""**Respuesta corta.** **{len(nunca)} municipios** no tienen sucursal de banca de desarrollo en ningún trimestre de {INICIO}–{FIN} (de {len(obs)} con al menos un dato en el panel; {incompletos} tienen algún trimestre sin dato, casi todos municipios de creación reciente). Son ~{100 * len(nunca) / len(obs):.0f}% del total, así que el grupo de nunca tratados **no es marginal**, pero es sistemáticamente distinto: más pequeños, más rurales y más marginados que los tratados.

{_md(tabla)}

Comparación adicional: los nunca tratados tienen mediana de población adulta de {tabla.loc[0, "pob. adulta 2019T1 (mediana)"]:,.0f} contra {tabla.loc[1, "pob. adulta 2019T1 (mediana)"]:,.0f} en las cohortes tratadas; solo {tabla.loc[0, "% con banca múltiple 2019T1"]:.0f}% tenía banca múltiple en {INICIO}. Esto favorece usar **aún no tratados** como control principal (más comparables) y nunca tratados como robustez, como propone el diseño. Lista en `outputs/tablas/auditoria_p6_nunca_tratados.csv`."""


def cohortes(d: dict) -> pd.DataFrame:
    bd = _matriz_panel(d)
    obs = bd.dropna(how="all")
    tratado = obs >= 1
    ya = tratado[INICIO]
    primera = tratado.idxmax(axis=1).where(tratado.any(axis=1))
    g = primera[~ya & tratado.any(axis=1)]
    tabla = (
        g.value_counts().reindex(PERIODOS_PANEL[1:], fill_value=0).rename("municipios").to_frame()
    )
    tabla["t"] = [periodo_a_t(p) for p in tabla.index]
    tabla["acumulado"] = tabla["municipios"].cumsum()
    return tabla.reset_index().rename(columns={"index": "periodo"})


def p7_cohortes(d: dict) -> str:
    tabla = cohortes(d)
    ref = _guardar(tabla, "p7_cohortes")
    FIGURAS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(tabla["periodo"], tabla["municipios"], color="#2a6f97")
    ax.set_ylabel("Municipios que entran (primera sucursal BD)")
    ax.set_title(
        f"Cohortes de tratamiento: primer trimestre con sucursal de banca de desarrollo ({PERIODOS_PANEL[1]}–{FIN}), sin los ya tratados en {INICIO}"
    )
    ax.tick_params(axis="x", rotation=90)
    ax2 = ax.twinx()
    ax2.plot(tabla["periodo"], tabla["acumulado"], color="#c44536", marker="o", ms=3)
    ax2.set_ylabel("Acumulado")
    fig.tight_layout()
    fig.savefig(FIGURAS / "cohortes.png", dpi=150)
    plt.close(fig)
    total = int(tabla["municipios"].sum())
    grandes = tabla.sort_values("municipios", ascending=False).head(6)
    return f"""**Respuesta corta.** {total} municipios entran por primera vez entre {PERIODOS_PANEL[1]} y {FIN}. Casi nadie entra en 2019–2021 (hay entradas y salidas pequeñas de la red heredada) y la expansión se concentra en **2022T1–2024T1** (9 trimestres), con picos en {", ".join(f"{r.periodo} ({r.municipios})" for r in grandes.itertuples())}. En 2024T2–2024T4 no entra ningún municipio nuevo: las cohortes útiles son 2022T1–2024T1, con 3–11 trimestres post-tratamiento dentro del panel.

{_md(tabla)}

Figura: `outputs/figuras/cohortes.png`. Tabla: {ref}.

![cohortes](../outputs/figuras/cohortes.png)"""


def p8_cierres(d: dict) -> str:
    bd = d["bd"]  # todos los trimestres 2016–2025
    obs = bd.dropna(how="all").fillna(0)
    tr = obs >= 1
    cambios = tr.astype(int).diff(axis=1)
    cierres = cambios == -1
    n_mun_cierre = int(cierres.any(axis=1).sum())
    por_periodo = cierres.sum().rename("municipios_que_pasan_a_0").to_frame()
    # Reapertura = entrada (0 -> >=1) en un municipio que ya había tenido sucursal antes y la perdió.
    tuvo_antes = tr.cumsum(axis=1).shift(axis=1, fill_value=0) > 0
    por_periodo["reaperturas"] = ((cambios == 1) & tuvo_antes).sum()
    por_periodo["primeras_entradas"] = ((cambios == 1) & ~tuvo_antes).sum()
    # dentro del panel
    panel = tr[PERIODOS_PANEL]
    cambios_p = panel.astype(int).diff(axis=1)
    cierres_p = cambios_p == -1
    mun_cierre_p = cierres_p.any(axis=1)
    # ¿vuelven a abrir? después del primer cierre dentro del panel
    reabren = []
    for cve in panel.index[mun_cierre_p]:
        fila = panel.loc[cve]
        primer_cierre = cierres_p.loc[cve].idxmax()
        despues = fila.loc[primer_cierre:]
        reabren.append(
            {
                "cve_mun": cve,
                "primer_cierre": primer_cierre,
                "reabre": bool(despues.any()),
                "tratado_en_fin": bool(fila[FIN]),
                "n_cambios": int((cambios_p.loc[cve] != 0).sum()),
            }
        )
    rea = pd.DataFrame(reabren)
    ref = _guardar(rea, "p8_cierres_panel")
    resumen_rea = rea["reabre"].value_counts().to_dict() if not rea.empty else {}
    # cierres de municipios que ya tenían >1 sucursal (no pierden el tratamiento) no cuentan; reportar caídas en conteo
    caidas = (
        ((obs[PERIODOS_PANEL].diff(axis=1) < 0) & (obs[PERIODOS_PANEL].shift(axis=1) >= 1))
        .sum()
        .sum()
    )
    return f"""**Respuesta corta.** Sí, pero pocos. Dentro del panel {INICIO}–{FIN}, **{int(mun_cierre_p.sum())} municipios** pasan de tener ≥1 sucursal de banca de desarrollo a 0 en algún trimestre; de ellos **{resumen_rea.get(True, 0)} vuelven a abrir** después y **{resumen_rea.get(False, 0)} no** (quedan en 0 hasta {FIN}). {AMARILLO} Además hay {int(caidas)} caídas trimestrales en el número de sucursales sin perder el tratamiento (municipios con ≥2 sucursales). En toda la serie 2016T1–2025T4 hay {n_mun_cierre} municipios con al menos un cierre total.

Fechas con más cierres (municipios que pasan a 0) y reaperturas, toda la serie:

{_md(por_periodo.reset_index()[(por_periodo["municipios_que_pasan_a_0"] > 0).values].rename(columns={"index": "periodo"}))}

Nota CNBV (reporte 2024T4, nota 5): "las sucursales cerradas temporales por Covid-19 dejaron de reportarse en 2022", lo que explica parte de las salidas de 2021T4–2022T1. Para el supuesto de irreversibilidad de Callaway y Sant'Anna el número es manejable: se propone definir G como la primera entrada y tratar las reaperturas como continuidad (absorbing), o excluir los {int(mun_cierre_p.sum())} municipios en robustez. Detalle: {ref}."""


# ----------------------------------------------------------------------------- P9-P11
def p9_validacion(d: dict) -> str:
    bd, babien = d["bd"], d["babien"]
    n_bab = babien.groupby("cve_mun_espacial").size()
    filas = []
    for per in ["2024Q4", "2025Q4"]:
        bdif_mun = set(bd.index[bd[per] >= 1])
        bab_mun = set(n_bab.index)
        filas.append(
            {
                "BDIF": per,
                "municipios BDIF con BD>=1": len(bdif_mun),
                "municipios con BABIEN (foto 2026T1)": len(bab_mun),
                "en ambos": len(bdif_mun & bab_mun),
                "solo BDIF": len(bdif_mun - bab_mun),
                "solo BABIEN": len(bab_mun - bdif_mun),
                "% BABIEN en BDIF": 100 * len(bdif_mun & bab_mun) / len(bab_mun),
                "% BDIF en BABIEN": 100 * len(bdif_mun & bab_mun) / len(bdif_mun),
            }
        )
    tabla = pd.DataFrame(filas)
    comp = (
        pd.DataFrame({"bdif_2025q4": bd["2025Q4"]})
        .join(n_bab.rename("babien"), how="outer")
        .fillna(0)
    )
    comp = comp[(comp["bdif_2025q4"] > 0) | (comp["babien"] > 0)]
    iguales = int((comp["bdif_2025q4"] == comp["babien"]).sum())
    corr = comp["bdif_2025q4"].corr(comp["babien"])
    coinc = babien["coincide"].sum()
    sin_nombre = babien["cve_mun_declarado"].isna().sum()
    return f"""**Respuesta corta.** Alta coincidencia. El directorio del Banco del Bienestar (foto 1T 2026, {len(babien):,} sucursales, {len(n_bab)} municipios por cruce espacial) contra la BDIF:

{_md(tabla)}

En el cruce a nivel municipio con 2025T4, el número de sucursales coincide exactamente en {iguales} de {len(comp)} municipios (correlación {corr:.3f}). Los "solo BDIF" son candidatos a Banjercito o a cierres entre 2025T4 y 2026T1 (ver P2); los "solo BABIEN" son aperturas de 2025T4–2026T1 o diferencias de georreferencia en municipios fronterizos.

Calidad del directorio: {int(babien["sin_coordenadas"].sum())} sucursales sin coordenadas válidas; **todas** caen dentro de un polígono municipal del MG 2024. El municipio declarado en texto (`municipio_alcaldia` + `entidad`) coincide con el espacial en {int(coinc)} casos; {int(sin_nombre)} no se pudieron emparejar por nombre (variantes ortográficas) y {int((~babien["coincide"] & babien["cve_mun_declarado"].notna()).sum())} discrepan con nombre emparejado. Se usa **siempre** la clave espacial."""


def p10_desiertos(d: dict) -> str:
    bm = d["bm"][INICIO]
    bd = d["bd"][INICIO]
    n0 = int((bm == 0).sum())
    obs = int(bm.notna().sum())
    ambos = int(((bm == 0) & (bd == 0)).sum())
    socap = d["suc"][d["suc"]["periodo"] == INICIO].set_index("cve_mun")
    sin_nada = int((socap["todos"] == 0).sum())
    return f"""**Respuesta corta.** **{n0} municipios** ({100 * n0 / obs:.0f}% de {obs} con dato) no tenían ninguna sucursal de banca múltiple en {INICIO}: son los "desiertos bancarios" para la heterogeneidad. De ellos, {ambos} tampoco tenían banca de desarrollo, y {sin_nada} municipios no tenían **ninguna** sucursal de ningún sector (ni SOCAP ni SOFIPO). Coincide con la cifra CNBV de ~912 municipios con banca múltiple en 2024 ({int((d["bm"]["2024Q4"] >= 1).sum())} en la BDIF 2024T4)."""


def p11_corresponsales(d: dict) -> str:
    b = d["bdif"]
    c = b[(b["variable"] == "corresponsales")].pivot(
        index="cve_mun", columns="periodo", values="valor"
    )
    nac = c.sum().rename("total_nacional").to_frame()
    nac["cambio_%"] = nac["total_nacional"].pct_change() * 100
    nac["municipios_con_>0"] = (c > 0).sum()
    nac["municipios_con_dato"] = c.notna().sum()
    # cambio 2018Q4 -> 2019Q1 por municipio
    cambio = c["2019Q1"] - c["2018Q4"]
    rel = cambio / c["2018Q4"].replace(0, np.nan)
    ventana = nac.loc["2018Q1":"2020Q2"].reset_index()
    ventana2 = nac.loc["2023Q4":"2025Q4"].reset_index()
    ref = _guardar(nac.reset_index(), "p11_corresponsales_nacional")
    return f"""**Respuesta corta.** Sí. {ROJO} El total nacional de módulos de corresponsales cambia {nac.loc["2019Q1", "cambio_%"]:+.1f}% entre 2018T4 y 2019T1 (contra cambios trimestrales de un dígito antes y después). La CNBV lo documenta: "se actualizó la serie de corresponsales a partir del primer trimestre de 2019, ya que se ajustó la metodología para su contabilización" (reporte 2019T1, nota 5). A nivel municipal, la mediana del cambio relativo 2018T4→2019T1 es {rel.median() * 100:+.0f}% y {int((rel.abs() > 0.5).sum())} municipios cambian más de ±50%. Además: (i) en 2020T4 la CNBV revisó el histórico de corresponsales; (ii) en **marzo de 2024** ajustó otra vez la metodología de conteo de módulos (reporte 2024T4, nota 6); (iii) en 2025T4 la columna pasa a "Corresponsales únicos". Los corresponsales **no vienen por sector** en ningún trimestre.

Serie nacional alrededor del corte de 2019T1:

{_md(ventana, floatfmt=".1f")}

Alrededor del ajuste de 2024:

{_md(ventana2, floatfmt=".1f")}

Implicación: como el panel empieza en {INICIO}, el corte de 2019T1 queda en el borde (útil: no hay pre-2019 en el panel base, pero sí afecta la robustez con 2016–2018). El ajuste de 2024T1 sí cae dentro del panel: usar corresponsales como resultado requiere controlar por ese salto (efectos fijos de tiempo lo absorben si es homogéneo entre municipios, no si es heterogéneo). Serie completa: {ref}."""


# ----------------------------------------------------------------------------- P12
def p12_calidad(d: dict) -> str:
    b, pob, mun = d["bdif"], d["pob"], d["mun"]
    periodos = sorted(b["periodo"].unique())
    esperados = rango(periodos[0], periodos[-1])
    faltan_trim = sorted(set(esperados) - set(periodos))
    dup = int(b.duplicated(["cve_mun", "periodo", "sector", "variable"]).sum())
    dup_pob = int(pob.duplicated(["cve_mun", "periodo"]).sum())
    neg = b[b["valor"] < 0]
    neg_tab = neg.groupby(["periodo", "sector", "variable"]).size().rename("n").reset_index()
    na = (
        b["valor"]
        .isna()
        .groupby([b["periodo"]])
        .mean()
        .mul(100)
        .rename("% valores faltantes")
        .to_frame()
    )
    na_var = (
        b[b["valor"].isna()]
        .groupby(["variable", "sector"])
        .size()
        .rename("n_faltantes")
        .reset_index()
        .sort_values("n_faltantes", ascending=False)
        .head(15)
    )
    n_mun = pob.groupby("periodo")["cve_mun"].nunique().rename("municipios").to_frame()
    n_mun["cambio"] = n_mun["municipios"].diff()
    aparecen = mun[mun["en_bdif"] & (mun["bdif_desde"] != periodos[0])][
        ["cve_mun", "nom_mun", "nom_ent", "bdif_desde"]
    ]
    desaparecen = mun[mun["en_bdif"] & (mun["bdif_hasta"] != periodos[-1])][
        ["cve_mun", "nom_mun", "nom_ent", "bdif_hasta"]
    ]
    # unidades: población float->int; capt_tradicionales -> n4; corresponsales únicos; sucursales Compartamos
    frac = (
        pob.groupby("periodo")["poblacion_adulta"]
        .apply(lambda s: float((s.dropna() % 1 != 0).mean() * 100))
        .rename("% pob. adulta con decimales")
        .to_frame()
    )
    # saltos en totales nacionales por variable/sector (cambio trimestral > 30%)
    tot = b.groupby(["variable", "sector", "periodo"])["valor"].sum().unstack("periodo")
    saltos = []
    for (var, sec), fila in tot.iterrows():
        f = fila.dropna()
        pc = f.pct_change()
        for per, v in pc.items():
            if abs(v) > 0.3 and f.loc[per] > 1000:
                saltos.append(
                    {
                        "variable": var,
                        "sector": sec,
                        "periodo": per,
                        "cambio_%": 100 * v,
                        "total": f.loc[per],
                    }
                )
    saltos = (
        pd.DataFrame(saltos).sort_values(["variable", "sector", "periodo"])
        if saltos
        else pd.DataFrame()
    )
    ref_saltos = _guardar(saltos, "p12_saltos_nacionales")
    ref_na = _guardar(na.reset_index(), "p12_faltantes_por_periodo")
    return f"""**Trimestres.** Descargados {len(periodos)} trimestres consecutivos {periodos[0]}–{periodos[-1]}; trimestres ausentes: **{faltan_trim or "ninguno"}**.

**Duplicados.** Llaves `(cve_mun, periodo, sector, variable)` duplicadas: **{dup}**; `(cve_mun, periodo)` en población: **{dup_pob}**.

**Valores negativos.** {len(neg)} celdas negativas{":" if len(neg) else "."}
{_md(neg_tab) if len(neg) else ""}

**Faltantes.** {b["valor"].isna().mean() * 100:.2f}% de las celdas de la tabla larga son NaN ({int(b["valor"].isna().sum())} celdas vacías en el Excel).{(" Concentradas en:" + chr(10) + _md(na_var)) if len(na_var) else " Ninguna."} Por periodo: {ref_na}.

**Municipios que aparecen o desaparecen.** Número de municipios por trimestre: mínimo {n_mun["municipios"].min()}, máximo {n_mun["municipios"].max()}. Aparecen después de {periodos[0]} ({len(aparecen)}, municipios de nueva creación; ver `docs/diccionarios/crosswalk_municipios.md`):
{_md(aparecen)}
Desaparecen antes de {periodos[-1]}: {len(desaparecen)}{"." if len(desaparecen) == 0 else ":"}
{_md(desaparecen) if len(desaparecen) else ""}
Tres municipios del MG 2024 (24059 Villa de Pozos, 25019 Eldorado, 25020 Juan José Ríos) aún no aparecen en la BDIF.

**Cambios de unidad o definición detectados.**
- Población: proyección CONAPO con decimales hasta 2022T3 → Censo 2020 (enteros, fijo) desde 2022T4 (% con decimales por trimestre: {frac.iloc[0, 0]:.0f}% en {frac.index[0]}, {frac.loc["2022Q3"].iloc[0]:.0f}% en 2022Q3, {frac.loc["2022Q4"].iloc[0]:.0f}% en 2022Q4).
- Captación banca: "Cuentas transaccionales tradicionales" (hasta 2022T3) → "Transaccionales Nivel 4" (desde 2022T4); no se fuerza la equivalencia en la tabla larga (`capt_tradicionales` vs `capt_n4`).
- Totales de captación y crédito (`capt_total`, `cred_total`) solo existen desde 2022T4; antes hay que sumarlos con productos no idénticos entre sectores.
- Sucursales de banca múltiple: hasta 2018T4 la CNBV contaba aparte "Módulos de atención Compartamos" (2017T2–2018T4) y desde 2019T1 dejó de contarlos (reporte 2019T1, nota 4) → la serie de banca múltiple tiene un escalón en 2019T1 en municipios con Compartamos.
- Corresponsales: cambios metodológicos 2019T1, 2020T4 (revisión histórica) y 2024T1; "Corresponsales únicos" en 2025T4.
- Crédito no revolvente municipal: la CNBV advierte inconsistencias entre mayo 2017 y junio 2019 (reporte 2024T4, nota 2).
- Todas las variables son **conteos** (contratos, número); no hay columnas de montos en las hojas municipales usadas (los saldos de la hoja de género se descartaron). No hay mezcla de montos con contratos.

**Saltos > 30% en totales nacionales por variable × sector** (cambio trimestral; detecta cambios de definición o reclasificaciones de las instituciones): {len(saltos)} casos, en {ref_saltos}. Se concentran en productos de bajo volumen (cuentas N1, cuentas de ahorro de banca) y en los cortes 2018T1, 2019T4, 2021T2, 2022T4 y 2023T2–T3; por ejemplo, las cuentas de ahorro de banca saltan de ~10 mil a ~544 mil en 2021T2 (entrada del Banco del Bienestar al reporte de captación) y las de EACP de ~1.1 a ~9.8 millones en 2019T4. {AMARILLO} Cualquier resultado con estas series debe revisarse contra estos cortes. Los primeros 25:
{_md(saltos.head(25), floatfmt=".1f") if len(saltos) else ""}"""


# ----------------------------------------------------------------------------- reporte
def generar() -> None:
    d = cargar()
    secciones = [
        ("1. Separación por sector (banca de desarrollo vs banca múltiple)", p1_separacion),
        ("2. Banjercito", p2_banjercito),
        ("3. EACP: SOCAP y SOFIPO", p3_eacp),
        ("4. Denominador: población adulta", p4_denominador),
        ("5. Municipios ya tratados en 2019T1", p5_ya_tratados),
        ("6. Nunca tratados", p6_nunca_tratados),
        ("7. Cohortes", p7_cohortes),
        ("8. Cierres", p8_cierres),
        ("9. Validación cruzada BDIF vs directorio Banco del Bienestar", p9_validacion),
        ("10. Desiertos bancarios", p10_desiertos),
        ("11. Corresponsales", p11_corresponsales),
        ("12. Calidad", p12_calidad),
    ]
    partes = [
        "# Auditoría de datos\n",
        f"Generado por `python -m proyecto.utils.auditoria` el {date.today().isoformat()}. Panel objetivo: {INICIO}–{FIN} ({len(PERIODOS_PANEL)} trimestres); BDIF descargada 2016T1–2025T4. Leyenda: {VERDE} sin problema, {AMARILLO} atención, {ROJO} bandera roja para el diseño.\n",
        "## Resumen de banderas rojas\n",
        f"- {ROJO} **P1.** Contratos de captación/crédito, cajeros, TPV y transacciones solo se separan por sector desde 2022T4. Antes vienen como 'Banca' (múltiple + desarrollo). Sucursales sí se separan en todo el periodo → el tratamiento se puede fechar, pero los resultados 'sin Banco del Bienestar' solo existen 9 trimestres del panel.",
        f"- {AMARILLO} **P2.** Banjército no es identificable en la BDIF municipal, pero el Portafolio de Información de la CNBV lo separa por municipio (2016-01 – 2021-12). Serie corregida `sucursales_bienestar.parquet`: 12 municipios 'solo Banjército', 5 cohortes con G falso, 8 sospechosos residuales (2022+).",
        f"- {ROJO} **P4.** Población adulta = 15+, no 18+; y el denominador salta de proyección CONAPO a Censo 2020 fijo en 2022T4.",
        f"- {ROJO} **P11.** Corresponsales: cambios de metodología en 2019T1 y 2024T1; sin sector.",
        f"- {AMARILLO} **P3, P8, P12.** EACP con productos distintos a la banca; pocos cierres; escalón de Compartamos en banca múltiple en 2019T1; municipios nuevos.\n",
    ]
    for titulo, fn in secciones:
        log.info(titulo)
        partes.append(f"## {titulo}\n\n{fn(d)}\n")
    partes.append("""## Qué significa para el diseño

Esta auditoría se hizo cuando la unidad prevista era el municipio. **El diseño se rediseñó el
2026-09-26** (ver `docs/decisiones.md`): la unidad principal pasó a ser la **localidad**, con el
DENUE georreferenciado como fuente de resultados. Lo que sigue traduce cada hallazgo al diseño
vigente.

1. **Tratamiento.** La primera sucursal de banca de desarrollo es observable en todo el panel y
   coincide con la cronología de la ASF (cohortes 2022T1–2024T1). A nivel localidad se fecha
   combinando esa fecha municipal con el directorio georreferenciado: 1,270 municipios tratados
   tienen una sola sucursal, así que la fecha identifica la localidad sin ambigüedad.
2. **La limitación de P1 dejó de ser vinculante.** Que la BDIF solo separe contratos por sector
   desde 2022T4 importaba cuando los resultados venían solo de la CNBV. Ahora los resultados
   principales (emprendimiento, consumo, salud y presencia financiera privada) vienen del DENUE,
   que cubre 2016–2025 completo. Los contratos de la CNBV quedan como resultado secundario y el
   pipeline los **salta automáticamente** por falta de periodos previos.
3. **Denominador.** A nivel localidad se usa la población del Censo 2020 (fija), que evita el
   escalón de 2022T4 de la población adulta de la CNBV. A nivel municipal se conserva la población
   adulta de la BDIF con ese escalón documentado.
4. **Banjército.** `suc_bienestar` (BDIF menos Banjército del Portafolio) define G en los tres
   niveles; los municipios `sospechoso_banjercito_nuevo` se excluyen en robustez.
5. **Unidades.** Los 22 municipios creados después de 2010 se colapsan en su municipio de origen
   en los paneles municipales; a nivel localidad no aplica.
6. **Corresponsales** (P11) siguen siendo el resultado más frágil: sin sector y con cambios
   metodológicos en 2019T1 y 2024T1. Solo se usan como resultado secundario.
""")
    (DOCS / "data_audit.md").write_text("\n".join(partes), encoding="utf-8")
    log.info("reporte escrito en docs/data_audit.md")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

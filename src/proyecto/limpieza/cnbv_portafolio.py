"""CNBV Portafolio de Información, operativa de banca de desarrollo por institución (2016-01 – 2021-12).

Salidas:
- `data/interim/cnbv_portafolio_operativa.parquet`: largo mensual
  `yyyymm, periodo (trimestre del mes), cve_mun, institucion, producto, valor`. La clave municipal
  se toma de los dígitos 4–8 de `cve_inegi` (484 + ent 2 + mun 3 + loc 4). Solo se conservan
  Banco del Bienestar y Banjército (los únicos que la BDIF cuenta como banca de desarrollo con
  captación al menudeo); las demás instituciones (Banobras, Nafin, Bancomext, SHF) se guardan
  con `en_bdif = False` para poder cuadrar totales. "Bansefi" (nombre usado por la CNBV hasta
  2021-07) se renombra a "Banco del Bienestar".
- `data/interim/banjercito_municipios.parquet`: una fila por municipio con sucursales de
  Banjército en algún mes: `cve_mun, suc_banjercito_202112, suc_bienestar_202112, meses_con_banjercito,
  primer_mes, ultimo_mes, solo_banjercito_202112` (Banjército presente y Bienestar ausente).

Layouts: 2016-01 a 2016-12 (xls) traen una hoja pivote por producto (filas = localidad, columnas =
institución); 2016-09 en adelante traen `Hoja1` plana. El archivo de 2026 (modelo Power Pivot) se
ignora con aviso.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd

from proyecto.utils.claves import es_valida
from proyecto.utils.io import INTERIM, RAW
from proyecto.utils.periodos import yyyymm_a_periodo

log = logging.getLogger(__name__)

FUENTE = "cnbv_portafolio"
SALIDA = INTERIM / "cnbv_portafolio_operativa.parquet"
SALIDA_BANJ = INTERIM / "banjercito_municipios.parquet"
_RE = re.compile(r"BD_Operativa_(\d{6})\.(xlsx|xlsm|xls)$", re.I)
HOJA = "Hoja1"
INSTITUCIONES_BDIF = {"Banco del Bienestar", "Banjército"}
# La CNBV siguió publicando al banco como "Bansefi" hasta 2021-07 aunque cambió de nombre en 2019.
RENOMBRES = {
    "Bansefi": "Banco del Bienestar",
    "Hipotecaria Federal": "Sociedad Hipotecaria Federal",
}
PRODUCTO_SUCURSALES = "Número de Sucursales"


def _trimestre_de_mes(yyyymm: str) -> str | None:
    """Trimestre BDIF si el mes es de cierre (03/06/09/12); None en meses intermedios."""
    return yyyymm_a_periodo(yyyymm) if yyyymm[4:] in ("03", "06", "09", "12") else None


# Layout 2016 (xls): una hoja por producto, filas = localidad (clave INEGI 12 dígitos), columnas =
# institución. Nombre de hoja -> nombre de producto como aparece en `Hoja1` de 2017+.
HOJAS_2016 = {
    "Num de Sucursales": "Número de Sucursales",
    "Num de Cajeros Automaticos": "Número de Cajeros Automáticos",
    "Num de TPV": "Número de Terminales Punto de Venta (TPV)",
    "Num de Est con TPV": "Número de Establecimientos con TPV",
    "Num de Transac en TPV": "Número de Transacciones en TPV",
    "Num de Transac en Cajeros Aut": "Número de Transacciones en Cajeros Automáticos",
}
COLUMNAS_FIJAS_2016 = {"Estado", "Cve Localidad", "Localidad", "Total general"}


def _leer_pivot_2016(ruta: Path, yyyymm: str) -> pd.DataFrame:
    partes = []
    xl = pd.ExcelFile(ruta)
    for hoja, producto in HOJAS_2016.items():
        if hoja not in xl.sheet_names:
            continue
        d = pd.read_excel(xl, sheet_name=hoja, header=None, dtype=str)
        # fila 1: instituciones (desde la col. 4); fila 2: encabezados Estado/Cve Localidad/Localidad
        instituciones = d.iloc[1, 3:].tolist()
        cuerpo = d.iloc[3:, :].copy()
        cuerpo.columns = ["estado", "cve_inegi", "localidad", *instituciones]
        cuerpo = cuerpo[cuerpo["cve_inegi"].fillna("").str.fullmatch(r"\d{12}")]
        largo = cuerpo.melt(
            id_vars=["cve_inegi"],
            value_vars=[c for c in instituciones if c not in COLUMNAS_FIJAS_2016],
            var_name="institucion",
            value_name="valor",
        )
        largo["valor"] = pd.to_numeric(largo["valor"], errors="coerce")
        largo = largo[largo["valor"].notna() & (largo["valor"] != 0)]
        largo["producto"] = producto
        partes.append(largo)
    if not partes:
        return pd.DataFrame()
    return pd.concat(partes, ignore_index=True)


def leer_archivo(ruta: Path) -> pd.DataFrame | None:
    yyyymm = _RE.search(ruta.name).group(1)
    hojas = pd.ExcelFile(ruta).sheet_names
    if HOJA in hojas:
        d = pd.read_excel(ruta, sheet_name=HOJA, dtype=str).rename(
            columns={
                "nombre_publicacion": "institucion",
                "dl_producto_financiero": "producto",
                "dat_num_total": "valor",
            }
        )
    elif "Num de Sucursales" in hojas:
        d = _leer_pivot_2016(ruta, yyyymm)
    else:
        log.warning("%s: sin hoja %s ni layout 2016 (modelo de datos); se omite", ruta.name, HOJA)
        return None
    d["institucion"] = d["institucion"].replace(RENOMBRES)
    d["cve_mun"] = d["cve_inegi"].str[3:8]
    d = d[d["cve_mun"].map(es_valida)]
    d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
    d["yyyymm"] = yyyymm
    d["periodo"] = _trimestre_de_mes(yyyymm)
    d["en_bdif"] = d["institucion"].isin(INSTITUCIONES_BDIF)
    return d[["yyyymm", "periodo", "cve_mun", "institucion", "producto", "valor", "en_bdif"]]


def limpiar() -> Path:
    partes = []
    for ruta in sorted((RAW / FUENTE).glob("BD_Operativa_*.xls*")):
        d = leer_archivo(ruta)
        if d is not None:
            partes.append(d)
    largo = pd.concat(partes, ignore_index=True)
    largo = (
        largo.groupby(
            ["yyyymm", "periodo", "cve_mun", "institucion", "producto", "en_bdif"], dropna=False
        )["valor"]
        .sum()
        .reset_index()
    )
    largo.to_parquet(SALIDA, index=False)

    suc = largo[(largo["producto"] == PRODUCTO_SUCURSALES) & largo["en_bdif"]]
    piv = suc.pivot_table(
        index=["cve_mun", "yyyymm"], columns="institucion", values="valor", aggfunc="sum"
    ).fillna(0)
    piv.columns = ["suc_" + ("banjercito" if "Banj" in c else "bienestar") for c in piv.columns]
    piv = piv.reset_index()
    ultimo = piv["yyyymm"].max()
    con_banj = piv[piv["suc_banjercito"] > 0]
    resumen = con_banj.groupby("cve_mun").agg(
        meses_con_banjercito=("yyyymm", "nunique"),
        primer_mes=("yyyymm", "min"),
        ultimo_mes=("yyyymm", "max"),
    )
    fin = piv[piv["yyyymm"] == ultimo].set_index("cve_mun")[["suc_banjercito", "suc_bienestar"]]
    fin.columns = [f"{c}_{ultimo}" for c in fin.columns]
    banj = (
        resumen.join(fin, how="left")
        .fillna({f"suc_banjercito_{ultimo}": 0, f"suc_bienestar_{ultimo}": 0})
        .reset_index()
    )
    banj[f"solo_banjercito_{ultimo}"] = (banj[f"suc_banjercito_{ultimo}"] > 0) & (
        banj[f"suc_bienestar_{ultimo}"] == 0
    )
    banj.to_parquet(SALIDA_BANJ, index=False)
    log.info(
        "Portafolio: %d meses (%s–%s); Banjército en %d municipios en algún mes, %d en %s (%d solo Banjército)",
        largo["yyyymm"].nunique(),
        largo["yyyymm"].min(),
        largo["yyyymm"].max(),
        len(banj),
        int((banj[f"suc_banjercito_{ultimo}"] > 0).sum()),
        ultimo,
        int(banj[f"solo_banjercito_{ultimo}"].sum()),
    )
    return SALIDA

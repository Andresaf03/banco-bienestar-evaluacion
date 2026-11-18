"""Descriptivos B2 y B3 de la fase 6 (preregistro y adenda en `docs/decisiones.md`, 2026-11-17).

- **B2, cobro local** (`fase6_cobro_local.csv`): transacciones en los cajeros del Banco del
  Bienestar (Portafolio CNBV, modelo Power Pivot, tipo 34) por beneficiario único del padrón de
  Bienestar (foto de octubre de 2026), por bimestre, enero–julio de 2026, según el grupo del
  municipio. La pensión de adultos mayores y las becas pagan una vez por bimestre: 1.0 sería un
  retiro en cajero del banco por cada pago.
- **B3, ENIF 2021 contra 2024** (`fase6_enif_apoyos.csv`): entre los adultos que reciben apoyos de
  gobierno (`P3_4 = 1`), la proporción con cuenta para recibirlos (`P5_4_3`), la que usó una
  sucursal (`P10_1`), la que no la usa porque "están muy lejos o no hay" (`P10_2 = 4`) y el tiempo
  a la sucursal que usa (`P10_3_1` horas, `P10_3_2` minutos; 99 = no sabe). Por tamaño de
  localidad (`TLOC`), con el factor de expansión (`FAC_ELE` en 2021, `FAC_PER` en 2024). La ENIF no
  trae municipio: es nacional y no se cruza con el tratamiento.

Los códigos de 2021 vienen del descriptor (`enif_2021_estructura_del_archivo.xlsx`); 2024 no trae
descriptor, así que se verifica que los códigos observados sean los mismos antes de calcular.
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM, PROCESSED, RAW, TABLAS

log = logging.getLogger(__name__)

TRANSACCIONES_CAJERO = "34"
BANCO_DEL_BIENESTAR = "037166"
MESES_2026 = [f"2026{m:02d}" for m in range(1, 8)]
ENIF = {
    2021: ("enif_2021_bd_csv.zip", "FAC_ELE"),
    2024: ("enif_2024_bd_csv.zip", "FAC_PER"),
}
TLOC = {"1": "15 mil o más", "2": "15 mil o más", "3": "2,500 a 15 mil", "4": "menos de 2,500"}
VARIABLES_ENIF = ["P3_4", "P5_4_3", "P10_1", "P10_2", "P10_3_1", "P10_3_2", "TLOC"]
CODIGOS_ESPERADOS = {
    "P3_4": {"1", "2"},
    "P5_4_3": {"1", "2"},
    "P10_1": {"1", "2"},
    "TLOC": {"1", "2", "3", "4"},
}
# La razón de no usar sucursal cambió de catálogo en 2024 (se agregaron "prefiere las aplicaciones"
# y "no ha tenido necesidad"): "están muy lejos o no hay" es 4 en 2021 (descriptor) y 05 en 2024
# (diccionario del INEGI, catálogo 1081, variable V8863).
RAZONES_P10_2 = {
    2021: ({str(i) for i in range(1, 10)}, "4"),
    2024: ({f"{i:02d}" for i in range(1, 11)}, "05"),
}


# --------------------------------------------------------------------------- B2
def cobro_local() -> pd.DataFrame:
    mod = pd.read_parquet(INTERIM / "cnbv_portafolio_modelo.parquet")
    tx = mod[
        (mod["institucion"] == BANCO_DEL_BIENESTAR)
        & (mod["tipo"].astype(str) == TRANSACCIONES_CAJERO)
        & (mod["yyyymm"].astype(str).isin(MESES_2026))
    ]
    meses = tx["yyyymm"].nunique()
    # El Portafolio usa las claves vigentes del INEGI; el padrón ya viene en claves estables.
    estable = tx["cve_mun"].map(mapa_crosswalk()).fillna(tx["cve_mun"])
    por_mun = tx.groupby(estable)["valor"].sum().rename("transacciones")
    pub = pd.read_parquet(PROCESSED / "pub_municipio_f6.parquet")
    pub = pub.merge(por_mun, left_on="cve_mun", right_index=True, how="left")
    pub["transacciones"] = pub["transacciones"].fillna(0)
    filas = []
    for grupo, d in [("todos", pub), *pub.groupby("grupo")]:
        benef = d["beneficiarios_unicos"].sum()
        filas.append(
            {
                "grupo": grupo,
                "municipios": len(d),
                "con_cajero_del_banco": int((d["transacciones"] > 0).sum()),
                "beneficiarios_unicos": benef,
                "transacciones_mensuales": d["transacciones"].sum() / meses,
                "tx_por_beneficiario_bimestre": 2 * d["transacciones"].sum() / meses / benef,
            }
        )
    salida = pd.DataFrame(filas)
    salida["meses"] = meses
    return salida


# --------------------------------------------------------------------------- B3
def _leer_enif(anio: int) -> pd.DataFrame:
    archivo, factor = ENIF[anio]
    with zipfile.ZipFile(RAW / "enif" / str(anio) / archivo) as z, z.open("TMODULO.csv") as f:
        d = pd.read_csv(f, dtype=str, usecols=[*VARIABLES_ENIF, factor], encoding="latin-1")
    d = d.rename(columns={factor: "factor"})
    d["factor"] = pd.to_numeric(d["factor"], errors="raise")
    for c in VARIABLES_ENIF:
        d[c] = d[c].fillna("").str.strip()
    esperados_p10_2, _ = RAZONES_P10_2[anio]
    for c, esperados in [*CODIGOS_ESPERADOS.items(), ("P10_2", esperados_p10_2)]:
        observados = set(d[c].unique()) - {""}
        if not observados <= esperados:
            raise ValueError(f"ENIF {anio}: códigos de {c} fuera del descriptor: {observados}")
    return d


def _pct(d: pd.DataFrame, condicion: pd.Series, universo: pd.Series) -> float:
    w = d.loc[universo, "factor"]
    return float(100 * w[condicion[universo]].sum() / w.sum()) if w.sum() else np.nan


def _minutos(d: pd.DataFrame) -> pd.Series:
    h = pd.to_numeric(d["P10_3_1"], errors="coerce")
    m = pd.to_numeric(d["P10_3_2"], errors="coerce")
    valido = h.notna() & m.notna() & (h != 99) & (m != 99)
    return (60 * h + m).where(valido)


def _mediana_ponderada(x: pd.Series, w: pd.Series) -> float:
    ok = x.notna()
    if not ok.any():
        return np.nan
    x, w = x[ok].to_numpy(float), w[ok].to_numpy(float)
    orden = np.argsort(x)
    acumulado = np.cumsum(w[orden]) / w.sum()
    return float(x[orden][np.searchsorted(acumulado, 0.5)])


def enif_apoyos() -> pd.DataFrame:
    filas = []
    for anio in ENIF:
        d = _leer_enif(anio)
        d["tamano"] = d["TLOC"].map(TLOC)
        d["minutos"] = _minutos(d)
        for tamano, g in [("nacional", d), *d.groupby("tamano")]:
            recibe = g["P3_4"] == "1"
            usa = recibe & (g["P10_1"] == "1")
            no_usa = recibe & (g["P10_1"] == "2")
            lejania = g["P10_2"] == RAZONES_P10_2[anio][1]
            filas.append(
                {
                    "anio": anio,
                    "tamano_localidad": tamano,
                    "n_recibe": int(recibe.sum()),
                    "pct_adultos_recibe": _pct(g, recibe, pd.Series(True, index=g.index)),
                    "pct_cuenta_para_apoyos": _pct(g, g["P5_4_3"] == "1", recibe),
                    "pct_uso_sucursal": _pct(g, g["P10_1"] == "1", recibe),
                    "pct_no_usa_por_lejania": _pct(g, lejania, no_usa),
                    "minutos_sucursal_mediana": _mediana_ponderada(
                        g.loc[usa, "minutos"], g.loc[usa, "factor"]
                    ),
                    "minutos_sucursal_media": float(
                        np.average(
                            g.loc[usa & g["minutos"].notna(), "minutos"],
                            weights=g.loc[usa & g["minutos"].notna(), "factor"],
                        )
                    )
                    if (usa & g["minutos"].notna()).any()
                    else np.nan,
                }
            )
    return pd.DataFrame(filas)


def generar() -> list[Path]:
    TABLAS.mkdir(parents=True, exist_ok=True)
    rutas = []
    for nombre, tabla in (
        ("fase6_cobro_local", cobro_local()),
        ("fase6_enif_apoyos", enif_apoyos()),
    ):
        ruta = TABLAS / f"{nombre}.csv"
        tabla.round(3).to_csv(ruta, index=False)
        log.info("%s:\n%s", nombre, tabla.round(2).to_string(index=False))
        rutas.append(ruta)
    return rutas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

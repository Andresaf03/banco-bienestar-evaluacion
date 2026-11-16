"""Limpieza de la BDIF municipal: apila todos los trimestres en formato largo.

Salidas (Parquet):
- `data/interim/cnbv_bdif.parquet`: `cve_mun, periodo, t, sector, variable, valor, hoja, archivo`.
  Solo conteos absolutos (sucursales, contratos, transacciones...). Los indicadores por 10 mil
  adultos se descartan porque se recalculan en el panel con el denominador elegido.
- `data/interim/cnbv_bdif_poblacion.parquet`: `cve_mun, periodo, t, poblacion, poblacion_adulta,
  poblacion_adulta_mujeres, poblacion_adulta_hombres, tipo_poblacion, region, nom_ent, nom_mun,
  indice_rezago_social` (una fila por municipio-trimestre, tomada de la hoja de infraestructura).
- `data/interim/cnbv_bdif/<YYYYMM>.parquet`: caché por trimestre (se salta si ya existe).
- `data/interim/cnbv_bdif_columnas.csv`: bitácora de cómo se clasificó cada columna de cada hoja
  de cada trimestre (insumo del diccionario).

Los valores se leen con `openpyxl` en modo `data_only=True` (valores cacheados de las fórmulas
`=SUM(...)` que la CNBV deja en algunas celdas).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import openpyxl
import pandas as pd

from proyecto.limpieza.bdif_columnas import clasificar, normalizar
from proyecto.utils.claves import es_valida, normalizar_cve
from proyecto.utils.io import INTERIM, RAW
from proyecto.utils.periodos import periodo_a_t, yyyymm_a_periodo

log = logging.getLogger(__name__)

FUENTE = "cnbv_bdif"
CACHE = INTERIM / FUENTE
SALIDA = INTERIM / f"{FUENTE}.parquet"
SALIDA_POB = INTERIM / f"{FUENTE}_poblacion.parquet"
SALIDA_COLS = INTERIM / f"{FUENTE}_columnas.csv"
_RE_ARCHIVO = re.compile(r"Base_de_Datos_de_Inclusion_Financiera_(\d{6})\.(xlsx|xlsm|xls)$")
MAX_FILAS_ENCABEZADO = 14
# Renglones sobre el encabezado donde la CNBV pone las etiquetas de bloque. En las eras B y C la
# etiqueta "Indicadores Demográficos (Contratos por cada 10,000 adultos)" está 5 filas arriba.
FILAS_NIVELES = 6
COLS_POBLACION = [
    "poblacion",
    "poblacion_adulta",
    "poblacion_adulta_mujeres",
    "poblacion_adulta_hombres",
    "tipo_poblacion",
    "region",
    "nom_ent",
    "nom_mun",
    "indice_rezago_social",
]


def archivos_bdif() -> list[tuple[str, Path]]:
    """[(YYYYMM, ruta)] ordenados, de los Excel municipales descargados."""
    salida = []
    for p in sorted((RAW / FUENTE).glob("Base_de_Datos_de_Inclusion_Financiera_*.xls*")):
        m = _RE_ARCHIVO.search(p.name)
        if m:
            salida.append((m.group(1), p))
    return salida


def _es_encabezado(fila: tuple) -> bool:
    return any(normalizar(c).startswith("clave municipio") for c in fila if c is not None)


def _niveles(filas: list[tuple], hdr: int, ncol: int) -> list[list[str]]:
    """Etiquetas de los renglones sobre el encabezado, con forward-fill hacia la derecha."""
    niveles = []
    for k in range(max(0, hdr - FILAS_NIVELES), hdr):
        fila = list(filas[k]) + [None] * (ncol - len(filas[k]))
        celdas = [str(v).strip() for v in fila if v is not None and str(v).strip()]
        if not celdas or all(c.replace(".", "").isdigit() for c in celdas):
            continue  # renglón vacío o con índices numéricos de la CNBV
        ff, actual = [], ""
        for v in fila:
            if v is not None and str(v).strip():
                actual = str(v).strip()
            ff.append(actual)
        niveles.append(ff)
    return niveles


def leer_hoja(ws, hoja: str, yyyymm: str) -> tuple[pd.DataFrame, list[dict]]:
    """Lee una hoja municipal y devuelve (tabla larga, bitácora de columnas)."""
    filas = list(ws.iter_rows(values_only=True))
    hdr = next((i for i, f in enumerate(filas[:MAX_FILAS_ENCABEZADO]) if _es_encabezado(f)), None)
    if hdr is None:
        return pd.DataFrame(), []
    ncol = max(len(f) for f in filas[: hdr + 1])
    niveles = _niveles(filas, hdr, ncol)
    encabezado = list(filas[hdr]) + [None] * (ncol - len(filas[hdr]))

    mapa: dict[int, tuple[str, str]] = {}
    bitacora = []
    for j in range(ncol):
        enc = encabezado[j]
        if enc is None or not str(enc).strip():
            continue
        niv = [n[j] for n in niveles]
        res = clasificar(hoja, niv, str(enc))
        bitacora.append(
            {
                "yyyymm": yyyymm,
                "hoja": hoja,
                "columna": j + 1,
                "niveles": " | ".join(niv),
                "encabezado": str(enc).replace("\n", " "),
                "sector": res[0] if res else "",
                "variable": res[1] if res else "",
            }
        )
        if res and res in mapa.values() and res[0] != "_general":
            # Bloque repetido sin etiqueta: la CNBV pone primero los conteos y luego los
            # indicadores por 10 mil adultos; se conserva la primera aparición.
            bitacora[-1]["sector"], bitacora[-1]["variable"] = "", ""
            bitacora[-1]["nota"] = "descartada: bloque repetido (indicador por 10 mil adultos)"
            continue
        if res:
            mapa[j] = res
    if "cve_mun" not in {v for s, v in mapa.values() if s == "_general"}:
        raise ValueError(f"{yyyymm} {hoja}: no se encontró la columna de clave municipal")

    col_cve = next(j for j, (s, v) in mapa.items() if s == "_general" and v == "cve_mun")
    registros = []
    for fila in filas[hdr + 1 :]:
        fila = list(fila) + [None] * (ncol - len(fila))
        cve = normalizar_cve(fila[col_cve])
        if cve is None or not es_valida(cve):
            continue
        reg = {"cve_mun": cve}
        for j, (sector, variable) in mapa.items():
            if j != col_cve:
                reg[(sector, variable)] = fila[j]
        registros.append(reg)
    ancho = pd.DataFrame(registros)
    return ancho, bitacora


def _a_largo(ancho: pd.DataFrame, hoja: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa columnas generales (población) de las variables y pasa estas a formato largo."""
    generales = {c: c[1] for c in ancho.columns if isinstance(c, tuple) and c[0] == "_general"}
    pob = ancho[["cve_mun", *generales]].rename(columns=generales)
    var_cols = [c for c in ancho.columns if isinstance(c, tuple) and c[0] != "_general"]
    if not var_cols:
        return pob, pd.DataFrame()
    largo = ancho[["cve_mun", *var_cols]].melt(
        id_vars="cve_mun", var_name="clave", value_name="valor"
    )
    largo["sector"] = largo["clave"].map(lambda c: c[0])
    largo["variable"] = largo["clave"].map(lambda c: c[1])
    largo["valor"] = pd.to_numeric(largo["valor"], errors="coerce")
    largo["hoja"] = hoja
    return pob, largo.drop(columns="clave")


def procesar_trimestre(yyyymm: str, ruta: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    periodo = yyyymm_a_periodo(yyyymm)
    t = periodo_a_t(periodo)
    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    largos, poblaciones, bitacora = [], [], []
    for ws in wb.worksheets:
        if not ws.title.strip().endswith("Mun"):
            continue
        ancho, bit = leer_hoja(ws, ws.title.strip(), yyyymm)
        bitacora.extend(bit)
        if ancho.empty:
            continue
        pob, largo = _a_largo(ancho, ws.title.strip())
        if not largo.empty:
            largos.append(largo)
        poblaciones.append(pob)
    wb.close()
    largo = pd.concat(largos, ignore_index=True)
    largo.insert(1, "periodo", periodo)
    largo.insert(2, "t", t)
    largo["archivo"] = ruta.name
    # Población: se toma de la hoja con más columnas generales (infraestructura); se completa con
    # el resto por si alguna hoja trae una columna que las demás no.
    pob = pd.concat(poblaciones, ignore_index=True)
    pob = pob.groupby("cve_mun", as_index=False).first()
    for c in COLS_POBLACION:
        if c not in pob.columns:
            pob[c] = pd.NA
    pob = pob[["cve_mun", *COLS_POBLACION]]
    pob.insert(1, "periodo", periodo)
    pob.insert(2, "t", t)
    for c in (
        "poblacion",
        "poblacion_adulta",
        "poblacion_adulta_mujeres",
        "poblacion_adulta_hombres",
    ):
        pob[c] = pd.to_numeric(pob[c], errors="coerce")
    return largo, pob, bitacora


def limpiar(force: bool = False) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    largos, pobs, bitacoras = [], [], []
    for yyyymm, ruta in archivos_bdif():
        cache_largo = CACHE / f"{yyyymm}.parquet"
        cache_pob = CACHE / f"{yyyymm}_poblacion.parquet"
        cache_cols = CACHE / f"{yyyymm}_columnas.csv"
        if not force and cache_largo.exists() and cache_pob.exists() and cache_cols.exists():
            largos.append(pd.read_parquet(cache_largo))
            pobs.append(pd.read_parquet(cache_pob))
            bitacoras.append(pd.read_csv(cache_cols, dtype=str, keep_default_na=False))
            continue
        log.info("BDIF %s", yyyymm)
        largo, pob, bit = procesar_trimestre(yyyymm, ruta)
        largo.to_parquet(cache_largo, index=False)
        pob.to_parquet(cache_pob, index=False)
        pd.DataFrame(bit).to_csv(cache_cols, index=False)
        largos.append(largo)
        pobs.append(pob)
        bitacoras.append(pd.DataFrame(bit).fillna("").astype(str))
    largo = pd.concat(largos, ignore_index=True)
    largo = largo.astype(
        {
            "cve_mun": "string",
            "periodo": "string",
            "sector": "string",
            "variable": "string",
            "hoja": "string",
            "archivo": "string",
        }
    )
    largo.to_parquet(SALIDA, index=False)
    pob = pd.concat(pobs, ignore_index=True)
    pob.to_parquet(SALIDA_POB, index=False)
    pd.concat(bitacoras, ignore_index=True).to_csv(SALIDA_COLS, index=False)
    log.info("BDIF: %d filas largas, %d filas de población", len(largo), len(pob))
    return SALIDA

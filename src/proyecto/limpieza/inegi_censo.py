"""INEGI, ITER 2020 y 2010: totales municipales y localidades con coordenadas.

Salidas:
- `data/interim/inegi_censo_2020.parquet`: una fila por municipio (`LOC == 0000`) con todas las
  variables del ITER 2020, clave `cve_mun` de 5 dígitos. Los valores `*` (confidencialidad) y
  `N/D` quedan como faltantes.
- `data/interim/inegi_censo_2010.parquet`: ídem para 2010.
- `data/interim/inegi_censo_localidades_2010.parquet` y `..._2020.parquet`: localidades con
  coordenadas decimales (`lon`, `lat`), población y clave municipal vigente en ese censo. Se usan
  para el crosswalk de municipios (ver `limpieza.municipios`).
"""

from __future__ import annotations

import logging
import re
import zipfile
from pathlib import Path

import pandas as pd

from proyecto.utils.claves import combinar, combinar_localidad
from proyecto.utils.io import INTERIM, RAW

log = logging.getLogger(__name__)

FUENTE = "inegi_censo"
ZIPS = {
    2020: (RAW / FUENTE / "iter_00_cpv2020_csv.zip", "conjunto_de_datos_iter_00CSV20.csv"),
    2010: (RAW / FUENTE / "iter_nal_2010_csv.zip", "iter_00_cpv2010.csv"),
}
FALTANTES = {"*", "N/D", "", "-"}
_RE_DMS = re.compile(r"""^\s*(\d+)°(\d+)'([\d.]+)"\s*([NSEW])\s*$""")


def _leer_csv(anio: int) -> pd.DataFrame:
    ruta, nombre = ZIPS[anio]
    with zipfile.ZipFile(ruta) as z:
        miembro = next(m for m in z.namelist() if m.endswith(nombre))
        with z.open(miembro) as f:
            df = pd.read_csv(f, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def dms_a_decimal(texto: str) -> float | None:
    """`102°17'45.768" W` -> -102.296... (ITER 2020)."""
    m = _RE_DMS.match(texto or "")
    if not m:
        return None
    g, mi, s, h = int(m.group(1)), int(m.group(2)), float(m.group(3)), m.group(4)
    valor = g + mi / 60 + s / 3600
    return -valor if h in ("W", "S") else valor


def ddmmss_a_decimal(texto: str, hemisferio_negativo: bool) -> float | None:
    """`1021746` -> -102.296... (ITER 2010: grados, minutos y segundos concatenados)."""
    t = (texto or "").strip()
    if not t.isdigit() or len(t) < 5:
        return None
    s, mi, g = int(t[-2:]), int(t[-4:-2]), int(t[:-4])
    valor = g + mi / 60 + s / 3600
    return -valor if hemisferio_negativo else valor


def _numerico(df: pd.DataFrame, excluir: set[str]) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if c in excluir:
            continue
        out[c] = pd.to_numeric(out[c].where(~out[c].isin(FALTANTES)), errors="coerce")
    return out


def limpiar_anio(anio: int) -> tuple[Path, Path]:
    df = _leer_csv(anio)
    df["cve_mun"] = combinar(df["entidad"], df["mun"])
    texto = {
        "entidad",
        "nom_ent",
        "mun",
        "nom_mun",
        "loc",
        "nom_loc",
        "longitud",
        "latitud",
        "cve_mun",
    }

    municipal = df[(df["mun"] != "000") & (df["loc"] == "0000")].copy()
    municipal = _numerico(municipal, texto).drop(columns=["loc", "nom_loc", "longitud", "latitud"])
    municipal = municipal[["cve_mun", *[c for c in municipal.columns if c != "cve_mun"]]]
    salida_mun = INTERIM / f"{FUENTE}_{anio}.parquet"
    municipal.to_parquet(salida_mun, index=False)

    loc = df[(df["mun"] != "000") & (~df["loc"].isin(["0000", "9998", "9999"]))].copy()
    if anio == 2020:
        loc["lon"] = loc["longitud"].map(dms_a_decimal)
        loc["lat"] = loc["latitud"].map(dms_a_decimal)
    else:
        loc["lon"] = loc["longitud"].map(lambda v: ddmmss_a_decimal(v, True))
        loc["lat"] = loc["latitud"].map(lambda v: ddmmss_a_decimal(v, False))
    loc["pobtot"] = pd.to_numeric(
        loc["pobtot"].where(~loc["pobtot"].isin(FALTANTES)), errors="coerce"
    )
    # La clave única de localidad es ent(2)+mun(3)+loc(4) = 9 dígitos; el ITER publica el
    # consecutivo de 4 por separado, que no es único a nivel nacional.
    loc["cve_loc"] = combinar_localidad(loc["cve_mun"], loc["loc"])
    loc = loc[
        ["cve_loc", "cve_mun", "entidad", "mun", "loc", "nom_loc", "lon", "lat", "pobtot"]
    ].rename(columns={"entidad": "cve_ent", "mun": "cve_mun3", "loc": "cve_loc4"})
    salida_loc = INTERIM / f"{FUENTE}_localidades_{anio}.parquet"
    loc.to_parquet(salida_loc, index=False)
    log.info(
        "ITER %d: %d municipios, %d localidades (%d sin coordenadas)",
        anio,
        len(municipal),
        len(loc),
        loc["lon"].isna().sum(),
    )
    return salida_mun, salida_loc


def limpiar() -> Path:
    for anio in (2020, 2010):
        limpiar_anio(anio)
    return INTERIM / f"{FUENTE}_2020.parquet"

"""Luz nocturna VIIRS por localidad -> `data/interim/viirs_localidad.parquet` (fase 2).

Para cada año de `parametros.fase2.viirs.anios` se recorta la ventana de México del GeoTIFF global
(`data/raw/viirs/`) con `gdal_translate` a un ráster crudo temporal (ENVI, Int16), alineado a la
malla original (`-srcwin` en píxeles, sin remuestrear). Luego, para cada localidad del marco del
panel de localidades (ITER 2020, piso de población de config), se suma la radiancia de los píxeles
cuyo **centro** cae:

- a ≤ `radio_km` del punto de la localidad (`luz_1km`, `npix_1km`), y
- en el anillo (`anillo_km[0]`, `anillo_km[1]`] (`luz_anillo`, `npix_anillo`): la luz de alrededor
  sin el núcleo, donde está la sucursal (su propia iluminación es un efecto mecánico).

Unidades (verificado el 2026-10-07, antes de estimar): el autor reescaló el VNL V2 a 0–2000, pero
los archivos no son homogéneos. En 2016–2021 el entero almacenado es 10 × radiancia (sin etiqueta
de escala; CDMX 2021 = 1,200 → 120 nW/cm²/sr); en 2022–2024 el entero es la radiancia redondeada
con la etiqueta GDAL `scale = 10` (CDMX 2022 = 133). La radiancia es `valor × escala / 10`, y con
`armonizar_precision` los años con precisión de 0.1 se redondean al entero, para que el margen
extensivo (radiancia > 0) no cambie de definición en 2022. Además 2022 es el producto VNL v2.2 de
dos satélites (`npp-j01`) y 2023–2024 el VNL v2 de SNPP: ruptura documentada en docs/decisiones.md.
`-32768` es sin dato y se excluye (no se cuenta como cero). La distancia es equirrectangular local
(error < 0.1% a 3 km).

Requiere GDAL en la línea de comandos (`gdal_translate`, `brew install gdal`).
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.utils.io import INTERIM, RAW, parametros

log = logging.getLogger(__name__)

SALIDA = INTERIM / "viirs_localidad.parquet"
SIN_DATO = -32768
KM_GRADO_LAT = 110.574
KM_GRADO_LON_ECUADOR = 111.320


def _info(tif: Path) -> dict:
    import json

    return json.loads(
        subprocess.run(
            ["gdalinfo", "-json", str(tif)], check=True, capture_output=True, text=True
        ).stdout
    )


def _geotransform(tif: Path) -> tuple[float, float, float, float]:
    """(lon0, px_lon, lat0, px_lat) del GeoTIFF global, leídos con gdalinfo."""
    gt = _info(tif)["geoTransform"]
    return gt[0], gt[1], gt[3], gt[5]


def factor_radiancia(tif: Path) -> float:
    """Multiplicador que lleva el entero almacenado a nW/cm²/sr: escala GDAL (1 si falta) / 10."""
    banda = _info(tif)["bands"][0]
    return float(banda.get("scale", 1.0)) / 10.0


def recortar(tif: Path, ventana: list[float], tmp: Path) -> tuple[np.ndarray, float, float, float]:
    """Recorta la ventana `[lon_min, lat_max, lon_max, lat_min]` sin remuestrear.

    Devuelve la matriz Int16 y (lon del borde izquierdo, lat del borde superior, tamaño de píxel).
    """
    lon0, px, lat0, py = _geotransform(tif)
    if abs(px + py) > 1e-12:
        raise ValueError("se esperaba píxel cuadrado en grados")
    lon_min, lat_max, lon_max, lat_min = ventana
    col0 = int(np.floor((lon_min - lon0) / px))
    fila0 = int(np.floor((lat_max - lat0) / py))
    ncol = int(np.ceil((lon_max - lon0) / px)) - col0
    nfila = int(np.ceil((lat_min - lat0) / py)) - fila0
    crudo = tmp / f"{tif.stem}.img"
    subprocess.run(
        [
            "gdal_translate",
            "-q",
            "-of",
            "ENVI",
            "-srcwin",
            str(col0),
            str(fila0),
            str(ncol),
            str(nfila),
            str(tif),
            str(crudo),
        ],
        check=True,
    )
    m = np.fromfile(crudo, dtype="<i2").reshape(nfila, ncol)
    return m, lon0 + col0 * px, lat0 + fila0 * py, px


def sumas_por_localidad(
    m: np.ndarray,
    lon_izq: float,
    lat_sup: float,
    px: float,
    lat: np.ndarray,
    lon: np.ndarray,
    radio_km: float,
    anillo_km: tuple[float, float],
    factor: float,
    redondear: bool,
    bloque: int = 5000,
) -> pd.DataFrame:
    """Suma de radiancia y píxeles válidos en el disco y el anillo, por bloques de localidades."""
    partes = [
        _sumas_bloque(
            m,
            lon_izq,
            lat_sup,
            px,
            lat[i : i + bloque],
            lon[i : i + bloque],
            radio_km,
            anillo_km,
            factor,
            redondear,
        )
        for i in range(0, len(lat), bloque)
    ]
    return pd.concat(partes, ignore_index=True)


def _sumas_bloque(
    m: np.ndarray,
    lon_izq: float,
    lat_sup: float,
    px: float,
    lat: np.ndarray,
    lon: np.ndarray,
    radio_km: float,
    anillo_km: tuple[float, float],
    factor: float,
    redondear: bool,
) -> pd.DataFrame:
    alcance = anillo_km[1]
    k = int(np.ceil(alcance / (px * KM_GRADO_LON_ECUADOR * np.cos(np.radians(33.0))))) + 1
    dj, di = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
    dj, di = dj.ravel(), di.ravel()
    col = np.floor((lon - lon_izq) / px).astype(int)
    fila = np.floor((lat_sup - lat) / px).astype(int)
    cols = col[:, None] + dj[None, :]
    filas = fila[:, None] + di[None, :]
    dentro = (cols >= 0) & (cols < m.shape[1]) & (filas >= 0) & (filas < m.shape[0])
    valores = np.where(
        dentro, m[np.clip(filas, 0, m.shape[0] - 1), np.clip(cols, 0, m.shape[1] - 1)], SIN_DATO
    )
    lon_c = lon_izq + (cols + 0.5) * px
    lat_c = lat_sup - (filas + 0.5) * px
    dx = (lon_c - lon[:, None]) * KM_GRADO_LON_ECUADOR * np.cos(np.radians(lat[:, None]))
    dy = (lat_c - lat[:, None]) * KM_GRADO_LAT
    d = np.hypot(dx, dy)
    # Radiancia negativa = sin dato: artefactos puntuales que solo aparecen en 2016–2021 (decenas de
    # píxeles por año en la ventana de México; el log de `limpiar` los cuenta).
    valido = (valores != SIN_DATO) & (valores >= 0)
    rad = valores * factor
    if redondear:
        rad = np.round(rad)
    rad = np.where(valido, rad, 0.0)
    disco = valido & (d <= radio_km)
    anillo = valido & (d > anillo_km[0]) & (d <= anillo_km[1])
    return pd.DataFrame(
        {
            "luz_1km": (rad * disco).sum(axis=1),
            "npix_1km": disco.sum(axis=1),
            "luz_anillo": (rad * anillo).sum(axis=1),
            "npix_anillo": anillo.sum(axis=1),
        }
    )


def limpiar() -> Path:
    cfg = parametros()["fase2"]["viirs"]
    if shutil.which("gdal_translate") is None:
        raise RuntimeError("falta gdal_translate (GDAL) en el PATH")
    minimo = parametros()["unidades"]["localidad_pob_minima"]
    censo = pd.read_parquet(
        INTERIM / "inegi_censo_localidades_2020.parquet",
        columns=["cve_loc", "cve_mun", "lat", "lon", "pobtot"],
    )
    marco = censo[(censo["pobtot"] >= minimo) & censo["lat"].notna() & censo["lon"].notna()]
    marco = marco.reset_index(drop=True)
    lat, lon = marco["lat"].to_numpy(float), marco["lon"].to_numpy(float)
    partes = []
    with tempfile.TemporaryDirectory(prefix="viirs_") as d:
        tmp = Path(d)
        for anio in cfg["anios"]:
            tif = next((RAW / "viirs").glob(f"*_{anio}0101_{anio}1231_*.tif"), None)
            if tif is None:
                raise FileNotFoundError(f"falta el GeoTIFF de {anio}: corre `make descargar-fase2`")
            m, lon_izq, lat_sup, px = recortar(tif, cfg["ventana_mexico"], tmp)
            negativos = int(((m < 0) & (m != SIN_DATO)).sum())
            factor = factor_radiancia(tif)
            # Solo los años con precisión de 0.1 (factor < 1) se redondean al entero.
            redondear = bool(cfg["armonizar_precision"]) and factor < 1.0
            s = sumas_por_localidad(
                m,
                lon_izq,
                lat_sup,
                px,
                lat,
                lon,
                cfg["radio_km"],
                tuple(cfg["anillo_km"]),
                factor,
                redondear,
            )
            s.insert(0, "cve_loc", marco["cve_loc"].to_numpy())
            s["anio"] = anio
            s["factor_radiancia"] = factor
            s["producto"] = (
                _info(tif).get("metadata", {}).get("", {}).get("TIFFTAG_DOCUMENTNAME", "")
            )
            partes.append(s)
            log.info(
                "VIIRS %d: %d localidades; factor %.1f%s; píxeles negativos excluidos %d; con "
                "luz a 1 km %.1f%%; luz total %.0f",
                anio,
                len(s),
                factor,
                " (redondeado)" if redondear else "",
                negativos,
                100 * (s["luz_1km"] > 0).mean(),
                s["luz_1km"].sum(),
            )
            for f in tmp.iterdir():
                f.unlink()
    out = pd.concat(partes, ignore_index=True)
    out.to_parquet(SALIDA, index=False)
    return SALIDA

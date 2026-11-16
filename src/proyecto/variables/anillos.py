"""Anillos: conteo de establecimientos del DENUE dentro de un radio de cada centro.

Motivación (nota del asesor): el municipio puede ser demasiado grande para que una sucursal mueva
el agregado. Contando establecimientos dentro de 1, 2, 5 y 10 km de cada sucursal se puede ver si
el efecto **decae con la distancia**. Si no decae suavemente, el radio no es la unidad adecuada y
la localidad sí; si decae, el radio captura mejor el área de influencia.

Centros:
- **tratados**: las localidades con sucursal del Banco del Bienestar (`tratamiento_localidad`),
  usando las coordenadas de la propia localidad para que tratados y controles sean comparables
  (si se usara la coordenada exacta de la sucursal, el centro tratado estaría sesgado hacia donde
  ya había actividad económica);
- **controles**: localidades sin sucursal, con al menos `localidad_pob_minima` habitantes.

Salida `data/interim/anillos.parquet`: una fila por `cve_loc × radio_km × semestre × bloque` con
`n_estab`, `n_micro` y `empleo_est`. El conteo usa distancia haversine sobre un `BallTree` de
scikit-learn cuando está disponible; si no, una malla espacial propia (sin dependencia nueva).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.limpieza.denue_clasificacion import BLOQUES
from proyecto.utils.io import INTERIM, parametros

log = logging.getLogger(__name__)

SALIDA = INTERIM / "anillos.parquet"
PARTES = INTERIM / "denue" / "partes"
RADIO_TIERRA_KM = 6371.0
GRADO_LAT_KM = 111.32
MIN_POB_CENTRO_ANILLO = 500  # controles con al menos 500 habitantes


def _indice_malla(lat: np.ndarray, lon: np.ndarray, celda_km: float):
    """Índice espacial simple: diccionario de celdas -> índices de puntos.

    Evita agregar una dependencia solo para esto y es suficientemente rápido: cada consulta
    revisa las celdas vecinas al radio pedido.
    """
    paso_lat = celda_km / GRADO_LAT_KM
    paso_lon = celda_km / (GRADO_LAT_KM * np.cos(np.radians(np.clip(lat, -89, 89))))
    cel_lat = np.floor(lat / paso_lat).astype(np.int64)
    cel_lon = np.floor(lon / np.where(paso_lon == 0, 1e-9, paso_lon)).astype(np.int64)
    malla: dict[tuple[int, int], list[int]] = {}
    for i, (a, b) in enumerate(zip(cel_lat, cel_lon, strict=True)):
        malla.setdefault((int(a), int(b)), []).append(i)
    return malla, paso_lat


def _haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * RADIO_TIERRA_KM * np.arcsin(np.sqrt(a))


def contar_en_radios(
    centros: pd.DataFrame, puntos: pd.DataFrame, radios_km: list[float]
) -> pd.DataFrame:
    """Cuenta puntos dentro de cada radio alrededor de cada centro.

    `centros`: columnas `cve_loc, lat, lon`. `puntos`: `lat, lon, micro, empleo_est` + una columna
    booleana por bloque. Devuelve filas `cve_loc × radio_km × bloque`.
    """
    try:
        from sklearn.neighbors import BallTree  # type: ignore

        arbol = BallTree(np.radians(puntos[["lat", "lon"]].to_numpy()), metric="haversine")
        vecinos_por_radio = {
            r: arbol.query_radius(
                np.radians(centros[["lat", "lon"]].to_numpy()), r=r / RADIO_TIERRA_KM
            )
            for r in radios_km
        }
    except ImportError:  # malla propia
        vecinos_por_radio = _vecinos_malla(centros, puntos, radios_km)

    micro = puntos["micro"].to_numpy(dtype=bool)
    empleo = np.nan_to_num(puntos["empleo_est"].to_numpy(dtype=float))
    marcas = {b: puntos[b].to_numpy(dtype=bool) for b in BLOQUES if b in puntos.columns}
    claves = centros["cve_loc"].to_numpy()
    n_centros = len(claves)

    bloques_salida = []
    for r, vecinos in vecinos_por_radio.items():
        # Aplanar la lista de vecinos: en vez de un bucle de Python por centro (que domina el
        # costo con decenas de miles de centros), se acumula con bincount sobre el array plano.
        largos = np.fromiter((len(v) for v in vecinos), dtype=np.int64, count=n_centros)
        plano = np.concatenate(vecinos) if largos.sum() else np.empty(0, dtype=np.int64)
        centro_de = np.repeat(np.arange(n_centros), largos)
        for bloque, marca in marcas.items():
            sel = marca[plano] if plano.size else np.empty(0, dtype=bool)
            c = centro_de[sel]
            n_estab = np.bincount(c, minlength=n_centros)
            n_micro = np.bincount(c, weights=micro[plano[sel]], minlength=n_centros)
            empl = np.bincount(c, weights=empleo[plano[sel]], minlength=n_centros)
            bloques_salida.append(
                pd.DataFrame(
                    {
                        "cve_loc": claves,
                        "radio_km": r,
                        "bloque": bloque,
                        "n_estab": n_estab.astype("int32"),
                        "n_micro": n_micro.astype("int32"),
                        "empleo_est": empl.astype("float32"),
                    }
                )
            )
    return pd.concat(bloques_salida, ignore_index=True)


def _vecinos_malla(centros, puntos, radios_km):
    lat_p = puntos["lat"].to_numpy(dtype=float)
    lon_p = puntos["lon"].to_numpy(dtype=float)
    salida = {}
    for r in radios_km:
        malla, paso_lat = _indice_malla(lat_p, lon_p, r)
        vecinos = []
        for lat_c, lon_c in centros[["lat", "lon"]].to_numpy(dtype=float):
            paso_lon = r / (GRADO_LAT_KM * max(np.cos(np.radians(lat_c)), 1e-6))
            cl, co = int(np.floor(lat_c / paso_lat)), int(np.floor(lon_c / paso_lon))
            cand = [
                i
                for da in (-1, 0, 1)
                for db in (-1, 0, 1)
                for i in malla.get((cl + da, co + db), ())
            ]
            if not cand:
                vecinos.append(np.array([], dtype=int))
                continue
            cand = np.array(cand)
            d = _haversine(lat_c, lon_c, lat_p[cand], lon_p[cand])
            vecinos.append(cand[d <= r])
        salida[r] = vecinos
    return salida


def centros() -> pd.DataFrame:
    """Localidades tratadas (con sucursal) y controles con población suficiente."""
    p = parametros()
    loc = pd.read_parquet(INTERIM / "inegi_censo_localidades_2020.parquet")
    trat = pd.read_parquet(INTERIM / "tratamiento_localidad.parquet")
    # Para los anillos basta con las localidades tratadas y controles con cierto tamaño: incluir
    # las ~69 mil localidades diminutas multiplicaría el costo sin aportar controles útiles.
    minimo = max(p["unidades"]["localidad_pob_minima"], MIN_POB_CENTRO_ANILLO)
    base = loc[(loc["pobtot"] >= minimo) | loc["cve_loc"].isin(trat["cve_loc"])]
    base = base[["cve_loc", "cve_mun", "nom_loc", "lat", "lon", "pobtot"]].copy()
    base["tratada"] = base["cve_loc"].isin(trat["cve_loc"])
    return base


def construir(versiones: list[str] | None = None) -> Path:
    p = parametros()
    radios = [float(r) for r in p["unidades"]["anillos_km"]]
    cen = centros()
    log.info("anillos: %d centros (%d tratados)", len(cen), int(cen["tratada"].sum()))

    partes = sorted(PARTES.glob("pts_*.parquet"))
    if not partes:
        raise FileNotFoundError(
            "faltan las partes de puntos del DENUE; corre `make descargar-denue`"
        )
    por_version: dict[str, list[Path]] = {}
    for ruta in partes:
        version = "_".join(ruta.stem.split("_")[1:3])
        if versiones and version not in versiones:
            continue
        por_version.setdefault(version, []).append(ruta)

    salidas = []
    for version, rutas in sorted(por_version.items()):
        puntos = pd.concat([pd.read_parquet(r) for r in rutas], ignore_index=True)
        conteos = contar_en_radios(cen, puntos, radios)
        conteos["version"] = version
        salidas.append(conteos)
        log.info("anillos %s: %d puntos, %d filas", version, len(puntos), len(conteos))
    out = pd.concat(salidas, ignore_index=True)
    out.to_parquet(SALIDA, index=False, compression="zstd")
    log.info("anillos: %d filas, %d versiones", len(out), out["version"].nunique())
    return SALIDA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    construir()

"""DENUE histórico del INEGI: descarga por streaming y agregación inmediata.

El DENUE publica dos versiones por año (2016-01 … 2025-05, 18 versiones) repartidas en 23–25
archivos por sector SCIAN, ~13 GB en total. Como la máquina tiene ~16 GB libres, **el crudo no se
conserva**: cada zip se descarga a un temporal, se agrega (localidad, municipio y puntos de los
municipios del panel), se registra su sha256 en `data/raw/MANIFEST.csv` con nota explícita y se
borra. Con `--force` se vuelve a bajar y reprocesar.

El catálogo de URLs está en `config/denue_catalogo.json`; se construyó a partir de los 436 enlaces
reales de la página oficial de descarga masiva (que se carga por JavaScript). Cada URL se valida
con HEAD antes de descargarse: si el INEGI cambia el patrón, el módulo lo reporta en vez de
inventar rutas.

Salidas por (versión, sector) en `data/interim/denue/partes/`:
- `loc_<version>_<sector>.parquet`  — conteos por localidad y clase
- `mun_<version>_<sector>.parquet`  — conteos por municipio y clase
- `pts_<version>_<sector>.parquet`  — puntos (lat, lon, bloque, micro) restringidos a los
  municipios que alguna vez tuvieron sucursal del Banco del Bienestar (para los anillos)

`proyecto.limpieza.denue` consolida esas partes en las tablas finales.
"""

from __future__ import annotations

import json
import logging
import tempfile
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from proyecto.limpieza.denue_clasificacion import BLOQUES, clasificar
from proyecto.utils import http, manifest
from proyecto.utils.claves import combinar, es_valida
from proyecto.utils.io import CONFIG, INTERIM, parametros
from proyecto.utils.periodos import yyyymm_a_semestre

log = logging.getLogger(__name__)

FUENTE = "denue"
PARTES = INTERIM / FUENTE / "partes"
HILOS = 8  # la descarga desde el INEGI va a ~0.5 MB/s por conexión; 8 hilos sin saturar
RUTA_CATALOGO = CONFIG / "denue_catalogo.json"
NOTA = (
    "DENUE histórico; el zip se agrega y se borra (streaming, 13 GB de crudo contra 16 GB libres). "
    "Reproducible con `make descargar-denue FORCE=1`."
)
COLS = [
    "codigo_act",
    "per_ocu",
    "cve_ent",
    "cve_mun",
    "cve_loc",
    "latitud",
    "longitud",
    "fecha_alta",
]


def catalogo() -> list[dict]:
    with open(RUTA_CATALOGO, encoding="utf-8") as f:
        return json.load(f)["archivos"]


def _municipios_panel() -> set[str]:
    """Municipios que alguna vez tuvieron sucursal del Banco del Bienestar (para los puntos)."""
    ruta = INTERIM / "sucursales_bienestar.parquet"
    if not ruta.exists():
        return set()
    sb = pd.read_parquet(ruta, columns=["cve_mun", "suc_bienestar"])
    return set(sb.loc[sb["suc_bienestar"] > 0, "cve_mun"].unique())


def _leer_csv(ruta_zip: Path) -> pd.DataFrame:
    """Lee el CSV del zip y normaliza los encabezados a minúsculas.

    El INEGI publica algunos archivos con los encabezados en mayúsculas (sector 56 en 2022-11 y
    2024-05, entre otros); sin normalizar, `usecols` no empata ninguna columna y el archivo se
    lee vacío.
    """
    with zipfile.ZipFile(ruta_zip) as z:
        miembro = next(
            n for n in z.namelist() if n.lower().endswith(".csv") and "diccionario" not in n.lower()
        )
        with z.open(miembro) as f:
            d = pd.read_csv(
                f, dtype=str, encoding="latin-1", usecols=lambda c: c.strip().lower() in COLS
            )
    d.columns = [c.strip().lower() for c in d.columns]
    return d


def agregar_archivo(ruta_zip: Path, meta: dict, municipios_panel: set[str]) -> dict[str, int]:
    """Lee un zip del DENUE y escribe las tres partes agregadas. Devuelve conteos de control."""
    cfg = parametros()["denue"]
    d = _leer_csv(ruta_zip)
    faltantes = [c for c in COLS if c not in d.columns]
    if faltantes:
        raise ValueError(f"{ruta_zip.name}: faltan columnas {faltantes}")
    n_crudo = len(d)

    d["cve_mun"] = combinar(d["cve_ent"], d["cve_mun"])
    d = d[d["cve_mun"].map(es_valida)]
    d["cve_loc"] = d["cve_mun"] + d["cve_loc"].str.zfill(4)
    d["empleo_est"] = d["per_ocu"].map(cfg["per_ocu_punto_medio"]).astype("float32")
    # Micronegocio = el rango más pequeño de personas ocupadas ("0 a 5 personas"): proxy de
    # autoempleo y negocio de subsistencia, que es el margen donde Bruhn y Love (2014) hallan efecto.
    rango_micro = min(cfg["per_ocu_punto_medio"], key=cfg["per_ocu_punto_medio"].get)
    d["micro"] = d["per_ocu"].eq(rango_micro)

    marcas = clasificar(d["codigo_act"])
    d = pd.concat([d.reset_index(drop=True), marcas.reset_index(drop=True)], axis=1)
    d["version"] = meta["version"]
    d["semestre"] = yyyymm_a_semestre(meta["yyyymm"])

    filas = []
    for bloque in BLOQUES:
        sub = d[d[bloque]]
        if sub.empty:
            continue
        g = sub.assign(bloque=bloque, clase=sub[f"clase_{bloque}"])
        filas.append(
            g[
                [
                    "cve_loc",
                    "cve_mun",
                    "version",
                    "semestre",
                    "bloque",
                    "clase",
                    "micro",
                    "empleo_est",
                ]
            ]
        )
    if not filas:
        return {"crudo": n_crudo, "validos": len(d), "loc": 0, "mun": 0, "pts": 0}
    largo = pd.concat(filas, ignore_index=True)

    llaves = ["version", "semestre", "bloque", "clase"]
    por_loc = (
        largo.groupby(["cve_loc", "cve_mun", *llaves], observed=True)
        .agg(n_estab=("micro", "size"), n_micro=("micro", "sum"), empleo_est=("empleo_est", "sum"))
        .reset_index()
    )
    por_mun = (
        largo.groupby(["cve_mun", *llaves], observed=True)
        .agg(n_estab=("micro", "size"), n_micro=("micro", "sum"), empleo_est=("empleo_est", "sum"))
        .reset_index()
    )

    sufijo = f"{meta['version']}_{meta['sector']}"
    PARTES.mkdir(parents=True, exist_ok=True)
    por_loc.to_parquet(PARTES / f"loc_{sufijo}.parquet", index=False, compression="zstd")
    por_mun.to_parquet(PARTES / f"mun_{sufijo}.parquet", index=False, compression="zstd")

    # Puntos: solo municipios del panel y solo lo necesario para contar dentro de un radio.
    pts = d[d["cve_mun"].isin(municipios_panel)].copy()
    pts["lat"] = pd.to_numeric(pts["latitud"], errors="coerce").astype("float32")
    pts["lon"] = pd.to_numeric(pts["longitud"], errors="coerce").astype("float32")
    pts = pts[pts["lat"].notna() & pts["lon"].notna()]
    cols_pts = ["cve_loc", "cve_mun", "lat", "lon", "micro", "empleo_est", *BLOQUES]
    pts[cols_pts].to_parquet(PARTES / f"pts_{sufijo}.parquet", index=False, compression="zstd")

    return {
        "crudo": n_crudo,
        "validos": len(d),
        "loc": len(por_loc),
        "mun": len(por_mun),
        "pts": len(pts),
    }


def _partes_existen(meta: dict) -> bool:
    sufijo = f"{meta['version']}_{meta['sector']}"
    return all((PARTES / f"{p}_{sufijo}.parquet").exists() for p in ("loc", "mun", "pts"))


def _procesar_uno(meta: dict, municipios_panel: set[str], lock: threading.Lock) -> dict:
    """Descarga un zip a un temporal propio, lo agrega, lo registra y lo borra."""
    destino = Path(tempfile.gettempdir()) / f"denue_{meta['version']}_{meta['sector']}.zip"
    try:
        _bajar(meta["url"], destino, http.sesion())
        control = agregar_archivo(destino, meta, municipios_panel)
        with lock:  # el manifiesto es un CSV compartido: una escritura a la vez
            manifest.registrar_procesado(
                FUENTE, destino, meta["url"], f"data/raw/denue/{meta['archivo']}", notas=NOTA
            )
        return control
    finally:
        destino.unlink(missing_ok=True)


def descargar(force: bool = False, hilos: int = HILOS) -> None:
    municipios_panel = _municipios_panel()
    if not municipios_panel:
        log.warning("sin sucursales_bienestar.parquet: los puntos para anillos quedarán vacíos")
    archivos = catalogo()
    pendientes = [m for m in archivos if force or not _partes_existen(m)]
    log.info(
        "DENUE: %d archivos en el catálogo, %d por procesar con %d hilos",
        len(archivos),
        len(pendientes),
        hilos,
    )

    lock = threading.Lock()
    fallidos: list[str] = []
    hechos = 0
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        futuros = {pool.submit(_procesar_uno, m, municipios_panel, lock): m for m in pendientes}
        for fut in as_completed(futuros):
            meta = futuros[fut]
            hechos += 1
            try:
                control = fut.result()
                log.info(
                    "[%d/%d] %s %s: %d establecimientos, %d puntos del panel",
                    hechos,
                    len(pendientes),
                    meta["version"],
                    meta["sector"],
                    control["validos"],
                    control["pts"],
                )
            except Exception:
                log.exception("%s %s: falló", meta["version"], meta["sector"])
                fallidos.append(meta["archivo"])
    if fallidos:
        raise RuntimeError(f"DENUE: {len(fallidos)} archivos fallidos: {fallidos[:5]}")


def _bajar(url: str, destino: Path, s) -> None:
    """Descarga a un temporal validando primero que la URL exista (el catálogo no se inventa)."""
    cab = http.cabecera(url, s)
    total = int(cab.headers.get("Content-Length") or 0)
    with s.get(url, timeout=http.TIMEOUT, stream=True) as resp:
        resp.raise_for_status()
        escritos = 0
        with open(destino, "wb") as f:
            for trozo in resp.iter_content(chunk_size=1 << 20):
                f.write(trozo)
                escritos += len(trozo)
    if total and escritos != total:
        destino.unlink(missing_ok=True)
        raise http.ErrorTransitorio(f"descarga trunca: {escritos} de {total} bytes en {url}")

"""IMSS, datos abiertos: puestos de trabajo afiliados por municipio (fase 1), por streaming.

Cada archivo mensual (`asg-AAAA-MM-DD.csv`, separado por `|`, ~385 MB) trae los puestos afiliados
por delegación, municipio (catálogo IMSS), sector, tamaño del registro patronal, sexo, edad y
salario. Solo se bajan los **cierres de trimestre** 2019T1–2025T4 (28 archivos, ~11 GB de
tráfico), que coinciden con la G trimestral de la BDIF. Como el DENUE, el crudo no se conserva:
se descarga a un temporal, se agrega por municipio IMSS, se registra su sha256 en
`data/raw/MANIFEST.csv` y se borra.

Las fechas y el patrón de URL se descubrieron en las páginas `asg-<año>` del portal de datos
abiertos del IMSS; cada URL se valida con HEAD antes de bajarla.

Salida por fecha en `data/interim/imss/partes/asg_<fecha>.parquet`: `cve_entidad, cve_municipio`
(catálogo IMSS) y `tamano_patron` (S1–S7, o vacío) con `asegurados`, `ta` (puestos afiliados a un
empleo) y `masa_sal_ta` (masa salarial diaria). Se guarda el desglose por tamaño completo para no
tener que volver a bajar si cambia la definición de micro o pequeña empresa. Ojo: el diccionario
del IMSS escribe los tamaños en minúsculas (`s1`) y los archivos en mayúsculas (`S1`); aquí se
normalizan a mayúsculas. El cruce a la clave INEGI es una excepción controlada a la regla 6
(`utils/cruce_nombres.py`).
"""

from __future__ import annotations

import logging
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from proyecto.descarga.denue import _bajar
from proyecto.utils import http, manifest
from proyecto.utils.io import INTERIM, fuentes
from proyecto.utils.periodos import yyyymm_a_periodo

log = logging.getLogger(__name__)

FUENTE = "imss"
PARTES = INTERIM / FUENTE / "partes"
HILOS = 3
NOTA = (
    "IMSS, puestos afiliados (cierre de trimestre); el CSV se agrega por municipio IMSS y se "
    "borra (streaming, ~385 MB por archivo). Reproducible con `make descargar-imss FORCE=1`."
)
COLUMNAS = ["cve_entidad", "cve_municipio", "tamaño_patron", "asegurados", "ta", "masa_sal_ta"]


def catalogo() -> list[dict]:
    cfg = fuentes()[FUENTE]
    # YAML lee `2019-03-31` como fecha: se vuelve texto AAAA-MM-DD.
    return [
        {"fecha": f, "url": cfg["patron_url"].format(fecha=f), "archivo": f"asg-{f}.csv"}
        for f in map(str, cfg["fechas"])
    ]


def _codificacion(ruta: Path) -> str:
    """El IMSS publica la mayoría de los archivos en latin-1, pero algunos en UTF-8: se decide por
    cómo viene escrita la columna `tamaño_patron` en la cabecera."""
    with open(ruta, "rb") as f:
        cabecera = f.readline()
    return "utf-8-sig" if "tamaño_patron".encode() in cabecera else "latin-1"


def agregar_archivo(ruta: Path, fecha: str) -> pd.DataFrame:
    """Suma los puestos por municipio IMSS; separa los de micro y pequeños registros patronales."""
    partes = []
    for trozo in pd.read_csv(
        ruta,
        sep="|",
        usecols=COLUMNAS,
        dtype={"cve_entidad": "string", "cve_municipio": "string", "tamaño_patron": "string"},
        encoding=_codificacion(ruta),
        chunksize=2_000_000,
    ):
        trozo = trozo.assign(
            tamano_patron=trozo["tamaño_patron"].str.strip().str.upper().fillna("")
        )
        partes.append(
            trozo.groupby(["cve_entidad", "cve_municipio", "tamano_patron"], dropna=False)[
                ["asegurados", "ta", "masa_sal_ta"]
            ].sum()
        )
    agregado = pd.concat(partes).groupby(level=[0, 1, 2], dropna=False).sum().reset_index()
    agregado["fecha"] = fecha
    agregado["periodo"] = yyyymm_a_periodo(fecha[:4] + fecha[5:7])
    return agregado


def _procesar_uno(meta: dict, lock: threading.Lock) -> dict:
    destino = Path(tempfile.gettempdir()) / f"imss_{meta['archivo']}"
    try:
        _bajar(meta["url"], destino, http.sesion())
        agregado = agregar_archivo(destino, meta["fecha"])
        PARTES.mkdir(parents=True, exist_ok=True)
        agregado.to_parquet(PARTES / f"asg_{meta['fecha']}.parquet", index=False)
        with lock:
            manifest.registrar_procesado(
                FUENTE, destino, meta["url"], f"data/raw/imss/{meta['archivo']}", notas=NOTA
            )
        return {"municipios": len(agregado), "ta": int(agregado["ta"].sum())}
    finally:
        destino.unlink(missing_ok=True)


def descargar(force: bool = False, hilos: int = HILOS) -> None:
    archivos = catalogo()
    pendientes = [
        m for m in archivos if force or not (PARTES / f"asg_{m['fecha']}.parquet").exists()
    ]
    log.info(
        "IMSS: %d archivos, %d por procesar con %d hilos", len(archivos), len(pendientes), hilos
    )
    lock = threading.Lock()
    fallidos: list[str] = []
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        futuros = {pool.submit(_procesar_uno, m, lock): m for m in pendientes}
        for i, fut in enumerate(as_completed(futuros), start=1):
            meta = futuros[fut]
            try:
                control = fut.result()
                log.info(
                    "[%d/%d] %s: %d municipios IMSS, %d puestos afiliados",
                    i,
                    len(pendientes),
                    meta["fecha"],
                    control["municipios"],
                    control["ta"],
                )
            except Exception:
                log.exception("%s: falló", meta["fecha"])
                fallidos.append(meta["archivo"])
    if fallidos:
        raise RuntimeError(f"IMSS: {len(fallidos)} archivos fallidos: {fallidos}")

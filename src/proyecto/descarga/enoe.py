"""INEGI, ENOE / ENOE^N: microdatos trimestrales agregados por municipio, por streaming (fase 2).

Réplica más cercana a Bruhn y Love (2014), que usaron la ENE con identificador municipal: la tabla
SDEM de la ENOE trae `ent` y `mun`. Cada zip trimestral (25–45 MB) se baja a un temporal, se agrega
la tabla SDEM por municipio con el ponderador trimestral (`fac` hasta 2020T1, `fac_tri` después),
se registra su sha256 y se borra. 2020T2 (levantamiento telefónico ETOE) no se baja.

Universo (descriptor oficial, `enoe_325_fd_c_bas_amp.pdf`): `r_def = 00`, `c_res` 1 o 3 y edad
15–98. Sumas ponderadas por municipio-trimestre:

- `pob15`, `ocupados` (`clase2 = 1`);
- `pos_validos` (ocupados con `pos_ocu` 1–4), `negocio` (`pos_ocu` 2 empleadores o 3 cuenta propia);
- `informal` (ocupados con `tue2 = 5`, sector informal);
- `ing_validos` y `ing_log_suma` (ocupados con `ingocup > 0`).

Salida: `data/interim/enoe/partes/<periodo>.parquet`.
"""

from __future__ import annotations

import logging
import tempfile
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.descarga.denue import _bajar
from proyecto.utils import http, manifest
from proyecto.utils.io import INTERIM, fuentes, parametros
from proyecto.utils.periodos import descomponer, rango

log = logging.getLogger(__name__)

FUENTE = "enoe"
PARTES = INTERIM / FUENTE / "partes"
HILOS = 3
COLUMNAS = {
    "r_def",
    "c_res",
    "eda",
    "ent",
    "mun",
    "fac",
    "fac_tri",
    "clase2",
    "pos_ocu",
    "tue2",
    "ingocup",
}
NOTA = "ENOE, tabla SDEM agregada por municipio y borrada (streaming)."
# Desde 2025T3 las claves geográficas se llaman `cve_ent`, `cve_mun`, `cve_loc` (verificado el
# 2026-10-07 en ENOE_SDEMT325.csv); antes, `ent`, `mun`, `loc`.
ALIAS = {"cve_ent": "ent", "cve_mun": "mun"}


def _limpio(c: str) -> str:
    """Nombre de columna normalizado: sin BOM (2022T2 lo trae en `r_def`), minúsculas y alias."""
    c = c.replace("\ufeff", "").replace("ï»¿", "").strip().lower()
    return ALIAS.get(c, c)


def catalogo() -> list[dict]:
    cfg, f2 = fuentes()[FUENTE], parametros()["fase2"]["enoe"]
    excluir = set(f2["excluir"])
    salida = []
    for era in cfg["eras"]:
        for periodo in rango(era["desde"], era["hasta"]):
            if periodo in excluir or not (f2["inicio"] <= periodo <= f2["fin"]):
                continue
            anio, trimestre = descomponer(periodo)
            archivo = era["patron"].format(anio=anio, trimestre=trimestre)
            salida.append(
                {"periodo": periodo, "archivo": archivo, "url": cfg["url_base"] + archivo}
            )
    return salida


def agregar_zip(ruta: Path, periodo: str) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as z:
        nombre = next(n for n in z.namelist() if "sdem" in n.lower() and n.lower().endswith(".csv"))
        partes = []
        for d in pd.read_csv(
            z.open(nombre),
            usecols=lambda c: _limpio(c) in COLUMNAS,
            dtype=str,
            encoding="latin-1",
            chunksize=1_000_000,
        ):
            d.columns = [_limpio(c) for c in d.columns]
            num = {c: pd.to_numeric(d[c], errors="coerce") for c in d.columns}
            f = (num["fac_tri"] if "fac_tri" in num else num["fac"]).fillna(0)
            universo = (num["r_def"] == 0) & num["c_res"].isin([1, 3]) & num["eda"].between(15, 98)
            ocup = universo & (num["clase2"] == 1)
            pos = num["pos_ocu"]
            ing = num["ingocup"]
            ing_ok = ocup & (ing > 0)
            mun = d["mun"].str.strip()
            # Si el municipio ya viene con la clave de 5 dígitos, se usa tal cual.
            cve = mun.str.zfill(5).where(
                mun.str.len() >= 5, d["ent"].str.strip().str.zfill(2) + mun.str.zfill(3)
            )
            tabla = pd.DataFrame(
                {
                    "cve_mun": cve,
                    "pob15": f * universo,
                    "ocupados": f * ocup,
                    "pos_validos": f * (ocup & pos.between(1, 4)),
                    "negocio": f * (ocup & pos.isin([2, 3])),
                    "informal": f * (ocup & (num["tue2"] == 5)),
                    "ing_validos": f * ing_ok,
                    "ing_log_suma": (f * np.log(ing.where(ing_ok))).fillna(0),
                    "n_registros": universo.astype(int),
                }
            )
            partes.append(tabla.groupby("cve_mun").sum())
    out = pd.concat(partes).groupby(level=0).sum().reset_index()
    out["periodo"] = periodo
    return out


def _procesar_uno(meta: dict, lock: threading.Lock) -> dict:
    destino = Path(tempfile.gettempdir()) / f"enoe_{meta['archivo']}"
    try:
        _bajar(meta["url"], destino, http.sesion())
        if not zipfile.is_zipfile(destino):
            raise RuntimeError(f"{meta['archivo']} no es un zip (¿página de error del INEGI?)")
        agregado = agregar_zip(destino, meta["periodo"])
        PARTES.mkdir(parents=True, exist_ok=True)
        agregado.to_parquet(PARTES / f"{meta['periodo']}.parquet", index=False)
        with lock:
            manifest.registrar_procesado(
                FUENTE, destino, meta["url"], f"data/raw/{FUENTE}/{meta['archivo']}", notas=NOTA
            )
        return {"municipios": len(agregado), "registros": int(agregado["n_registros"].sum())}
    finally:
        destino.unlink(missing_ok=True)


def descargar(force: bool = False, hilos: int = HILOS) -> None:
    archivos = catalogo()
    pendientes = [m for m in archivos if force or not (PARTES / f"{m['periodo']}.parquet").exists()]
    log.info("ENOE: %d trimestres, %d por procesar", len(archivos), len(pendientes))
    lock = threading.Lock()
    fallidos: list[str] = []
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        futuros = {pool.submit(_procesar_uno, m, lock): m for m in pendientes}
        for i, fut in enumerate(as_completed(futuros), start=1):
            meta = futuros[fut]
            try:
                c = fut.result()
                log.info(
                    "[%d/%d] %s: %d municipios, %d personas en el universo",
                    i,
                    len(pendientes),
                    meta["periodo"],
                    c["municipios"],
                    c["registros"],
                )
            except Exception:
                log.exception("%s: falló", meta["periodo"])
                fallidos.append(meta["archivo"])
    if fallidos:
        raise RuntimeError(f"ENOE: {len(fallidos)} trimestres fallidos: {fallidos}")

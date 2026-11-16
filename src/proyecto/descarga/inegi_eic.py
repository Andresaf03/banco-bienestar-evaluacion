"""INEGI: Encuesta Intercensal 2015, Censo 2020 (cuestionario ampliado) y EIC 2025, por streaming.

Fase 2 (preregistro en `docs/decisiones.md`, 2026-10-07). Los microdatos se publican por entidad:
un zip con las tablas de viviendas y personas (EIC 2015: 7–81 MB; Censo 2020: 2–63 MB; EIC 2025:
3–79 MB). Como el DENUE y el IMSS, el crudo **no se conserva**: cada zip se baja a un temporal, se
agrega por municipio con el factor de expansión, se registra su sha256 en `data/raw/MANIFEST.csv`
y se borra (~2.5 GB de tráfico contra ~12 GB libres en la máquina).

Salida por archivo en `data/interim/inegi_eic/partes/<anio>_<clave>.parquet`: **sumas ponderadas**
por municipio (no proporciones), para que la limpieza pueda colapsar municipios nuevos sumando y
calcular las proporciones al final. Los códigos de cada año salen de `parametros.fase2.eic`
(verificados en los descriptores de 2015 y 2025 y en la muestra del Censo 2020).

Los URL y las claves de entidad se descubrieron en las pestañas "Microdatos" del INEGI
(`fuentes.inegi_eic`); cada URL se valida con HEAD antes de bajarla.
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

log = logging.getLogger(__name__)

FUENTE = "inegi_eic"
PARTES = INTERIM / FUENTE / "partes"
HILOS = 3
TROZO = 1_000_000
NOTA = (
    "Microdatos por entidad agregados por municipio con FACTOR y borrados (streaming). "
    "Reproducible con `make descargar-fase2 FORCE=1`."
)
# Columnas que se leen de cada tabla (nombres en mayúsculas, sin BOM). Las de posición en el trabajo
# cambian de nombre en 2015 (`SITUACION_TRAB`) y la clave municipal en 2025 (`CVE_ENT`, `CVE_MUN`).
PERSONAS = {
    "ENT",
    "MUN",
    "CVE_ENT",
    "CVE_MUN",
    "FACTOR",
    "EDAD",
    "CONACT",
    "SITTRA",
    "SITUACION_TRAB",
    "INGTRMEN",
    "MUN_TRAB",
    "ENT_PAIS_TRAB",
}
VIVIENDAS = {
    "ENT",
    "MUN",
    "CVE_ENT",
    "CVE_MUN",
    "FACTOR",
    "INGR_AYUGOB",
    "INGR_PEROTROPAIS",
    "CELULAR",
    "INTERNET",
}


def catalogo() -> list[dict]:
    """`(anio, clave, url, archivo)` de los 96 zips: 32 entidades × 3 cortes."""
    salida = []
    for corte in fuentes()[FUENTE]["cortes"]:
        for clave in corte["claves"]:
            url = corte["patron_url"].format(clave=clave)
            salida.append(
                {
                    "anio": int(corte["anio"]),
                    "clave": clave,
                    "url": url,
                    "archivo": url.rsplit("/", 1)[-1],
                }
            )
    return salida


def _miembro(z: zipfile.ZipFile, tabla: str) -> str:
    """Nombre del CSV de personas o viviendas dentro del zip (mayúsculas y prefijos varían)."""
    candidatos = [n for n in z.namelist() if n.lower().endswith(".csv") and tabla in n.lower()]
    if len(candidatos) != 1:
        raise ValueError(f"se esperaba un CSV de {tabla} y hay {candidatos}")
    return candidatos[0]


def _leer(z: zipfile.ZipFile, tabla: str, columnas: set[str]):
    """Lee por trozos las columnas pedidas, con nombres normalizados (mayúsculas, sin BOM)."""
    nombre = _miembro(z, tabla)

    def limpio(c: str) -> str:
        # BOM de UTF-8 como carácter (U+FEFF) o leído como latin-1 ("ï»¿").
        return c.replace("﻿", "").replace("ï»¿", "").strip().upper()

    def usar(c: str) -> bool:
        return limpio(c) in columnas

    for trozo in pd.read_csv(
        z.open(nombre), usecols=usar, dtype=str, encoding="latin-1", chunksize=TROZO
    ):
        trozo.columns = [limpio(c) for c in trozo]
        yield trozo


def _clave_mun(d: pd.DataFrame) -> pd.Series:
    ent = d["CVE_ENT"] if "CVE_ENT" in d else d["ENT"]
    mun = d["CVE_MUN"] if "CVE_MUN" in d else d["MUN"]
    return ent.str.strip().str.zfill(2) + mun.str.strip().str.zfill(3)


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def agregar_personas(z: zipfile.ZipFile, anio: int, cfg: dict) -> pd.DataFrame:
    """Sumas ponderadas por municipio: población, 12+, ocupados, posición, ingreso y movilidad."""
    ocupado = set(cfg["ocupado"][anio])
    partes = []
    for d in _leer(z, "persona", PERSONAS):
        f = _num(d["FACTOR"]).fillna(0)
        edad = _num(d["EDAD"])
        doce = edad.between(cfg["edad_minima"], 130)
        ocup = doce & _num(d["CONACT"]).isin(ocupado)
        pos = _num(d["SITTRA"] if "SITTRA" in d else d["SITUACION_TRAB"])
        pos_ok = ocup & pos.between(1, 6)
        ing = _num(d["INGTRMEN"])
        ing_ok = ocup & ing.between(1, 999_997)
        ent_t = _num(d["ENT_PAIS_TRAB"])
        mun_t = _num(d["MUN_TRAB"])
        ent_p = _num(d["CVE_ENT"] if "CVE_ENT" in d else d["ENT"])
        mun_p = _num(d["CVE_MUN"] if "CVE_MUN" in d else d["MUN"])
        # Lugar de trabajo conocido: entidad 1–32 con municipio válido, o un país (100–536).
        en_mexico = ent_t.between(1, 32) & mun_t.between(1, 570)
        en_otro_pais = ent_t.between(100, 536)
        lugar_ok = ocup & (en_mexico | en_otro_pais)
        otro_mun = lugar_ok & (en_otro_pais | (ent_t != ent_p) | (mun_t != mun_p))
        logi = np.log(ing.where(ing_ok))
        tabla = pd.DataFrame(
            {
                "cve_mun": _clave_mun(d),
                "pob": f,
                "pob12": f * doce,
                "ocupados": f * ocup,
                "pos_validos": f * pos_ok,
                "cuenta_propia": f * (pos_ok & (pos == 5)),
                "empleadores": f * (pos_ok & (pos == 4)),
                "ing_validos": f * ing_ok,
                "ing_log_suma": (f * logi).fillna(0),
                "lugar_validos": f * lugar_ok,
                "otro_mun": f * otro_mun,
                "n_personas": 1,
            }
        )
        partes.append(tabla.groupby("cve_mun").sum())
    return pd.concat(partes).groupby(level=0).sum()


def agregar_viviendas(z: zipfile.ZipFile, anio: int, cfg: dict) -> pd.DataFrame:
    """Sumas ponderadas por municipio de viviendas con programas, remesas, internet y celular."""
    partes = []
    for d in _leer(z, "vivienda", VIVIENDAS):
        f = _num(d["FACTOR"]).fillna(0)
        prog, rem = _num(d["INGR_AYUGOB"]), _num(d["INGR_PEROTROPAIS"])
        cel, net = _num(d["CELULAR"]), _num(d["INTERNET"])
        si_c, no_c = cfg["si_celular"][anio], cfg["no_celular"][anio]
        si_i, no_i = cfg["si_internet"][anio], cfg["no_internet"][anio]
        tabla = pd.DataFrame(
            {
                "cve_mun": _clave_mun(d),
                "viv_prog_validas": f * prog.isin([5, 6]),
                "viv_programas": f * (prog == 5),
                "viv_rem_validas": f * rem.isin([1, 2]),
                "viv_remesas": f * (rem == 1),
                "viv_cel_validas": f * cel.isin([si_c, no_c]),
                "viv_celular": f * (cel == si_c),
                "viv_net_validas": f * net.isin([si_i, no_i]),
                "viv_internet": f * (net == si_i),
                "n_viviendas": 1,
            }
        )
        partes.append(tabla.groupby("cve_mun").sum())
    return pd.concat(partes).groupby(level=0).sum()


def agregar_zip(ruta: Path, anio: int) -> pd.DataFrame:
    cfg = parametros()["fase2"]["eic"]
    with zipfile.ZipFile(ruta) as z:
        personas = agregar_personas(z, anio, cfg)
        viviendas = agregar_viviendas(z, anio, cfg)
    out = personas.join(viviendas, how="outer").reset_index()
    out["anio"] = anio
    return out


def _procesar_uno(meta: dict, lock: threading.Lock) -> dict:
    destino = Path(tempfile.gettempdir()) / f"inegi_eic_{meta['archivo']}"
    try:
        _bajar(meta["url"], destino, http.sesion())
        agregado = agregar_zip(destino, meta["anio"])
        PARTES.mkdir(parents=True, exist_ok=True)
        agregado.to_parquet(PARTES / f"{meta['anio']}_{meta['clave']}.parquet", index=False)
        with lock:
            manifest.registrar_procesado(
                FUENTE,
                destino,
                meta["url"],
                f"data/raw/{FUENTE}/{meta['anio']}/{meta['archivo']}",
                notas=NOTA,
            )
        return {"municipios": len(agregado), "personas": int(agregado["n_personas"].sum())}
    finally:
        destino.unlink(missing_ok=True)


def descargar(force: bool = False, hilos: int = HILOS) -> None:
    archivos = catalogo()
    pendientes = [
        m for m in archivos if force or not (PARTES / f"{m['anio']}_{m['clave']}.parquet").exists()
    ]
    log.info(
        "EIC/Censo: %d archivos, %d por procesar con %d hilos",
        len(archivos),
        len(pendientes),
        hilos,
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
                    "[%d/%d] %d %s: %d municipios, %d registros de personas",
                    i,
                    len(pendientes),
                    meta["anio"],
                    meta["clave"],
                    control["municipios"],
                    control["personas"],
                )
            except Exception:
                log.exception("%d %s: falló", meta["anio"], meta["clave"])
                fallidos.append(meta["archivo"])
    if fallidos:
        raise RuntimeError(f"EIC/Censo: {len(fallidos)} archivos fallidos: {fallidos}")

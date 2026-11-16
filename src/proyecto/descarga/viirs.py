"""Luz nocturna VIIRS anual (VNL V2 de EOG) redistribuida en Zenodo: fase 2.

El producto original de la Colorado School of Mines exige cuenta (`eogdata.mines.edu` redirige a
OpenID; verificado el 2026-10-07). OpenGeoHub lo redistribuye sin registro y con licencia CC-BY en
Zenodo (registro 17294744): un GeoTIFF global por año (500 m, COG Int16, 59–84 MB). Se bajan los
años de `parametros.fase2.viirs.anios` y se **conservan** en `data/raw/viirs/` (~650 MB): el recorte
por localidad se puede rehacer sin volver a bajar.

Zenodo responde 429 cuando se le piden muchos archivos seguidos. No se evade: se baja uno por uno
con una pausa entre archivos y, ante un 429, se espera y se reintenta un número acotado de veces.
"""

from __future__ import annotations

import logging
import time

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes, parametros

log = logging.getLogger(__name__)

FUENTE = "viirs"
DESTINO = RAW / FUENTE
PAUSA_S = 20
ESPERA_429_S = 120
INTENTOS_429 = 4


def catalogo() -> list[dict]:
    cfg = fuentes()[FUENTE]
    return [
        {"anio": a, "url": cfg["patron_url"].format(anio=a)}
        for a in parametros()["fase2"]["viirs"]["anios"]
    ]


def descargar(force: bool = False) -> None:
    s = http.sesion()
    for i, meta in enumerate(catalogo()):
        destino = DESTINO / meta["url"].rsplit("/", 1)[-1]
        for intento in range(1, INTENTOS_429 + 1):
            try:
                http.descargar(
                    meta["url"],
                    destino,
                    FUENTE,
                    notas=f"VNL V2 anual {meta['anio']} (Zenodo 17294744, CC-BY)",
                    force=force,
                    s=s,
                )
                break
            except http.Bloqueado as exc:
                if intento == INTENTOS_429:
                    raise
                log.warning("%s; se espera %d s (intento %d)", exc, ESPERA_429_S, intento)
                time.sleep(ESPERA_429_S)
        if i < len(catalogo()) - 1:
            time.sleep(PAUSA_S)

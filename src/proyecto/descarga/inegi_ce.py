"""INEGI, Censos Económicos: datos abiertos por entidad federativa (fase 1).

La pestaña "Datos abiertos" del CE 2024 publica, en una misma carpeta, los resultados definitivos
del CE 2024 y un comparativo histórico (CE 2019, 2014, 2009 y 2004) homologado a SCIAN 2023. Cada
archivo es un zip por entidad (1–3 MB) con desglose municipal y su diccionario de datos. Con cinco
cortes homogéneos, el diseño de diferencias largas tiene varios periodos previos para la
pre-prueba (2004→2009→2014→2019) y un corte posterior (2024).

El patrón de URL y las claves de entidad se descubrieron en la página del INEGI
(`fuentes.inegi_ce.url_pagina`); un archivo que no exista falla con el error HTTP en vez de
suponerse.
"""

from __future__ import annotations

import logging

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "inegi_ce"
DESTINO = RAW / FUENTE
log = logging.getLogger(__name__)


def catalogo() -> list[tuple[str, int, str]]:
    """`(entidad, anio, url)` de cada archivo a descargar."""
    cfg = fuentes()[FUENTE]
    return [
        (e, a, cfg["patron_url"].format(entidad=e, anio=a))
        for a in cfg["anios"]
        for e in cfg["entidades"]
    ]


def descargar(force: bool = False) -> None:
    s = http.sesion()
    archivos = catalogo()
    for i, (entidad, anio, url) in enumerate(archivos, start=1):
        destino = DESTINO / str(anio) / url.rsplit("/", 1)[-1]
        http.descargar(url, destino, FUENTE, notas=f"CE {anio}, {entidad}", force=force, s=s)
        if i % 33 == 0:
            log.info("CE: %d de %d archivos", i, len(archivos))

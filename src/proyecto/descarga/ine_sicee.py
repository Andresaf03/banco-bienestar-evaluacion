"""INE, SICEE: diputaciones federales de mayoría relativa por casilla (fase 3).

Un zip por proceso electoral (2015, 2018, 2021 y 2024, 31–44 MB cada uno) con los cómputos
distritales por casilla. Se conservan en `data/raw/ine_sicee/`. Rutas descubiertas en
https://sicee.ine.mx/downloadzip (ámbito Federal, 2026-10-11); el servidor responde 200 sin
bloqueo a clientes que no son navegador.
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "ine_sicee"


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    for anio in cfg["anios"]:
        url = cfg["patron_url"].format(anio=anio)
        destino = RAW / FUENTE / url.rsplit("/", 1)[-1]
        http.descargar(
            url,
            destino,
            FUENTE,
            notas=f"diputaciones federales MR {anio}, por casilla",
            force=force,
        )

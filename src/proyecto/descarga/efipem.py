"""INEGI, EFIPEM municipal (datos abiertos, 1989–2025): fase 2.

Un solo zip (~96 MB) con un CSV por año en formato largo (`ANIO, CVEGEO, TEMA, CATEGORIA,
DESCRIPCION_CATEGORIA, VALOR, ESTATUS`). Se conserva en `data/raw/efipem/`. URL descubierta en la
pestaña "Datos abiertos" de https://www.inegi.org.mx/programas/finanzas/ (2026-10-07).
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "efipem"


def descargar(force: bool = False) -> None:
    url = fuentes()[FUENTE]["url_archivo"]
    destino = RAW / FUENTE / url.rsplit("/", 1)[-1]
    http.descargar(url, destino, FUENTE, notas="EFIPEM municipal anual 1989–2025", force=force)

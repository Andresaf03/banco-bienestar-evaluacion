"""INEGI, ENIGH nueva serie 2016–2024: conjunto de datos en CSV (fase 4, C2, D y B3).

Un zip por edición (41–103 MB, ~371 MB en total) con las tablas de hogares, viviendas, gastos,
ingresos y el concentrado. Rutas tomadas de la pestaña "Datos abiertos" de cada edición
(2026-10-14); el servidor responde 200 a clientes que no son navegador. Se conservan en
`data/raw/enigh/`.
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "enigh"


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    for anio, ruta in cfg["archivos"].items():
        url = cfg["url_base"] + ruta
        destino = RAW / FUENTE / str(anio) / ruta.rsplit("/", 1)[-1]
        http.descargar(
            url,
            destino,
            FUENTE,
            notas=f"ENIGH {anio}, nueva serie, datos abiertos (CSV)",
            force=force,
        )

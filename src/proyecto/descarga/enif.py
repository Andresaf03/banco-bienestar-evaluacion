"""INEGI/CNBV, Encuesta Nacional de Inclusión Financiera: microdatos 2018, 2021 y 2024 (fase 1).

Sirve para el contraste a nivel personas que plantea la propuesta: tenencia de cuenta, cuenta en el
Banco del Bienestar y distancia a sucursal. No es representativa por municipio, así que se usa
como descriptivo (por región y tamaño de localidad), no en la estimación causal. Los enlaces se
descubrieron en la pestaña "Microdatos" de cada edición.
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "enif"
DESTINO = RAW / FUENTE


def descargar(force: bool = False) -> None:
    s = http.sesion()
    for archivo in fuentes()[FUENTE]["archivos"]:
        url = archivo["url"]
        destino = DESTINO / str(archivo["anio"]) / url.rsplit("/", 1)[-1]
        http.descargar(url, destino, FUENTE, notas=f"ENIF {archivo['anio']}", force=force, s=s)

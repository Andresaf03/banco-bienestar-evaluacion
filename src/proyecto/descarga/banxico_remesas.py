"""Banco de México, SIE: ingresos por remesas por municipio (cuadro CE166), trimestral (fase 1).

El cuadro CE166 ("Ingresos por Remesas — Distribución por Municipio") no tiene archivo fijo: se
exporta desde la interfaz del SIE marcando las series. Aquí se reproduce esa exportación: se lee la
página del cuadro, se toman las claves de serie de sus casillas (`series`) y se envía el mismo
formulario que envía el botón "Exportar series en formato CSV". La API del SIE requiere un token
de registro, así que no se usa.

Las series traen solo el **nombre** del municipio; el cruce con la clave INEGI es una excepción
controlada a la regla 6 (ver `utils/cruce_nombres.py` y `docs/decisiones.md`).
"""

from __future__ import annotations

import logging
import re

from proyecto.utils import http, manifest
from proyecto.utils.io import RAW, fuentes

FUENTE = "banxico_remesas"
DESTINO = RAW / FUENTE
log = logging.getLogger(__name__)


def series_del_cuadro(s, url_cuadro: str) -> list[str]:
    """Claves de serie (`SE…`) de las casillas del cuadro, en el orden de la página."""
    html = http.obtener(url_cuadro, s=s).text
    claves = re.findall(r'name="series"[^>]*value="(SE\d+)"', html)
    claves += re.findall(r'value="(SE\d+)"[^>]*name="series"', html)
    vistas: set[str] = set()
    return [c for c in claves if not (c in vistas or vistas.add(c))]


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    destino = DESTINO / cfg["archivo"]
    if not force and manifest.esta_vigente(destino):
        log.info("ya vigente, se salta: %s", destino.name)
        return
    s = http.sesion()
    series = series_del_cuadro(s, cfg["url_cuadro"])
    if len(series) < cfg["series_minimas"]:
        raise RuntimeError(
            f"el cuadro trajo {len(series)} series; se esperaban al menos {cfg['series_minimas']}"
        )
    formulario = [
        ("idCuadro", cfg["id_cuadro"]),
        ("sector", "1"),
        ("version", "3"),
        ("locale", "es"),
        ("anoInicial", str(cfg["anio_inicial"])),
        ("anoFinal", str(cfg["anio_final"])),
        ("tipoInformacion", "4,1"),
        ("metadatosWeb", "true"),
        ("formatoHorizontal", "false"),
        ("formatoCSV.x", "10"),
        ("formatoCSV.y", "10"),
        *[("series", c) for c in series],
    ]
    resp = s.post(cfg["url_exportar"], data=formulario, timeout=(20, 300))
    resp.raise_for_status()
    if "text/html" in resp.headers.get("Content-Type", "") and b"<html" in resp.content[:500]:
        raise RuntimeError(
            "el SIE devolvió HTML en vez del CSV: revisa el formulario de exportación"
        )
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(resp.content)
    manifest.registrar(
        FUENTE,
        destino,
        cfg["url_exportar"],
        notas=f"exportación CSV del cuadro {cfg['id_cuadro']}, {len(series)} series, "
        f"{cfg['anio_inicial']}–{cfg['anio_final']}",
    )
    log.info("remesas: %d series, %d bytes", len(series), len(resp.content))

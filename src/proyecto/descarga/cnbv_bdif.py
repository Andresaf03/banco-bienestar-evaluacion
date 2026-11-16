"""CNBV, Bases de Datos de Inclusión Financiera (BDIF).

La página oficial en gob.mx enlaza directamente a un archivo Excel por trimestre en
`https://www.cnbv.gob.mx/Inclusión/BasesDeDatos/Base_de_Datos_de_Inclusion_Financiera_YYYYMM.*`
(2009-12 en adelante; extensiones .xls/.xlsx/.xlsm según el año) y a algunos reportes
trimestrales en PDF. Los diccionarios y notas metodológicas van dentro de cada Excel
(hojas "Definición", "Ficha técnica" e "Indicadores IF"), no como archivos aparte.

Se descargan todos los trimestres desde `config/parametros.yaml: periodo.robustez_inicio`
(2016Q1) hasta el último publicado.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from urllib.parse import unquote, urljoin

from bs4 import BeautifulSoup

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes, parametros
from proyecto.utils.periodos import periodo_a_yyyymm

log = logging.getLogger(__name__)

FUENTE = "cnbv_bdif"
DESTINO = RAW / FUENTE
_RE_BASE = re.compile(r"^Base_de_Datos_de_Inclusion_Financiera_(\d{6})\.(xlsx|xlsm|xls)$", re.I)
_RE_PDF = re.compile(r"^(ReporteTrimestralBDIF|Mapas_Infraestructura)_(\d{6})\.pdf$", re.I)


def enlaces_en_pagina(s=None) -> tuple[dict[str, str], dict[str, str]]:
    """Devuelve (bases, pdfs): diccionarios `nombre_archivo -> url` descubiertos en la página."""
    cfg = fuentes()[FUENTE]
    resp = http.obtener(cfg["url_pagina"], s)
    sopa = BeautifulSoup(resp.text, "html.parser")
    bases: dict[str, str] = {}
    pdfs: dict[str, str] = {}
    for a in sopa.find_all("a", href=True):
        url = urljoin(cfg["url_pagina"], a["href"])
        # Solo el nombre base: `unquote` podría reintroducir "/" (%2F) y salir de DESTINO.
        nombre = Path(unquote(url.rsplit("/", 1)[-1])).name
        if _RE_BASE.search(nombre):
            bases[nombre] = url
        elif _RE_PDF.search(nombre):
            pdfs[nombre] = url
    return bases, pdfs


def descargar(force: bool = False) -> None:
    s = http.sesion()
    bases, pdfs = enlaces_en_pagina(s)
    desde = periodo_a_yyyymm(parametros()["periodo"]["robustez_inicio"])
    seleccion = {n: u for n, u in bases.items() if _RE_BASE.search(n).group(1) >= desde}
    log.info("BDIF: %d bases en la página, %d desde %s", len(bases), len(seleccion), desde)
    for nombre, url in sorted(seleccion.items()):
        http.descargar(url, DESTINO / nombre, FUENTE, force=force, s=s)
    for nombre, url in sorted(pdfs.items()):
        http.descargar(
            url,
            DESTINO / "reportes" / nombre,
            FUENTE,
            notas="reporte trimestral en PDF enlazado desde la página oficial",
            force=force,
            s=s,
        )

"""CNBV, Portafolio de Información: información operativa de banca de desarrollo por institución.

https://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/ (lista SharePoint) publica
`BD_Operativa_YYYYMM.xls(x)`. Los archivos mensuales de 2016-01 a 2021-12 traen una hoja plana
`Hoja1` con una fila por institución × localidad (clave INEGI de 12 dígitos) × producto
(sucursales, cajeros, TPV, ...) y valor. Permite separar **Banjército** de **Banco del Bienestar**
a nivel municipal, cosa que la BDIF no permite. El archivo más reciente (2026) es un modelo de
datos Power Pivot (`xl/model/item.data`) sin hoja plana: se descarga para documentar, pero no se
puede leer con herramientas abiertas.
"""

from __future__ import annotations

import html
import logging
import re
from pathlib import Path
from urllib.parse import unquote, urljoin

from bs4 import BeautifulSoup

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

log = logging.getLogger(__name__)

FUENTE = "cnbv_portafolio"
DESTINO = RAW / FUENTE
_RE = re.compile(r"^BD_Operativa_(\d{6})\.(xlsx|xlsm|xls)$", re.I)


_RE_PAGINA = re.compile(
    r"Paged=TRUE.*?p(?:_|%5F|%255F)Modified=([^&\"']+).*?p(?:_|%5F|%255F)ID=(\d+).*?PageFirstRow=(\d+).*?View=(\{[0-9A-Fa-f-]+\}|%7B[0-9A-Fa-f-]+%7D)",
    re.I,
)
MAX_PAGINAS = 20


def _enlaces_de(texto: str, base: str) -> dict[str, str]:
    sopa = BeautifulSoup(texto, "html.parser")
    out: dict[str, str] = {}
    for a in sopa.find_all("a", href=True):
        url = urljoin(base, a["href"])
        nombre = Path(unquote(url.rsplit("/", 1)[-1])).name
        if _RE.match(nombre):
            out[nombre] = url
    return out


def _siguiente_pagina(texto: str, base: str) -> str | None:
    """La lista de SharePoint pagina (~2,100 elementos): reconstruye la URL de la página siguiente."""
    m = _RE_PAGINA.search(html.unescape(texto))
    if not m:
        return None
    modificado, p_id, primera_fila, vista = m.groups()
    vista = unquote(vista)
    return (
        f"{base}?Paged=TRUE&p_SortBehavior=0&p_Modified={modificado}&p_ID={p_id}"
        f"&PageFirstRow={primera_fila}&View={vista}"
    )


def enlaces(s=None) -> dict[str, str]:
    """`nombre_archivo -> url` de todos los BD_Operativa, recorriendo las páginas de la lista."""
    cfg = fuentes()[FUENTE]
    base = cfg["url_pagina"]
    url: str | None = base
    vistas: set[str] = set()
    out: dict[str, str] = {}
    while url and url not in vistas and len(vistas) < MAX_PAGINAS:
        vistas.add(url)
        resp = http.obtener(url, s)
        nuevos = _enlaces_de(resp.text, base)
        if not (set(nuevos) - set(out)) and url != base:
            break  # página repetida (SharePoint enlaza a sí misma en la última)
        out.update(nuevos)
        url = _siguiente_pagina(resp.text, base)
    log.info("Portafolio: %d páginas recorridas", len(vistas))
    return out


def descargar(force: bool = False) -> None:
    s = http.sesion()
    archivos = enlaces(s)
    log.info("Portafolio: %d archivos BD_Operativa en la lista", len(archivos))
    for nombre, url in sorted(archivos.items()):
        http.descargar(
            url,
            DESTINO / nombre,
            FUENTE,
            notas="información operativa de banca de desarrollo por institución y localidad (mensual)",
            force=force,
            s=s,
        )

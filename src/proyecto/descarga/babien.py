"""Banco del Bienestar, Directorio de Ubicaciones de Sucursales (datos.gob.mx).

El recurso vive en `repodatos.atdt.gob.mx`, que responde 403 a clientes que no son navegador
(igual que la API CKAN de datos.gob.mx). No se fuerza: el CSV se descarga a mano con un
navegador y se deja en `data/manual/babien/`. Este módulo intenta la descarga automática por
si el bloqueo desaparece y, si falla, registra la copia manual.
"""

from __future__ import annotations

from proyecto.descarga.manual import intentar_automatico_o_manual
from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "babien"
NOMBRE = "sucursalesbabien_1ertrim2026.csv"


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    url = cfg["url_recurso"]
    intentar_automatico_o_manual(
        FUENTE,
        NOMBRE,
        url,
        notas_manual="repodatos.atdt.gob.mx devuelve 403 a requests; recurso CC BY 4.0",
        automatico=lambda: http.descargar(
            url, RAW / FUENTE / NOMBRE, FUENTE, force=force, intentos=1, timeout=http.TIMEOUT_CORTO
        ),
    )

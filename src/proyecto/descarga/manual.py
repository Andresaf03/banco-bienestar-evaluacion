"""Apoyo para fuentes que requieren descarga manual.

Cuando un servidor bloquea clientes que no son navegador (403 de Akamai en datos.gob.mx y
repodatos.atdt.gob.mx) o no responde, el archivo se baja a mano siguiendo
`docs/descarga_manual.md` y se deja en `data/manual/<fuente>/`. Estas funciones verifican que
esté ahí, lo registran en el manifiesto (con la URL oficial y una nota) y devuelven la ruta.
"""

from __future__ import annotations

import logging
from pathlib import Path

from proyecto.utils import manifest
from proyecto.utils.io import MANUAL

log = logging.getLogger(__name__)


class FaltaArchivoManual(FileNotFoundError):
    pass


def registrar_manual(fuente: str, nombre: str, url: str, notas: str) -> Path:
    """Registra `data/manual/<fuente>/<nombre>` en el manifiesto. Lanza si no existe."""
    ruta = MANUAL / fuente / nombre
    if not ruta.exists():
        raise FaltaArchivoManual(
            f"Falta {ruta.relative_to(MANUAL.parent.parent)}. "
            f"Descárgalo a mano desde {url} (ver docs/descarga_manual.md)."
        )
    if not manifest.esta_vigente(ruta):
        manifest.registrar(fuente, ruta, url, notas=f"descarga manual desde navegador; {notas}")
    return ruta


def intentar_automatico_o_manual(
    fuente: str,
    nombre: str,
    url: str,
    notas_manual: str,
    automatico,
) -> Path:
    """Ejecuta `automatico()`; si falla por bloqueo o red, cae a la copia manual.

    Si la copia manual ya existe y su hash está vigente en el manifiesto, **no** se intenta la
    descarga automática (idempotencia; evita esperar timeouts de servidores caídos).
    """
    from requests import ConnectionError as ErrorConexion
    from requests import Timeout

    from proyecto.utils.http import Bloqueado

    ruta_manual = MANUAL / fuente / nombre
    if manifest.esta_vigente(ruta_manual):
        log.info("%s: copia manual vigente, se salta la descarga automática: %s", fuente, nombre)
        return ruta_manual
    try:
        return automatico()
    except (Bloqueado, ErrorConexion, Timeout, OSError) as exc:
        log.warning("%s: descarga automática fallida (%s); usando copia manual", fuente, exc)
        return registrar_manual(fuente, nombre, url, notas_manual)

"""Cliente HTTP para descargas: user-agent identificable, reintentos con espera y timeouts.

Reglas:
- No se evaden protecciones. Un 403/401/429 persistente se reporta como `Bloqueado` y el módulo
  de la fuente debe caer a la ruta manual (`data/manual/<fuente>/`).
- Las descargas son idempotentes: si el archivo existe y su hash coincide con el manifiesto,
  se salta salvo `force=True`.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import requests
import truststore
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from tqdm import tqdm

from proyecto.utils import manifest

log = logging.getLogger(__name__)

# Identificable (proyecto + contacto). El correo de contacto se lee de PROYECTO_CONTACTO para no
# versionarlo; sin la variable, el UA identifica solo al proyecto. El WAF de cnbv.gob.mx rechaza
# cadenas con "python-requests", así que no se incluye ese token.
_CONTACTO = os.environ.get("PROYECTO_CONTACTO", "").strip()
USER_AGENT = "proyecto-ITAM-PPII/0.1 (trabajo académico{})".format(
    f"; +mailto:{_CONTACTO}" if _CONTACTO else ""
)
TIMEOUT = (15, 120)  # (conexión, lectura) en segundos
TIMEOUT_CORTO = (5, 60)  # para fuentes con copia manual: no esperar a servidores caídos
INTENTOS = 4
CODIGOS_BLOQUEO = {401, 403, 429}


class Bloqueado(RuntimeError):
    """El servidor rechazó la petición (403/401/429 o similar). No se reintenta a la fuerza."""


class ErrorTransitorio(RuntimeError):
    """Error de red o 5xx: se reintenta con espera exponencial."""


# Usa el almacén de certificados del sistema (macOS Keychain) en vez del paquete certifi:
# www.cnbv.gob.mx no envía la cadena intermedia y certifi no la trae. Sigue verificando TLS.
truststore.inject_into_ssl()


def sesion() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})
    return s


def _clasificar(resp: requests.Response) -> None:
    if resp.status_code in CODIGOS_BLOQUEO:
        raise Bloqueado(f"{resp.status_code} en {resp.url}")
    if resp.status_code >= 500:
        raise ErrorTransitorio(f"{resp.status_code} en {resp.url}")
    resp.raise_for_status()


def _politica(intentos: int):
    return retry(
        retry=retry_if_exception_type(
            (ErrorTransitorio, requests.ConnectionError, requests.Timeout)
        ),
        stop=stop_after_attempt(intentos),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        reraise=True,
    )


_reintentos = _politica(INTENTOS)


@_reintentos
def obtener(url: str, s: requests.Session | None = None, **kw) -> requests.Response:
    """GET con reintentos. Lanza `Bloqueado` en 401/403/429."""
    s = s or sesion()
    resp = s.get(url, timeout=TIMEOUT, **kw)
    _clasificar(resp)
    return resp


@_reintentos
def cabecera(url: str, s: requests.Session | None = None) -> requests.Response:
    """HEAD con reintentos (sigue redirecciones)."""
    s = s or sesion()
    resp = s.head(url, timeout=TIMEOUT, allow_redirects=True)
    _clasificar(resp)
    return resp


@_reintentos
def rango(url: str, inicio: int, fin: int, s: requests.Session | None = None) -> bytes:
    """Descarga los bytes [inicio, fin] (inclusivo) con la cabecera Range."""
    s = s or sesion()
    with s.get(
        url, headers={"Range": f"bytes={inicio}-{fin}"}, timeout=TIMEOUT, stream=True
    ) as resp:
        _clasificar(resp)
        if resp.status_code != 206:
            # Un 200 aquí sería el archivo completo; no se lee el cuerpo.
            raise ErrorTransitorio(f"El servidor no respondió 206 a Range en {url}")
        contenido = resp.content
    esperado = fin - inicio + 1
    if len(contenido) != esperado:
        raise ErrorTransitorio(
            f"Range devolvió {len(contenido)} bytes, se esperaban {esperado} ({url})"
        )
    return contenido


def descargar(
    url: str,
    destino: Path,
    fuente: str,
    notas: str = "",
    force: bool = False,
    s: requests.Session | None = None,
    intentos: int = INTENTOS,
    timeout: tuple[int, int] = TIMEOUT,
) -> Path:
    """Descarga `url` a `destino` de forma idempotente y la registra en el manifiesto.

    - Si `destino` existe y su hash coincide con el manifiesto y no `force`: se salta.
    - Escribe primero a `<destino>.part` y renombra al terminar, para no dejar archivos truncos.
    """
    if not force and manifest.esta_vigente(destino):
        log.info("ya vigente, se salta: %s", destino.name)
        return destino

    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_suffix(destino.suffix + ".part")
    s = s or sesion()

    @_politica(intentos)
    def _bajar() -> None:
        with s.get(url, timeout=timeout, stream=True) as resp:
            _clasificar(resp)
            total = int(resp.headers.get("Content-Length") or 0)
            escritos = 0
            with (
                open(parcial, "wb") as f,
                tqdm(
                    total=total or None,
                    unit="B",
                    unit_scale=True,
                    desc=destino.name[:40],
                    leave=False,
                ) as barra,
            ):
                for trozo in resp.iter_content(chunk_size=1 << 16):
                    f.write(trozo)
                    escritos += len(trozo)
                    barra.update(len(trozo))
        # Un cierre limpio prematuro del servidor no lanza excepción: se verifica el tamaño para
        # no registrar en el manifiesto un archivo trunco.
        if total and escritos != total:
            parcial.unlink(missing_ok=True)
            raise ErrorTransitorio(f"descarga trunca: {escritos} de {total} bytes en {url}")

    _bajar()
    parcial.replace(destino)
    manifest.registrar(fuente, destino, url, notas)
    log.info("descargado: %s (%d bytes)", destino.name, destino.stat().st_size)
    return destino

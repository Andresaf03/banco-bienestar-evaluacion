"""Padrón Único de Beneficiarios (PUB) de la Secretaría de Bienestar: agregados municipales (fase 6).

Qué publica el portal https://pub.bienestar.gob.mx (revisado el 2026-11-17):
- **Consolidado municipal vigente** (`/data/v2/cons/consMpo<edo>.xlsx`, enlazado desde
  `/pub/agregado`): por municipio, beneficiarios únicos y monto; una sola foto (corte de octubre
  de 2026, con el último periodo de cada programa).
- **Historia de padrones** (`/v2/api/resume/publish/history`, la que usa `/pub/historyProgram`):
  agregados municipales `_m` por periodo, pero solo de programas ya terminados (28 filas; ninguno
  de los que paga el Banco del Bienestar). Se guarda como evidencia de esa limitación.
- Los periodos anteriores de los programas vigentes (p. ej., la pensión de adultos mayores desde
  enero de 2019) solo existen como **listas de personas con nombre e importe**. No se descargan
  (preregistro y adenda de la fase 6, `docs/decisiones.md`).

Se guardan en `data/raw/pub_bienestar/`: `historia_<AAAA-MM-DD>.json` y `consMpo<edo>.xlsx`.
"""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from proyecto.utils import http, manifest
from proyecto.utils.io import RAW, fuentes

log = logging.getLogger(__name__)

FUENTE = "pub_bienestar"
DESTINO = RAW / FUENTE
ENTIDADES = range(1, 33)


def _url(ruta: str) -> str:
    return fuentes()[FUENTE]["url_base"].rstrip("/") + ruta


def historia(s=None) -> Path:
    """Guarda la lista de historia del portal y la registra en el manifiesto."""
    url = _url(fuentes()[FUENTE]["ruta_historia"])
    datos = http.obtener(url, s).json()
    if not isinstance(datos, list):
        raise ValueError(f"la historia del PUB no es una lista: {type(datos).__name__}")
    ruta = DESTINO / f"historia_{date.today().isoformat()}.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    manifest.registrar(
        FUENTE, ruta, url, notas=f"historia del PUB: {len(datos)} filas, solo programas terminados"
    )
    return ruta


def descargar(force: bool = False) -> None:
    s = http.sesion()
    if force or not list(DESTINO.glob("historia_*.json")):
        historia(s)
    plantilla = fuentes()[FUENTE]["ruta_consolidado_municipal"]
    for edo in ENTIDADES:
        ruta = plantilla.format(edo=edo)
        http.descargar(
            _url(ruta),
            DESTINO / ruta.rsplit("/", 1)[-1],
            FUENTE,
            notas=f"consolidado municipal vigente del PUB, entidad {edo:02d}",
            force=force,
            s=s,
        )

"""SESNSP, incidencia delictiva municipal del fuero común 2015–2025 (fase 3).

El archivo está en el OneDrive del SESNSP (`sspcgob-my.sharepoint.com`). El enlace es anónimo,
pero el servidor pide la cookie de invitado que da el visor web. No se automatiza: el zip se bajó
una vez, con autorización, el 2026-10-11 (ver `docs/descarga_manual.md`) y vive en
`data/manual/sesnsp/`. Este módulo solo verifica que esté y lo registra en el manifiesto.
"""

from __future__ import annotations

from proyecto.descarga.manual import registrar_manual
from proyecto.utils.io import fuentes

FUENTE = "sesnsp"


def descargar(force: bool = False) -> None:
    del force  # la copia manual no se vuelve a bajar desde aquí
    cfg = fuentes()[FUENTE]
    registrar_manual(
        FUENTE,
        cfg["archivo"],
        cfg["url_recurso"],
        notas="SharePoint del SESNSP; corte ago-2026; CSV latin-1 de 2015-2025 + xlsx anuales",
    )

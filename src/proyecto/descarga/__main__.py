"""CLI: `python -m proyecto.descarga <fuente|todas> [--force]`."""

from __future__ import annotations

import argparse
import importlib
import logging
import sys

from proyecto.descarga.manual import FaltaArchivoManual

FUENTES = [
    "cnbv_bdif",
    "cnbv_portafolio",
    "denue",
    "babien",
    "inegi_mg",
    "conapo_marginacion",
    "conapo_proyecciones",
    "inegi_censo",
    "literatura",
    "inegi_ce",
    "enif",
    "banxico_remesas",
    "imss",
]
# Fase 2 (preregistro del 2026-10-07): por nombre o con `fase2`; `todas` no las incluye.
FASE2 = ["inegi_eic", "viirs", "efipem", "enoe"]
# Fase 3 (preregistro del 2026-10-11): delitos y elecciones.
FASE3 = ["ine_sicee", "sesnsp"]
# Fase 4 (preregistro del 2026-10-14): ENIGH.
FASE4 = ["enigh"]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Descarga de fuentes (idempotente).")
    p.add_argument(
        "fuente", choices=[*FUENTES, "todas", *FASE2, "fase2", *FASE3, "fase3", *FASE4, "fase4"]
    )
    p.add_argument(
        "--force", action="store_true", help="vuelve a descargar aunque el hash coincida"
    )
    a = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    seleccion = {"todas": FUENTES, "fase2": FASE2, "fase3": FASE3, "fase4": FASE4}.get(
        a.fuente, [a.fuente]
    )
    fallas: list[str] = []
    for nombre in seleccion:
        modulo = importlib.import_module(f"proyecto.descarga.{nombre}")
        try:
            modulo.descargar(force=a.force)
        except FaltaArchivoManual as exc:
            logging.error("%s: %s", nombre, exc)
            fallas.append(nombre)
        except Exception:
            logging.exception("%s: descarga fallida", nombre)
            fallas.append(nombre)
    if fallas:
        logging.error("fuentes con fallas: %s", ", ".join(fallas))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

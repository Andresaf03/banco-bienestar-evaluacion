"""CLI: `python -m proyecto.limpieza <fuente|todas>`. Orden: bdif -> inegi_censo -> municipios -> babien -> conapo."""

from __future__ import annotations

import argparse
import importlib
import logging
import sys

ORDEN = [
    "bdif",
    "cnbv_portafolio",
    "denue",
    "inegi_censo",
    "municipios",
    "babien",
    "banjercito",
    "conapo",
    "inegi_ce",
    "banxico_remesas",
    "imss",
    "diccionarios",
]
# Fase 2 (preregistro del 2026-10-07): se corren por nombre o con `fase2`; `todas` no las incluye
# para que `make limpiar` siga haciendo exactamente lo mismo que en la corrida final.
FASE2 = ["cnbv_portafolio_modelo", "inegi_eic", "viirs", "efipem", "enoe"]
# Fase 3 (preregistro del 2026-10-11): elecciones federales e incidencia delictiva.
FASE3 = ["ine_elecciones", "sesnsp"]
# Fase 4 (preregistro del 2026-10-14): ENIGH.
FASE4 = ["enigh"]
# Fase 6 (preregistro del 2026-11-17): consolidado municipal del padrón de Bienestar.
FASE6 = ["pub_bienestar"]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Limpieza mínima por fuente -> data/interim/*.parquet")
    p.add_argument(
        "fuente",
        choices=[
            *ORDEN,
            "todas",
            *FASE2,
            "fase2",
            *FASE3,
            "fase3",
            *FASE4,
            "fase4",
            *FASE6,
            "fase6",
        ],
    )
    p.add_argument("--force", action="store_true", help="BDIF: reprocesa aunque exista caché")
    a = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    seleccion = {
        "todas": ORDEN,
        "fase2": FASE2,
        "fase3": FASE3,
        "fase4": FASE4,
        "fase6": FASE6,
    }.get(a.fuente, [a.fuente])
    for nombre in seleccion:
        mod = importlib.import_module(f"proyecto.limpieza.{nombre}")
        if nombre == "bdif":
            mod.limpiar(force=a.force)
        elif nombre == "diccionarios":
            mod.generar()
        else:
            mod.limpiar()
    return 0


if __name__ == "__main__":
    sys.exit(main())

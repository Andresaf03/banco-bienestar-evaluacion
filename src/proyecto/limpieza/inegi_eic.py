"""EIC 2015, Censo 2020 (ampliado) y EIC 2025 por municipio -> `inegi_eic_municipio.parquet`.

Junta las sumas ponderadas que deja `descarga/inegi_eic.py` (una parte por entidad y corte), colapsa
los municipios creados después de 2010 en su municipio de origen (P-7, sumando antes de dividir) y
calcula los indicadores preregistrados el 2026-10-07 (`docs/decisiones.md`), en porcentaje:

| indicador | numerador / denominador (ponderados con FACTOR) |
|---|---|
| `pct_negocio` | (patrón + cuenta propia) / ocupados con posición especificada |
| `pct_cuenta_propia`, `pct_empleador` | cuenta propia / ídem; patrón / ídem |
| `pct_ocupacion` | ocupados / población de 12 años y más |
| `log_ingreso_trabajo` | media ponderada de log(ingreso mensual por trabajo > 0) |
| `pct_trabaja_otro_mun` | ocupados que trabajan en otro municipio o país / lugar especificado |
| `pct_hog_programas` | viviendas con dinero de programas de gobierno / respuesta especificada |
| `pct_hog_remesas` | viviendas con dinero de otro país / respuesta especificada |
| `pct_viv_internet`, `pct_viv_celular` | viviendas con el bien / respuesta especificada |
| `log_poblacion_est` | log de la población estimada (suma de FACTOR) |

`n_personas` y `n_viviendas` son los registros muestrales (no ponderados) de cada municipio-corte.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM

log = logging.getLogger(__name__)

PARTES = INTERIM / "inegi_eic" / "partes"
SALIDA = INTERIM / "inegi_eic_municipio.parquet"


def _pct(num: pd.Series, den: pd.Series) -> pd.Series:
    return 100 * num / den.where(den > 0)


def indicadores(s: pd.DataFrame) -> pd.DataFrame:
    """Indicadores a partir de las sumas ponderadas (una fila por municipio y corte)."""
    out = s[["cve_mun", "anio", "n_personas", "n_viviendas"]].copy()
    out["pct_negocio"] = _pct(s["cuenta_propia"] + s["empleadores"], s["pos_validos"])
    out["pct_cuenta_propia"] = _pct(s["cuenta_propia"], s["pos_validos"])
    out["pct_empleador"] = _pct(s["empleadores"], s["pos_validos"])
    out["pct_ocupacion"] = _pct(s["ocupados"], s["pob12"])
    out["log_ingreso_trabajo"] = s["ing_log_suma"] / s["ing_validos"].where(s["ing_validos"] > 0)
    out["pct_trabaja_otro_mun"] = _pct(s["otro_mun"], s["lugar_validos"])
    out["pct_hog_programas"] = _pct(s["viv_programas"], s["viv_prog_validas"])
    out["pct_hog_remesas"] = _pct(s["viv_remesas"], s["viv_rem_validas"])
    out["pct_viv_internet"] = _pct(s["viv_internet"], s["viv_net_validas"])
    out["pct_viv_celular"] = _pct(s["viv_celular"], s["viv_cel_validas"])
    out["log_poblacion_est"] = np.log(s["pob"].where(s["pob"] > 0))
    out["poblacion_est"] = s["pob"]
    return out


def limpiar() -> None:
    archivos = sorted(PARTES.glob("*.parquet"))
    if len(archivos) != 96:
        raise RuntimeError(
            f"se esperaban 96 partes (32 entidades × 3 cortes) y hay {len(archivos)}"
        )
    s = pd.concat([pd.read_parquet(a) for a in archivos], ignore_index=True)
    s["cve_mun"] = s["cve_mun"].map(mapa_crosswalk()).fillna(s["cve_mun"])
    sumas = [c for c in s.columns if c not in ("cve_mun", "anio")]
    s = s.groupby(["cve_mun", "anio"], as_index=False)[sumas].sum()
    d = indicadores(s)
    d.to_parquet(SALIDA, index=False)
    nac = indicadores(s.groupby("anio", as_index=False)[sumas].sum().assign(cve_mun="00000"))
    log.info(
        "EIC/Censo municipal: %d filas, municipios por corte %s\nnacional:\n%s",
        len(d),
        d.groupby("anio")["cve_mun"].nunique().to_dict(),
        nac.drop(columns=["cve_mun"]).round(2).to_string(index=False),
    )

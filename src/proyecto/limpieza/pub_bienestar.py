"""Consolidado municipal vigente del Padrón Único de Beneficiarios (fase 6, adenda).

Lee la hoja `Municipio` de los 32 `consMpo<edo>.xlsx` (`data/raw/pub_bienestar/`): por municipio,
beneficiarios únicos (personas con al menos un programa en el último periodo publicado de cada
programa) y monto (suma de esos periodos). Es una foto con corte de octubre de 2026.

Advertencias (ver `docs/diccionarios/fase6.md`):
- el monto suma periodos distintos según el programa (trimestral, bimestral o anual), así que solo
  sirve para comparar municipios entre sí, no como flujo de un periodo;
- la clave `999` ("NO ESPECIFICADO") se descarta: no tiene municipio;
- las claves vienen como texto de entidad (2) y municipio (3) y se combinan sin cruzar por nombre.

Salida: `data/interim/pub_municipio.parquet` con `cve_mun, nom_mun_pub, beneficiarios_unicos,
monto`.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from proyecto.utils import claves
from proyecto.utils.io import INTERIM, RAW

log = logging.getLogger(__name__)

ORIGEN = RAW / "pub_bienestar"
SALIDA = INTERIM / "pub_municipio.parquet"
COLUMNAS = {
    "Clave Entidad": "cve_ent",
    "Clave Municipio": "cve_mun3",
    "Nombe Municipio": "nom_mun_pub",
    "Beneficiarios Unicos": "beneficiarios_unicos",
    "Monto": "monto",
}


def leer_consolidado(ruta: Path) -> pd.DataFrame:
    """Tabla municipal de un `consMpo<edo>.xlsx`; el encabezado está en la fila 5."""
    crudo = pd.read_excel(ruta, sheet_name="Municipio", header=None, dtype=object)
    fila = crudo.index[crudo.iloc[:, 0].astype(str).str.strip() == "Clave Entidad"]
    if len(fila) != 1:
        raise ValueError(f"{ruta.name}: no se encontró el encabezado de la hoja Municipio")
    tabla = crudo.iloc[fila[0] + 1 :, : len(COLUMNAS)].copy()
    tabla.columns = list(COLUMNAS.values())
    tabla = tabla.dropna(subset=["cve_ent", "cve_mun3"])
    tabla["cve_ent"] = tabla["cve_ent"].astype(str).str.strip().str.zfill(2)
    tabla["cve_mun3"] = tabla["cve_mun3"].astype(str).str.strip().str.zfill(3)
    tabla["beneficiarios_unicos"] = pd.to_numeric(tabla["beneficiarios_unicos"], errors="raise")
    tabla["monto"] = pd.to_numeric(tabla["monto"], errors="raise")
    return tabla


def limpiar() -> Path:
    rutas = sorted(ORIGEN.glob("consMpo*.xlsx"))
    if len(rutas) != 32:
        raise FileNotFoundError(
            f"se esperaban 32 consolidados en {ORIGEN}, hay {len(rutas)}; corre "
            "`make descargar-fase6`"
        )
    tabla = pd.concat([leer_consolidado(r) for r in rutas], ignore_index=True)
    sin_mun = tabla["cve_mun3"] == "999"
    log.info(
        "PUB: %s beneficiarios sin municipio (%.1f%%) se descartan",
        f"{tabla.loc[sin_mun, 'beneficiarios_unicos'].sum():,.0f}",
        100
        * tabla.loc[sin_mun, "beneficiarios_unicos"].sum()
        / tabla["beneficiarios_unicos"].sum(),
    )
    tabla = tabla[~sin_mun].copy()
    tabla["cve_mun"] = claves.combinar(tabla["cve_ent"], tabla["cve_mun3"])
    invalidas = ~tabla["cve_mun"].map(claves.es_valida)
    if invalidas.any():
        raise ValueError(
            f"claves municipales inválidas: {tabla.loc[invalidas, 'cve_mun'].tolist()}"
        )
    if tabla["cve_mun"].duplicated().any():
        raise ValueError("claves municipales duplicadas en el consolidado del PUB")
    salida = tabla[["cve_mun", "nom_mun_pub", "beneficiarios_unicos", "monto"]]
    salida.to_parquet(SALIDA, index=False)
    log.info(
        "PUB: %d municipios, %s beneficiarios únicos",
        len(salida),
        f"{salida['beneficiarios_unicos'].sum():,.0f}",
    )
    return SALIDA

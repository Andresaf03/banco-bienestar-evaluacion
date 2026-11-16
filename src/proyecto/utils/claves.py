"""Claves municipales: siempre texto de 5 dígitos (`cve_ent` de 2 + `cve_mun` de 3).

Nunca se unen bases por nombre de municipio. Estas funciones normalizan lo que venga
(enteros, floats, textos con o sin ceros) a la clave canónica.
"""

from __future__ import annotations

import pandas as pd

LARGO_ENT = 2
LARGO_MUN = 3
LARGO_CVE = LARGO_ENT + LARGO_MUN
LARGO_LOC = 4
LARGO_CVE_LOC = LARGO_CVE + LARGO_LOC  # clave de localidad: ent(2) + mun(3) + loc(4) = 9


def normalizar_cve(valor: object) -> str | None:
    """Convierte un valor a clave de 5 dígitos. Devuelve None si no es interpretable.

    >>> normalizar_cve(1001)
    '01001'
    >>> normalizar_cve("1001.0")
    '01001'
    >>> normalizar_cve("09002")
    '09002'
    """
    if valor is None:
        return None
    if isinstance(valor, float):
        if pd.isna(valor):
            return None
        valor = int(valor)
    texto = str(valor).strip()
    if texto.endswith(".0"):
        texto = texto[:-2]
    if not texto.isdigit():
        return None
    if len(texto) > LARGO_CVE:
        return None
    return texto.zfill(LARGO_CVE)


def normalizar_serie(s: pd.Series) -> pd.Series:
    """Aplica `normalizar_cve` a toda una serie; devuelve dtype `string`."""
    return s.map(normalizar_cve).astype("string")


def combinar(cve_ent: pd.Series, cve_mun: pd.Series) -> pd.Series:
    """Construye la clave de 5 dígitos a partir de entidad (2) y municipio (3)."""
    ent = cve_ent.map(lambda v: None if v is None or pd.isna(v) else str(int(float(v))).zfill(2))
    mun = cve_mun.map(lambda v: None if v is None or pd.isna(v) else str(int(float(v))).zfill(3))
    return (ent + mun).astype("string")


def es_valida(cve: object) -> bool:
    """True si es texto de exactamente 5 dígitos con entidad entre 01 y 32."""
    if not isinstance(cve, str) or len(cve) != LARGO_CVE or not cve.isdigit():
        return False
    return 1 <= int(cve[:LARGO_ENT]) <= 32


def cve_ent_de(cve: str) -> str:
    return cve[:LARGO_ENT]


def combinar_localidad(cve_mun: pd.Series, cve_loc4: pd.Series) -> pd.Series:
    """Clave de localidad de 9 dígitos a partir del municipio (5) y el consecutivo (4).

    El ITER y el DENUE publican el consecutivo de localidad por separado; la clave única nacional
    es la concatenación. Nunca se usa el consecutivo solo como llave.
    """
    loc = cve_loc4.map(
        lambda v: None if v is None or pd.isna(v) else str(v).strip().zfill(LARGO_LOC)
    )
    return (cve_mun.astype("string") + loc.astype("string")).astype("string")


def es_valida_localidad(cve_loc: object) -> bool:
    """True si es texto de 9 dígitos cuyo municipio es válido."""
    if not isinstance(cve_loc, str) or len(cve_loc) != LARGO_CVE_LOC or not cve_loc.isdigit():
        return False
    return es_valida(cve_loc[:LARGO_CVE])

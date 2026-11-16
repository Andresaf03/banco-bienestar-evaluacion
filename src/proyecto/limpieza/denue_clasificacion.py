"""Clasificación SCIAN del DENUE en los bloques temáticos del proyecto.

Cada establecimiento del DENUE trae `codigo_act` (SCIAN 2018, 6 dígitos). Se clasifica en:

- `emprendimiento`: **todos** los establecimientos (el bloque se mide con conteos y con el
  subconjunto de micronegocios de 0 a 5 personas, proxy de autoempleo / informalidad).
- `consumo`: comercio al por menor (46) y servicios de alimentos y bebidas (722).
- `salud`: servicios médicos (62) y farmacias (46411, dentro de comercio al por menor).
- `financiero`: banca múltiple (5221), cajas de ahorro popular y otras instituciones de ahorro
  (5223), uniones de crédito (5224) y casas de empeño (5222).

Un establecimiento puede caer en varios bloques (una farmacia es `consumo` y `salud`); los
conteos por bloque no son excluyentes y así se documenta en el diccionario.

**Advertencia sobre el bloque financiero.** El DENUE cuenta *establecimientos*, no sucursales en
el sentido regulatorio: en 2016 registra 23,437 unidades de banca múltiple (SCIAN 5221) cuando la
CNBV reporta unas 13,000 sucursales, porque incluye cajeros y módulos como establecimientos
separados. Sirve como medida de **presencia** financiera privada a nivel localidad —que es lo que
la BDIF no puede dar— pero no es comparable en niveles con el conteo de la CNBV. Para conteos de
sucursales en sentido estricto se usa el panel municipal trimestral.
"""

from __future__ import annotations

import pandas as pd

# Clases finas dentro de cada bloque (prefijos de SCIAN; el primero que empata gana).
CLASES: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "consumo": [
        ("farmacia", ("46411",)),
        ("abarrotes_alimentos", ("4611", "4612")),
        ("comercio_menor_otros", ("46",)),
        ("restaurantes", ("7223", "7224", "7225")),
        ("hospedaje", ("7211", "7212", "7213")),
    ],
    "salud": [
        ("farmacia", ("46411",)),
        ("consultorios", ("6211", "6212", "6213")),
        ("hospitales", ("622",)),
        ("otros_salud", ("6214", "6215", "6216", "6219", "623", "624")),
    ],
    "financiero": [
        ("banca_multiple", ("5221",)),
        ("casas_empeno", ("5222",)),
        ("cajas_ahorro", ("5223",)),
        ("uniones_credito", ("5224",)),
        ("otros_financiero", ("523", "524", "525")),
    ],
}

BLOQUES = ("emprendimiento", "consumo", "salud", "financiero")


def clasificar(codigo_act: pd.Series) -> pd.DataFrame:
    """Devuelve un DataFrame booleano con una columna por bloque y la clase fina de cada bloque.

    `emprendimiento` es True para todo establecimiento con SCIAN válido.
    """
    cod = codigo_act.fillna("").astype(str).str.strip()
    salida = pd.DataFrame(index=cod.index)
    salida["emprendimiento"] = cod.str.len() >= 2
    salida["clase_emprendimiento"] = cod.str[:2].where(salida["emprendimiento"], "")
    for bloque, reglas in CLASES.items():
        clase = pd.Series("", index=cod.index, dtype="object")
        for nombre, prefijos in reglas:
            sin_asignar = clase == ""
            empata = cod.str.startswith(prefijos)
            clase = clase.mask(sin_asignar & empata, nombre)
        salida[bloque] = clase != ""
        salida[f"clase_{bloque}"] = clase
    return salida

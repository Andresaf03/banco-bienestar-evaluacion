"""Clasificación de columnas de la BDIF municipal a nombres canónicos.

La BDIF cambió de layout cuatro veces entre 2016T1 y 2025T4 (ver docs/diccionarios/cnbv_bdif.md):

- Era A (2016T1–2017T4): hojas `BD Acceso Mun`, `BD Uso Mun`, `BD Uso EACP Mun`. Encabezado plano.
- Era B (2018T1–2018T4): `BD Acceso Mun`, `BD Uso Banca Mun`, `BD Uso EACP Mun`, `BD Género Mun`.
- Era C (2019T1–2022T3): `BD Infraestructura Mun`, `BD Tenencia Uso Banca Mun`,
  `BD Tenencia Uso EACP Mun`, `BD Género Mun`.
- Era D (2022T4–): `BD Infraestructura Mun`, `BD Captación Mun`, `BD Crédito Mun`,
  `BD por sexo * Mun`, con encabezado multinivel por sector.

En las eras A–C solo las **sucursales** vienen separadas por sector; captación, crédito y
transacciones vienen como "Banca" (múltiple + desarrollo) y "EACP" (SOCAP + SOFIPO) combinados.
En la era D todo viene por sector.

`clasificar(hoja, niveles, encabezado)` recibe las etiquetas de los renglones superiores
(forward-fill hacia la derecha) y el encabezado de la columna, y devuelve `(sector, variable)`
o `None` si la columna no se conserva (indicadores por 10 mil adultos, saldos, columnas de
información general).
"""

from __future__ import annotations

import re
import unicodedata

SECTORES = ("todos", "banca", "banca_multiple", "banca_desarrollo", "socap", "sofipo", "eacp")

COLUMNAS_GENERALES = {
    "clave municipio": "cve_mun",
    "clave estado": "cve_ent",
    "region": "region",
    "estado": "nom_ent",
    "municipio": "nom_mun",
    "poblacion": "poblacion",
    "poblacion total": "poblacion",
    "poblacion adulta": "poblacion_adulta",
    "poblacion adulta mujeres": "poblacion_adulta_mujeres",
    "poblacion adulta hombres": "poblacion_adulta_hombres",
    "tipo de poblacion": "tipo_poblacion",
    "indice de rezago social": "indice_rezago_social",
    "superficie km2": "superficie_km2",
}


def normalizar(texto: str | None) -> str:
    """Minúsculas, sin acentos, espacios colapsados, sin sufijos 'Número ...'."""
    if texto is None:
        return ""
    t = str(texto).replace("\n", " ").replace("´", "'").replace("'s", "")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\bnumero( de (cuentas|creditos|tarjetas))?\b", "", t)
    t = re.sub(r"\s+", " ", t).strip(" -")
    return t


def _sector_por_nivel(niveles: list[str]) -> str | None:
    texto = " | ".join(normalizar(n) for n in niveles)
    if "banca multiple" in texto:
        return "banca_multiple"
    if "banca de desarrollo" in texto:
        return "banca_desarrollo"
    if "sociedades cooperativas" in texto or "socap" in texto:
        return "socap"
    if "sociedades financieras populares" in texto or "sofipo" in texto:
        return "sofipo"
    if "todos los sectores" in texto:
        # Era D, bloque "Todos los sectores": sub-bloques Banca / EACP / Total.
        if "entidades de ahorro y credito popular" in texto or "| eacp" in texto:
            return "eacp"
        if "| banca" in texto:
            return "banca"
        return "todos"
    if "eacp" in texto or "entidades de ahorro y credito popular" in texto:
        return "eacp"
    if "banca" in texto:
        return "banca"
    return None


def _bloque(hoja: str, niveles: list[str]) -> str:
    """Bloque temático de la columna; se revisa del nivel más específico al más general."""
    h = normalizar(hoja)
    etiquetas_sector = ("sectores", "entidades de ahorro", "sociedades", "banca", "eacp")
    for nivel in reversed(niveles):
        texto = normalizar(nivel)
        if texto == "infraestructura y transacciones":
            continue
        if any(e in texto for e in etiquetas_sector):
            continue  # etiqueta de sector, no de bloque
        for clave in ("captacion", "credito", "transacciones", "clientes", "socios", "usuarios"):
            if clave in texto:
                return clave
        if "infraestructura" in texto or "puntos de acceso" in texto:
            return "infraestructura"
    if "captacion" in h:
        return "captacion"
    if "credito" in h:
        return "credito"
    if "acceso" in h or "infraestructura" in h:
        return "infraestructura"
    return ""


_VARIABLES_INFRA = [
    (r"^(sucursales )?banca comercial$", ("banca_multiple", "sucursales")),
    (r"^(sucursales )?banca de desarrollo$", ("banca_desarrollo", "sucursales")),
    (r"^(sucursales socap|cooperativas)$", ("socap", "sucursales")),
    (r"^(sucursales sofipo|microfinancieras)$", ("sofipo", "sucursales")),
    (r"^total sucursales$", ("todos", "sucursales")),
    (r"^sucursales$", (None, "sucursales")),
    (r"^modulos de atencion compartamos$", ("banca_multiple", "modulos_compartamos")),
    (r"^corresponsales( unicos)?1?$", ("todos", "corresponsales")),
    (r"^cajeros( automaticos)?$", (None, "cajeros")),
    (r"^(terminales punto de venta|tpv)$", (None, "tpv")),
    (r"^establecimientos con tpv$", (None, "establecimientos_tpv")),
    (
        r"^(contratos que (utilizan banca movil|afectan por celular)|cuentas que efectuan transacciones por celular)$",
        (None, "cuentas_celular"),
    ),
    (r"^transacciones en cajeros automaticos$", (None, "transacciones_cajeros")),
    (r"^transacciones en tpv$", (None, "transacciones_tpv")),
]

_VARIABLES_CAPTACION = [
    (r"^(cuentas de ahorro|ahorro|depositos? al ahorro)$", "capt_ahorro"),
    (r"^(depositos? a plazo|plazo)$", "capt_plazo"),
    (r"^depositos? a la vista$", "capt_vista"),
    (r"^(cuentas )?transaccionales nivel 1$", "capt_n1"),
    (r"^(cuentas )?transaccionales nivel 2$", "capt_n2"),
    (r"^(cuentas )?transaccionales nivel 3$", "capt_n3"),
    (r"^(cuentas )?transaccionales nivel 4$", "capt_n4"),
    (r"^cuentas transaccionales tradicionales$", "capt_tradicionales"),
    (r"^tarjetas? (de )?debito$", "tarjetas_debito"),
    (r"^total( captacion)?$", "capt_total"),
]

_VARIABLES_CREDITO = [
    (r"^tarjetas? de credito$", "tarjetas_credito"),
    (r"^personal$", "cred_personal"),
    (r"^nomina$", "cred_nomina"),
    (r"^abcd$", "cred_abcd"),
    (r"^grupal$", "cred_grupal"),
    (r"^hipotecario$", "cred_hipotecario"),
    (r"^automotriz$", "cred_automotriz"),
    (r"^(credito al )?consumo$", "cred_consumo"),
    (r"^(credito a la )?vivienda$", "cred_vivienda"),
    (r"^comercial$", "cred_comercial"),
    (r"^total$", "cred_total"),
]

_VARIABLES_TRANSACCIONES = [
    (r"^(en tpv|transacciones en tpv)$", "transacciones_tpv"),
    (r"^(en cajeros automaticos|transacciones en cajeros automaticos)$", "transacciones_cajeros"),
]


def _buscar(tabla, texto):
    for patron, valor in tabla:
        if re.match(patron, texto):
            return valor
    return None


def clasificar(hoja: str, niveles: list[str], encabezado: str) -> tuple[str, str] | None:
    """Devuelve (sector, variable) canónicos o None si la columna se descarta.

    Las columnas de información general (clave, población, ...) devuelven ("_general", nombre).
    """
    enc = normalizar(encabezado)
    if not enc:
        return None
    if enc in COLUMNAS_GENERALES:
        return ("_general", COLUMNAS_GENERALES[enc])
    niv_txt = " | ".join(normalizar(n) for n in niveles)
    if "10,000" in niv_txt or "10 000" in niv_txt or "por cada" in niv_txt:
        return None  # indicadores por 10 mil adultos: se recalculan en el panel
    if "saldo" in niv_txt or "sexo" in niv_txt or normalizar(hoja).startswith("bd genero"):
        return None
    if "sin comercial" in enc:
        return None

    bloque = _bloque(hoja, niveles)
    sector_nivel = _sector_por_nivel(niveles)

    if bloque == "infraestructura":
        res = _buscar(_VARIABLES_INFRA, enc)
        if res is None:
            return None
        sector_fijo, variable = res
        sector = sector_nivel if sector_nivel else sector_fijo
        if sector_nivel == "todos" and sector_fijo not in (None, "todos"):
            sector = sector_fijo
        if sector is None:
            sector = "todos"
        return (sector, variable)

    if bloque == "transacciones":
        var = _buscar(_VARIABLES_TRANSACCIONES, enc)
        if var is None:
            return None
        sector = sector_nivel or ("eacp" if "eacp" in normalizar(hoja) else "banca")
        return (sector, var)

    if bloque == "captacion":
        var = _buscar(_VARIABLES_CAPTACION, enc)
        if var is None:
            return None
        sector = sector_nivel or ("eacp" if "eacp" in normalizar(hoja) else "banca")
        return (sector, var)

    if bloque == "credito":
        var = _buscar(_VARIABLES_CREDITO, enc)
        if var is None:
            return None
        sector = sector_nivel or ("eacp" if "eacp" in normalizar(hoja) else "banca")
        return (sector, var)

    if bloque in ("clientes", "socios", "usuarios"):
        if enc not in ("mujeres", "hombres"):
            return None
        if "sofipo" in niv_txt:
            return ("sofipo", f"usuarios_{enc}")
        if "socap" in niv_txt:
            return ("socap", f"usuarios_{enc}")
        return ("eacp", f"usuarios_{enc}")

    return None

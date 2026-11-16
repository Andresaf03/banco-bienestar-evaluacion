"""INE, diputaciones federales de MR por casilla -> `data/interim/ine_diputados_municipio.parquet`.

Fase 3 (preregistro del 2026-10-11). De cada zip del SICEE (`data/raw/ine_sicee/`) se lee el
archivo por casilla (`*_NAL_CAS.csv`) y se agrega por municipio:

- Entran las casillas básicas, contiguas y extraordinarias. Salen las especiales (votan sin lista
  nominal), las mesas sin sección (prisión preventiva, voto anticipado) y las casillas no
  instaladas, con paquete no entregado o con la votación suspendida, del numerador y del
  denominador.
- Los votos por combinación de coalición se reparten por igual entre los partidos de la
  combinación (sin redondeo). El bloque en el gobierno tiene composición fija en las cuatro
  elecciones (`parametros.fase3.elecciones.bloque`).
- La clave municipal del INE no es la del INEGI: se cruza por nombre dentro de la entidad con
  `utils.cruce_nombres` (excepción controlada a la regla 6). El cruce y su resumen quedan en
  `data/interim/cruce_municipios_ine.parquet` y `docs/diccionarios/cruce_municipios_ine.md`.

Los archivos vienen en UTF-8, pero 2024 trae líneas en latin-1: se decodifica línea por línea.
"""

from __future__ import annotations

import io
import logging
import zipfile

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.cruce_nombres import cruzar, manuales, normalizar, resumen_md
from proyecto.utils.io import DICCIONARIOS, INTERIM, RAW, parametros

log = logging.getLogger(__name__)

SALIDA = INTERIM / "ine_diputados_municipio.parquet"
CRUCE = INTERIM / "cruce_municipios_ine.parquet"
# Siglas de partido que aparecen en las cuatro elecciones. `NVA_ALIANZA` lleva guion bajo, así que
# las combinaciones se separan buscando siglas completas, no partiendo por "_".
PARTIDOS = [
    "NVA_ALIANZA",
    "MORENA",
    "PVEM",
    "PAN",
    "PRI",
    "PRD",
    "MC",
    "PT",
    "NA",
    "PH",
    "ES",
    "PES",
    "RSP",
    "FXM",
]
SUMAS = [
    "votos_bloque",
    "votos_morena",
    "votos_validos",
    "votos_nulos",
    "votos_no_registrados",
    "total_votos",
    "lista_nominal",
    "casillas",
]


def decodificar(contenido: bytes) -> str:
    """UTF-8 línea por línea, con respaldo en latin-1 para las líneas que no lo son."""
    lineas = []
    for linea in contenido.split(b"\n"):
        try:
            lineas.append(linea.decode("utf-8"))
        except UnicodeDecodeError:
            lineas.append(linea.decode("latin-1"))
    return "\n".join(lineas).lstrip("﻿")


def miembros(columna: str) -> list[str] | None:
    """Partidos de una columna de votos: `[p]` si es un partido, la lista si es una combinación
    (`PRI_PVEM`, `PT_MORENA_ES`, `PAN_NVA_ALIANZA`) y None si no es ninguna de las dos."""
    if columna in PARTIDOS:
        return [columna]
    resto, partes = columna, []
    while resto:
        siguiente = next((p for p in PARTIDOS if resto == p or resto.startswith(p + "_")), None)
        if siguiente is None:
            return None
        partes.append(siguiente)
        resto = resto[len(siguiente) + 1 :]
    return partes if len(partes) >= 2 else None


def votos_por_partido(d: pd.DataFrame) -> pd.DataFrame:
    """Votos de cada partido con su parte igual de cada combinación en la que participa."""
    columnas = {c: m for c in d.columns if (m := miembros(c)) is not None}
    partidos = sorted({p for m in columnas.values() for p in m})
    salida = pd.DataFrame(0.0, index=d.index, columns=partidos)
    for columna, m in columnas.items():
        votos = pd.to_numeric(d[columna], errors="coerce").fillna(0)
        for p in m:
            salida[p] += votos / len(m)
    return salida


def _tipo_casilla(d: pd.DataFrame) -> pd.Series:
    # 2015 no trae TIPO_CASILLA: la letra inicial de CASILLA (B01, C02, E1C1, S1) es el tipo.
    if "TIPO_CASILLA" in d.columns:
        return d["TIPO_CASILLA"].astype(str).str.strip()
    return d["CASILLA"].astype(str).str.strip().str[0]


def leer_casillas(anio: int) -> pd.DataFrame:
    ruta = RAW / "ine_sicee" / f"DIPUTACIONES_FED_MR_{anio}.zip"
    with zipfile.ZipFile(ruta) as z:
        nombre = next(n for n in z.namelist() if n.endswith(f"{anio}_SEE_DIP_FED_MR_NAL_CAS.csv"))
        texto = decodificar(z.read(nombre))
    return pd.read_csv(io.StringIO(texto), low_memory=False)


def casillas_validas(d: pd.DataFrame, cfg: dict) -> pd.Series:
    """Casillas que entran: con sección y lista nominal, instaladas y con paquete computado."""
    tipo = _tipo_casilla(d)
    estatus = d["ESTATUS_ACTA"].fillna("").astype(str)
    fuera_estatus = estatus.str.contains(cfg["estatus_fuera"], case=False, regex=True)
    return ~tipo.isin(cfg["tipos_fuera"]) & ~fuera_estatus & (d["ID_MUNICIPIO"] > 0)


def agregar_anio(anio: int, cfg: dict) -> pd.DataFrame:
    """Casillas de un año -> municipio INE con votos del bloque, de Morena, válidos y totales."""
    d = leer_casillas(anio)
    entra = casillas_validas(d, cfg)
    num = lambda c: pd.to_numeric(d[c], errors="coerce").fillna(0)  # noqa: E731
    por_partido = votos_por_partido(d)
    independientes = [c for c in d.columns if c.startswith("CAND_IND")]
    validos = por_partido.sum(axis=1) + sum((num(c) for c in independientes), 0)
    c = pd.DataFrame(
        {
            "cve_ent": d["ID_ESTADO"].astype(int).astype(str).str.zfill(2),
            "id_municipio_ine": d["ID_MUNICIPIO"].astype(int),
            "municipio_ine": d["MUNICIPIO"].astype(str).str.strip(),
            "votos_bloque": por_partido[[p for p in cfg["bloque"] if p in por_partido]].sum(axis=1),
            "votos_morena": por_partido["MORENA"],
            "votos_validos": validos,
            "votos_nulos": num("NUM_VOTOS_NULOS"),
            "votos_no_registrados": num("NUM_VOTOS_CAN_NREG"),
            "total_votos": num("TOTAL_VOTOS"),
            "lista_nominal": num("LISTA_NOMINAL"),
            "casillas": 1,
        }
    )
    # Cuadre: votos válidos + nulos + no registrados = total de votos del acta.
    descuadre = (c["votos_validos"] + c["votos_nulos"] + c["votos_no_registrados"]) - c[
        "total_votos"
    ]
    log.info(
        "%d: %d casillas, entran %d; fuera %d votos de %d (%.2f%%); actas que no cuadran: %d",
        anio,
        len(c),
        int(entra.sum()),
        int(c.loc[~entra, "total_votos"].sum()),
        int(c["total_votos"].sum()),
        100 * c.loc[~entra, "total_votos"].sum() / c["total_votos"].sum(),
        int((descuadre.abs() > 0.5).sum()),
    )
    c = c[entra]
    agregado = c.groupby(["cve_ent", "id_municipio_ine"], as_index=False)[SUMAS].sum()
    nombres = c.groupby(["cve_ent", "id_municipio_ine"])["municipio_ine"].agg(
        lambda s: s.mode().iloc[0]
    )
    agregado = agregado.merge(nombres.reset_index(), on=["cve_ent", "id_municipio_ine"])
    return agregado.assign(anio=anio)


def _clave_ine(d: pd.DataFrame) -> pd.Series:
    """Entidad, municipio INE y nombre normalizado: `07-120|mezcalapa`.

    El nombre entra en la clave porque el INE **reasigna** claves cuando se crean municipios (en
    Chiapas, 07-120 a 07-124 cambian de municipio entre 2015 y 2024): cada combinación se cruza por
    su cuenta y una clave reasignada no mezcla dos municipios.
    """
    return (
        d["cve_ent"]
        + "-"
        + d["id_municipio_ine"].astype(str).str.zfill(3)
        + "|"
        + d["municipio_ine"].map(normalizar)
    )


def catalogo_ine(d: pd.DataFrame) -> pd.DataFrame:
    """Un renglón por clave INE + nombre, con las elecciones en que aparece."""
    d = d.assign(clave_ine=_clave_ine(d))
    numero = d["clave_ine"].str.split("|").str[0]
    reasignadas = d.assign(numero=numero).groupby("numero")["clave_ine"].nunique()
    reasignadas = reasignadas[reasignadas > 1]
    if len(reasignadas):
        log.info(
            "claves INE con más de un nombre entre elecciones (%d; se cruzan por separado): %s",
            len(reasignadas),
            ", ".join(reasignadas.index),
        )
    cat = d.groupby(["clave_ine", "cve_ent"], as_index=False).agg(
        municipio_ine=("municipio_ine", "last"),
        elecciones=("anio", lambda s: ", ".join(str(a) for a in sorted(s))),
    )
    return cat


def limpiar() -> None:
    cfg = parametros()["fase3"]["elecciones"]
    d = pd.concat([agregar_anio(a, cfg) for a in cfg["anios"]], ignore_index=True)
    cruce = cruzar(catalogo_ine(d), "clave_ine", "cve_ent", "municipio_ine", manuales("ine"))
    cruce.to_parquet(CRUCE, index=False)
    (DICCIONARIOS / "cruce_municipios_ine.md").write_text(
        resumen_md(cruce, "INE (diputaciones federales 2015–2024)", "clave_ine", "municipio_ine"),
        encoding="utf-8",
    )
    d = d.assign(clave_ine=_clave_ine(d)).merge(
        cruce[["clave_ine", "cve_mun", "metodo"]], on="clave_ine", how="left"
    )
    # Dentro de una misma elección, dos claves INE no deben caer en el mismo municipio INEGI (entre
    # elecciones sí: claves reasignadas y nombres que cambian).
    duplicadas = d.dropna(subset=["cve_mun"]).groupby(["anio", "cve_mun"])["clave_ine"].nunique()
    if (duplicadas > 1).any():
        raise ValueError(f"claves INE duplicadas en un año: {duplicadas[duplicadas > 1].to_dict()}")
    sin = d["cve_mun"].isna()
    for anio, g in d.groupby("anio"):
        log.info(
            "%d: %d de %d municipios INE sin cruzar; %.3f%% de la lista nominal fuera",
            anio,
            int(sin[g.index].sum()),
            len(g),
            100 * g.loc[sin[g.index], "lista_nominal"].sum() / g["lista_nominal"].sum(),
        )
    d = d[~sin]
    d["cve_mun"] = d["cve_mun"].map(mapa_crosswalk()).fillna(d["cve_mun"])
    salida = d.groupby(["cve_mun", "anio"], as_index=False)[SUMAS].sum()
    salida.to_parquet(SALIDA, index=False)
    log.info(
        "INE municipal: %d filas, %d municipios; por año %s",
        len(salida),
        salida["cve_mun"].nunique(),
        salida.groupby("anio")["cve_mun"].nunique().to_dict(),
    )

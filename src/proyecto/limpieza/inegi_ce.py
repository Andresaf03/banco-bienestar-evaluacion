"""Censos Económicos 2004–2024 por municipio -> `data/interim/inegi_ce_municipio.parquet`.

Cada zip por entidad (`data/raw/inegi_ce/<año>/`) trae la tabla `tr_ce_<ent>_<año>.csv` con claves
INEGI de entidad (`E03`) y municipio (`E04`). El total de cada municipio es la fila con
`CODIGO = "TOTAL DE SECTOR"` y sin sector ni estrato; los estratos de tamaño se omiten porque
vienen suprimidos por confidencialidad en muchos municipios (estrato 99).

Variables (nombres del diccionario del INEGI): `UE` unidades económicas, `H001A` personal ocupado,
`J000A` remuneraciones, `A111A` producción bruta, `A131A` valor agregado censal bruto y `Q000A`
acervo de activos fijos (millones de pesos corrientes). Los municipios creados después de 2010 se
colapsan en su municipio de origen (decisión P-7), para que los cinco cortes tengan las mismas
unidades.
"""

from __future__ import annotations

import logging
import zipfile

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM, RAW, fuentes

log = logging.getLogger(__name__)
SALIDA = INTERIM / "inegi_ce_municipio.parquet"
VARIABLES = {
    "UE": "ue",
    "H001A": "personal_ocupado",
    "J000A": "remuneraciones",
    "A111A": "produccion_bruta",
    "A131A": "vacb",
    "Q000A": "activos_fijos",
}


def _totales(ruta_zip) -> pd.DataFrame:
    with zipfile.ZipFile(ruta_zip) as z:
        nombre = next(n for n in z.namelist() if n.startswith("conjunto_de_datos/tr_"))
        d = pd.read_csv(
            z.open(nombre),
            dtype=str,
            encoding="latin-1",
            usecols=["E03", "E04", "SECTOR", "ID_ESTRATO", "CODIGO", *VARIABLES],
        )
    tot = d[d["E04"].notna() & d["SECTOR"].isna() & d["ID_ESTRATO"].isna()]
    tot = tot[tot["CODIGO"].str.strip().str.upper() == "TOTAL DE SECTOR"]
    if tot[["E03", "E04"]].duplicated().any():
        raise ValueError(f"{ruta_zip.name}: más de un total por municipio")
    salida = pd.DataFrame(
        {"cve_mun": tot["E03"].str.zfill(2) + tot["E04"].str.zfill(3)}
    ).reset_index(drop=True)
    for col, nuevo in VARIABLES.items():
        salida[nuevo] = pd.to_numeric(tot[col].to_numpy(), errors="coerce")
    return salida


def limpiar() -> None:
    cfg = fuentes()["inegi_ce"]
    partes = []
    for anio in cfg["anios"]:
        for ent in cfg["entidades"]:
            if ent == "nac":
                continue
            ruta = RAW / "inegi_ce" / str(anio) / f"conjunto_de_datos_ce_{ent}_{anio}_csv.zip"
            partes.append(_totales(ruta).assign(anio_censo=anio))
    d = pd.concat(partes, ignore_index=True)
    d["cve_mun"] = d["cve_mun"].map(mapa_crosswalk()).fillna(d["cve_mun"])
    columnas = list(VARIABLES.values())
    d = d.groupby(["cve_mun", "anio_censo"], as_index=False)[columnas].sum(min_count=1)
    d.to_parquet(SALIDA, index=False)
    por_anio = d.groupby("anio_censo").agg(municipios=("cve_mun", "nunique"), ue=("ue", "sum"))
    log.info("CE municipal: %d filas\n%s", len(d), por_anio.to_string())

"""EFIPEM municipal -> `data/interim/efipem_municipio.parquet` (fase 2).

Del zip de datos abiertos (`data/raw/efipem/`) se leen los años de `parametros.fase2.efipem.anios`
y, del tema "Ingresos", los renglones preregistrados (2026-10-07):

- `impuestos`: capítulo "Impuestos";
- `predial`: partida genérica "Impuesto predial";
- `derechos`: capítulo "Derechos";
- `ingresos_total`: tema "Total de ingresos" (marca que el municipio reportó ese año).

Montos en pesos corrientes. Un renglón ausente queda NaN (el municipio no lo desglosó), no cero.
Los municipios creados después de 2010 se colapsan en su municipio de origen (P-7) con
`sum(min_count=1)`.
"""

from __future__ import annotations

import logging
import zipfile

import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM, RAW, fuentes, parametros

log = logging.getLogger(__name__)

SALIDA = INTERIM / "efipem_municipio.parquet"
RENGLONES = {
    ("Capítulo", "impuestos"): "impuestos",
    ("Partida Genérica", "impuesto predial"): "predial",
    ("Capítulo", "derechos"): "derechos",
    ("Tema", "total de ingresos"): "ingresos_total",
}


def _normalizar(s: pd.Series) -> pd.Series:
    return s.str.replace("\xa0", " ", regex=False).str.strip()


def limpiar() -> None:
    url = fuentes()["efipem"]["url_archivo"]
    ruta = RAW / "efipem" / url.rsplit("/", 1)[-1]
    partes = []
    with zipfile.ZipFile(ruta) as z:
        for anio in parametros()["fase2"]["efipem"]["anios"]:
            nombre = f"conjunto_de_datos/efipem_municipal_anual_tr_cifra_{anio}.csv"
            d = pd.read_csv(z.open(nombre), dtype=str, encoding="utf-8")
            d = d[_normalizar(d["TEMA"]) == "Ingresos"]
            clave = list(
                zip(
                    _normalizar(d["CATEGORIA"]),
                    _normalizar(d["DESCRIPCION_CATEGORIA"]).str.lower(),
                    strict=True,
                )
            )
            d = d.assign(variable=[RENGLONES.get(k) for k in clave]).dropna(subset=["variable"])
            d["valor"] = pd.to_numeric(d["VALOR"], errors="coerce")
            ancho = d.pivot_table(index="CVEGEO", columns="variable", values="valor", aggfunc="sum")
            ancho = ancho.reindex(columns=list(RENGLONES.values())).reset_index()
            partes.append(ancho.rename(columns={"CVEGEO": "cve_mun"}).assign(anio=anio))
    f = pd.concat(partes, ignore_index=True)
    f["cve_mun"] = f["cve_mun"].str.zfill(5)
    f["cve_mun"] = f["cve_mun"].map(mapa_crosswalk()).fillna(f["cve_mun"])
    columnas = list(RENGLONES.values())
    f = f.groupby(["cve_mun", "anio"], as_index=False)[columnas].sum(min_count=1)
    f.to_parquet(SALIDA, index=False)
    log.info(
        "EFIPEM: %d filas; municipios con dato por año:\n%s",
        len(f),
        f.groupby("anio")[columnas].count().to_string(),
    )

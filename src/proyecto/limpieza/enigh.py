"""INEGI, ENIGH nueva serie 2016–2024 → hogar y municipio × ola (fase 4: C2, D y B3).

Adenda de datos en `docs/decisiones.md` (2026-10-14):

- **Municipio.** `ubica_geo` = entidad + municipio (5 dígitos), salvo en 2016, que trae 9 (con la
  localidad): se toman los primeros 5. Los municipios creados después de 2010 se colapsan en su
  padre (P-7).
- **Pago electrónico.** Un gasto de `gastoshogar` es electrónico si alguna de sus tres formas de
  pago es domiciliación (03), transferencia (04), crédito (05), débito (06) o pago móvil (09). El
  denominador es el gasto con al menos una forma de pago registrada (distinta de 00). El catálogo
  es idéntico en las cinco olas.
- **Codificación.** Los CSV vienen en UTF-8 con BOM o en latin-1 según la ola.

Salidas:
- `data/interim/enigh_hogar.parquet`: un renglón por hogar y ola.
- `data/interim/enigh_municipio.parquet`: promedios por municipio × ola, ponderados con el factor
  de expansión del hogar.
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.construccion.panel import mapa_crosswalk
from proyecto.utils.io import INTERIM, RAW

log = logging.getLogger(__name__)

RAIZ = RAW / "enigh"
SALIDA_HOGAR = INTERIM / "enigh_hogar.parquet"
SALIDA_MUNICIPIO = INTERIM / "enigh_municipio.parquet"
ELECTRONICAS = {3, 4, 5, 6, 9}
CONCENTRADO = [
    "folioviv",
    "foliohog",
    "ubica_geo",
    "factor",
    "upm",
    "est_dis",
    "tam_loc",
    "tot_integ",
    "ing_cor",
    "gasto_mon",
    "deposito",
    "bene_gob",
]
FORMAS = ["forma_pag1", "forma_pag2", "forma_pag3"]


def _leer(zf: zipfile.ZipFile, tabla: str, columnas: list[str]) -> pd.DataFrame:
    nombre = next(
        m
        for m in zf.namelist()
        if f"conjunto_de_datos/conjunto_de_datos_{tabla}" in m and m.endswith(".csv")
    )
    texto = {c: str for c in ("folioviv", "foliohog", "ubica_geo", "upm", "est_dis", "tam_loc")}
    for codificacion in ("utf-8-sig", "latin-1"):
        try:
            with zf.open(nombre) as f:
                return pd.read_csv(
                    f, usecols=columnas, encoding=codificacion, dtype=texto, low_memory=False
                )
        except UnicodeDecodeError:
            continue
    raise ValueError(f"no se pudo leer {nombre}")


def municipio(ubica_geo: pd.Series, anio: int) -> pd.Series:
    """Clave municipal de 5 dígitos (en 2016 `ubica_geo` incluye la localidad)."""
    largo = 9 if anio == 2016 else 5
    return ubica_geo.str.strip().str.zfill(largo).str[:5]


def gasto_por_forma(gastos: pd.DataFrame) -> pd.DataFrame:
    """Por hogar: gasto con forma de pago registrada, gasto pagado de forma electrónica y si hubo
    algún pago electrónico (`gastos`: `folioviv, foliohog, forma_pag1..3, gasto_tri`)."""
    formas = gastos[FORMAS].apply(pd.to_numeric, errors="coerce")
    conocida = formas.gt(0).any(axis=1)
    electronica = formas.isin(ELECTRONICAS).any(axis=1)
    monto = pd.to_numeric(gastos["gasto_tri"], errors="coerce").fillna(0)
    d = pd.DataFrame(
        {
            "folioviv": gastos["folioviv"],
            "foliohog": gastos["foliohog"],
            "gasto_forma": monto.where(conocida, 0),
            "gasto_electronico": monto.where(electronica, 0),
            "pago_electronico": electronica,
        }
    )
    return d.groupby(["folioviv", "foliohog"], as_index=False).agg(
        gasto_forma=("gasto_forma", "sum"),
        gasto_electronico=("gasto_electronico", "sum"),
        pago_electronico=("pago_electronico", "any"),
    )


def hogares(anio: int, ruta: Path) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as zf:
        c = _leer(zf, "concentradohogar", CONCENTRADO)
        g = _leer(zf, "gastoshogar", ["folioviv", "foliohog", *FORMAS, "gasto_tri"])
    h = c.merge(gasto_por_forma(g), on=["folioviv", "foliohog"], how="left")
    h["pago_electronico"] = h["pago_electronico"].fillna(False).astype(bool)
    h[["gasto_forma", "gasto_electronico"]] = h[["gasto_forma", "gasto_electronico"]].fillna(0)
    h["cve_mun"] = municipio(h["ubica_geo"], anio)
    h["cve_mun"] = h["cve_mun"].map(mapa_crosswalk()).fillna(h["cve_mun"])
    h["anio"] = anio
    return h.drop(columns="ubica_geo")


def agregar_municipio(h: pd.DataFrame) -> pd.DataFrame:
    """Promedios por municipio × ola, ponderados con el factor de expansión."""
    w = h["factor"]
    d = h.assign(
        w=w,
        w_ing=w * h["ing_cor"],
        w_gasto=w * h["gasto_mon"],
        w_integ=w * h["tot_integ"],
        w_forma=w * h["gasto_forma"],
        w_elec=w * h["gasto_electronico"],
        w_pago=w * h["pago_electronico"],
        w_dep=w * (h["deposito"] > 0),
        w_bene=w * (h["bene_gob"] > 0),
    )
    s = d.groupby(["cve_mun", "anio"]).agg(
        n_hogares=("w", "size"),
        w=("w", "sum"),
        w_ing=("w_ing", "sum"),
        w_gasto=("w_gasto", "sum"),
        w_integ=("w_integ", "sum"),
        w_forma=("w_forma", "sum"),
        w_elec=("w_elec", "sum"),
        w_pago=("w_pago", "sum"),
        w_dep=("w_dep", "sum"),
        w_bene=("w_bene", "sum"),
    )
    out = pd.DataFrame(
        {
            "n_hogares": s["n_hogares"],
            "pct_gasto_electronico": 100 * s["w_elec"] / s["w_forma"].replace(0, np.nan),
            "pct_hog_pago_electronico": 100 * s["w_pago"] / s["w"],
            "pct_hog_deposito": 100 * s["w_dep"] / s["w"],
            "pct_hog_bene_gob": 100 * s["w_bene"] / s["w"],
            "log_ing_cor_pc": np.log(s["w_ing"] / s["w_integ"]),
            "log_gasto_mon_pc": np.log(s["w_gasto"].where(s["w_gasto"] > 0) / s["w_integ"]),
        }
    )
    return out.reset_index()


def limpiar() -> list[Path]:
    partes = []
    for ruta in sorted(RAIZ.glob("*/*.zip")):
        anio = int(ruta.parent.name)
        h = hogares(anio, ruta)
        log.info(
            "ENIGH %d: %d hogares, %d municipios, %.1f%% con algún pago electrónico (ponderado)",
            anio,
            len(h),
            h["cve_mun"].nunique(),
            100 * np.average(h["pago_electronico"], weights=h["factor"]),
        )
        partes.append(h)
    if not partes:
        raise FileNotFoundError(f"sin zips de la ENIGH en {RAIZ}: correr `make descargar-fase4`")
    hogar = pd.concat(partes, ignore_index=True)
    hogar.to_parquet(SALIDA_HOGAR, index=False, compression="zstd")
    agregar_municipio(hogar).to_parquet(SALIDA_MUNICIPIO, index=False, compression="zstd")
    return [SALIDA_HOGAR, SALIDA_MUNICIPIO]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    limpiar()

"""Modelo Power Pivot del Portafolio de Información CNBV (2022-01 en adelante): fase 2, P-8.

Desde 2022 la CNBV ya no publica hojas planas mensuales del Portafolio: `BD_Operativa_2026MM.xlsx`
es un libro con un **modelo de datos** de Excel (Power Pivot). `docs/data_audit.md` lo daba por
ilegible, pero `xl/model/item.data` es un respaldo de Analysis Services sin la compresión XPress9 de
los .pbix y `pbixray` lo decodifica (preregistro de la fase 2, `docs/decisiones.md`, 2026-10-07).

La tabla de hechos `FT_datos` trae `periodo` (AAAAMM), `entidad` (clave de institución: Banco del
Bienestar 037166, Banjército 037019, …), `tipo_info_operativa` (31 = sucursales) e
`id_estado_municipio` (484 + entidad de 2 dígitos + municipio de 3: `48420001` → `20001`) con el
`dato`. Es municipal (no trae localidad).

Salidas:
- `data/interim/cnbv_portafolio_modelo.parquet`: la tabla de hechos completa en formato largo
  (`yyyymm`, `periodo` trimestral solo en meses de cierre, `cve_mun`, `institucion`, `tipo`,
  `descripcion_tipo`, `valor`).
- `data/interim/sucursales_bienestar_obs.parquet`: la serie del tratamiento con el Banco del
  Bienestar **observado** desde 2022T1 (`suc_bienestar_obs`), y la de siempre hasta 2021T4. Junto a
  la BDIF de banca de desarrollo para validar (`suc_bd_bdif`, `suc_bd_modelo`).
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from proyecto.utils.io import INTERIM, parametros, ruta
from proyecto.utils.periodos import yyyymm_a_periodo

log = logging.getLogger(__name__)

SALIDA_MODELO = INTERIM / "cnbv_portafolio_modelo.parquet"
SALIDA_SERIE = INTERIM / "sucursales_bienestar_obs.parquet"
MESES_CIERRE = ("03", "06", "09", "12")


def _cve_mun(id_estado_municipio: pd.Series) -> pd.Series:
    """`48420001` → `20001`: el prefijo 484 es el código de país; el resto, la clave INEGI.

    `-1` es la ubicación "Sin clasificar" del catálogo: queda como clave nula (no se asigna a ningún
    municipio) y se reporta en el log. Cualquier otro formato es un error.
    """
    texto = id_estado_municipio.astype("int64").astype(str)
    sin_clasificar = texto == "-1"
    valido = texto.str.startswith("484") & texto.str.len().eq(8)
    if not (valido | sin_clasificar).all():
        raise ValueError("id_estado_municipio con formato inesperado (se esperaba 484EEMMM o -1)")
    return texto.str[3:].where(valido).astype("string")


def leer_modelo(archivo: Path) -> pd.DataFrame:
    """Decodifica el modelo de datos y devuelve la tabla de hechos con sus etiquetas."""
    from pbixray import PBIXRay

    with PBIXRay(str(archivo)) as m:
        ft = m.get_table("FT_datos")
        inst = m.get_table("LT_instituciones")[["entidad", "nombre_entidad"]]
        tipos = m.get_table("LT_tipo_info_operativa")[
            ["tipo_info_operativa", "descripcion_tipo_info_operativa"]
        ]
    d = pd.DataFrame(
        {
            "yyyymm": ft["periodo"].astype("int64").astype(str),
            "cve_mun": _cve_mun(ft["id_estado_municipio"]),
            "institucion": ft["entidad"].astype("string"),
            "tipo": ft["tipo_info_operativa"].astype("int64"),
            "valor": pd.to_numeric(ft["dato"]),
        }
    )
    d = d.merge(inst.rename(columns={"entidad": "institucion"}), on="institucion", how="left")
    d = d.merge(
        tipos.rename(
            columns={
                "tipo_info_operativa": "tipo",
                "descripcion_tipo_info_operativa": "descripcion_tipo",
            }
        ),
        on="tipo",
        how="left",
    )
    cierre = d["yyyymm"].str[4:].isin(MESES_CIERRE)
    d["periodo"] = (
        d["yyyymm"]
        .where(cierre)
        .map(lambda m: yyyymm_a_periodo(m) if isinstance(m, str) else pd.NA)
    )
    return d


def _serie_observada(modelo: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Sucursales por municipio y trimestre: Banco del Bienestar observado desde `cfg['desde']`."""
    suc = modelo[(modelo["tipo"] == cfg["tipo_sucursales"]) & modelo["periodo"].notna()]
    por_inst = suc.pivot_table(
        index=["cve_mun", "periodo"], columns="institucion", values="valor", aggfunc="sum"
    )
    bb = por_inst.get(cfg["clave_bienestar"], pd.Series(dtype=float)).fillna(0)
    banj = por_inst.get(cfg["clave_banjercito"], pd.Series(dtype=float)).fillna(0)
    obs = pd.DataFrame({"suc_bienestar_modelo": bb, "suc_banjercito_modelo": banj})
    obs["suc_bd_modelo"] = obs["suc_bienestar_modelo"] + obs["suc_banjercito_modelo"]
    return obs.reset_index()


def limpiar() -> Path:
    cfg = parametros()["fase2"]["portafolio_modelo"]
    modelo = leer_modelo(ruta(cfg["archivo"]))
    modelo.to_parquet(SALIDA_MODELO, index=False)
    sin_mun = modelo["cve_mun"].isna()
    log.info(
        "ubicación 'Sin clasificar': %d filas; sucursales-mes del Banco del Bienestar sin municipio: %d",
        int(sin_mun.sum()),
        int(
            modelo.loc[
                sin_mun
                & (modelo["institucion"] == cfg["clave_bienestar"])
                & (modelo["tipo"] == cfg["tipo_sucursales"]),
                "valor",
            ].sum()
        ),
    )
    modelo = modelo[~sin_mun]
    log.info(
        "modelo Portafolio: %d filas, %s–%s, %d municipios, instituciones %s",
        len(modelo),
        modelo["yyyymm"].min(),
        modelo["yyyymm"].max(),
        modelo["cve_mun"].nunique(),
        ", ".join(sorted(modelo["nombre_entidad"].dropna().unique())),
    )

    base = pd.read_parquet(INTERIM / "sucursales_bienestar.parquet")
    obs = _serie_observada(modelo, cfg)
    obs = obs[obs["periodo"] <= base["periodo"].max()]
    # `outer`: el modelo trae sucursales en municipios nuevos (p. ej. 12082 Las Vigas desde 2022T3)
    # que la BDIF todavía no separa de su municipio de origen en esos trimestres. Con `left` se
    # perdían (30 sucursal-trimestres en 7 municipios; revisión del 2026-10-08). Esas filas quedan
    # sin dato de la BDIF y `_tratamiento_trimestral` las suma al municipio estable (P-7).
    serie = base.merge(obs, on=["cve_mun", "periodo"], how="outer")
    solo_modelo = serie["suc_bd_bdif"].isna() & serie["suc_bienestar_modelo"].fillna(0).gt(0)
    log.info(
        "sucursal-trimestres del Banco del Bienestar solo en el modelo (municipios nuevos): %d en %d "
        "municipios",
        int(serie.loc[solo_modelo, "suc_bienestar_modelo"].sum()),
        serie.loc[solo_modelo, "cve_mun"].nunique(),
    )
    desde = serie["periodo"] >= cfg["desde"]
    # Un municipio sin filas en el modelo en un trimestre observado no tiene sucursales de banca de
    # desarrollo ese trimestre (el modelo solo trae celdas con dato).
    for c in ("suc_bienestar_modelo", "suc_banjercito_modelo", "suc_bd_modelo"):
        serie.loc[desde, c] = serie.loc[desde, c].fillna(0)
    serie["suc_bienestar_obs"] = serie["suc_bienestar"].where(~desde, serie["suc_bienestar_modelo"])
    serie["fuente_obs"] = desde.map({True: "modelo_portafolio", False: "serie_base"})
    serie.to_parquet(SALIDA_SERIE, index=False)

    # La validación solo compara filas con dato en las dos fuentes.
    val = serie[desde & serie["periodo"].le("2025Q4") & serie["suc_bd_bdif"].notna()]
    coincide = (val["suc_bd_bdif"] == val["suc_bd_modelo"]).mean()
    log.info(
        "validación 2022T1–2025T4: BB + Banjército (modelo) = banca de desarrollo (BDIF) en %.1f%% "
        "de %d municipio-trimestres; Banjército observado en %d municipios (2025T4)",
        100 * coincide,
        len(val),
        int((val.loc[val["periodo"] == "2025Q4", "suc_banjercito_modelo"] > 0).sum()),
    )
    return SALIDA_SERIE

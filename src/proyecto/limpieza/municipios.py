"""Catálogo de municipios y crosswalk hacia unidades estables.

Fuentes que se combinan:
- Marco Geoestadístico dic. 2024 (`00mun.shp`, 2,478 polígonos) y su catálogo CSV.
- Catálogo Único de Claves (wscatgeo `mgem`): población censal 2020 y cabecera.
- Presencia por trimestre en la BDIF (2016T1–2025T4).
- ITER 2010 y 2020 (totales municipales) y CONAPO IMM 2010/2015/2020.

Salidas:
- `data/interim/municipios.parquet`: una fila por clave observada en cualquier fuente, con
  nombre, entidad, banderas de presencia, primer y último trimestre en la BDIF y una fecha de
  alta estimada (primer trimestre BDIF en que aparece si no estaba en 2016T1).
- `data/interim/crosswalk_municipios.parquet`: `cve_mun` (clave vigente 2024) -> `cve_estable`
  (clave del municipio del que se desprendió, vigente en 2010). Los municipios creados después
  de 2010 se asignan a su "padre" por cruce espacial: las localidades del ITER 2010 (con la
  clave municipal de 2010 y coordenadas) se intersectan con los polígonos 2024; el padre es la
  clave 2010 con más población dentro del polígono nuevo. `share_padre` < 0.9 marca casos con
  más de un donante. Es el análogo de las áreas mínimas comparables (AMC).
- `docs/diccionarios/crosswalk_municipios.md`: tabla con cada caso.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

from proyecto.utils.claves import combinar, normalizar_serie
from proyecto.utils.io import DICCIONARIOS, INTERIM, MANUAL, RAW

log = logging.getLogger(__name__)

RUTA_MUN_SHP = RAW / "inegi_mg" / "mg_2024_integrado" / "conjunto_de_datos" / "00mun.shp"
RUTA_CATALOGO_CSV = (
    RAW / "inegi_mg" / "mg_2024_integrado" / "catalogos" / "áreas_geoestadísticas_municipales.csv"
)
RUTA_WSCATGEO = RAW / "inegi_mg" / "wscatgeo" / "mgem_por_entidad.json"
SALIDA_MUN = INTERIM / "municipios.parquet"
SALIDA_CW = INTERIM / "crosswalk_municipios.parquet"
SALIDA_DOC = DICCIONARIOS / "crosswalk_municipios.md"
UMBRAL_SHARE = 0.9


def poligonos_2024() -> gpd.GeoDataFrame:
    g = gpd.read_file(RUTA_MUN_SHP)
    g = g.rename(columns={"CVEGEO": "cve_mun", "CVE_ENT": "cve_ent", "NOMGEO": "nom_mun"})
    g["cve_mun"] = normalizar_serie(g["cve_mun"])
    return g[["cve_mun", "cve_ent", "nom_mun", "geometry"]]


def catalogo_csv_2024() -> pd.DataFrame:
    df = pd.read_csv(RUTA_CATALOGO_CSV, encoding="latin-1", skiprows=2, dtype=str)
    df.columns = ["cve_ent", "nom_ent", "cve_mun3", "nom_mun"]
    df["cve_mun"] = combinar(df["cve_ent"], df["cve_mun3"])
    return df[["cve_mun", "nom_ent", "nom_mun"]]


def catalogo_wscatgeo() -> pd.DataFrame:
    with open(RUTA_WSCATGEO, encoding="utf-8") as f:
        datos = json.load(f)["datos"]
    df = pd.DataFrame(datos)
    df["cve_mun"] = normalizar_serie(df["cvegeo"])
    df["pob_total_2020"] = pd.to_numeric(df["pob_total"], errors="coerce")
    return df[["cve_mun", "nomgeo", "nom_cab", "pob_total_2020"]].rename(
        columns={"nomgeo": "nom_mun_wscatgeo"}
    )


def presencia_bdif() -> pd.DataFrame:
    pob = pd.read_parquet(
        INTERIM / "cnbv_bdif_poblacion.parquet",
        columns=["cve_mun", "periodo", "t", "nom_mun", "nom_ent"],
    )
    g = pob.groupby("cve_mun")
    out = g.agg(
        bdif_desde=("periodo", "min"),
        bdif_hasta=("periodo", "max"),
        bdif_t_min=("t", "min"),
        bdif_t_max=("t", "max"),
        bdif_n_trimestres=("periodo", "nunique"),
        nom_mun_bdif=("nom_mun", "last"),
        nom_ent_bdif=("nom_ent", "last"),
    ).reset_index()
    n_total = pob["periodo"].nunique()
    out["bdif_completo"] = out["bdif_n_trimestres"] == n_total
    return out


def _claves_de(ruta: Path, col_ent: str, col_mun: str | None = None, **kw) -> set[str]:
    df = pd.read_csv(ruta, dtype=str, **kw)
    df.columns = [c.strip().lstrip("﻿") for c in df.columns]
    if col_mun is None:
        return set(normalizar_serie(df[col_ent]).dropna())
    return set(combinar(df[col_ent], df[col_mun]).dropna())


def claves_otras_fuentes() -> dict[str, set[str]]:
    iter2010 = set(
        pd.read_parquet(INTERIM / "inegi_censo_2010.parquet", columns=["cve_mun"])["cve_mun"]
    )
    iter2020 = set(
        pd.read_parquet(INTERIM / "inegi_censo_2020.parquet", columns=["cve_mun"])["cve_mun"]
    )
    marg = MANUAL / "conapo_marginacion"
    return {
        "iter2010": iter2010,
        "iter2020": iter2020,
        "imm2010": _claves_de(marg / "imm_dp2_2010.csv", "CVE_MUN"),
        "imm2015": _claves_de(marg / "imm_dp2_2015.csv", "CVE_MUN", encoding="utf-8-sig"),
        "imm2020": _claves_de(marg / "imm_2020.csv", "CVE_MUN"),
    }


def construir_catalogo() -> pd.DataFrame:
    mg = poligonos_2024().drop(columns="geometry")
    csv = catalogo_csv_2024()
    ws = catalogo_wscatgeo()
    bdif = presencia_bdif()
    otras = claves_otras_fuentes()

    claves = (
        set(mg["cve_mun"])
        | set(csv["cve_mun"])
        | set(bdif["cve_mun"])
        | set().union(*otras.values())
    )
    cat = pd.DataFrame({"cve_mun": sorted(claves)})
    cat["cve_ent"] = cat["cve_mun"].str[:2]
    cat = (
        cat.merge(csv, on="cve_mun", how="left")
        .merge(ws, on="cve_mun", how="left")
        .merge(bdif, on="cve_mun", how="left")
    )
    cat["nom_mun"] = cat["nom_mun"].fillna(cat["nom_mun_wscatgeo"]).fillna(cat["nom_mun_bdif"])
    cat["nom_ent"] = cat["nom_ent"].fillna(cat["nom_ent_bdif"])
    cat["en_mg2024"] = cat["cve_mun"].isin(set(mg["cve_mun"]))
    for k, v in otras.items():
        cat[f"en_{k}"] = cat["cve_mun"].isin(v)
    cat["en_bdif"] = cat["bdif_n_trimestres"].notna()
    cat["bdif_completo"] = cat["bdif_completo"].fillna(False).astype(bool)
    primer_bdif = bdif["bdif_desde"].min()
    cat["alta_estimada"] = cat["bdif_desde"].where(cat["bdif_desde"] != primer_bdif)
    cat.loc[
        ~cat["en_iter2010"] & cat["alta_estimada"].isna() & ~cat["en_bdif"], "alta_estimada"
    ] = "posterior a 2010, sin fecha en BDIF"
    cat["baja_estimada"] = cat["bdif_hasta"].where(
        cat["en_bdif"] & (cat["bdif_hasta"] != bdif["bdif_hasta"].max()) & ~cat["en_mg2024"]
    )
    cols = [
        "cve_mun",
        "cve_ent",
        "nom_mun",
        "nom_ent",
        "nom_cab",
        "pob_total_2020",
        "en_mg2024",
        "en_iter2010",
        "en_iter2020",
        "en_imm2010",
        "en_imm2015",
        "en_imm2020",
        "en_bdif",
        "bdif_desde",
        "bdif_hasta",
        "bdif_t_min",
        "bdif_t_max",
        "bdif_n_trimestres",
        "bdif_completo",
        "alta_estimada",
        "baja_estimada",
    ]
    return cat[cols]


def construir_crosswalk(cat: pd.DataFrame) -> pd.DataFrame:
    """hijo -> padre por cruce espacial de localidades 2010 contra polígonos 2024."""
    pol = poligonos_2024()
    loc = pd.read_parquet(INTERIM / "inegi_censo_localidades_2010.parquet")
    loc = loc.dropna(subset=["lon", "lat"])
    pts = gpd.GeoDataFrame(
        loc, geometry=gpd.points_from_xy(loc["lon"], loc["lat"]), crs="EPSG:4326"
    ).to_crs(pol.crs)
    cruce = gpd.sjoin(
        pts,
        pol[["cve_mun", "geometry"]].rename(columns={"cve_mun": "cve_mun_2024"}),
        how="inner",
        predicate="within",
    )
    cruce["pobtot"] = cruce["pobtot"].fillna(0)
    resumen = (
        cruce.groupby(["cve_mun_2024", "cve_mun"])
        .agg(n_localidades=("cve_loc", "size"), pob_2010=("pobtot", "sum"))
        .reset_index()
        .rename(columns={"cve_mun": "cve_mun_2010"})
    )
    total = resumen.groupby("cve_mun_2024")["pob_2010"].transform("sum")
    resumen["share"] = resumen["pob_2010"] / total.where(total > 0)
    # padre = clave 2010 con más población dentro del polígono 2024
    padre = resumen.sort_values(
        ["cve_mun_2024", "pob_2010", "n_localidades"], ascending=[True, False, False]
    ).drop_duplicates("cve_mun_2024")
    padre = padre.rename(
        columns={
            "cve_mun_2010": "padre_espacial",
            "share": "share_padre",
            "n_localidades": "n_loc_padre",
            "pob_2010": "pob_2010_padre",
        }
    )

    cw = (
        cat[cat["en_mg2024"]][
            ["cve_mun", "nom_mun", "cve_ent", "en_iter2010", "bdif_desde", "alta_estimada"]
        ]
        .merge(
            padre[
                ["cve_mun_2024", "padre_espacial", "share_padre", "n_loc_padre", "pob_2010_padre"]
            ],
            left_on="cve_mun",
            right_on="cve_mun_2024",
            how="left",
        )
        .drop(columns="cve_mun_2024")
    )
    es_hijo = ~cw["en_iter2010"]
    cw["cve_estable"] = cw["cve_mun"].where(~es_hijo, cw["padre_espacial"])
    cw["tipo"] = "estable"
    cw.loc[es_hijo, "tipo"] = "hijo"
    donantes = set(cw.loc[es_hijo, "cve_estable"].dropna())
    cw.loc[cw["cve_mun"].isin(donantes), "tipo"] = "padre_donante"
    cw["revisar"] = es_hijo & ((cw["share_padre"] < UMBRAL_SHARE) | cw["padre_espacial"].isna())
    # municipios 2010 que ya no existen en 2024 (bajas): se agregan mapeados a sí mismos, marcados
    bajas = cat[cat["en_iter2010"] & ~cat["en_mg2024"]]
    if not bajas.empty:
        extra = bajas[["cve_mun", "nom_mun", "cve_ent"]].assign(
            cve_estable=bajas["cve_mun"], tipo="baja_sin_poligono_2024", revisar=True
        )
        cw = pd.concat([cw, extra], ignore_index=True)
    # detalle de donantes secundarios para los hijos
    secundarios = resumen[resumen["cve_mun_2024"].isin(cw.loc[es_hijo, "cve_mun"])].merge(
        padre[["cve_mun_2024", "padre_espacial"]], on="cve_mun_2024"
    )
    secundarios = secundarios[secundarios["cve_mun_2010"] != secundarios["padre_espacial"]]
    otros = secundarios.groupby("cve_mun_2024").apply(
        lambda d: "; ".join(
            f"{r.cve_mun_2010} ({r.share:.1%}, {r.n_localidades} loc)" for r in d.itertuples()
        ),
        include_groups=False,
    )
    cw["otros_donantes_2010"] = cw["cve_mun"].map(otros)
    cols = [
        "cve_mun",
        "nom_mun",
        "cve_ent",
        "cve_estable",
        "tipo",
        "en_iter2010",
        "bdif_desde",
        "alta_estimada",
        "padre_espacial",
        "share_padre",
        "n_loc_padre",
        "pob_2010_padre",
        "otros_donantes_2010",
        "revisar",
    ]
    return cw[cols].sort_values(["tipo", "cve_mun"]).reset_index(drop=True)


def documentar(cat: pd.DataFrame, cw: pd.DataFrame) -> None:
    hijos = cw[cw["tipo"] == "hijo"]
    donantes = cw[cw["tipo"] == "padre_donante"]
    bajas = cw[cw["tipo"].str.startswith("baja")]
    sin_bdif = cat[cat["en_mg2024"] & ~cat["en_bdif"]]
    incompletos = cat[cat["en_bdif"] & ~cat["bdif_completo"]]
    lineas = [
        "# Crosswalk de municipios (2010 → 2024)\n",
        "Generado por `proyecto.limpieza.municipios`. Ver docstring del módulo para el método.\n",
        f"- Municipios en el Marco Geoestadístico 2024: **{cat['en_mg2024'].sum()}**",
        f"- Municipios en el ITER 2010: **{cat['en_iter2010'].sum()}**; en el ITER 2020: **{cat['en_iter2020'].sum()}**",
        f"- Municipios observados en la BDIF (2016T1–2025T4): **{cat['en_bdif'].sum()}**; con los 40 trimestres: **{cat['bdif_completo'].sum()}**",
        f"- Municipios creados después de 2010 (hijos): **{len(hijos)}**; padres donantes: **{len(donantes)}**; bajas sin polígono 2024: **{len(bajas)}**",
        f"- Hijos con `share_padre` < {UMBRAL_SHARE:.0%} o sin padre espacial (revisar a mano): **{int(hijos['revisar'].sum())}**\n",
        "## Municipios creados después de 2010 (hijo → padre)\n",
        "| cve_mun | nombre | padre (2010) | share padre | loc. 2010 en polígono | otros donantes | primer trimestre BDIF | revisar |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in hijos.itertuples():
        share = "" if pd.isna(r.share_padre) else f"{r.share_padre:.1%}"
        lineas.append(
            f"| {r.cve_mun} | {r.nom_mun} | {r.cve_estable or ''} | {share} | {'' if pd.isna(r.n_loc_padre) else int(r.n_loc_padre)} | {'' if pd.isna(r.otros_donantes_2010) else r.otros_donantes_2010} | {r.bdif_desde or 'no aparece'} | {'sí' if r.revisar else ''} |"
        )
    lineas += ["\n## Padres donantes\n", "| cve_mun | nombre | hijos |", "|---|---|---|"]
    for r in donantes.itertuples():
        h = hijos[hijos["cve_estable"] == r.cve_mun]["cve_mun"].tolist()
        lineas.append(f"| {r.cve_mun} | {r.nom_mun} | {', '.join(h)} |")
    lineas += ["\n## Bajas (en 2010, sin polígono en 2024)\n"]
    lineas += [f"- {r.cve_mun} {r.nom_mun}" for r in bajas.itertuples()] or ["- ninguna"]
    lineas += ["\n## Municipios del MG 2024 que no aparecen en la BDIF\n"]
    lineas += [f"- {r.cve_mun} {r.nom_mun} ({r.nom_ent})" for r in sin_bdif.itertuples()] or [
        "- ninguno"
    ]
    lineas += [
        "\n## Municipios con trimestres faltantes en la BDIF\n",
        "| cve_mun | nombre | desde | hasta | trimestres | en MG 2024 |",
        "|---|---|---|---|---|---|",
    ]
    lineas += [
        f"| {r.cve_mun} | {r.nom_mun} | {r.bdif_desde} | {r.bdif_hasta} | {int(r.bdif_n_trimestres)} | {'sí' if r.en_mg2024 else 'no'} |"
        for r in incompletos.itertuples()
    ]
    lineas += [
        "\n## Uso previsto\n",
        "Para el panel se propone colapsar cada hijo con su padre (`cve_estable`) sumando conteos en todos los",
        "trimestres, de modo que la unidad sea estable 2016–2025. Decisión pendiente: ver `docs/decisiones.md`.",
    ]
    SALIDA_DOC.parent.mkdir(parents=True, exist_ok=True)
    SALIDA_DOC.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def limpiar() -> Path:
    cat = construir_catalogo()
    cw = construir_crosswalk(cat)
    cat.to_parquet(SALIDA_MUN, index=False)
    cw.to_parquet(SALIDA_CW, index=False)
    documentar(cat, cw)
    log.info(
        "municipios: %d claves; crosswalk: %d filas (%d hijos)",
        len(cat),
        len(cw),
        (cw["tipo"] == "hijo").sum(),
    )
    return SALIDA_MUN

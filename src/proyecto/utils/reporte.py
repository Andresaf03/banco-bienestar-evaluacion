"""Consolida las salidas de estimación en el reporte de resultados.

Lee `outputs/tablas/tabla_final.csv` (la deja `analisis/07_inferencia.R`) y las tablas de
robustez, diseños, heterogeneidad, balance y medición del DENUE que dejan los scripts de R, y
escribe `entregables/04_final/resultados_preliminares.md` con:

- la especificación principal preregistrada, con potencia, equivalencia, inferencia múltiple y la
  auditoría de pre-tendencias de cada especificación;
- la evidencia de medición del DENUE que justifica el diseño entre actualizaciones;
- las secundarias, el contraste de diseños, los diseños alternativos (DiD apilado y decaimiento
  espacial), la intensidad municipal del tratamiento, la robustez, la heterogeneidad y el balance;
- la fase 2 (fuentes nuevas, preregistro del 2026-10-07) en una sección aparte, al final: sus
  robusteces y HonestDiD no se mezclan con los de la especificación principal.

No estima nada: solo ordena lo que ya se corrió. Con `PROYECTO_SALIDAS` escribe el reporte junto a
esas salidas y no en entregables/ (pruebas de humo).
"""

from __future__ import annotations

import logging
import os
from datetime import date
from pathlib import Path

import pandas as pd

from proyecto.utils.io import SALIDAS, TABLAS, parametros, ruta

log = logging.getLogger(__name__)

SALIDA = (
    SALIDAS / "resultados_preliminares.md"
    if os.environ.get("PROYECTO_SALIDAS")
    else ruta("entregables", "04_final", "resultados_preliminares.md")
)
NOMBRE_PANEL = {
    "localidad": "Localidad",
    "municipio": "Municipio (semestral)",
    "municipio_trim": "Municipio (trimestral, BDIF)",
}
# Paneles de la fase 2 (`construccion/panel_fase2.py`): sus `rob_*` van a su propia sección.
PANELES_FASE2 = {
    "municipio_trim_obs",
    "municipio_eic",
    "localidad_viirs",
    "municipio_efipem",
    "municipio_enoe",
}
NOMBRE_DISENO = {
    "actualizaciones": "entre actualizaciones",
    "escalonado": "escalonado",
    "completo": "panel completo",
}


def _md(df: pd.DataFrame, decimales: int = 3) -> str:
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:,.{decimales}f}")
    cols = [str(c) for c in d.columns]
    filas = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in d.itertuples(index=False):
        filas.append("| " + " | ".join("" if v is None or v is pd.NA else str(v) for v in r) + " |")
    return "\n".join(filas)


def _leer(patron: str) -> pd.DataFrame:
    archivos = sorted(TABLAS.glob(patron))
    if not archivos:
        return pd.DataFrame()
    return pd.concat([pd.read_csv(a) for a in archivos], ignore_index=True)


def _estrellas(p: float) -> str:
    if pd.isna(p):
        return ""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def _tabla_resultados(t: pd.DataFrame) -> pd.DataFrame:
    """Columnas del reporte: estimando, precisión, potencia, inferencia múltiple y pre-tendencias."""
    salida = pd.DataFrame(
        {
            "panel": t["panel"].map(NOMBRE_PANEL).fillna(t["panel"]),
            "diseño": t["diseno"].map(NOMBRE_DISENO).fillna(t["diseno"]),
            "resultado": t["resultado"],
            "ATT": t["valor"],
            "ee": t["ee"],
            "sig": t["p"].map(_estrellas),
            "efecto %": t["efecto_pct"],
            "MDE80 %": t["mde80_pct"],
            "cota TOST %": t["cota_equivalencia_pct"],
            "previos sig.": t["pre_sig"].astype("Int64").astype(str)
            + "/"
            + t["pre_n"].astype("Int64").astype(str),
            "Wald previa p": t["pre_wald_p"],
            "placebo 2019S2": t.get("placebo"),
            "q BH": t["q_bh"],
        }
    )
    if "p_rw" in t.columns:
        salida["p Romano–Wolf"] = t["p_rw"]
    if "honest_lb_m1" in t.columns:
        salida["HonestDiD M̄=1"] = [
            "" if pd.isna(a) else f"[{a:,.3f}, {b:,.3f}]"
            for a, b in zip(t["honest_lb_m1"], t["honest_ub_m1"], strict=True)
        ]
    salida["n trat./ctrl."] = (
        t["n_tratadas"].astype("Int64").astype(str)
        + "/"
        + t["n_controles"].astype("Int64").astype(str)
    )
    return salida


def _seccion_alternativos() -> list[str]:
    """Diseños alternativos (08_disenos_alternativos.R, preregistrados el 2026-10-02) y la intensidad
    municipal del tratamiento (01_descriptivos.R)."""
    L: list[str] = []
    apilado = _leer("apilado_resumen.csv")
    if not apilado.empty:
        cols = [
            "resultado",
            "controles",
            "pilas",
            "tratadas",
            "att",
            "ee",
            "efecto_pct",
            "cota_equivalencia_pct",
            "pre_sig",
            "pre_n",
            "pre_wald_p",
            "cs_att",
            "cs_ee",
            "cs_efecto_pct",
        ]
        L += [
            "## DiD apilado (Wing, Freedman y Hollingsworth 2024)\n",
            "Municipio trimestral 2019T1–2025T4; una pila por cohorte con ventana de evento "
            "e ∈ [−8, 7] y controles limpios ponderados; efectos fijos unidad × pila y evento; sin "
            "covariables; ee agrupado por municipio. *att* = promedio de δ_0…δ_7; la pre-prueba es "
            "la Wald de δ_−8…δ_−2. *cs_* es la estimación de Callaway y Sant'Anna de referencia.\n",
            _md(apilado[[c for c in cols if c in apilado.columns]]),
            "",
        ]
    dec = _leer("decaimiento_*.csv")
    if not dec.empty:
        bandas = dec[dec["banda"].notna()]
        difs = dec[dec["contraste"].notna()] if "contraste" in dec.columns else pd.DataFrame()
        L += [
            "## Decaimiento espacial (DENUE, entre actualizaciones)\n",
            "ATT(17, 18) por banda de distancia a la sucursal más cercana, cada banda contra los "
            "mismos controles a ≥10 km; la sucursal propia es la especificación principal. Los "
            "contrastes están en % de la media previa de cada banda, con covarianza agrupada por "
            "municipio.\n",
            _md(
                bandas[
                    [
                        "resultado",
                        "banda",
                        "tratadas",
                        "att",
                        "ee",
                        "media_base",
                        "efecto_pct",
                        "pre_sig",
                        "pre_n",
                        "pre_wald_p",
                        "placebo",
                        "placebo_ee",
                    ]
                ]
            ),
            "",
        ]
        if not difs.empty:
            L += [_md(difs[["resultado", "contraste", "dif_pct", "ee_dif_pct", "p_dif"]]), ""]
    reg = _leer("regimen_*.csv")
    if not reg.empty:
        L += [
            "## Régimen censal (exploratorio, no preregistrado)\n",
            "Especificación principal del DENUE estimada dentro de cada régimen de levantamiento de "
            "los Censos Económicos: recorrido total (cabecera o 2,500+ habitantes) y muestra rural. "
            "Las diferencias están en % de la media previa de cada grupo.\n",
            _md(
                reg[
                    [
                        c
                        for c in [
                            "resultado",
                            "regimen",
                            "banda",
                            "contraste",
                            "tratadas",
                            "controles",
                            "att",
                            "ee",
                            "efecto_pct",
                            "pre_wald_p",
                            "placebo",
                            "placebo_ee",
                            "dif_pct",
                            "ee_dif_pct",
                            "p_dif",
                        ]
                        if c in reg.columns
                    ]
                ]
            ),
            "",
        ]
    intensidad = _leer("desc_intensidad_municipal.csv")
    if not intensidad.empty:
        L += [
            "## Intensidad del tratamiento municipal (descriptivo)\n",
            "Sucursales del Banco del Bienestar (netas de Banjército) por municipio que abrió en la "
            "ventana, al cierre de 2024T4.\n",
            _md(intensidad, decimales=2),
            "",
        ]
    return L


def _sin_fase2(d: pd.DataFrame) -> pd.DataFrame:
    return d[~d["panel"].isin(PANELES_FASE2)] if "panel" in d.columns else d


def _seccion_fase2() -> list[str]:
    """Fase 2 (analisis/10_fase2.R): resumen con Romano–Wolf y BH de la fase, tratamiento observado,
    decaimiento de la luz nocturna, dosis y heterogeneidad de la EIC, robustez y HonestDiD."""
    resumen = _leer("fase2_resumen.csv")
    if resumen.empty:
        return []
    L = [
        "# Fase 2: fuentes nuevas (preregistro del 2026-10-07)\n",
        "Fuera de la maestra y de las familias de la especificación principal; criterios iguales. "
        "En los resultados en logaritmo, *efecto %* y *cota* están en puntos log × 100.\n",
    ]
    cols = [
        "familia",
        "resultado",
        "n_tratadas",
        "n_controles",
        "valor",
        "ee",
        "efecto_pct",
        "cota_equivalencia_pct",
        "pre_sig",
        "pre_n",
        "pre_wald_p",
        "p",
        "p_rw",
        "q_bh_fase2",
        "lectura",
    ]
    resumen = resumen.sort_values(["familia", "resultado"])
    L += ["## Resumen de la fase 2\n", _md(resumen[[c for c in cols if c in resumen]]), ""]
    secciones = [
        ("fase2_tratamiento_obs.csv", "Tratamiento con el Banco del Bienestar observado (P-8)"),
        ("fase2_decaimiento_viirs_*.csv", "Luz nocturna por banda de distancia (puntos log × 100)"),
        ("fase2_rob_extra_viirs_*.csv", "Luz nocturna: régimen censal y grupos de control"),
        (
            "fase2_desc_viirs_ruptura.csv",
            "Luz nocturna: cambio anual de log(1 + luz) en los controles por decil de brillo de 2021",
        ),
        ("fase2_dosis_eic_*.csv", "EIC: dosis (aperturas tempranas contra tardías)"),
        (
            "fase2_het_eic_*.csv",
            "EIC: desierto bancario (el grupo con banca previa tiene solo 21 controles)",
        ),
    ]
    for patron, titulo in secciones:
        d = _leer(patron)
        if not d.empty:
            L += [f"## {titulo}\n", _md(d), ""]
    rob = _leer("rob_[!dh]*.csv")
    if not rob.empty and "panel" in rob.columns:
        rob = rob[rob["panel"].isin(PANELES_FASE2)]
        cols = [
            "panel",
            "resultado",
            "variante",
            "tratadas",
            "controles",
            "att",
            "ee",
            "pre_sig",
            "pre_n",
            "pre_wald_p",
        ]
        L += ["## Robustez de la fase 2\n", _md(rob[[c for c in cols if c in rob]]), ""]
    honest = _leer("rob_honest_*.csv")
    if not honest.empty and "panel" in honest.columns:
        L += ["## HonestDiD de la fase 2\n", _md(honest[honest["panel"].isin(PANELES_FASE2)]), ""]
    return L


def generar() -> Path:
    ruta_final = TABLAS / "tabla_final.csv"
    if not ruta_final.exists():
        raise FileNotFoundError("falta tabla_final.csv; corre `make estimar` y `make inferencia`")
    final = pd.read_csv(ruta_final)
    sesoi = parametros()["estimacion"]["sesoi_pct"]

    L = [
        "# Resultados\n",
        f"Generado por `python -m proyecto.utils.reporte` el {date.today().isoformat()}. La "
        "especificación principal, las familias de inferencia múltiple y el umbral de equivalencia "
        "están preregistrados en `docs/decisiones.md` (2026-09-29).\n",
        "Convenciones: ATT de Callaway y Sant'Anna (DR) con error estándar agrupado por municipio "
        "(Liang–Zeger sobre la función de influencia). *Efecto %*, *MDE80 %* y *cota TOST %* están "
        "en porcentaje de la media de las tratadas en su último periodo previo. *Cota TOST* es el "
        "mayor valor absoluto del IC al 90%: si queda por debajo de "
        f"{sesoi}% y el ATT no es significativo, el nulo es informativo. *Previos sig.* cuenta los "
        "coeficientes previos significativos al 5%; *Wald previa* prueba que todos sean cero; el "
        "*placebo 2019S2* es el salto de la actualización integral previa a todo tratamiento. "
        "Significancia: * 10%, ** 5%, *** 1%.\n",
    ]

    principal = final[final["variante"] == "principal"]
    if not principal.empty:
        L += ["## Especificación principal\n", _md(_tabla_resultados(principal)), ""]
        if "nulo_informativo" in principal.columns:
            # Sin línea base el indicador queda vacío: vacío no es "nulo informativo".
            info = principal[principal["nulo_informativo"].eq(True)]["resultado"].tolist()
            L += [f"Nulos informativos (±{sesoi}%): {', '.join(info) if info else 'ninguno'}.\n"]

    enif = _leer("desc_enif_cuentas.csv")
    if not enif.empty:
        L += [
            "## ENIF: tenencia de cuenta por tamaño de localidad (descriptivo)\n",
            "Tabulados oficiales, población de 18 a 70 años. La ENIF no es representativa por "
            "municipio: es contraste, no estimación causal.\n",
            _md(enif, decimales=1),
            "",
        ]

    medicion = _leer("desc_medicion_denue_*.csv")
    if not medicion.empty:
        L += [
            "## Medición del DENUE entre versiones\n",
            "Porcentaje de localidades cuyo conteo cambia respecto de la versión anterior y "
            "crecimiento del total. Las actualizaciones integrales son s = 8 (2019S2) y s = 18 "
            "(2024S2); entre ellas el resultado casi no se actualiza.\n",
            _md(medicion),
            "",
        ]

    regimen = _leer("desc_regimen_censal_*.csv")
    if not regimen.empty:
        L += [
            "## Régimen de levantamiento censal (descriptivo)\n",
            "Los Censos Económicos que alimentan las actualizaciones integrales del DENUE recorren "
            "manzana por manzana las cabeceras municipales y las localidades de 2,500 habitantes o "
            "más; el resto del territorio rural va por muestra (INEGI, CE 2024, Metodología). Cambio "
            "medio del resultado en cada actualización por grupo y régimen, y su diferencia bruta "
            "contra los controles del mismo régimen (sin covariables).\n",
            _md(
                regimen[
                    [
                        "resultado",
                        "grupo",
                        "regimen",
                        "unidades",
                        "pct_unidades_grupo",
                        "base_2024S1",
                        "cambio_2019S2",
                        "cambio_2024S2",
                        "dif_2019S2_vs_control",
                        "dif_2024S2_vs_control",
                    ]
                ],
                decimales=2,
            ),
            "",
        ]

    for variante, titulo in [
        ("eacp", "EACP: captación, crédito y tarjetas, 2019T1–2025T4"),
        (
            "inclusion_total",
            "Inclusión total (banca múltiple + desarrollo, incluye al Banco del Bienestar)",
        ),
        ("primera_etapa", "Primera etapa: sucursales totales y cuentas del Banco del Bienestar"),
        ("imss", "Empleo formal (IMSS, cierres de trimestre 2019T1–2025T4)"),
        ("ce", "Censos Económicos 2004–2024 (una cohorte en el CE 2024, tres placebos)"),
        ("remesas", "Remesas por municipio (Banxico)"),
        ("hasta_2025", "Extensión a 2025T4 de la especificación financiera principal"),
        ("secundaria", "Especificaciones secundarias"),
        ("derrame", "Derrame a localidades vecinas (<10 km)"),
        ("panel_corto", "BDIF, panel corto 2022T4–2024T4"),
        ("panel_corto_2025", "BDIF, panel corto 2022T4–2025T4"),
    ]:
        sub = final[final["variante"] == variante]
        if not sub.empty:
            L += [f"## {titulo}\n", _md(_tabla_resultados(sub)), ""]
            if variante == "eacp" and "nulo_informativo" in sub.columns:
                info = sub[sub["nulo_informativo"].eq(True)]["resultado"].tolist()
                L += [
                    f"Nulos informativos (±{sesoi}%): {', '.join(info) if info else 'ninguno'}.\n"
                ]

    columnas_otros = [c for c in final.columns if c.startswith("valor_")]
    if columnas_otros:
        comp = final[["panel", "diseno", "variante", "resultado", "valor", *columnas_otros]].rename(
            columns={
                "valor": "Callaway y Sant'Anna",
                **{c: c.removeprefix("valor_") for c in columnas_otros},
            }
        )
        L += ["## Comparación de estimadores\n", _md(comp), ""]

    disenos = _leer("rob_disenos_*.csv")
    bacon = _leer("bacon_[!d]*.csv")  # resúmenes; `bacon_detalle_*` trae cada 2×2
    if not disenos.empty:
        L += ["## Contraste de diseños\n", _md(disenos), ""]
    if not bacon.empty:
        L += ["Descomposición de Goodman-Bacon del TWFE (ventana escalonada):\n", _md(bacon), ""]

    L += _seccion_alternativos()

    rob = _sin_fase2(_leer("rob_[!dh]*.csv"))
    if not rob.empty:
        cols = [
            c
            for c in [
                "panel",
                "diseno",
                "resultado",
                "variante",
                "tratadas",
                "controles",
                "att",
                "ee",
                "pre_sig",
                "pre_n",
                "pre_wald_p",
            ]
            if c in rob.columns
        ]
        L += [
            "## Robustez (con la auditoría de pre-tendencias de cada variante)\n",
            _md(rob[cols]),
            "",
        ]

    honest = _sin_fase2(_leer("rob_honest_*.csv"))
    if not honest.empty:
        L += ["## HonestDiD (magnitudes relativas, base universal)\n", _md(honest), ""]

    het = _leer("het_q.csv")
    if not het.empty:
        cols = [
            c
            for c in [
                "resultado",
                "dimension",
                "grupo",
                "tratadas",
                "att",
                "ee",
                "dif_vs_ref",
                "p_dif",
                "q_dif",
            ]
            if c in het.columns
        ]
        L += ["## Heterogeneidad (q-values BH sobre las diferencias)\n", _md(het[cols]), ""]

    balance = _leer("balance_*.csv")
    if not balance.empty:
        L += ["## Balance del emparejamiento\n", _md(balance), ""]

    L += _seccion_fase2()

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text("\n".join(L), encoding="utf-8")
    log.info("reporte escrito en %s", SALIDA)
    return SALIDA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

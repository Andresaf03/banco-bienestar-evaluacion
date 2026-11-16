"""Fase 3: reglas que cambian resultados si se rompen (colapso trimestral, coaliciones, cohorte)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from proyecto.construccion.panel_fase3 import cohorte_electoral
from proyecto.limpieza.ine_elecciones import miembros, votos_por_partido
from proyecto.limpieza.sesnsp import colapsar_trimestres
from proyecto.utils.io import parametros


# --------------------------------------------------------------------------- SESNSP: meses -> trimestres
def test_colapso_trimestral_suma_meses_y_conserva_trimestres_sin_dato():
    mensual = pd.DataFrame(
        {
            "cve_mun": ["01001"] * 6,
            "anio": [2019] * 6,
            "mes": [1, 2, 3, 4, 5, 6],
            "valor": [1.0, np.nan, 2.0, np.nan, np.nan, np.nan],
        }
    )
    t = colapsar_trimestres(mensual, "valor").set_index("periodo")["valor"]
    # Un mes faltante no anula el trimestre; un trimestre sin ningún dato no se vuelve cero.
    assert t["2019Q1"] == 3
    assert np.isnan(t["2019Q2"])


def test_colapso_trimestral_asigna_meses_al_trimestre_correcto():
    mensual = pd.DataFrame(
        {"cve_mun": ["01001"] * 4, "anio": [2020] * 4, "mes": [3, 4, 9, 10], "valor": [1, 2, 4, 8]}
    )
    t = colapsar_trimestres(mensual, "valor").set_index("periodo")["valor"]
    assert t.to_dict() == {"2020Q1": 1, "2020Q2": 2, "2020Q3": 4, "2020Q4": 8}


# --------------------------------------------------------------------------- INE: coaliciones
@pytest.mark.parametrize(
    ("columna", "esperado"),
    [
        ("MORENA", ["MORENA"]),
        ("PRI_PVEM", ["PRI", "PVEM"]),
        ("PAN_NVA_ALIANZA", ["PAN", "NVA_ALIANZA"]),
        ("PT_MORENA_ES", ["PT", "MORENA", "ES"]),
        ("PVEM_PT_MORENA", ["PVEM", "PT", "MORENA"]),
        ("CAND_IND1", None),
        ("LISTA_NOMINAL", None),
    ],
)
def test_columnas_de_votos_se_separan_en_partidos(columna, esperado):
    assert miembros(columna) == esperado


def test_combinaciones_se_reparten_por_igual_y_el_bloque_suma_bien():
    casilla = pd.DataFrame(
        {
            "MORENA": [100],
            "PT": [10],
            "PVEM": [20],
            "PRI": [50],
            "PRI_PVEM": [6],  # 2018: PVEM coligado con el PRI -> 3 al PVEM
            "PT_MORENA_ES": [9],  # 3 a cada uno
            "LISTA_NOMINAL": [500],
        }
    )
    v = votos_por_partido(casilla).iloc[0]
    assert v["PVEM"] == pytest.approx(23)
    assert v["MORENA"] == pytest.approx(103)
    assert v["PT"] == pytest.approx(13)
    assert v["ES"] == pytest.approx(3)
    bloque = v[parametros()["fase3"]["elecciones"]["bloque"]].sum()
    assert bloque == pytest.approx(139)
    # Ningún voto se pierde ni se duplica al repartir.
    assert v.sum() == pytest.approx(100 + 10 + 20 + 50 + 6 + 9)


# --------------------------------------------------------------------------- cohorte electoral
def test_cohorte_electoral_tratadas_controles_y_exclusiones():
    cfg = parametros()["fase3"]["elecciones"]
    g = pd.Series(
        [
            "2021Q3",
            "2022Q4",
            "2023Q1",
            "2024Q1",
            "2021Q2",
            "2020Q2",
            "2024Q2",
            "2024Q3",
            None,
            "2019Q1",
        ]
    )
    c = cohorte_electoral(g, cfg, inicio_panel="2019Q1")
    # Entre las elecciones de 2021 y 2024: tratadas (G = 4), con la dosis temprana hasta 2022T4.
    assert c["G"].tolist() == [4, 4, 4, 4, 0, 0, 0, 0, 0, 0]
    assert c["exposicion_ce"].tolist()[:4] == ["temprana", "temprana", "tardía", "tardía"]
    # Expuestas en una elección previa o con trimestre ambiguo: fuera de la muestra.
    assert c["apertura_posterior_ce"].tolist() == [
        False,
        False,
        False,
        False,
        True,
        True,
        True,
        False,
        False,
        False,
    ]
    # Abre después de la elección de 2024 o nunca: control. 2019T1 = ya tratado (lo quita
    # `ya_tratado_inicio`, no esta regla).
    assert c.loc[[7, 8, 9], "exposicion_ce"].tolist() == ["control"] * 3

"""Fase 4: reglas que cambian resultados si se rompen (series privadas, trimestres del Portafolio,
contigüidad y equivalencia del TWFE extendido con BJS)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

from proyecto.construccion.panel_fase4 import (
    OLAS_ENIGH,
    a_trimestres,
    mes_a_trimestre,
    ola_de_apertura,
    restar,
)
from proyecto.limpieza.enigh import gasto_por_forma
from proyecto.variables.vecinos import pares_contiguos, vecino_de_tratado

RAIZ = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------- series privadas
def test_restar_deja_lo_privado_y_conserva_el_total():
    total = pd.Series([100.0, 50.0, 10.0])
    banco = pd.Series([0.0, 0.0, 0.0])
    banjercito = pd.Series([20.0, 0.0, 10.0])
    privado = restar(total, banco, banjercito)
    assert privado.tolist() == [80.0, 50.0, 0.0]
    # Lo privado más lo público reproduce el total (el cuadre nacional de la adenda).
    assert (privado + banco + banjercito).sum() == total.sum()


def test_restar_un_negativo_es_inconsistencia_no_cantidad():
    privado = restar(pd.Series([5.0, 8.0]), pd.Series([7.0, 1.0]))
    assert np.isnan(privado.iloc[0])
    assert privado.iloc[1] == 7.0


# --------------------------------------------------------------------------- Portafolio: meses -> trimestres
def _mensual(valores: dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame(
        {"cve_mun": "01001", "yyyymm": list(valores), "valor": list(valores.values())}
    )


def test_mes_a_trimestre_acepta_cualquier_mes():
    assert [mes_a_trimestre(m) for m in ("202201", "202205", "202209", "202212")] == [
        "2022Q1",
        "2022Q2",
        "2022Q3",
        "2022Q4",
    ]


def test_saldo_toma_el_cierre_y_flujo_suma_los_tres_meses():
    d = _mensual({"202201": 10, "202202": 30, "202203": 20, "202204": 5})
    saldo = a_trimestres(d, flujo=False).set_index("periodo")["valor"]
    flujo = a_trimestres(d, flujo=True).set_index("periodo")["valor"]
    # Saldo: el mes de cierre, no el promedio ni el último mes observado de un trimestre a medias.
    assert saldo.to_dict() == {"2022Q1": 20}
    # Flujo: la suma del trimestre completo; el trimestre con un solo mes publicado sale.
    assert flujo.to_dict() == {"2022Q1": 60}


# --------------------------------------------------------------------------- contigüidad
def test_contiguidad_queen_simetrica_y_sin_islas_falsas():
    # Cuadrícula 2 × 2 (todos se tocan, también en diagonal) más una isla separada.
    g = gpd.GeoDataFrame(
        {"cve_mun": ["01001", "01002", "01003", "01004", "01005"]},
        geometry=[
            box(0, 0, 1, 1),
            box(1, 0, 2, 1),
            box(0, 1, 1, 2),
            box(1, 1, 2, 2),
            box(5, 5, 6, 6),
        ],
        crs=6372,
    )
    pares = pares_contiguos(g)
    conjunto = set(map(tuple, pares[["cve_mun", "cve_mun_vecino"]].to_numpy()))
    assert all((b, a) in conjunto for a, b in conjunto)
    assert not any(a == b for a, b in conjunto)
    assert pares.groupby("cve_mun").size().to_dict() == {
        "01001": 3,
        "01002": 3,
        "01003": 3,
        "01004": 3,
    }
    assert "01005" not in set(pares["cve_mun"])


def test_vecino_de_tratado_separa_aperturas_nuevas_de_heredadas():
    pares = pd.DataFrame(
        {
            "cve_mun": ["A", "A", "A", "B", "C"],
            "cve_mun_vecino": ["B", "C", "D", "A", "A"],
        }
    )
    g = pd.Series({"B": "2023Q2", "C": "2016Q1", "D": "2022Q3"})
    v = vecino_de_tratado(g, inicio="2019Q1", pares=pares).set_index("cve_mun")
    # A: su primera apertura vecina nueva es 2022Q3 (D), y tiene un vecino heredado (C).
    assert v.loc["A", "G_trimestre_vecino"] == "2022Q3"
    assert bool(v.loc["A", "vecino_heredado"])
    assert v.loc["A", "n_vecinos"] == 3
    # B y C solo colindan con A, que nunca abre.
    assert pd.isna(v.loc["B", "G_trimestre_vecino"])
    assert not bool(v.loc["B", "vecino_heredado"])


# --------------------------------------------------------------------------- ENIGH
@pytest.mark.parametrize(
    ("apertura", "esperado"),
    [
        ("2022Q2", (4, False)),  # abre antes del levantamiento (21 de agosto): tratada en 2022
        ("2022Q3", (4, True)),  # abre durante el levantamiento: ambigua
        ("2022Q4", (5, False)),  # abre después: tratada hasta 2024
        ("2019Q2", (3, False)),  # entre olas: tratada desde la de 2020
        ("2024Q4", (0, False)),  # después de la última ola: no tratada en la ventana
        (np.nan, (0, False)),  # nunca abre
    ],
)
def test_ola_de_apertura_respeta_el_levantamiento(apertura, esperado):
    assert ola_de_apertura(apertura, OLAS_ENIGH) == esperado


def test_gasto_electronico_cuenta_cualquiera_de_las_tres_formas():
    gastos = pd.DataFrame(
        {
            "folioviv": ["1", "1", "1", "2"],
            "foliohog": ["1", "1", "1", "1"],
            # efectivo; efectivo + débito; sin forma registrada (00); transferencia
            "forma_pag1": ["01", "01", "00", "04"],
            "forma_pag2": [np.nan, "06", np.nan, np.nan],
            "forma_pag3": [np.nan, np.nan, np.nan, np.nan],
            "gasto_tri": [100.0, 50.0, 30.0, 20.0],
        }
    )
    h = gasto_por_forma(gastos).set_index("folioviv")
    # El gasto sin forma de pago no entra al denominador; el mixto cuenta como electrónico.
    assert h.loc["1", "gasto_forma"] == 150
    assert h.loc["1", "gasto_electronico"] == 50
    assert bool(h.loc["1", "pago_electronico"])
    assert h.loc["2", "gasto_electronico"] == h.loc["2", "gasto_forma"] == 20


# --------------------------------------------------------------------------- TWFE extendido = BJS
@pytest.mark.skipif(shutil.which("Rscript") is None, reason="sin R")
def test_twfe_extendido_sin_covariables_reproduce_bjs(tmp_path):
    """Wooldridge (2021): sin covariables y con pesos por observación, el TWFE extendido es el
    estimador de imputación de Borusyak et al. Panel sintético escalonado con efectos que crecen
    con la exposición y difieren entre cohortes."""
    script = tmp_path / "equivalencia.R"
    script.write_text(
        f"""
        Sys.setenv(PROYECTO_SALIDAS = "{tmp_path}")
        source(file.path("{RAIZ}", "analisis", "13_fase4.R"))
        set.seed(1)
        d <- data.table::CJ(id = 1:120, tiempo = 1:12)
        g <- c(rep(0, 40), rep(5, 30), rep(8, 30), rep(10, 20))
        d[, G := g[id]]
        d[, cluster := id]
        d[, y := 0.1 * id / 120 + 0.05 * tiempo + rnorm(.N, sd = 0.2) +
                fifelse(G > 0 & tiempo >= G, 0.3 + 0.05 * (tiempo - G) + 0.1 * (G == 8), 0)]
        d[, cve_mun := sprintf("%05d", id)]
        x <- twfe_extendido(d, "y", covariables = FALSE, pesos = "observaciones")
        b <- bjs_imputacion(d, "y")
        cat(sprintf("%.10f %.10f\\n", x$att, b$estimate[1]))
        """,
        encoding="utf-8",
    )
    salida = subprocess.run(
        ["Rscript", str(script)], cwd=RAIZ, capture_output=True, text=True, timeout=300
    )
    assert salida.returncode == 0, salida.stderr[-2000:]
    etwfe, bjs = map(float, salida.stdout.strip().splitlines()[-1].split())
    assert etwfe == pytest.approx(bjs, abs=1e-8)

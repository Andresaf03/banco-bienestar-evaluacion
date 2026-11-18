"""Fase 6: reglas que cambian resultados si se rompen (sectores, cotas de apertura, padrón)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from proyecto.construccion.panel_fase6 import sectores_denue
from proyecto.limpieza.pub_bienestar import leer_consolidado
from proyecto.utils.fase6_descriptivos import _mediana_ponderada
from proyecto.variables.accesibilidad import apertura_central, cotas_apertura, distancia_minima


# --------------------------------------------------------------------------- DENUE por sector
def _largo(clases: dict[str, int], bloque: str = "emprendimiento") -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cve_loc": "010010001",
            "semestre": "2024S2",
            "bloque": bloque,
            "clase": list(clases),
            "n_estab": list(clases.values()),
        }
    )


def test_sectores_suman_el_total_y_separan_consumo_del_resto():
    loc = pd.concat(
        [
            _largo({"46": 10, "72": 4, "81": 3, "31": 2, "33": 1, "52": 5, "93": 2, "43": 7}),
            # Otro bloque no debe contarse: una farmacia también está en `consumo`.
            _largo({"farmacia": 99}, bloque="consumo"),
        ]
    )
    s = sectores_denue(loc).iloc[0]
    assert s["estab_total_sectores"] == 34
    assert s["estab_consumo_amplio"] == 17
    assert s["estab_resto"] == 17
    assert s["estab_s3133"] == 3
    assert s["estab_sin_52_93"] == 27


def test_sector_ausente_vale_cero():
    s = sectores_denue(_largo({"46": 2})).iloc[0]
    assert s["estab_s72"] == 0
    assert s["estab_resto"] == 0


# --------------------------------------------------------------------------- B1: cotas de apertura
def test_cotas_de_apertura_respetan_heredadas_ambiguas_y_la_principal():
    trat = pd.DataFrame(
        {
            "cve_mun_estable": ["A", "A", "A", "B", "C"],
            "G_trimestre": [None, "2022Q1", None, "2023Q2", None],
            "ya_tratado_inicio": [False, False, False, False, True],
            "fecha_ambigua": [True, True, False, False, False],
            "pobtot": [5_000, 300, 100, 800, 900],
        }
    )
    g_mun = pd.Series(["2022Q1", "2022Q1", "2022Q1", "2023Q2", "2019Q1"])
    c = cotas_apertura(trat, g_mun)
    # Ambiguas: optimista = fecha del municipio; pesimista = solo la más poblada la conserva.
    assert c.loc[0].tolist() == ["2022Q1", "2022Q1"]
    assert c.loc[1].tolist() == ["2022Q1", "2024Q4"]
    # Sin fecha propia ni ambigüedad: cae a la fecha del municipio en las dos cotas.
    assert c.loc[2].tolist() == ["2022Q1", "2022Q1"]
    assert c.loc[3].tolist() == ["2023Q2", "2023Q2"]
    # Heredada de Bansefi sin ambigüedad: abierta desde 2019T1.
    assert c.loc[4].tolist() == ["2019Q1", "2019Q1"]


def test_apertura_central_abre_por_poblacion_cuando_sube_el_conteo():
    trat = pd.DataFrame(
        {
            "cve_mun": ["M", "M", "M", "N"],
            "cve_loc": ["M1", "M2", "M3", "N1"],
            "fecha_ambigua": [True, True, True, False],
            "n_sucursales_loc": [2, 1, 1, 1],
            "pobtot": [9_000, 3_000, 500, 100],
        }
    )
    conteo = pd.DataFrame(
        {
            "cve_mun": ["M"] * 4,
            "periodo": ["2019Q1", "2022Q1", "2023Q1", "2024Q1"],
            "suc_bienestar": [1, 2, 3, 3],
        }
    )
    c = apertura_central(trat, conteo)
    # La más poblada (2 sucursales) abre con la primera; la segunda necesita 3 en el municipio.
    assert c.loc[0] == "2019Q1"
    assert c.loc[1] == "2023Q1"
    # El conteo nunca llega a 4: abre con la red completa de 2024T4.
    assert c.loc[2] == "2024Q4"
    # Las no ambiguas no se tocan.
    assert pd.isna(c.loc[3])


def test_distancia_minima_es_cero_en_la_propia_y_crece_con_la_separacion():
    destino = pd.DataFrame({"lat": [19.0], "lon": [-99.0]})
    origen = pd.DataFrame({"lat": [19.0, 19.09], "lon": [-99.0, -99.0]})
    km = distancia_minima(origen, destino)
    assert km[0] == pytest.approx(0, abs=1e-9)
    assert km[1] == pytest.approx(10.0, rel=0.01)  # 0.09° de latitud ≈ 10 km


# --------------------------------------------------------------------------- padrón y ENIF
def test_consolidado_del_padron_lee_la_hoja_municipio(tmp_path):
    ruta = tmp_path / "consMpo1.xlsx"
    filas = [[None] * 5] * 4 + [
        ["Clave Entidad", "Clave Municipio", "Nombe Municipio", "Beneficiarios Unicos", "Monto"],
        ["01", "999", "NO ESPECIFICADO", 7483, 199.26],
        ["1", "8", "SAN JOSÉ DE GRACIA", 3115, 19768583.38],
    ]
    with pd.ExcelWriter(ruta) as w:
        pd.DataFrame([[None]]).to_excel(w, sheet_name="consMpo", header=False, index=False)
        pd.DataFrame(filas).to_excel(w, sheet_name="Municipio", header=False, index=False)
    t = leer_consolidado(ruta)
    assert t["cve_ent"].tolist() == ["01", "01"]
    assert t["cve_mun3"].tolist() == ["999", "008"]
    assert t["beneficiarios_unicos"].tolist() == [7483, 3115]


def test_mediana_ponderada_usa_los_factores_e_ignora_faltantes():
    x = pd.Series([10.0, 20.0, 30.0, np.nan])
    w = pd.Series([1.0, 1.0, 10.0, 100.0])
    assert _mediana_ponderada(x, w) == 30.0
    assert np.isnan(_mediana_ponderada(pd.Series([np.nan]), pd.Series([1.0])))

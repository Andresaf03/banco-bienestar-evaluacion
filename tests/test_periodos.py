"""Periodos: formato YYYYQn, índice t consecutivo con 2019Q1 = 1, sin huecos en la BDIF."""

import pytest

from proyecto.utils import periodos as p


def test_conversiones_basicas():
    assert p.yyyymm_a_periodo("201903") == "2019Q1"
    assert p.yyyymm_a_periodo(202412) == "2024Q4"
    assert p.periodo_a_yyyymm("2019Q1") == "201903"
    with pytest.raises(ValueError):
        p.yyyymm_a_periodo("201902")


def test_indice_t_base_2019q1():
    assert p.periodo_a_t("2019Q1") == 1
    assert p.periodo_a_t("2024Q4") == 24
    assert p.periodo_a_t("2016Q1") == -11
    assert p.t_a_periodo(1) == "2019Q1"
    assert p.t_a_periodo(24) == "2024Q4"
    assert [p.periodo_a_t(x) for x in p.rango("2019Q1", "2019Q4")] == [1, 2, 3, 4]


def test_son_consecutivos():
    assert p.son_consecutivos(["2019Q1", "2019Q2", "2019Q3"])
    assert not p.son_consecutivos(["2019Q1", "2019Q3"])
    assert p.son_consecutivos([])


def test_bdif_periodos_consecutivos_y_t_coherente(bdif):
    pares = bdif[["periodo", "t"]].drop_duplicates().sort_values("t")
    assert pares["periodo"].str.fullmatch(r"\d{4}Q[1-4]").all()
    assert p.son_consecutivos(pares["periodo"].tolist()), "hay trimestres faltantes en la BDIF"
    assert (pares["t"].diff().dropna() == 1).all(), "t no es consecutivo"
    assert (pares["periodo"].map(p.periodo_a_t) == pares["t"]).all(), "t no coincide con periodo"
    assert pares.loc[pares["periodo"] == "2019Q1", "t"].item() == 1
    assert pares["periodo"].min() <= "2019Q1" and pares["periodo"].max() >= "2024Q4"

"""Claves municipales: texto de 5 dígitos, entidad 01–32, en todas las tablas interim."""

import pandas as pd
import pytest

from proyecto.utils import claves


def test_normalizar_cve_casos():
    assert claves.normalizar_cve(1001) == "01001"
    assert claves.normalizar_cve("1001.0") == "01001"
    assert claves.normalizar_cve(1001.0) == "01001"
    assert claves.normalizar_cve("09002") == "09002"
    assert claves.normalizar_cve(None) is None
    assert claves.normalizar_cve("abc") is None
    assert claves.normalizar_cve(123456) is None


def test_combinar_ent_mun():
    s = claves.combinar(pd.Series(["1", "9", 32]), pd.Series(["1", "2", "58"]))
    assert s.tolist() == ["01001", "09002", "32058"]


def test_es_valida():
    assert claves.es_valida("01001")
    assert not claves.es_valida("1001")
    assert not claves.es_valida("33001")
    assert not claves.es_valida(1001)


@pytest.mark.parametrize(
    "nombre", ["bdif", "poblacion", "municipios", "crosswalk", "marginacion", "censo_2020"]
)
def test_cve_mun_5_digitos(request, nombre):
    df = request.getfixturevalue(nombre)
    col = df["cve_mun"].dropna()
    assert (col.str.len() == 5).all(), f"{nombre}: claves con largo != 5"
    assert col.str.fullmatch(r"\d{5}").all(), f"{nombre}: claves no numéricas"
    assert col.map(claves.es_valida).all(), f"{nombre}: entidad fuera de 01–32"


def test_babien_cve_espacial(babien):
    col = babien["cve_mun_espacial"].dropna()
    assert (col.str.len() == 5).all() and col.map(claves.es_valida).all()


def test_crosswalk_estable_valida(crosswalk):
    est = crosswalk["cve_estable"].dropna()
    assert est.map(claves.es_valida).all()
    hijos = crosswalk[crosswalk["tipo"] == "hijo"]
    assert hijos["cve_estable"].notna().all(), "todo hijo debe tener padre"
    assert (hijos["cve_estable"] != hijos["cve_mun"]).all()

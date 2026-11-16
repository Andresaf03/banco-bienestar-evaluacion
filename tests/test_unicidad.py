"""Unicidad municipio-periodo (y sector-variable) en las tablas interim."""


def test_bdif_largo_sin_duplicados(bdif):
    assert not bdif.duplicated(["cve_mun", "periodo", "sector", "variable"]).any()


def test_poblacion_unica_por_municipio_periodo(poblacion):
    assert not poblacion.duplicated(["cve_mun", "periodo"]).any()
    assert poblacion["poblacion_adulta"].notna().all()
    assert (poblacion["poblacion_adulta"] > 0).all()


def test_sucursales_bd_una_fila_por_mun_periodo(bdif):
    suc = bdif[(bdif["variable"] == "sucursales") & (bdif["sector"] == "banca_desarrollo")]
    assert not suc.duplicated(["cve_mun", "periodo"]).any()
    assert suc["periodo"].nunique() == bdif["periodo"].nunique(), (
        "sucursales BD faltan en algún trimestre"
    )
    assert (suc["valor"].dropna() >= 0).all()


def test_municipios_unicos(municipios, crosswalk):
    assert municipios["cve_mun"].is_unique
    assert crosswalk["cve_mun"].is_unique


def test_marginacion_unica_por_anio(marginacion):
    assert not marginacion.duplicated(["cve_mun", "anio"]).any()
    assert set(marginacion["anio"].unique()) == {2010, 2015, 2020}

"""Serie de sucursales del Bienestar sin Banjército: consistencia con la BDIF y con el Portafolio."""

import pandas as pd
import pytest

from proyecto.utils.io import INTERIM, raiz


@pytest.fixture(scope="session")
def sucursales_bienestar() -> pd.DataFrame:
    ruta = INTERIM / "sucursales_bienestar.parquet"
    if not ruta.exists():
        pytest.skip(f"falta {ruta.relative_to(raiz())}; corre `make limpiar`")
    return pd.read_parquet(ruta)


def test_unicidad_y_cotas(sucursales_bienestar):
    d = sucursales_bienestar
    assert not d.duplicated(["cve_mun", "periodo"]).any()
    assert (d["suc_banjercito"] >= 0).all() and (d["suc_bienestar"] >= 0).all()
    assert (d["suc_banjercito"] <= d["suc_bd_bdif"]).all()
    assert ((d["suc_bienestar"] + d["suc_banjercito"]) == d["suc_bd_bdif"]).all()


def test_ventana_observada_cuadra_con_portafolio(sucursales_bienestar):
    d = sucursales_bienestar
    obs = d[d["fuente_banjercito"] == "portafolio"]
    assert obs["periodo"].min() == "2016Q1" and obs["periodo"].max() == "2021Q4"
    assert obs["periodo"].nunique() == 24
    op = pd.read_parquet(INTERIM / "cnbv_portafolio_operativa.parquet")
    banj = op[
        (op["producto"] == "Número de Sucursales")
        & (op["institucion"] == "Banjército")
        & (op["periodo"] == "2021Q4")
    ]
    assert banj["valor"].sum() == obs.loc[obs["periodo"] == "2021Q4", "suc_banjercito"].sum() == 83

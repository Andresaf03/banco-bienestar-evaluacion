"""Fixtures: cargan las tablas interim (deben existir; `make limpiar`)."""

from __future__ import annotations

import pandas as pd
import pytest

from proyecto.utils.io import INTERIM, raiz


def _leer(nombre: str, **kw) -> pd.DataFrame:
    ruta = INTERIM / nombre
    if not ruta.exists():
        pytest.skip(f"falta {ruta.relative_to(raiz())}; corre `make limpiar`")
    return pd.read_parquet(ruta, **kw)


@pytest.fixture(scope="session")
def bdif() -> pd.DataFrame:
    return _leer(
        "cnbv_bdif.parquet", columns=["cve_mun", "periodo", "t", "sector", "variable", "valor"]
    )


@pytest.fixture(scope="session")
def poblacion() -> pd.DataFrame:
    return _leer("cnbv_bdif_poblacion.parquet")


@pytest.fixture(scope="session")
def municipios() -> pd.DataFrame:
    return _leer("municipios.parquet")


@pytest.fixture(scope="session")
def crosswalk() -> pd.DataFrame:
    return _leer("crosswalk_municipios.parquet")


@pytest.fixture(scope="session")
def babien() -> pd.DataFrame:
    return _leer("babien.parquet")


@pytest.fixture(scope="session")
def marginacion() -> pd.DataFrame:
    return _leer("conapo_marginacion.parquet")


@pytest.fixture(scope="session")
def censo_2020() -> pd.DataFrame:
    return _leer("inegi_censo_2020.parquet", columns=["cve_mun", "pobtot"])

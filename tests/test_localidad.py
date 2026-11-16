"""Claves de localidad (9 dígitos) y tratamiento a nivel localidad."""

import pandas as pd
import pytest

from proyecto.utils import claves
from proyecto.utils.io import INTERIM, raiz


def _leer(nombre: str, **kw) -> pd.DataFrame:
    ruta = INTERIM / nombre
    if not ruta.exists():
        pytest.skip(f"falta {ruta.relative_to(raiz())}; corre `make limpiar`")
    return pd.read_parquet(ruta, **kw)


@pytest.fixture(scope="session")
def localidades() -> pd.DataFrame:
    return _leer("inegi_censo_localidades_2020.parquet")


@pytest.fixture(scope="session")
def tratamiento_loc() -> pd.DataFrame:
    return _leer("tratamiento_localidad.parquet")


def test_combinar_localidad():
    s = claves.combinar_localidad(pd.Series(["01001", "09002"]), pd.Series(["1", "0345"]))
    assert s.tolist() == ["010010001", "090020345"]


def test_es_valida_localidad():
    assert claves.es_valida_localidad("010010001")
    assert not claves.es_valida_localidad("0100100")  # largo incorrecto
    assert not claves.es_valida_localidad("330010001")  # entidad fuera de rango
    assert not claves.es_valida_localidad(10010001)  # no es texto


def test_localidades_clave_unica_y_valida(localidades):
    assert localidades["cve_loc"].is_unique
    assert localidades["cve_loc"].map(claves.es_valida_localidad).all()
    # La clave de localidad debe contener a la del municipio.
    assert (localidades["cve_loc"].str[:5] == localidades["cve_mun"]).all()


def test_tratamiento_localidad_coherente(tratamiento_loc, localidades):
    t = tratamiento_loc
    assert t["cve_loc"].is_unique
    assert t["cve_loc"].map(claves.es_valida_localidad).all()
    assert t["cve_loc"].isin(localidades["cve_loc"]).all()
    # Toda localidad con fecha propia tiene una sola sucursal en su municipio.
    con_fecha = t[t["G_trimestre"].notna() & ~t["fecha_ambigua"]]
    assert (con_fecha["n_sucursales_mun"] == 1).all()
    # La asignación espacial es cercana: la mediana debe estar por debajo de 1 km.
    assert t["dist_sucursal_km"].median() < 1.0
    assert (t["g_s"] >= 0).all()


def test_tratamiento_localidad_cubre_municipios_tratados(tratamiento_loc):
    sb = _leer("sucursales_bienestar.parquet", columns=["cve_mun", "suc_bienestar"])
    con_sucursal = set(sb.loc[sb["suc_bienestar"] > 0, "cve_mun"])
    asignados = set(tratamiento_loc["cve_mun"])
    # El directorio es una foto de 2026: puede faltar algún municipio que cerró antes.
    assert len(asignados - con_sucursal) / max(len(asignados), 1) < 0.02


N_VERSIONES_DENUE = 18


@pytest.fixture(scope="session")
def denue_cobertura() -> pd.DataFrame:
    c = _leer("denue_cobertura.parquet")
    completas = c["completa"].sum() if "completa" in c.columns else 0
    if completas < N_VERSIONES_DENUE:
        pytest.skip(
            f"descarga del DENUE en curso ({completas}/{N_VERSIONES_DENUE} versiones completas); "
            "termina `make descargar-denue` antes de validar la cobertura"
        )
    return c


def test_denue_cobertura_versiones(denue_cobertura):
    """Las versiones procesadas deben estar completas y sin huecos de semestre inesperados."""
    c = denue_cobertura
    assert c["version"].is_unique
    incompletas = c.loc[~c["completa"], "version"].tolist() if "completa" in c else []
    assert not incompletas, f"versiones DENUE incompletas: {incompletas}"
    # El INEGI no publicó versión en el primer semestre de 2023: es el único hueco esperado.
    semestres = set(c["semestre"])
    esperados = {f"{a}S{s}" for a in range(2016, 2026) for s in (1, 2)} - {"2025S2"}
    faltantes = esperados - semestres
    assert faltantes == {"2023S1"}, f"huecos inesperados: {sorted(faltantes)}"


def test_denue_totales_plausibles(denue_cobertura):
    """El DENUE nacional va de 5.0 millones (2016) a 6.1 millones (2025) de establecimientos.

    El tope tiene que dejar pasar la actualización integral de noviembre de 2024, que subió el
    total nacional 8.9% de golpe: 2024S2 tiene 6,058,543 y 2025S1 6,097,681. Ese salto está
    documentado en `docs/decisiones.md` y se prueba como robustez en `analisis/05_robustez.R`; el
    rango de aquí solo verifica que no se perdió ni se duplicó un sector al agregar.
    """
    c = denue_cobertura
    assert c["establecimientos"].between(4_000_000, 7_000_000).all(), c[
        ["version", "establecimientos"]
    ].to_dict("records")
    assert (c["municipios"] > 2_300).all()


def test_denue_localidad_claves_validas(denue_cobertura):
    d = _leer("denue_localidad.parquet", columns=["cve_loc", "cve_mun", "bloque"])
    muestra = d["cve_loc"].drop_duplicates().head(5000)
    assert muestra.map(claves.es_valida_localidad).all()
    assert set(d["bloque"].unique()) <= {"emprendimiento", "consumo", "salud", "financiero"}


def test_denue_lee_encabezados_en_mayusculas(tmp_path):
    """El INEGI publica algunos sectores con encabezados en mayúsculas (56 en 2022-11 y 2024-05).

    Sin normalizarlos, `usecols` no empata ninguna columna y el archivo se lee vacío, lo que
    borraría ese sector del panel sin avisar.
    """
    import zipfile

    from proyecto.descarga.denue import _leer_csv

    contenido = (
        "ID,CODIGO_ACT,PER_OCU,CVE_ENT,CVE_MUN,CVE_LOC,LATITUD,LONGITUD,FECHA_ALTA\n"
        "1,464111,0 a 5 personas,01,001,0001,21.88,-102.29,2020-01\n"
    )
    ruta = tmp_path / "denue_mayusculas.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("conjunto_de_datos/denue_inegi_56_.csv", contenido.encode("latin-1"))
    d = _leer_csv(ruta)
    assert list(d.columns) == [
        "codigo_act",
        "per_ocu",
        "cve_ent",
        "cve_mun",
        "cve_loc",
        "latitud",
        "longitud",
        "fecha_alta",
    ]
    assert len(d) == 1

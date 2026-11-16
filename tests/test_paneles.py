"""Los paneles deben cumplir lo que `did` exige: balanceados, sin duplicados y con G bien formado.

Un panel mal formado no produce un error: produce un ATT equivocado. Por eso estas pruebas
verifican las propiedades de las que depende la interpretación de los resultados.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from proyecto.utils import claves
from proyecto.utils.io import PROCESSED, raiz

PANELES = {
    "panel_localidad.parquet": ("cve_loc", "s"),
    "panel_municipio.parquet": ("cve_mun", "s"),
    "panel_municipio_trim.parquet": ("cve_mun", "t"),
    "panel_anillo.parquet": ("cve_loc", "s"),
    "panel_municipio_trim_largo.parquet": ("cve_mun", "t"),
    "panel_municipio_ce.parquet": ("cve_mun", "t"),
}


def _leer(nombre: str) -> pd.DataFrame:
    ruta = PROCESSED / nombre
    if not ruta.exists():
        pytest.skip(f"falta {ruta.relative_to(raiz())}; corre `make panel`")
    return pd.read_parquet(ruta)


@pytest.mark.parametrize("nombre", list(PANELES))
def test_panel_balanceado_y_sin_duplicados(nombre):
    d = _leer(nombre)
    id_col, tiempo = PANELES[nombre]
    llaves = [id_col, tiempo]
    if "radio_km" in d.columns:
        llaves.insert(1, "radio_km")
    assert not d.duplicated(llaves).any(), f"{nombre}: filas duplicadas"
    esperado = int(np.prod([d[c].nunique() for c in llaves]))
    assert len(d) == esperado, f"{nombre}: panel desbalanceado ({len(d)} de {esperado})"


@pytest.mark.parametrize("nombre", list(PANELES))
def test_g_bien_formado(nombre):
    """G debe estar en la misma escala que el tiempo, con 0 para los nunca tratados."""
    d = _leer(nombre)
    id_col, tiempo = PANELES[nombre]
    assert d["G"].notna().all()
    validos = set(d[tiempo].unique()) | {0}
    assert set(d["G"].unique()) <= validos, f"{nombre}: G fuera de la escala de {tiempo}"
    # G es constante dentro de cada unidad: el tratamiento es irreversible.
    por_unidad = d.groupby(id_col)["G"].nunique()
    assert (por_unidad == 1).all(), f"{nombre}: G cambia dentro de una unidad"
    # `tratado` es exactamente 1{t >= G, G > 0}.
    esperado = ((d["G"] > 0) & (d[tiempo] >= d["G"])).astype(int)
    assert (d["tratado"] == esperado).all()


@pytest.mark.parametrize("nombre", list(PANELES))
def test_claves_validas(nombre):
    d = _leer(nombre)
    id_col, _ = PANELES[nombre]
    validador = claves.es_valida_localidad if id_col == "cve_loc" else claves.es_valida
    assert d[id_col].drop_duplicates().map(validador).all()


@pytest.mark.parametrize("nombre", list(PANELES))
def test_tamano_de_cohorte_coherente(nombre):
    d = _leer(nombre)
    id_col, _ = PANELES[nombre]
    if "n_cohorte" not in d.columns:
        pytest.skip("el panel no trae n_cohorte")
    reales = d.drop_duplicates(id_col).groupby("G")[id_col].size()
    declarados = d.drop_duplicates(id_col).groupby("G")["n_cohorte"].first()
    assert (reales == declarados).all()


def test_resultados_no_negativos():
    """Los conteos de establecimientos y sus tasas nunca pueden ser negativos."""
    for nombre in PANELES:
        ruta = PROCESSED / nombre
        if not ruta.exists():
            continue
        d = pd.read_parquet(ruta)
        columnas = [c for c in d.columns if c.startswith(("estab_", "micro_", "empleo_"))]
        for c in columnas:
            negativos = (d[c] < 0).sum()
            assert negativos == 0, f"{nombre}.{c}: {negativos} valores negativos"


@pytest.mark.parametrize(
    "variable",
    [
        "captacion_privado",
        "credito_privado",
        "cajeros_privado",
        "tpv_privado",
        "transacciones_tpv_privado",
    ],
)
def test_bdif_por_sector_sin_ceros_falsos(variable):
    """La BDIF no publica estas variables por sector antes de 2022T4: deben ser NaN, no ceros.

    Convertirlas en cero crea un salto artificial en 2022T4 que el estimador lee como efecto del
    tratamiento (ver docs/decisiones.md, 2026-09-26 y 2026-09-29). Desde 2022T4 no hay faltantes:
    un municipio ausente es un cero real.
    """
    d = _leer("panel_municipio_trim.parquet")
    if variable not in d.columns:
        pytest.skip(f"el panel no trae {variable}")
    antes = d[d["periodo"] < "2022Q4"][variable]
    assert antes.isna().all(), f"{variable}: hay ceros donde la BDIF no publica el dato"
    despues = d[d["periodo"] >= "2022Q4"][variable]
    assert despues.notna().all(), f"{variable}: faltantes desde 2022T4"


@pytest.mark.parametrize("nombre", ["panel_localidad.parquet"])
def test_piso_de_poblacion_simetrico(nombre):
    """El piso de población aplica igual a tratadas y controles.

    Si las tratadas quedaran exentas, la robustez "sin piso" solo reincorporaría tratadas diminutas
    (tasas por mil de hasta 53,500) y dejaría fuera a sus controles equivalentes.
    """
    from proyecto.utils.io import parametros

    d = _leer(nombre).drop_duplicates("cve_loc")
    piso = parametros()["unidades"]["localidad_pob_minima"]
    assert (d["pobtot"] >= piso).all(), "hay localidades bajo el piso de población"


def test_sucursales_bm_mas_eacp_igual_a_privado():
    """Banca múltiple + EACP debe reproducir exactamente el total privado en cada celda."""
    d = _leer("panel_municipio_trim.parquet")
    if not {"sucursales_bm", "sucursales_eacp"} <= set(d.columns):
        pytest.skip("el panel no separa banca múltiple y EACP")
    suma = d["sucursales_bm"] + d["sucursales_eacp"]
    assert np.allclose(suma, d["sucursales_privado"])


def test_denominador_bdif_fijo():
    """La tasa por diez mil adultos usa un denominador constante dentro de cada municipio."""
    d = _leer("panel_municipio_trim.parquet")
    if "poblacion_adulta_fija" not in d.columns:
        pytest.skip("el panel no trae el denominador fijo")
    assert (d.groupby("cve_mun")["poblacion_adulta_fija"].nunique(dropna=False) == 1).all()
    assert (d["poblacion_adulta_fija"] > 0).all()


def test_exposicion_espacial_coherente():
    """La distancia a la sucursal vecina es finita y no negativa, y G_vecina está en la escala."""
    completo = _leer("panel_localidad.parquet")
    if "dist_bb_km" not in completo.columns:
        pytest.skip("el panel no trae la exposición espacial")
    d = completo.drop_duplicates("cve_loc")
    con_coord = d[d["lat"].notna()]
    assert (con_coord["dist_bb_km"] >= 0).all()
    assert set(d["G_vecina"].unique()) <= set(completo["s"].unique()) | {0}
    # Hay controles lejos de toda sucursal: sin ellos el diseño principal no tiene comparación.
    assert ((d["G"] == 0) & (d["dist_bb_km"] >= 10)).sum() > 1000


@pytest.mark.parametrize(
    "variable",
    [
        "capt_ahorro_eacp",
        "capt_plazo_eacp",
        "capt_vista_eacp",
        "cred_consumo_eacp",
        "cred_vivienda_eacp",
        "tarjetas_debito_eacp",
    ],
)
def test_series_eacp_continuas_en_2022T4(variable):
    """La serie `eacp` no salta cuando la BDIF empieza a publicar SOCAP y SOFIPO por separado.

    Si el panel sumara `eacp` con `socap` y `sofipo`, el total nacional se duplicaría en 2022T4.
    """
    d = _leer("panel_municipio_trim.parquet")
    if variable not in d.columns:
        pytest.skip(f"el panel no trae {variable}")
    total = d.groupby("periodo")[variable].sum()
    assert 0.8 < total["2022Q4"] / total["2022Q3"] < 1.25, f"{variable}: salto en 2022T4"


def test_panel_largo_misma_g():
    """El panel desde 2016 fecha el tratamiento igual que el principal, 12 trimestres corrido."""
    corto = _leer("panel_municipio_trim.parquet").drop_duplicates("cve_mun").set_index("cve_mun")
    largo = _leer("panel_municipio_trim_largo.parquet").drop_duplicates("cve_mun")
    largo = largo.set_index("cve_mun")
    comunes = corto.index.intersection(largo.index)
    g_corto, g_largo = corto.loc[comunes, "G"], largo.loc[comunes, "G"]
    tratados = g_corto > 0
    assert (g_largo[tratados] == g_corto[tratados] + 12).all()
    assert (g_largo[~tratados] == 0).all()


def test_censos_economicos_una_cohorte_expuesta():
    """En el panel de los CE solo hay una cohorte (el último censo) y las aperturas posteriores al
    año de referencia del CE 2024 quedan marcadas, nunca como tratadas."""
    d = _leer("panel_municipio_ce.parquet").drop_duplicates("cve_mun")
    assert set(d["G"].unique()) <= {0, 5}
    assert not (d["apertura_posterior_ce"] & (d["G"] > 0)).any()

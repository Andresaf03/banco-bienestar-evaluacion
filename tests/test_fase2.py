"""Fase 2: reglas que cambian resultados si se rompen (tratamiento anual, claves, códigos, escala)."""

from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd
import pytest

from proyecto.construccion.panel_fase2 import _g_anual, anio_de_apertura
from proyecto.descarga import enoe, inegi_eic
from proyecto.limpieza.cnbv_portafolio_modelo import _cve_mun
from proyecto.limpieza.viirs import _sumas_bloque
from proyecto.utils.io import INTERIM, parametros, raiz


# --------------------------------------------------------------------------- tratamiento anual
@pytest.mark.parametrize(
    ("periodo", "fmt", "anio"),
    [
        ("2022S1", "semestre", 2022),
        ("2022S2", "semestre", 2023),
        ("2022Q2", "trimestre", 2022),
        ("2022Q3", "trimestre", 2023),
    ],
)
def test_apertura_en_la_segunda_mitad_cuenta_el_anio_siguiente(periodo, fmt, anio):
    assert anio_de_apertura(periodo, fmt) == anio


def test_g_anual_en_escala_t_y_cero_fuera_de_la_ventana():
    anios = list(range(2016, 2025))
    g = _g_anual(pd.Series(["2019S1", "2024S2", None, "2016S2"]), anios, "semestre")
    # 2019 → t = 4; 2024S2 cuenta en 2025, fuera de la ventana → 0; sin apertura → 0; 2017 → t = 2.
    assert g.tolist() == [4, 0, 0, 2]


# --------------------------------------------------------------------------- modelo Power Pivot
def test_clave_municipal_del_modelo_y_sin_clasificar():
    cve = _cve_mun(pd.Series([48420001, 48409017, -1]))
    assert cve.iloc[0] == "20001" and cve.iloc[1] == "09017" and pd.isna(cve.iloc[2])
    with pytest.raises(ValueError):
        _cve_mun(pd.Series([12345]))


def test_modelo_cuadra_con_la_bdif():
    """Banco del Bienestar + Banjército del modelo = banca de desarrollo de la BDIF (≥ 99%)."""
    ruta = INTERIM / "sucursales_bienestar_obs.parquet"
    if not ruta.exists():
        pytest.skip(f"falta {ruta.relative_to(raiz())}; corre `make limpiar-fase2`")
    d = pd.read_parquet(ruta)
    val = d[(d["periodo"] >= "2022Q1") & (d["periodo"] <= "2025Q4") & d["suc_bd_bdif"].notna()]
    assert (val["suc_bd_bdif"] == val["suc_bd_modelo"]).mean() >= 0.99
    antes = d[d["periodo"] < "2022Q1"]
    assert (antes["suc_bienestar_obs"] == antes["suc_bienestar"]).all()
    # Sucursales en municipios nuevos que la BDIF aún no separa: se conservan (cruce `outer`).
    nuevas = d[d["suc_bd_bdif"].isna() & d["suc_bienestar_modelo"].fillna(0).gt(0)]
    assert not nuevas.empty
    assert (nuevas["suc_bienestar_obs"] == nuevas["suc_bienestar_modelo"]).all()


# --------------------------------------------------------------------------- EIC / Censo
def _zip_eic(personas: str, viviendas: str) -> zipfile.ZipFile:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("TR_PERSONA01.CSV", personas)
        z.writestr("TR_VIVIENDA01.CSV", viviendas)
    buf.seek(0)
    return zipfile.ZipFile(buf)


def test_eic_armoniza_codigos_de_2015_y_2025():
    cfg = parametros()["fase2"]["eic"]
    # Misma persona ocupada (CONACT 16 en 2015 / 20 en 2025 = tenía trabajo) y un buscador (20 en
    # 2015 = buscó trabajo; 30 en 2025). Cuenta propia en su municipio; patrón que trabaja fuera.
    p15 = (
        "﻿ENT,MUN,FACTOR,EDAD,CONACT,SITUACION_TRAB,INGTRMEN,MUN_TRAB,ENT_PAIS_TRAB\n"
        "01,001,10,30,16,5,5000,001,001\n"
        "01,001,10,40,20,,,,\n"
        "01,001,10,50,10,4,9000,002,001\n"
    )
    v15 = "ENT,MUN,FACTOR,INGR_AYUGOB,INGR_PEROTROPAIS,CELULAR,INTERNET\n01,001,5,5,2,3,6\n"
    p25 = (
        p15.replace("SITUACION_TRAB", "SITTRA")
        .replace(",16,5,", ",20,5,")
        .replace("01,001,10,40,20,,,,", "01,001,10,40,30,,,,")
    )
    v25 = "ENT,MUN,FACTOR,INGR_AYUGOB,INGR_PEROTROPAIS,CELULAR,INTERNET\n01,001,5,5,2,5,8\n"
    for anio, p, v in [(2015, p15, v15), (2025, p25, v25)]:
        z = _zip_eic(p, v)
        per = inegi_eic.agregar_personas(z, anio, cfg).loc["01001"]
        viv = inegi_eic.agregar_viviendas(z, anio, cfg).loc["01001"]
        assert per["pob12"] == 30 and per["ocupados"] == 20, anio
        assert per["cuenta_propia"] == 10 and per["empleadores"] == 10, anio
        assert per["otro_mun"] == 10 and per["lugar_validos"] == 20, anio
        assert viv["viv_celular"] == 5 and viv["viv_cel_validas"] == 5, anio
        assert viv["viv_internet"] == 0 and viv["viv_net_validas"] == 5, anio
        assert viv["viv_programas"] == 5, anio


# --------------------------------------------------------------------------- ENOE
def test_enoe_normaliza_bom_y_claves_de_2025():
    assert enoe._limpio("ï»¿r_def") == "r_def"
    assert enoe._limpio("﻿R_DEF ") == "r_def"
    assert enoe._limpio("cve_ent") == "ent" and enoe._limpio("cve_mun") == "mun"


# --------------------------------------------------------------------------- VIIRS
def _malla(valor: int, centro: int | None = None) -> np.ndarray:
    m = np.full((41, 41), valor, dtype="<i2")
    if centro is not None:
        m[20, 20] = centro
    return m


def test_viirs_escala_redondeo_y_negativos():
    px = 0.004166666666666667
    lon_izq, lat_sup = -100.0, 20.0
    lat = np.array([lat_sup - 20.5 * px])  # centro del píxel (20, 20)
    lon = np.array([lon_izq + 20.5 * px])
    # 2016–2021: entero = 10 × radiancia (factor 0.1); 14 → 1.4 nW → redondeado a 1.
    viejo = _sumas_bloque(_malla(14), lon_izq, lat_sup, px, lat, lon, 1.0, (1.0, 3.0), 0.1, True)
    # 2022+: entero = radiancia (factor 1.0).
    nuevo = _sumas_bloque(_malla(1), lon_izq, lat_sup, px, lat, lon, 1.0, (1.0, 3.0), 1.0, False)
    assert viejo["luz_1km"].iloc[0] == viejo["npix_1km"].iloc[0] > 0
    pd.testing.assert_frame_equal(viejo, nuevo)
    # Un píxel negativo en el centro es sin dato: no suma ni cuenta.
    neg = _sumas_bloque(_malla(1, -5), lon_izq, lat_sup, px, lat, lon, 1.0, (1.0, 3.0), 1.0, False)
    assert neg["npix_1km"].iloc[0] == nuevo["npix_1km"].iloc[0] - 1
    assert neg["luz_1km"].iloc[0] == nuevo["luz_1km"].iloc[0] - 1
    # El anillo excluye el núcleo de 1 km.
    assert nuevo["npix_anillo"].iloc[0] > nuevo["npix_1km"].iloc[0]

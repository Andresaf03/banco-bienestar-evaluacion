"""El cruce por nombre es una excepción a la regla 6: debe ser conservador.

Exacto dentro del estado, contención solo si es única, difuso solo con margen, homónimos
pendientes y correcciones manuales con prioridad. Se prueba con un catálogo sintético.
"""

from __future__ import annotations

import pandas as pd

from proyecto.utils.cruce_nombres import cruzar, normalizar

CATALOGO = pd.DataFrame(
    {
        "cve_mun": ["07017", "20208", "20209", "14039", "02001", "09001"],
        "cve_ent": ["07", "20", "20", "14", "02", "09"],
        "nom_mun": [
            "Cintalapa de Figueroa",
            "San Juan Mixtepec",
            "San Juan Mixtepec",
            "Guadalajara",
            "Ensenada",
            "Azcapotzalco",
        ],
    }
).assign(norma=lambda d: d["nom_mun"].map(normalizar))


def _cruza(filas, correcciones=None):
    fuente = pd.DataFrame(filas, columns=["clave", "cve_ent", "nombre"])
    return cruzar(fuente, "clave", "cve_ent", "nombre", correcciones, catalogo=CATALOGO).set_index(
        "clave"
    )


def test_normalizar_quita_acentos_y_expande_abreviaturas():
    assert normalizar("Gral. Escobedo") == "general escobedo"
    assert normalizar("Jesús  María") == "jesus maria"


def test_exacto_contenido_y_homonimo():
    r = _cruza(
        [
            ("a", "14", "Guadalajara"),
            ("b", "07", "Cintalapa"),
            ("c", "20", "San Juan Mixtepec"),
        ]
    )
    assert r.loc["a", ["cve_mun", "metodo"]].tolist() == ["14039", "exacto"]
    assert r.loc["b", ["cve_mun", "metodo"]].tolist() == ["07017", "contenido"]
    assert r.loc["c", "metodo"] == "pendiente" and pd.isna(r.loc["c", "cve_mun"])


def test_no_cruza_entre_estados_y_respeta_manuales():
    r = _cruza([("d", "02", "Guadalajara"), ("e", "02", "Isla de Cedros")], {"e": "02001"})
    assert r.loc["d", "metodo"] == "pendiente"
    assert r.loc["e", ["cve_mun", "metodo"]].tolist() == ["02001", "manual"]

"""El emparejamiento respeta los bloques exactos, no reutiliza controles y su balance es coherente.

Se prueba con datos sintéticos: la lógica no depende de los paneles construidos.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from proyecto.construccion.matching import balance, emparejar


def _cov(semilla: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    filas = []
    for ent in ("01", "02"):
        for cab in (True, False):
            for i in range(40):
                filas.append(
                    {
                        "cve_loc": f"{ent}{int(cab)}{i:03d}",
                        "cve_ent": ent,
                        "es_cabecera": cab,
                        "tratada": i < 5,
                        "x1": rng.normal(1.0 if i < 5 else 0.0),
                        "x2": rng.normal(),
                    }
                )
    return pd.DataFrame(filas)


def test_bloques_exactos_y_sin_reemplazo():
    cov = _cov()
    pares = emparejar(cov, "cve_loc", ["x1", "x2"], ["cve_ent", "es_cabecera"], k=3)
    info = cov.set_index("cve_loc")
    for c in ("cve_ent", "es_cabecera"):
        assert (
            info.loc[pares["tratado"], c].to_numpy() == info.loc[pares["control"], c].to_numpy()
        ).all()
    assert not pares["control"].duplicated().any(), "un control se usó dos veces sin reemplazo"
    assert (pares.groupby("tratado").size() <= 3).all()
    assert not info.loc[pares["control"], "tratada"].any(), "se emparejó una tratada como control"


def test_balance_mejora_en_la_variable_desbalanceada():
    cov = _cov(1)
    pares = emparejar(cov, "cve_loc", ["x1", "x2"], ["cve_ent", "es_cabecera"], k=3)
    tabla = balance(cov, pares, "cve_loc", ["x1", "x2"]).set_index("variable")
    assert abs(tabla.loc["x1", "dif_est_despues"]) < abs(tabla.loc["x1", "dif_est_antes"])


def test_caliper_descarta_pares_lejanos():
    cov = _cov(2)
    pares = emparejar(cov, "cve_loc", ["x1", "x2"], ["cve_ent", "es_cabecera"], k=3, caliper=0.5)
    assert (pares["distancia"] <= 0.5).all()

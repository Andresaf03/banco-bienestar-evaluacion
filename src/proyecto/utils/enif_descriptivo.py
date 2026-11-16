"""ENIF 2018, 2021 y 2024: tenencia de cuenta por tamaño de localidad (descriptivo, fase 1).

La ENIF no es representativa por municipio, así que no entra en la estimación causal: sirve como
contraste a nivel personas. Se leen los **tabulados oficiales** (los microdatos de 2024 no traen
descriptor de variables) de la población de 18 a 70 años, comparable entre ediciones:

- 2021 y 2024: cuadro 5.5 del tema Ahorro (bloques nacional, 1–14 999 y 15 000 y más habitantes;
  columnas absolutos y relativos).
- 2018: cuadro 4.6 del tema Ahorro (una columna por tamaño de localidad, en porcentaje).

Indicadores: % de adultos con alguna cuenta de ahorro y % de adultos con cuenta o tarjeta para
recibir apoyos del gobierno (el canal del Banco del Bienestar). En los tabulados el tipo de cuenta
viene como porcentaje de quienes tienen cuenta; aquí se convierte a porcentaje de la población.

Salida: `outputs/tablas/desc_enif_cuentas.csv`.
"""

from __future__ import annotations

import logging
import tempfile
import zipfile
from pathlib import Path

import pandas as pd

from proyecto.utils.io import RAW, TABLAS

log = logging.getLogger(__name__)
TIENE = "Sí tiene alguna cuenta de ahorro"
APOYOS = "apoyos"
BLOQUES = {
    "Estados Unidos Mexicanos": "nacional",
    "1 a 14 999": "menos de 15 mil",
    "15 000": "15 mil y más",
}


def _libro(anio: int) -> Path:
    """Ruta al libro de estimaciones puntuales del tema Ahorro de la edición."""
    if anio == 2018:
        return RAW / "enif" / "2018" / "enif_2018_tabulados_ahorro.xlsx"
    nombre = {
        2021: "enif_2021_tabulados_ahorro_xlsx.zip",
        2024: "enif_2024_tab_18_a_70_anios_ahorro_xlsx.zip",
    }[anio]
    destino = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(RAW / "enif" / str(anio) / nombre) as z:
        libro = next(n for n in z.namelist() if n.split("/")[-1].startswith("01EST"))
        z.extract(libro, destino)
    return destino / libro


def _filas(hoja: pd.DataFrame) -> list[list[str]]:
    return [
        [str(x).replace("\n", " ").strip() for x in fila if str(x).strip()] for fila in hoja.values
    ]


def _bloques_2021_2024(anio: int) -> list[dict]:
    """Bloques consecutivos nacional / rural / urbano con columnas (etiqueta, absolutos, relativos).
    El bloque rural no trae encabezado con el nombre en todas las ediciones: se asigna por orden."""
    filas = _filas(pd.read_excel(_libro(anio), sheet_name="Cuadro 5.5", header=None).fillna(""))
    salida, orden = [], ["nacional", "menos de 15 mil", "15 mil y más"]
    actual: dict | None = None
    for f in filas:
        if not f:
            continue
        if (
            f[0].startswith(TIENE)
            and actual is None
            or (f[0].startswith(TIENE) and "tiene" in actual)
        ):
            actual = {"bloque": orden[len(salida)]} if len(salida) < 3 else None
            if actual is None:
                break
            actual["tiene"] = float(f[2])
        elif actual is not None and APOYOS in f[0] and "apoyos" not in actual:
            actual["apoyos"] = float(f[2])
        elif actual is not None and f[0].startswith("No tiene"):
            salida.append(actual)
            actual = None
            if len(salida) == 3:
                break
    return [{**b, "anio": anio} for b in salida]


def _bloques_2018() -> list[dict]:
    """Primer bloque del cuadro 4.6 (porcentajes): nacional, 1–14 999 y 15 000 y más."""
    filas = _filas(pd.read_excel(_libro(2018), sheet_name="Cuadro 4.6", header=None).fillna(""))
    tiene = next(f for f in filas if f and f[0].startswith(TIENE))
    apoyos = next(f for f in filas if f and APOYOS in f[0])
    nombres = ["nacional", "menos de 15 mil", "15 mil y más"]
    return [
        {"anio": 2018, "bloque": n, "tiene": float(tiene[i + 1]), "apoyos": float(apoyos[i + 1])}
        for i, n in enumerate(nombres)
    ]


def generar() -> Path:
    filas = _bloques_2018() + _bloques_2021_2024(2021) + _bloques_2021_2024(2024)
    d = pd.DataFrame(filas).rename(
        columns={"tiene": "pct_con_cuenta", "apoyos": "pct_cuentahabientes_con_cuenta_apoyos"}
    )
    d["pct_adultos_con_cuenta_apoyos"] = (
        d["pct_con_cuenta"] * d["pct_cuentahabientes_con_cuenta_apoyos"] / 100
    )
    d = d[
        [
            "anio",
            "bloque",
            "pct_con_cuenta",
            "pct_cuentahabientes_con_cuenta_apoyos",
            "pct_adultos_con_cuenta_apoyos",
        ]
    ].sort_values(["bloque", "anio"])
    TABLAS.mkdir(parents=True, exist_ok=True)
    ruta = TABLAS / "desc_enif_cuentas.csv"
    d.round(2).to_csv(ruta, index=False)
    log.info("ENIF:\n%s", d.round(1).to_string(index=False))
    return ruta


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

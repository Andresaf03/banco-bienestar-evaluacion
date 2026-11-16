"""CONAPO, Reconstrucción y proyecciones de la población de los municipios 1990–2040.

Recursos del conjunto https://datos.gob.mx/dataset/proyecciones-de-poblacion (CC BY 4.0):
- `pobproy_quinq1.csv`: población a mitad de año por municipio, sexo y grupos quinquenales.
- `pobproy_ggrupos.csv`: por municipio, sexo y grandes grupos (0-11, 12-29, 30-59, 60+).
- `pobproy_inddemo.csv`: indicadores demográficos municipales.
El portal bloquea clientes no navegador (403), así que se registran las copias manuales.
"""

from __future__ import annotations

from proyecto.descarga.manual import intentar_automatico_o_manual
from proyecto.utils import http
from proyecto.utils.io import RAW

FUENTE = "conapo_proyecciones"
_BASE = "https://www.datos.gob.mx/dataset/f2b9b220-3ef7-4e3a-bde6-87e1dac78c6a/resource/"
RECURSOS = {
    "pobproy_quinq1.csv": _BASE
    + "3c3092be-583e-4490-8c23-67ef9a64b198/download/pobproy_quinq1.csv",
    "pobproy_ggrupos.csv": _BASE
    + "99b28bb6-8e31-48e1-b162-85a7e4deafc3/download/pobproy_ggrupos.csv",
    "pobproy_inddemo.csv": _BASE
    + "e9160552-769b-41ee-88d1-afc765552608/download/pobproy_inddemo.csv",
}


def descargar(force: bool = False) -> None:
    s = http.sesion()
    for nombre, url in RECURSOS.items():
        intentar_automatico_o_manual(
            FUENTE,
            nombre,
            url,
            notas_manual="datos.gob.mx devuelve 403 a requests",
            automatico=lambda u=url, n=nombre: http.descargar(
                u,
                RAW / FUENTE / n,
                FUENTE,
                force=force,
                s=s,
                intentos=1,
                timeout=http.TIMEOUT_CORTO,
            ),
        )

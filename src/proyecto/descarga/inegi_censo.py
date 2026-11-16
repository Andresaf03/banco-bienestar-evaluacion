"""INEGI, Censo de Población y Vivienda 2020: ITER (principales resultados por localidad).

Las filas con `LOC == "0000"` son los totales municipales. Se descarga el zip nacional y el
descriptor de archivo (diccionario) en PDF. Ambos enlaces se verificaron en el sitio de INEGI.

También se baja el ITER del Censo 2010 (enlace descubierto en la página del CPV 2010, sección
"Datos abiertos"): sus localidades traen coordenadas y la clave municipal vigente en 2010, lo que
permite asignar a cada municipio creado después de 2010 su municipio "padre" por cruce espacial
contra los polígonos del Marco Geoestadístico 2024 (crosswalk municipal).
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "inegi_censo"
DESTINO = RAW / FUENTE


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    s = http.sesion()
    http.descargar(
        cfg["url_archivo"], DESTINO / "iter_00_cpv2020_csv.zip", FUENTE, force=force, s=s
    )
    http.descargar(
        cfg["url_diccionario"],
        DESTINO / "fd_iter_cpv2020.pdf",
        FUENTE,
        notas="descriptor de archivos del ITER 2020",
        force=force,
        s=s,
    )
    http.descargar(
        cfg["url_iter_2010"],
        DESTINO / "iter_nal_2010_csv.zip",
        FUENTE,
        notas="ITER 2010 nacional; se usa para el crosswalk de municipios creados después de 2010",
        force=force,
        s=s,
    )

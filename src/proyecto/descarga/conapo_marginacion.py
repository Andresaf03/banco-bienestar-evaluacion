"""CONAPO, Índices de marginación municipal 2020, 2015 y 2010.

Enlaces oficiales (página gob.mx de CONAPO): archivos .xlsx en `conapo.segob.gob.mx`, servidor
que no respondía (timeout) al construir este proyecto. Espejo en datos abiertos
(https://www.datos.gob.mx/dataset/indices_marginacion) con los mismos datos en CSV, pero
bloqueado a clientes no navegador. Se intenta el .xlsx oficial y, si falla, se usa la copia
manual del CSV en `data/manual/conapo_marginacion/`.
"""

from __future__ import annotations

from proyecto.descarga.manual import intentar_automatico_o_manual
from proyecto.utils import http
from proyecto.utils.io import RAW, fuentes

FUENTE = "conapo_marginacion"
# (nombre oficial xlsx, nombre CSV del espejo, url del espejo)
ARCHIVOS = [
    (
        "IMM_2020.xlsx",
        "imm_2020.csv",
        "https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/551d8f48-5d0c-4d11-964a-e2911f732615/download/imm_2020-3.csv",
    ),
    (
        "IMM_DP2_2015.xlsx",
        "imm_dp2_2015.csv",
        "https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/d65dbd44-2fad-4344-bfc2-45152067a14d/download/imm_dp2_2015.csv",
    ),
    (
        "IMM_DP2_2010.xlsx",
        "imm_dp2_2010.csv",
        "https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/216bb68c-d3fa-42a7-84ac-10337cd1f6cd/download/imm_dp2_2010.csv",
    ),
]


def descargar(force: bool = False) -> None:
    cfg = fuentes()[FUENTE]
    oficiales = {u.rsplit("/", 1)[-1]: u for u in cfg["url_archivos"]}
    s = http.sesion()
    for xlsx, csv, url_espejo in ARCHIVOS:
        url_oficial = oficiales[xlsx]
        intentar_automatico_o_manual(
            FUENTE,
            csv,
            url_espejo,
            notas_manual=f"espejo CSV en datos.gob.mx del oficial {url_oficial} (servidor CONAPO sin respuesta)",
            automatico=lambda u=url_oficial, n=xlsx: http.descargar(
                u,
                RAW / FUENTE / n,
                FUENTE,
                force=force,
                s=s,
                intentos=1,
                timeout=http.TIMEOUT_CORTO,
            ),
        )

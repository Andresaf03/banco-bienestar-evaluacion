"""Documentos y papers con fuente pública (van a `literatura/`, no se versionan).

Solo se bajan documentos con enlace público y legal. El Programa Institucional 2020-2024 se
publica en SIDOF como página HTML (sin PDF enlazado; dof.gob.mx no respondía), así que se
guarda el HTML. Bruhn y Love (WP 2009) se resuelve desde la página del repositorio del Banco
Mundial al bitstream `.../bitstreams/<id>/download`, que redirige al PDF.
"""

from __future__ import annotations

from proyecto.utils import http
from proyecto.utils.io import LITERATURA

FUENTE = "literatura"
DOCUMENTOS = {
    "asf_2023_auditoria_2022-0018-a.pdf": (
        "https://www.asf.gob.mx/Trans/Informes/IR2022c/Documentos/Auditorias/2022_0018_a.pdf",
        "ASF, Auditoría 2022-0018-A, Cuenta Pública 2022",
    ),
    "imco_2022_banco_del_bienestar_reporte.pdf": (
        "https://imco.org.mx/wp-content/uploads/2022/04/Reporte-Banco-del-Bienestar_Reporte_06042022.pdf",
        "IMCO (2022), Banco del Bienestar a la deriva (reporte)",
    ),
    "babien_2020_programa_institucional_2020_2024.html": (
        "https://sidof.segob.gob.mx/notas/docFuente/5612609",
        "Programa Institucional 2020-2024 del Banco del Bienestar (DOF vía SIDOF, HTML)",
    ),
    "cnbv_impacto_corresponsales_bancarios.pdf": (
        "https://www.cnbv.gob.mx/CNBV/Estudios-de-la-CNBV/Estudios%20de%20investigacion/Impacto_Corresponsales_Bancarios.pdf",
        "CNBV, El impacto de los corresponsales bancarios en la inclusión financiera",
    ),
    "fonseca_matray_2022_wp308_brazil_unbanked.pdf": (
        "https://gceps.princeton.edu/wp-content/uploads/2023/03/wp308_FonsecaMatray_Brazil_unbanked.pdf",
        "Fonseca y Matray, Griswold Center WP 308 (versión de trabajo del JFE 2024)",
    ),
    "callaway_santanna_2021_did_multiple_periods.pdf": (
        "https://arxiv.org/pdf/1803.09015",
        "Callaway y Sant'Anna (2021), arXiv 1803.09015",
    ),
    "bruhn_love_2009_wps4981_banking_the_unbanked.pdf": (
        "https://openknowledge.worldbank.org/bitstreams/0d9e116c-676f-5df5-99ef-07c9caa5113b/download",
        "Bruhn y Love, World Bank PRWP 4981 (2009); bitstream enlazado desde handle/10986/4173",
    ),
    "aportela_1999_financial_access_savings.pdf": (
        "http://users.nber.org/~rdehejia/!@$devo/Lecture%2006%20Microcredit/supplemental/Aportela.pdf",
        "Aportela (1999), copia pública en users.nber.org",
    ),
}


def descargar(force: bool = False) -> None:
    s = http.sesion()
    for nombre, (url, nota) in DOCUMENTOS.items():
        http.descargar(url, LITERATURA / nombre, FUENTE, notas=nota, force=force, s=s)

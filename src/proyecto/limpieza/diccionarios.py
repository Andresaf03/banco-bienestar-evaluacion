"""Genera `docs/diccionarios/<fuente>.md` a partir de las tablas interim y descripciones curadas."""

from __future__ import annotations

import logging

import pandas as pd

from proyecto.utils.io import DICCIONARIOS, INTERIM

log = logging.getLogger(__name__)

DESCRIPCIONES_BDIF = {
    "sucursales": ("Sucursales en operación", "número"),
    "modulos_compartamos": (
        "Módulos de atención de Compartamos (2017T2–2018T4; la CNBV los contaba aparte de sucursales de banca comercial)",
        "número",
    ),
    "corresponsales": (
        "Módulos de corresponsales bancarios; sin sector (solo total). Cambio de metodología en 2019T1; 'corresponsales únicos' desde 2025T4",
        "número",
    ),
    "cajeros": ("Cajeros automáticos", "número"),
    "tpv": ("Terminales punto de venta", "número"),
    "establecimientos_tpv": ("Establecimientos con TPV", "número"),
    "cuentas_celular": (
        "Contratos/cuentas que usan banca móvil (transacciones por celular)",
        "número",
    ),
    "transacciones_cajeros": ("Transacciones en cajeros automáticos en el trimestre", "número"),
    "transacciones_tpv": ("Transacciones en TPV en el trimestre", "número"),
    "capt_ahorro": ("Cuentas de ahorro (captación)", "contratos"),
    "capt_plazo": ("Depósitos a plazo", "contratos"),
    "capt_vista": ("Depósitos a la vista (EACP)", "contratos"),
    "capt_n1": ("Cuentas transaccionales nivel 1", "contratos"),
    "capt_n2": ("Cuentas transaccionales nivel 2", "contratos"),
    "capt_n3": ("Cuentas transaccionales nivel 3", "contratos"),
    "capt_n4": (
        "Cuentas transaccionales nivel 4 (desde 2022T4; antes 'tradicionales')",
        "contratos",
    ),
    "capt_tradicionales": (
        "Cuentas transaccionales tradicionales (hasta 2022T3; después 'nivel 4')",
        "contratos",
    ),
    "capt_total": ("Total de contratos de captación (solo viene desde 2022T4)", "contratos"),
    "tarjetas_debito": ("Tarjetas de débito", "número"),
    "tarjetas_credito": ("Tarjetas de crédito", "contratos"),
    "cred_personal": ("Créditos personales", "contratos"),
    "cred_nomina": ("Créditos de nómina", "contratos"),
    "cred_abcd": ("Créditos ABCD (bienes de consumo duradero)", "contratos"),
    "cred_grupal": ("Créditos grupales", "contratos"),
    "cred_hipotecario": ("Créditos hipotecarios", "contratos"),
    "cred_automotriz": ("Créditos automotrices", "contratos"),
    "cred_consumo": ("Créditos al consumo (EACP)", "contratos"),
    "cred_vivienda": ("Créditos a la vivienda (EACP)", "contratos"),
    "cred_comercial": ("Créditos comerciales (EACP, desde 2022T4)", "contratos"),
    "cred_total": ("Total de contratos de crédito (solo viene desde 2022T4)", "contratos"),
    "usuarios_mujeres": ("Socias (SOCAP) / clientas (SOFIPO) / usuarias (EACP)", "personas"),
    "usuarios_hombres": ("Socios (SOCAP) / clientes (SOFIPO) / usuarios (EACP)", "personas"),
}
SECTORES_BDIF = {
    "todos": "Todos los sectores (banca múltiple + desarrollo + SOCAP + SOFIPO)",
    "banca": "Banca = múltiple + desarrollo combinadas (única desagregación antes de 2022T4 en captación/crédito/transacciones)",
    "banca_multiple": "Banca múltiple (comercial)",
    "banca_desarrollo": "Banca de desarrollo (Banco del Bienestar + Banjercito; no separables a nivel municipal)",
    "socap": "Sociedades Cooperativas de Ahorro y Préstamo",
    "sofipo": "Sociedades Financieras Populares",
    "eacp": "EACP = SOCAP + SOFIPO combinadas",
}
ERAS = [
    (
        "A",
        "2016T1–2017T4",
        "`BD Acceso Mun`, `BD Uso Mun`, `BD Uso EACP Mun`",
        "Encabezado plano (fila 8/9). Sucursales por sector; captación/crédito/transacciones solo 'Banca (Comercial y de Desarrollo)' y 'EACP'. 2016T1 usa 'Banca Comercial/Banca de Desarrollo/Cooperativas/Microfinancieras'; desde 2016T2 'Sucursales banca comercial/... Socap/... Sofipo'. Trae 'Superficie km2'. Cajeros y TPV sin sector.",
    ),
    (
        "B",
        "2018T1–2018T4",
        "`BD Acceso Mun`, `BD Uso Banca Mun`, `BD Uso EACP Mun`, `BD Género Mun`",
        "Encabezado en fila 12. Agrega población adulta por sexo y 'Módulos de atención Compartamos'. Mismo alcance sectorial que A.",
    ),
    (
        "C",
        "2019T1–2022T3",
        "`BD Infraestructura Mun`, `BD Tenencia Uso Banca Mun`, `BD Tenencia Uso EACP Mun`, `BD Género Mun`",
        "Encabezado en fila 12. Renombra hojas; agrega transacciones y usuarios (socios/clientes) para EACP. Desde 2020T2 'Cajeros automáticos' y 'Sucursales Banca comercial' (mayúscula). Mismo alcance sectorial que A/B.",
    ),
    (
        "D",
        "2022T4–2025T4",
        "`BD Infraestructura Mun`, `BD Captación Mun`, `BD Crédito Mun`, `BD por sexo Banca Mun`, `BD por sexo EACP Mun` (+ hojas por institución a nivel nacional desde 2023T3)",
        "Encabezado multinivel (filas 10–12): sector × bloque × variable. **Todo por sector** (banca múltiple, desarrollo, SOCAP, SOFIPO) y además totales 'Banca' y 'EACP'. Corresponsales solo total. Aparece 'Índice de rezago social' (2023T1). Población: 'Población total/adulta' (2022T4–2024T4) y 'Población/Población Adulta' (2025).",
    ),
]


def _tabla(df: pd.DataFrame, descripciones: dict[str, tuple[str, str]], fuente: str) -> list[str]:
    filas = ["| variable | descripción | tipo | unidad | fuente |", "|---|---|---|---|---|"]
    for c, dt in df.dtypes.items():
        desc, unidad = descripciones.get(c, ("", ""))
        filas.append(f"| `{c}` | {desc} | {dt} | {unidad} | {fuente} |")
    return filas


def bdif() -> None:
    cols = pd.read_csv(INTERIM / "cnbv_bdif_columnas.csv", dtype=str, keep_default_na=False)
    largo = pd.read_parquet(
        INTERIM / "cnbv_bdif.parquet", columns=["periodo", "sector", "variable"]
    )
    cobertura = (
        largo.drop_duplicates()
        .groupby(["sector", "variable"])["periodo"]
        .agg(["min", "max", "nunique"])
        .reset_index()
    )
    pob = pd.read_parquet(INTERIM / "cnbv_bdif_poblacion.parquet")
    L = [
        "# Diccionario: CNBV, BDIF municipal (`data/interim/cnbv_bdif.parquet`)\n",
        "Formato largo: una fila por municipio × trimestre × sector × variable. Solo conteos absolutos; los indicadores 'por cada 10 mil adultos' se descartan y se recalculan en el panel.\n",
        "## Columnas\n",
        "| variable | descripción | tipo | unidad | fuente |",
        "|---|---|---|---|---|",
        "| `cve_mun` | Clave municipal INEGI, texto de 5 dígitos | string | — | CNBV 'Clave Municipio' |",
        "| `periodo` | Trimestre `YYYYQn` (mes de cierre 03/06/09/12) | string | — | nombre del archivo |",
        "| `t` | Índice consecutivo, 2019Q1 = 1 (2016Q1 = −11) | int | — | derivado |",
        "| `sector` | Ver tabla de sectores | string | — | encabezado multinivel u hoja |",
        "| `variable` | Ver tabla de variables | string | — | encabezado |",
        "| `valor` | Valor numérico (NaN si la celda venía vacía o no numérica) | float | según variable | celda |",
        "| `hoja` | Hoja de origen en el Excel | string | — | — |",
        "| `archivo` | Archivo de origen | string | — | — |",
        "\n## Sectores\n",
        "| sector | significado |",
        "|---|---|",
    ]
    L += [f"| `{k}` | {v} |" for k, v in SECTORES_BDIF.items()]
    L += [
        "\n## Variables y cobertura temporal por sector\n",
        "| variable | descripción | unidad | sector | primer trimestre | último | n trimestres |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in cobertura.sort_values(["variable", "sector"]).itertuples():
        d, u = DESCRIPCIONES_BDIF.get(r.variable, ("", ""))
        L.append(f"| `{r.variable}` | {d} | {u} | `{r.sector}` | {r.min} | {r.max} | {r.nunique} |")
    L += [
        "\n## Eras de layout y cómo se unificaron\n",
        "| era | trimestres | hojas municipales | notas |",
        "|---|---|---|---|",
    ]
    L += [f"| {e} | {p} | {h} | {n} |" for e, p, h, n in ERAS]
    L += [
        "\nLa unificación la hace `proyecto.limpieza.bdif_columnas.clasificar`: normaliza el encabezado (minúsculas, sin acentos, sin sufijos 'Número de cuentas/créditos'), detecta el sector en los renglones superiores y el bloque (infraestructura/captación/crédito/transacciones) y asigna el nombre canónico. La bitácora completa columna por columna está en `data/interim/cnbv_bdif_columnas.csv`.\n",
        "## Encabezados originales por variable canónica\n",
        "| sector | variable | hoja | encabezado original (niveles → encabezado) | trimestres |",
        "|---|---|---|---|---|",
    ]
    usadas = cols[cols["variable"] != ""]
    g = (
        usadas.groupby(["sector", "variable", "hoja", "niveles", "encabezado"])["yyyymm"]
        .agg(["min", "max", "count"])
        .reset_index()
    )
    for r in g.sort_values(["variable", "sector", "min"]).itertuples():
        L.append(
            f"| `{r.sector}` | `{r.variable}` | {r.hoja} | {r.niveles} → {r.encabezado} | {r.min}–{r.max} ({r.count}) |"
        )
    L += [
        "\n## Columnas descartadas (no son conteos absolutos)\n",
        "| hoja | niveles → encabezado | trimestres |",
        "|---|---|---|",
    ]
    desc = (
        cols[cols["variable"] == ""]
        .groupby(["hoja", "niveles", "encabezado"])["yyyymm"]
        .agg(["min", "max", "count"])
        .reset_index()
    )
    L += [
        f"| {r.hoja} | {r.niveles} → {r.encabezado} | {r.min}–{r.max} ({r.count}) |"
        for r in desc.itertuples()
    ]
    L += [
        "\n# Diccionario: población BDIF (`data/interim/cnbv_bdif_poblacion.parquet`)\n",
        "Una fila por municipio-trimestre. La CNBV publica población y población adulta por municipio en cada base (fuente declarada en la 'Ficha técnica' de cada Excel: proyecciones CONAPO hasta 2022T3, valores con decimales; Censo 2020 desde 2022T4, enteros). Adulto = 18 años o más según la ficha técnica de la CNBV (confirmar en `docs/data_audit.md`).\n",
    ]
    L += _tabla(
        pob,
        {
            "cve_mun": ("Clave municipal", "—"),
            "periodo": ("Trimestre", "—"),
            "t": ("Índice", "—"),
            "poblacion": ("Población total", "personas"),
            "poblacion_adulta": ("Población adulta (18+)", "personas"),
            "poblacion_adulta_mujeres": ("Población adulta mujeres (desde 2018T1)", "personas"),
            "poblacion_adulta_hombres": ("Población adulta hombres (desde 2018T1)", "personas"),
            "tipo_poblacion": (
                "Clasificación CNBV: Rural, En transición, Semi-urbano, Urbano, Semi-metrópoli, Metrópoli",
                "categoría",
            ),
            "region": ("Región CNBV", "categoría"),
            "nom_ent": ("Entidad", "—"),
            "nom_mun": ("Municipio", "—"),
            "indice_rezago_social": ("Grado de rezago social CONEVAL (desde 2023T1)", "categoría"),
        },
        "CNBV",
    )
    (DICCIONARIOS / "cnbv_bdif.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def _simple(
    nombre: str, titulo: str, intro: str, tablas: list[tuple[str, dict]], fuente: str
) -> None:
    L = [f"# Diccionario: {titulo}\n", intro, ""]
    for archivo, desc in tablas:
        ruta = INTERIM / archivo
        if not ruta.exists():
            # Tablas que se generan más adelante en el pipeline (anillos, por ejemplo): se
            # documentan cuando existen, sin romper la generación del resto del diccionario.
            L += [f"## `data/interim/{archivo}` — aún no generada\n"]
            continue
        df = pd.read_parquet(ruta)
        L += [f"## `data/interim/{archivo}` ({len(df):,} filas)\n", *_tabla(df, desc, fuente), ""]
    (DICCIONARIOS / f"{nombre}.md").write_text("\n".join(L), encoding="utf-8")


def resto() -> None:
    _simple(
        "municipios",
        "catálogo de municipios y crosswalk",
        "Ver `crosswalk_municipios.md` para el método y los casos. Fuentes: MG 2024 (INEGI), wscatgeo (INEGI), BDIF (CNBV), ITER 2010/2020 (INEGI), IMM 2010/2015/2020 (CONAPO).",
        [
            (
                "municipios.parquet",
                {
                    "cve_mun": ("Clave municipal 5 dígitos", "—"),
                    "cve_ent": ("Clave de entidad", "—"),
                    "nom_mun": ("Nombre (MG 2024, o wscatgeo/BDIF si no está en MG)", "—"),
                    "nom_ent": ("Entidad", "—"),
                    "nom_cab": ("Cabecera municipal (wscatgeo)", "—"),
                    "pob_total_2020": ("Población censal 2020 (wscatgeo)", "personas"),
                    "en_mg2024": ("Tiene polígono en MG dic. 2024", "bool"),
                    "en_iter2010": ("Aparece en ITER 2010", "bool"),
                    "en_iter2020": ("Aparece en ITER 2020", "bool"),
                    "en_imm2010": ("Aparece en IMM 2010", "bool"),
                    "en_imm2015": ("Aparece en IMM 2015", "bool"),
                    "en_imm2020": ("Aparece en IMM 2020", "bool"),
                    "en_bdif": ("Aparece en algún trimestre BDIF 2016T1–2025T4", "bool"),
                    "bdif_desde": ("Primer trimestre en BDIF", "YYYYQn"),
                    "bdif_hasta": ("Último trimestre en BDIF", "YYYYQn"),
                    "bdif_t_min": ("t del primer trimestre", "—"),
                    "bdif_t_max": ("t del último", "—"),
                    "bdif_n_trimestres": ("Trimestres observados", "—"),
                    "bdif_completo": ("Observado en los 40 trimestres", "bool"),
                    "alta_estimada": (
                        "Primer trimestre BDIF si no estaba en 2016T1 (alta)",
                        "YYYYQn",
                    ),
                    "baja_estimada": (
                        "Último trimestre si desaparece y no está en MG 2024",
                        "YYYYQn",
                    ),
                },
            ),
            (
                "crosswalk_municipios.parquet",
                {
                    "cve_mun": ("Clave vigente (MG 2024)", "—"),
                    "nom_mun": ("Nombre", "—"),
                    "cve_ent": ("Entidad", "—"),
                    "cve_estable": (
                        "Clave de la unidad estable (municipio de 2010 del que proviene; igual a cve_mun si es estable)",
                        "—",
                    ),
                    "tipo": (
                        "estable | hijo | padre_donante | baja_sin_poligono_2024",
                        "categoría",
                    ),
                    "en_iter2010": ("Existía en 2010", "bool"),
                    "bdif_desde": ("Primer trimestre en BDIF", "YYYYQn"),
                    "alta_estimada": ("Alta estimada", "YYYYQn"),
                    "padre_espacial": (
                        "Clave 2010 con más población 2010 dentro del polígono 2024",
                        "—",
                    ),
                    "share_padre": (
                        "Participación del padre en la población 2010 del polígono",
                        "proporción",
                    ),
                    "n_loc_padre": ("Localidades 2010 del padre dentro del polígono", "—"),
                    "pob_2010_padre": ("Población 2010 de esas localidades", "personas"),
                    "otros_donantes_2010": (
                        "Otras claves 2010 con localidades dentro del polígono",
                        "—",
                    ),
                    "revisar": ("share_padre < 0.9 o sin padre", "bool"),
                },
            ),
        ],
        "INEGI/CNBV/CONAPO",
    )
    _simple(
        "babien",
        "Banco del Bienestar, directorio de sucursales (foto 1T 2026)",
        "Fuente: datos.gob.mx/dataset/sucursales (CC BY 4.0), copia manual en `data/manual/babien/`. No trae fecha de apertura: **no sirve para fechar el tratamiento**.",
        [
            (
                "babien.parquet",
                {
                    "id_sucursal": ("Identificador secuencial (orden del CSV)", "—"),
                    "nombre_institucion": ("Siempre 'Banco del Bienestar'", "—"),
                    "nombre_sucursal": ("Nombre comercial", "—"),
                    "domicilio": ("Domicilio completo", "—"),
                    "localidad": ("Localidad declarada", "—"),
                    "municipio_alcaldia": ("Municipio declarado (texto)", "—"),
                    "entidad": ("Entidad declarada (texto)", "—"),
                    "horario_publico": ("Horario", "—"),
                    "latitud": ("Latitud WGS84", "grados"),
                    "longitud": ("Longitud WGS84", "grados"),
                    "sin_coordenadas": ("Sin lat/lon válidas dentro de México", "bool"),
                    "cve_mun_espacial": (
                        "Municipio del polígono MG 2024 que contiene el punto (clave a usar)",
                        "—",
                    ),
                    "cve_mun_declarado": (
                        "Clave inferida por nombre entidad+municipio (solo validación)",
                        "—",
                    ),
                    "coincide": ("cve_mun_espacial == cve_mun_declarado", "bool"),
                },
            )
        ],
        "Banco del Bienestar",
    )
    _simple(
        "conapo",
        "CONAPO, marginación y proyecciones de población",
        "Marginación: IMM 2020 (Censo 2020) y series DP2 2010/2015. Proyecciones: reconstrucción 1990–2019 y proyección 2020–2040 por municipio, sexo y grupo quinquenal. Todas las variables originales se conservan con nombre en snake_case.",
        [
            (
                "conapo_marginacion.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "cve_ent": ("Entidad", "—"),
                    "nom_ent": ("Entidad", "—"),
                    "nom_mun": ("Municipio", "—"),
                    "anio": ("2010, 2015 o 2020", "—"),
                    "pob_tot": ("Población total", "personas"),
                    "im": ("Índice de marginación", "índice"),
                    "gm": ("Grado: Muy bajo, Bajo, Medio, Alto, Muy alto", "categoría"),
                    "imn": ("Índice normalizado 0–1", "índice"),
                    "analf": ("% población 15+ analfabeta", "%"),
                    "sbasc": ("% población 15+ sin educación básica", "%"),
                    "ovsde": ("% ocupantes en viviendas sin drenaje ni excusado", "%"),
                    "ovsee": ("% ocupantes en viviendas sin energía eléctrica", "%"),
                    "ovsae": ("% ocupantes en viviendas sin agua entubada", "%"),
                    "ovpt": ("% ocupantes en viviendas con piso de tierra", "%"),
                    "vhac": ("% viviendas con hacinamiento", "%"),
                    "pl_5000": ("% población en localidades < 5,000 hab.", "%"),
                    "po2sm": ("% población ocupada con ingreso hasta 2 salarios mínimos", "%"),
                },
            ),
            (
                "conapo_proyecciones_quinq.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "cve_ent": ("Entidad", "—"),
                    "nom_ent": ("Entidad", "—"),
                    "nom_mun": ("Municipio", "—"),
                    "sexo": ("HOMBRES / MUJERES", "—"),
                    "anio": ("Año (1 de julio)", "—"),
                    "pob_total": ("Población a mitad de año", "personas"),
                    "pob_15_mas": ("Población 15+ (suma de grupos)", "personas"),
                    "pob_18_mas_aprox": (
                        "Población 18+ aproximada: 15+ menos 3/5 del grupo 15–19 (el grupo exacto no existe)",
                        "personas",
                    ),
                },
            ),
            (
                "conapo_proyecciones_inddemo.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "anio": ("Año", "—"),
                    "pob_mit_mun": ("Población a mitad de año", "personas"),
                    "pob_015_64": ("Población 15–64", "personas"),
                    "edad_med": ("Edad mediana", "años"),
                    "raz_dep": ("Razón de dependencia", "por 100"),
                },
            ),
        ],
        "CONAPO",
    )
    _simple(
        "cnbv_portafolio",
        "CNBV Portafolio de Información, operativa de banca de desarrollo por institución; serie Bienestar sin Banjército",
        "Fuente: https://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/ (`BD_Operativa_YYYYMM.xls(x)`, 2016-01 – 2021-12). 'Bansefi' se renombra a 'Banco del Bienestar'. Ver `docs/data_audit.md` P2 para el método de la serie corregida.",
        [
            (
                "cnbv_portafolio_operativa.parquet",
                {
                    "yyyymm": ("Mes de la publicación", "YYYYMM"),
                    "periodo": (
                        "Trimestre BDIF si el mes es de cierre (03/06/09/12); nulo si no",
                        "YYYYQn",
                    ),
                    "cve_mun": ("Clave municipal (dígitos 4–8 de cve_inegi)", "—"),
                    "institucion": (
                        "Banco del Bienestar, Banjército, Banobras, Nafin, Bancomext, Sociedad Hipotecaria Federal",
                        "—",
                    ),
                    "producto": ("Producto/indicador operativo tal como lo publica la CNBV", "—"),
                    "valor": ("Suma de dat_num_total en el municipio", "número"),
                    "en_bdif": (
                        "True para Bienestar y Banjército (las dos instituciones que la BDIF cuenta como banca de desarrollo)",
                        "bool",
                    ),
                },
            ),
            (
                "banjercito_municipios.parquet",
                {
                    "cve_mun": ("Municipio con sucursal de Banjército en algún mes", "—"),
                    "meses_con_banjercito": ("Meses con sucursal (máx. 72)", "—"),
                    "primer_mes": ("Primer mes observado", "YYYYMM"),
                    "ultimo_mes": ("Último mes observado", "YYYYMM"),
                    "suc_banjercito_202112": ("Sucursales de Banjército en dic-2021", "número"),
                    "suc_bienestar_202112": ("Sucursales del Bienestar en dic-2021", "número"),
                    "solo_banjercito_202112": (
                        "Banjército presente y Bienestar ausente en dic-2021",
                        "bool",
                    ),
                },
            ),
            (
                "sucursales_bienestar.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "periodo": ("Trimestre", "YYYYQn"),
                    "t": ("Índice (2019Q1 = 1)", "—"),
                    "suc_bd_bdif": (
                        "Sucursales de banca de desarrollo según BDIF (Bienestar + Banjército)",
                        "número",
                    ),
                    "suc_banjercito": (
                        "Sucursales de Banjército: observadas 2016T1–2021T4, extrapoladas 2022+ (acotadas por suc_bd_bdif)",
                        "número",
                    ),
                    "suc_bienestar": (
                        "suc_bd_bdif − suc_banjercito; **define el tratamiento**",
                        "número",
                    ),
                    "fuente_banjercito": (
                        "portafolio | extrapolado_2021-12",
                        "categoría",
                    ),
                    "sospechoso_banjercito_nuevo": (
                        "Entra al tratamiento después de 2021T4 y el directorio Bienestar 2026 no respalda la sucursal (posible Banjército nuevo)",
                        "bool",
                    ),
                },
            ),
        ],
        "CNBV",
    )
    _simple(
        "denue",
        "INEGI, DENUE histórico (18 versiones semestrales 2016-01 – 2025-05) y tratamiento a nivel localidad",
        "Directorio de establecimientos georreferenciado. Se descarga por streaming (el crudo no se conserva: 13 GB contra 16 GB libres) y se agrega a localidad, municipio y anillos. Los bloques temáticos **no son excluyentes**: una farmacia cuenta en `consumo` y en `salud`, y todo establecimiento cuenta en `emprendimiento`. Clasificación SCIAN en `limpieza/denue_clasificacion.py`.\n\n**El DENUE cuenta establecimientos, no sucursales regulatorias**: en 2016 registra 23,437 unidades de banca múltiple contra las ~13,000 sucursales que reporta la CNBV, porque incluye cajeros y módulos. Es una medida de presencia a nivel localidad, no comparable en niveles con la BDIF.\n\n**Los archivos grandes vienen partidos** por el INEGI en bloques de 520,000 registros (sectores 72 y 81 desde 2019-11): se descargan todas las partes, así que los totales están completos.",
        [
            (
                "denue_localidad.parquet",
                {
                    "cve_loc": ("Clave de localidad de 9 dígitos (ent 2 + mun 3 + loc 4)", "—"),
                    "cve_mun": ("Clave municipal", "—"),
                    "version": ("Versión del DENUE (AAAA_MM)", "—"),
                    "semestre": ("Semestre calendario de la versión", "YYYYSn"),
                    "s": ("Índice de semestre (2016S1 = 1)", "—"),
                    "bloque": ("emprendimiento | consumo | salud | financiero", "categoría"),
                    "clase": (
                        "Clase fina dentro del bloque (farmacia, restaurantes, banca_multiple, ...)",
                        "categoría",
                    ),
                    "n_estab": ("Establecimientos", "número"),
                    "n_micro": (
                        "Establecimientos de 0 a 5 personas (proxy de micronegocio / autoempleo)",
                        "número",
                    ),
                    "empleo_est": (
                        "Empleo estimado con el punto medio del rango de personas ocupadas",
                        "personas",
                    ),
                },
            ),
            (
                "denue_municipio.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "version": ("Versión del DENUE", "—"),
                    "semestre": ("Semestre", "YYYYSn"),
                    "s": ("Índice de semestre", "—"),
                    "bloque": ("Bloque temático", "categoría"),
                    "clase": ("Clase fina", "categoría"),
                    "n_estab": ("Establecimientos", "número"),
                    "n_micro": ("Micronegocios", "número"),
                    "empleo_est": ("Empleo estimado", "personas"),
                },
            ),
            (
                "denue_cobertura.parquet",
                {
                    "version": ("Versión del DENUE", "—"),
                    "semestre": ("Semestre", "YYYYSn"),
                    "establecimientos": (
                        "Total nacional de la versión (control de calidad)",
                        "número",
                    ),
                    "localidades": ("Localidades con al menos un establecimiento", "número"),
                    "municipios": ("Municipios con al menos un establecimiento", "número"),
                    "sectores_procesados": ("Archivos sectoriales agregados", "número"),
                    "sectores_esperados": (
                        "Archivos que publica el INEGI en esa versión",
                        "número",
                    ),
                    "completa": (
                        "True si se procesaron todos los sectores; si no, no usar en el panel",
                        "bool",
                    ),
                },
            ),
            (
                "tratamiento_localidad.parquet",
                {
                    "cve_loc": ("Localidad con sucursal del Banco del Bienestar", "—"),
                    "cve_mun": ("Municipio", "—"),
                    "nom_loc": ("Nombre de la localidad", "—"),
                    "n_sucursales_loc": ("Sucursales asignadas a la localidad", "número"),
                    "n_sucursales_mun": ("Sucursales en todo el municipio", "número"),
                    "dist_sucursal_km": (
                        "Distancia entre la sucursal y el punto de la localidad asignada",
                        "km",
                    ),
                    "G_trimestre": (
                        "Primer trimestre con sucursal (BDIF municipal, neta de Banjército)",
                        "YYYYQn",
                    ),
                    "G_semestre": ("Lo mismo en semestres", "YYYYSn"),
                    "g_s": ("Índice del semestre de apertura; 0 si no aplica", "—"),
                    "fecha_ambigua": (
                        "El municipio tiene 2+ sucursales, así que la fecha no identifica a esta localidad",
                        "bool",
                    ),
                    "ya_tratado_inicio": (
                        "El municipio ya tenía sucursal en el primer periodo (herencia Bansefi)",
                        "bool",
                    ),
                    "sospechoso_banjercito": (
                        "Posible sucursal nueva de Banjército (ver auditoría P2)",
                        "bool",
                    ),
                    "pobtot": ("Población de la localidad (Censo 2020)", "personas"),
                    "lat": ("Latitud de la localidad", "grados"),
                    "lon": ("Longitud", "grados"),
                },
            ),
            (
                "anillos.parquet",
                {
                    "cve_loc": ("Centro del anillo (localidad)", "—"),
                    "radio_km": ("Radio", "km"),
                    "version": ("Versión del DENUE", "—"),
                    "bloque": ("Bloque temático", "categoría"),
                    "n_estab": ("Establecimientos dentro del radio", "número"),
                    "n_micro": ("Micronegocios dentro del radio", "número"),
                    "empleo_est": ("Empleo estimado dentro del radio", "personas"),
                },
            ),
        ],
        "INEGI",
    )
    _simple(
        "inegi_censo",
        "INEGI, Censo 2020 y 2010 (ITER)",
        "Totales municipales (`LOC == 0000`) con todas las variables del ITER; diccionario oficial en `data/raw/inegi_censo/fd_iter_cpv2020.pdf` y en el zip de 2010. `*` y `N/D` son faltantes. Localidades con coordenadas decimales para cruces espaciales.",
        [
            (
                "inegi_censo_2020.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "pobtot": ("Población total", "personas"),
                    "p_18ymas": ("Población 18+", "personas"),
                    "p_15ymas": ("Población 15+", "personas"),
                },
            ),
            (
                "inegi_censo_2010.parquet",
                {
                    "cve_mun": ("Clave municipal", "—"),
                    "pobtot": ("Población total", "personas"),
                    "p_18ymas": ("Población 18+", "personas"),
                },
            ),
            (
                "inegi_censo_localidades_2010.parquet",
                {
                    "cve_mun": ("Clave municipal 2010", "—"),
                    "cve_loc": ("Clave de localidad", "—"),
                    "lon": ("Longitud decimal (de DDMMSS)", "grados"),
                    "lat": ("Latitud decimal", "grados"),
                    "pobtot": ("Población 2010", "personas"),
                },
            ),
            (
                "inegi_censo_localidades_2020.parquet",
                {
                    "cve_mun": ("Clave municipal 2020", "—"),
                    "cve_loc": ("Clave de localidad", "—"),
                    "lon": ("Longitud decimal (de DMS)", "grados"),
                    "lat": ("Latitud decimal", "grados"),
                    "pobtot": ("Población 2020", "personas"),
                },
            ),
        ],
        "INEGI",
    )


def generar() -> None:
    DICCIONARIOS.mkdir(parents=True, exist_ok=True)
    bdif()
    resto()
    log.info("diccionarios escritos en %s", DICCIONARIOS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generar()

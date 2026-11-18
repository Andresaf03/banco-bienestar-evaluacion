"""Tablas en Markdown para el trabajo final y la presentación (Quarto).

Lee las salidas de la batería (`outputs/tablas/`) y escribe una tabla por archivo en
`entregables/_tablas/`, que los `.qmd` incluyen con `{{< include >}}`. Así ninguna cifra del
documento se copia a mano: si la batería cambia, `make entregables` regenera las tablas.

No estima nada. Convenciones: efecto en % de la media previa de las tratadas (en los resultados en
logaritmo, 100 × puntos log); "se descarta más de" es el mayor valor absoluto del IC al 90% en esa
escala. Cada efecto y su error estándar se redondean a dos cifras significativas del error estándar
(Nikolov 2022), para no reportar precisión falsa.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from proyecto.utils.io import TABLAS, ruta

log = logging.getLogger(__name__)
DESTINO = ruta("entregables", "_tablas")

FINANCIERA = [
    ("principal", "sucursales_privado_pc", "Sucursales privadas (BM + EACP)"),
    ("principal", "sucursales_bm_pc", "Sucursales de banca múltiple"),
    ("principal", "sucursales_eacp_pc", "Sucursales de EACP"),
    ("hasta_2025", "sucursales_privado_pc", "Sucursales privadas, hasta 2025T4"),
    ("panel_corto", "captacion_privado_pc", "Contratos de captación privados (2022T4+)"),
    ("panel_corto", "credito_privado_pc", "Contratos de crédito privados (2022T4+)"),
    ("eacp", "capt_ahorro_eacp_pc", "Captación de ahorro de EACP"),
    ("eacp", "cred_consumo_eacp_pc", "Crédito al consumo de EACP"),
]
# Especificación de CS con la que se compara cada serie apilada.
APILADO_CS = {
    ("hasta_2025", "sucursales_privado_pc"),
    ("eacp", "capt_ahorro_eacp_pc"),
    ("eacp", "cred_consumo_eacp_pc"),
}
PRIMERA_ETAPA = [
    ("sucursales_total_pc", "Sucursales totales (incluye al banco)"),
    ("capt_total_bd_pc", "Contratos de captación del banco (2022T4+)"),
    ("tarjetas_debito_bd_pc", "Tarjetas de débito del banco (2022T4+)"),
]
ACTIVIDAD = [
    ("principal", "localidad", "estab_emprendimiento_pc", "Establecimientos", "DENUE"),
    ("principal", "localidad", "micro_emprendimiento_pc", "Micronegocios, 0–5 personas", "DENUE"),
    ("principal", "localidad", "empleo_est_emprendimiento_pc", "Empleo estimado", "DENUE"),
    ("principal", "localidad", "estab_consumo_pc", "Comercio y alimentos", "DENUE"),
    ("principal", "localidad", "estab_salud_pc", "Salud", "DENUE"),
    ("ce", "municipio_ce", "ue_pc", "Unidades económicas", "CE"),
    ("ce", "municipio_ce", "personal_ocupado_pc", "Personal ocupado", "CE"),
    ("ce", "municipio_ce", "log_vacb", "Valor agregado, log", "CE"),
    ("imss", "municipio_trim", "ta_pc", "Puestos afiliados", "IMSS"),
    ("imss", "municipio_trim", "log_salario_diario", "Salario diario, log", "IMSS"),
]
BANDAS = ["sucursal propia", "0–2 km", "2–5 km", "5–10 km"]


MENOS = "\u2212"  # signo menos tipográfico: no permite cortar la línea entre el signo y el número
Z90 = 1.644854  # cuantil 0.95 de la normal: intervalo al 90%, como `ic90_*` en tabla_final


def _num(v: float, d: int = 3) -> str:
    return "" if pd.isna(v) else f"{v:,.{d}f}".replace("-", MENOS)


def _pct(v: float) -> str:
    return "" if pd.isna(v) else f"{v:+.1f}%".replace("-", MENOS)


def _p(v: float) -> str:
    if pd.isna(v):
        return ""
    return "<0.001" if v < 0.001 else f"{v:.3f}"


def _decimales(ee: float) -> int:
    """Decimales que dejan dos cifras significativas del error estándar (0.083 → 3, 1.10 → 1,
    165 → 0): el efecto se redondea a la misma posición."""
    if pd.isna(ee) or ee == 0:
        return 3
    return max(0, min(4, 1 - int(math.floor(math.log10(abs(ee))))))


def _con_ee(v: float, ee: float) -> str:
    d = _decimales(ee)
    return f"{_num(v, d)} ({_num(ee, d)})"


def _media(v: float) -> str:
    """Media previa con dos o tres cifras significativas."""
    if pd.isna(v):
        return ""
    return _num(v, 2 if abs(v) < 10 else 1 if abs(v) < 100 else 0)


def _n(r: pd.Series) -> str:
    # Espacios duros: el par tratados / controles no se parte entre renglones.
    return f"{int(r['n_tratadas']):,}\u00a0/\u00a0{int(r['n_controles']):,}"


def _md(filas: list[list[str]], columnas: list[str], alinear: str | None = None) -> str:
    """Tabla pipe de Pandoc. Cuando una línea excede el ancho de texto, Pandoc reparte el ancho de
    las columnas en proporción a los guiones del separador: se ponen tantos como el contenido más
    largo de cada columna (sin esto las columnas salen iguales y la de nombres queda aplastada)."""
    alinear = alinear or "l" + "r" * (len(columnas) - 1)
    # Columnas de texto con tope (el texto se parte en líneas); numéricas con mínimo (no se parten).
    anchos = [
        min(26, max(len(f[j]) for f in filas))
        if al == "l"
        else max(10, max(len(f[j]) for f in filas))
        for j, al in enumerate(alinear)
    ]
    sep = [
        "-" * (a - 1) + ":" if al == "r" else ":" + "-" * (a - 1)
        for a, al in zip(anchos, alinear, strict=True)
    ]
    lineas = ["| " + " | ".join(columnas) + " |", "|" + "|".join(sep) + "|"]
    lineas += ["| " + " | ".join(f) + " |" for f in filas]
    return "\n".join(lineas) + "\n"


def _fila(t: pd.DataFrame, **filtro: str) -> pd.Series | None:
    m = pd.Series(True, index=t.index)
    for k, v in filtro.items():
        m &= t[k] == v
    sub = t[m]
    return None if sub.empty else sub.iloc[0]


def _cota(r: pd.Series) -> str:
    return _pct(r["cota_equivalencia_pct"]).lstrip("+").replace("%", "") + "%"


# Estadísticas descriptivas en 2019T1: (variable, etiqueta, escala, decimales).
DESCRIPTIVAS = [
    ("sucursales_privado_pc", "Sucursales privadas por 10 mil adultos", 1, 2),
    ("sucursales_bm_pc", "Sucursales de banca múltiple por 10 mil adultos", 1, 2),
    ("sucursales_eacp_pc", "Sucursales de EACP por 10 mil adultos", 1, 2),
    ("poblacion_2020", "Población 2020 (miles)", 1e-3, 1),
    ("poblacion_adulta_fija", "Población adulta, 2022T4 (miles)", 1e-3, 1),
    ("indice_marginacion_2020", "Índice de marginación 2020", 1, 1),
    ("banca_mun_2019", "Con banca múltiple en 2019T1 (%)", 100, 1),
]


def tabla_descriptivas(desc: pd.DataFrame) -> str:
    """Media (desviación estándar) en 2019T1 de tratados y controles de la muestra financiera, y la
    diferencia estandarizada entre ambos grupos."""
    if desc.empty:
        return ""
    filas = []
    for variable, nombre, escala, d in DESCRIPTIVAS:
        t = _fila(desc, variable=variable, grupo="tratados")
        c = _fila(desc, variable=variable, grupo="controles")
        if t is None or c is None:
            continue
        dif = (t["media"] - c["media"]) / math.sqrt((t["de"] ** 2 + c["de"] ** 2) / 2)
        filas.append(
            [
                nombre,
                f"{_num(escala * t['media'], d)} ({_num(escala * t['de'], d)})",
                f"{_num(escala * c['media'], d)} ({_num(escala * c['de'], d)})",
                _num(dif, 2),
            ]
        )
    n = desc.drop_duplicates("grupo").set_index("grupo")["n"]
    filas.append(["Municipios", f"{int(n['tratados']):,}", f"{int(n['controles']):,}", ""])
    return _md(
        filas,
        ["Variable", "Tratados: media (de)", "Controles: media (de)", "Diferencia estandarizada"],
    )


def tabla_financiera(t: pd.DataFrame, apilado: pd.DataFrame) -> str:
    filas = []
    for variante, resultado, nombre in FINANCIERA:
        r = _fila(t, variante=variante, panel="municipio_trim", resultado=resultado)
        if r is None:
            continue
        a = None
        if (variante, resultado) in APILADO_CS and not apilado.empty:
            a = _fila(apilado, resultado=resultado, controles="limpios (nunca + aún no tratados)")
        filas.append(
            [
                nombre,
                _con_ee(r["valor"], r["ee"]),
                _pct(r["efecto_pct"]),
                "±" + _cota(r),
                _p(r["pre_wald_p"]),
                _p(r.get("p_rw")),
                "" if a is None else f"{_pct(a['efecto_pct'])} ({_p(a['pre_wald_p'])})",
                _n(r),
            ]
        )
    return _md(
        filas,
        [
            "Variable dependiente",
            "Efecto (ee)",
            "% de la media",
            "Se descarta más de",
            "Previos (p)",
            "p (RW)",
            "DiD apilado: % (previos p)",
            "Tratados / controles",
        ],
    )


def tabla_primera_etapa(t: pd.DataFrame) -> str:
    filas = []
    for resultado, nombre in PRIMERA_ETAPA:
        r = _fila(t, variante="primera_etapa", resultado=resultado)
        if r is None:
            continue
        filas.append(
            [
                nombre,
                _con_ee(r["valor"], r["ee"]),
                _media(r["media_base"]),
                _p(r["pre_wald_p"]),
                _n(r),
            ]
        )
    return _md(
        filas,
        [
            "Variable dependiente",
            "Efecto (ee)",
            "Media previa",
            "Previos (p)",
            "Tratados / controles",
        ],
    )


def tabla_actividad(t: pd.DataFrame) -> str:
    filas = []
    for variante, panel, resultado, nombre, fuente in ACTIVIDAD:
        r = _fila(t, variante=variante, panel=panel, resultado=resultado)
        if r is None:
            continue
        d = _decimales(r["ee"])
        honest = (
            ""
            if pd.isna(r.get("honest_lb_m1"))
            else f"[{_num(r['honest_lb_m1'], d)}, {_num(r['honest_ub_m1'], d)}]"
        )
        placebo = "" if pd.isna(r.get("placebo")) else _con_ee(r["placebo"], r["placebo_ee"])
        filas.append(
            [
                f"{nombre} ({fuente})",
                _con_ee(r["valor"], r["ee"]),
                _pct(r["efecto_pct"]),
                placebo,
                _p(r["pre_wald_p"]),
                honest,
                _n(r),
            ]
        )
    return _md(
        filas,
        [
            "Variable dependiente (fuente)",
            "Efecto (ee)",
            "% de la media",
            "Placebo 2019 (ee)",
            "Previos (p)",
            "IC robusto ($\\bar M = 1$)",
            "Tratados / controles",
        ],
    )


def tabla_denue_espacial(resultado: str = "estab_emprendimiento_pc") -> str:
    dec = _leer(f"decaimiento_{resultado}.csv")
    reg = _leer(f"regimen_{resultado}.csv")
    if dec.empty or reg.empty:
        return ""
    reg_total = reg[reg["regimen"] == "recorrido_total"]
    filas = []
    for banda in BANDAS:
        a = _fila(dec, banda=banda)
        b = _fila(reg_total, banda=banda)
        filas.append(
            [
                "Con sucursal" if banda == "sucursal propia" else f"Vecina a {banda}",
                "" if a is None else f"{int(a['tratadas']):,}",
                "" if a is None else _pct(a["efecto_pct"]),
                "" if a is None else _p(a["pre_wald_p"]),
                "" if b is None else f"{int(b['tratadas']):,}",
                "" if b is None else _pct(b["efecto_pct"]),
                "" if b is None else _p(b["pre_wald_p"]),
            ]
        )
    return _md(
        filas,
        [
            "Localidades",
            "N (todas)",
            "% de la media",
            "Previos (p)",
            "N (recorrido total)",
            "% de la media",
            "Previos (p)",
        ],
    )


# Decisiones discrecionales (Simmons et al. 2011): (archivo rob_*, título del panel, [(variante, etiqueta)]).
DECISIONES = [
    (
        "rob_municipio_trim_esc_sucursales_privado_pc.csv",
        "*A. Sucursales privadas (BDIF)*",
        [
            ("base (aún no tratados, δ=0, DR)", "Especificación principal"),
            ("sin covariables", "Sin covariables"),
            ("solo nunca tratados como control", "Solo nunca tratados como comparación"),
            ("anticipación δ=1", "Anticipación de un trimestre"),
            ("incluye fechas ambiguas y sospechosas", "Con las 8 fechas dudosas por Banjército"),
            (
                "incluye cohortes de menos de 5 unidades",
                "Con las cohortes de menos de 5 municipios",
            ),
            ("sin municipios con cierres (P-9)", "Sin los municipios con cierres"),
        ],
    ),
    (
        "rob_localidad_act_estab_emprendimiento_pc.csv",
        "*B. Establecimientos (DENUE)*",
        [
            ("base (≥10 km, DR, cluster municipal)", "Especificación principal"),
            ("sin covariables", "Sin covariables"),
            ("sin nivel previo del resultado", "Sin el nivel previo de establecimientos"),
            ("controles: dist5", "Controles a 5 km o más"),
            ("controles: dist20", "Controles a 20 km o más"),
            ("controles: municipal", "Controles en municipios sin aperturas"),
            ("controles: todos", "Todas las localidades sin sucursal"),
            ("piso simétrico de 1,000 habitantes", "Localidades de 1,000 habitantes o más"),
            ("incluye fechas ambiguas y sospechosas", "Con las fechas de apertura ambiguas"),
            ("muestra emparejada (matching)", "Muestra emparejada"),
            ("post en 2025S1", "Medido en 2025S1"),
        ],
    ),
]


def tabla_decisiones() -> str:
    """Cómo cambian los dos resultados principales con cada decisión discrecional: covariables,
    grupo de comparación y observaciones excluidas, en % de la media previa de cada variante."""
    filas = []
    for archivo, titulo, variantes in DECISIONES:
        rob = _leer(archivo)
        if rob.empty:
            continue
        filas.append([titulo, "", "", "", ""])
        for variante, etiqueta in variantes:
            r = _fila(rob, variante=variante)
            if r is None:
                continue
            escala = 100 / r["media_base"]
            bajo, alto = (r["att"] + z * r["ee"] for z in (-Z90, Z90))
            ic = f"[{_num(escala * bajo, 1)}, {_num(escala * alto, 1)}]"
            filas.append(
                [
                    etiqueta,
                    _pct(escala * r["att"]),
                    ic,
                    _p(r["pre_wald_p"]),
                    f"{int(r['tratadas']):,} / {int(r['controles']):,}",
                ]
            )
    if not filas:
        return ""
    return _md(
        filas,
        ["Especificación", "% de la media", "IC al 90%", "Previos (p)", "Tratados / controles"],
    )


def tabla_heterogeneidad(het: pd.DataFrame) -> str:
    casos = [
        ("localidad", "estab_emprendimiento_pc", "Establecimientos (DENUE)"),
        ("localidad", "estab_consumo_pc", "Comercio y alimentos (DENUE)"),
        ("municipio_trim", "sucursales_privado_pc", "Sucursales privadas (BDIF)"),
        ("municipio_trim", "cred_consumo_eacp_pc", "Crédito al consumo EACP (BDIF)"),
        ("municipio_ce", "ue_pc", "Unidades económicas (CE)"),
    ]
    filas = []
    for panel, resultado, nombre in casos:
        sub = het[
            (het["panel"] == panel)
            & (het["resultado"] == resultado)
            & (het["dimension"] == "desierto_bancario")
        ]
        con = sub[sub["grupo"].astype(str) == "0"]
        sin = sub[sub["grupo"].astype(str) == "1"]
        if con.empty or sin.empty:
            continue
        c, s = con.iloc[0], sin.iloc[0]
        filas.append(
            [
                nombre,
                _con_ee(c["att"], c["ee"]),
                _con_ee(s["att"], s["ee"]),
                _num(s["dif_vs_ref"], _decimales(max(c["ee"], s["ee"]))),
                _p(s["q_dif"]),
            ]
        )
    return _md(
        filas,
        [
            "Variable dependiente",
            "Con banca múltiple en 2019 (ee)",
            "Desierto bancario (ee)",
            "Diferencia",
            "q ajustado (BH)",
        ],
    )


# Fase 2 (preregistro del 2026-10-07): las filas que van al anexo del trabajo final y a la lámina de
# respaldo, en este orden: (familia, resultado, nombre, fuente).
FASE2 = [
    ("eic", "pct_negocio", "Dueños de negocio (patrón o cuenta propia)", "EIC"),
    ("eic", "pct_ocupacion", "Tasa de ocupación", "EIC"),
    ("eic", "log_ingreso_trabajo", "Ingreso por trabajo (log)", "EIC"),
    ("eic_mecanismo", "pct_hog_programas", "Hogares con programas de gobierno", "EIC"),
    ("viirs", "log1p_luz_1km", "Luz nocturna a 1 km (log)", "VIIRS"),
    ("efipem", "log_impuestos_pc", "Impuestos municipales por habitante (log)", "EFIPEM"),
    ("enoe", "pct_negocio", "Dueños de negocio (trimestral)", "ENOE"),
]


def tabla_fase2(resumen: pd.DataFrame) -> str:
    """Anexo de la fase 2: efecto, % de la media (puntos log ×100 en los logaritmos), cota de
    equivalencia, pre-prueba y la lectura con los criterios preregistrados."""
    if resumen.empty:
        return ""
    filas = []
    for familia, resultado, nombre, fuente in FASE2:
        r = _fila(resumen, familia=familia, resultado=resultado)
        if r is None:
            continue
        filas.append(
            [
                f"{nombre}, {fuente}",
                _con_ee(r["valor"], r["ee"]),
                _pct(r["efecto_pct"]),
                _cota(r),
                _p(r["pre_wald_p"]),
                str(r["lectura"]).split(" (")[0],
            ]
        )
    return _md(
        filas,
        [
            "Resultado y fuente",
            "Efecto (ee)",
            "% de la media",
            "Se descarta más de",
            "Previos (p)",
            "Lectura",
        ],
        alinear="lrrrrl",
    )


# Fase 3 (preregistro del 2026-10-11): (familia, resultado, nombre, fuente).
FASE3 = [
    ("delitos", "tasa_robo_transeunte", "Robo a transeúnte", "SESNSP"),
    ("delitos", "tasa_robo_negocio", "Robo a negocio", "SESNSP"),
    ("delitos", "tasa_extorsion", "Extorsión", "SESNSP"),
    ("delitos", "tasa_robo_total", "Robo total", "SESNSP"),
    ("delitos", "tasa_homicidio_doloso", "Homicidio doloso", "SESNSP"),
    ("delitos_secundarios", "tasa_dano_propiedad", "Daño a la propiedad (placebo)", "SESNSP"),
    ("elecciones", "pct_participacion", "Participación", "INE"),
    ("elecciones", "pct_bloque_gobierno", "Voto Morena + PT + PVEM", "INE"),
    ("elecciones_secundarios", "pct_morena", "Voto Morena", "INE"),
    ("elecciones_secundarios", "pct_nulos", "Votos nulos", "INE"),
]
# Robustez preregistrada que se muestra junto a la principal: el resultado neto de la media estado ×
# elección absorbe la concurrencia con elecciones locales.
FASE3_NETO = "resultado neto de la media estado × elección"


def _lectura(att: float, ee: float, media: float, wald_p: float, sesoi: float = 5.0) -> str:
    """Lectura con los criterios del proyecto, sin corrección múltiple (para filas de robustez)."""
    z = att / ee
    p = math.erfc(abs(z) / math.sqrt(2))
    cota = 100 * (abs(att) + 1.6448536 * ee) / abs(media)
    if not pd.isna(wald_p) and wald_p < 0.05:
        return "descriptivo"
    if p >= 0.05 and cota <= sesoi:
        return "nulo informativo"
    return "significativo" if p < 0.05 else "no informativo"


def tabla_fase3(resumen: pd.DataFrame, extras: dict[str, pd.DataFrame]) -> str:
    """Anexo de la fase 3: como el de la fase 2, más la variante neta de estado × elección de los
    dos resultados electorales principales."""
    if resumen.empty:
        return ""
    filas = []
    for familia, resultado, nombre, fuente in FASE3:
        r = _fila(resumen, familia=familia, resultado=resultado)
        if r is None:
            continue
        filas.append(
            [
                f"{nombre}, {fuente}",
                _con_ee(r["valor"], r["ee"]),
                _pct(r["efecto_pct"]),
                _cota(r),
                _p(r["pre_wald_p"]),
                str(r["lectura"]).split(" (")[0],
            ]
        )
        extra = extras.get(resultado, pd.DataFrame())
        n = _fila(extra, variante=FASE3_NETO) if not extra.empty else None
        if n is not None:
            cota = 100 * (abs(n["att"]) + 1.6448536 * n["ee"]) / abs(n["media_base"])
            filas.append(
                [
                    f"{nombre}, neto de estado × elección",
                    _con_ee(n["att"], n["ee"]),
                    _pct(n["efecto_pct"]),
                    f"{cota:.1f}%",
                    _p(n["pre_wald_p"]),
                    _lectura(n["att"], n["ee"], n["media_base"], n["pre_wald_p"]),
                ]
            )
    return _md(
        filas,
        [
            "Resultado y fuente",
            "Efecto (ee)",
            "% de la media",
            "Se descarta más de",
            "Previos (p)",
            "Lectura",
        ],
        alinear="lrrrrl",
    )


CALENDARIO = [
    ("log_poblacion_2020", "Población 2020 (log)"),
    ("indice_marginacion_2020", "Índice de marginación 2020"),
    ("banca_mun_2019", "Banca múltiple en 2019T1"),
    ("nivel_2019", "Sucursales privadas por 10 mil adultos, 2019T1"),
]


def tabla_calendario(cal: pd.DataFrame) -> str:
    """Predictores del calendario de aperturas: meses de adelanto (−) o atraso (+) de la apertura por
    desviación estándar de cada covariable, sin y con efectos fijos de estado (descriptivo)."""
    if cal.empty:
        return ""
    modelos = ["sin efectos fijos", "efectos fijos de estado"]
    filas = []
    for termino, nombre in CALENDARIO:
        celdas = [nombre]
        for m in modelos:
            r = _fila(cal, modelo=m, termino=termino)
            celdas.append(
                ""
                if r is None
                else f"{_num(round(r['meses'], 1) + 0.0, 1)} ({_num(12 * r['ee'], 1)})"
            )
        filas.append(celdas)
    pie = {m: cal[cal["modelo"] == m].iloc[0] for m in modelos}
    filas.append(["Municipios", *(f"{int(pie[m]['n']):,}" for m in modelos)])
    filas.append(["R²", *(_num(pie[m]["r2"], 3) for m in modelos)])
    filas.append(["Wald conjunta p", *(_p(pie[m]["wald_p"]) for m in modelos)])
    return _md(filas, ["Predictor", "Meses, sin efectos fijos", "Meses, efectos fijos de estado"])


# Fase 4 (preregistro del 2026-10-14). Estimadores en el orden de la tabla: (estimador en
# `fase4_estimadores.csv`, nombre en la tabla).
FASE4_ESTIMADORES = [
    ("Callaway y Sant'Anna", "Callaway y Sant'Anna (principal)"),
    ("TWFE estático", "TWFE estático"),
    ("TWFE estudio de evento (promedio e = 0…8)", "Estudio de evento TWFE (promedio post)"),
    ("Sun y Abraham", "Sun y Abraham"),
    ("Borusyak et al.", "Borusyak et al."),
    ("DiD apilado, id^pila + e", "DiD apilado"),
    ("DiD apilado, id^pila + e^cve_ent^pila", "DiD apilado, estado × evento"),
    ("TWFE extendido (Wooldridge) sin covariables", "TWFE extendido, sin covariables"),
    ("TWFE extendido (Wooldridge)", "TWFE extendido, con covariables"),
    (
        "TWFE extendido con covariables, solo municipios que abren",
        "TWFE extendido, con covariables, solo los que abren (hasta 2023T4)",
    ),
]
FASE4_FINANCIERA = [
    ("sucursales_privado_pc", "Privadas"),
    ("sucursales_bm_pc", "Banca múltiple"),
    ("sucursales_eacp_pc", "EACP"),
]


def tabla_fase4_estimadores(est: pd.DataFrame) -> str:
    """0.5 Triangulación: el efecto en % de la media previa y su IC al 90%, por estimador."""
    if est.empty:
        return ""
    filas = []
    for estimador, nombre in FASE4_ESTIMADORES:
        celdas = [nombre]
        for resultado, _ in FASE4_FINANCIERA:
            r = _fila(est, resultado=resultado, estimador=estimador)
            celdas.append(
                ""
                if r is None
                else f"{_pct(r['efecto_pct'])} [{_num(r['ic90_bajo'], 1)}, {_num(r['ic90_alto'], 1)}]"
            )
        filas.append(celdas)
    return _md(filas, ["Estimador", *(n for _, n in FASE4_FINANCIERA)], alinear="lrrr")


def _fila_prueba(nombre: str, att: float, ee: float, media: float, wald_p: float) -> list[str]:
    cota = 100 * (abs(att) + 1.6448536 * ee) / abs(media)
    return [
        nombre,
        _con_ee(att, ee),
        _pct(100 * att / abs(media)),
        f"{cota:.1f}%",
        _p(wald_p),
        _lectura(att, ee, media, wald_p),
    ]


def tabla_fase4(
    resumen: pd.DataFrame,
    controles: pd.DataFrame,
    extra: dict[str, pd.DataFrame],
) -> str:
    """Pruebas de la fase 4 sobre sucursales privadas, bancarización y uso privado."""
    if resumen.empty:
        return ""
    priv = "sucursales_privado_pc"
    filas = []
    for variante, nombre in [
        (
            "H1c solo municipios que alguna vez abren",
            "Solo municipios que alguna vez abren (hasta 2023T4)",
        ),
        ("H1d nunca tratados emparejados (PS 1:1, región)", "Nunca tratados emparejados"),
        ("H1e apilado, controles sin vecino con apertura nueva", "Controles sin vecino que abra"),
    ]:
        r = _fila(controles, resultado=priv, variante=variante)
        if r is not None:
            filas.append(_fila_prueba(nombre, r["att"], r["ee"], r["media_base"], r["pre_wald_p"]))
    h2 = controles[(controles["resultado"] == priv) & controles["variante"].str.startswith("H2")]
    if not h2.empty:
        pct = 100 * h2["att"] / h2["media_base"].abs()
        filas.append(
            [
                "Covariables una por una (6 variantes)",
                "",
                f"{_pct(pct.min())} a {_pct(pct.max())}",
                "",
                "",
                "",
            ]
        )
    for variante, resultado, nombre in [
        ("A1b", priv, "Derrame en municipios vecinos"),
        ("A2_placebo", priv, "Placebo de fecha (2017–2021)"),
    ]:
        r = _fila(resumen, variante=variante, resultado=resultado)
        if r is not None:
            filas.append(
                _fila_prueba(nombre, r["valor"], r["ee"], r["media_base"], r["pre_wald_p"])
            )
    perm, sd, estados = extra.get("permutacion"), extra.get("honest_sd"), extra.get("estados")
    if perm is not None and not perm.empty:
        filas.append(
            [
                "Permutación dentro del estado",
                "",
                "",
                "",
                "",
                f"p = {perm['p_permutacion'].iloc[0]:.2f}",
            ]
        )
    if sd is not None and not sd.empty:
        r = _fila(sd, resultado=priv, M=0.0)
        if r is not None:
            filas.append(
                [
                    "HonestDiD con suavidad (M = 0, 3 primeros trimestres)",
                    "",
                    f"{_pct(r['lb_pct'])} a {_pct(r['ub_pct'])}",
                    "",
                    "",
                    "",
                ]
            )
    if estados is not None and not estados.empty:
        pct = 100 * estados["att"] / estados["media_base"].abs()
        filas.append(
            [
                "Sin un estado a la vez (32)",
                "",
                f"{_pct(pct.min())} a {_pct(pct.max())}",
                "",
                "",
                "",
            ]
        )
    for variante, resultado, nombre in [
        ("B1_C1", "tarjetas_debito_bb_pc", "Tarjetas de débito del banco"),
        ("B1_C1", "transacciones_cajero_bb_pc", "Transacciones en cajeros del banco"),
        ("B2", "tarjetas_debito_bb_pc", "Traslado: heredadas con vecino que abre"),
        ("C4", "tarjetas_credito_bm_pc", "Tarjetas de crédito privadas"),
        ("C3", "establecimientos_tpv_privado_pc", "Comercios con TPV privados (2022–2025)"),
    ]:
        r = _fila(resumen, variante=variante, resultado=resultado)
        if r is None:
            continue
        fila = _fila_prueba(nombre, r["valor"], r["ee"], r["media_base"], r["pre_wald_p"])
        if variante == "B1_C1":
            # La media previa del banco es casi cero: el porcentaje no dice nada.
            fila[2], fila[3] = "", ""
        filas.append(fila)
    return _md(
        filas,
        [
            "Prueba",
            "Efecto (ee)",
            "% de la media",
            "Se descarta más de",
            "Previos (p)",
            "Lectura",
        ],
        alinear="lrrrrl",
    )


def _leer(nombre: str) -> pd.DataFrame:
    archivo = TABLAS / nombre
    return pd.read_csv(archivo) if archivo.exists() else pd.DataFrame()


def generar() -> list[Path]:
    t = _leer("tabla_final.csv")
    if t.empty:
        raise FileNotFoundError("falta outputs/tablas/tabla_final.csv: corre la batería")
    apilado = _leer("apilado_resumen.csv")
    het = _leer("het_q.csv")
    DESTINO.mkdir(parents=True, exist_ok=True)
    tablas: dict[str, Callable[[], str]] = {
        "tab_descriptivas.md": lambda: tabla_descriptivas(
            _leer("desc_estadisticas_municipio_trim.csv")
        ),
        "tab_primera_etapa.md": lambda: tabla_primera_etapa(t),
        "tab_financiera.md": lambda: tabla_financiera(t, apilado),
        "tab_actividad.md": lambda: tabla_actividad(t),
        "tab_denue_espacial.md": tabla_denue_espacial,
        "tab_decisiones.md": tabla_decisiones,
        "tab_heterogeneidad.md": lambda: tabla_heterogeneidad(het),
        "tab_calendario.md": lambda: tabla_calendario(_leer("desc_calendario_aperturas.csv")),
        # Fase 2: solo si existe su resumen (`make bateria-fase2`).
        "tab_fase2.md": lambda: tabla_fase2(_leer("fase2_resumen.csv")),
        # Fase 4: solo si existe su resumen (`make bateria-fase4`).
        "tab_fase4_estimadores.md": lambda: tabla_fase4_estimadores(_leer("fase4_estimadores.csv")),
        "tab_fase4.md": lambda: tabla_fase4(
            _leer("fase4_resumen.csv"),
            _leer("fase4_controles.csv"),
            {
                "permutacion": _leer("fase4_permutacion.csv"),
                "honest_sd": _leer("fase4_honest_sd.csv"),
                "estados": _leer("fase4_sin_un_estado.csv"),
            },
        ),
        # Fase 3: solo si existe su resumen (`make bateria-fase3`).
        "tab_fase3.md": lambda: tabla_fase3(
            _leer("fase3_resumen.csv"),
            {
                r: _leer(f"fase3_rob_extra_municipio_elecciones_{r}.csv")
                for r in ("pct_participacion", "pct_bloque_gobierno")
            },
        ),
    }
    # Fase 6: módulo aparte; cada tabla se omite si faltan sus insumos (`make bateria-fase6`).
    from proyecto.utils.entregables_fase6 import TABLAS_FASE6

    tablas.update(TABLAS_FASE6)
    escritos = []
    for nombre, f in tablas.items():
        contenido = f()
        if not contenido:
            log.warning("sin datos para %s", nombre)
            continue
        (DESTINO / nombre).write_text(contenido, encoding="utf-8")
        escritos.append(DESTINO / nombre)
    log.info("tablas de entregables: %s", ", ".join(p.name for p in escritos))
    return escritos


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generar()

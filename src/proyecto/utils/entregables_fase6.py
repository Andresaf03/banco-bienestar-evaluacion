"""Tablas de la fase 6 para el trabajo final (programas, acceso, DENUE por sector y controles).

Mismas convenciones que `entregables.py`, de donde se reutilizan los formatos. Cada función
devuelve "" si faltan sus insumos (`make bateria-fase6`), y `generar()` de `entregables.py` la omite.
"""

from __future__ import annotations

import pandas as pd

from proyecto.utils.entregables import (
    _con_ee,
    _lectura,
    _leer,
    _md,
    _num,
    _p,
    _pct,
)

CORTES = ("2019Q1", "2024Q4")
SECTORES = [
    ("estab_s46_pc", "Comercio al por menor (46)"),
    ("estab_s72_pc", "Alimentos y hospedaje (72)"),
    ("estab_s81_pc", "Otros servicios (81)"),
    ("estab_s3133_pc", "Manufactura (31–33)"),
    ("estab_resto_pc", "Resto (incluye manufactura)"),
    ("estab_sin_52_93_pc", "Todos, sin financieros ni gobierno"),
]
OTRAS_PRUEBAS = [
    ("C3", "Reubicación: lejanas de municipios que abren"),
    ("C3b", "Controles solo de municipios sin apertura"),
    ("C6", "Placebo: cabeceras sin sucursal"),
    ("C6b", "Placebo: cabeceras, controles de 2,500+"),
]
CONTROLES = [
    ("base", "Principal: aún no tratados"),
    ("solo nunca tratados como control", "Solo nunca tratados"),
    ("H1c solo municipios que alguna vez abren", "Solo los que abren (calendario)"),
    ("H1d nunca tratados emparejados (PS 1:1, región)", "Nunca tratados emparejados"),
    ("H1e apilado, controles sin vecino con apertura nueva", "Apilado, sin vecino que abra"),
    ("apilado: solo nunca tratados", "Apilado, solo nunca tratados"),
]


def _fila_cs(nombre: str, r: pd.Series, n: str) -> list[str]:
    return [
        nombre,
        n,
        _con_ee(r["valor"], r["ee"]),
        _pct(r["efecto_pct"]),
        _p(r["pre_wald_p"]),
        _lectura(r["valor"], r["ee"], r["media_base"], r["pre_wald_p"]),
    ]


def tabla_acceso() -> str:
    acc = _leer("fase6_accesibilidad.csv")
    enif = _leer("fase6_enif_apoyos.csv")
    if acc.empty or enif.empty:
        return ""
    a = acc[(acc["cota"] == "central") & (acc["poblacion_tipo"] == "65 y más")]

    def acceso(tipo: str, grupo: str, col: str) -> list[str]:
        v = [
            a[(a["grupo_tipo"] == tipo) & (a["grupo"] == grupo) & (a["corte"] == c)][col]
            for c in CORTES
        ]
        d = 1 if col == "km_media" else 0
        return [_num(float(x.iloc[0]), d) if len(x) else "" for x in v]

    def encuesta(tamano: str, col: str, d: int = 0) -> list[str]:
        v = [
            enif[(enif["anio"] == y) & (enif["tamano_localidad"] == tamano)][col]
            for y in (2021, 2024)
        ]
        return [_num(float(x.iloc[0]), d) if len(x) else "" for x in v]

    filas = [
        ["*Adultos de 65 años o más (ITER 2020)*", "*2019T1*", "*2024T4*"],
        ["Distancia media a una sucursal del banco (km)", *acceso("nacional", "todas", "km_media")],
        ["A 10 km o menos (%)", *acceso("nacional", "todas", "pct_a_10km")],
        [
            "A 10 km o menos, municipios de marginación muy alta (%)",
            *acceso("marginacion", "Muy alto", "pct_a_10km"),
        ],
        [
            "A 10 km o menos, localidades de menos de 2,500 hab. (%)",
            *acceso("tamano", "menos de 2,500", "pct_a_10km"),
        ],
        ["*Quienes reciben apoyos de gobierno (ENIF)*", "*2021*", "*2024*"],
        [
            "Con cuenta o tarjeta para recibirlos (%)",
            *encuesta("nacional", "pct_cuenta_para_apoyos"),
        ],
        [
            "Con cuenta, localidades de menos de 2,500 hab. (%)",
            *encuesta("menos de 2,500", "pct_cuenta_para_apoyos"),
        ],
        ["Usaron una sucursal en el último año (%)", *encuesta("nacional", "pct_uso_sucursal")],
        [
            "Minutos a su sucursal, localidades de menos de 2,500 hab. (mediana)",
            *encuesta("menos de 2,500", "minutos_sucursal_mediana"),
        ],
    ]
    return _md(filas, ["Indicador", "Antes", "Después"])


def tabla_radios(resultado: str = "estab_emprendimiento_pc") -> str:
    d = _leer(f"fase6_radios_{resultado}.csv")
    if d.empty:
        return ""
    filas = []
    for _, r in d.iterrows():
        filas.append(
            [
                "Con sucursal" if r["banda"] == "sucursal propia" else f"Vecina a {r['banda']}",
                f"{int(r['tratadas']):,}",
                _con_ee(r["att"], r["ee"]),
                f"{r['pct_del_total_sin_ponderar']:.1f}%".replace("-", "−"),
                _con_ee(r["att_pond"], r["ee_pond"]),
                _con_ee(r["estab_implicados"], r["estab_implicados_ee"]),
                f"{r['pct_del_total']:.1f}%".replace("-", "−"),
                _p(r["pre_wald_p"]),
            ]
        )
    return _md(
        filas,
        [
            "Localidades",
            "N",
            "Por mil (ee)",
            "% del total",
            "Ponderado por población (ee)",
            "Establecimientos (ee)",
            "% del total",
            "Previos (p)",
        ],
    )


def tabla_denue_fase6() -> str:
    res = _leer("fase6_resumen.csv")
    comp = _leer("fase6_composicion.csv")
    dos = _leer("fase6_dosis_estab_emprendimiento_pc.csv")
    if res.empty:
        return ""
    filas = [["*C1–C2. Por sector*", "", "", "", "", ""]]
    for resultado, nombre in SECTORES:
        r = res[(res["bloque"] == "C1") & (res["resultado"] == resultado)]
        if not r.empty:
            filas.append(_fila_cs(nombre, r.iloc[0], f"{int(r.iloc[0]['n_tratadas']):,}"))
    if not comp.empty:
        c = comp.iloc[0]
        filas.append(
            [
                "Consumo amplio (46 + 72 + 81) − resto, en puntos",
                "",
                _con_ee(c["dif_pct"], c["ee_dif_pct"]),
                "",
                "",
                f"p = {_p(c['p_dif'])}",
            ]
        )
    if not dos.empty:
        filas.append(["*C4. Por tercil de la proporción de 65+*", "", "", "", "", ""])
        for _, r in dos.iterrows():
            nombre = {"T1": "Tercil bajo", "T2": "Tercil medio", "T3": "Tercil alto"}[r["variante"]]
            fila = [
                nombre,
                f"{int(r['tratadas']):,}",
                _con_ee(r["att"], r["ee"]),
                _pct(r["efecto_pct"]),
                _p(r["pre_wald_p"]),
                _lectura(r["att"], r["ee"], r["media_base"], r["pre_wald_p"]),
            ]
            filas.append(fila)
    filas.append(["*C3 y C6. Reubicación, controles y placebo*", "", "", "", "", ""])
    for bloque, nombre in OTRAS_PRUEBAS:
        r = res[res["bloque"] == bloque]
        if not r.empty:
            filas.append(_fila_cs(nombre, r.iloc[0], f"{int(r.iloc[0]['n_tratadas']):,}"))
    return _md(filas, ["Prueba", "N", "Efecto (ee)", "% de la media", "Previos (p)", "Lectura"])


def tabla_controles() -> str:
    c = _leer("fase6_controles.csv")
    if c.empty:
        return ""
    series = [
        ("sucursales_privado_pc", "Privadas"),
        ("sucursales_bm_pc", "Banca múltiple"),
        ("sucursales_eacp_pc", "EACP"),
    ]
    filas = []
    for variante, nombre in CONTROLES:
        fila = [nombre]
        for resultado, _ in series:
            sub = c[(c["resultado"] == resultado) & c["variante"].str.startswith(variante)]
            if sub.empty:
                fila.append("")
                continue
            r = sub.iloc[0]
            fila.append(f"{_pct(r['efecto_pct'])} ({r['cota_pct']:.1f}%)")
        n = c[(c["resultado"] == series[0][0]) & c["variante"].str.startswith(variante)]
        fila.append(
            "" if n.empty else f"{int(n.iloc[0]['tratadas']):,} / {int(n.iloc[0]['controles']):,}"
        )
        filas.append(fila)
    return _md(filas, ["Grupo de control", *[s[1] for s in series], "Tratados / controles"])


TABLAS_FASE6 = {
    "tab_acceso.md": tabla_acceso,
    "tab_radios.md": tabla_radios,
    "tab_denue_fase6.md": tabla_denue_fase6,
    "tab_controles.md": tabla_controles,
}

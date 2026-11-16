"""Periodos trimestrales.

Convenciones del proyecto:
- `periodo`: texto `YYYYQn` (p. ej. `2019Q1`).
- `t`: entero consecutivo con `2019Q1 = 1` (configurable en `config/parametros.yaml`).
- La CNBV nombra sus archivos con `YYYYMM` donde MM es el mes de cierre del trimestre
  (03, 06, 09, 12).
"""

from __future__ import annotations

import re

from proyecto.utils.io import parametros

_MES_A_TRIM = {3: 1, 6: 2, 9: 3, 12: 4}
_TRIM_A_MES = {v: k for k, v in _MES_A_TRIM.items()}
_RE_PERIODO = re.compile(r"^(\d{4})Q([1-4])$")


def yyyymm_a_periodo(yyyymm: str | int) -> str:
    """`201903` -> `2019Q1`."""
    s = str(yyyymm)
    if len(s) != 6 or not s.isdigit():
        raise ValueError(f"YYYYMM inválido: {yyyymm!r}")
    anio, mes = int(s[:4]), int(s[4:])
    if mes not in _MES_A_TRIM:
        raise ValueError(f"Mes de cierre no trimestral: {yyyymm!r}")
    return f"{anio}Q{_MES_A_TRIM[mes]}"


def periodo_a_yyyymm(periodo: str) -> str:
    """`2019Q1` -> `201903`."""
    anio, trim = descomponer(periodo)
    return f"{anio}{_TRIM_A_MES[trim]:02d}"


def descomponer(periodo: str) -> tuple[int, int]:
    m = _RE_PERIODO.match(periodo)
    if not m:
        raise ValueError(f"Periodo inválido: {periodo!r}")
    return int(m.group(1)), int(m.group(2))


def _indice_absoluto(periodo: str) -> int:
    anio, trim = descomponer(periodo)
    return anio * 4 + (trim - 1)


def periodo_a_t(periodo: str, base: str | None = None, valor_base: int | None = None) -> int:
    """Índice consecutivo. Por defecto `2019Q1 = 1` según `config/parametros.yaml`.

    Periodos anteriores a la base dan valores <= 0 (útil para robustez con 2016–2018).
    """
    cfg = parametros()["indice_t"]
    base = base or cfg["base"]
    valor_base = cfg["valor_base"] if valor_base is None else valor_base
    return _indice_absoluto(periodo) - _indice_absoluto(base) + valor_base


def t_a_periodo(t: int, base: str | None = None, valor_base: int | None = None) -> str:
    cfg = parametros()["indice_t"]
    base = base or cfg["base"]
    valor_base = cfg["valor_base"] if valor_base is None else valor_base
    absoluto = _indice_absoluto(base) + (t - valor_base)
    anio, trim0 = divmod(absoluto, 4)
    return f"{anio}Q{trim0 + 1}"


def rango(inicio: str, fin: str) -> list[str]:
    """Lista de periodos consecutivos de `inicio` a `fin`, inclusivos."""
    a, b = _indice_absoluto(inicio), _indice_absoluto(fin)
    if b < a:
        raise ValueError("fin anterior a inicio")
    salida = []
    for k in range(a, b + 1):
        anio, trim0 = divmod(k, 4)
        salida.append(f"{anio}Q{trim0 + 1}")
    return salida


def son_consecutivos(periodos: list[str]) -> bool:
    """True si la lista (ordenada) no tiene huecos."""
    if not periodos:
        return True
    idx = sorted(_indice_absoluto(p) for p in periodos)
    return all(b - a == 1 for a, b in zip(idx, idx[1:], strict=False))


# ----------------------------------------------------------------- semestres (DENUE)
# El DENUE publica dos versiones por año (primavera y otoño). Se mapea cada versión al semestre
# calendario correspondiente: meses 01–06 → S1, meses 07–12 → S2.
_RE_SEMESTRE = re.compile(r"^(\d{4})S([12])$")


def yyyymm_a_semestre(yyyymm: str | int) -> str:
    """`202211` -> `2022S2`; `202205` -> `2022S1`."""
    s = str(yyyymm)
    if len(s) != 6 or not s.isdigit():
        raise ValueError(f"YYYYMM inválido: {yyyymm!r}")
    anio, mes = int(s[:4]), int(s[4:])
    if not 1 <= mes <= 12:
        raise ValueError(f"mes inválido: {yyyymm!r}")
    return f"{anio}S{1 if mes <= 6 else 2}"


def periodo_a_semestre(periodo: str) -> str:
    """`2022Q3` -> `2022S2` (trimestres 1–2 → S1, 3–4 → S2)."""
    anio, trim = descomponer(periodo)
    return f"{anio}S{1 if trim <= 2 else 2}"


def descomponer_semestre(semestre: str) -> tuple[int, int]:
    m = _RE_SEMESTRE.match(semestre)
    if not m:
        raise ValueError(f"Semestre inválido: {semestre!r}")
    return int(m.group(1)), int(m.group(2))


def _indice_absoluto_semestre(semestre: str) -> int:
    anio, sem = descomponer_semestre(semestre)
    return anio * 2 + (sem - 1)


def semestre_a_s(semestre: str, base: str | None = None, valor_base: int | None = None) -> int:
    """Índice consecutivo de semestres. Por defecto `2016S1 = 1` (config/parametros.yaml)."""
    cfg = parametros()["indice_s"]
    base = base or cfg["base"]
    valor_base = cfg["valor_base"] if valor_base is None else valor_base
    return _indice_absoluto_semestre(semestre) - _indice_absoluto_semestre(base) + valor_base


def s_a_semestre(s: int, base: str | None = None, valor_base: int | None = None) -> str:
    cfg = parametros()["indice_s"]
    base = base or cfg["base"]
    valor_base = cfg["valor_base"] if valor_base is None else valor_base
    absoluto = _indice_absoluto_semestre(base) + (s - valor_base)
    anio, sem0 = divmod(absoluto, 2)
    return f"{anio}S{sem0 + 1}"


def rango_semestres(inicio: str, fin: str) -> list[str]:
    """Semestres consecutivos de `inicio` a `fin`, inclusivos."""
    a, b = _indice_absoluto_semestre(inicio), _indice_absoluto_semestre(fin)
    if b < a:
        raise ValueError("fin anterior a inicio")
    salida = []
    for k in range(a, b + 1):
        anio, sem0 = divmod(k, 2)
        salida.append(f"{anio}S{sem0 + 1}")
    return salida

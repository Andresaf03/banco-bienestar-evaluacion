"""Emparejamiento de localidades tratadas y controles (lo pidió el asesor como táctica de balance).

Sigue la lógica de Fonseca y Matray (2024): para cada localidad tratada se buscan `k` controles
**dentro del mismo estado y del mismo tipo de localidad** (cabecera municipal o no), minimizando la
distancia de Mahalanobis sobre covariables previas al tratamiento. Después se estima Callaway y
Sant'Anna sobre la muestra emparejada (`analisis/05_robustez.R`, variante "muestra emparejada"): el
emparejamiento sirve para acotar la comparación a controles parecidos, no como estimador aparte.

Detalles que importan para que el emparejamiento sea legítimo:

- Misma muestra que la especificación principal (diseño entre actualizaciones, preregistrado en
  docs/decisiones.md): tratadas con apertura entre 2020S1 y 2024S1, controles sin sucursal propia a
  10 km o más de cualquier sucursal, piso de población y banderas de exclusión.
- Solo variables **medidas antes** del tratamiento y en logaritmos: población 2020, marginación,
  establecimientos en 2016S1 y el nivel del resultado en 2016S1 y 2019S1. **No** se empareja sobre
  el cambio de la actualización 2019S2: ese salto es el placebo del diseño, y emparejar sobre él lo
  volvería mecánico.
- Distancia de Mahalanobis con la covarianza de toda la muestra elegible (los bloques chicos dan
  covarianzas singulares) y asignación voraz global dentro de cada bloque. Con reemplazo
  (`matching.con_reemplazo`): las cabeceras lejanas de toda sucursal son pocas en cada estado, y
  sin reemplazo quedaban sin pareja dos de cada tres tratadas. Con caliper (`matching.caliper`):
  sin él la |dif. estandarizada| máxima quedaba en 0.25–0.30; con 1.0 baja a 0.03–0.06, a cambio
  de emparejar alrededor de la mitad de las tratadas. El ATT de la muestra emparejada es el de la
  región con soporte común, no el de todas las tratadas.
- Balance: diferencias estandarizadas antes (tratadas contra todos los controles elegibles) y
  después (tratadas emparejadas contra sus controles, con peso 1/k_i). Si la máxima supera
  `matching.smd_maximo`, se registra como balance fallido.

Salidas:
- `data/processed/matching_<panel>_<resultado>.parquet`: `cve_loc, rol, tratado, peso, distancia`
- `outputs/tablas/balance_<panel>_<resultado>.csv`: diferencias estandarizadas antes y después
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proyecto.utils.io import PROCESSED, TABLAS, parametros

log = logging.getLogger(__name__)

P = parametros()


def muestra_localidades(panel: pd.DataFrame, resultado: str) -> pd.DataFrame:
    """Una fila por localidad elegible, con las covariables de emparejamiento.

    Replica los filtros de `leer_panel()` en analisis/00_utils.R para la especificación principal:
    si las dos muestras se separan, el matching empareja unidades que R no estima.
    """
    act = P["estimacion"]["actualizaciones"]
    radio = float(P["estimacion"]["controles"]["principal"].removeprefix("dist"))
    d = panel
    for bandera in ("ya_tratado_inicio", "fecha_ambigua", "sospechoso_banjercito"):
        d = d[~d[bandera].fillna(False)]
    d = d[d["pobtot"] >= P["unidades"]["localidad_pob_minima"]]
    tratada = (d["G"] >= act["g_min"]) & (d["G"] <= act["g"])
    control = (d["G"] == 0) & (d["dist_bb_km"] >= radio)
    d = d[tratada | control]

    previos = P["matching"]["periodos_previos"]
    nivel = d[d["s"].isin(previos)].groupby("cve_loc")[resultado].mean()
    u = d.drop_duplicates("cve_loc").set_index("cve_loc")
    salida = u[
        ["G", "cve_mun", "es_cabecera", "log_poblacion_2020", "indice_marginacion_2020"]
        + ["log1p_estab_previos"]
    ].copy()
    salida["log1p_nivel_previo"] = np.log1p(nivel.reindex(salida.index))
    salida["cve_ent"] = salida.index.str[:2]
    salida["tratada"] = salida["G"] > 0
    return salida.reset_index()


def _mahalanobis(x: np.ndarray, centro: np.ndarray, inv_cov: np.ndarray) -> np.ndarray:
    d = x - centro
    return np.sqrt(np.einsum("ij,jk,ik->i", d, inv_cov, d))


def emparejar(
    cov: pd.DataFrame,
    id_col: str,
    variables: list[str],
    bloques: list[str],
    k: int,
    con_reemplazo: bool = False,
    caliper: float | None = None,
) -> pd.DataFrame:
    """Vecino más cercano por Mahalanobis dentro de cada bloque exacto. Devuelve pares.

    La covarianza es la de toda la muestra (estable aunque un bloque tenga pocas unidades). La
    asignación es voraz y global dentro del bloque: el par tratada-control más cercano se forma
    primero, así que no depende del orden del archivo. Con `caliper`, un par a mayor distancia de
    Mahalanobis no se forma: la tratada sin control cercano queda fuera (soporte común).
    """
    cov = cov.dropna(subset=variables)
    matriz = np.cov(cov[variables].to_numpy(dtype=float), rowvar=False)
    matriz = np.atleast_2d(matriz) + np.eye(len(variables)) * 1e-8
    inv = np.linalg.pinv(matriz)

    pares = []
    for _, bloque in cov.groupby(bloques, dropna=False):
        tratados = bloque[bloque["tratada"]]
        controles = bloque[~bloque["tratada"]]
        if tratados.empty or controles.empty:
            continue
        x_t = tratados[variables].to_numpy(dtype=float)
        x_c = controles[variables].to_numpy(dtype=float)
        dist = np.vstack([_mahalanobis(x_c, fila, inv) for fila in x_t])
        usados: set[int] = set()
        cuenta = dict.fromkeys(range(len(tratados)), 0)
        for i, j in zip(*np.unravel_index(np.argsort(dist, axis=None), dist.shape), strict=True):
            if caliper is not None and dist[i, j] > caliper:
                break  # las distancias vienen ordenadas: ningún par restante cabe
            if cuenta[i] >= k or (not con_reemplazo and j in usados):
                continue
            pares.append(
                {
                    "tratado": tratados.iloc[i][id_col],
                    "control": controles.iloc[j][id_col],
                    "distancia": float(dist[i, j]),
                }
            )
            usados.add(int(j))
            cuenta[i] += 1
    return pd.DataFrame(pares, columns=["tratado", "control", "distancia"])


def balance(
    cov: pd.DataFrame, pares: pd.DataFrame, id_col: str, variables: list[str]
) -> pd.DataFrame:
    """Diferencias estandarizadas antes y después de emparejar (|d| < 0.1 es balance, < 0.25 aceptable).

    Antes: todas las tratadas contra todos los controles elegibles. Después: las tratadas
    emparejadas contra sus controles, cada control con peso 1/k_i (k_i = controles de su tratada),
    que es la comparación que implica la muestra emparejada.
    """
    tratadas = cov[cov["tratada"]].set_index(id_col)
    controles = cov[~cov["tratada"]].set_index(id_col)
    k_i = pares.groupby("tratado")["control"].transform("size")
    pesos = pd.Series(1.0 / k_i.to_numpy(), index=pares["control"].to_numpy())
    emparejadas = tratadas.loc[pares["tratado"].unique()]
    sus_controles = controles.loc[pesos.index]
    filas = []
    for v in variables:
        s = np.sqrt((tratadas[v].var() + controles[v].var()) / 2)
        s = s if s and np.isfinite(s) else np.nan
        media_ctrl_emp = np.average(sus_controles[v], weights=pesos.to_numpy())
        filas.append(
            {
                "variable": v,
                "media_tratadas": tratadas[v].mean(),
                "media_controles": controles[v].mean(),
                "media_tratadas_emparejadas": emparejadas[v].mean(),
                "media_controles_emparejados": media_ctrl_emp,
                "dif_est_antes": (tratadas[v].mean() - controles[v].mean()) / s,
                "dif_est_despues": (emparejadas[v].mean() - media_ctrl_emp) / s,
            }
        )
    return pd.DataFrame(filas)


def construir(panel_nombre: str, resultado: str) -> Path:
    from proyecto.construccion.panel import SALIDAS

    if panel_nombre != "localidad":
        raise ValueError("el emparejamiento se define para el panel de localidades")
    id_col = "cve_loc"
    panel = pd.read_parquet(SALIDAS[panel_nombre])
    cov = muestra_localidades(panel, resultado)
    cfg = P["matching"]
    variables = list(cfg["variables"])
    k = cfg["n_controles"]
    pares = emparejar(
        cov, id_col, variables, list(cfg["bloquear_por"]), k, cfg["con_reemplazo"], cfg["caliper"]
    )
    if pares.empty:
        raise RuntimeError("el emparejamiento no produjo pares: revisa bloques y covariables")

    tratados = pares.groupby("tratado", as_index=False)["distancia"].mean()
    tratados = tratados.rename(columns={"tratado": id_col}).assign(
        rol="tratado", tratado=lambda x: x[id_col], peso=1.0
    )
    controles = pares.rename(columns={"control": id_col}).assign(rol="control")
    controles["peso"] = 1.0 / controles.groupby("tratado")[id_col].transform("size")
    salida = pd.concat([tratados, controles], ignore_index=True)
    salida["panel"], salida["resultado"] = panel_nombre, resultado
    ruta = PROCESSED / f"matching_{panel_nombre}_{resultado}.parquet"
    salida.to_parquet(ruta, index=False)

    tabla = balance(cov, pares, id_col, variables)
    tabla.insert(0, "resultado", resultado)
    tabla["tratadas_emparejadas"] = pares["tratado"].nunique()
    tabla["tratadas_elegibles"] = int(cov["tratada"].sum())
    TABLAS.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(TABLAS / f"balance_{panel_nombre}_{resultado}.csv", index=False)
    maximo = tabla["dif_est_despues"].abs().max()
    n_trat = int(cov["tratada"].sum())
    log.info(
        "matching %s/%s: %d de %d tratadas emparejadas con %d controles; |dif. estandarizada| "
        "máxima antes %.3f, después %.3f%s",
        panel_nombre,
        resultado,
        pares["tratado"].nunique(),
        n_trat,
        pares["control"].nunique(),
        tabla["dif_est_antes"].abs().max(),
        maximo,
        "" if maximo <= cfg["smd_maximo"] else " — BALANCE FALLIDO (supera el umbral de config)",
    )
    return ruta


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    construir(sys.argv[1], sys.argv[2])

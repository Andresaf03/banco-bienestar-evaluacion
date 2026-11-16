"""Cruce de municipios identificados solo por nombre a la clave INEGI.

Es una **excepción controlada a la regla 6** ("nunca unir por nombre"), autorizada el 2026-09-30
para dos fuentes que no publican la clave INEGI: el IMSS (catálogo propio de municipios) y Banxico
(remesas por municipio, series nombradas). Controles:

1. Solo **dentro de la misma entidad**: la clave de entidad del IMSS coincide con la del INEGI en
   las 32 entidades; Banxico trae el nombre de la entidad, que se cruza igual que los municipios.
2. Nombres **normalizados** (minúsculas, sin acentos ni puntuación, abreviaturas expandidas).
3. **Exacto** primero; **difuso** solo si el mejor candidato supera `umbral` y aventaja al
   segundo por `margen` (si no, queda pendiente en vez de adivinar).
4. **Correcciones manuales** en `config/cruces_municipios.yaml` (versionado y revisable), que
   tienen prioridad sobre lo automático.
5. Todo lo que no se cruza se reporta; nada se descarta en silencio. La tabla de cruce y su
   resumen (conteo por método y lista de los no exactos) quedan en `docs/diccionarios/`.
"""

from __future__ import annotations

import difflib
import re
import unicodedata

import pandas as pd

from proyecto.utils.io import CONFIG, INTERIM

ABREVIATURAS = {
    r"\bgral\b": "general",
    r"\bsta\b": "santa",
    r"\bsto\b": "santo",
    r"\bsn\b": "san",
    r"\bdr\b": "doctor",
    r"\bcd\b": "ciudad",
    r"\bmpio\b": "municipio",
    r"\bma\b": "maria",
    r"\bh\b": "heroica",
    r"\bvda\b": "viuda",
    r"\bfco\b": "francisco",
    r"\bj\b": "jose",
}


def normalizar(nombre: str) -> str:
    """Minúsculas, sin acentos ni puntuación, abreviaturas comunes expandidas, espacios simples."""
    if not isinstance(nombre, str):
        return ""
    texto = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-z0-9 ]", " ", texto.lower())
    for patron, reemplazo in ABREVIATURAS.items():
        texto = re.sub(patron, reemplazo, texto)
    return re.sub(r"\s+", " ", texto).strip()


def catalogo_inegi() -> pd.DataFrame:
    """Municipios vigentes del Marco Geoestadístico 2024 con su nombre normalizado."""
    m = pd.read_parquet(INTERIM / "municipios.parquet", columns=["cve_mun", "cve_ent", "nom_mun"])
    m = m.dropna(subset=["nom_mun"]).drop_duplicates("cve_mun")
    return m.assign(norma=m["nom_mun"].map(normalizar))


def manuales(fuente: str) -> dict[str, str]:
    """Correcciones manuales `clave de la fuente -> cve_mun` (config/cruces_municipios.yaml)."""
    import yaml

    ruta = CONFIG / "cruces_municipios.yaml"
    if not ruta.exists():
        return {}
    datos = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    return {str(k): str(v) for k, v in (datos.get(fuente) or {}).items()}


def _contencion_unica(nombre: str, candidatos: pd.DataFrame) -> str | None:
    """cve_mun del único municipio cuyo nombre contiene (o está contenido en) `nombre`, por
    palabras completas; None si no hay exactamente uno. Cubre los nombres oficiales largos
    ("Cintalapa" / "Cintalapa de Figueroa")."""
    if len(nombre) < 5:
        return None
    patron = re.compile(rf"(^| ){re.escape(nombre)}( |$)")
    hits = candidatos[
        candidatos["norma"].map(
            lambda c: (
                bool(patron.search(c)) or bool(re.search(rf"(^| ){re.escape(c)}( |$)", nombre))
            )
        )
    ]
    return hits["cve_mun"].iloc[0] if len(hits) == 1 else None


def _mejor(nombre: str, candidatos: pd.DataFrame) -> tuple[str | None, float, float]:
    """Mejor candidato difuso (cve_mun, puntaje) y el puntaje del segundo."""
    if candidatos.empty:
        return None, 0.0, 0.0
    puntajes = candidatos["norma"].map(lambda c: difflib.SequenceMatcher(None, nombre, c).ratio())
    orden = puntajes.sort_values(ascending=False)
    primero = orden.index[0]
    segundo = float(orden.iloc[1]) if len(orden) > 1 else 0.0
    return candidatos.loc[primero, "cve_mun"], float(orden.iloc[0]), segundo


def cruzar(
    fuente: pd.DataFrame,
    clave: str,
    entidad: str,
    nombre: str,
    correcciones: dict[str, str] | None = None,
    umbral: float = 0.9,
    margen: float = 0.05,
    catalogo: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Asigna `cve_mun` a cada fila de `fuente` (`clave`, `entidad` = cve_ent INEGI, `nombre`).

    Devuelve `fuente` con `cve_mun`, `nom_mun`, `metodo` (manual, exacto, difuso, pendiente) y
    `puntaje`. Varias claves de la fuente pueden ir al mismo municipio (el IMSS tiene más de una
    clave por municipio); quien llama decide si eso es válido para su fuente.
    """
    cat = catalogo if catalogo is not None else catalogo_inegi()
    correcciones = correcciones or {}
    nombres = cat.set_index("cve_mun")["nom_mun"]
    filas = []
    fuente = fuente.drop_duplicates(clave)
    for fila in fuente[[clave, entidad, nombre]].itertuples(index=False):
        k, ent, nom = str(fila[0]), str(fila[1]), fila[2]
        norma = normalizar(nom)
        del_estado = cat[cat["cve_ent"] == ent]
        if k in correcciones:
            cve, metodo, puntaje = correcciones[k], "manual", 1.0
        else:
            exactos = del_estado[del_estado["norma"] == norma]
            contienen = _contencion_unica(norma, del_estado)
            if len(exactos) == 1:
                cve, metodo, puntaje = exactos["cve_mun"].iloc[0], "exacto", 1.0
            elif len(exactos) > 1:
                # Homónimos dentro del estado: no hay forma de elegir sin más información.
                cve, metodo, puntaje = None, "pendiente", 1.0
            elif contienen is not None:
                cve, metodo, puntaje = contienen, "contenido", 1.0
            else:
                cve, puntaje, segundo = _mejor(norma, del_estado)
                if cve is not None and puntaje >= umbral and puntaje - segundo >= margen:
                    metodo = "difuso"
                else:
                    cve, metodo = None, "pendiente"
        filas.append(
            {
                clave: k,
                "cve_mun": cve,
                "nom_mun": nombres.get(cve) if cve else None,
                "metodo": metodo,
                "puntaje": round(puntaje, 3),
            }
        )
    resultado = pd.DataFrame(filas).drop_duplicates(clave)
    return fuente.assign(**{clave: fuente[clave].astype(str)}).merge(
        resultado, on=clave, how="left"
    )


def resumen_md(cruce: pd.DataFrame, fuente: str, clave: str, nombre: str) -> str:
    """Resumen auditable del cruce: conteo por método y todos los casos no exactos."""
    conteo = cruce["metodo"].value_counts().to_dict()
    lineas = [
        f"# Cruce de municipios por nombre: {fuente}",
        "",
        "Excepción controlada a la regla 6 (ver `src/proyecto/utils/cruce_nombres.py` y "
        "`docs/decisiones.md`). Generado por `proyecto.limpieza`.",
        "",
        "| método | casos |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(conteo.items())],
        "",
        "## Casos no exactos (revisar)",
        "",
        f"| {clave} | nombre en la fuente | cve_mun | nombre INEGI | método | puntaje |",
        "|---|---|---|---|---|---|",
    ]
    no_exactos = cruce[cruce["metodo"] != "exacto"].sort_values(["metodo", clave])
    for _, d in no_exactos.iterrows():
        lineas.append(
            f"| {d[clave]} | {d[nombre]} | {d['cve_mun'] or ''} | {d['nom_mun'] or ''} | "
            f"{d['metodo']} | {d['puntaje']} |"
        )
    return "\n".join(lineas) + "\n"

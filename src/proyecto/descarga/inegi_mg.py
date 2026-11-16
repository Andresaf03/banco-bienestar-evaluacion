"""INEGI, Marco Geoestadístico (diciembre 2024) y Catálogo Único de Claves Geoestadísticas.

1. Polígonos municipales. El producto nacional (`794551132173_s.zip`, 3.1 GB) contiene
   `mg_2024_integrado.zip` (284 MB, almacenado sin compresión), que a su vez trae
   `conjunto_de_datos/00mun.*`, `00ent.*`, `catalogos/*` y `metadatos/*`. El servidor acepta
   `Range`, así que se leen solo los miembros necesarios (~80 MB) con `utils.zip_remoto` y se
   guardan conservando la ruta interna bajo `data/raw/inegi_mg/mg_2024_integrado/`.

2. Catálogo y equivalencias (AGEEML como servicio web, https://gaia.inegi.org.mx/wscatgeo/):
   - `v2/mgem/{cve_ent}`: municipios vigentes por entidad con población censal 2020.
   - `v2/mgemEquivalencia/{cve_ent}/{cve_mun}`: historial de cambios (altas, bajas, cambios de
     nombre) de cada municipio. Se consulta para todos los municipios del catálogo y se guarda
     en un solo JSON.
   Los enlaces salen de la guía oficial https://www.inegi.org.mx/servicios/catalogounico.html.
"""

from __future__ import annotations

import json
import logging
import re
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

from proyecto.utils import http, manifest, zip_remoto
from proyecto.utils.io import RAW, fuentes

log = logging.getLogger(__name__)

FUENTE = "inegi_mg"
DESTINO = RAW / FUENTE
ANIDADO = "mg_2024_integrado.zip"
PATRON_MIEMBROS = re.compile(
    r"^(conjunto_de_datos/00(mun|ent)\.[a-z]{3}|catalogos/(áreas_geoestadísticas_(municipales|estatales)\.(csv|pdf)|léeme\.txt|contenido\.txt)|metadatos/.*)$"
)
ENTIDADES = [f"{k:02d}" for k in range(1, 33)]
URL_API = "https://gaia.inegi.org.mx/wscatgeo/v2/"
PAUSA = 0.05
HILOS = 4


def _poligonos(force: bool, s) -> None:
    cfg = fuentes()[FUENTE]
    url = cfg["url_zip_nacional"]
    carpeta = DESTINO / ANIDADO.removesuffix(".zip")
    remoto = zip_remoto.ArchivoRemoto(url, s)
    with zipfile.ZipFile(remoto) as externo, zip_remoto.abrir_anidado(externo, ANIDADO) as z:
        miembros = [i.filename for i in z.infolist() if PATRON_MIEMBROS.match(i.filename)]
        pendientes = [m for m in miembros if force or not manifest.esta_vigente(carpeta / m)]
        log.info("MG: %d miembros de interés, %d por extraer", len(miembros), len(pendientes))
        rutas = zip_remoto.extraer_de(z, pendientes, carpeta)
    for r in rutas:
        manifest.registrar(
            FUENTE,
            r,
            url,
            notas=f"extraído por rangos HTTP de {ANIDADO} dentro del zip nacional (sin descarga completa)",
        )
    log.info("MG: %d peticiones Range", remoto.peticiones)


def _json(url: str, s) -> dict:
    resp = http.obtener(url, s)
    time.sleep(PAUSA)
    return resp.json()


def _catalogo(force: bool, s) -> list[dict]:
    ruta = DESTINO / "wscatgeo" / "mgem_por_entidad.json"
    url = URL_API + "mgem/{cve_ent}"
    if not force and manifest.esta_vigente(ruta):
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)["datos"]
    datos = []
    for ent in ENTIDADES:
        r = _json(URL_API + f"mgem/{ent}", s)
        datos.extend(r.get("datos", []))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"url": url, "datos": datos}, f, ensure_ascii=False, indent=1)
    manifest.registrar(FUENTE, ruta, url, notas="concatenación de las 32 respuestas por entidad")
    return datos


def _equivalencias(force: bool, s, catalogo: list[dict]) -> None:
    ruta = DESTINO / "wscatgeo" / "mgem_equivalencias.json"
    url = URL_API + "mgemEquivalencia/{cve_ent}/{cve_mun}"
    if not force and manifest.esta_vigente(ruta):
        return
    claves = sorted({(d["cve_ent"], d["cve_mun"]) for d in catalogo})

    def uno(clave: tuple[str, str]) -> dict:
        ent, mun = clave
        r = _json(URL_API + f"mgemEquivalencia/{ent}/{mun}", s)
        return {"cve_ent": ent, "cve_mun": mun, "respuesta": r}

    with ThreadPoolExecutor(max_workers=HILOS) as pool:
        resultados = list(pool.map(uno, claves))
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(
            {"url": url, "n_consultas": len(claves), "datos": resultados}, f, ensure_ascii=False
        )
    manifest.registrar(
        FUENTE, ruta, url, notas=f"una consulta por municipio del catálogo ({len(claves)} claves)"
    )


def descargar(force: bool = False) -> None:
    s = http.sesion()
    _poligonos(force, s)
    catalogo = _catalogo(force, s)
    _equivalencias(force, s, catalogo)

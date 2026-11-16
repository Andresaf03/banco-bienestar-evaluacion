"""MANIFEST.csv: columnas exigidas, sin hashes vacíos, archivos existentes y hash vigente (muestra)."""

import csv
import hashlib

from proyecto.utils import manifest
from proyecto.utils.io import raiz


def test_manifest_existe_y_columnas():
    assert manifest.RUTA_MANIFEST.exists(), "falta data/raw/MANIFEST.csv; corre `make descargar`"
    with open(manifest.RUTA_MANIFEST, encoding="utf-8", newline="") as f:
        cols = next(csv.reader(f))
    assert cols == manifest.COLUMNAS


def test_manifest_sin_hashes_vacios():
    entradas = manifest.leer()
    assert entradas, "MANIFEST vacío"
    for e in entradas:
        assert e.sha256 and len(e.sha256) == 64, f"hash vacío o inválido: {e.archivo}"
        assert e.tamaño_bytes > 0, f"tamaño 0: {e.archivo}"
        assert e.url.startswith("http"), f"url inválida: {e.archivo}"
        assert e.fecha_descarga, f"sin fecha: {e.archivo}"


def test_manifest_archivos_existen():
    faltan = [
        e.archivo
        for e in manifest.leer()
        if manifest.conservado(e) and not (raiz() / e.archivo).exists()
    ]
    assert not faltan, f"archivos registrados que no existen: {faltan[:5]}"


def test_manifest_hash_coincide_en_muestra():
    """Verifica el SHA-256 de los archivos pequeños (< 5 MB) para no tardar."""
    for e in manifest.leer():
        ruta = raiz() / e.archivo
        if manifest.conservado(e) and ruta.stat().st_size < 5_000_000:
            h = hashlib.sha256(ruta.read_bytes()).hexdigest()
            assert h == e.sha256, f"hash distinto: {e.archivo}"


def test_manifest_cubre_fuentes_clave():
    fuentes = {e.fuente for e in manifest.leer()}
    assert {
        "cnbv_bdif",
        "inegi_mg",
        "inegi_censo",
        "babien",
        "conapo_marginacion",
        "conapo_proyecciones",
        "literatura",
        "cnbv_portafolio",
    } <= fuentes
    bdif = [
        e
        for e in manifest.leer()
        if e.fuente == "cnbv_bdif" and e.archivo.endswith((".xlsx", ".xlsm"))
    ]
    assert len(bdif) >= 24, "menos de 24 trimestres de BDIF registrados"

"""Manifiesto de descargas: `data/raw/MANIFEST.csv`.

Columnas: fuente, archivo, url, fecha_descarga, tamaño_bytes, sha256, notas.
`archivo` es la ruta relativa a la raíz del repo (p. ej. `data/raw/cnbv_bdif/x.xlsx`).
Una fila por archivo; si se vuelve a descargar el mismo archivo se sobreescribe la fila.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from proyecto.utils.io import RAW, raiz

COLUMNAS = ["fuente", "archivo", "url", "fecha_descarga", "tamaño_bytes", "sha256", "notas"]
RUTA_MANIFEST = RAW / "MANIFEST.csv"
# Marca para archivos que se descargaron, se procesaron y NO se conservaron (streaming del DENUE:
# 13 GB de crudo contra 16 GB libres). Quedan registrados con su hash para poder reproducirlos.
MARCA_NO_CONSERVADO = "[no conservado]"


@dataclass(frozen=True)
class Entrada:
    fuente: str
    archivo: str
    url: str
    fecha_descarga: str
    tamaño_bytes: int
    sha256: str
    notas: str = ""


def sha256_de(path: Path, bloque: int = 1 << 20) -> str:
    """SHA-256 de un archivo leído por bloques."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bloque)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def relativa(path: Path) -> str:
    return str(path.resolve().relative_to(raiz()))


def leer() -> list[Entrada]:
    """Lee el manifiesto; lista vacía si no existe."""
    if not RUTA_MANIFEST.exists():
        return []
    with open(RUTA_MANIFEST, encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f))
    return [
        Entrada(
            fuente=r["fuente"],
            archivo=r["archivo"],
            url=r["url"],
            fecha_descarga=r["fecha_descarga"],
            tamaño_bytes=int(r["tamaño_bytes"] or 0),
            sha256=r["sha256"],
            notas=r.get("notas", ""),
        )
        for r in filas
    ]


def _escribir(entradas: list[Entrada]) -> None:
    RUTA_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    ordenadas = sorted(entradas, key=lambda e: (e.fuente, e.archivo))
    with open(RUTA_MANIFEST, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        for e in ordenadas:
            w.writerow(asdict(e))


def registrar(fuente: str, path: Path, url: str, notas: str = "") -> Entrada:
    """Calcula hash y tamaño del archivo y lo registra (reemplaza la fila si ya existía)."""
    entrada = Entrada(
        fuente=fuente,
        archivo=relativa(path),
        url=url,
        fecha_descarga=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        tamaño_bytes=path.stat().st_size,
        sha256=sha256_de(path),
        notas=notas,
    )
    existentes = [e for e in leer() if e.archivo != entrada.archivo]
    _escribir([*existentes, entrada])
    return entrada


def registrar_procesado(
    fuente: str, temporal: Path, url: str, archivo_logico: str, notas: str = ""
) -> Entrada:
    """Registra un archivo que se descargó y se borró tras procesarlo.

    `archivo_logico` es la ruta que *tendría* en `data/raw/` si se conservara; sirve para
    identificarlo y para volver a bajarlo con `--force`. Se antepone `MARCA_NO_CONSERVADO` a las
    notas para que las pruebas y el lector sepan que no está en disco.
    """
    entrada = Entrada(
        fuente=fuente,
        archivo=archivo_logico,
        url=url,
        fecha_descarga=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        tamaño_bytes=temporal.stat().st_size,
        sha256=sha256_de(temporal),
        notas=f"{MARCA_NO_CONSERVADO} {notas}".strip(),
    )
    existentes = [e for e in leer() if e.archivo != entrada.archivo]
    _escribir([*existentes, entrada])
    return entrada


def conservado(entrada: Entrada) -> bool:
    """False si el archivo se procesó por streaming y no se guardó en disco."""
    return not entrada.notas.startswith(MARCA_NO_CONSERVADO)


def buscar(path: Path) -> Entrada | None:
    """Entrada del manifiesto para un archivo, o None."""
    rel = relativa(path)
    for e in leer():
        if e.archivo == rel:
            return e
    return None


def esta_vigente(path: Path) -> bool:
    """True si el archivo existe y su hash coincide con el registrado en el manifiesto."""
    if not path.exists():
        return False
    e = buscar(path)
    return e is not None and e.sha256 == sha256_de(path)

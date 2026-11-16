"""Lectura parcial de un ZIP remoto mediante peticiones HTTP con `Range`.

Permite extraer solo algunos miembros de un archivo enorme (p. ej. el Marco Geoestadístico
nacional de INEGI, 3.1 GB) sin descargarlo completo. `ArchivoRemoto` implementa la interfaz
mínima de archivo (`seek`, `tell`, `read`) que `zipfile.ZipFile` necesita; cada lectura se
traduce en un GET con `Range` y se cachea por bloques para no multiplicar peticiones.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import requests

from proyecto.utils import http

BLOQUE = 4 << 20  # 4 MiB por petición


class ArchivoRemoto(io.RawIOBase):
    def __init__(self, url: str, s: requests.Session | None = None, bloque: int = BLOQUE):
        super().__init__()
        self.url = url
        self.s = s or http.sesion()
        self.bloque = bloque
        cab = http.cabecera(url, self.s)
        if cab.headers.get("Accept-Ranges", "").lower() == "none":
            raise http.ErrorTransitorio(f"El servidor no acepta Range: {url}")
        self.tamanio = int(cab.headers["Content-Length"])
        self.pos = 0
        self._cache: dict[int, bytes] = {}
        self.peticiones = 0

    # --- interfaz de archivo -------------------------------------------------
    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.tamanio + offset
        else:
            raise ValueError(whence)
        self.pos = max(0, min(self.pos, self.tamanio))
        return self.pos

    def _bloque(self, k: int) -> bytes:
        if k not in self._cache:
            ini = k * self.bloque
            fin = min(ini + self.bloque, self.tamanio) - 1
            self._cache[k] = http.rango(self.url, ini, fin, self.s)
            self.peticiones += 1
        return self._cache[k]

    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            n = self.tamanio - self.pos
        n = min(n, self.tamanio - self.pos)
        partes = []
        pos = self.pos
        restante = n
        while restante > 0:
            k, desplaz = divmod(pos, self.bloque)
            b = self._bloque(k)
            trozo = b[desplaz : desplaz + restante]
            partes.append(trozo)
            pos += len(trozo)
            restante -= len(trozo)
        self.pos = pos
        return b"".join(partes)

    def readinto(self, b) -> int:
        datos = self.read(len(b))
        b[: len(datos)] = datos
        return len(datos)


def listar(url: str, s: requests.Session | None = None) -> list[zipfile.ZipInfo]:
    """Lista los miembros del ZIP remoto leyendo solo el directorio central."""
    with zipfile.ZipFile(ArchivoRemoto(url, s)) as z:
        return z.infolist()


def extraer(
    url: str,
    miembros: list[str],
    destino: Path,
    s: requests.Session | None = None,
) -> list[Path]:
    """Extrae `miembros` (rutas dentro del ZIP) a `destino`, conservando solo el nombre base."""
    destino.mkdir(parents=True, exist_ok=True)
    salida = []
    with zipfile.ZipFile(ArchivoRemoto(url, s)) as z:
        for m in miembros:
            ruta = destino / Path(m).name
            with z.open(m) as fin, open(ruta, "wb") as fout:
                while True:
                    trozo = fin.read(1 << 20)
                    if not trozo:
                        break
                    fout.write(trozo)
            salida.append(ruta)
    return salida


class Ventana(io.RawIOBase):
    """Vista de solo lectura sobre un rango [inicio, inicio+tamanio) de otro archivo.

    Sirve para abrir un ZIP *almacenado sin compresión* dentro de otro ZIP remoto sin
    descargarlo: se calcula el desplazamiento de sus datos y se expone como archivo.
    """

    def __init__(self, base: io.RawIOBase, inicio: int, tamanio: int):
        super().__init__()
        self.base, self.inicio, self.tamanio, self.pos = base, inicio, tamanio, 0

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.tamanio + offset
        else:
            raise ValueError(whence)
        self.pos = max(0, min(self.pos, self.tamanio))
        return self.pos

    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            n = self.tamanio - self.pos
        n = min(n, self.tamanio - self.pos)
        self.base.seek(self.inicio + self.pos)
        datos = self.base.read(n)
        self.pos += len(datos)
        return datos

    def readinto(self, b) -> int:
        datos = self.read(len(b))
        b[: len(datos)] = datos
        return len(datos)


_LARGO_CABECERA_LOCAL = 30


def abrir_anidado(externo: zipfile.ZipFile, nombre: str) -> zipfile.ZipFile:
    """Abre un ZIP `nombre` almacenado (sin comprimir) dentro de `externo` como otro ZipFile."""
    import struct

    zi = externo.getinfo(nombre)
    if zi.compress_type != zipfile.ZIP_STORED:
        raise ValueError(f"{nombre} está comprimido dentro del ZIP externo; no se puede ventanear")
    base = externo.fp
    base.seek(zi.header_offset)
    cab = base.read(_LARGO_CABECERA_LOCAL)
    firma, *_resto, largo_nombre, largo_extra = struct.unpack("<IHHHHHIIIHH", cab)
    if firma != 0x04034B50:
        raise ValueError("cabecera local de ZIP inválida")
    inicio = zi.header_offset + _LARGO_CABECERA_LOCAL + largo_nombre + largo_extra
    return zipfile.ZipFile(Ventana(base, inicio, zi.file_size))


def extraer_de(z: zipfile.ZipFile, miembros: list[str], destino: Path) -> list[Path]:
    """Extrae `miembros` de un ZipFile ya abierto a `destino`, conservando la ruta interna."""
    salida = []
    base = destino.resolve()
    for m in miembros:
        ruta = (destino / m).resolve()
        if base not in ruta.parents:
            raise ValueError(f"miembro con ruta fuera del destino (zip-slip): {m!r}")
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with z.open(m) as fin, open(ruta, "wb") as fout:
            while True:
                trozo = fin.read(1 << 20)
                if not trozo:
                    break
                fout.write(trozo)
        salida.append(ruta)
    return salida

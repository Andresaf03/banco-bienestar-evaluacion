# Diccionario: Banco del Bienestar, directorio de sucursales (foto 1T 2026)

Fuente: datos.gob.mx/dataset/sucursales (CC BY 4.0), copia manual en `data/manual/babien/`. No trae fecha de apertura: **no sirve para fechar el tratamiento**.

## `data/interim/babien.parquet` (3,150 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `id_sucursal` | Identificador secuencial (orden del CSV) | int64 | — | Banco del Bienestar |
| `nombre_institucion` | Siempre 'Banco del Bienestar' | str | — | Banco del Bienestar |
| `nombre_sucursal` | Nombre comercial | str | — | Banco del Bienestar |
| `domicilio` | Domicilio completo | str | — | Banco del Bienestar |
| `localidad` | Localidad declarada | str | — | Banco del Bienestar |
| `municipio_alcaldia` | Municipio declarado (texto) | str | — | Banco del Bienestar |
| `entidad` | Entidad declarada (texto) | str | — | Banco del Bienestar |
| `horario_publico` | Horario | str | — | Banco del Bienestar |
| `latitud` | Latitud WGS84 | float64 | grados | Banco del Bienestar |
| `longitud` | Longitud WGS84 | float64 | grados | Banco del Bienestar |
| `sin_coordenadas` | Sin lat/lon válidas dentro de México | bool | bool | Banco del Bienestar |
| `cve_mun_espacial` | Municipio del polígono MG 2024 que contiene el punto (clave a usar) | string | — | Banco del Bienestar |
| `cve_mun_declarado` | Clave inferida por nombre entidad+municipio (solo validación) | string | — | Banco del Bienestar |
| `coincide` | cve_mun_espacial == cve_mun_declarado | bool[pyarrow] | bool | Banco del Bienestar |

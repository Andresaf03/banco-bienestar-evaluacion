# Diccionario: INEGI, DENUE histórico (18 versiones semestrales 2016-01 – 2025-05) y tratamiento a nivel localidad

Directorio de establecimientos georreferenciado. Se descarga por streaming (el crudo no se conserva: 13 GB contra 16 GB libres) y se agrega a localidad, municipio y anillos. Los bloques temáticos **no son excluyentes**: una farmacia cuenta en `consumo` y en `salud`, y todo establecimiento cuenta en `emprendimiento`. Clasificación SCIAN en `limpieza/denue_clasificacion.py`.

**El DENUE cuenta establecimientos, no sucursales regulatorias**: en 2016 registra 23,437 unidades de banca múltiple contra las ~13,000 sucursales que reporta la CNBV, porque incluye cajeros y módulos. Es una medida de presencia a nivel localidad, no comparable en niveles con la BDIF.

**Los archivos grandes vienen partidos** por el INEGI en bloques de 520,000 registros (sectores 72 y 81 desde 2019-11): se descargan todas las partes, así que los totales están completos.

## `data/interim/denue_localidad.parquet` (2,530,646 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_loc` | Clave de localidad de 9 dígitos (ent 2 + mun 3 + loc 4) | string | — | INEGI |
| `cve_mun` | Clave municipal | string | — | INEGI |
| `version` | Versión del DENUE (AAAA_MM) | str | — | INEGI |
| `semestre` | Semestre calendario de la versión | str | YYYYSn | INEGI |
| `bloque` | emprendimiento | consumo | salud | financiero | str | categoría | INEGI |
| `clase` | Clase fina dentro del bloque (farmacia, restaurantes, banca_multiple, ...) | str | categoría | INEGI |
| `n_estab` | Establecimientos | int32 | número | INEGI |
| `n_micro` | Establecimientos de 0 a 5 personas (proxy de micronegocio / autoempleo) | int32 | número | INEGI |
| `empleo_est` | Empleo estimado con el punto medio del rango de personas ocupadas | float32 | personas | INEGI |
| `s` | Índice de semestre (2016S1 = 1) | int64 | — | INEGI |

## `data/interim/denue_municipio.parquet` (1,125,824 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal | string | — | INEGI |
| `version` | Versión del DENUE | str | — | INEGI |
| `semestre` | Semestre | str | YYYYSn | INEGI |
| `bloque` | Bloque temático | str | categoría | INEGI |
| `clase` | Clase fina | str | categoría | INEGI |
| `n_estab` | Establecimientos | int32 | número | INEGI |
| `n_micro` | Micronegocios | int32 | número | INEGI |
| `empleo_est` | Empleo estimado | float32 | personas | INEGI |
| `s` | Índice de semestre | int64 | — | INEGI |

## `data/interim/denue_cobertura.parquet` (18 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `version` | Versión del DENUE | str | — | INEGI |
| `semestre` | Semestre | str | YYYYSn | INEGI |
| `s` |  | int64 |  | INEGI |
| `establecimientos` | Total nacional de la versión (control de calidad) | int32 | número | INEGI |
| `micronegocios` |  | int32 |  | INEGI |
| `empleo_est` |  | float32 |  | INEGI |
| `localidades` | Localidades con al menos un establecimiento | int64 | número | INEGI |
| `municipios` | Municipios con al menos un establecimiento | int64 | número | INEGI |
| `sectores_procesados` | Archivos sectoriales agregados | int64 | número | INEGI |
| `sectores_esperados` | Archivos que publica el INEGI en esa versión | int64 | número | INEGI |
| `completa` | True si se procesaron todos los sectores; si no, no usar en el panel | bool | bool | INEGI |

## `data/interim/tratamiento_localidad.parquet` (2,880 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Municipio | str | — | INEGI |
| `cve_loc` | Localidad con sucursal del Banco del Bienestar | str | — | INEGI |
| `nom_loc` | Nombre de la localidad | str | — | INEGI |
| `n_sucursales_loc` | Sucursales asignadas a la localidad | int64 | número | INEGI |
| `dist_sucursal_km` | Distancia entre la sucursal y el punto de la localidad asignada | float64 | km | INEGI |
| `n_sucursales_mun` | Sucursales en todo el municipio | int64 | número | INEGI |
| `G_trimestre` | Primer trimestre con sucursal (BDIF municipal, neta de Banjército) | str | YYYYQn | INEGI |
| `ya_tratado_inicio` | El municipio ya tenía sucursal en el primer periodo (herencia Bansefi) | bool | bool | INEGI |
| `sospechoso_banjercito` | Posible sucursal nueva de Banjército (ver auditoría P2) | bool | bool | INEGI |
| `pobtot` | Población de la localidad (Censo 2020) | int64 | personas | INEGI |
| `fecha_ambigua` | El municipio tiene 2+ sucursales, así que la fecha no identifica a esta localidad | bool | bool | INEGI |
| `G_semestre` | Lo mismo en semestres | str | YYYYSn | INEGI |
| `g_s` | Índice del semestre de apertura; 0 si no aplica | int64 | — | INEGI |
| `lat` | Latitud de la localidad | float64 | grados | INEGI |
| `lon` | Longitud | float64 | grados | INEGI |

## `data/interim/anillos.parquet` (334,656 filas)

🔴 **Subconteo en los controles (revisión del 2026-11-17).** Los puntos (`pts_*`) solo cubren los
1,975 municipios que alguna vez tuvieron sucursal, así que un anillo centrado en un control de
otro municipio solo cuenta los establecimientos que caen dentro de esos municipios: los 802
controles fuera de ellos tienen 10.3 establecimientos a 1 km contra 105 en su propia localidad.
`panel_anillo` es solo descriptivo y no entra a ninguna estimación; las bandas de distancia del
decaimiento usan los conteos por localidad y no tienen este problema.

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_loc` | Centro del anillo (localidad) | str | — | INEGI |
| `radio_km` | Radio | float64 | km | INEGI |
| `bloque` | Bloque temático | str | categoría | INEGI |
| `n_estab` | Establecimientos dentro del radio | int32 | número | INEGI |
| `n_micro` | Micronegocios dentro del radio | int32 | número | INEGI |
| `empleo_est` | Empleo estimado dentro del radio | float32 | personas | INEGI |
| `version` | Versión del DENUE | str | — | INEGI |

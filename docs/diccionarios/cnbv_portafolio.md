# Diccionario: CNBV Portafolio de Información, operativa de banca de desarrollo por institución; serie Bienestar sin Banjército

Fuente: https://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/ (`BD_Operativa_YYYYMM.xls(x)`, 2016-01 – 2021-12). 'Bansefi' se renombra a 'Banco del Bienestar'. Ver `docs/data_audit.md` P2 para el método de la serie corregida.

## `data/interim/cnbv_portafolio_operativa.parquet` (298,222 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `yyyymm` | Mes de la publicación | str | YYYYMM | CNBV |
| `periodo` | Trimestre BDIF si el mes es de cierre (03/06/09/12); nulo si no | str | YYYYQn | CNBV |
| `cve_mun` | Clave municipal (dígitos 4–8 de cve_inegi) | str | — | CNBV |
| `institucion` | Banco del Bienestar, Banjército, Banobras, Nafin, Bancomext, Sociedad Hipotecaria Federal | str | — | CNBV |
| `producto` | Producto/indicador operativo tal como lo publica la CNBV | str | — | CNBV |
| `en_bdif` | True para Bienestar y Banjército (las dos instituciones que la BDIF cuenta como banca de desarrollo) | bool | bool | CNBV |
| `valor` | Suma de dat_num_total en el municipio | float64 | número | CNBV |

## `data/interim/banjercito_municipios.parquet` (76 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Municipio con sucursal de Banjército en algún mes | str | — | CNBV |
| `meses_con_banjercito` | Meses con sucursal (máx. 72) | int64 | — | CNBV |
| `primer_mes` | Primer mes observado | str | YYYYMM | CNBV |
| `ultimo_mes` | Último mes observado | str | YYYYMM | CNBV |
| `suc_banjercito_202112` | Sucursales de Banjército en dic-2021 | float64 | número | CNBV |
| `suc_bienestar_202112` | Sucursales del Bienestar en dic-2021 | float64 | número | CNBV |
| `solo_banjercito_202112` | Banjército presente y Bienestar ausente en dic-2021 | bool | bool | CNBV |

## `data/interim/sucursales_bienestar.parquet` (98,616 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal | str | — | CNBV |
| `periodo` | Trimestre | str | YYYYQn | CNBV |
| `t` | Índice (2019Q1 = 1) | int64 | — | CNBV |
| `suc_bd_bdif` | Sucursales de banca de desarrollo según BDIF (Bienestar + Banjército) | int64 | número | CNBV |
| `suc_banjercito` | Sucursales de Banjército: observadas 2016T1–2021T4, extrapoladas 2022+ (acotadas por suc_bd_bdif) | float64 | número | CNBV |
| `suc_bienestar` | suc_bd_bdif − suc_banjercito; **define el tratamiento** | float64 | número | CNBV |
| `fuente_banjercito` | portafolio | extrapolado_2021-12 | str | categoría | CNBV |
| `sospechoso_banjercito_nuevo` | Entra al tratamiento después de 2021T4 y el directorio Bienestar 2026 no respalda la sucursal (posible Banjército nuevo) | bool | bool | CNBV |

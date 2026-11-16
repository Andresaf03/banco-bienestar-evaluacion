# Diccionario: CONAPO, marginación y proyecciones de población

Marginación: IMM 2020 (Censo 2020) y series DP2 2010/2015. Proyecciones: reconstrucción 1990–2019 y proyección 2020–2040 por municipio, sexo y grupo quinquenal. Todas las variables originales se conservan con nombre en snake_case.

## `data/interim/conapo_marginacion.parquet` (7,382 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal | string | — | CONAPO |
| `cve_ent` | Entidad | string | — | CONAPO |
| `nom_ent` | Entidad | str | — | CONAPO |
| `nom_mun` | Municipio | str | — | CONAPO |
| `anio` | 2010, 2015 o 2020 | int64 | — | CONAPO |
| `pob_tot` | Población total | int64 | personas | CONAPO |
| `im` | Índice de marginación | float64 | índice | CONAPO |
| `gm` | Grado: Muy bajo, Bajo, Medio, Alto, Muy alto | str | categoría | CONAPO |
| `imn` | Índice normalizado 0–1 | float64 | índice | CONAPO |
| `analf` | % población 15+ analfabeta | float64 | % | CONAPO |
| `sbasc` | % población 15+ sin educación básica | float64 | % | CONAPO |
| `ovsde` | % ocupantes en viviendas sin drenaje ni excusado | float64 | % | CONAPO |
| `ovsee` | % ocupantes en viviendas sin energía eléctrica | float64 | % | CONAPO |
| `ovsae` | % ocupantes en viviendas sin agua entubada | float64 | % | CONAPO |
| `ovpt` | % ocupantes en viviendas con piso de tierra | float64 | % | CONAPO |
| `vhac` | % viviendas con hacinamiento | float64 | % | CONAPO |
| `pl_5000` | % población en localidades < 5,000 hab. | float64 | % | CONAPO |
| `po2sm` | % población ocupada con ingreso hasta 2 salarios mínimos | float64 | % | CONAPO |

## `data/interim/conapo_proyecciones_quinq.parquet` (252,450 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal | string | — | CONAPO |
| `cve_ent` | Entidad | string | — | CONAPO |
| `nom_ent` | Entidad | str | — | CONAPO |
| `nom_mun` | Municipio | str | — | CONAPO |
| `sexo` | HOMBRES / MUJERES | str | — | CONAPO |
| `anio` | Año (1 de julio) | Int64 | — | CONAPO |
| `pob_total` | Población a mitad de año | int64 | personas | CONAPO |
| `pob_15_mas` | Población 15+ (suma de grupos) | int64 | personas | CONAPO |
| `pob_18_mas_aprox` | Población 18+ aproximada: 15+ menos 3/5 del grupo 15–19 (el grupo exacto no existe) | float64 | personas | CONAPO |
| `pob_00_04` |  | int64 |  | CONAPO |
| `pob_05_09` |  | int64 |  | CONAPO |
| `pob_010_014` |  | int64 |  | CONAPO |
| `pob_015_019` |  | int64 |  | CONAPO |
| `pob_20_24` |  | int64 |  | CONAPO |
| `pob_25_29` |  | int64 |  | CONAPO |
| `pob_30_34` |  | int64 |  | CONAPO |
| `pob_35_39` |  | int64 |  | CONAPO |
| `pob_40_44` |  | int64 |  | CONAPO |
| `pob_45_49` |  | int64 |  | CONAPO |
| `pob_50_54` |  | int64 |  | CONAPO |
| `pob_55_59` |  | int64 |  | CONAPO |
| `pob_60_64` |  | int64 |  | CONAPO |
| `pob_65_69` |  | int64 |  | CONAPO |
| `pob_70_74` |  | int64 |  | CONAPO |
| `pob_75_79` |  | int64 |  | CONAPO |
| `pob_80_84` |  | int64 |  | CONAPO |
| `pob_85_mm` |  | int64 |  | CONAPO |

## `data/interim/conapo_proyecciones_inddemo.parquet` (126,225 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_ent` |  | string |  | CONAPO |
| `nom_ent` |  | str |  | CONAPO |
| `nom_mun` |  | str |  | CONAPO |
| `hom_mit_ano` |  | int64 |  | CONAPO |
| `muj_mit_ano` |  | int64 |  | CONAPO |
| `pob_mit_mun` | Población a mitad de año | int64 | personas | CONAPO |
| `muj_00_014` |  | int64 |  | CONAPO |
| `hom_00_014` |  | int64 |  | CONAPO |
| `pob_00_014` |  | int64 |  | CONAPO |
| `muj_015_64` |  | int64 |  | CONAPO |
| `hom_015_64` |  | int64 |  | CONAPO |
| `pob_015_64` | Población 15–64 | int64 | personas | CONAPO |
| `muj_60_mas` |  | int64 |  | CONAPO |
| `hom_60_mas` |  | int64 |  | CONAPO |
| `pob_60_mas` |  | int64 |  | CONAPO |
| `muj_65_mas` |  | int64 |  | CONAPO |
| `hom_65_mas` |  | int64 |  | CONAPO |
| `pob_65_mas` |  | int64 |  | CONAPO |
| `pob_mit_ent` |  | int64 |  | CONAPO |
| `edad_med` | Edad mediana | int64 | años | CONAPO |
| `por_mun` |  | float64 |  | CONAPO |
| `ind_env_60` |  | float64 |  | CONAPO |
| `ind_env_65` |  | float64 |  | CONAPO |
| `rhm` |  | float64 |  | CONAPO |
| `raz_dep_adu` |  | float64 |  | CONAPO |
| `raz_dep_inf` |  | float64 |  | CONAPO |
| `raz_dep` | Razón de dependencia | float64 | por 100 | CONAPO |
| `nom_ent_etq` |  | float64 |  | CONAPO |
| `cve_mun` | Clave municipal | string | — | CONAPO |
| `anio` | Año | Int64 | — | CONAPO |

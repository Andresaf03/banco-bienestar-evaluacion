# Diccionario: catálogo de municipios y crosswalk

Ver `crosswalk_municipios.md` para el método y los casos. Fuentes: MG 2024 (INEGI), wscatgeo (INEGI), BDIF (CNBV), ITER 2010/2020 (INEGI), IMM 2010/2015/2020 (CONAPO).

## `data/interim/municipios.parquet` (2,478 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal 5 dígitos | str | — | INEGI/CNBV/CONAPO |
| `cve_ent` | Clave de entidad | str | — | INEGI/CNBV/CONAPO |
| `nom_mun` | Nombre (MG 2024, o wscatgeo/BDIF si no está en MG) | str | — | INEGI/CNBV/CONAPO |
| `nom_ent` | Entidad | str | — | INEGI/CNBV/CONAPO |
| `nom_cab` | Cabecera municipal (wscatgeo) | str | — | INEGI/CNBV/CONAPO |
| `pob_total_2020` | Población censal 2020 (wscatgeo) | float64 | personas | INEGI/CNBV/CONAPO |
| `en_mg2024` | Tiene polígono en MG dic. 2024 | bool | bool | INEGI/CNBV/CONAPO |
| `en_iter2010` | Aparece en ITER 2010 | bool | bool | INEGI/CNBV/CONAPO |
| `en_iter2020` | Aparece en ITER 2020 | bool | bool | INEGI/CNBV/CONAPO |
| `en_imm2010` | Aparece en IMM 2010 | bool | bool | INEGI/CNBV/CONAPO |
| `en_imm2015` | Aparece en IMM 2015 | bool | bool | INEGI/CNBV/CONAPO |
| `en_imm2020` | Aparece en IMM 2020 | bool | bool | INEGI/CNBV/CONAPO |
| `en_bdif` | Aparece en algún trimestre BDIF 2016T1–2025T4 | bool | bool | INEGI/CNBV/CONAPO |
| `bdif_desde` | Primer trimestre en BDIF | str | YYYYQn | INEGI/CNBV/CONAPO |
| `bdif_hasta` | Último trimestre en BDIF | str | YYYYQn | INEGI/CNBV/CONAPO |
| `bdif_t_min` | t del primer trimestre | float64 | — | INEGI/CNBV/CONAPO |
| `bdif_t_max` | t del último | float64 | — | INEGI/CNBV/CONAPO |
| `bdif_n_trimestres` | Trimestres observados | float64 | — | INEGI/CNBV/CONAPO |
| `bdif_completo` | Observado en los 40 trimestres | bool | bool | INEGI/CNBV/CONAPO |
| `alta_estimada` | Primer trimestre BDIF si no estaba en 2016T1 (alta) | str | YYYYQn | INEGI/CNBV/CONAPO |
| `baja_estimada` | Último trimestre si desaparece y no está en MG 2024 | str | YYYYQn | INEGI/CNBV/CONAPO |

## `data/interim/crosswalk_municipios.parquet` (2,478 filas)

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave vigente (MG 2024) | str | — | INEGI/CNBV/CONAPO |
| `nom_mun` | Nombre | str | — | INEGI/CNBV/CONAPO |
| `cve_ent` | Entidad | str | — | INEGI/CNBV/CONAPO |
| `cve_estable` | Clave de la unidad estable (municipio de 2010 del que proviene; igual a cve_mun si es estable) | str | — | INEGI/CNBV/CONAPO |
| `tipo` | estable | hijo | padre_donante | baja_sin_poligono_2024 | str | categoría | INEGI/CNBV/CONAPO |
| `en_iter2010` | Existía en 2010 | bool | bool | INEGI/CNBV/CONAPO |
| `bdif_desde` | Primer trimestre en BDIF | str | YYYYQn | INEGI/CNBV/CONAPO |
| `alta_estimada` | Alta estimada | str | YYYYQn | INEGI/CNBV/CONAPO |
| `padre_espacial` | Clave 2010 con más población 2010 dentro del polígono 2024 | string | — | INEGI/CNBV/CONAPO |
| `share_padre` | Participación del padre en la población 2010 del polígono | float64 | proporción | INEGI/CNBV/CONAPO |
| `n_loc_padre` | Localidades 2010 del padre dentro del polígono | int64 | — | INEGI/CNBV/CONAPO |
| `pob_2010_padre` | Población 2010 de esas localidades | int64 | personas | INEGI/CNBV/CONAPO |
| `otros_donantes_2010` | Otras claves 2010 con localidades dentro del polígono | str | — | INEGI/CNBV/CONAPO |
| `revisar` | share_padre < 0.9 o sin padre | bool | bool | INEGI/CNBV/CONAPO |

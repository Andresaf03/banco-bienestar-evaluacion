# Diccionario: paneles de estimación (`data/processed/`)

Los cuatro paneles comparten estructura para poder correr el mismo código de estimación sobre los
tres niveles de agregación y comparar. Los construye `proyecto.construccion.panel` (`make panel`).

| panel | unidad | tiempo | periodos | resultados |
|---|---|---|---|---|
| `panel_localidad.parquet` | localidad (`cve_loc`, 9 dígitos) | `s` (semestre) | 2016S1–2025S1 (18 versiones) | DENUE: 4 bloques |
| `panel_municipio.parquet` | municipio (`cve_mun`) | `s` | 18 | DENUE: 4 bloques |
| `panel_anillo.parquet` | localidad × radio | `s` | 18 | DENUE dentro de 1/2/5/10 km |
| `panel_municipio_trim.parquet` | municipio | `t` (trimestre) | 2019T1–2024T4 (24) | CNBV: financieras |

## Columnas comunes

| variable | descripción |
|---|---|
| `cve_loc` / `cve_mun` | Identificador de la unidad; texto, nunca se une por nombre |
| `periodo` / `semestre` | Etiqueta del periodo (`2022Q1`, `2022S1`) |
| `t` / `s` | Índice entero consecutivo (2019Q1 = 1; 2016S1 = 1) |
| `G` | Primer periodo con sucursal del Banco del Bienestar, en la misma escala que `t`/`s`. **0 = nunca tratado** en la ventana, como exige `did` |
| `G_trimestre` / `G_semestre` | La misma fecha con etiqueta legible |
| `tratado` | `1{t >= G, G > 0}` |
| `n_cohorte` | Unidades que comparten ese `G`. Las cohortes de una o dos unidades no tienen varianza utilizable y se excluyen (`min_cohorte = 5`) |
| `ya_tratado_inicio` | La unidad ya tenía sucursal en el primer periodo (herencia Bansefi): se excluye de la especificación principal |
| `fecha_ambigua` | Solo en paneles de localidad: el municipio tiene 2+ sucursales, así que la fecha municipal no identifica a esta localidad |
| `sospechoso_banjercito` | Posible sucursal nueva de Banjército posterior a 2021 (ver `docs/data_audit.md` P2) |
| `pobtot` / `poblacion_adulta` | Denominador de las tasas |
| `indice_marginacion_2020`, `grado_marginacion_2020`, `poblacion_2020`, `banca_previa` | Covariables **previas** al tratamiento, fijas por unidad |

## Resultados

Los conteos llevan el sufijo `_pc` en su versión normalizada: **por cada mil habitantes** en los
paneles de localidad y **por cada diez mil adultos** en los municipales.

| prefijo | significado |
|---|---|
| `estab_<bloque>` | Establecimientos del bloque (emprendimiento, consumo, salud, financiero) |
| `micro_<bloque>` | Establecimientos de 0 a 5 personas ocupadas (proxy de autoempleo) |
| `empleo_<bloque>` | Empleo estimado con el punto medio del rango de personas ocupadas |
| `estab_farmacia`, `estab_restaurantes`, `estab_abarrotes`, `estab_consultorios`, `estab_banca`, `estab_cajas` | Clases finas dentro de los bloques |
| `sucursales_privado`, `cajeros_privado`, `tpv_privado`, `transacciones_tpv_privado` | CNBV, banca múltiple + SOCAP + SOFIPO |
| `captacion_privado`, `credito_privado` | CNBV; **solo existen desde 2022T4**, así que no tienen periodo previo y el runner los salta |
| `sucursales_total`, `corresponsales_total` | Incluyen banca de desarrollo; resultado secundario (efecto mecánico) |

## Advertencias

1. **Los bloques no son excluyentes**: una farmacia cuenta en `consumo` y en `salud`; todo
   establecimiento cuenta en `emprendimiento`.
2. **2023S1 no existe** en los paneles semestrales: el INEGI no publicó versión del DENUE esa
   primavera. Las unidades cuya apertura cae ahí se asignan al primer periodo observado posterior.
3. **Municipios nuevos**: los 22 creados después de 2010 se colapsan en su municipio de origen en
   los paneles municipales (`crosswalk_municipios.parquet`). Al colapsar se conserva el faltante
   (`sum(min_count=1)`): convertirlo en cero crearía saltos artificiales.
4. Un resultado solo es estimable si tiene **al menos dos periodos previos con dato**.

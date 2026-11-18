# Fase 6: diccionario de datos (2026-11-17)

Preregistro, adenda y resultados en `docs/decisiones.md`. Nada de esto entra a la maestra.

## Insumos nuevos

| archivo | origen | contenido |
|---|---|---|
| `data/raw/pub_bienestar/consMpo<edo>.xlsx` (32) | pub.bienestar.gob.mx, `/data/v2/cons/` | consolidado municipal vigente del Padrón Único de Beneficiarios: hoja `Municipio` con `Clave Entidad`, `Clave Municipio`, `Nombe Municipio` (sic), `Beneficiarios Unicos`, `Monto`; corte de octubre de 2026 |
| `data/raw/pub_bienestar/historia_2026-11-17.json` | `/v2/api/resume/publish/history` | lista de padrones históricos publicados (28 filas, solo programas terminados); evidencia de la adenda |

Los periodos anteriores de los programas vigentes solo existen como listas de personas con nombre e
importe (`/data/v2/programs/...`, `_p`): **no se descargan**.

## `data/interim/pub_municipio.parquet` (`limpieza/pub_bienestar.py`)

| variable | descripción | tipo |
|---|---|---|
| `cve_mun` | clave INEGI de 5 dígitos (entidad + municipio del padrón; 2,469 de 2,478 cruzan con el Censo 2020, el resto son municipios nuevos) | str |
| `nom_mun_pub` | nombre en el padrón (solo para revisión; nunca se une por nombre) | str |
| `beneficiarios_unicos` | personas con al menos un programa en el último periodo publicado de cada programa | float |
| `monto` | suma de los montos de esos periodos (mezcla periodos trimestrales, bimestrales y anuales: solo compara municipios) | float |

La clave `999` ("no especificado", 187,928 beneficiarios, 0.4%) se descarta.

## `data/processed/panel_localidad_f6.parquet` (`construccion/panel_fase6.py`)

`panel_localidad` más:

| variable | descripción |
|---|---|
| `estab_s46`, `estab_s72`, `estab_s81`, `estab_s3133` | establecimientos del DENUE en comercio al por menor, alimentos y hospedaje, otros servicios y manufactura (SCIAN a 2 dígitos) |
| `estab_consumo_amplio` | 46 + 72 + 81 |
| `estab_resto` | todos menos consumo amplio (incluye manufactura) |
| `estab_sin_52_93` | todos menos servicios financieros (52) y gobierno (93) |
| `*_pc` | por mil habitantes del Censo 2020 (fijo) |
| `G_mun` | semestre efectivo (índice `s`) de la primera apertura del municipio, con la clave estable del crosswalk; 0 sin apertura |
| `mun_ya_tratado` | el municipio tenía sucursal heredada en 2019T1 |
| `prop_65_mas` | población de 65+ / población total del municipio, Censo 2020 |

## `data/processed/pub_municipio_f6.parquet`

Un renglón por municipio estable: tratamiento y covariables de `panel_municipio_trim`, la foto del
padrón con el crosswalk aplicado, población total y de 65+ del Censo 2020, `benef_100hab`,
`monto_pc` y `grupo` (`tratado_2022_2024`, `ya_tratado`, `sin_apertura`).

## Salidas (`outputs/tablas/fase6_*.csv`)

| archivo | qué es |
|---|---|
| `fase6_accesibilidad.csv` | B1: distancia de la población (total y 65+) a la sucursal más cercana por corte, en tres versiones (`cota`): `central`, la que se reporta (las sucursales de un municipio abren en orden de población según el conteo de la BDIF), y las cotas `optimista` y `pesimista`; nacional, por marginación y por tamaño de localidad |
| `fase6_cobro_local.csv` | B2: transacciones en cajeros del banco por beneficiario único y bimestre, ene–jul 2026 |
| `fase6_enif_apoyos.csv` | B3: ENIF 2021 y 2024 entre quienes reciben apoyos (cuenta, uso de sucursal, lejanía, minutos) |
| `fase6_pub_medias.csv`, `fase6_pub_ajuste.csv` | A-foto: beneficiarios y monto por grupo, en bruto y ajustado |
| `fase6_sectores.csv`, `fase6_composicion.csv` | C1–C2 |
| `fase6_reubicacion.csv` | C3 y C3b |
| `fase6_dosis_estab_emprendimiento_pc.csv` | C4 |
| `fase6_radios_estab_emprendimiento_pc.csv` | C5: `att`/`ee` promedio por localidad; `att_pond`/`ee_pond` ponderados por población; `estab_implicados` (con el ponderado) y `pct_del_total`; `estab_implicados_sin_ponderar` y `pct_del_total_sin_ponderar` |
| `fase6_cabeceras.csv` | C6 y C6b |
| `fase6_controles.csv`, `fase6_deriva_nunca_tratados.csv` | D (estimaciones ya hechas, reunidas) |
| `fase6_resumen.csv`, `fase6_lectura_denue.csv` | lectura con Romano–Wolf, BH y la regla preregistrada |

## Códigos de la ENIF que cambian entre ediciones

`P10_2` (razón para no usar sucursal): "están muy lejos o no hay" es `4` en 2021 (descriptor) y `05`
en 2024 (diccionario del INEGI, catálogo 1081, variable V8863), que agregó "prefiere las
aplicaciones" y "no ha tenido necesidad". Factor de expansión: `FAC_ELE` (2021), `FAC_PER` (2024).

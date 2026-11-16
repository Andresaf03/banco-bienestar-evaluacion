# Diccionario: CNBV, BDIF municipal (`data/interim/cnbv_bdif.parquet`)

Formato largo: una fila por municipio × trimestre × sector × variable. Solo conteos absolutos; los indicadores 'por cada 10 mil adultos' se descartan y se recalculan en el panel.

## Columnas

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal INEGI, texto de 5 dígitos | string | — | CNBV 'Clave Municipio' |
| `periodo` | Trimestre `YYYYQn` (mes de cierre 03/06/09/12) | string | — | nombre del archivo |
| `t` | Índice consecutivo, 2019Q1 = 1 (2016Q1 = −11) | int | — | derivado |
| `sector` | Ver tabla de sectores | string | — | encabezado multinivel u hoja |
| `variable` | Ver tabla de variables | string | — | encabezado |
| `valor` | Valor numérico (NaN si la celda venía vacía o no numérica) | float | según variable | celda |
| `hoja` | Hoja de origen en el Excel | string | — | — |
| `archivo` | Archivo de origen | string | — | — |

## Sectores

| sector | significado |
|---|---|
| `todos` | Todos los sectores (banca múltiple + desarrollo + SOCAP + SOFIPO) |
| `banca` | Banca = múltiple + desarrollo combinadas (única desagregación antes de 2022T4 en captación/crédito/transacciones) |
| `banca_multiple` | Banca múltiple (comercial) |
| `banca_desarrollo` | Banca de desarrollo (Banco del Bienestar + Banjercito; no separables a nivel municipal) |
| `socap` | Sociedades Cooperativas de Ahorro y Préstamo |
| `sofipo` | Sociedades Financieras Populares |
| `eacp` | EACP = SOCAP + SOFIPO combinadas |

## Variables y cobertura temporal por sector

| variable | descripción | unidad | sector | primer trimestre | último | n trimestres |
|---|---|---|---|---|---|---|
| `cajeros` | Cajeros automáticos | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cajeros` | Cajeros automáticos | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cajeros` | Cajeros automáticos | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cajeros` | Cajeros automáticos | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cajeros` | Cajeros automáticos | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `capt_ahorro` | Cuentas de ahorro (captación) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `capt_n1` | Cuentas transaccionales nivel 1 | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `capt_n1` | Cuentas transaccionales nivel 1 | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_n1` | Cuentas transaccionales nivel 1 | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_n2` | Cuentas transaccionales nivel 2 | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `capt_n2` | Cuentas transaccionales nivel 2 | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_n2` | Cuentas transaccionales nivel 2 | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_n3` | Cuentas transaccionales nivel 3 | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `capt_n3` | Cuentas transaccionales nivel 3 | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_n3` | Cuentas transaccionales nivel 3 | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_n4` | Cuentas transaccionales nivel 4 (desde 2022T4; antes 'tradicionales') | contratos | `banca` | 2022Q4 | 2025Q4 | 13 |
| `capt_n4` | Cuentas transaccionales nivel 4 (desde 2022T4; antes 'tradicionales') | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_n4` | Cuentas transaccionales nivel 4 (desde 2022T4; antes 'tradicionales') | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_plazo` | Depósitos a plazo | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `capt_plazo` | Depósitos a plazo | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_plazo` | Depósitos a plazo | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_plazo` | Depósitos a plazo | contratos | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `capt_plazo` | Depósitos a plazo | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `capt_plazo` | Depósitos a plazo | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `capt_total` | Total de contratos de captación (solo viene desde 2022T4) | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `capt_total` | Total de contratos de captación (solo viene desde 2022T4) | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `capt_total` | Total de contratos de captación (solo viene desde 2022T4) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `capt_total` | Total de contratos de captación (solo viene desde 2022T4) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `capt_total` | Total de contratos de captación (solo viene desde 2022T4) | contratos | `todos` | 2022Q4 | 2025Q4 | 13 |
| `capt_tradicionales` | Cuentas transaccionales tradicionales (hasta 2022T3; después 'nivel 4') | contratos | `banca` | 2016Q1 | 2022Q3 | 27 |
| `capt_vista` | Depósitos a la vista (EACP) | contratos | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `capt_vista` | Depósitos a la vista (EACP) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `capt_vista` | Depósitos a la vista (EACP) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `corresponsales` | Módulos de corresponsales bancarios; sin sector (solo total). Cambio de metodología en 2019T1; 'corresponsales únicos' desde 2025T4 | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `cred_abcd` | Créditos ABCD (bienes de consumo duradero) | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_abcd` | Créditos ABCD (bienes de consumo duradero) | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_abcd` | Créditos ABCD (bienes de consumo duradero) | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_automotriz` | Créditos automotrices | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_automotriz` | Créditos automotrices | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_automotriz` | Créditos automotrices | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_comercial` | Créditos comerciales (EACP, desde 2022T4) | contratos | `eacp` | 2022Q4 | 2025Q4 | 13 |
| `cred_comercial` | Créditos comerciales (EACP, desde 2022T4) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cred_comercial` | Créditos comerciales (EACP, desde 2022T4) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cred_consumo` | Créditos al consumo (EACP) | contratos | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `cred_consumo` | Créditos al consumo (EACP) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cred_consumo` | Créditos al consumo (EACP) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cred_grupal` | Créditos grupales | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_grupal` | Créditos grupales | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_grupal` | Créditos grupales | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_hipotecario` | Créditos hipotecarios | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_hipotecario` | Créditos hipotecarios | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_hipotecario` | Créditos hipotecarios | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_nomina` | Créditos de nómina | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_nomina` | Créditos de nómina | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_nomina` | Créditos de nómina | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_personal` | Créditos personales | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `cred_personal` | Créditos personales | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_personal` | Créditos personales | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_total` | Total de contratos de crédito (solo viene desde 2022T4) | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cred_total` | Total de contratos de crédito (solo viene desde 2022T4) | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cred_total` | Total de contratos de crédito (solo viene desde 2022T4) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cred_total` | Total de contratos de crédito (solo viene desde 2022T4) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cred_total` | Total de contratos de crédito (solo viene desde 2022T4) | contratos | `todos` | 2022Q4 | 2025Q4 | 13 |
| `cred_vivienda` | Créditos a la vivienda (EACP) | contratos | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `cred_vivienda` | Créditos a la vivienda (EACP) | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cred_vivienda` | Créditos a la vivienda (EACP) | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cuentas_celular` | Contratos/cuentas que usan banca móvil (transacciones por celular) | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `cuentas_celular` | Contratos/cuentas que usan banca móvil (transacciones por celular) | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `cuentas_celular` | Contratos/cuentas que usan banca móvil (transacciones por celular) | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `cuentas_celular` | Contratos/cuentas que usan banca móvil (transacciones por celular) | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `cuentas_celular` | Contratos/cuentas que usan banca móvil (transacciones por celular) | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `establecimientos_tpv` | Establecimientos con TPV | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `establecimientos_tpv` | Establecimientos con TPV | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `establecimientos_tpv` | Establecimientos con TPV | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `establecimientos_tpv` | Establecimientos con TPV | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `establecimientos_tpv` | Establecimientos con TPV | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `modulos_compartamos` | Módulos de atención de Compartamos (2017T2–2018T4; la CNBV los contaba aparte de sucursales de banca comercial) | número | `banca_multiple` | 2017Q2 | 2018Q4 | 7 |
| `sucursales` | Sucursales en operación | número | `banca_desarrollo` | 2016Q1 | 2025Q4 | 40 |
| `sucursales` | Sucursales en operación | número | `banca_multiple` | 2016Q1 | 2025Q4 | 40 |
| `sucursales` | Sucursales en operación | número | `socap` | 2016Q1 | 2025Q4 | 40 |
| `sucursales` | Sucursales en operación | número | `sofipo` | 2016Q1 | 2025Q4 | 40 |
| `sucursales` | Sucursales en operación | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `banca` | 2016Q1 | 2025Q4 | 40 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `eacp` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `socap` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_credito` | Tarjetas de crédito | contratos | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_debito` | Tarjetas de débito | número | `banca` | 2016Q1 | 2025Q4 | 40 |
| `tarjetas_debito` | Tarjetas de débito | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_debito` | Tarjetas de débito | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_debito` | Tarjetas de débito | número | `eacp` | 2016Q1 | 2025Q4 | 40 |
| `tarjetas_debito` | Tarjetas de débito | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `tarjetas_debito` | Tarjetas de débito | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `tpv` | Terminales punto de venta | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `tpv` | Terminales punto de venta | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `tpv` | Terminales punto de venta | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `tpv` | Terminales punto de venta | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `tpv` | Terminales punto de venta | número | `todos` | 2016Q1 | 2025Q4 | 40 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `banca` | 2016Q1 | 2022Q3 | 27 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `eacp` | 2019Q1 | 2022Q3 | 15 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_cajeros` | Transacciones en cajeros automáticos en el trimestre | número | `todos` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `banca` | 2016Q1 | 2022Q3 | 27 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `banca_desarrollo` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `banca_multiple` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `eacp` | 2019Q1 | 2022Q3 | 15 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `socap` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `sofipo` | 2022Q4 | 2025Q4 | 13 |
| `transacciones_tpv` | Transacciones en TPV en el trimestre | número | `todos` | 2022Q4 | 2025Q4 | 13 |
| `usuarios_hombres` | Socios (SOCAP) / clientes (SOFIPO) / usuarios (EACP) | personas | `socap` | 2018Q3 | 2022Q3 | 17 |
| `usuarios_hombres` | Socios (SOCAP) / clientes (SOFIPO) / usuarios (EACP) | personas | `sofipo` | 2018Q3 | 2022Q3 | 17 |
| `usuarios_mujeres` | Socias (SOCAP) / clientas (SOFIPO) / usuarias (EACP) | personas | `socap` | 2018Q3 | 2022Q3 | 17 |
| `usuarios_mujeres` | Socias (SOCAP) / clientas (SOFIPO) / usuarias (EACP) | personas | `sofipo` | 2018Q3 | 2022Q3 | 17 |

## Eras de layout y cómo se unificaron

| era | trimestres | hojas municipales | notas |
|---|---|---|---|
| A | 2016T1–2017T4 | `BD Acceso Mun`, `BD Uso Mun`, `BD Uso EACP Mun` | Encabezado plano (fila 8/9). Sucursales por sector; captación/crédito/transacciones solo 'Banca (Comercial y de Desarrollo)' y 'EACP'. 2016T1 usa 'Banca Comercial/Banca de Desarrollo/Cooperativas/Microfinancieras'; desde 2016T2 'Sucursales banca comercial/... Socap/... Sofipo'. Trae 'Superficie km2'. Cajeros y TPV sin sector. |
| B | 2018T1–2018T4 | `BD Acceso Mun`, `BD Uso Banca Mun`, `BD Uso EACP Mun`, `BD Género Mun` | Encabezado en fila 12. Agrega población adulta por sexo y 'Módulos de atención Compartamos'. Mismo alcance sectorial que A. |
| C | 2019T1–2022T3 | `BD Infraestructura Mun`, `BD Tenencia Uso Banca Mun`, `BD Tenencia Uso EACP Mun`, `BD Género Mun` | Encabezado en fila 12. Renombra hojas; agrega transacciones y usuarios (socios/clientes) para EACP. Desde 2020T2 'Cajeros automáticos' y 'Sucursales Banca comercial' (mayúscula). Mismo alcance sectorial que A/B. |
| D | 2022T4–2025T4 | `BD Infraestructura Mun`, `BD Captación Mun`, `BD Crédito Mun`, `BD por sexo Banca Mun`, `BD por sexo EACP Mun` (+ hojas por institución a nivel nacional desde 2023T3) | Encabezado multinivel (filas 10–12): sector × bloque × variable. **Todo por sector** (banca múltiple, desarrollo, SOCAP, SOFIPO) y además totales 'Banca' y 'EACP'. Corresponsales solo total. Aparece 'Índice de rezago social' (2023T1). Población: 'Población total/adulta' (2022T4–2024T4) y 'Población/Población Adulta' (2025). |

La unificación la hace `proyecto.limpieza.bdif_columnas.clasificar`: normaliza el encabezado (minúsculas, sin acentos, sin sufijos 'Número de cuentas/créditos'), detecta el sector en los renglones superiores y el bloque (infraestructura/captación/crédito/transacciones) y asigna el nombre canónico. La bitácora completa columna por columna está en `data/interim/cnbv_bdif_columnas.csv`.

## Encabezados originales por variable canónica

| sector | variable | hoja | encabezado original (niveles → encabezado) | trimestres |
|---|---|---|---|---|
| `banca_desarrollo` | `cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Infraestructura → Cajeros automáticos Número | 202212–202512 (13) |
| `banca_multiple` | `cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Infraestructura → Cajeros automáticos Número | 202212–202512 (13) |
| `socap` | `cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Infraestructura → Cajeros automáticos Número | 202212–202512 (13) |
| `sofipo` | `cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Infraestructura → Cajeros automáticos Número | 202212–202512 (13) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Cajeros | 201603–201603 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Cajeros | 201606–201606 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Cajeros | 201609–201609 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Cajeros | 201612–201612 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Cajeros | 201703–201703 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Cajeros | 201706–201706 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Cajeros | 201709–201709 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Cajeros | 201712–201712 (1) |
| `todos` | `cajeros` | BD Acceso Mun | Número de puntos de acceso → Cajeros | 201803–201812 (4) |
| `todos` | `cajeros` | BD Infraestructura Mun | Número de puntos de acceso → Cajeros | 201903–202003 (5) |
| `todos` | `cajeros` | BD Infraestructura Mun | Número de puntos de acceso → Cajeros automáticos | 202006–202209 (10) |
| `todos` | `cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Cajeros automáticos Número | 202212–202512 (13) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Cuentas de ahorro | 201603–201603 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201606–201606 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201609–201609 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201612–201612 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201703–201703 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201706–201706 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201709–201709 (1) |
| `banca` | `capt_ahorro` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201712–201712 (1) |
| `banca` | `capt_ahorro` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Cuentas de ahorro | 201803–201812 (4) |
| `banca` | `capt_ahorro` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Cuentas de ahorro | 201903–202209 (15) |
| `banca` | `capt_ahorro` | BD Captación Mun | Captación | Todos los sectores | Banca → Ahorro Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_ahorro` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Ahorro Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_ahorro` | BD Captación Mun | Captación | Banca múltiple | Captación → Ahorro Número de cuentas | 202212–202512 (13) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Captación → Depósito al ahorro | 201603–201603 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Captación → Depósito al ahorro | 201606–201606 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Captación → Depósito al ahorro | 201609–201609 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Captación → Depósito al ahorro | 201612–201612 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Captación → Depósito al ahorro | 201703–201703 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Captación → Depósito al ahorro | 201706–201706 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Captación → Depósito al ahorro | 201709–201709 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Captación → Depósito al ahorro | 201712–201712 (1) |
| `eacp` | `capt_ahorro` | BD Uso EACP Mun | Número de contratos - EACP | Captación → Depósito al ahorro | 201803–201812 (4) |
| `eacp` | `capt_ahorro` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósito al ahorro | 201903–202003 (5) |
| `eacp` | `capt_ahorro` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósitos al ahorro | 202006–202209 (10) |
| `eacp` | `capt_ahorro` | BD Captación Mun | Captación | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Ahorro Número de cuentas | 202212–202512 (13) |
| `socap` | `capt_ahorro` | BD Captación Mun | Captación | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Ahorro Número de cuentas | 202212–202512 (13) |
| `sofipo` | `capt_ahorro` | BD Captación Mun | Captación | Sociedades Financieras Populares | Captación → Ahorro Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Cuentas transaccionales Nivel 1 | 201603–201603 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201606–201606 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201609–201609 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201612–201612 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201703–201703 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201706–201706 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201709–201709 (1) |
| `banca` | `capt_n1` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201712–201712 (1) |
| `banca` | `capt_n1` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 1 | 201803–201812 (4) |
| `banca` | `capt_n1` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Cuentas transaccionales nivel 1 | 201903–202209 (15) |
| `banca` | `capt_n1` | BD Captación Mun | Captación | Todos los sectores | Banca → Transaccionales Nivel 1 Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_n1` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Transaccionales Nivel 1 Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_n1` | BD Captación Mun | Captación | Banca múltiple | Captación → Transaccionales Nivel 1 Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Cuentas transaccionales Nivel 2 | 201603–201603 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201606–201606 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201609–201609 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201612–201612 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201703–201703 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201706–201706 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201709–201709 (1) |
| `banca` | `capt_n2` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201712–201712 (1) |
| `banca` | `capt_n2` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 2 | 201803–201812 (4) |
| `banca` | `capt_n2` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Cuentas transaccionales nivel 2 | 201903–202209 (15) |
| `banca` | `capt_n2` | BD Captación Mun | Captación | Todos los sectores | Banca → Transaccionales Nivel 2 Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_n2` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Transaccionales Nivel 2 Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_n2` | BD Captación Mun | Captación | Banca múltiple | Captación → Transaccionales Nivel 2 Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Cuentas transaccionales Nivel 3 | 201603–201603 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201606–201606 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201609–201609 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201612–201612 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201703–201703 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201706–201706 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201709–201709 (1) |
| `banca` | `capt_n3` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201712–201712 (1) |
| `banca` | `capt_n3` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales nivel 3 | 201803–201812 (4) |
| `banca` | `capt_n3` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Cuentas transaccionales nivel 3 | 201903–202209 (15) |
| `banca` | `capt_n3` | BD Captación Mun | Captación | Todos los sectores | Banca → Transaccionales Nivel 3 Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_n3` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Transaccionales Nivel 3 Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_n3` | BD Captación Mun | Captación | Banca múltiple | Captación → Transaccionales Nivel 3 Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_n4` | BD Captación Mun | Captación | Todos los sectores | Banca → Transaccionales Nivel 4 Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_n4` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Transaccionales Nivel 4 Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_n4` | BD Captación Mun | Captación | Banca múltiple | Captación → Transaccionales Nivel 4 Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Depósitos a plazo | 201603–201603 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201606–201606 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201609–201609 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201612–201612 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201703–201703 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201706–201706 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201709–201709 (1) |
| `banca` | `capt_plazo` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201712–201712 (1) |
| `banca` | `capt_plazo` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Depósitos a plazo | 201803–201812 (4) |
| `banca` | `capt_plazo` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Depósitos a plazo | 201903–202209 (15) |
| `banca` | `capt_plazo` | BD Captación Mun | Captación | Todos los sectores | Banca → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_plazo` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_plazo` | BD Captación Mun | Captación | Banca múltiple | Captación → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Captación → Depósito a plazo | 201603–201603 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Captación → Depósito a plazo | 201606–201606 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Captación → Depósito a plazo | 201609–201609 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Captación → Depósito a plazo | 201612–201612 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Captación → Depósito a plazo | 201703–201703 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Captación → Depósito a plazo | 201706–201706 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Captación → Depósito a plazo | 201709–201709 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Captación → Depósito a plazo | 201712–201712 (1) |
| `eacp` | `capt_plazo` | BD Uso EACP Mun | Número de contratos - EACP | Captación → Depósito a plazo | 201803–201812 (4) |
| `eacp` | `capt_plazo` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósito a plazo | 201903–202003 (5) |
| `eacp` | `capt_plazo` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósitos a plazo | 202006–202209 (10) |
| `eacp` | `capt_plazo` | BD Captación Mun | Captación | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `socap` | `capt_plazo` | BD Captación Mun | Captación | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `sofipo` | `capt_plazo` | BD Captación Mun | Captación | Sociedades Financieras Populares | Captación → Depósitos a plazo Número de cuentas | 202212–202512 (13) |
| `banca_desarrollo` | `capt_total` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Total Número de cuentas | 202212–202512 (13) |
| `banca_multiple` | `capt_total` | BD Captación Mun | Captación | Banca múltiple | Captación → Total Número de cuentas | 202212–202512 (13) |
| `socap` | `capt_total` | BD Captación Mun | Captación | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Total Número de cuentas | 202212–202512 (13) |
| `sofipo` | `capt_total` | BD Captación Mun | Captación | Sociedades Financieras Populares | Captación → Total Número de cuentas | 202212–202512 (13) |
| `todos` | `capt_total` | BD Captación Mun | Captación | Todos los sectores | Total → Total Número de cuentas | 202212–202512 (13) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Cuentas transaccionales tradicionales | 201603–201603 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201606–201606 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201609–201609 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201612–201612 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201703–201703 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201706–201706 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201709–201709 (1) |
| `banca` | `capt_tradicionales` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201712–201712 (1) |
| `banca` | `capt_tradicionales` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Cuentas transaccionales tradicionales | 201803–201812 (4) |
| `banca` | `capt_tradicionales` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Cuentas transaccionales tradicionales | 201903–202209 (15) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Captación → Depósito a la vista | 201603–201603 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Captación → Depósito a la vista | 201606–201606 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Captación → Depósito a la vista | 201609–201609 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Captación → Depósito a la vista | 201612–201612 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Captación → Depósito a la vista | 201703–201703 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Captación → Depósito a la vista | 201706–201706 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Captación → Depósito a la vista | 201709–201709 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Captación → Depósito a la vista | 201712–201712 (1) |
| `eacp` | `capt_vista` | BD Uso EACP Mun | Número de contratos - EACP | Captación → Depósito a la vista | 201803–201812 (4) |
| `eacp` | `capt_vista` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósito a la vista | 201903–202003 (5) |
| `eacp` | `capt_vista` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Depósitos a la vista | 202006–202209 (10) |
| `eacp` | `capt_vista` | BD Captación Mun | Captación | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Depósitos a la vista Número de cuentas | 202212–202512 (13) |
| `socap` | `capt_vista` | BD Captación Mun | Captación | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a la vista Número de cuentas | 202212–202512 (13) |
| `sofipo` | `capt_vista` | BD Captación Mun | Captación | Sociedades Financieras Populares | Captación → Depósitos a la vista Número de cuentas | 202212–202512 (13) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Corresponsales1 | 201603–201603 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Corresponsales | 201606–201606 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Corresponsales | 201609–201609 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Corresponsales | 201612–201612 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Corresponsales | 201703–201703 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Corresponsales | 201706–201706 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Corresponsales | 201709–201709 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Corresponsales | 201712–201712 (1) |
| `todos` | `corresponsales` | BD Acceso Mun | Número de puntos de acceso → Corresponsales | 201803–201812 (4) |
| `todos` | `corresponsales` | BD Infraestructura Mun | Número de puntos de acceso → Corresponsales | 201903–202209 (15) |
| `todos` | `corresponsales` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Corresponsales Número | 202212–202509 (12) |
| `todos` | `corresponsales` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Corresponsales únicos Número | 202512–202512 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → ABCD | 201603–201603 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → ABCD | 201606–201606 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → ABCD | 201609–201609 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → ABCD | 201612–201612 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → ABCD | 201703–201703 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → ABCD | 201706–201706 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → ABCD | 201709–201709 (1) |
| `banca` | `cred_abcd` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → ABCD | 201712–201712 (1) |
| `banca` | `cred_abcd` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → ABCD | 201803–201812 (4) |
| `banca` | `cred_abcd` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → ABCD | 201903–202209 (15) |
| `banca` | `cred_abcd` | BD Crédito Mun | Crédito | Todos los sectores | Banca → ABCD Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_abcd` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → ABCD Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_abcd` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → ABCD Número de créditos | 202212–202512 (13) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Automotriz | 201603–201603 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201606–201606 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201609–201609 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201612–201612 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201703–201703 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201706–201706 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201709–201709 (1) |
| `banca` | `cred_automotriz` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Automotriz | 201712–201712 (1) |
| `banca` | `cred_automotriz` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Automotriz | 201803–201812 (4) |
| `banca` | `cred_automotriz` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Automotriz | 201903–202209 (15) |
| `banca` | `cred_automotriz` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Automotriz Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_automotriz` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Automotriz Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_automotriz` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Automotriz Número de créditos | 202212–202512 (13) |
| `eacp` | `cred_comercial` | BD Crédito Mun | Crédito | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Comercial Número de créditos | 202212–202512 (13) |
| `socap` | `cred_comercial` | BD Crédito Mun | Crédito | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Comercial Número de créditos | 202212–202512 (13) |
| `sofipo` | `cred_comercial` | BD Crédito Mun | Crédito | Sociedades Financieras Populares | Crédito → Comercial Número de créditos | 202212–202512 (13) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Crédito → Crédito al consumo | 201603–201603 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Crédito → Crédito al consumo | 201606–201606 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Crédito → Crédito al consumo | 201609–201609 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Crédito → Crédito al consumo | 201612–201612 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Crédito → Crédito al consumo | 201703–201703 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Crédito → Crédito al consumo | 201706–201706 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Crédito → Crédito al consumo | 201709–201709 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Crédito → Crédito al consumo | 201712–201712 (1) |
| `eacp` | `cred_consumo` | BD Uso EACP Mun | Número de contratos - EACP | Crédito → Crédito al consumo | 201803–201812 (4) |
| `eacp` | `cred_consumo` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Crédito → Crédito al consumo | 201903–202209 (15) |
| `eacp` | `cred_consumo` | BD Crédito Mun | Crédito | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Consumo Número de créditos | 202212–202512 (13) |
| `socap` | `cred_consumo` | BD Crédito Mun | Crédito | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Consumo Número de créditos | 202212–202512 (13) |
| `sofipo` | `cred_consumo` | BD Crédito Mun | Crédito | Sociedades Financieras Populares | Crédito → Consumo Número de créditos | 202212–202512 (13) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Grupal | 201603–201603 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Grupal | 201606–201606 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Grupal | 201609–201609 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Grupal | 201612–201612 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Grupal | 201703–201703 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Grupal | 201706–201706 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Grupal | 201709–201709 (1) |
| `banca` | `cred_grupal` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Grupal | 201712–201712 (1) |
| `banca` | `cred_grupal` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Grupal | 201803–201812 (4) |
| `banca` | `cred_grupal` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Grupal | 201903–202209 (15) |
| `banca` | `cred_grupal` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Grupal Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_grupal` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Grupal Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_grupal` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Grupal Número de créditos | 202212–202512 (13) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Hipotecario  | 201603–201603 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201606–201606 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201609–201609 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201612–201612 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201703–201703 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201706–201706 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201709–201709 (1) |
| `banca` | `cred_hipotecario` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201712–201712 (1) |
| `banca` | `cred_hipotecario` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Hipotecario  | 201803–201812 (4) |
| `banca` | `cred_hipotecario` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Hipotecario  | 201903–202209 (15) |
| `banca` | `cred_hipotecario` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Hipotecario Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_hipotecario` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Hipotecario Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_hipotecario` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Hipotecario Número de créditos | 202212–202512 (13) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Nómina | 201603–201603 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Nómina | 201606–201606 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Nómina | 201609–201609 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Nómina | 201612–201612 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Nómina | 201703–201703 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Nómina | 201706–201706 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Nómina | 201709–201709 (1) |
| `banca` | `cred_nomina` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Nómina | 201712–201712 (1) |
| `banca` | `cred_nomina` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Nómina | 201803–201812 (4) |
| `banca` | `cred_nomina` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Nómina | 201903–202209 (15) |
| `banca` | `cred_nomina` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Nómina Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_nomina` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Nómina Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_nomina` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Nómina Número de créditos | 202212–202512 (13) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Personal | 201603–201603 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Personal | 201606–201606 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Personal | 201609–201609 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Personal | 201612–201612 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Personal | 201703–201703 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Personal | 201706–201706 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Personal | 201709–201709 (1) |
| `banca` | `cred_personal` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Personal | 201712–201712 (1) |
| `banca` | `cred_personal` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Personal | 201803–201812 (4) |
| `banca` | `cred_personal` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Personal | 201903–202209 (15) |
| `banca` | `cred_personal` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Personal Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_personal` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Personal Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_personal` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Personal Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cred_total` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Total Número de créditos | 202212–202512 (13) |
| `banca_multiple` | `cred_total` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Total Número de créditos | 202212–202512 (13) |
| `socap` | `cred_total` | BD Crédito Mun | Crédito | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Total Número de créditos | 202212–202512 (13) |
| `sofipo` | `cred_total` | BD Crédito Mun | Crédito | Sociedades Financieras Populares | Crédito → Total Número de créditos | 202212–202512 (13) |
| `todos` | `cred_total` | BD Crédito Mun | Crédito | Todos los sectores | Total → Total Número de créditos | 202212–202512 (13) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201603–201603 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201606–201606 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201609–201609 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201612–201612 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201703–201703 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201706–201706 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201709–201709 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201712–201712 (1) |
| `eacp` | `cred_vivienda` | BD Uso EACP Mun | Número de contratos - EACP | Crédito → Crédito a la vivienda | 201803–201812 (4) |
| `eacp` | `cred_vivienda` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Crédito → Crédito a la vivienda | 201903–202209 (15) |
| `eacp` | `cred_vivienda` | BD Crédito Mun | Crédito | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Vivienda Número de créditos | 202212–202512 (13) |
| `socap` | `cred_vivienda` | BD Crédito Mun | Crédito | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Vivienda Número de créditos | 202212–202512 (13) |
| `sofipo` | `cred_vivienda` | BD Crédito Mun | Crédito | Sociedades Financieras Populares | Crédito → Vivienda Número de créditos | 202212–202512 (13) |
| `banca_desarrollo` | `cuentas_celular` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Infraestructura → Cuentas que efectúan transacciones por celular Número | 202212–202512 (13) |
| `banca_multiple` | `cuentas_celular` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Infraestructura → Cuentas que efectúan transacciones por celular Número | 202212–202512 (13) |
| `socap` | `cuentas_celular` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Infraestructura → Cuentas que efectúan transacciones por celular Número | 202212–202512 (13) |
| `sofipo` | `cuentas_celular` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Infraestructura → Cuentas que efectúan transacciones por celular Número | 202212–202512 (13) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Contratos que afectan por celular | 201603–201603 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201606–201606 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201609–201609 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201612–201612 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201703–201703 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201706–201706 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201709–201709 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Contratos que utilizan banca móvil | 201712–201712 (1) |
| `todos` | `cuentas_celular` | BD Acceso Mun | Número de puntos de acceso → Contratos que utilizan banca móvil | 201803–201812 (4) |
| `todos` | `cuentas_celular` | BD Infraestructura Mun | Número de puntos de acceso → Contratos que utilizan banca móvil | 201903–202209 (15) |
| `todos` | `cuentas_celular` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Cuentas que efectúan transacciones por celular Número | 202212–202512 (13) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Clave  Estado | 201603–201603 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Clave  Estado | 201603–201603 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Clave  Estado | 201603–201603 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Clave  Estado | 201606–201606 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Clave  Estado | 201606–201606 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Clave  Estado | 201606–201606 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Clave  Estado | 201609–201609 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Clave  Estado | 201609–201609 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Clave  Estado | 201609–201609 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Clave  Estado | 201612–201612 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Clave  Estado | 201612–201612 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Clave  Estado | 201612–201612 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Clave  Estado | 201703–201703 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Clave  Estado | 201703–201703 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Clave  Estado | 201703–201703 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Clave  Estado | 201706–201706 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Clave  Estado | 201706–201706 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Clave  Estado | 201706–201706 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Clave  Estado | 201709–201709 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Clave  Estado | 201709–201709 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Clave  Estado | 201709–201709 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Clave  Estado | 201712–201712 (1) |
| `_general` | `cve_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Clave  Estado | 201712–201712 (1) |
| `_general` | `cve_ent` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Clave  Estado | 201712–201712 (1) |
| `_general` | `cve_ent` | BD Acceso Mun | Información general → Clave  Estado | 201803–201812 (4) |
| `_general` | `cve_ent` | BD Género Mun |  | Información general → Clave  Estado | 201803–202209 (19) |
| `_general` | `cve_ent` | BD Uso Banca Mun |  | Información general → Clave  Estado | 201803–201812 (4) |
| `_general` | `cve_ent` | BD Uso EACP Mun |  | Información general → Clave  Estado | 201803–201812 (4) |
| `_general` | `cve_ent` | BD Infraestructura Mun | Información general → Clave  Estado | 201903–202209 (15) |
| `_general` | `cve_ent` | BD Tenencia Uso Banca Mun |  | Información general → Clave  Estado | 201903–202209 (15) |
| `_general` | `cve_ent` | BD Tenencia Uso EACP Mun |  | Información general → Clave  Estado | 201903–202209 (15) |
| `_general` | `cve_ent` | BD Captación Mun |  | Información general |  → Clave  Estado | 202212–202512 (13) |
| `_general` | `cve_ent` | BD Crédito Mun |  | Información general |  → Clave  Estado | 202212–202512 (13) |
| `_general` | `cve_ent` | BD Infraestructura Mun |  | Información general |  → Clave  Estado | 202212–202512 (13) |
| `_general` | `cve_ent` | BD por sexo Banca Mun |  | Información general |  → Clave  Estado | 202212–202512 (13) |
| `_general` | `cve_ent` | BD por sexo EACP Mun |  | Información general |  → Clave  Estado | 202212–202512 (13) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Clave Municipio | 201603–201603 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Clave Municipio | 201603–201603 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Clave Municipio | 201603–201603 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Clave Municipio | 201606–201606 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Clave Municipio | 201606–201606 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Clave Municipio | 201606–201606 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Clave Municipio | 201609–201609 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Clave Municipio | 201609–201609 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Clave Municipio | 201609–201609 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Clave Municipio | 201612–201612 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Clave Municipio | 201612–201612 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Clave Municipio | 201612–201612 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Clave Municipio | 201703–201703 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Clave Municipio | 201703–201703 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Clave Municipio | 201703–201703 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Clave Municipio | 201706–201706 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Clave Municipio | 201706–201706 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Clave Municipio | 201706–201706 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Clave Municipio | 201709–201709 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Clave Municipio | 201709–201709 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Clave Municipio | 201709–201709 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Clave Municipio | 201712–201712 (1) |
| `_general` | `cve_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Clave Municipio | 201712–201712 (1) |
| `_general` | `cve_mun` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Clave Municipio | 201712–201712 (1) |
| `_general` | `cve_mun` | BD Acceso Mun | Información general → Clave Municipio | 201803–201812 (4) |
| `_general` | `cve_mun` | BD Género Mun |  | Información general → Clave Municipio | 201803–202209 (19) |
| `_general` | `cve_mun` | BD Uso Banca Mun |  | Información general → Clave Municipio | 201803–201812 (4) |
| `_general` | `cve_mun` | BD Uso EACP Mun |  | Información general → Clave Municipio | 201803–201812 (4) |
| `_general` | `cve_mun` | BD Infraestructura Mun | Información general → Clave Municipio | 201903–202209 (15) |
| `_general` | `cve_mun` | BD Tenencia Uso Banca Mun |  | Información general → Clave Municipio | 201903–202209 (15) |
| `_general` | `cve_mun` | BD Tenencia Uso EACP Mun |  | Información general → Clave Municipio | 201903–202209 (15) |
| `_general` | `cve_mun` | BD Captación Mun |  | Información general |  → Clave Municipio | 202212–202512 (13) |
| `_general` | `cve_mun` | BD Crédito Mun |  | Información general |  → Clave Municipio | 202212–202512 (13) |
| `_general` | `cve_mun` | BD Infraestructura Mun |  | Información general |  → Clave Municipio | 202212–202512 (13) |
| `_general` | `cve_mun` | BD por sexo Banca Mun |  | Información general |  → Clave Municipio | 202212–202512 (13) |
| `_general` | `cve_mun` | BD por sexo EACP Mun |  | Información general |  → Clave Municipio | 202212–202512 (13) |
| `banca_desarrollo` | `establecimientos_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Infraestructura → Establecimientos con TPV Número | 202212–202512 (13) |
| `banca_multiple` | `establecimientos_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Infraestructura → Establecimientos con TPV Número | 202212–202512 (13) |
| `socap` | `establecimientos_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Infraestructura → Establecimientos con TPV Número | 202212–202512 (13) |
| `sofipo` | `establecimientos_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Infraestructura → Establecimientos con TPV Número | 202212–202512 (13) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Establecimientos con TPV | 201603–201603 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Establecimientos con TPV | 201606–201606 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Establecimientos con TPV | 201609–201609 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Establecimientos con TPV | 201612–201612 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Establecimientos con TPV | 201703–201703 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Establecimientos con TPV | 201706–201706 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Establecimientos con TPV | 201709–201709 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Establecimientos con TPV | 201712–201712 (1) |
| `todos` | `establecimientos_tpv` | BD Acceso Mun | Número de puntos de acceso → Establecimientos con TPV | 201803–201812 (4) |
| `todos` | `establecimientos_tpv` | BD Infraestructura Mun | Número de puntos de acceso → Establecimientos con TPV | 201903–202209 (15) |
| `todos` | `establecimientos_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Establecimientos con TPV Número | 202212–202512 (13) |
| `_general` | `indice_rezago_social` | BD Captación Mun |  | Información general |  → Índice de rezago social | 202303–202512 (12) |
| `_general` | `indice_rezago_social` | BD Crédito Mun |  | Información general |  → Índice de rezago social | 202303–202512 (12) |
| `_general` | `indice_rezago_social` | BD Infraestructura Mun |  | Información general |  → Índice de rezago social | 202303–202512 (12) |
| `_general` | `indice_rezago_social` | BD por sexo Banca Mun |  | Información general |  → Índice de rezago social | 202303–202512 (12) |
| `_general` | `indice_rezago_social` | BD por sexo EACP Mun |  | Información general |  → Índice de rezago social | 202303–202512 (12) |
| `banca_multiple` | `modulos_compartamos` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Módulos de atención Compartamos | 201706–201706 (1) |
| `banca_multiple` | `modulos_compartamos` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Módulos de atención Compartamos | 201709–201709 (1) |
| `banca_multiple` | `modulos_compartamos` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Módulos de atención Compartamos | 201712–201712 (1) |
| `banca_multiple` | `modulos_compartamos` | BD Acceso Mun | Número de puntos de acceso → Módulos de atención Compartamos | 201803–201812 (4) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Estado | 201603–201603 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Estado | 201603–201603 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Estado | 201603–201603 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Estado | 201606–201606 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Estado | 201606–201606 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Estado | 201606–201606 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Estado | 201609–201609 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Estado | 201609–201609 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Estado | 201609–201609 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Estado | 201612–201612 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Estado | 201612–201612 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Estado | 201612–201612 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Estado | 201703–201703 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Estado | 201703–201703 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Estado | 201703–201703 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Estado | 201706–201706 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Estado | 201706–201706 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Estado | 201706–201706 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Estado | 201709–201709 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Estado | 201709–201709 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Estado | 201709–201709 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Estado | 201712–201712 (1) |
| `_general` | `nom_ent` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Estado | 201712–201712 (1) |
| `_general` | `nom_ent` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Estado | 201712–201712 (1) |
| `_general` | `nom_ent` | BD Acceso Mun | Información general → Estado | 201803–201812 (4) |
| `_general` | `nom_ent` | BD Género Mun |  | Información general → Estado | 201803–202209 (19) |
| `_general` | `nom_ent` | BD Uso Banca Mun |  | Información general → Estado | 201803–201812 (4) |
| `_general` | `nom_ent` | BD Uso EACP Mun |  | Información general → Estado | 201803–201812 (4) |
| `_general` | `nom_ent` | BD Infraestructura Mun | Información general → Estado | 201903–202209 (15) |
| `_general` | `nom_ent` | BD Tenencia Uso Banca Mun |  | Información general → Estado | 201903–202209 (15) |
| `_general` | `nom_ent` | BD Tenencia Uso EACP Mun |  | Información general → Estado | 201903–202209 (15) |
| `_general` | `nom_ent` | BD Captación Mun |  | Información general |  → Estado | 202212–202512 (13) |
| `_general` | `nom_ent` | BD Crédito Mun |  | Información general |  → Estado | 202212–202512 (13) |
| `_general` | `nom_ent` | BD Infraestructura Mun |  | Información general |  → Estado | 202212–202512 (13) |
| `_general` | `nom_ent` | BD por sexo Banca Mun |  | Información general |  → Estado | 202212–202512 (13) |
| `_general` | `nom_ent` | BD por sexo EACP Mun |  | Información general |  → Estado | 202212–202512 (13) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Municipio | 201603–201603 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Municipio | 201603–201603 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Municipio | 201603–201603 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Municipio | 201606–201606 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Municipio | 201606–201606 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Municipio | 201606–201606 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Municipio | 201609–201609 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Municipio | 201609–201609 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Municipio | 201612–201612 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Municipio | 201612–201612 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Municipio | 201612–201612 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Municipio | 201703–201703 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Municipio | 201703–201703 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Municipio | 201703–201703 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Municipio | 201706–201706 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Municipio | 201706–201706 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Municipio | 201706–201706 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Municipio | 201709–201709 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Municipio | 201709–201709 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Municipio | 201709–201709 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Municipio | 201712–201712 (1) |
| `_general` | `nom_mun` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Municipio | 201712–201712 (1) |
| `_general` | `nom_mun` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Municipio | 201712–201712 (1) |
| `_general` | `nom_mun` | BD Acceso Mun | Información general → Municipio | 201803–201812 (4) |
| `_general` | `nom_mun` | BD Género Mun |  | Información general → Municipio | 201803–202209 (19) |
| `_general` | `nom_mun` | BD Uso Banca Mun |  | Información general → Municipio | 201803–201812 (4) |
| `_general` | `nom_mun` | BD Uso EACP Mun |  | Información general → Municipio | 201803–201812 (4) |
| `_general` | `nom_mun` | BD Infraestructura Mun | Información general → Municipio | 201903–202209 (15) |
| `_general` | `nom_mun` | BD Tenencia Uso Banca Mun |  | Información general → Municipio | 201903–202209 (15) |
| `_general` | `nom_mun` | BD Tenencia Uso EACP Mun |  | Información general → Municipio | 201903–202209 (15) |
| `_general` | `nom_mun` | BD Captación Mun |  | Información general |  → Municipio | 202212–202512 (13) |
| `_general` | `nom_mun` | BD Crédito Mun |  | Información general |  → Municipio | 202212–202512 (13) |
| `_general` | `nom_mun` | BD Infraestructura Mun |  | Información general |  → Municipio | 202212–202512 (13) |
| `_general` | `nom_mun` | BD por sexo Banca Mun |  | Información general |  → Municipio | 202212–202512 (13) |
| `_general` | `nom_mun` | BD por sexo EACP Mun |  | Información general |  → Municipio | 202212–202512 (13) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Población | 201603–201603 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Población | 201603–201603 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Población | 201603–201603 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Población | 201606–201606 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Población | 201606–201606 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Población | 201606–201606 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Población | 201609–201609 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Población | 201609–201609 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Población | 201609–201609 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Población | 201612–201612 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Población | 201612–201612 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Población | 201612–201612 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Población | 201703–201703 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Población | 201703–201703 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Población | 201703–201703 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Población | 201706–201706 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Población | 201706–201706 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Población | 201706–201706 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Población | 201709–201709 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Población | 201709–201709 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Población | 201709–201709 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Población | 201712–201712 (1) |
| `_general` | `poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Población | 201712–201712 (1) |
| `_general` | `poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Población | 201712–201712 (1) |
| `_general` | `poblacion` | BD Acceso Mun | Información general → Población | 201803–201812 (4) |
| `_general` | `poblacion` | BD Género Mun |  | Información general → Población | 201803–202209 (19) |
| `_general` | `poblacion` | BD Uso Banca Mun |  | Información general → Población | 201803–201812 (4) |
| `_general` | `poblacion` | BD Uso EACP Mun |  | Información general → Población | 201803–201812 (4) |
| `_general` | `poblacion` | BD Infraestructura Mun | Información general → Población | 201903–202209 (15) |
| `_general` | `poblacion` | BD Tenencia Uso Banca Mun |  | Información general → Población | 201903–202209 (15) |
| `_general` | `poblacion` | BD Tenencia Uso EACP Mun |  | Información general → Población | 201903–202209 (15) |
| `_general` | `poblacion` | BD Captación Mun |  | Información general |  → Población | 202212–202512 (13) |
| `_general` | `poblacion` | BD Crédito Mun |  | Información general |  → Población total | 202212–202412 (9) |
| `_general` | `poblacion` | BD Infraestructura Mun |  | Información general |  → Población total | 202212–202512 (13) |
| `_general` | `poblacion` | BD por sexo Banca Mun |  | Información general |  → Población total | 202212–202412 (9) |
| `_general` | `poblacion` | BD por sexo EACP Mun |  | Información general |  → Población total | 202212–202412 (9) |
| `_general` | `poblacion` | BD Crédito Mun |  | Información general |  → Población | 202503–202512 (4) |
| `_general` | `poblacion` | BD por sexo Banca Mun |  | Información general |  → Población | 202503–202512 (4) |
| `_general` | `poblacion` | BD por sexo EACP Mun |  | Información general |  → Población | 202503–202512 (4) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Población adulta | 201603–201603 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Población adulta | 201603–201603 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Población adulta | 201603–201603 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Población adulta | 201606–201606 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Población adulta | 201606–201606 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Población adulta | 201606–201606 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Población adulta | 201609–201609 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Población adulta | 201609–201609 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Población adulta | 201609–201609 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Población adulta | 201612–201612 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Población adulta | 201612–201612 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Población adulta | 201612–201612 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Población adulta | 201703–201703 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Población adulta | 201703–201703 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Población adulta | 201703–201703 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Población adulta | 201706–201706 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Población adulta | 201706–201706 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Población adulta | 201706–201706 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Población adulta | 201709–201709 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Población adulta | 201709–201709 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Población adulta | 201709–201709 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Población adulta | 201712–201712 (1) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Población adulta | 201712–201712 (1) |
| `_general` | `poblacion_adulta` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Población adulta | 201712–201712 (1) |
| `_general` | `poblacion_adulta` | BD Acceso Mun | Información general → Población Adulta | 201803–201812 (4) |
| `_general` | `poblacion_adulta` | BD Género Mun |  | Información general → Población Adulta | 201803–202209 (19) |
| `_general` | `poblacion_adulta` | BD Uso Banca Mun |  | Información general → Población Adulta | 201803–201812 (4) |
| `_general` | `poblacion_adulta` | BD Uso EACP Mun |  | Información general → Población Adulta | 201803–201812 (4) |
| `_general` | `poblacion_adulta` | BD Infraestructura Mun | Información general → Población Adulta | 201903–202209 (15) |
| `_general` | `poblacion_adulta` | BD Tenencia Uso Banca Mun |  | Información general → Población Adulta | 201903–202209 (15) |
| `_general` | `poblacion_adulta` | BD Tenencia Uso EACP Mun |  | Información general → Población Adulta | 201903–202209 (15) |
| `_general` | `poblacion_adulta` | BD Captación Mun |  | Información general |  → Población Adulta | 202212–202512 (13) |
| `_general` | `poblacion_adulta` | BD Crédito Mun |  | Información general |  → Población adulta | 202212–202412 (9) |
| `_general` | `poblacion_adulta` | BD Infraestructura Mun |  | Información general |  → Población adulta | 202212–202512 (13) |
| `_general` | `poblacion_adulta` | BD por sexo Banca Mun |  | Información general |  → Población adulta | 202212–202412 (9) |
| `_general` | `poblacion_adulta` | BD por sexo EACP Mun |  | Información general |  → Población adulta | 202212–202412 (9) |
| `_general` | `poblacion_adulta` | BD Crédito Mun |  | Información general |  → Población Adulta | 202503–202512 (4) |
| `_general` | `poblacion_adulta` | BD por sexo Banca Mun |  | Información general |  → Población Adulta | 202503–202512 (4) |
| `_general` | `poblacion_adulta` | BD por sexo EACP Mun |  | Información general |  → Población Adulta | 202503–202512 (4) |
| `_general` | `poblacion_adulta_hombres` | BD Acceso Mun | Información general → Población Adulta Hombres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_hombres` | BD Género Mun |  | Información general → Población Adulta Hombres | 201803–202209 (19) |
| `_general` | `poblacion_adulta_hombres` | BD Uso Banca Mun |  | Información general → Población Adulta Hombres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_hombres` | BD Uso EACP Mun |  | Información general → Población Adulta Hombres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_hombres` | BD Infraestructura Mun | Información general → Población Adulta Hombres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_hombres` | BD Tenencia Uso Banca Mun |  | Información general → Población Adulta Hombres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_hombres` | BD Tenencia Uso EACP Mun |  | Información general → Población Adulta Hombres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_hombres` | BD Captación Mun |  | Información general |  → Población Adulta Hombres | 202212–202512 (13) |
| `_general` | `poblacion_adulta_hombres` | BD Crédito Mun |  | Información general |  → Población adulta Hombres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_hombres` | BD Infraestructura Mun |  | Información general |  → Población adulta Hombres | 202212–202512 (13) |
| `_general` | `poblacion_adulta_hombres` | BD por sexo Banca Mun |  | Información general |  → Población adulta Hombres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_hombres` | BD por sexo EACP Mun |  | Información general |  → Población adulta Hombres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_hombres` | BD Crédito Mun |  | Información general |  → Población Adulta Hombres | 202503–202512 (4) |
| `_general` | `poblacion_adulta_hombres` | BD por sexo Banca Mun |  | Información general |  → Población Adulta Hombres | 202503–202512 (4) |
| `_general` | `poblacion_adulta_hombres` | BD por sexo EACP Mun |  | Información general |  → Población Adulta Hombres | 202503–202512 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD Acceso Mun | Información general → Población Adulta Mujeres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD Género Mun |  | Información general → Población Adulta Mujeres | 201803–202209 (19) |
| `_general` | `poblacion_adulta_mujeres` | BD Uso Banca Mun |  | Información general → Población Adulta Mujeres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD Uso EACP Mun |  | Información general → Población Adulta Mujeres | 201803–201812 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD Infraestructura Mun | Información general → Población Adulta Mujeres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_mujeres` | BD Tenencia Uso Banca Mun |  | Información general → Población Adulta Mujeres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_mujeres` | BD Tenencia Uso EACP Mun |  | Información general → Población Adulta Mujeres | 201903–202209 (15) |
| `_general` | `poblacion_adulta_mujeres` | BD Captación Mun |  | Información general |  → Población Adulta Mujeres | 202212–202512 (13) |
| `_general` | `poblacion_adulta_mujeres` | BD Crédito Mun |  | Información general |  → Población adulta Mujeres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_mujeres` | BD Infraestructura Mun |  | Información general |  → Población adulta Mujeres | 202212–202512 (13) |
| `_general` | `poblacion_adulta_mujeres` | BD por sexo Banca Mun |  | Información general |  → Población adulta Mujeres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_mujeres` | BD por sexo EACP Mun |  | Información general |  → Población adulta Mujeres | 202212–202412 (9) |
| `_general` | `poblacion_adulta_mujeres` | BD Crédito Mun |  | Información general |  → Población Adulta Mujeres | 202503–202512 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD por sexo Banca Mun |  | Información general |  → Población Adulta Mujeres | 202503–202512 (4) |
| `_general` | `poblacion_adulta_mujeres` | BD por sexo EACP Mun |  | Información general |  → Población Adulta Mujeres | 202503–202512 (4) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Región | 201603–201603 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Región | 201603–201603 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Región | 201603–201603 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Región | 201606–201606 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Región | 201606–201606 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Región | 201606–201606 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Región | 201609–201609 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Región | 201609–201609 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Región | 201609–201609 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Región | 201612–201612 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Región | 201612–201612 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Región | 201612–201612 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Región | 201703–201703 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Región | 201703–201703 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Región | 201703–201703 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Región | 201706–201706 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Región | 201706–201706 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Región | 201706–201706 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Región | 201709–201709 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Región | 201709–201709 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Región | 201709–201709 (1) |
| `_general` | `region` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Región | 201712–201712 (1) |
| `_general` | `region` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Región | 201712–201712 (1) |
| `_general` | `region` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Región | 201712–201712 (1) |
| `_general` | `region` | BD Acceso Mun | Información general → Región | 201803–201812 (4) |
| `_general` | `region` | BD Género Mun |  | Información general → Región | 201803–202209 (19) |
| `_general` | `region` | BD Uso Banca Mun |  | Información general → Región | 201803–201812 (4) |
| `_general` | `region` | BD Uso EACP Mun |  | Información general → Región | 201803–201812 (4) |
| `_general` | `region` | BD Infraestructura Mun | Información general → Región | 201903–202209 (15) |
| `_general` | `region` | BD Tenencia Uso Banca Mun |  | Información general → Región | 201903–202209 (15) |
| `_general` | `region` | BD Tenencia Uso EACP Mun |  | Información general → Región | 201903–202209 (15) |
| `_general` | `region` | BD Captación Mun |  | Información general |  → Región | 202212–202512 (13) |
| `_general` | `region` | BD Crédito Mun |  | Información general |  → Región | 202212–202512 (13) |
| `_general` | `region` | BD Infraestructura Mun |  | Información general |  → Región | 202212–202512 (13) |
| `_general` | `region` | BD por sexo Banca Mun |  | Información general |  → Región | 202212–202512 (13) |
| `_general` | `region` | BD por sexo EACP Mun |  | Información general |  → Región | 202212–202512 (13) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Banca de Desarrollo | 201603–201603 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Sucursales banca de desarrollo | 201606–201606 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Sucursales banca de desarrollo | 201609–201609 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Sucursales banca de desarrollo | 201612–201612 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Sucursales banca de desarrollo | 201703–201703 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Sucursales banca de desarrollo | 201706–201706 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Sucursales banca de desarrollo | 201709–201709 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Sucursales banca de desarrollo | 201712–201712 (1) |
| `banca_desarrollo` | `sucursales` | BD Acceso Mun | Número de puntos de acceso → Sucursales banca de desarrollo | 201803–201812 (4) |
| `banca_desarrollo` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales banca de desarrollo | 201903–202003 (5) |
| `banca_desarrollo` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales Banca de desarrollo | 202006–202209 (10) |
| `banca_desarrollo` | `sucursales` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Infraestructura → Sucursales Número | 202212–202512 (13) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Banca Comercial | 201603–201603 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Sucursales banca comercial | 201606–201606 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Sucursales banca comercial | 201609–201609 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Sucursales banca comercial | 201612–201612 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Sucursales banca comercial | 201703–201703 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Sucursales banca comercial | 201706–201706 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Sucursales banca comercial | 201709–201709 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Sucursales banca comercial | 201712–201712 (1) |
| `banca_multiple` | `sucursales` | BD Acceso Mun | Número de puntos de acceso → Sucursales banca comercial | 201803–201812 (4) |
| `banca_multiple` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales banca comercial | 201903–202003 (5) |
| `banca_multiple` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales Banca comercial | 202006–202209 (10) |
| `banca_multiple` | `sucursales` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Infraestructura → Sucursales Número | 202212–202512 (13) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Cooperativas | 201603–201603 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Sucursales Socap | 201606–201606 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Sucursales Socap | 201609–201609 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Sucursales Socap | 201612–201612 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Sucursales Socap | 201703–201703 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Sucursales Socap | 201706–201706 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Sucursales Socap | 201709–201709 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Sucursales Socap | 201712–201712 (1) |
| `socap` | `sucursales` | BD Acceso Mun | Número de puntos de acceso → Sucursales Socap | 201803–201812 (4) |
| `socap` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales Socap | 201903–202209 (15) |
| `socap` | `sucursales` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Infraestructura → Sucursales Número | 202212–202512 (13) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Microfinancieras | 201603–201603 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Sucursales Sofipo | 201606–201606 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Sucursales Sofipo | 201609–201609 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Sucursales Sofipo | 201612–201612 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Sucursales Sofipo | 201703–201703 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Sucursales Sofipo | 201706–201706 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Sucursales Sofipo | 201709–201709 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Sucursales Sofipo | 201712–201712 (1) |
| `sofipo` | `sucursales` | BD Acceso Mun | Número de puntos de acceso → Sucursales Sofipo | 201803–201812 (4) |
| `sofipo` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Sucursales Sofipo | 201903–202209 (15) |
| `sofipo` | `sucursales` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Infraestructura → Sucursales Número | 202212–202512 (13) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Total Sucursales | 201603–201603 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Total Sucursales | 201606–201606 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Total Sucursales | 201609–201609 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Total Sucursales | 201612–201612 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Total Sucursales | 201703–201703 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Total Sucursales | 201706–201706 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Total Sucursales | 201709–201709 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Total Sucursales | 201712–201712 (1) |
| `todos` | `sucursales` | BD Acceso Mun | Número de puntos de acceso → Total Sucursales | 201803–201812 (4) |
| `todos` | `sucursales` | BD Infraestructura Mun | Número de puntos de acceso → Total Sucursales | 201903–202209 (15) |
| `todos` | `sucursales` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → Sucursales Número | 202212–202512 (13) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Superficie km2 | 201603–201603 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Superficie km2 | 201603–201603 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Superficie km2 | 201603–201603 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Superficie km2 | 201606–201606 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Superficie km2 | 201606–201606 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Superficie km2 | 201606–201606 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Superficie km2 | 201609–201609 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Superficie km2 | 201609–201609 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Superficie km2 | 201609–201609 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Superficie km2 | 201612–201612 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Superficie km2 | 201612–201612 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Superficie km2 | 201612–201612 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Superficie km2 | 201703–201703 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Superficie km2 | 201703–201703 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Superficie km2 | 201703–201703 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Superficie km2 | 201706–201706 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Superficie km2 | 201706–201706 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Superficie km2 | 201706–201706 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Superficie km2 | 201709–201709 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Superficie km2 | 201709–201709 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Superficie km2 | 201709–201709 (1) |
| `_general` | `superficie_km2` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Superficie km2 | 201712–201712 (1) |
| `_general` | `superficie_km2` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Superficie km2 | 201712–201712 (1) |
| `_general` | `superficie_km2` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Superficie km2 | 201712–201712 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de crédito → Tarjetas de Crédito | 201603–201603 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201606–201606 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201609–201609 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201612–201612 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201703–201703 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201706–201706 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201709–201709 (1) |
| `banca` | `tarjetas_credito` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201712–201712 (1) |
| `banca` | `tarjetas_credito` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de crédito → Tarjetas de Crédito | 201803–201812 (4) |
| `banca` | `tarjetas_credito` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Tarjetas de Crédito | 201903–202003 (5) |
| `banca` | `tarjetas_credito` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Crédito → Tarjetas de crédito | 202006–202209 (10) |
| `banca` | `tarjetas_credito` | BD Crédito Mun | Crédito | Todos los sectores | Banca → Tarjetas de crédito Número | 202212–202512 (13) |
| `banca_desarrollo` | `tarjetas_credito` | BD Crédito Mun | Crédito | Banca de desarrollo | Crédito → Tarjetas de crédito Número | 202212–202512 (13) |
| `banca_multiple` | `tarjetas_credito` | BD Crédito Mun | Crédito | Banca múltiple | Crédito → Tarjetas de crédito Número | 202212–202512 (13) |
| `eacp` | `tarjetas_credito` | BD Crédito Mun | Crédito | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Tarjetas de crédito Número | 202212–202512 (13) |
| `socap` | `tarjetas_credito` | BD Crédito Mun | Crédito | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Tarjetas de crédito Número | 202212–202512 (13) |
| `sofipo` | `tarjetas_credito` | BD Crédito Mun | Crédito | Sociedades Financieras Populares | Crédito → Tarjetas de crédito Número | 202212–202512 (13) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Contratos de captación → Tarjetas de Débito | 201603–201603 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201606–201606 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201609–201609 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201612–201612 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201703–201703 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201706–201706 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201709–201709 (1) |
| `banca` | `tarjetas_debito` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201712–201712 (1) |
| `banca` | `tarjetas_debito` | BD Uso Banca Mun | Número de contratos - Banca | Contratos de captación → Tarjetas de débito | 201803–201812 (4) |
| `banca` | `tarjetas_debito` | BD Tenencia Uso Banca Mun | Tenencia
Número de contratos - Banca | Captación → Tarjetas de débito | 201903–202209 (15) |
| `banca` | `tarjetas_debito` | BD Captación Mun | Captación | Todos los sectores | Banca → Tarjetas de débito Número | 202212–202512 (13) |
| `banca_desarrollo` | `tarjetas_debito` | BD Captación Mun | Captación | Banca de desarrollo | Captación → Tarjetas de débito Número | 202212–202512 (13) |
| `banca_multiple` | `tarjetas_debito` | BD Captación Mun | Captación | Banca múltiple | Captación → Tarjetas de débito Número | 202212–202512 (13) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Número de contratos - EACP | Captación → Tarjeta débito | 201603–201603 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Número de contratos - EACP | Captación → Tarjeta débito | 201606–201606 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Número de contratos - EACP | Captación → Tarjeta débito | 201609–201609 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Número de contratos - EACP | Captación → Tarjeta débito | 201612–201612 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Número de contratos - EACP | Captación → Tarjeta débito | 201703–201703 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Número de contratos - EACP | Captación → Tarjeta débito | 201706–201706 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Número de contratos - EACP | Captación → Tarjeta débito | 201709–201709 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Número de contratos - EACP | Captación → Tarjeta débito | 201712–201712 (1) |
| `eacp` | `tarjetas_debito` | BD Uso EACP Mun | Número de contratos - EACP | Captación → Tarjeta débito | 201803–201812 (4) |
| `eacp` | `tarjetas_debito` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Tarjeta débito | 201903–202003 (5) |
| `eacp` | `tarjetas_debito` | BD Tenencia Uso EACP Mun | Tenencia
Número de contratos - EACP | Captación → Tarjetas de débito | 202006–202209 (10) |
| `eacp` | `tarjetas_debito` | BD Captación Mun | Captación | Todos los sectores | Entidades de Ahorro y Crédito Popular (EACP) → Tarjetas de débito Número | 202212–202512 (13) |
| `socap` | `tarjetas_debito` | BD Captación Mun | Captación | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Tarjetas de débito Número | 202212–202512 (13) |
| `sofipo` | `tarjetas_debito` | BD Captación Mun | Captación | Sociedades Financieras Populares | Captación → Tarjetas de débito Número | 202212–202512 (13) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 |  → Tipo de población | 201603–201603 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 |  |  → Tipo de población | 201603–201603 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 |  |  → Tipo de población | 201603–201603 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 |  → Tipo de población | 201606–201606 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 |  |  → Tipo de población | 201606–201606 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 |  |  → Tipo de población | 201606–201606 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 |  → Tipo de población | 201609–201609 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 |  |  → Tipo de población | 201609–201609 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Tipo de población | 201609–201609 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 |  → Tipo de población | 201612–201612 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 |  |  → Tipo de población | 201612–201612 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 |  |  → Tipo de población | 201612–201612 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 |  → Tipo de población | 201703–201703 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 |  |  → Tipo de población | 201703–201703 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 |  |  → Tipo de población | 201703–201703 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 |  → Tipo de población | 201706–201706 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 |  |  → Tipo de población | 201706–201706 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 |  |  → Tipo de población | 201706–201706 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 |  → Tipo de población | 201709–201709 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 |  |  → Tipo de población | 201709–201709 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 |  |  → Tipo de población | 201709–201709 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 |  → Tipo de población | 201712–201712 (1) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 |  |  → Tipo de población | 201712–201712 (1) |
| `_general` | `tipo_poblacion` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 |  |  → Tipo de población | 201712–201712 (1) |
| `_general` | `tipo_poblacion` | BD Acceso Mun | Información general → Tipo de población | 201803–201812 (4) |
| `_general` | `tipo_poblacion` | BD Género Mun |  | Información general → Tipo de población | 201803–202209 (19) |
| `_general` | `tipo_poblacion` | BD Uso Banca Mun |  | Información general → Tipo de población | 201803–201812 (4) |
| `_general` | `tipo_poblacion` | BD Uso EACP Mun |  | Información general → Tipo de población | 201803–201812 (4) |
| `_general` | `tipo_poblacion` | BD Infraestructura Mun | Información general → Tipo de población | 201903–202209 (15) |
| `_general` | `tipo_poblacion` | BD Tenencia Uso Banca Mun |  | Información general → Tipo de población | 201903–202209 (15) |
| `_general` | `tipo_poblacion` | BD Tenencia Uso EACP Mun |  | Información general → Tipo de población | 201903–202209 (15) |
| `_general` | `tipo_poblacion` | BD Captación Mun |  | Información general |  → Tipo de población | 202212–202512 (13) |
| `_general` | `tipo_poblacion` | BD Crédito Mun |  | Información general |  → Tipo de población | 202212–202512 (13) |
| `_general` | `tipo_poblacion` | BD Infraestructura Mun |  | Información general |  → Tipo de población | 202212–202512 (13) |
| `_general` | `tipo_poblacion` | BD por sexo Banca Mun |  | Información general |  → Tipo de población | 202212–202512 (13) |
| `_general` | `tipo_poblacion` | BD por sexo EACP Mun |  | Información general |  → Tipo de población | 202212–202512 (13) |
| `banca_desarrollo` | `tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Infraestructura → TPV Número | 202212–202512 (13) |
| `banca_multiple` | `tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Infraestructura → TPV Número | 202212–202512 (13) |
| `socap` | `tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Infraestructura → TPV Número | 202212–202512 (13) |
| `sofipo` | `tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Infraestructura → TPV Número | 202212–202512 (13) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Número de puntos de acceso → Terminales Punto de Venta | 201603–201603 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Número de puntos de acceso → Terminales punto de venta | 201606–201606 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Número de puntos de acceso → Terminales punto de venta | 201609–201609 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Número de puntos de acceso → Terminales punto de venta | 201612–201612 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Número de puntos de acceso → Terminales punto de venta | 201703–201703 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Número de puntos de acceso → Terminales punto de venta | 201706–201706 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Número de puntos de acceso → Terminales punto de venta | 201709–201709 (1) |
| `todos` | `tpv` | BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Número de puntos de acceso → Terminales punto de venta | 201712–201712 (1) |
| `todos` | `tpv` | BD Acceso Mun | Número de puntos de acceso → Terminales punto de venta | 201803–201812 (4) |
| `todos` | `tpv` | BD Infraestructura Mun | Número de puntos de acceso → Terminales punto de venta | 201903–202209 (15) |
| `todos` | `tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Infraestructura → TPV Número | 202212–202512 (13) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Transacciones → En cajeros automáticos | 201603–201603 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201606–201606 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201609–201609 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201612–201612 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201703–201703 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201706–201706 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201709–201709 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201712–201712 (1) |
| `banca` | `transacciones_cajeros` | BD Uso Banca Mun | Número de contratos - Banca | Transacciones → En cajeros automáticos | 201803–201812 (4) |
| `banca` | `transacciones_cajeros` | BD Tenencia Uso Banca Mun | Uso
Transacciones - Banca | Transacciones → En cajeros automáticos | 201903–202209 (15) |
| `banca_desarrollo` | `transacciones_cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Transacciones → Transacciones en cajeros automáticos Número | 202212–202512 (13) |
| `banca_multiple` | `transacciones_cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Transacciones → Transacciones en cajeros automáticos Número | 202212–202512 (13) |
| `eacp` | `transacciones_cajeros` | BD Tenencia Uso EACP Mun | Uso
Transacciones - EACP | Transacciones → En cajeros automáticos | 201903–202209 (15) |
| `socap` | `transacciones_cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Transacciones → Transacciones en cajeros automáticos Número | 202212–202512 (13) |
| `sofipo` | `transacciones_cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Transacciones → Transacciones en cajeros automáticos Número | 202212–202512 (13) |
| `todos` | `transacciones_cajeros` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Transacciones → Transacciones en cajeros automáticos Número | 202212–202512 (13) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Banca (Comercial y de Desarrollo) | Transacciones → En TPV´s | 201603–201603 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Número de contratos - Banca | Transacciones → En TPV | 201606–201606 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Número de contratos - Banca | Transacciones → En TPV | 201609–201609 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Número de contratos - Banca | Transacciones → En TPV | 201612–201612 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Número de contratos - Banca | Transacciones → En TPV | 201703–201703 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Número de contratos - Banca | Transacciones → En TPV | 201706–201706 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Número de contratos - Banca | Transacciones → En TPV | 201709–201709 (1) |
| `banca` | `transacciones_tpv` | BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Número de contratos - Banca | Transacciones → En TPV | 201712–201712 (1) |
| `banca` | `transacciones_tpv` | BD Uso Banca Mun | Número de contratos - Banca | Transacciones → En TPV | 201803–201812 (4) |
| `banca` | `transacciones_tpv` | BD Tenencia Uso Banca Mun | Uso
Transacciones - Banca | Transacciones → En TPV | 201903–202209 (15) |
| `banca_desarrollo` | `transacciones_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca de desarrollo | Transacciones → Transacciones en TPV Número | 202212–202512 (13) |
| `banca_multiple` | `transacciones_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Banca múltiple | Transacciones → Transacciones en TPV Número | 202212–202512 (13) |
| `eacp` | `transacciones_tpv` | BD Tenencia Uso EACP Mun | Uso
Transacciones - EACP | Transacciones → En TPV | 201903–202209 (15) |
| `socap` | `transacciones_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Cooperativas de Ahorro y Préstamo | Transacciones → Transacciones en TPV Número | 202212–202512 (13) |
| `sofipo` | `transacciones_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Sociedades Financieras Populares | Transacciones → Transacciones en TPV Número | 202212–202512 (13) |
| `todos` | `transacciones_tpv` | BD Infraestructura Mun | Infraestructura y transacciones | Todos los sectores | Transacciones → Transacciones en TPV Número | 202212–202512 (13) |
| `socap` | `usuarios_hombres` | BD Uso EACP Mun | Número de usuarios - EACP | Socios - Socap → Hombres | 201809–201812 (2) |
| `socap` | `usuarios_hombres` | BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Socios - Socap → Hombres | 201903–202209 (15) |
| `sofipo` | `usuarios_hombres` | BD Uso EACP Mun | Número de usuarios - EACP | Clientes - Sofipo → Hombres | 201809–201812 (2) |
| `sofipo` | `usuarios_hombres` | BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Clientes - Sofipo → Hombres | 201903–202209 (15) |
| `socap` | `usuarios_mujeres` | BD Uso EACP Mun | Número de usuarios - EACP | Socios - Socap → Mujeres | 201809–201812 (2) |
| `socap` | `usuarios_mujeres` | BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Socios - Socap → Mujeres | 201903–202209 (15) |
| `sofipo` | `usuarios_mujeres` | BD Uso EACP Mun | Número de usuarios - EACP | Clientes - Sofipo → Mujeres | 201809–201812 (2) |
| `sofipo` | `usuarios_mujeres` | BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Clientes - Sofipo → Mujeres | 201903–202209 (15) |

## Columnas descartadas (no son conteos absolutos)

| hoja | niveles → encabezado | trimestres |
|---|---|---|
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201612–201612 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Módulos de atención Compartamos | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Diciembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201712–201712 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201606–201606 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Módulos de atención Compartamos | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Junio de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201706–201706 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Banca Comercial | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Banca de Desarrollo | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que afectan por celular | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cooperativas | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Microfinancieras | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales Punto de Venta | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201603–201603 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Marzo de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201703–201703 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2016 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201609–201609 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Módulos de atención Compartamos | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201709–201709 (1) |
| BD Acceso Mun | Base de Datos Acceso
Septiembre de 2017 | Indicadores Demográficos 
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201709–201709 (1) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Módulos de atención Compartamos | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201803–201812 (4) |
| BD Acceso Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201803–201812 (4) |
| BD Género Mun | Número de contratos - Banca | Ahorro → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Ahorro → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Ahorro → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Ahorro → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N1 → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N1 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N1 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N1 → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N2 → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N2 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N2 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N2 → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N3 → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N3 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N3 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | N3 → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Plazo → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Plazo → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Plazo → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Plazo → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Total → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Total → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Total → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Total → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Transaccionales tradicionales → Hombres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Transaccionales tradicionales → Mujeres | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Transaccionales tradicionales → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Número de contratos - Banca | Transaccionales tradicionales → Total | 201803–201806 (2) |
| BD Género Mun | Número de contratos de captación
Banca | Ahorro → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Ahorro → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Ahorro → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | Ahorro → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | Ahorro → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N1 → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N1 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N1 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | N1 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | N1 → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N2 → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N2 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N2 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | N2 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | N2 → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N3 → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N3 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | N3 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | N3 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | N3 → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Plazo → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Plazo → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Plazo → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | Plazo → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | Plazo → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Total → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Total → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Total → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | Total → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | Total → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Transaccionales tradicionales → Hombres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Transaccionales tradicionales → Mujeres | 201809–202209 (17) |
| BD Género Mun | Número de contratos de captación
Banca | Transaccionales tradicionales → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Número de contratos de captación
Banca | Transaccionales tradicionales → Personas morales | 202006–202209 (10) |
| BD Género Mun | Número de contratos de captación
Banca | Transaccionales tradicionales → Total | 201809–202209 (17) |
| BD Género Mun | Número de contratos de crédito
Banca Múltiple | Hipotecarios → Hombres | 201809–201812 (2) |
| BD Género Mun | Número de contratos de crédito
Banca Múltiple | Hipotecarios → Mujeres | 201809–201812 (2) |
| BD Género Mun | Número de contratos de crédito
Banca Múltiple | Hipotecarios → Total | 201809–201812 (2) |
| BD Género Mun | Número de contratos de crédito
Banca múltiple | Hipotecarios → Hombres | 201903–202209 (15) |
| BD Género Mun | Número de contratos de crédito
Banca múltiple | Hipotecarios → Mujeres | 201903–202209 (15) |
| BD Género Mun | Número de contratos de crédito
Banca múltiple | Hipotecarios → Total | 201903–202209 (15) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de crédito → Hombres | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de crédito → Mujeres | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de crédito → Personas Morales | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de crédito → Total | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de débito → Hombres | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de débito → Mujeres | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de débito → Personas Morales | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca Múltiple | Tarjeta de débito → Total | 201809–201812 (2) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de crédito → Hombres | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de crédito → Mujeres | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de crédito → Personas Morales | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de crédito → Total | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de débito → Hombres | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de débito → Mujeres | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de débito → Personas Morales | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjeta de débito → Total | 201903–202003 (5) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de crédito → Hombres | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de crédito → Mujeres | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de crédito → Personas Morales | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de crédito → Total | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de débito → Hombres | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de débito → Mujeres | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de débito → Personas Morales | 202006–202209 (10) |
| BD Género Mun | Número de tarjetas
Banca múltiple | Tarjetas de débito → Total | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos - Banca | Ahorro → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Ahorro → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Ahorro → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Ahorro → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N1 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N1 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N1 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N1 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N2 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N2 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N2 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N2 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N3 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N3 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N3 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | N3 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Plazo → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Plazo → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Plazo → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Plazo → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Total → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Total → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Total → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Total → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Transaccionales tradicionales → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Transaccionales tradicionales → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Transaccionales tradicionales → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos - Banca | Transaccionales tradicionales → Total | 201803–201806 (2) |
| BD Género Mun | Saldo de contratos de captación
Banca | Ahorro → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Ahorro → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Ahorro → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | Ahorro → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | Ahorro → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N1 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N1 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N1 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | N1 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | N1 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N2 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N2 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N2 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | N2 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | N2 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N3 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N3 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | N3 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | N3 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | N3 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Plazo → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Plazo → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Plazo → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | Plazo → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | Plazo → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Total → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Total → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Total → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | Total → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | Total → Total | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Transaccionales tradicionales → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Transaccionales tradicionales → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo de contratos de captación
Banca | Transaccionales tradicionales → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo de contratos de captación
Banca | Transaccionales tradicionales → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo de contratos de captación
Banca | Transaccionales tradicionales → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio - Banca | Ahorro → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Ahorro → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Ahorro → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Ahorro → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N1 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N1 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N1 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N1 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N2 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N2 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N2 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N2 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N3 → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N3 → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N3 → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | N3 → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Plazo → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Plazo → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Plazo → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Plazo → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Total → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Total → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Total → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Total → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Transaccionales tradicionales → Hombres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Transaccionales tradicionales → Mujeres | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Transaccionales tradicionales → Personas Morales | 201803–201806 (2) |
| BD Género Mun | Saldo promedio - Banca | Transaccionales tradicionales → Total | 201803–201806 (2) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Ahorro → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Ahorro → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Ahorro → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Ahorro → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Ahorro → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N1 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N1 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N1 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N1 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N1 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N2 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N2 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N2 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N2 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N2 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N3 → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N3 → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N3 → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N3 → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | N3 → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Plazo → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Plazo → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Plazo → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Plazo → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Plazo → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Total → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Total → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Total → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Total → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Total → Total | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Transaccionales tradicionales → Hombres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Transaccionales tradicionales → Mujeres | 201809–202209 (17) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Transaccionales tradicionales → Personas Morales | 201809–202003 (7) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Transaccionales tradicionales → Personas morales | 202006–202209 (10) |
| BD Género Mun | Saldo promedio de contratos de captación
Banca | Transaccionales tradicionales → Total | 201809–202209 (17) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Cajeros | 201903–202003 (5) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Cajeros automáticos | 202006–202209 (10) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Contratos que utilizan banca móvil | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Corresponsales | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Establecimientos con TPV | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Banca comercial | 202006–202209 (10) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Banca de desarrollo | 202006–202209 (10) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Socap | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales Sofipo | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca comercial | 201903–202003 (5) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Sucursales banca de desarrollo | 201903–202003 (5) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Terminales punto de venta | 201903–202209 (15) |
| BD Infraestructura Mun | Indicadores demográficos
(Puntos de acceso por cada 10,000 adultos) → Total Sucursales | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores
(Transacciones por cada 10,000 adultos) | Transacciones → En TPV | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores
(Transacciones por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Cuentas de ahorro | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Cuentas transaccionales nivel 1 | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Cuentas transaccionales nivel 2 | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Cuentas transaccionales nivel 3 | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Cuentas transaccionales tradicionales | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósitos a plazo | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjetas de débito | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → ABCD | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Automotriz | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Grupal | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Hipotecario  | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Nómina | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Personal | 201903–202209 (15) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Tarjetas de Crédito | 201903–202003 (5) |
| BD Tenencia Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Tarjetas de crédito | 202006–202209 (10) |
| BD Tenencia Uso EACP Mun | Indicadores
(Transacciones por cada 10,000 adultos) | Transacciones → En TPV | 201903–202209 (15) |
| BD Tenencia Uso EACP Mun | Indicadores
(Transacciones por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201903–202209 (15) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201903–202003 (5) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201903–202003 (5) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201903–202003 (5) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósitos a la vista | 202006–202209 (10) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósitos a plazo | 202006–202209 (10) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósitos al ahorro | 202006–202209 (10) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201903–202003 (5) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjetas de débito | 202006–202209 (10) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201903–202209 (15) |
| BD Tenencia Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201903–202209 (15) |
| BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Total de usuarios - EACP → Hombres | 201903–202209 (15) |
| BD Tenencia Uso EACP Mun | Número de usuarios - EACP | Total de usuarios - EACP → Mujeres | 201903–202209 (15) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201803–201812 (4) |
| BD Uso Banca Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201803–201812 (4) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201612–201612 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201712–201712 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201606–201606 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201706–201706 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201603–201603 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201703–201703 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201609–201609 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201709–201709 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201709–201709 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201709–201709 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201709–201709 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201709–201709 (1) |
| BD Uso EACP Mun | Base de Datos Uso - EACP
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201709–201709 (1) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a la vista | 201803–201812 (4) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito a plazo | 201803–201812 (4) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Depósito al ahorro | 201803–201812 (4) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Captación → Tarjeta débito | 201803–201812 (4) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito a la vivienda | 201803–201812 (4) |
| BD Uso EACP Mun | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Crédito → Crédito al consumo | 201803–201812 (4) |
| BD Uso EACP Mun | Número de usuarios - EACP | Total de usuarios - EACP → Hombres | 201809–201812 (2) |
| BD Uso EACP Mun | Número de usuarios - EACP | Total de usuarios - EACP → Mujeres | 201809–201812 (2) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201612–201612 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Diciembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201712–201712 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201606–201606 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Junio de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201706–201706 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales Nivel 1 | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales Nivel 2 | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales Nivel 3 | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de Débito | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV´s | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201603–201603 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Marzo de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201703–201703 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 |  |  → Números de municipios | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2016 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201609–201609 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas de ahorro | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 1 | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 2 | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales nivel 3 | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Cuentas transaccionales tradicionales | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Depósitos a plazo | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de captación → Tarjetas de débito | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → ABCD | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Automotriz | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Grupal | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Hipotecario  | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Nómina | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Personal | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Contratos de crédito → Tarjetas de Crédito | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En TPV | 201709–201709 (1) |
| BD Uso Mun | Base de Datos Uso - Banca
Septiembre de 2017 | Indicadores Demográficos 
(Contratos por cada 10,000 adultos) | Transacciones → En cajeros automáticos | 201709–201709 (1) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Tarjetas de débito Número de tarjetas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Tarjetas de débito Número de tarjetas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Total Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Total Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 1 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 1 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 2 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 2 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 3 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 3 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 4 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca de desarrollo | Captación → Transaccionales Nivel 4 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Tarjetas de débito Número de tarjetas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Tarjetas de débito Número de tarjetas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Total Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Total Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 1 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 1 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 2 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 2 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 3 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 3 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 4 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca múltiple | Captación → Transaccionales Nivel 4 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Tarjetas de débito Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Tarjetas de débito Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Total captación Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Total captación Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 1 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 1 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 2 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 2 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 3 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 3 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 4 Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Captación por sexo | Banca | Captación → Transaccionales Nivel 4 Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → ABCD Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → ABCD Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Automotriz Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Automotriz Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Grupal Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Grupal Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Hipotecario Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Hipotecario Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Nómina Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Nómina Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Personal Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Personal Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Tarjetas de crédito Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Tarjetas de crédito Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Total Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca de desarrollo | Crédito → Total Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → ABCD Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → ABCD Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Automotriz Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Automotriz Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Grupal Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Grupal Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Hipotecario Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Hipotecario Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Nómina Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Nómina Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Personal Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Personal Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Tarjetas de crédito Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Tarjetas de crédito Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Total Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca múltiple | Crédito → Total Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → ABCD Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → ABCD Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Automotriz Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Automotriz Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Grupal Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Grupal Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Hipotecario Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Hipotecario Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Nómina Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Nómina Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Personal Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Personal Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Tarjetas de crédito Número Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Tarjetas de crédito Número Mujeres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Total Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo Banca Mun | Crédito por sexo | Banca | Crédito → Total Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Depósitos a la vista Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Depósitos a la vista Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Total captación Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Captación → Total captación Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a la vista Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a la vista Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Total Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Captación → Total Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Ahorro Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Ahorro Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Depósitos a la vista Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Depósitos a la vista Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Depósitos a plazo Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Depósitos a plazo Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Total Número de cuentas Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Captación por sexo | Sociedades Financieras Populares | Captación → Total Número de cuentas Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Comercial Número Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Comercial Número Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Consumo Número Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Consumo Número Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Vivienda Número Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Entidades de Ahorro y Crédito Popular (EACP) | Crédito → Vivienda Número Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Comercial Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Comercial Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Consumo Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Consumo Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Vivienda Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Cooperativas de Ahorro y Préstamo | Crédito → Vivienda Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Comercial Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Comercial Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Consumo Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Consumo Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Vivienda Número de créditos Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Crédito por sexo | Sociedades Financieras Populares | Crédito → Vivienda Número de créditos Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Personas socias y clientes | Socap | Personas socias → Socias Número Mujeres | 202212–202512 (13) |
| BD por sexo EACP Mun | Personas socias y clientes | Socap | Personas socias → Socios Número Hombres | 202212–202512 (13) |
| BD por sexo EACP Mun | Personas socias y clientes | Sofipo | Clientes → Clientes Número Hombres | 202309–202512 (10) |
| BD por sexo EACP Mun | Personas socias y clientes | Sofipo | Clientes → Clientes Número Mujeres | 202309–202512 (10) |
| BD por sexo EACP Mun | Personas socias y clientes | Sofipo | Clientes
Número
Mujeres → Clientes Número Hombres | 202212–202306 (3) |
| BD por sexo EACP Mun | Personas socias y clientes | Sofipo | Clientes
Número
Mujeres → Clientes Número Mujeres | 202212–202306 (3) |

# Diccionario: población BDIF (`data/interim/cnbv_bdif_poblacion.parquet`)

Una fila por municipio-trimestre. La CNBV publica población y población adulta por municipio en cada base (fuente declarada en la 'Ficha técnica' de cada Excel: proyecciones CONAPO hasta 2022T3, valores con decimales; Censo 2020 desde 2022T4, enteros). Adulto = 18 años o más según la ficha técnica de la CNBV (confirmar en `docs/data_audit.md`).

| variable | descripción | tipo | unidad | fuente |
|---|---|---|---|---|
| `cve_mun` | Clave municipal | str | — | CNBV |
| `periodo` | Trimestre | str | — | CNBV |
| `t` | Índice | int64 | — | CNBV |
| `poblacion` | Población total | float64 | personas | CNBV |
| `poblacion_adulta` | Población adulta (18+) | float64 | personas | CNBV |
| `poblacion_adulta_mujeres` | Población adulta mujeres (desde 2018T1) | float64 | personas | CNBV |
| `poblacion_adulta_hombres` | Población adulta hombres (desde 2018T1) | float64 | personas | CNBV |
| `tipo_poblacion` | Clasificación CNBV: Rural, En transición, Semi-urbano, Urbano, Semi-metrópoli, Metrópoli | str | categoría | CNBV |
| `region` | Región CNBV | str | categoría | CNBV |
| `nom_ent` | Entidad | str | — | CNBV |
| `nom_mun` | Municipio | str | — | CNBV |
| `indice_rezago_social` | Grado de rezago social CONEVAL (desde 2023T1) | str | categoría | CNBV |

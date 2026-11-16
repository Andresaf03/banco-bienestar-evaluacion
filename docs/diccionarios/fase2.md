# Diccionario: datos de la fase 2 (2026-10-07)

Preregistro y lectura en `docs/decisiones.md`; fuentes y URLs en `config/fuentes.yaml`; parámetros
en `config/parametros.yaml` (`fase2`). Se reconstruye todo con:

```
make descargar-fase2   # EIC/Censo y ENOE por streaming; VIIRS y EFIPEM se conservan en data/raw
make bateria-fase2     # limpieza, paneles y analisis/10_fase2.R
```

## Insumos intermedios (`data/interim/`)

| Archivo | Unidad | Columnas principales | Módulo |
|---|---|---|---|
| `cnbv_portafolio_modelo.parquet` | municipio × institución × mes (2022-01–2026-07) | `yyyymm`, `periodo` (solo meses de cierre), `cve_mun`, `institucion` (037166 Banco del Bienestar, 037019 Banjército…), `nombre_entidad`, `tipo` (31 = sucursales), `descripcion_tipo`, `valor` | `limpieza/cnbv_portafolio_modelo.py` |
| `sucursales_bienestar_obs.parquet` | municipio × trimestre 2016T1–2025T4 | la serie de siempre más `suc_bienestar_modelo`, `suc_banjercito_modelo`, `suc_bd_modelo` (2022T1+) y `suc_bienestar_obs` (modelo desde 2022T1) | ídem |
| `inegi_eic/partes/<anio>_<clave>.parquet` | municipio (clave del corte) | sumas ponderadas con `FACTOR`: `pob`, `pob12`, `ocupados`, `pos_validos`, `cuenta_propia`, `empleadores`, `ing_validos`, `ing_log_suma`, `lugar_validos`, `otro_mun`, `viv_*`, `n_personas`, `n_viviendas` | `descarga/inegi_eic.py` |
| `inegi_eic_municipio.parquet` | municipio estable × {2015, 2020, 2025} | indicadores `pct_*`, `log_ingreso_trabajo`, `log_poblacion_est`, `poblacion_est`, `n_personas`, `n_viviendas` | `limpieza/inegi_eic.py` |
| `viirs_localidad.parquet` | localidad (marco de `panel_localidad`) × año 2016–2024 | `luz_1km`, `npix_1km`, `luz_anillo`, `npix_anillo` (nW/cm²/sr, enteros), `factor_radiancia`, `producto` | `limpieza/viirs.py` |
| `efipem_municipio.parquet` | municipio estable × año 2016–2024 | `impuestos`, `predial`, `derechos`, `ingresos_total` (pesos corrientes; NaN = no desglosado) | `limpieza/efipem.py` |
| `enoe/partes/<periodo>.parquet` | municipio × trimestre | sumas ponderadas: `pob15`, `ocupados`, `pos_validos`, `negocio`, `informal`, `ing_validos`, `ing_log_suma`, `n_registros` | `descarga/enoe.py` |
| `enoe_municipio.parquet` | municipio estable × trimestre | `pct_negocio`, `pct_informal`, `pct_ocupacion`, `log_ingreso`, `n_registros` | `limpieza/enoe.py` |

## Paneles (`data/processed/`, `construccion/panel_fase2.py`)

Misma estructura que los de la corrida final (`id, t, G, tratado, ya_tratado_inicio,
sospechoso_banjercito, covariables, resultados`).

| Panel | t | G | Notas |
|---|---|---|---|
| `panel_municipio_trim_obs` | 1 = 2019T1 … 28 = 2025T4 | primer trimestre con sucursal del Banco del Bienestar **observado** desde 2022 | `G_base` y `G_trimestre_base` = los de la corrida final; nadie es sospechoso |
| `panel_municipio_eic` | 1 = 2015, 2 = 2020, 3 = 2025 | 3 si abrió entre 2020T2 y 2025T3; 0 si nunca | `apertura_posterior_ce` = fuera por exposición (abrió en 2019T2–2020T1 o en 2025T4); `exposicion_ce` = control/temprana/tardía |
| `panel_localidad_viirs` | 1 = 2016 … 9 = 2024 | año de apertura (semestre 1) o el siguiente (semestre 2) | marco, exposición espacial y covariables de `panel_localidad`; `G_vecina` anual; resultados `log1p_luz_1km`, `luz_1km_pos`, `log1p_luz_anillo` |
| `panel_municipio_efipem` | 1 = 2016 … 9 = 2024 | año de apertura (T1–T2) o el siguiente (T3–T4) | `log_impuestos_pc`, `log_predial_pc`, `log_derechos_pc` (pesos por habitante del Censo 2020) |
| `panel_municipio_enoe` | trimestres desde 2019T1 (2020T2 es hueco común) | primer trimestre observado con sucursal | solo municipios presentes en los 27 trimestres |

## Rupturas y advertencias

- **VIIRS.**
  - 2016–2021 vienen en décimas de nW con el entero ×10; 2022–2024 en enteros con `scale = 10`.
    Se lleva todo a nW enteros.
  - 2022 es el VNL v2.2 de dos satélites; 2023–2024, el VNL v2 de SNPP.
  - Los píxeles negativos (solo en 2016–2021) se excluyen.
  - El diagnóstico está en `outputs/tablas/fase2_desc_viirs_ruptura.csv`.
- **EIC 2015.** Cambian los códigos de `CONACT` (ocupado = 10–16), `CELULAR` (sí = 3) e `INTERNET`
  (sí = 5); la posición en el trabajo se llama `SITUACION_TRAB`.
- **EFIPEM.** Reporte voluntario: entre 1,835 y 2,147 municipios con impuestos por año. El panel se
  balancea en R, que quita a los municipios con años faltantes.
- **ENOE.**
  - Ponderador `fac` hasta 2020T1 y `fac_tri` después.
  - ENOE^N desde 2020T3.
  - El INEGI responde 200 con una página de error a los nombres de archivo inexistentes: se valida
    que cada descarga sea un zip.

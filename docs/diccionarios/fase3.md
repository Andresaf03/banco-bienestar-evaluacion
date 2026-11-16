# Diccionario: datos de la fase 3 (2026-10-11)

Preregistro, adenda y lectura en `docs/decisiones.md`; fuentes y URLs en `config/fuentes.yaml`;
parámetros en `config/parametros.yaml` (`fase3`). Se reconstruye todo con:

```
make descargar-fase3   # INE SICEE automático; SESNSP manual (solo verifica data/manual/sesnsp/)
make bateria-fase3     # limpieza, paneles, analisis/11_fase3.R y entregables
```

## Crudos

| Archivo | Fuente | Contenido |
|---|---|---|
| `data/raw/ine_sicee/DIPUTACIONES_FED_MR_<año>.zip` (2015, 2018, 2021, 2024) | INE, SICEE | Cómputos distritales por casilla (`*_NAL_CAS.csv`) y agregados por sección, municipio, distrito y entidad. UTF-8; 2024 trae 1,505 líneas en latin-1 |
| `data/manual/sesnsp/Municipal-Delitos-2015-2025_ago2026.zip` | SESNSP (SharePoint, manual) | `Municipal-Delitos-2015-2025_ago2026.csv` (latin-1): `Año, Clave_Ent, Entidad, Cve. Municipio, Municipio, Bien jurídico afectado, Tipo de delito, Subtipo de delito, Modalidad, Enero…Diciembre`; además xlsx por año y un PDF de advertencias |

## Insumos intermedios (`data/interim/`)

| Archivo | Unidad | Columnas | Módulo |
|---|---|---|---|
| `ine_diputados_municipio.parquet` | municipio estable × elección | `votos_bloque` (Morena + PT + PVEM), `votos_morena`, `votos_validos`, `votos_nulos`, `votos_no_registrados`, `total_votos`, `lista_nominal`, `casillas` | `limpieza/ine_elecciones.py` |
| `cruce_municipios_ine.parquet` | clave INE + nombre (`07-120\|mezcalapa`) | `cve_mun`, `nom_mun`, `metodo` (exacto, contenido, difuso, manual), `puntaje`, `elecciones` | ídem (resumen en `cruce_municipios_ine.md`) |
| `sesnsp_municipio_trim.parquet` | municipio estable × trimestre 2015T1–2025T4 | `delitos_robo_transeunte`, `delitos_robo_negocio`, `delitos_extorsion`, `delitos_robo_total`, `delitos_homicidio_doloso`, `delitos_dano_propiedad` (carpetas; NaN = el municipio no aparece ese año) | `limpieza/sesnsp.py` |

## Paneles (`data/processed/`, `construccion/panel_fase3.py`)

| Panel | t | G | Notas |
|---|---|---|---|
| `panel_municipio_delitos` | 1 = 2019T1 … 28 = 2025T4 | el de `panel_municipio_trim` | `tasa_*` por 100 mil habitantes del Censo 2020 (`pobtot` = `poblacion_2020`); `con_registro_2019` |
| `panel_municipio_delitos_largo` | 1 = 2016T1 … 40 = 2025T4 | el de `panel_municipio_trim_largo` | se estima desde t = 5 (2017T1) |
| `panel_municipio_delitos_obs` | igual que el principal | G observado (P-8) | robustez |
| `panel_municipio_elecciones` | 1 = 2015, 2 = 2018, 3 = 2021, 4 = 2024 | 4 si la primera sucursal abrió en 2021T3–2024T1; 0 si no abrió antes de la elección de 2024 | sin los 103 municipios con geografía electoral inestable; `apertura_posterior_ce` (abrió en 2019T2–2021T2 o 2024T2); `exposicion_ce` (temprana hasta 2022T4); `pct_*_neto` y `pct_*_2015` |
| `panel_municipio_elecciones_todos` | igual | igual | con los municipios de geografía inestable |
| `panel_municipio_elecciones_obs` | igual | con el Banco del Bienestar observado | robustez |

## Resultados

| Variable | Definición |
|---|---|
| `tasa_robo_transeunte` | robo a transeúnte en vía pública + en espacio abierto al público, por 100 mil habitantes y trimestre |
| `tasa_robo_negocio` | robo a negocio |
| `tasa_extorsion` | extorsión |
| `tasa_robo_total` | todos los subtipos de "Robo" |
| `tasa_homicidio_doloso` | homicidio doloso (carpetas, no víctimas) |
| `tasa_dano_propiedad` | daño a la propiedad (placebo de denuncia) |
| `pct_participacion` | votos / lista nominal × 100, sin casillas especiales ni mesas sin sección |
| `pct_bloque_gobierno` | (Morena + PT + PVEM, con su parte igual de las combinaciones) / votos válidos × 100 |
| `pct_morena` | Morena con su parte de las combinaciones / votos válidos × 100 |
| `pct_nulos` | votos nulos / votos × 100 |

## Advertencias

- **Denuncias, no delitos.** El SESNSP cuenta carpetas de investigación registradas por las
  fiscalías estatales, en el municipio de registro, que no siempre es el de ocurrencia.
- **Cobertura del SESNSP.** 1,921 municipios estables en 2015–2016 y 2,456 desde 2017.
- **Claves del INE.** No son las del INEGI, y el INE las reasigna (Chiapas 07-120 a 07-124). En
  2015 el INE aún no separaba varios municipios (Chiapas 1999, Tulum, Oaxaca).
- **Aguascalientes D01, 2015.** El SICEE trae la elección extraordinaria de diciembre de 2015 (445
  casillas), no la ordinaria de junio.
- **Reparto de coaliciones.** Igualitario y sin redondeo. Los cómputos oficiales asignan el sobrante
  al partido más votado de la casilla; la diferencia es de menos de un voto por casilla.

# Presentación para Tópicos de Política Pública II

Deck de 14 láminas para 12 minutos (más 4 de respaldo después de "Gracias") sobre el proyecto:
política, pregunta y mérito, historia causal, datos, estrategia, resultados, uso de las cuentas,
actividad económica e implicaciones de política. Formato **.pptx para importar a Google Slides**,
con notas del presentador en cada lámina. Mismo estilo que el deck de Ciencia de Datos Aplicada II
(`../05_ciencia_datos/`): Lora y Source Sans 3, fondo `FAFAFA`, azul `0B5FFF`.

```bash
make presentacion-ppii
```

1. `figuras.py` lee `outputs/tablas/` (no estima nada), el panel municipal, el Marco Geoestadístico y
   `app/public/datos/uso.json`; dibuja `outputs/figuras/ppii_*.png` y escribe `cifras.json`.
   Reutiliza el estilo y los lectores de `05_ciencia_datos/figuras.py` (lo carga como módulo, sin
   tocarlo). Las únicas cifras escritas a mano están en `EXTERNAS`, cada una con su fuente.
2. `presentacion.js` (pptxgenjs) arma `presentacion_ppii.pptx`. El diagrama causal y las tablas
   son formas nativas, editables en Slides. Imprime las palabras de las notas por lámina y falla si
   las de la exposición pasan de 1,500.

**Importar a Google Slides:** Archivo → Importar diapositivas (o subir el .pptx a Drive y abrirlo
con Slides). Las notas llegan. Si Slides no reconoce "Source Sans 3", seleccionar todo y asignarla.

**PDF de revisión** (LibreOffice; `fonts.conf` le enseña las fuentes de `~/Library/Fonts`, sin él
sustituye Lora y Source Sans 3 por las suyas y pinta mal los signos):

```bash
FONTCONFIG_FILE=$PWD/entregables/06_politica_publica/fonts.conf SAL_USE_VCLPLUGIN=svp soffice -env:UserInstallation=file:///tmp/lo_ppii --headless --convert-to pdf --outdir entregables/06_politica_publica entregables/06_politica_publica/presentacion_ppii.pptx
```

Requisitos: `uv`, Node ≥ 18 y, para el PDF, LibreOffice. `node_modules/`, el .pptx y el PDF no se
versionan; `make` corre `npm ci` la primera vez.

## Tiempos y reparto

| # | Lámina | s | Presenta |
|---|---|---|---|
| 1 | Portada | 15 | Andrés |
| 2 | De Bansefi al Banco del Bienestar | 45 | Andrés |
| 3 | Pregunta y mérito | 50 | Andrés |
| 4 | Historia causal | 60 | Andrés |
| 5 | Aperturas escalonadas | 35 | Fernando |
| 6 | Datos y variables | 55 | Fernando |
| 7 | Estrategia empírica | 75 | Fernando |
| 8 | Primera etapa | 30 | Luis |
| 9 | Banca privada | 50 | Luis |
| 10 | ¿Aguanta? | 50 | Luis |
| 11 | ¿Se usan las cuentas? | 30 | Luis |
| 12 | El aumento del DENUE no es de la sucursal | 35 | Luis |
| 13 | Interpretación y política | 90 | Luis |
| 14 | Conclusiones | 30 | Luis |
| | **Total** | **650 (10:50)** | |

Bloques del curso: pregunta y mérito 1:50 (1–3), metodología 2:50 (4, 5 y 7), datos 0:55 (6),
resultados 3:15 (8–12), interpretación y política 2:00 (13–14). Notas de la exposición: 1,341
palabras. Respaldo (no cuenta en el tiempo): emparejamiento y balance, efectos fijos, desierto
bancario, fases 2 y 3.

## De dónde sale cada cifra

Todas pasan por `cifras.json`. Tablas en `outputs/tablas/` salvo que se diga otra cosa.

| Cifra en el deck | Lámina | Origen |
|---|---|---|
| 540 sucursales (2019T1) y 3,149 (2024T4) | 2 | `data/interim/sucursales_bienestar.parquet` (BDIF sin Banjército) |
| Meta de 2,744; 1,873 terminadas y 922 operando en 2022 | 2 | ASF (2023), `EXTERNAS` en `figuras.py` |
| 62% de municipios sin banca múltiple en 2019 | 2 | `data/processed/panel_municipio_trim.parquet` (2019Q1) |
| 0.5 créditos por 100 cuentas contra 61 (2025T4) | 2, 11 | `app/public/datos/uso.json` (`app/datos/temas.py`; `docs/decisiones.md`, fase 5) |
| +7.6% y 815 sucursales de Banco Azteca | 3, 7 | Bruhn y Love (2014), `EXTERNAS` |
| ≈+10% en Brasil | 3 | Fonseca y Matray (2024), `EXTERNAS` |
| 1,457 tratados contra 500 | 5, 8 | `tabla_final.csv` (principal, `sucursales_privado_pc`) |
| 487 / 475 / 785 / 209 / 500 por cohorte (mapa) | 5 | `panel_municipio_trim.parquet` (`G`) |
| 2,456 municipios | 6 | `panel_municipio_trim.parquet` |
| ±5% = 0.046 por 10 mil adultos ≈ 132 sucursales | 7, 10, 14 | `config/parametros.yaml` (`sesoi_pct`) y `desc_soporte_comun.csv` |
| +2.00 (ee 0.08), previos p = 0.28 | 8 | `tabla_final.csv` (primera etapa, `sucursales_total_pc`) |
| +3,284 tarjetas, previos p = 0.99 | 8 | `fase4_bancarizacion.csv` |
| +0.7% (0.007, ee 0.009), cota ±2.4%, Wald p = 0.29 | 9, 10 | `tabla_final.csv` (principal) |
| Banca múltiple −0.2%, EACP +1.5% | 9 | `tabla_final.csv` (principal) |
| Captación −0.2%, crédito −0.1%, 766 contra 500 | 9 | `tabla_final.csv` (`panel_corto`) |
| Tarjetas de crédito de banca múltiple +0.8% | 9 | `fase4_uso.csv` (C4) |
| Crédito al consumo de EACP +4.3%; previos del apilado p < 0.001 | 9 | `tabla_final.csv` (`eacp`) y `apilado_resumen.csv` |
| Placebo de fecha −0.6% | 10 | `fase4_validez.csv` (A2) |
| Permutación p = 0.32 | 10 | `fase4_permutacion.csv` |
| HonestDiD −4.0% a +2.2% | 10 | `fase4_honest_sd.csv` (M = 0) |
| Otros 7 estimadores −0.6% a +2.5% | 10 | `fase4_estimadores.csv` |
| Solo por calendario −1.9% (−4.2% a +0.3%; p = 0.14) | 9, 10 | `poder_inyectado_diagnostico.csv` |
| ±5% inyectado: se detecta 90% a 98%; ±2.8%: 44% a 72% (notas) | 10 | `poder_inyectado_calibrado.csv` |
| +1.9% contra nunca tratados con fechas barajadas (notas) | R2 | `poder_inyectado_diagnostico.csv` |
| +1,316 contratos y +6.2 créditos; 763 contra 498 | 11, 14 | `uso_resumen.csv` |
| +5,999 transacciones en cajeros del banco; 1.8 por tarjeta (notas) | 11 | `fase4_bancarizacion.csv` |
| DENUE +10.4%; 1,106 contra 21,719 | 12 | `tabla_final.csv` (localidad, principal) |
| Decaimiento +11.7% / +8.9% / +0.9% | 12 | `decaimiento_estab_emprendimiento_pc.csv` |
| Sin dosis: 2022 +11.2% contra 2023–24 +10.0% (notas) | 12 | `het_q.csv` (exposición) |
| Censos −0.9% (±4.0%), 1,252 municipios | 12 | `tabla_final.csv` (`ce`, `ue_pc`) |
| Dueños de negocio −1.2 puntos; descarta más de +1.8% | 12, R4 | `fase2_resumen.csv` (`municipio_eic`) |
| ±6% con M̄ = 0.25 (notas) | 13 | `rob_honest_municipio_trim_esc_sucursales_privado_pc.csv` |
| Banca múltiple −2.5% a −2.2% con efectos fijos (notas) | 13 | `fase4_estimadores.csv` |
| +2.3% (±7.4%), 320 contra 320 | R1 | `fase4_controles.csv` (H1d) |
| +9.7%, 562 contra 724, previos p = 0.29, diferencias ≤ 0.03 | R1 | `rob_localidad_act_estab_emprendimiento_pc.csv`, `balance_localidad_estab_emprendimiento_pc.csv` |
| Balance 0.11 / 0.23 / 0.38; sin 2023T4–2024T1 −0.4% (±2.7%) | R1 | `desc_soporte_comun.csv`, `desc_soporte_robustez.csv` |
| TWFE extendido +6.8% (ee 2.7%), solo los que abren +1.3%, soporte común +7.7% | R2 | `fase4_diagnostico_etwfe.csv` (figura: `fase4_estimadores.csv`) |
| CS con ajuste lineal +2.1% | R2 | `fase4_diagnostico_cs_metodo.csv` |
| q = 0.66 y 0.04; DENUE +12.3% contra +5.3% | R3 | `het_q.csv` |
| VIIRS +0.15 puntos log (por calendario, ee 0.83) | R4 | `fase2_rob_extra_viirs_log1p_luz_1km.csv` (solo con sucursal) |
| Robo a transeúnte −0.2%, homicidio +0.1%, cotas 12%–50% | R4 | `fase3_resumen.csv` |
| Participación −2.9 puntos, previos p < 0.001 | R4 | `fase3_resumen.csv` |

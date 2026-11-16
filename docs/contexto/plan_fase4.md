<!-- Plan aprobado el 2026-10-14. Copia de trabajo; el preregistro formal está en docs/decisiones.md. -->

# Fase 4: efectos fijos, controles, causalidad, bancarización, uso y bienestar

## Contexto

La metodología se entrega el jueves 15 de octubre y el trabajo final el **lunes 7 de diciembre de
2026**. Hoy el resultado central es un nulo informativo: el banco abre cuentas donde llega, pero
no desplaza ni atrae a la banca privada (+0.7%, IC90 dentro de ±2.4%).

Hay dos motivos para la fase 4.

**1. Critican el uso de Callaway–Sant'Anna y la forma de los controles.** La respuesta es mostrar
que el nulo **no depende del estimador ni de los controles**:
- poner la regresión con efectos fijos (la que piden) al mismo nivel que CS;
- hacerlo con versiones que no se sesgan con efectos heterogéneos;
- cambiar el grupo de control y las covariables una por una.

**2. Ampliar el alcance:**
- validar que el nulo es causal (derrames, placebos);
- separar cuentas nuevas de cuentas trasladadas;
- medir el uso y el bienestar.

Ya existe un borrador sin versionar, `docs/contexto/plan_fase4.md` (escrito antes de este plan).
Este plan lo reemplaza y lo amplía.

## Respuesta corta a la crítica, con lo que ya está corrido

Sucursales privadas por cada 10 mil adultos. Media previa: 0.929. Umbral de ±5% = ±0.046.

| Estimador o variante | Efecto | ee | Fuente |
|---|---|---|---|
| CS DR, aún no tratados (base) | +0.0066 | 0.0094 | `comp_municipio_trim_esc_sucursales_privado_pc.csv` |
| TWFE estático, efectos fijos de municipio y de trimestre | +0.0091 | 0.0204 | ídem |
| Sun y Abraham | +0.0029 | 0.0135 | ídem |
| Borusyak et al. (imputación) | +0.0115 | 0.0247 | ídem |
| DiD apilado, efectos fijos de unidad × pila y de evento | +0.8% (±2.7%) | — | `apilado_resumen.csv` |
| CS solo con nunca tratados | +0.0081 | 0.0106 | `rob_municipio_trim_esc_sucursales_privado_pc.csv` |
| CS sin covariables | +0.0038 | 0.0102 | ídem |
| CS con anticipación de un trimestre | +0.0067 | 0.0128 | ídem |
| CS sin las cohortes desbalanceadas (2023T4, 2024T1) | −0.0037 | 0.0128 | `desc_soporte_robustez.csv` |

- **Goodman-Bacon:** solo el 11.9% del peso del TWFE está en comparaciones prohibidas, por eso el
  TWFE se parece a CS.
- **Lo honesto:** las regresiones con efectos fijos son menos precisas que CS. El IC90 del TWFE
  llega a 4.6% de la media (pasa ±5% por poco) y el de BJS a 5.6% (no pasa solo). El de Sun y
  Abraham llega a 2.7%.
- Las covariables son tres, todas previas: log de población 2020, índice de marginación 2020 y
  banca múltiple en 2019T1. Verificado en `config/parametros.yaml` (`covariables_previas`) y en
  `analisis/00_utils.R::formula_covariables`.

## Datos verificados (2026-10-14)

- **Portafolio CNBV** (`data/interim/cnbv_portafolio_{operativa,modelo}.parquet`). Banco del
  Bienestar (`037166` en el modelo, "Banco del Bienestar" en la operativa) por municipio y mes,
  2016-01 a 2026-07: sucursales, contratos de tarjeta de débito y transacciones en cajeros.
  - Los saldos son de fin de mes y el empalme dic-2021 → ene-2022 es continuo (14.1 y 13.9
    millones de tarjetas).
  - 🔴 Saltos de −4.3 millones en sep-2021 y de +5.9 millones en feb-2022.
  - 🔴 Las transacciones siguen el pago bimestral de programas: hay que sumar los tres meses del
    trimestre.
- **BDIF** (`data/interim/cnbv_bdif.parquet`): `tarjetas_credito` de "banca" y
  `establecimientos_tpv` de "todos", sin hueco 2016–2025. Restando lo que el Portafolio atribuye al
  banco y a Banjército quedan series privadas con panel largo.
  - 🔴 Hay un escalón de Compartamos en banca múltiple en 2019T1 (P-11). Hay que corregirlo con
    `modulos_compartamos` (2017T2–2018T4) antes de usar los periodos 2016–2018.
- **ENIGH 2024, nueva serie.** Del descriptor (ya leído):
  - `ubica_geo` C(5) = entidad + municipio;
  - `forma_pag1..3` con 01 efectivo, 04 transferencia, 05 crédito, 06 débito y 09 pago móvil;
  - `fpago_2` y `fpago_4` para los negocios del hogar;
  - `deposito`, `bene_gob`, ingreso y gasto en el concentrado.
  - **Falta verificar:** los códigos de 2016–2022, el número de municipios repetidos entre olas,
    las fechas de levantamiento y el tamaño de los archivos.
- **ENIF 2024:** 13,303 viviendas con `ENT`, `TLOC` y `REGION`, sin municipio. Solo descriptivo.
- **MG 2024** (`data/raw/inegi_mg/`) más `geopandas` (Python) y `sf` (R, ya en renv): de ahí sale
  la contigüidad municipal.
- **No disponible:** fecha de obra por sucursal (habría que pedirla por la PNT; opcional), padrón
  de programas con forma de pago, ubicación de las sucursales privadas.

## Bloques

### 0. Regresión con efectos fijos (prioridad 1; responde la crítica al estimador)

| # | Especificación | Implementación |
|---|---|---|
| 0.1 | **Estudio de evento TWFE clásico**: efectos fijos de municipio y de trimestre, e ∈ [−8, 8] con extremos agrupados, ref = −1, cluster municipal | `fixest::feols(y ~ i(e_bin, ref = -1) \| id + tiempo)`. Figura junto a Sun–Abraham y CS para mostrar cuánto contamina el TWFE |
| 0.2 | **TWFE extendido de Wooldridge (2021)**: una sola regresión con efectos fijos de municipio y de trimestre e interacciones cohorte × periodo post. Robusto a efectos heterogéneos | `feols(y ~ i(celda) \| id + tiempo)`, con `celda` = (G, t) para t ≥ G. Con covariables: pendientes variables `tiempo[log_pob, marg, banca]`. ATT agregado con pesos por cohorte y varianza por combinación lineal, como en `estimar_apilado`. Sin covariables debe coincidir con BJS (prueba interna) |
| 0.3 | **Apilado con efectos fijos estado × evento** | `apilar()` y `estimar_apilado()` de `08_disenos_alternativos.R`, con efectos fijos `id^pila + e^estado` |
| 0.4 | **Sensibilidad de los efectos fijos** | TWFE y TWFE extendido con: (a) estado × trimestre; (b) decil de tamaño × trimestre (`efectos_fijos(fe_tamano)` ya existe); (c) tendencias lineales municipales `id[tiempo]`; (d) covariables × trimestre |
| 0.5 | **Triangulación** | `fase4_estimadores.csv` y la figura `fig_fase4_estimadores.png`: un renglón por estimador y variante, para las tres variables financieras y la primera etapa. Va al trabajo final y a la presentación |

### H. Grupo de control y covariables (prioridad 1; responde la crítica a los controles)

**H1. Grupo de control:**
- (a) aún no tratados (base);
- (b) solo nunca tratados (ya existe);
- (c) **solo municipios que alguna vez abren**: sin los 500 nunca tratados, se identifica solo por
  el calendario, tempranos contra tardíos. Responde a "los nunca tratados no se parecen";
- (d) nunca tratados emparejados por puntaje de propensión. Hay que revisar si
  `data/processed/matching_municipio_trim_sucursales_privado_pc.parquet` sirve; si no, se extiende
  `construccion/matching.py`;
- (e) controles sin vecino tratado (A1).

**H2. Covariables, una por una:**
- la secuencia: ninguna → población → + marginación → + banca 2019;
- \+ tendencia previa del resultado 2016–2018, ya corregida por Compartamos;
- \+ distancia del centroide al municipio más cercano con banca múltiple en 2019T1 (MG + BDIF;
  completa la `distancia_banca_km` pendiente en `parametros.yaml`);
- \+ región.

**H3.** Tabla de balance y soporte común para el trabajo final, a partir de `desc_soporte_comun.csv`.

**H4.** `docs/contexto/defensa_estimador.md`: una nota de una página para el profesor y el equipo,
con por qué CS, por qué aún no tratados, por qué esas covariables y qué muestran 0 y H. Con las
cifras de la tabla de arriba ya se puede escribir.

### A. ¿Es causal el nulo? (prioridad 1)

- **A1. Derrames.** Contigüidad de primer orden. (a) Controles sin vecino tratado. (b) Efecto en
  los vecinos de los municipios que abren, contra controles lejanos.
- **A2. Placebo de fecha.** Panel largo 2016–2018, con la fecha de apertura adelantada 8
  trimestres; banca múltiple corregida por Compartamos.
- **A3. Inferencia por permutación.** 199 reasignaciones de fechas dentro del estado, con el TWFE
  extendido (rápido).
- **A4. HonestDiD con suavidad.** Restricción Δ^SD además de magnitudes relativas, y M̄ de quiebre
  por resultado (se reutiliza `honest()` de `05_robustez.R`).
- **A5.** ATT(g) por cohorte, y dejando fuera un estado a la vez.

### B. Bancarización (prioridad 1)

- **B1.** Tarjetas de débito del banco por municipio 2016–2026 (Portafolio), para los 1,457
  municipios tratados y no solo 766. Antes, revisar si los saltos de sep-2021 y feb-2022 se
  concentran en ciertos municipios.
- **B2. Traslado contra bancarización.** Tarjetas del banco en los municipios vecinos cuando abre
  una sucursal (contigüidad de A1). Si bajan, parte de la primera etapa es traslado.

### C. Uso

- **C4.** Crédito privado con panel largo: tarjetas de crédito de "banca" menos banco y
  Banjército, 2016–2025. *(Prioridad 1.)*
- **C1.** Transacciones en cajeros ÷ tarjetas del banco (suma trimestral). *(Prioridad 2.)*
- **C3.** Comercios con TPV privados con panel largo (BDIF menos banco). *(Prioridad 2.)*
- **C2.** Proporción del gasto de los hogares pagado con débito, transferencia o pago móvil (ENIGH
  2016–2024, cortes transversales repetidos). Hogar × ola, tratamiento = municipio con sucursal
  antes del levantamiento, efectos fijos de municipio y de ola, CS con `panel = FALSE` y TWFE
  extendido, cluster municipal. **Antes, el efecto mínimo detectable.** *(Prioridad 3.)*

### D. Bienestar (prioridad 3, ENIGH)

Ingreso per cápita, gasto, `deposito > 0` y `bene_gob`, con el diseño de C2. Si el efecto mínimo
detectable es mayor a ~10%, queda como descriptivo y así se dice. Lo que ya existe (IMSS, EIC,
VIIRS) se resume como "sin efecto detectable en ingreso laboral".

### E. Mecanismo

- **E1.** La distancia de H2 como moderador continuo.
- **E2.** θ(e) a más de 16 trimestres para los resultados del Portafolio.
- No se puede desagregar por sexo: el Portafolio solo lo trae 2018–2021, antes del tratamiento.

### F. Trabajo final y presentación (siempre; para el 7 de diciembre)

1. `trabajo_final.qmd` al formato del curso: abstract de 150 palabras como máximo, 10 cuartillas
   a doble espacio en 11 pt, una tabla o figura por página con nota, al menos 15 referencias en
   formato AER.
2. En la estrategia empírica: CS como principal y el TWFE extendido y el apilado como regresiones
   con efectos fijos de respaldo (bloque 0), la triangulación, el balance (H3) y los diagnósticos
   del 12 de octubre.
3. La fase 4 en un apéndice.
4. Presentación de 6–7 láminas sustantivas, más una lámina de respaldo con la triangulación.

## Implementación

- **Preregistro primero:** `docs/decisiones.md`, sección "Preregistro de la fase 4", con hipótesis,
  familias y criterios de siempre:
  - pre-prueba fallida = descriptivo;
  - IC90 dentro de ±5% = nulo informativo;
  - Romano–Wolf en la familia `financiero_fe` (bloque 0) y en `bancarizacion`; BH en el resto.
- **Configuración:** sección `fase4:` en `config/parametros.yaml` (ventanas, rangos de evento,
  permutaciones). Entrada `enigh` en `config/fuentes.yaml`.
- **Python:**
  - `src/proyecto/variables/contiguidad.py`: pares de municipios vecinos y distancia entre
    centroides, a partir del MG 2024 con `geopandas`.
  - `src/proyecto/construccion/panel_fase4.py`, sin tocar `panel.py`:
    - `municipio_trim_banco` (Portafolio por trimestre);
    - `municipio_trim_largo_privado` (crédito y TPV privados, corregidos por Compartamos);
    - banderas de vecino.
  - ENIGH: `descarga/enigh.py` y `limpieza/enigh.py`, después de verificar los códigos y los
    tamaños.
- **R:** `analisis/13_fase4.R`, que hace `source()` de `03_twfe_comparacion.R`,
  `05_robustez.R`, `08_disenos_alternativos.R`, `10_fase2.R` y `12_diagnosticos.R`, y registra sus
  paneles en tiempo de ejecución, como `11_fase3.R`.
  - Funciones nuevas: `estudio_evento_twfe()`, `twfe_extendido()`, `sensibilidad_fe()`,
    `controles()`, `covariables_secuencia()`, `derrames()`, `placebo_fecha()`, `permutacion()`,
    `banco_largo()`, `uso()`, `enigh()` y `resumen()`.
  - Se reutilizan:
    - `correr_bloque()` y `subgrupos()` (`10_fase2.R`);
    - `variante()` y `honest()` (`05_robustez.R`);
    - `apilar()` y `estimar_apilado()` (`08`);
    - `twfe_estatico()`, `sun_abraham()`, `bjs_imputacion()` y `bacon_resumen()` (`03`);
    - `diagnostico()` (`12`);
    - `leer_panel()`, `formula_covariables()` y `guardar_tabla()` (`00_utils.R`).
- **Make:** `descargar-fase4`, `panel-fase4`, `fase4` y `bateria-fase4` (termina con
  `make entregables`).
- **Entregables:** `tabla_fase4()` en `utils/entregables.py` → `_tablas/tab_fase4.md`, la figura
  de triangulación, el apéndice y la lámina.
- **Pruebas** (`tests/test_fase4.py`, solo si las apruebas):
  - la serie privada (total − banco − Banjército) nunca es negativa y suma igual a nivel nacional;
  - la contigüidad es simétrica y no hay municipios sin vecinos, salvo islas documentadas;
  - el TWFE extendido sin covariables coincide con BJS;
  - la suma trimestral del Portafolio cuadra con los meses.

## Calendario (unas 60 horas)

| Semana | Trabajo |
|---|---|
| 15–21 oct | Entregar la metodología. Preregistro de la fase 4. `defensa_estimador.md` (H4) con lo ya corrido |
| 22–28 oct | Bloque 0 (0.1–0.5) y H1–H2. Contigüidad y A1 |
| 29 oct–4 nov | B1, B2 y C4. A2, A4 y A5 |
| 5–11 nov | A3, C1 y C3. Corrida `bateria-fase4` (prioridades 1–2) y lectura |
| 12–18 nov | ENIGH: verificar, descargar, limpiar, efecto mínimo detectable. Se decide si sigue |
| 19–25 nov | C2, D y B3 si sigue. Empieza F |
| 26 nov–2 dic | F completo. `/code-review` |
| 3–7 dic | Margen y entrega |

Si falta tiempo se corta, en este orden: la solicitud a la PNT, synthdid, D, C2 y A3. **El bloque
0, H, A1, B1 y F no se cortan.**

## Verificación

- **Pruebas de humo** de cada bloque:
  `PROYECTO_SALIDAS=$(mktemp -d) PROYECTO_NBOOT=49 Rscript analisis/13_fase4.R <bloque>`.
- **Comprobaciones internas, en el registro de la corrida:**
  - CS base reproduce exactamente `tabla_final` (+0.0066, ee 0.0094);
  - el TWFE extendido sin covariables coincide con BJS (+0.0115);
  - el TWFE clásico estático coincide con +0.0091;
  - las series privadas reconstruidas cuadran con los totales nacionales de la BDIF;
  - la contigüidad es simétrica.
- **Al terminar:** `make test`, `make lint` y `make entregables` en verde, con el PDF y la
  presentación revisados a ojo.
- `pgrep -f 'bin/exec/R|Rscript'` vacío antes de editar `analisis/*.R` y al terminar.
- `/code-review` de todo lo nuevo, y la lista de cifras escritas a mano con su CSV de origen.
- Commits pequeños, uno por bloque, con aprobación, en formato `type(scope): …` y sin push. El
  primero: `docs: plan de la fase 4` (`CLAUDE.md` y `docs/contexto/plan_fase4.md`, actualizado
  con este plan).

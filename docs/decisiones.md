# Bitácora de decisiones

Formato: fecha · decisión · razón · fuente. Las **tomadas** están cerradas; las **propuestas y
pendientes** requieren decisión del equipo antes de construir el panel (`make panel`).

## Tomadas

| Fecha | Decisión | Razón / fuente |
|---|---|---|
| 2026-09-14 | Lista de lectura: solo papers o reviews; ASF, IMCO, BDIF y Programa Institucional son contexto y datos. | `docs/contexto/investigacion_1.md` §6 |
| 2026-09-14 | Los 4 papers núcleo: Bruhn y Love (2014), Fonseca y Matray (2024), Callaway y Sant'Anna (2021), Aportela (1999). Fonseca y Matray sustituye a Célerier y Matray en el top 4. | `investigacion_1.md` §6 |
| 2026-09-14 | Los resultados principales se miden **sin** el Banco del Bienestar (solo banca múltiple y EACP) por el efecto mecánico: el banco dispersa programas sociales y sus cuentas suben por construcción. El total va como resultado secundario. | ASF 2023 (en 2022 el banco no dio crédito); `bases-de-datos.md` riesgo 1 |
| 2026-09-14 | Las fechas de tratamiento salen de sucursales **operando** en la BDIF, no de avance de obra (ASF: 1,873 terminadas vs 922 operando al cierre de 2022). | `investigacion_1.md` §0.9 |
| 2026-09-15 | Estimador: Callaway y Sant'Anna (2021), paquete `did`; comparación con TWFE. | Diseño del proyecto |
| 2026-09-15 | Claves municipales siempre como texto de 5 dígitos; nunca unir por nombre. Periodo `YYYYQn` y `t` con 2019Q1 = 1; `G = 0` para nunca tratados. | Reglas del proyecto |
| 2026-09-15 | `data/raw/` inmutable; transformaciones a `data/interim/` y `data/processed/` en Parquet. | Reglas del proyecto |
| 2026-09-15 | Descargar la BDIF desde 2016T1 (no solo 2019T1) para robustez y pre-tendencias; se bajaron 40 trimestres hasta 2025T4. | Tarea; disponibilidad en la página CNBV |
| 2026-09-15 | ENIF no se descarga (no es municipal; no entra en la estimación). | Tarea |
| 2026-09-15 | Sitios que bloquean clientes no navegador (datos.gob.mx, repodatos.atdt.gob.mx) y servidores caídos (conapo.segob.gob.mx) → descarga manual documentada, sin evadir protecciones. | Regla 5; `docs/descarga_manual.md` |
| 2026-09-15 | Polígonos municipales: extracción parcial por rangos HTTP de `00mun.*` del zip nacional del MG 2024 (3.1 GB) en vez de bajarlo completo. Registrado en MANIFEST con nota. | Tamaño; `src/proyecto/utils/zip_remoto.py` |
| 2026-09-15 | Crosswalk municipal hijo→padre por cruce espacial de localidades ITER 2010 contra polígonos 2024 (22 hijos, 21 padres). | `docs/diccionarios/crosswalk_municipios.md` |
| 2026-09-26 | 🔴 **Los saltos metodológicos del DENUE son heterogéneos.** La serie nacional crece ~0.5% por versión salvo en **2019S2 (+6.5%)** y **2024S2 (+8.9%)**, que son actualizaciones integrales del INEGI. Al separar por grupo: en 2019S2 las localidades tratadas crecen **11.2%** contra **6.1%** de los controles; en 2024S2, **12.4%** contra **8.5%**. Es composición (la actualización incorpora más establecimientos donde hay más actividad, y las tratadas son más grandes), pero contamina el diseño: el salto de 2019S2 es **previo** al tratamiento y el de 2024S2 es **posterior**. Robustez obligatoria: excluir 2024S2–2025S1 y verificar que el event study no herede la pre-tendencia de 2019S2. | `denue_cobertura.parquet`; comparación de crecimiento por grupo |
| 2026-09-26 | El tratamiento a nivel localidad usa la fecha municipal de la BDIF solo cuando el municipio tiene **una sola** sucursal (1,270 casos); con 2+ se marca `fecha_ambigua` y se excluye de la especificación principal. | `tratamiento_localidad.parquet`; distancia mediana sucursal-localidad de 0.41 km |
| 2026-09-26 | Se excluyen las **cohortes de menos de 5 unidades**: producían ATT(g,t) sin varianza utilizable que dominaban los rezagos largos del event study (con cohortes de 1 municipio aparecían efectos de −1.14 con intervalos de ±0.02). | `leer_panel(min_cohorte = 5)` en `analisis/00_utils.R` |
| 2026-09-26 | El **matching** empareja contra **aún no tratados** (no solo nunca tratados): hay 1,461 municipios tratados contra 500 nunca tratados, y estos son sistemáticamente más pequeños y rurales. Coincide con el grupo de comparación del estimador. Balance máximo: 0.64 → 0.22 de diferencia estandarizada. | `construccion/matching.py`; `outputs/tablas/balance_*.csv` |
| 2026-09-26 | Un resultado solo se estima si tiene **al menos dos periodos previos con dato**. Captación y crédito por sector (BDIF desde 2022T4) no lo cumplen: estimarlos daba un falso efecto de +177 contratos por 10 mil adultos que en realidad era el salto de cobertura de la fuente. | `06_correr_todo.R`; ver también el arreglo de `min_count=1` al colapsar municipios |
| 2026-09-26 | **Rediseño tras la reunión con el asesor:** la unidad principal pasa a ser la **localidad** (el municipio es demasiado grande para que una sucursal mueva el agregado); se agregan resultados reales (emprendimiento, consumo, salud) además de los financieros; se agrega **matching** como especificación alterna; el reporte central es el **event study** del estimador escalonado. | Reunión del 2026-09-26; notas de Fernando Barba |
| 2026-09-26 | Se prueban **tres unidades en paralelo** (localidad, municipio, anillos de 1/2/5/10 km) y los cuatro bloques de resultados en orden: emprendimiento → consumo → salud → financieras. La comparación entre radios es la prueba de que la localidad es la unidad correcta (si el efecto no decae suavemente con el radio, el agregado municipal no sirve). | Decisión de Andrés, 2026-09-26 |
| 2026-09-26 | Fuente nueva: **DENUE histórico del INEGI** (18 versiones semestrales 2016-01 – 2025-05, georreferenciado, SCIAN y personal ocupado). Da emprendimiento, consumo, salud y presencia financiera privada a nivel localidad o radio, que la BDIF no puede dar. | Verificado el 2026-09-26; ver `docs/diccionarios/denue.md` |
| 2026-09-26 | El DENUE se descarga por **streaming**: se baja el zip, se agrega a localidad/municipio/puntos, se registra el hash en MANIFEST y se borra el crudo. Motivo: 13 GB de crudo contra 16 GB libres en disco. Reproducible con `--force`. | `df -h`; regla 2 del proyecto (raw inmutable) se mantiene para lo que sí se conserva |
| 2026-09-26 | El tratamiento a nivel localidad se fecha combinando la fecha municipal de la BDIF con el directorio georreferenciado: 1,270 de 1,482 cohortes (86%) tienen una sola sucursal. Los municipios con 2+ sucursales se marcan `fecha_ambigua` y salen de la especificación principal. | Cruce `babien.parquet` × `sucursales_bienestar.parquet` |
| 2026-09-26 | El DENUE **no** se usa para el tratamiento: en 2022-11 todavía lista 593 establecimientos como "BANSEFI" y solo 53 como "Bienestar". | Búsqueda por `nom_estab` en el sector 52 |
| 2026-09-26 | Panel semestral con 18 versiones sobre 19 semestres calendario: **2023S1 no existe para nadie** (el INEGI no publicó versión de primavera 2023). Hueco común, no desbalance. | Listado de versiones en la página de descarga masiva |
| 2026-09-15 | Banjército se descuenta del tratamiento con el Portafolio de Información CNBV (`BD_Operativa` mensual 2016-01 – 2021-12, por institución × localidad), extrapolando su red de 2021-12 (75 municipios) solo hacia 2022+. Serie: `data/interim/sucursales_bienestar.parquet`. | Cuadre exacto con la BDIF en 2016T1–2020T1 (totales y municipio por municipio); `docs/data_audit.md` P2 |
| 2026-09-26 | 🔴 **La ventana limpia del DENUE (2019S2–2024S1) es la especificación principal.** Sin ella el diseño daba +2.669 (ee 0.313) en emprendimiento, pero la agregación por **calendario** muestra ATT ≈ 0 en todos los semestres hasta 2024S1 (−0.001, −0.016, +0.197, +0.193) y **+5.573 en 2024S2**: las cuatro cohortes saltan a la vez en tiempo calendario, sin importar cuánto llevan tratadas, justo cuando la actualización integral del DENUE sumó 8.9% de establecimientos nacionales y más donde ya había actividad (tratadas +12.4% contra controles +8.5%). No es composición del control: con solo nunca tratados daba +2.665. La ventana también elimina el único coeficiente previo significativo (e = −8, que era el cambio 2019S1→2019S2, la otra actualización): al empezar en s = 8 ese cambio deja de ser estimable. Con la ventana el resultado es un **nulo preciso** en los cuatro bloques, con las 8 pre-tendencias planas. El panel completo se reporta como robustez, para mostrar de dónde sale el efecto grande. | `estimacion.ventana_semestral` en `config/parametros.yaml`; `outputs/tablas/cs_agg_*` tipo `calendar`; `rob_localidad_*` |
| 2026-09-26 | 🔴 **Los anillos no se usan para identificar; la localidad sí.** Auditoría de coeficientes previos significativos sobre las 33 especificaciones: **localidad 0 de 9**, **BDIF trimestral 0 de 3**, municipio 1 de 7 (emprendimiento, e = −8), **anillos 1 a 4 en cada una** (el de 1 km tiene e = −8, −7, −6 y −4 positivos y significativos). El +0.889 del anillo de 1 km no se distingue de una tendencia que ya venía, y el aparente decaimiento con el radio era esa tendencia. El argumento a favor de la localidad no es potencia sino identificación: es el único nivel donde se sostienen tendencias paralelas. Los anillos quedan como descriptivo del alcance espacial. | Conteo de previos significativos en `outputs/tablas/cs_agg_*` tipo `dynamic` |
| 2026-09-26 | 🔴 **El bloque financiero del DENUE no se usa como variable respuesta.** El SCIAN 52 tiene seis rupturas de cobertura nacional: 2018S1 **+41.5%**, 2019S1 **+23.9%**, 2019S2 **−17.2%**, 2020S1 **+19.4%**, 2024S2 −3.8% y 2025S1 **−8.1%**; dentro del bloque, `banca_multiple` pasa de 23,240 (2017S2) a 46,385 (2018S1) y las casas de empeño de 1,186 a 2,724 (2023S2) y de ahí a 392 (2025S1). Los otros tres bloques solo tienen las dos actualizaciones integrales conocidas (2019S2 y 2024S2, ≤14%). Con saltos de ese tamaño en el pre-periodo el estimador lee cobertura, no tratamiento; el síntoma fue que el efecto por anillo **crecía** con el radio (+0.29 a 1 km, +2.56 a 10 km) al revés de todos los demás resultados. El financiero se mide solo con la **BDIF**, que es la fuente regulatoria; el DENUE queda como descriptivo. | Totales nacionales por bloque y semestre desde `data/interim/denue/partes/`; `DENUE_FINANCIERO_DESCRIPTIVO` en `analisis/06_correr_todo.R` |
| 2026-09-26 | Las covariables **constantes en la submuestra** se descartan al construir `xformla`: al partir el panel por una dimensión de heterogeneidad, la covariable que define la partición queda con un solo nivel y rompe `model.matrix` (`contrasts can be applied only to factors with 2 or more levels`). Sin esto faltaban los subgrupos «marginación media» y «con banca múltiple previa», que es justo el contrafactual del resultado de desiertos bancarios. | `formula_covariables()` en `analisis/00_utils.R`; fallaba 5 de 5 veces |
| 2026-09-15 | En la BDIF, cuando un bloque de columnas se repite sin etiqueta, se conserva el primero (conteos) y se descarta el segundo (indicadores por 10 mil adultos). Los indicadores se recalculan en el panel. | `src/proyecto/limpieza/bdif.py` |
| 2026-09-29 | 🔴 **C1. El DENUE casi no se actualiza entre actualizaciones integrales.** Localidades tratadas que cambian de una versión a otra: 83.8% en 2019S2 y 83.0% en 2024S2, contra 8.7–15% en 2022; su stock crece +1.9% en 2019S2→2024S1 y +12.4% en 2024S2. El "nulo preciso" de la ventana escalonada era falta de medición. El DENUE pasa al diseño **entre actualizaciones** (s ∈ {1,7,8,17,18}, cohorte única g = 17, estimando ATT(17,18), placebo ATT(17,8)); la ventana escalonada queda como secundaria. | `outputs/tablas/desc_medicion_denue_*.csv`; preregistro abajo |
| 2026-09-29 | 🔴 **C2. Controles de localidad contaminados.** De 66,669 "nunca tratadas", 36,238 estaban en municipios que abrieron sucursal en la ventana y 24,586 en municipios "ya tratados" que abrieron más (413 de 487); solo 5,845 limpias. Control principal: sin sucursal propia y a ≥10 km de cualquier localidad con sucursal (`dist_bb_km`, 21,719 controles). | `panel.py::_exposicion_espacial`; `leer_panel(controles=)` |
| 2026-09-29 | 🔴 **C3. Cajeros y TPV valían 0 en todo el país antes de 2022T4** (`fillna(0)` de sectores que la BDIF no publica). Ahora un conteo solo se rellena desde el primer trimestre publicado; cajeros, TPV, transacciones, captación y crédito se estiman en el panel corto 2022T4–2024T4 (cohortes con ≥2 trimestres previos). | `panel.py::panel_municipio_trim`; `tests/test_paneles.py` |
| 2026-09-29 | Errores estándar **agrupados por municipio** (Liang–Zeger sobre la función de influencia) en todos los paneles y estimadores. El bootstrap agrupado de did 2.3 promedia la función de influencia por cluster y escala por el número de clusters: con municipios desiguales da ee ~10× mayor (11.05 contra 1.10). Se reporta como `ee_boot`. Orden de clusters verificado contra `did:::mboot`. | `02_cs_did.R::varianza_cluster`, `cluster_if` |
| 2026-09-29 | Covariables (P-5): `log_poblacion_2020`, `indice_marginacion_2020`, `banca_mun_2019` (BDIF) y `log1p_estab_previos` (2016S1). Se conserva el nivel previo: se mide 3.5 años y una actualización antes de la primera apertura, y la selección de sitios fue por niveles; la robustez lo quita. | `config/parametros.yaml` |
| 2026-09-29 | Denominador BDIF (P-6): población adulta **fija** en 2022T4; la serie de la CNBV salta en 2020T4 (p5 −20%, p95 +13%). | `panel.py`; `tests/test_paneles.py::test_denominador_bdif_fijo` |
| 2026-09-29 | Piso de 50 habitantes para **todas** las localidades (antes exentaba a las tratadas y la robustez "sin piso" era asimétrica). La robustez pasa a un piso simétrico de 1,000. | `panel.py::panel_localidad` |
| 2026-09-29 | Sun–Abraham en **posiciones** de periodo: por el hueco de 2023S1 la cohorte 16 no tenía periodo relativo −1 y fixest la normalizaba de forma arbitraria. BJS reporta el ATT global (antes el efecto en e = 0). CS se estima una sola vez por especificación. | `03_twfe_comparacion.R` |
| 2026-09-29 | Anillos fuera de la batería (fallan tendencias paralelas, se traslapan): quedan como descriptivo. Matching: exacto por estado × cabecera, Mahalanobis en logs, con reemplazo y caliper 1.0 → diferencia estandarizada máxima de 0.03–0.06 (antes 0.65), empareja ~50% de las tratadas; se estima CS sobre esa muestra. Goodman-Bacon en forma cerrada (bacondecomp no cabe en memoria), verificada contra bacondecomp en el panel municipal. | `matching.py`; `05_robustez.R` |
| 2026-09-30 | **Corrida final** (`make bateria`, 13 min). Financiera: nulo informativo (privadas +0.7%, IC90 ±2.4%; BM −0.2%; EACP +1.5%; pre-tendencias planas). DENUE: +10.4% en emprendimiento en la actualización 2024 (placebo n.s., Wald previa p = 0.057), robusto a radios, piso, matching y post 2025S1, pero sin gradiente por exposición, HonestDiD se rompe en M̄ = 1 y consumo y salud fallan la pre-prueba: evidencia sugestiva, no causal. | `outputs/tablas/tabla_final.csv`; CLAUDE.md §5.bis |

| 2026-09-30 | **Fase 0 (financiera, BDIF a 2025T4).** Primera etapa de inclusión fuerte: +1,268 contratos de captación y +2,412 tarjetas del banco por 10 mil adultos. Banca privada: nulo informativo (+0.5%, ±2.9%). EACP: captación nula (±2.5%), crédito al consumo +4.3% (RW p = 0.008). Desierto bancario sin diferencias. Heterogeneidad por marginación: sin covariables en los subgrupos sin controles suficientes (marcado). | `outputs/tablas/tabla_final.csv`, `het_q.csv` |
| 2026-09-30 | **Fase 1.** CE 2004–2024: unidades −0.9% (±4.0%), nulo informativo con 3 placebos planos y sin dosis. VACB +23 puntos log significativo pero aislado. IMSS: salario −1.9% (±3.6%), nulo informativo; empleo total no informativo. Remesas: reprueban la pre-prueba (descriptivo). ENIF: la tenencia de cuenta sube igual en lo rural y lo urbano en 2021–2024. | idem; `desc_enif_cuentas.csv` |
| 2026-09-30 | Resultados en logaritmo: el efecto, el MDE y la cota TOST se expresan en 100 × puntos log (antes se dividían entre la media del log, un error de la tabla final). | `07_inferencia.R` |
| 2026-09-30 | ENIF por **tabulados oficiales**: los microdatos 2024 no traen descriptor de variables y mapear preguntas a mano sería adivinar. | `utils/enif_descriptivo.py` |
| 2026-10-02 | **Verificado:** las actualizaciones integrales del DENUE del diseño son las de los Censos Económicos. La versión 11/2019 (s = 8, 2019S2) se actualizó por completo con los CE 2019 (5,447,591 establecimientos; comunicado 556/19 del 14 de noviembre de 2019) y la 11/2024 (s = 18, 2024S2) con los CE 2024 (6,058,548). Los CE recorren las áreas urbanas manzana por manzana, así que la incorporación de establecimientos en la actualización es mayor donde hay más área urbana. | [INEGI, DENUE 2019](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2019/OtrTemEcon/DENUE2019.pdf); [INEGI, DENUE 11/2024](https://inegi.org.mx/contenidos/saladeprensa/boletines/2024/denue/denue2024_11.pdf) |
| 2026-10-02 | **Diseños alternativos** (`make bateria-alternativos`, 25 s). *DiD apilado* (9 cohortes 2022T1–2024T1, 1,457 municipios, e ∈ [−8, 7]): sucursales privadas +0.8% (IC90 ±2.7%), banca múltiple +0.7% (±2.0%), EACP +0.8% (±4.1%) y captación de ahorro EACP −0.2% (±1.9%), todos con previos planos: el nulo financiero no depende del estimador. Primera etapa +2.00, igual que CS. **El crédito al consumo de las EACP (+3.9%) reprueba la pre-prueba** (Wald p < 0.001; los previos suben de −4.3 a 0 y la tendencia sigue): pasa a descriptivo. IMSS: puestos reprueban; salario −1.4% (ee 0.6%, previos planos), significativo pero dentro de ±5%. *Decaimiento espacial:* el +10% del DENUE no se concentra en la localidad con sucursal (propia +10.4%, 0–2 km +11.7%, 2–5 km +8.9%, 5–10 km +0.9%; propia − 0–2 km p = 0.53; propia − 5–10 km p = 0.006), y las bandas de 0–2 y 2–5 km reprueban la pre-prueba. La predicción preregistrada (mayor en la propia, previos planos) no se cumple: el patrón es de zona periurbana alrededor de la cabecera, compatible con la incorporación de los CE. *Intensidad:* 86% de los municipios abre una sola sucursal. | `outputs/tablas/apilado_resumen.csv`, `decaimiento_*.csv`, `desc_intensidad_municipal.csv` |
| 2026-10-02 | 🔴 **Hallazgo exploratorio (no preregistrado): el control del DENUE está en otro régimen de medición.** Los CE 2024 recorren manzana por manzana todas las cabeceras y las localidades de 2,500+ habitantes; el resto de lo rural va por muestra probabilística (INEGI, *CE 2024. Metodología*, 2025). El 82% de las localidades con sucursal está en el régimen de recorrido total contra el 2.2% de los controles a ≥10 km. En el régimen de muestra el DENUE casi no registra establecimientos (~2.5 por mil habitantes contra 62–85). Dentro del régimen de recorrido total (903 tratadas, 478 controles), la diferencia bruta de emprendimiento es +4.9 por mil en 2024S2 y +2.9 en el placebo 2019S2: el exceso neto es ≈ +2 por mil (~2.4% de la media), igual en las vecinas de 0–2 km. Siguiente paso: CS dentro del régimen de recorrido total, rotulado como exploratorio (resultado en la fila siguiente). | `analisis/01_descriptivos.R::medicion_por_regimen`; `outputs/tablas/desc_regimen_censal_*.csv` |
| 2026-10-02 | **Régimen censal, estimación formal (exploratoria).** Dentro del recorrido total (903 tratadas, 478 controles), emprendimiento +9.8% (ee 1.9%), previos planos (Wald p = 0.71), placebo +0.11 (ee 1.79) y HonestDiD M̄ = 1 [1.8, 15.1]. Con la regla fijada antes de estimar, **el régimen no explica el +10%**. El descriptivo bruto (exceso de ~2%) no ajustaba covariables. Consumo (+7.9%) y salud (+10.2%) reprueban la pre-prueba. Sigue siendo un efecto de zona: la localidad con sucursal ≈ vecinas a 0–2 km (p = 0.62) y ≈ 0 a 5–10 km. En el régimen de muestra rural (203 tratadas) el efecto es grande en % pero sobre bases mínimas. **Cierres (P-9):** sin los 41 municipios con cierres salen solo 2 tratados y el nulo financiero no cambia (privadas +0.0066, ee 0.0094). | `outputs/tablas/regimen_*.csv`, `rob_honest_localidad_act_regimen_total_*.csv`, `rob_municipio_trim_esc_*.csv` |
| 2026-10-03 | **Corrida final** (`make bateria`, 55 min, sin fallas). Reproduce exactamente todos los resultados vigentes: 77 especificaciones de la tabla final y 268 filas de la maestra con el mismo ATT, ee, Wald y Romano–Wolf. Solo cambian el `ee_boot` (bootstrap aleatorio de `did`), la variante sin cierres (P-9) ahora en todas las series de la BDIF (sin cambios) y los descriptivos con el panel hasta 2025T4. Se renderizan la metodología, el trabajo final y la presentación. | `outputs/logs/bateria_20261003_203153.log` |
| 2026-10-07 | **Fase 2, tratamiento observado (P-8 cerrada).** El modelo Power Pivot de `BD_Operativa_202607.xlsx` se lee con `pbixray`. Banco del Bienestar + Banjército coinciden con la banca de desarrollo de la BDIF en el 99.2% de 39,510 municipio-trimestres (2022T1–2025T4); Banjército se observa en 80 municipios en 2025T4 (la extrapolación suponía 75). Con G observado cambian 9 municipios (1 entra, 1 sale, 7 de cohorte; incluye 30 sucursal-trimestres en municipios nuevos que la BDIF aún no separa, recuperados en la revisión del 2026-10-08) y vuelven los 8 sospechosos. Ningún ATT financiero se mueve más de 0.73 ee (privadas +0.0081 contra +0.0066; primera etapa 1.995 contra 2.002). | `outputs/tablas/fase2_tratamiento_obs.csv` |
| 2026-10-07 | **Fase 2, VIIRS: sin más luz donde abre el banco, pero descriptivo.** Antes de estimar se corrigió la escala (×10 distinta antes y después de 2022) y se excluyeron los píxeles negativos (adenda del preregistro). Luz a 1 km: +0.3 puntos log (ee 0.9); la Wald previa falla (p = 0.0001), igual que en el margen extensivo, el anillo de 1–3 km, las tres bandas de vecinas y casi todas las variantes. Solo la comparación por calendario entre localidades con sucursal pasa la pre-prueba (p = 0.096) y da +0.15 (ee 0.83): nulo. El diagnóstico de ruptura muestra cambios año a año que dependen del brillo en todos los pasos (también 2016→2017), así que comparar pueblos iluminados con rancherías oscuras no es válido en luz nocturna. Dosis: estudio de evento e = 0, 1, 2 de +0.001, +0.007 y +0.042 (ee 0.04–0.23); por cohorte 2022 +0.020, 2023 +0.006, 2024 −0.007, ninguno significativo. | `fase2_viirs.csv`, `fase2_decaimiento_viirs_*.csv`, `fase2_rob_extra_viirs_*.csv`, `fase2_desc_viirs_ruptura.csv` |
| 2026-10-07 | **Fase 2, EIC 2015 / Censo 2020 / EIC 2025 (1,461 tratados contra 499).** El emprendimiento medido **en personas** no reproduce el +10% del DENUE: `pct_negocio` −1.2 puntos (ee 1.0; −4.2% de la media), con previos planos (p = 0.61), pero no informativo (cota de 10.1%); sin dosis (temprana −1.5, tardía −1.1, p = 0.77). Nulos informativos: ocupación (+1.2%, cota 3.1%) e ingreso por trabajo (+1.2 puntos log, cota 3.8). Empleadores +0.52 puntos (Romano–Wolf p = 0.069). Programas de gobierno +2.1 puntos, pero reprueba la pre-prueba (p = 0.013) → descriptivo. Población +2.3%, trabajo en otro municipio +2.2 puntos y celular −2.6 puntos: significativos sin corrección, ninguno sobrevive BH (q ≥ 0.11). Heterogeneidad por desierto bancario: no se interpreta, porque el grupo con banca múltiple previa tiene solo 21 controles. | `fase2_eic.csv`, `fase2_dosis_eic_*.csv`, `fase2_het_eic_*.csv`, `fase2_resumen.csv` |
| 2026-10-07 | **Fase 2, EFIPEM y ENOE: no informativos.** EFIPEM: impuestos −4.1 y derechos −6.4 puntos log (ee ~5), no significativos y no informativos; predial reprueba la pre-prueba. ENOE: solo 367 municipios están en los 27 trimestres (la muestra rota), y en la estimación quedan 146 tratados contra 12 controles; `pct_negocio` +2.1 puntos (ee 1.5, no significativo), informalidad +3.9 (ee 1.6; RW p = 0.035, BH q = 0.097, frágil: cambia de signo con cohortes de 30 o más); ingreso reprueba la pre-prueba. | `fase2_efipem.csv`, `fase2_enoe.csv`, `rob_municipio_enoe_esc_pct_negocio.csv` |
| 2026-10-08 | **Revisión del 2026-10-08 (descriptivo, no preregistrado).** *Calendario de aperturas:* año de apertura de los 1,457 municipios tratados contra las covariables previas estandarizadas y las sucursales privadas de 2019T1. Los más poblados abren 1.4 meses antes por de (1.7 con efectos fijos de estado; de del calendario 7.8 meses) y, dentro de cada estado, los más marginados 1.3 meses antes; R² 0.05 (0.15 con efectos fijos de estado), Wald conjunta p < 0.001. El nivel previo de sucursales privadas no predice la fecha dentro del estado. El orden no es aleatorio respecto de lo observable, pero son las covariables que condiciona el estimador DR. *Fase 2:* el cruce `left` del modelo Power Pivot perdía 30 sucursal-trimestres en 7 municipios nuevos; con `outer` cambian 9 municipios de G (antes 8) y ningún ATT financiero cambia. *Texto:* conclusiones con la cota correcta (±2.4% en sucursales privadas, ±5% en todas las series financieras principales), limitación de Banjército actualizada y la fase 2 en el cuerpo del trabajo. | `01_descriptivos.R calendario` → `outputs/tablas/desc_calendario_aperturas.csv`; `entregables/_tablas/tab_calendario.md` |
| 2026-10-11 | **Fase 3, A. Delitos (SESNSP; 1,457 municipios tratados contra 499): sin efecto detectable, no informativo.** Con previos planos (Wald p entre 0.13 y 0.89) el ATT es ≈ 0, pero el IC90 no descarta cambios de 12–50%: robo a transeúnte −0.2% (cota 19%), robo a negocio −22% (ee 13%, p = 0.10, Romano–Wolf 0.36), extorsión +9% (cota 50%), robo total −0.1% (cota 12%), homicidio doloso +0.1% (cota 21%). El placebo de denuncia (daño a la propiedad, +7.9%) tampoco se mueve. Robustez (G observado, pre-periodo desde 2017T1, piso de 5,000 habitantes, solo municipios con registro en 2019): mismo signo y tamaño. HonestDiD en robo a transeúnte (primeros 3 trimestres): IC original [−0.84, 0.04] por 100 mil, es decir [−32%, +2%]. El cluster estatal vuelve a romper la Wald con 19 previos (como en el DENUE). | `fase3_resumen.csv`, `rob_municipio_delitos_esc_*.csv`, `fase3_rob_extra_municipio_delitos_*.csv`, `rob_honest_municipio_delitos_esc_delitos_tasa_robo_transeunte.csv` |
| 2026-10-11 | **Fase 3, B. Elecciones (INE; 1,375 municipios contra 458): descriptivo, la pre-prueba falla.** Los placebos tienen vaivén: en participación −5.0 puntos en 2015→2018 y +3.6 en 2018→2021; en el bloque, −6.7 y +4.2 (Wald p < 0.001). Con el criterio fijado, ATT(4,4) de −2.9 puntos de participación y +0.9 de bloque son descriptivos. El vaivén coincide con la concurrencia local, que cambia por estado: el resultado neto de la media estado × elección sí pasa la pre-prueba (participación −1.4, ee 0.9, cota 4.5%, Wald p = 0.24; bloque +2.3, ee 2.1, p = 0.09). El TWFE con efectos fijos estado × elección da el signo contrario (+0.7, ee 0.4) con previos en el límite (p = 0.05). Sin dosis (temprana contra tardía, p ≥ 0.69). **No hay efecto electoral identificado.** *Ubicación (descriptivo):* dentro del estado, una desviación estándar más de voto del bloque en 2018 adelanta la apertura 0.7 meses (p = 0.01), contra 1.8 meses por desviación estándar de población; la desviación estándar del calendario es de 7.9 meses. **B2 (sección electoral) no se hizo:** con la pre-prueba municipal reprobada no aportaba identificación. | `fase3_resumen.csv`, `cs_previos_municipio_elecciones_*.csv`, `fase3_rob_extra_municipio_elecciones_*.csv`, `fase3_twfe_elecciones_*.csv`, `fase3_dosis_elecciones_*.csv`, `fase3_desc_ubicacion.csv` |
| 2026-10-12 | **Diagnósticos de la especificación financiera (descriptivo, no preregistrado; `analisis/12_diagnosticos.R`, `make diagnosticos`).** Se corrieron para que la descripción de la metodología solo prometa lo hecho. *Soporte común y balance del puntaje de propensión* (logit por cohorte contra los aún no tratados en el trimestre de apertura): las covariables separan a tratados y controles (AUC 0.66–0.86; diferencia estandarizada máxima sin ponderar 0.53–1.46, por población y marginación). Tras reponderar, las cohortes 2022T1–2023T3 quedan balanceadas (≤ 0.11), pero 2023T4 y 2024T1 no (0.23 y 0.38). 2024T1 solo se compara con los nunca tratados y tiene 4.8% de tratadas fuera del soporte. Sin esas dos cohortes (363 tratadas menos): sucursales privadas −0.4% (cota IC90 2.7%), banca múltiple −2.5% (cota 5.5%; previos p = 0.14), EACP +1.4% (cota 5.3%). El nulo no depende de las cohortes desbalanceadas, aunque los sectores pierden precisión. *Umbral de equivalencia en unidades:* ±5% de la media previa (0.929) = ±0.046 sucursales privadas por 10 mil adultos, unas 132 sucursales en los 28.4 millones de adultos de los municipios tratados. *Goodman-Bacon del TWFE estático:* 58.6% del peso en tratadas contra nunca tratadas, 29.5% en tempranas contra tardías y 11.9% en comparaciones prohibidas (tardías contra tempranas). TWFE +0.0091 contra CS +0.0066 en sucursales privadas. *Metodología:* reescrita como plan solo causal (se descarta la extensión predictiva de la propuesta), con los supuestos de anticipación y de ausencia de derrames, y lo que el diseño no puede decir. | `outputs/tablas/desc_soporte_comun.csv`, `desc_soporte_robustez.csv`, `bacon_municipio_trim_esc_*.csv`; `entregables/02_metodologia/metodologia.qmd` |

## Preregistro de la corrida final (2026-09-29)

Se fija **antes** de ver cualquier estimación con el código corregido. Lo que no esté aquí es
exploratorio y se reporta como tal. Motivo: la revisión del 2026-09-29 encontró tres problemas que
invalidan la conclusión vigente ("nulo preciso").

- **C1.** Dentro de la ventana 2019S2–2024S1 el DENUE casi no se actualiza. Las localidades tratadas
  crecen +1.9% en 4.5 años y en 2022 cambia ~10% de ellas por versión, contra +11 a +12% en cada
  actualización integral; el ATT(g,t) de 2022 tiene ee de 0.004.
- **C2.** El 91% de los controles de localidad estaba en municipios que abrieron una sucursal.
- **C3.** Cajeros y TPV valían 0 en todo el país antes de 2022T4.

**Especificación principal (DENUE).** Localidad, diseño entre actualizaciones integrales
(`estimacion.actualizaciones`), con estos periodos:

| s | Semestre | Papel |
|---|---|---|
| 1 | 2016S1 | antes |
| 7 | 2019S1 | antes |
| 8 | 2019S2 | actualización integral previa a todo tratamiento |
| 17 | 2024S1 | fin de la ventana |
| 18 | 2024S2 | actualización integral posterior |

- **Tratamiento.** Aperturas entre 2020S1 y 2024S1 en una sola cohorte `g = 17`.
- **Control.** Localidades sin sucursal propia a ≥10 km de cualquier localidad con sucursal. Se
  mantienen los filtros de siempre: piso de 50 habitantes para todas, sin fechas ambiguas, sin
  sospechosos de Banjército y sin ya tratadas.
- **Estimador.** Callaway y Sant'Anna DR con `log_poblacion_2020`, `indice_marginacion_2020`,
  `banca_mun_2019` y `log1p_estab_previos`; cluster por municipio; bootstrap multiplicador con 999
  réplicas.
- **Estimando principal.** ATT(17, 18).
- **Placebo.** ATT(17, 8), el salto de la actualización 2019S2. Si es distinto de cero, el diseño no
  identifica.

**Especificación principal (financiera).** Municipio trimestral 2019T1–2024T4, CS DR, aún no
tratados, cluster municipal. Resultados: sucursales privadas, de banca múltiple y de EACP por 10 mil
adultos, con el denominador fijo en 2022T4.

**Familias para Romano–Wolf** (`estimacion.familias_rw`), cada una con B = 9,999:
- DENUE-localidad: 9 resultados de emprendimiento, consumo y salud.
- Financiera: 3 resultados.

El resto de la batería lleva q-values de Benjamini–Hochberg, incluidas las diferencias de
heterogeneidad.

**Nulo informativo.** Solo se afirma si el IC al 90% cae dentro de **±5%** de la media previa de las
tratadas (TOST al 5%); siempre se reportan el MDE80 = 2.80·ee y la cota del IC90 como porcentaje de
esa media. Referencia: Bruhn y Love (2009) estiman +7.6% en dueños de negocio informal.

**Secundarias y robustez.** No cambian la conclusión principal; se reportan todas.
- Diseños alternativos para los 3 principales: ventana escalonada 2019S2–2024S1 con 4 estimadores;
  panel completo con CS; panel completo con BJS y SA con efectos fijos semestre × decil de tamaño.
- Controles alternativos: ≥5 km, ≥20 km, municipal limpio, todos los G=0 y solo localidades con
  sucursal (dosis temprana contra tardía).
- Derrame a menos de 10 km.
- Covariables: sin nivel previo y sin covariables. Piso simétrico de 1,000. Post en 2025S1.
  Incluir fechas ambiguas. Cluster por estado.
- HonestDiD con base universal para las principales.
- Heterogeneidad por desierto bancario (BDIF), marginación, tamaño y exposición.
- Matching con CS sobre la muestra emparejada.
- BDIF: primera etapa (sucursales totales), corresponsales 2021T1–2023T4 y panel corto 2022T4–2024T4
  (captación, crédito, cajeros, TPV y transacciones).

## Preregistro de la ampliación financiera — fase 0 (2026-09-30)

Se fija antes de estimar cualquiera de estas especificaciones. Vuelve al eje de la propuesta
original: ¿la sucursal incrementó la actividad financiera del municipio y fue mayor el efecto donde
no había banca? No modifica el preregistro anterior. Las especificaciones ya registradas conservan
su ventana 2019T1–2024T4, y su extensión a 2025T4 es una variante.

- **Panel.** Municipio trimestral de la BDIF de 2019T1 a 2025T4 (`periodo.fin_trimestral`);
  denominador fijo en 2022T4. Mismo estimador que la especificación financiera principal: CS DR con
  aún no tratados, cluster municipal y ee de Liang–Zeger.
- **EACP largas (familia de Romano–Wolf `eacp`), ventana 2019T1–2025T4.** Contratos por 10 mil
  adultos de SOCAP + SOFIPO (serie `eacp` de la BDIF, continua desde 2016): captación de ahorro, a
  plazo y a la vista, crédito al consumo y a la vivienda, y tarjetas de débito.
- **Inclusión total (efecto mecánico del banco adentro), ventana 2019T1–2025T4.** Captación de ahorro
  y a plazo y tarjetas de débito de la banca (múltiple + desarrollo), y cuentas en celular de todos
  los sectores.
- **Primera etapa de inclusión, ventana 2022T4–2025T4.** Captación total, tarjetas de débito y cuentas
  en celular de la banca de desarrollo (Banco del Bienestar + Banjército). Es una validación, no una
  hipótesis: queda fuera de BH. *Enmienda del mismo día, antes de estimar:* las cuentas en celular
  de la banca de desarrollo valen cero en todos los municipios y trimestres (el banco no las reporta)
  y salen.
- **Extensiones a 2025T4** (variantes `hasta_2025` y `panel_corto_2025`): sucursales privadas, de
  banca múltiple y de EACP; captación, crédito, cajeros, TPV y transacciones privadas.
- **Heterogeneidad (pregunta 2 de la propuesta).** Desierto bancario (sin banca múltiple en el
  municipio en 2019T1), marginación y tercil de población, en sucursales privadas, de banca múltiple
  y de EACP, y en captación de ahorro y crédito al consumo de EACP. BH sobre las diferencias.
- **Robustez.** Las variantes escalonadas de siempre, más el pre-periodo desde 2016 (panel largo)
  para EACP y sucursales de EACP. La banca múltiple 2016–2018 no, por el escalón de Compartamos. Más
  HonestDiD con base universal.
- **Criterios.** Nulo informativo = no significativo y el IC90 dentro de ±5% de la media previa de
  las tratadas. Una serie cuya pre-prueba falle (Wald p < 0.05) se reporta como descriptiva. Riesgo
  conocido: la captación a la vista de SOFIPO crece por las fintech digitales.

## Preregistro de la fase 1 — actividad medida de forma continua (2026-09-30)

Se fija antes de estimar. Objetivo: decidir si el +10% del DENUE en la actualización de 2024 es real
o es sesgo de medición, con fuentes que no dependen de las actualizaciones del padrón.

- **Excepción controlada a la regla 6 (autorizada el 2026-09-30).** El IMSS (catálogo de municipios
  propio) y Banxico (series nombradas) no traen la clave INEGI. Se cruzan por nombre solo dentro de
  cada entidad, con nombres normalizados. Se acepta el exacto, la contención única y el difuso con
  margen; hay correcciones manuales versionadas (`config/cruces_municipios.yaml`) y los homónimos
  quedan pendientes. Resumen auditable en `docs/diccionarios/cruce_municipios_{imss,banxico}.md`.
  Remesas: 5 series sin cruzar (0.22% del monto). IMSS: pendientes las alcaldías de la CDMX, que
  vienen sin nombre en el catálogo y de todos modos son ya tratadas, y los homónimos de Oaxaca.
- **IMSS (familia de Romano–Wolf `imss`), municipio trimestral 2019T1–2025T4, CS escalonado.**
  Especificación financiera. Resultados: puestos afiliados por 10 mil adultos, puestos en registros
  de 1–5 puestos (microempresa formal) y de 6–50, y log del salario diario promedio.
- **Censos Económicos 2004–2024 (familia `ce`).** Una cohorte: primera sucursal entre 2019T2 y 2023T4
  (expuesta en el año de referencia del CE 2024), fechada en el último censo. Las aperturas de
  2024–2025 salen por exposición parcial y los ya tratados salen como siempre. Controles: nunca
  tratados hasta 2025T4. Estimando: ATT en el CE 2024; placebos: 2004→2009, 2009→2014 y 2014→2019.
  Resultados: unidades económicas y personal ocupado por mil habitantes (Censo 2020 fijo), y log de
  remuneraciones, VACB y producción bruta. **Prueba de dosis:** aperturas hasta 2022T2 contra
  2022T3–2023T4; un efecto real debe ser mayor con más exposición.
- **Remesas (Banxico CE166).** Dólares por adulto, CS escalonado 2019T1–2025T4. Una sola serie, fuera
  de familia (BH).
- **Heterogeneidad.** Dosis y desierto bancario en los CE; desierto bancario en el IMSS.
- **Robustez y HonestDiD** para puestos totales y micro del IMSS, remesas, y unidades y personal de
  los CE.
- **Criterios.** Los mismos: nulo informativo con IC90 dentro de ±5%; una pre-prueba fallida (Wald
  p < 0.05) vuelve descriptivo el resultado. Los datos abiertos de los CE no traen acceso a
  financiamiento (solo están en tabulados especiales), así que esa variable no entra.
- **ENIF** (2018, 2021 y 2024): solo descriptiva.

## Preregistro de los diseños alternativos (2026-10-02)

Se fija antes de la corrida (`make alternativos`). No modifica los preregistros anteriores ni la
tabla final: son contrastes de identificación, sin familia de Romano–Wolf ni BH propios (como TWFE,
Sun–Abraham y BJS). **Transparencia:** las pruebas de humo del mismo día corrieron emprendimiento por
bandas y dos series apiladas (sucursales privadas y salario del IMSS) con los parámetros ya fijados en
`config/parametros.yaml` (`estimacion.bandas_derrame_km`, `estimacion.apilado`). No se cambió nada
después, salvo la escala del contraste entre bandas: se fija en % de la media previa de cada banda,
porque en niveles no se comparan (la base va de ~13 establecimientos por mil en las vecinas a ~70
en las localidades con sucursal).

**1. DiD apilado** (Cengiz, Dube, Lindner y Zipperer 2019; pesos de Wing, Freedman y Hollingsworth
2024; `analisis/08_disenos_alternativos.R`).
- **Panel.** Municipio trimestral 2019T1–2025T4, con los mismos filtros que la especificación
  financiera: sin ya tratados, sin sospechosos de Banjército, cohortes de 5 o más.
- **Pilas.** Una por cohorte con ventana de evento balanceada e ∈ [−8, 7] (`k_pre` = 8, `k_post` = 7):
  entran las 9 cohortes 2022T1–2024T1 (t = 13…21). La ventana post de 7 trimestres es la mayor que
  conserva la cohorte de 2024T1.
- **Controles limpios.** Nunca tratados hasta 2025T4 y aún no tratados al cierre de la ventana
  (G > g + 7). Variante: solo nunca tratados.
- **Pesos.** Los controles de la pila a pesan Q_a = (N^D_a / N^D) / (N^C_a / N^C).
- **Regresión.** y ~ Σ_{e≠−1} δ_e · 1{tratada}·1{e}, con efectos fijos de unidad × pila y de evento,
  ponderada, sin covariables (contraste transparente del CS doblemente robusto) y con ee agrupados
  por municipio.
- **Estimando y pre-prueba.** Estimando: el promedio de δ_0 … δ_7. Pre-prueba: la Wald conjunta de
  δ_−8 … δ_−2.
- **Resultados y su comparación con CS.**

  | Resultados | CS de referencia |
  |---|---|
  | Sucursales privadas, de banca múltiple y de EACP | `hasta_2025` |
  | Sucursales totales | primera etapa |
  | Captación de ahorro y crédito al consumo de EACP | `eacp` |
  | Puestos IMSS totales, micro y log del salario | `imss` |

- **Lectura.** Si el apilado coincide en signo y magnitud con CS, el resultado no depende de cómo CS
  agrega las cohortes ni de las covariables; las discrepancias se reportan tal cual. Criterios de
  siempre: nulo informativo con IC90 dentro de ±5%; Wald previa p < 0.05 → descriptivo.

**2. Decaimiento espacial en el DENUE** (reemplaza a los anillos con identificación).
- **Diseño.** Localidad, entre actualizaciones, ATT(17, 18) con placebo ATT(17, 8). Las localidades
  sin sucursal se parten por banda de distancia a la sucursal más cercana: [0, 2), [2, 5) y [5, 10)
  km. Cada banda va fechada con la G de esa sucursal y se compara contra los mismos controles a
  ≥10 km; la "banda" de la localidad con sucursal propia es la especificación principal.
- **Resultados.** Emprendimiento, consumo y salud (los tres principales).
- **Contrastes.** Sucursal propia − 0–2 km, sucursal propia − 5–10 km y 0–2 km − 5–10 km, en % de la
  media previa de cada banda. La covarianza es la agrupada por municipio de las funciones de
  influencia, porque las bandas comparten controles y municipios.
- **Predicción.** Un efecto de la sucursal debe ser mayor en la localidad con sucursal y caer con la
  distancia hasta ≈ 0, con previos planos en cada banda. Un perfil plano (el mismo % en todas las
  bandas) señala un choque regional o de incorporación del padrón que el control lejano no absorbe.
  Una banda con Wald previa p < 0.05 se reporta como descriptiva.

**3. Intensidad municipal** (descriptivo). Sucursales del banco por municipio tratado y por 10 mil
adultos al cierre de 2024T4: justifica el tratamiento binario.

## Análisis exploratorio: régimen censal y cierres (2026-10-02)

**No es preregistro.** Se decidió después de ver el descriptivo `medicion_por_regimen()` (fila del
2026-10-02 en "Tomadas") y se reporta como exploratorio. Se fija antes de estimar para no elegir
la especificación con los resultados.

- **Régimen censal** (`08_disenos_alternativos.R regimen`). Misma especificación principal del
  DENUE (entre actualizaciones, CS DR, covariables de siempre, controles a ≥10 km, cluster
  municipal), estimada **dentro** de cada régimen de levantamiento de los CE: recorrido total
  (cabecera o 2,500+ habitantes del Censo 2020) y muestra rural.
  - *Qué se estima.* En cada régimen: la localidad con sucursal y las bandas de 0–2, 2–5 y 5–10 km,
    con placebo 2019S2 y Wald previa. Además, la diferencia de la localidad con sucursal entre
    regímenes (en % de cada media) y HonestDiD dentro del recorrido total.
  - *Resultados.* Emprendimiento, consumo y salud.
  - *Lectura fijada antes de estimar.* Si dentro del recorrido total el efecto queda dentro de ±5%
    o reprueba la pre-prueba, el +10% de la especificación principal se atribuye a la diferencia de
    régimen de medición entre tratadas y controles. Si se sostiene cerca de +10% con previos planos
    y HonestDiD no se rompe en M̄ = 1, el régimen no lo explica.
- **Cierres (P-9)** (`05_robustez.R cierres`). Variante del diseño escalonado de la BDIF sin los
  municipios que vuelven a cero sucursales netas de Banjército después de abrir (41 en 2019T1–2025T4),
  para los tres resultados financieros principales; en la corrida completa entra en todas las series
  de `municipio_trim`.

## Preregistro de la fase 2 — fuentes nuevas (2026-10-07)

Se fija **antes** de construir los paneles y de estimar. Sale del ranking de
`docs/contexto/fuentes_panel_candidatas.md`. **Transparencia:** antes de escribir esto solo se
vieron diccionarios, estructura de archivos y conteos de cobertura (municipios en muestra,
categorías), nunca un resultado. Nada de esto toca los preregistros anteriores, la maestra, la
tabla final ni sus familias de Romano–Wolf: son contrastes nuevos con familias propias, como los
diseños alternativos del 2026-10-02 (`analisis/10_fase2.R`, salidas `fase2_*`).

**Criterios (los de siempre).**
- Una pre-prueba fallida (Wald previa p < 0.05) vuelve descriptivo el resultado.
- Nulo informativo = no significativo y el IC90 dentro de ±5% de la media previa de las tratadas.
  En logaritmos son ±5 puntos log.
- Romano–Wolf dentro de cada familia de la fase 2 y BH sobre todas las especificaciones de la fase.

### 1. Tratamiento observado 2022–2026: modelo Power Pivot del Portafolio CNBV (P-8)

- **Fuente.** `data/raw/cnbv_portafolio/BD_Operativa_202607.xlsx`, ya descargado.
  - Su modelo de datos (`xl/model/item.data`) se lee con `pbixray` 0.15.5.
  - Tabla `FT_datos`: periodo mensual 2022-01–2026-07 × institución × municipio × tipo de dato.
  - Claves: Banco del Bienestar = `037166`, Banjército = `037019`, sucursales = tipo 31.
- **Validación (descriptiva).** Banco del Bienestar + Banjército, en el mes de cierre de cada
  trimestre, contra las sucursales de banca de desarrollo de la BDIF por municipio y trimestre,
  2022T1–2025T4: % de coincidencia exacta.
- **Tratamiento alterno `G_obs`.**
  - Igual que `G`, pero la serie 2022+ es el Banco del Bienestar **observado** en el modelo, no
    la BDIF menos el Banjército extrapolado de 2021-12.
  - Hasta 2021T4 se usa la serie de siempre.
  - Se reportan cuántos municipios cambian de G.
- **Robustez.**
  - Con `G_obs` se reestiman los 3 resultados financieros principales (escalonado 2019T1–2024T4),
    su variante `hasta_2025` y la primera etapa.
  - En esta variante los sospechosos de Banjército **entran**: ya no hay residual que excluir.
- **Lectura.** Si los ATT se mueven menos de 1 ee, P-8 se cierra sin efecto.

### 2. Encuesta Intercensal 2015, Censo 2020 (cuestionario ampliado) y EIC 2025

- **Panel `municipio_eic`.** Municipio estable (crosswalk P-7) × 3 cortes:
  - t = 1: EIC 2015;
  - t = 2: Censo 2020, referencia 15 de marzo de 2020;
  - t = 3: EIC 2025, levantada del 6 de octubre al 14 de noviembre de 2025.
- **Agregación.** Microdatos por estado, agregados por municipio con `FACTOR`. El crudo no se
  conserva (streaming, hash en MANIFEST).
- **Tratamiento.** Primera sucursal (`G_trimestre`, serie de siempre) entre 2020T2 y 2025T3 → G = 3.
  - Salen las aperturas de 2019T2–2020T1 (ya expuestas en el Censo 2020) y las de 2025T4 (sin
    exposición en la EIC).
  - Controles: nunca tratados hasta 2025T4.
  - Salen ya tratados y sospechosos, como siempre.
  - Dosis: temprana (hasta 2022T2) contra tardía (2022T3–2025T3).
- **Resultados.** Proporciones en %.
  - Personas de 12 años y más:
    - `pct_negocio`: patrón o cuenta propia entre los ocupados con posición especificada. Es el
      análogo de los dueños de negocio de Bruhn y Love y mide emprendimiento **sin el padrón**:
      **principal**.
    - `pct_cuenta_propia` y `pct_empleador`.
    - `pct_ocupacion`: ocupados entre la población de 12+.
    - `log_ingreso_trabajo`: media del log del ingreso mensual por trabajo de los ocupados con
      ingreso especificado y positivo.
  - Mecanismo:
    - `pct_hog_programas`: viviendas que reciben dinero de programas de gobierno.
    - `pct_hog_remesas`: viviendas que reciben dinero de otro país.
    - `pct_viv_internet` y `pct_viv_celular`.
    - `pct_trabaja_otro_mun`: ocupados que trabajan fuera de su municipio (reubicación).
    - `log_poblacion_est`: suma de `FACTOR`; prueba de "se ubicó donde se esperaba crecimiento".
- **Armonización de códigos (verificada en los descriptores).**
  - Ocupado: 2015 `CONACT` 10–16; 2020 y 2025, 10–20.
  - Posición en el trabajo: `SITUACION_TRAB` (2015) y `SITTRA`, con 4 = patrón y 5 = cuenta
    propia; 9 y vacío fuera.
  - Celular: sí = 3 en 2015 y 5 después.
  - Internet: sí = 5 en 2015 y 7 después.
  - `INGR_*` igual en los tres: programas 5/6, remesas 1/2.
- **Estimación.** CS DR (`notyettreated`, que con una sola cohorte equivale a nunca tratados) con
  las covariables previas disponibles: `log_poblacion_2020`, `indice_marginacion_2020` y
  `banca_mun_2019`. Cluster municipal.
  - *Estimando:* ATT(3,3).
  - *Placebo y pre-prueba:* ATT(3,2), el cambio 2015→2020.
- **Familias.** Romano–Wolf `eic`: `pct_negocio`, `pct_cuenta_propia`, `pct_empleador`,
  `pct_ocupacion` y `log_ingreso_trabajo`. Mecanismo: BH.
- **Robustez.** Sin covariables; dosis temprana contra tardía; heterogeneidad por desierto
  bancario; HonestDiD (un solo previo, informativo apenas).
- **Advertencia fijada de antemano.** Entre 2020 y 2025 los hogares con programas pasaron de 25% a
  41% en todo el país, así que `pct_hog_programas` mide la cobertura **diferencial** donde abrió el
  banco. Las encuestas son muestras: los ee agrupados absorben el error de muestreo como varianza
  residual.

### 3. Luz nocturna VIIRS anual (localidad 2016–2024)

- **Fuente.** VNL V2 anual de EOG redistribuido sin cuenta en Zenodo (registro 17294744, CC-BY):
  `nightlights.average_viirs.v21_m_500m_s_<año>…tif`, 2016–2024. Los crudos se conservan en
  `data/raw/viirs/`.
- **Panel `localidad_viirs`.** El mismo marco, los mismos filtros, la misma exposición espacial y
  las mismas covariables que `panel_localidad`; t = año − 2015.
- **Tratamiento anual.** Apertura en el semestre 1 de un año → G = ese año; en el semestre 2 → el
  año siguiente (el compuesto anual promedia los 12 meses). `G_vecina` anual con la misma regla
  para la sucursal más cercana. Controles: aún no tratados y lejanos, a 10 km o más.
- **Resultados.**
  - `log1p_luz_1km`: log(1 + suma de radiancia de los píxeles con centro a ≤ 1 km del punto de la
    localidad). **Principal.**
  - `luz_1km_pos`: 1{radiancia > 0}, el margen extensivo.
  - `log1p_luz_anillo`: anillo de 1–3 km, que excluye el núcleo y con él la luz de la propia
    sucursal.
- **Estimación.** CS DR escalonado con las covariables previas del proyecto.
  - *Estimando:* ATT global.
  - *Pre-prueba:* Wald de los e < 0.
  - *Dosis:* estudio de evento e = 0…4 y ATT por cohorte.
  - *Decaimiento:* vecinas sin sucursal a 0–2, 2–5 y 5–10 km contra los mismos controles, con los
    contrastes de `08_disenos_alternativos.R`.
  - Familia Romano–Wolf `viirs`: los tres resultados.
- **Robustez.** Las variantes escalonadas de siempre (anticipación 1, nunca tratados, sin
  covariables, cohortes ≥ 30, fechas ambiguas, cluster estatal, controles todos y solo con
  sucursal), HonestDiD y el régimen de recorrido total.
- **Lectura fijada.**
  - Efecto con previos planos que decae con la distancia: actividad local real.
  - Nulo informativo: el +10% del DENUE no viene con más luz, lo que refuerza la lectura de
    medición.
  - Pre-prueba fallida: descriptivo.

**Adenda del 2026-10-07, antes de estimar VIIRS (corrección de datos, no de especificación).**

- **Escala.** Los GeoTIFF de Zenodo no son homogéneos.
  - En 2016–2021 el entero almacenado es 10 × radiancia, sin etiqueta de escala (CDMX 2021 =
    1,200).
  - En 2022–2024 es la radiancia entera, con `scale = 10` (CDMX 2022 = 133).
  - Leída sin corregir, la luz nacional caía 10× en 2022. Se corrige con radiancia =
    entero × escala / 10.
  - Los años con precisión de 0.1 nW se redondean al entero (`fase2.viirs.armonizar_precision`),
    para que el margen extensivo no cambie de definición. Luz nacional a 1 km, ya corregida:
    2.83 M (2021) → 2.91 M (2022) → 3.23 M (2023) → 3.57 M (2024).
- **Ruptura de producto.** Según el `TIFFTAG_DOCUMENTNAME`:
  - 2022 es el VNL **v2.2 de dos satélites** (`npp-j01`);
  - 2023 y 2024 son el VNL v2 de SNPP;
  - 2016–2021 no traen la etiqueta (VNL V2 según Zenodo).

  Un cambio común en 2022 lo absorben los efectos de tiempo. Pero si afecta distinto a pueblos
  iluminados que a rancherías oscuras, sesga la comparación. La pre-prueba lo detecta en parte: los
  previos de las cohortes 2023 y 2024 cruzan 2021→2022. **Diagnóstico agregado (exploratorio):**
  cambio de log(1 + luz) 2021→2022 y 2022→2023 entre los controles, por decil de luz de 2021. Si
  el cambio de producto pesa distinto por brillo, VIIRS se lee como no informativo aunque la
  pre-prueba pase.

### 4. EFIPEM municipal (anual 2016–2024)

- **Tratamiento.** G anual con la regla de los semestres: T1–T2 → ese año; T3–T4 → el siguiente.
- **Resultados.**
  - `log_impuestos_pc`: capítulo "Impuestos" de los ingresos.
  - `log_predial_pc`: partida del impuesto predial.
  - `log_derechos_pc`: capítulo "Derechos".
  - Pesos por habitante del Censo 2020; logaritmos de valores positivos.
- **Estimación.** CS DR escalonado sobre los municipios que reportan en todos los años de la
  ventana (panel balanceado; se reporta cuántos quedan).
  - Familia Romano–Wolf `efipem`: los tres resultados.
  - 2025 (preliminar) no entra.

### 5. ENOE (municipio trimestral 2019T1–2025T4) — solo si el tiempo alcanza

- **Agregación.** Tabla SDEM por municipio (`ent` + `mun`) y trimestre, ponderada con el factor
  trimestral, para la población de 15+.
- **Resultados.**
  - `pct_negocio`: empleadores y cuenta propia (`pos_ocu` 2 y 3) entre los ocupados.
  - `pct_informal`: sector informal (`tue2`).
  - `pct_ocupacion`.
  - `log_ingreso`: media del log de `ingocup` > 0.
- **Exclusiones.** 2020T2 (levantamiento telefónico) sale de todas las unidades. Entran solo los
  municipios observados en todos los trimestres.
- **Estimación.** G trimestral de la BDIF; CS DR escalonado y aún no tratados.
  - Familia Romano–Wolf `enoe`.
  - Es la réplica más cercana a Bruhn y Love (2014).

## Preregistro de la fase 3 — delitos y elecciones (2026-10-11)

Se fija **antes** de construir los paneles y de estimar. Origen: dos ideas del equipo (incidencia
delictiva y elecciones federales), filtradas por viabilidad y diseño. **Transparencia:** antes de
escribir esto solo se vieron encabezados, catálogos de categorías, tipos de casilla, estatus de
acta, cobertura de municipios por año y el calendario de aperturas de `panel_municipio_trim`;
ningún resultado cruzado con el tratamiento. Nada de esto toca los preregistros anteriores, la
maestra, la tabla final ni sus familias. Son contrastes nuevos con familias propias
(`analisis/11_fase3.R`, salidas `fase3_*`).

**Criterios (los de siempre).**
- Pre-prueba fallida (Wald previa p < 0.05) → descriptivo.
- Nulo informativo: no significativo y el IC90 dentro de ±5% de la media previa de las tratadas. En
  porcentajes es el 5% de la media, no 5 puntos: con una participación de ~55%, ±2.75 puntos.
- Romano–Wolf dentro de cada familia de la fase 3 y BH sobre todas sus especificaciones. MDE80 y
  cota del IC90 siempre.

### A. Incidencia delictiva municipal (SESNSP)

- **Fuente.** `data/manual/sesnsp/Municipal-Delitos-2015-2025_ago2026.zip`, el enlace "2015 - 2025
  (Fuero Común - Delitos). Incidencia delictiva municipal" de
  <https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva>.
  - Se usa el CSV consolidado (latin-1): `Año, Clave_Ent, Entidad, Cve. Municipio, Municipio,
    Bien jurídico afectado, Tipo de delito, Subtipo de delito, Modalidad, Enero…Diciembre`.
  - La clave municipal es la del INEGI sin el cero inicial (`1001` = `01001`), así que no hace
    falta unir por nombre.
  - Salen las claves `…998`/`…999` ("No especificado", "Otros municipios").
  - La metodología nueva (RNID, 2026) está en archivos aparte y no entra.
- **Cobertura vista.** 1,931 municipios en 2015–2016 y 2,466–2,486 desde 2017. El pre-periodo
  extendido empieza en **2017T1**, no en 2015, por la regla 10.
- **Panel `municipio_delitos`.** Municipio estable (P-7) × trimestre 2019T1–2025T4 (t = 1…28).
  - `G`, banderas y covariables son las de `panel_municipio_trim`, el mismo tratamiento que el
    bloque financiero.
  - Meses → trimestres con `sum(min_count=1)`.
  - Tasas por 100 mil habitantes con denominador **fijo**: población del Censo 2020 (`pobtot`).
- **Resultados.** Carpetas de investigación por 100 mil habitantes.
  - Familia Romano–Wolf `delitos`:
    - `tasa_robo_transeunte`: robo a transeúnte en vía pública + en espacio abierto al público.
      **Principal**: es el canal del efectivo de los programas.
    - `tasa_robo_negocio`: robo a negocio.
    - `tasa_extorsion`: extorsión.
    - `tasa_robo_total`: todos los subtipos del tipo "Robo".
    - `tasa_homicidio_doloso`: homicidio doloso, el de menor cifra negra.
  - Secundario con BH: `tasa_dano_propiedad`, placebo de denuncia. Si sube igual que los robos, lo
    que cambia es el registro, no la incidencia.
  - "Robo a cuentahabiente" no existe en el catálogo nacional. "Robo a institución bancaria" sí,
    pero es demasiado raro; queda fuera.
- **Estimación.** CS DR escalonado, aún no tratados, covariables `log_poblacion_2020`,
  `indice_marginacion_2020` y `banca_mun_2019`, cluster municipal.
  - *Estimando:* ATT global.
  - *Pre-prueba:* Wald de los e < 0.
  - *Hipótesis bilateral:* el efectivo atrae robos; la Guardia Nacional y la obra militar los
    disuaden.
- **Robustez.**
  - Las variantes escalonadas de siempre (`robustez_escalonado`).
  - Tratamiento observado (P-8, modelo Power Pivot).
  - Pre-periodo extendido desde 2017T1.
  - Piso de 5,000 habitantes.
  - Solo municipios con algún robo registrado en 2019: el municipio de registro (agencia del MP)
    no siempre es el de ocurrencia.
  - HonestDiD en `tasa_robo_transeunte`.

### B. Elecciones federales de diputados de mayoría relativa (INE)

- **Fuente.** INE, SICEE (<https://sicee.ine.mx/downloadzip>):
  `DIPUTACIONES_FED_MR_{2015,2018,2021,2024}.zip`, archivo `*_NAL_CAS.csv` (casilla).
  - Columnas: `ID_ESTADO`, `ID_MUNICIPIO` (clave **INE**), `MUNICIPIO`, `SECCION`, tipo de casilla
    (`TIPO_CASILLA`; en 2015, la letra de `CASILLA`), votos por partido y por combinación de
    coalición, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL` y
    `ESTATUS_ACTA`.
  - Codificación mixta: UTF-8, con 1,505 líneas en latin-1 en 2024. Se decodifica línea por línea.
  - Datos del datatón: no se usan.
- **Casillas que entran.** Básicas, contiguas y extraordinarias.
  - Salen las especiales (`S`, `SMR`: votan sin lista nominal) y las mesas sin sección (`P` en
    2021, `A` en 2024).
  - Salen también las casillas no instaladas, con paquete no entregado o no recibido y las de
    votación suspendida, del numerador y del denominador.
- **Clave INE → INEGI.** `cruce_nombres.cruzar()` dentro de la entidad (excepción controlada a la
  regla 6, como el IMSS):
  - correcciones en `config/cruces_municipios.yaml` (`ine:`);
  - diccionario en `docs/diccionarios/cruce_municipios_ine.md`;
  - colapso P-7.
  - La clave INE de cada municipio debe ser estable entre elecciones; lo que no cruce se reporta.
- **Panel `municipio_elecciones`.** Municipio estable × {2015, 2018, 2021, 2024}, t = 1…4.
  - **Una cohorte, G = 4:** primera sucursal entre 2021T3 y 2024T1 (entre la elección del
    6-jun-2021 y la del 2-jun-2024).
  - Fuera por exposición (`apertura_posterior_ce`): aperturas 2019T2–2021T2 y 2024T2. 2021T2 y
    2024T2 son ambiguas porque la BDIF reporta al cierre del trimestre; en el calendario no hay
    ninguna apertura en esos dos trimestres.
  - Controles: sin sucursal hasta 2024T2 (nunca tratados + aperturas desde 2024T3).
  - Ya tratados y sospechosos salen como siempre.
  - Dosis: temprana (2021T3–2022T4) contra tardía (2023T1–2024T1).
- **Resultados (%).**
  - Familia Romano–Wolf `elecciones`:
    - `pct_participacion`: votos / lista nominal.
    - `pct_bloque_gobierno`: Morena + PT + PVEM sobre la votación válida (partidos, combinaciones
      e independientes; sin nulos ni no registrados).
      - La **composición es fija** en las cuatro elecciones: la de las coaliciones de 2021 y 2024.
      - Los votos por combinación se reparten por igual entre los partidos de la combinación (regla
        del INE, sin redondeo), también cuando mezclan bloque y no bloque (PRI_PVEM en 2015 y
        2018).
      - *Por qué fijo:* el bloque "de cada elección" metería al PVEM en 2021, dentro del
        pre-periodo, con un peso que varía por región.
  - Secundarios con BH:
    - `pct_morena`: Morena sola, con su parte de las combinaciones.
    - `pct_nulos`: nulos / votos.
- **Estimación.** CS DR con las mismas covariables y cluster municipal.
  - *Estimando:* ATT(4,4), el cambio 2021→2024 contra los controles.
  - *Placebos:* ATT(4,2) y ATT(4,3), más la Wald conjunta.
- **Robustez.**
  - TWFE con efectos fijos de municipio y de estado × elección (fixest), estudio de evento con base
    2021. Con una sola cohorte no hay comparaciones prohibidas, y los efectos fijos absorben la
    concurrencia con elecciones locales, que cambia por estado y año.
  - Resultado neto de la media estado × elección.
  - Sin covariables; con el nivel de 2015 del resultado como covariable; tratamiento observado
    (P-8).
  - Dosis temprana contra tardía; HonestDiD (2 previos).
- **Diagnóstico descriptivo (no es estimación causal).** Entre los municipios tratados, la fecha
  de apertura contra la participación y el voto del bloque en 2018, sin y con efectos fijos de
  estado, como `01_descriptivos.R calendario`: ¿abrió primero donde el bloque ya era fuerte?
- **Lectura fijada.**
  - Pre-prueba fallida: descriptivo.
  - Efecto con previos planos: asociación de la apertura con el voto, que **no distingue** la
    sucursal de la obra militar ni de la entrega de programas en el mismo lugar.
  - Nulo informativo: la apertura no movió la participación ni el voto más allá de ±5%.
- **B2, exploratoria (solo si sobra tiempo).** Sección electoral con bandas de distancia a la
  sucursal (0–2, 2–5, 5–10 km contra ≥10 km). Se escribe su adenda antes de estimarla.

**Adenda del 2026-10-11, antes de estimar (datos, no especificación).** Se escribió al construir los
paneles, viendo solo listas nominales, conteos y cruces de claves.

- **Cruce INE → INEGI.**
  - El INE **reasigna** claves de municipio: en Chiapas, 07-120 a 07-124 corresponden a municipios
    distintos en 2018 y en 2021–2024. Por eso se cruza la combinación clave + nombre de cada
    elección, y se exige que dentro de una elección dos claves no caigan en el mismo municipio
    INEGI.
  - Resultado del cruce de 2,489 combinaciones: 2,464 exactas, 15 por nombre contenido, 5 difusas
    (todas revisadas en `docs/diccionarios/cruce_municipios_ine.md`) y 5 manuales.
  - Las manuales son los homónimos de Oaxaca (San Juan Mixtepec y San Pedro Mixtepec), resueltos por
    tamaño (lista nominal 2024 contra población de 18+ del Censo 2020), y Tezoatlán, con nombre
    abreviado. No queda lista nominal sin cruzar.
- **Geografía electoral inestable.** En 2015 el INE aún no separaba varios municipios:
  - los 7 de Chiapas creados en 1999, Tulum y unos 20 de Oaxaca no aparecen ese año y sus votantes
    se registran en el municipio vecino;
  - hay municipios sin casillas en alguna elección (Oxchuc en 2021; Pantelhó y Chicomuselo en
    2024).
  - **Regla:**
    - entran solo los municipios con las 4 elecciones (2,417 de 2,456);
    - en la especificación principal salen los 103 cuyo cambio de lista nominal entre elecciones
      consecutivas se aleja de la mediana de su estado en más de log(1.25), es decir, ~25%;
    - la robustez `municipio_elecciones_todos` los conserva.
- **Muestra resultante.** 1,375 municipios tratados (449 con apertura temprana, 926 tardía) contra
  458 controles; 2 fuera por exposición.
- **Aguascalientes, distrito 01, 2015.** El SICEE trae para ese distrito las 445 casillas de la
  elección **extraordinaria** de diciembre de 2015 (actas `JE2015E_01_…`), sin duplicados con la
  ordinaria. Se usan tal cual, como se fijó en el preregistro.
- **Votos que no entran.** Casillas especiales, mesas sin sección y casillas no instaladas o con
  paquete no entregado: 0.29–0.35% de los votos de cada elección. Todas las actas cuadran (válidos +
  nulos + no registrados = total).
- **SESNSP.**
  - Las claves 998/999 son 0.37% de las carpetas.
  - Los 2,456 municipios estables tienen dato en todos los trimestres desde 2017; en 2015–2016,
    solo 1,921.
  - Totales nacionales de control, 2019: 87,116 robos a transeúnte, 29,481 homicidios dolosos y
    765,561 robos.

## Preregistro de la fase 4 — efectos fijos, controles, derrames, bancarización y uso (2026-10-14)

Se fija **antes** de construir los paneles nuevos y de estimar. Plan completo en
`docs/contexto/plan_fase4.md`.

**Origen.** Critican el uso de Callaway–Sant'Anna y la forma de los controles, y queremos medir
bancarización y uso.

**Transparencia.** Ya se vieron los resultados de la fase 0 a la 3: TWFE estático, Sun–Abraham,
BJS, DiD apilado, CS solo con nunca tratados y CS sin covariables. También se vieron los totales
nacionales del Banco del Bienestar en el Portafolio (sucursales, tarjetas y transacciones; nada
cruzado con el tratamiento) y el descriptor de la ENIGH 2024. Ninguna de las especificaciones de
abajo se ha estimado.

Nada de esto toca la especificación principal, la maestra, la tabla final ni sus familias. Va en
`analisis/13_fase4.R` y `construccion/panel_fase4.py`, con salidas `fase4_*`.

**Criterios.** Los de siempre:
- pre-prueba fallida (Wald previa p < 0.05) = descriptivo;
- nulo informativo = no significativo y con el IC90 dentro de ±5% de la media previa de las
  tratadas;
- Romano–Wolf dentro de cada familia y BH sobre todas las especificaciones de la fase;
- MDE80 y cota del IC90 siempre.

### 0. Regresión con efectos fijos (familia `financiero_fe`)

- **Resultados:** `sucursales_privado_pc`, `sucursales_bm_pc` y `sucursales_eacp_pc`. Además, la
  primera etapa `sucursales_total_pc`, que queda fuera de la familia. Mismo panel, muestra y
  ventana que la especificación principal (`municipio_trim`, 2019T1–2024T4).
- **0.1 Estudio de evento TWFE clásico.**
  - Efectos fijos de municipio y de trimestre; e ∈ [−8, 8] con los extremos agrupados; ref = −1;
    cluster municipal.
  - Es descriptivo del sesgo: se reporta junto a Sun–Abraham y CS.
- **0.2 TWFE extendido (Wooldridge, 2021).** Es el estimador de la familia (Romano–Wolf).
  - Una regresión con efectos fijos de municipio y de trimestre, más un indicador por celda
    (cohorte g, trimestre t ≥ g) entre las tratadas.
  - Covariables: pendientes de trimestre en `log_poblacion_2020`, `indice_marginacion_2020` y
    `banca_mun_2019`.
  - ATT agregado: promedio de las celdas con pesos iguales a los de la agregación "group" de CS.
    Varianza por combinación lineal, con cluster municipal.
  - Pre-prueba: la misma regresión con indicadores de los periodos previos de cada cohorte, y la
    Wald conjunta.
  - Comprobación interna: sin covariables debe reproducir BJS (+0.0115).
- **0.3 Apilado** (Cengiz et al., 2019; pesos de Wing et al., 2024). El de `08_disenos_alternativos.R`
  con efectos fijos de estado × tiempo de evento × pila.
- **0.4 Sensibilidad de los efectos fijos.** El TWFE estático y el extendido, con:
  - (a) estado × trimestre;
  - (b) decil de tamaño × trimestre;
  - (c) tendencias lineales municipales;
  - (d) covariables × trimestre.
- **Hipótesis.** Si el nulo de CS es real, todas las especificaciones caen dentro de ±5%. Si fuera
  artefacto del estimador, el TWFE extendido y el apilado se separan de CS.

### H. Grupo de control y covariables (robustez de `sucursales_privado_pc`, `_bm_pc` y `_eacp_pc`)

**H1. Grupo de control**, con CS DR y las covariables base:
- (c) **solo municipios que alguna vez abren**: sin los nunca tratados, la identificación viene
  solo del calendario;
- (d) nunca tratados emparejados 1:1 por puntaje de propensión (vecino más cercano con calibre de
  0.2 de de del logit, dentro de la región) con las tratadas, contra la base;
- (e) controles sin vecino tratado: el apilado de 0.3 con controles limpios que, además, no tienen
  ningún municipio contiguo con sucursal dentro de la ventana de la pila.
  - **Regla fijada antes de contar:** si en la mediana de las pilas quedan menos de 100 controles,
    se usa la versión que solo excluye a los vecinos de **aperturas nuevas** (G ≥ 2019T2) y se
    ignoran las sucursales heredadas. Se reportan los conteos de las dos versiones.

**H2. Covariables**, con CS DR y aún no tratados. Se agregan en este orden:
1. ninguna;
2. población;
3. \+ marginación;
4. \+ banca 2019 (la base);
5. \+ tendencia previa del resultado, 2017T2–2018T4: la pendiente lineal de las sucursales por
   adulto. Empieza en 2017T2 porque es el primer trimestre en que la BDIF publica
   `modulos_compartamos` y se pueden restar de banca múltiple (P-11);
6. \+ distancia del centroide al municipio más cercano con banca múltiple en 2019T1;
7. \+ región: las cuatro del *Reporte sobre las Economías Regionales* de Banxico (norte, centro
   norte, centro y sur; nota 1 del reporte de abril–junio de 2018).

**H3.** Balance y soporte común: la tabla de `12_diagnosticos.R` se lleva al trabajo final.

H no tiene familia propia: son robusteces. Se lee si el ATT se mueve más de 1 ee respecto a la
base.

### A. Validez del nulo financiero

- **A1. Derrames.** Contigüidad de primer orden de los polígonos del MG 2024.
  - (a) Es H1(e).
  - (b) Efecto en los vecinos. Apilado con unidades sin sucursal propia en la ventana de la pila.
    "Tratada" = su primer vecino abre en g; controles = sin sucursal propia ni vecina en la
    ventana. Resultado: `sucursales_privado_pc`. Familia `derrames`, con BH.
- **A2. Placebo de fecha.**
  - Panel 2017T2–2021T4, con G falsa = G − 8 para las cohortes reales 2022T1–2024T1. La ventana
    queda entera antes de la apertura real. Empieza en 2017T2 por los módulos de Compartamos.
  - Salen las unidades con apertura real en 2019T2–2021T4.
  - CS DR, aún no tratados, y banca múltiple sin los módulos de Compartamos.
  - Hipótesis: ATT ≈ 0. Si no, las tratadas ya divergían antes.
- **A3. Permutación.** 199 reasignaciones del vector G dentro de cada estado (incluidos los
  ceros), con el TWFE extendido sin covariables. Valor p = proporción con |ATT| ≥ |ATT observado|.
  Solo para `sucursales_privado_pc`.
- **A4. HonestDiD con suavidad.** Δ^SD con M ∈ {0, 0.005, 0.01, 0.02} además de las magnitudes
  relativas. Base universal y los tres resultados financieros.
- **A5. Por cohorte y por estado.** ATT(g) por cohorte (de `cs_attgt`) y CS dejando fuera un
  estado a la vez (32 corridas). Se reportan el mínimo y el máximo.

### B. Bancarización (familia `bancarizacion`, con Romano–Wolf)

- **Panel `municipio_trim_banco`.** Del Portafolio:
  - operativa 2016-01 a 2021-12 y modelo 2022-01 a 2026-07;
  - el Banco del Bienestar por municipio estable (P-7);
  - saldos a fin de trimestre, y las transacciones como suma de los tres meses;
  - por 10 mil adultos con el denominador fijo de 2022T4 (P-6).
- **B1.** `tarjetas_debito_bb_pc`. CS DR, aún no tratados, covariables base, ventana 2019T1–2025T4,
  para todos los tratados.
  - **Antes de estimar** (adenda de datos): se mide qué parte de los saltos nacionales de sep-2021
    y feb-2022 cae en municipios que abren dentro de ±1 trimestre.
  - Si es más de la mitad, el principal pasa a δ = 1.
  - Hipótesis: positivo (primera etapa).
- **C1.** `transacciones_cajero_bb_pc` (suma trimestral). Hipótesis: positivo.
  - El cociente transacciones/tarjeta solo está definido donde el banco ya tiene tarjetas, así que
    va como descriptivo entre las tratadas.
- **B2. Traslado de cuentas.**
  - Unidades: los municipios con sucursal heredada (ya tratados en 2019T1).
  - "Tratada" = el primer municipio contiguo abre en g; controles = ya tratados sin aperturas
    vecinas en la ventana. Apilado.
  - Resultado: `tarjetas_debito_bb_pc`. Si baja, parte de la primera etapa es traslado de cuentas
    desde la sucursal heredada.
  - Además, como descriptivo: el crecimiento nacional de las tarjetas del banco contra la suma de
    los efectos estimados en las tratadas.
  - Familia `derrames`.

### C. Uso privado con panel largo (familia `privado_largo`, con Romano–Wolf)

- **C4.** `tarjetas_credito_privado_pc` = BDIF `tarjetas_credito` de "banca", menos el Banco del
  Bienestar del Portafolio, menos Banjército si la BDIF lo incluye.
  - Se verifica con 2022T4+, cuando la BDIF ya separa la banca de desarrollo.
  - Ventana 2019T1–2024T4 y robustez hasta 2025T4.
- **C3.** `establecimientos_tpv_privado_pc` = BDIF `establecimientos_tpv` de "todos", menos el
  banco y Banjército. Misma ventana.
- **Estimación:** CS DR, aún no tratados y las covariables base. Hipótesis bilateral; se espera
  nulo.

### Adenda de datos de la fase 4 (2026-10-14, antes de estimar)

Sale de `construccion/panel_fase4.py` y `variables/{vecinos,distancia}.py`
(`outputs/tablas/fase4_adenda_*.csv`). Nada se cruzó con un resultado.

- **Banca de desarrollo de la BDIF = Banco del Bienestar + Banjército del Portafolio**, exactas
  (26,061,835 tarjetas de débito en 2022T4 en las dos fuentes). Así que la "banca" de 2016–2022T3
  incluye a Banjército, y las series privadas se obtienen restando los dos. El banco no tiene
  tarjetas de crédito ni TPV; Banjército sí (~20 mil tarjetas y 300–550 comercios).
- **Las series privadas reconstruidas coinciden con lo que la BDIF publica por sector** de
  2022T4 a 2025T4: mismo total nacional, correlación municipal de 1.0 y un solo
  municipio-trimestre distinto (TPV, 2024T2, por una unidad).
- **Saltos de las tarjetas del banco.**
  - Sep-2021 (−4.50 millones): 0% en municipios que abren dentro de ±1 trimestre.
  - Feb-2022 (+5.89 millones): 1.9%.
  - Son movimientos de las sucursales heredadas. La regla de B1 no se activa: el principal queda
    con δ = 0.
- **Controles sin vecino tratado (H1e).** De los 500 controles limpios, en la mediana de las pilas
  quedan 24 sin ningún vecino con sucursal y 41 sin vecino con apertura nueva: el 92% de los nunca
  tratados colinda con un municipio que abre.
  - Por la regla fijada, se usa la versión de aperturas nuevas (41).
  - Con tan pocos controles, H1(e) y A1(b) probablemente no serán informativos. Se reportan igual,
    con sus conteos.
- 🔴 **Quiebre en los comercios con TPV.** La serie "todos" de la BDIF cae 21.7% entre 2021T4 y
  2022T1 (824,983 → 645,883) en el mismo formato de archivo; las tarjetas de crédito no tienen
  quiebre.
  - Como con el cambio de escala de VIIRS, C3 se estima **después del quiebre**, 2022T1–2025T4,
    con las cohortes que tengan dos previos.
  - La ventana 2019T1–2024T4 queda como robustez.
- **Placebo (A2):** 1,965 municipios × 19 trimestres (2017T2–2021T4). 1,256 tienen G falsa entre
  2020T1 y 2021T4; 709 tienen G = 0: los nunca tratados, más la cohorte real 2024T1, cuya G falsa
  cae fuera de la ventana.
- **Contigüidad:** 2,456 municipios estables, 14,312 pares simétricos, mediana de 6 vecinos y
  ninguno aislado.
- **Distancia a la banca múltiple 2019T1:** entre los municipios sin banca, mediana de 18.8 km y
  p90 de 42.4 km.
- **Regiones de Banxico:** sur 1,124 municipios, centro 599, centro norte 457, norte 276.

### Corrección del TWFE extendido antes de la corrida final (2026-10-14)

- **Qué cambia.** El preregistro describía el TWFE extendido con covariables solo con pendientes de
  trimestre por covariable. Pero el estimador de Wooldridge (2021) con covariables también
  interactúa cada celda (g, t) con las covariables centradas en la media de su cohorte. Sin esas
  interacciones, las pendientes absorben la parte de la heterogeneidad del efecto que se correlaciona
  con las covariables.
- **Cómo se vio.** En la prueba de humo, la primera etapa pasó de 2.01 (sin covariables) a 3.79
  (solo con pendientes), contra 2.00 de CS.
- **Transparencia.** La prueba de humo ya mostró las cifras de todo el bloque 0, de las que salió
  esta corrección.
- **Decisión.** El estimador de la familia `financiero_fe` es la versión completa de Wooldridge.
  La versión del preregistro se reporta en su propio renglón.
- **Comprobación interna:** sin covariables y con pesos por observación, reproduce BJS en las cuatro
  series (privadas 0.0115, banca múltiple −0.0093, EACP 0.0209 y primera etapa 1.8698).

**Exploratorio, registrado antes de correrlo (`diagnostico_etwfe`).**
- **Qué se vio en la prueba de humo.** Con covariables, el TWFE extendido da +6.8% en sucursales
  privadas (ee 2.7%) y +11% en EACP. CS da +0.7%, y todos los estimadores sin covariables dan entre
  +0.3% y +1.8%.
- **Primeras pistas:**
  - la diferencia crece en las celdas posteriores a 2024T1, cuando ya no quedan aún no tratados y
    las pendientes por covariable salen solo de los 500 nunca tratados (22 con banca múltiple; log
    de la población desde 4.4, contra 5.9 en las tratadas);
  - la cohorte desbalanceada de 2023T4 da 0.15.
- **Qué se corre:** el TWFE extendido con y sin covariables en cuatro muestras:
  - completa;
  - hasta 2024T1;
  - solo municipios que alguna vez abren;
  - soporte común (puntaje de propensión entre 0.1 y 0.9; Crump et al., 2009).
- **Cómo se lee:** si el efecto con covariables desaparece con soporte común o sin los nunca
  tratados, es extrapolación lineal fuera del soporte y manda CS (DR). Si se sostiene, la
  conclusión depende del ajuste por covariables y así se reporta.

### A4: método de HonestDiD con suavidad (2026-10-14)

- **El problema.** El método por defecto de HonestDiD 0.2.6 para Δ^SD (FLCI) falla en este entorno
  dentro del optimizador ("$ operator is invalid for atomic vectors"); no produjo ningún intervalo.
- **La solución.** Se usa el intervalo condicional híbrido (C-LF) de Rambachan y Roth (2023). Es el
  que el paquete usa por defecto en las magnitudes relativas, y da casi lo mismo que el condicional
  puro.

### Resultados de la fase 4 (corrida del 2026-10-14)

Registro en `outputs/logs/fase4_20261014_200519.log`. Tablas en `outputs/tablas/fase4_*`; figura
`fig_fase4_estimadores.png`. Cifras en % de la media previa de las tratadas (sucursales privadas:
0.929 por 10 mil adultos).

**0. Regresión con efectos fijos (sucursales privadas).**
- Todos los estimadores sin ajuste por covariables coinciden con CS (+0.7%):
  - TWFE estático +1.0%;
  - estudio de evento TWFE −0.6% (previos planos, p = 0.74);
  - Sun–Abraham +0.3%;
  - BJS +1.2%;
  - apilado +0.8%, y +2.5% con efectos fijos estado × evento;
  - TWFE extendido sin covariables +1.8% (cota 6.4%).
- **La excepción: el TWFE extendido de Wooldridge con covariables** da +6.8% (ee 2.7%, Romano–Wolf
  p = 0.009) en privadas y +11.0% en EACP (RW p = 0.001); en banca múltiple, +1.4%.
- El diagnóstico exploratorio lo atribuye a la comparación contra los nunca tratados con ajuste
  lineal:
  - hasta 2024T1, +4.4%;
  - con soporte común, +7.7%;
  - **solo con municipios que alguna vez abren (identificación por calendario, hasta 2023T4),
    +1.3% (ee 1.3%)**, y +1.4% en EACP.
  - *Corrección del 2026-10-15 (revisión):* la primera versión de esta muestra incluía 2024T1–2025T4,
    cuando ya todos están tratados; las celdas eran colineales con el efecto fijo de trimestre y
    `fixest` quitaba 16 (daba +1.6%, ee 1.9%). Ahora termina en 2023T4 y la cohorte de 2024T1 solo
    es control, como hace `did`.
  - *Diagnóstico adicional (revisión del 2026-10-15; exploratorio, después de ver los resultados;
    `diagnostico_cs_metodo`, `fase4_diagnostico_cs_metodo.csv`).* CS con el mismo ajuste lineal
    (solo regresión de resultado) da +2.1% (ee 1.7%) en privadas y +2.1% en EACP; solo con
    ponderación por propensión, +1.2% y +1.9%. El doblemente robusto reproduce la base (+0.7%). El
    +6.8% no lo produce el ajuste lineal por sí solo: es propio del TWFE extendido. Como recortar
    al soporte común no lo baja (+7.7%), la explicación por extrapolación no es cerrada: **una
    atracción pequeña está menos acotada que el desplazamiento**, y así se dice en el texto.
  - Por la regla registrada antes de correrlo, **manda CS**. Se reporta como sensibilidad de la
    conclusión de "sin atracción".
- **Sensibilidad de los efectos fijos** (TWFE estático / extendido):
  - estado × trimestre +1.1% / +1.9%;
  - decil de tamaño × trimestre +2.3% / +4.2%;
  - tendencias municipales −0.5% / −1.9%.
- **Banca múltiple:** los estimadores de imputación dan −2.2%, pero su pre-prueba falla (p = 0.004).
- **Primera etapa:** el TWFE extendido da 2.06 (con covariables) y 2.01 (sin ellas); CS, 2.00.

**H. Grupo de control y covariables (sucursales privadas).**
- **Solo municipios que alguna vez abren:** −1.9% (cota 4.2%: nulo informativo). En EACP, −3.3%
  (cota 7.0%). Sin nunca tratados, `did` corta la ventana en 2023T4 y deja la cohorte de 2024T1
  solo como control: son 1,248 tratadas contra 209 (antes la tabla decía 1,457 contra 0).
- **Nunca tratados emparejados** (320 contra 320): +2.3% (cota 7.4%).
- **Controles sin vecino con apertura nueva** (66): +0.6% (cota 2.0%).
- **Covariables una por una:** entre +0.4% y +1.2% en las seis variantes. En banca múltiple la
  pre-prueba falla con cuatro de las seis (ninguna, tendencia previa, distancia y región).

**A. Validez.**
- **Derrames:** en los vecinos de los municipios que abren, +0.5% (521 contra 105; cota 4.0%).
- **Placebo de fecha** (2017T2–2021T4): privadas −0.6% (cota 1.9%), banca múltiple −1.7% y EACP
  +0.3%. Los tres son nulos informativos.
- **Permutación** (199, dentro del estado): p = 0.315.
- **HonestDiD con suavidad** (C-LF), con M = 0 (permite tendencias lineales):
  - privadas, entre −4.0% y +2.2% (objetivo: el promedio de los tres primeros trimestres después
    de la apertura, no el ATT global);
  - banca múltiple, entre −3.9% y +3.0%;
  - EACP, entre −6.1% y +3.6%.
  - Con M = 0.005, privadas queda entre −5.7% y +3.9%.
- **Sin un estado a la vez:** entre +0.3% y +1.6%, cada uno con su propia media previa.

**B. Bancarización y uso del banco.**
- **Primera etapa para todas las cohortes** (1,457, contra 766 en la BDIF): +3,284 tarjetas de
  débito del banco por 10 mil adultos (ee 226), con previos planos (p = 0.99).
- **Transacciones en cajeros del banco:** +5,999 por 10 mil adultos por trimestre (ee 186).
- **Descriptivo:** entre las tratadas, ~1.5 transacciones en los cajeros del banco por tarjeta por
  trimestre a partir del primer año: una cada dos meses, como el calendario de pago de los
  programas. El Portafolio cuenta las transacciones en los cajeros del banco en el municipio; no
  incluye pagos con tarjeta ni retiros en cajeros de otros bancos.
- **Traslado de cuentas** (municipios con sucursal heredada cuyo vecino abre; 464 contra 47):
  +488 tarjetas (ee 334). No es informativo, pero no muestra el signo negativo que tendría un
  traslado.

**C. Privado con panel largo.**
- **Tarjetas de crédito de banca múltiple, 2019–2024:** +0.8% (cota 3.5%), nulo informativo.
  Hasta 2025: +1.2% (cota 4.7%).
- **Comercios con TPV** después del quiebre: +1.0% (cota 9.4%), no informativo. Con el quiebre, la
  pre-prueba falla (p = 0.006), como se esperaba.

**Lectura.**
1. **"No desplazó a la banca privada" es robusto en sucursales privadas:** ningún estimador, grupo
   de control ni conjunto de covariables da un efecto negativo significativo, y el crédito privado
   con panel largo tampoco se mueve.
   - En **banca múltiple**, tres estimadores dan entre −2.2% y −2.5%, significativos: el TWFE
     estático, BJS y el TWFE extendido sin covariables. En este último la pre-prueba falla
     (p = 0.004), y CS da −0.2%.
   - Si hay desplazamiento de la banca múltiple, es menor a 5%.
2. **"Tampoco la atrajo" depende de una especificación.** El TWFE extendido con covariables contra
   los nunca tratados da +6.8%. Identificando solo por el calendario baja a +1.3%, y CS (DR) da
   +0.7%.
3. **El banco sí abre cuentas en todas las cohortes.** En sus cajeros hay alrededor de una
   transacción por tarjeta cada dos meses, como el pago de los programas. No observamos pagos con
   tarjeta ni retiros en otros cajeros, así que esto no mide todo el uso de la cuenta.
4. **No hay evidencia de que las cuentas nuevas sean traslados** desde sucursales heredadas, pero
   la prueba no tiene potencia.
5. **La ENIGH no tiene potencia para uso ni bienestar.** Todo queda descriptivo
   (`fase4_enigh.csv`):
   - **Municipal (CS):** apenas 7–16 nunca tratados; MDE80 entre 34% y 480% de la media. La
     pre-prueba falla en ahorro, programas, ingreso y gasto.
   - **Hogares ponderados (TWFE extendido; 1,026 municipios tratados contra 175):**
     - pago electrónico −26% y gasto electrónico −20% (MDE80 de 58% y 72%);
     - depósitos +8.6% (MDE80 29%);
     - beneficios gubernamentales −8.8% (MDE80 35%);
     - ingreso +6.7 puntos log y gasto +8.3, ambos con la pre-prueba fallida.
   - **Por qué:**
     - la forma de pago solo es comparable desde 2020;
     - los municipios que nunca abren casi no están en la muestra;
     - la ENIGH no es representativa por municipio.
   - **Lectura:** con estos datos no se puede afirmar nada del uso de los servicios ni del bienestar
     de los hogares; los datos administrativos del Portafolio (C1) son la única medida de uso con
     poder estadístico.

### Adenda: ENIGH (C2, D y B3), fijada antes de descargar (2026-10-14)

- **Fuente.** INEGI, ENIGH nueva serie, "conjunto de datos" en CSV de la pestaña *Datos abiertos* de
  cada edición (`https://www.inegi.org.mx/contenidos/programas/enigh/nc/<año>/datosabiertos/…`):

  | Edición | Archivo | Tamaño |
  |---|---|---|
  | 2016 | `conjunto_de_datos_enigh2016_nueva_serie_csv.zip` | 41 MB |
  | 2018 | `conjunto_de_datos_enigh_2018_ns_csv.zip` | 43 MB |
  | 2020 | `conjunto_de_datos_enigh_ns_2020_csv.zip` | 94 MB |
  | 2022 | `conjunto_de_datos_enigh_ns_2022_csv.zip` | 90 MB |
  | 2024 | `conjunto_de_datos_enigh2024_ns_csv.zip` | 103 MB |

- **Levantamiento:** del 21 de agosto al 28 de noviembre en las cinco olas (páginas de presentación
  del INEGI). Geografía: `ubica_geo` = entidad + municipio (descriptor de 2024).
- **Tratamiento (una ola = un periodo, t = 1…5).** G = la primera ola levantada después de la
  apertura.
  - Abre a más tardar en el segundo trimestre del año de la ola: tratado en esa ola.
  - Abre en el tercer trimestre del año de una ola: **ambiguo** (abre durante el levantamiento) y
    sale.
  - Abre en el cuarto trimestre: tratado en la ola siguiente.
  - Salen los ya tratados en 2019T1 y los sospechosos de Banjército, como en el principal.
  - Las aperturas después de 2024T3 cuentan como no tratadas (G = 0).
- **Resultados por municipio × ola.** Promedios ponderados con el factor de expansión del hogar.
  - Familia `enigh_uso` (Romano–Wolf):
    - `pct_gasto_electronico`: % del gasto monetario con forma de pago registrada que se pagó con
      débito, crédito, transferencia, domiciliación o pago móvil;
    - `pct_hog_deposito`: % de hogares con depósitos de ahorro mayores a cero.
  - Familia `enigh_bienestar` (Romano–Wolf):
    - `log_ing_cor_pc`: log del ingreso corriente per cápita;
    - `pct_hog_bene_gob`: % de hogares con beneficios gubernamentales.
  - Secundarios (BH): `pct_hog_pago_electronico` (algún pago electrónico) y `log_gasto_mon_pc`.
- **Muestra principal:** municipios presentes en las cinco olas (panel balanceado). CS DR, aún no
  tratados, las covariables base y cluster municipal. Pre-prueba: Wald de los previos.
- **Robustez:** TWFE extendido a nivel hogar (efectos fijos de municipio y de ola, celdas
  cohorte × ola, ponderado por el factor, cluster municipal), con todos los municipios de cada ola.
- **Antes de estimar** (adenda de datos, sin cruzar con el tratamiento), se verifica:
  - que los códigos de forma de pago y las variables `deposito`, `bene_gob`, `ing_cor` y
    `tot_integ` existan y signifiquen lo mismo en las cinco olas;
  - cuántos municipios hay por ola y cuántos repiten en las cinco.
  - Si un código cambia de significado, el resultado se construye solo con las categorías
    comparables, y se documenta.
- **Lectura.** Si el MDE80 de un resultado es mayor a 10% de su media previa, queda como
  descriptivo (regla ya fijada para C2 y D).

**Adenda de datos de la ENIGH (2026-10-14, después de descargar y antes de estimar).**
- **Descarga.** Los cinco zips están en `data/raw/enigh/<año>/` y en el MANIFEST, con los tamaños
  esperados.
- **Formato.** El catálogo `forma_pag` es **idéntico en las cinco olas** (00 no aplica … 10 otro).
  `ubica_geo`, `factor`, `upm`, `est_dis`, `tot_integ`, `ing_cor`, `gasto_mon`, `deposito` y
  `bene_gob` existen en el concentrado de las cinco. `gastoshogar` trae `forma_pag1..3` y
  `gasto_tri` en las cinco. Dos ajustes de lectura:
  - En 2016 `ubica_geo` tiene 9 dígitos (incluye la localidad): el municipio son los primeros 5.
  - Los archivos vienen en UTF-8 con BOM o en latin-1, según la ola.
- **Cobertura.**
  - Municipios por ola: 961, 995, 1,088, 1,131 y 1,108.
  - **508 están en las cinco**, pero 259 tienen sucursal heredada y salen.
  - Quedan 249: 7 nunca tratados, 77 que abren antes de la ola 2022, 136 entre las olas 2022 y
    2024, y 28 ambiguos (2022T3).
  - Con tan pocos nunca tratados, la muestra principal compara sobre todo por calendario y tendrá
    poca potencia. **La robustez a nivel hogar, con todos los municipios de cada ola, pesa más que
    en otras fuentes.**
- **Regla del pago electrónico,** fijada antes de estimar:
  - un gasto de `gastoshogar` es electrónico si **alguna** de sus tres formas de pago es 03, 04,
    05, 06 o 09;
  - el denominador es el gasto con al menos una forma de pago distinta de 00;
  - `gastospersona` (educación y otros personales) no entra.
- **Ingreso:** `ing_cor` y `gasto_mon` son trimestrales y nominales. En logaritmos, la inflación
  común la absorben los efectos fijos de ola.
- 🔴 **La forma de pago no es comparable antes de 2020.**
  - En 2016 y 2018, `gastoshogar` cubre solo el 17% del gasto monetario del concentrado; desde
    2020, entre 92% y 94%.
  - Además, las claves de gasto cambian de clasificación en 2022 y en 2024, así que no hay una
    canasta común.
  - Por la regla 10, **los resultados de forma de pago** (`pct_gasto_electronico` y
    `pct_hog_pago_electronico`) se estiman solo con 2020, 2022 y 2024:
    - municipios en las tres olas: 369 sin sucursal heredada;
    - con dos previos solo cabe la cohorte que abre entre las olas 2022 y 2024 (216), contra 16
      nunca tratados.
  - Ahorro, programas, ingreso y gasto salen del concentrado, que es comparable, y se quedan con
    las cinco olas.
- **Promedios nacionales ponderados, como comprobación:**

  | | 2016 | 2018 | 2020 | 2022 | 2024 |
  |---|---|---|---|---|---|
  | Hogares con algún pago electrónico | 3.4% | 3.7% | 14.2% | 17.8% | 29.3% |
  | Hogares con depósitos de ahorro | 18.5% | 20.6% | 27.7% | 28.5% | 33.7% |
  | Hogares con beneficios gubernamentales | 30.8% | 28.0% | 29.7% | 34.2% | 31.7% |

  En 2024 hay 38.8 millones de hogares ponderados.

## Fase 5 (2026-10-21): ¿se usan las cuentas? Exploratoria, no preregistrada

Origen: comentarios del equipo sobre la presentación (el banco abre cuentas, pero ¿se usan para
crédito o pagos?). Se corrió después de ver los resultados de la fase 4, así que **no es
confirmatoria**: no entra en la maestra, la tabla final ni las familias de inferencia múltiple.

- **Datos.** `construccion/panel_uso.py` → `panel_municipio_uso.parquet`: el panel de la fase 4 más
  la banca de desarrollo de la BDIF desde 2022T4 (captación por nivel N1–N4, captación y crédito
  totales, crédito personal, de nómina y grupal, tarjetas de crédito). La banca de desarrollo es el
  banco más Banjército: salen los 86 municipios donde Banjército tuvo sucursal (Portafolio
  2016–2021 y modelo Power Pivot 2022–2026).
- **Diseño.** `analisis/14_uso.R` (`make uso`): CS DR con la especificación base en 2022T4–2025T4.
  Por la regla 10 entran solo las aperturas de 2023T2 en adelante (dos trimestres previos):
  763 tratadas contra 498 controles.
- **Resultados** (por diez mil adultos): captación +1,316 contratos (ee 161, previos p = 0.69),
  tarjetas de débito +2,458 (ee 295, p = 0.63) y crédito **+6.2** contratos (ee 2.2, p = 0.12):
  menos de un crédito por cada 100 cuentas nuevas.
- **Descriptivos** (`app/datos/temas.py`): en 2025T4 la banca de desarrollo sin Banjército tiene
  0.5 créditos por cada 100 cuentas y la banca múltiple de los mismos municipios, 61. En el
  Portafolio, los 2,957 cajeros del banco son solo de retiro y el banco no reporta tarjetas de
  crédito ni terminales punto de venta.
- 🔴 **Niveles de cuenta.** En 2025T2 la CNBV reclasificó las cuentas del banco de N4 a N2 en todo
  el país: los niveles no se estiman (el salto se leería como efecto); en 2025T4 el 92% son N2.
- **Lo que no se puede con datos públicos:** cuentas activas, saldos y crédito por sucursal (la
  BDIF municipal solo trae contratos). Requiere pedirlos al banco por transparencia.

**Ampliación de la fase 5 (2026-11-16, exploratoria).** A pedido del equipo, qué más hace el banco
además de abrir cuentas. Misma especificación y muestra (763 tratadas contra 498, 2022T4–2025T4, sin
los 86 municipios con Banjército); nuevas series de la banca de desarrollo de la BDIF en
`panel_uso.py`. Por diez mil adultos:

| Resultado | Efecto (ee) | Previos (p) | Por cada 100 cuentas nuevas |
|---|---|---|---|
| Contratos de captación | +1,316 (161) | 0.69 | — |
| Depósitos a plazo | +6.0 (0.6) | 0.59 | 0.45 |
| Crédito total | +6.2 (2.2) | 0.12 | 0.47 |
| Crédito personal | +6.0 (2.1) | 0.12 | — |
| Transacciones en cajeros, por trimestre | +2,218 (83) | 0.63 | — |

- **Sin dato:** la BDIF reporta en cero las cuentas de ahorro y las asociadas a un celular del banco en
  toda la ventana, así que no se estiman. Las transferencias desde la app empezaron en 2026, después
  de los datos.
- 🔴 **2024T2:** la captación del banco cae 74% en todo el país y se recupera al trimestre siguiente.
  Sin ese trimestre (`uso_sensibilidad.csv`): captación +1,420, plazo +6.1, crédito +7.5.
- **Crédito:** el saldo de contratos de crédito del banco baja de 288 mil (2022T4) a 111 mil (2025T4),
  casi todos personales. Es consistente con una cartera que se va pagando, aunque su origen no se
  conoce. El banco declara que no ofrece crédito (comunicado conjunto del 26 de mayo de 2023).
- **Lectura:** las cuentas sirven para cobrar y retirar los apoyos; por cada 100 cuentas nuevas hay
  menos de medio crédito y menos de medio depósito a plazo. Saldos y cuentas activas siguen sin ser
  públicos.
- Las transacciones de la BDIF (+2,218) y las del Portafolio (+5,999, fase 4) miden lo mismo con
  muestras y ventanas distintas.

## Efecto inyectado (2026-11-04): ¿el DiD detecta un efecto chico que sí existe? Exploratoria

Origen: pregunta del equipo sobre cómo sabemos que el DiD no da cero siempre. Los controles positivos
(primera etapa) son casi mecánicos y no prueban que detecte efectos chicos. Esta entrada se escribe
**antes de correr**; la verificación del código y la medición de tiempos no mostraron resultados de
potencia. No entra en la maestra, la tabla final ni las familias de inferencia múltiple.

- **Diseño.** `analisis/15_poder_inyectado.R` (`make poder-inyectado`), parámetros en
  `poder_inyectado` de `config/parametros.yaml`. Sucursales privadas ficticias sobre
  `sucursales_privado_pc`, con la especificación base del bloque financiero (CS DR, aún no tratados,
  2019T1–2024T4, ee de Liang–Zeger por municipio), como en Bertrand, Duflo y Mullainathan (2004).
- **Fechas.** El estimador es lineal en el resultado: con las fechas **reales**, el ATT se mueve
  exactamente lo inyectado y solo cambian el efecto sorteado y el ee (100 réplicas por escenario).
  Con las fechas **reasignadas** entre los municipios tratados de cada estado, cada réplica trae su
  propio ruido (200 réplicas): de ahí salen la potencia y los falsos positivos.
- **Escenarios.** Sin efecto (solo reasignadas); atracción de 2.8%, 5% y 7.6% (MDE80, umbral de
  equivalencia y Banco Azteca), con Poisson(λ · adultos / 10 mil) sucursales desde la apertura, y de
  5% gradual (entre 0 y 4 trimestres después); desplazamiento de 2.8% y 5%, donde cada sucursal
  privada que ya existía cierra con esa probabilidad.
- **Criterios (con fechas reasignadas).**

  | Medida | Esperado | Si falla |
  |---|---|---|
  | Falsos positivos sin efecto | Cerca de 5% | Más de 10%: los ee se quedan cortos y el nulo es optimista |
  | Detección de ±5% | Al menos 80% | Matizar "nulo informativo" en el trabajo y la presentación |
  | "Nulo informativo" por error con ±5% reales | Máximo 5% | Más de 10%: la regla de ±5% es demasiado laxa |
  | Cobertura del IC95 | Cerca de 95% | La inferencia no está bien calibrada |

- **Límites fijados de antemano.** Reasignar fechas rompe la relación entre fecha de apertura y
  covariables, así que la potencia puede salir algo optimista; los nunca tratados quedan fijos y
  las fechas solo se barajan dentro de cada estado. Solo cubre sucursales privadas, no banca múltiple
  ni EACP por separado.

### Resultados del efecto inyectado (corrida del 2026-11-04)

Registro en `outputs/logs/poder_inyectado_20261104.log`; tablas `poder_inyectado_{resumen,replicas}.csv`;
2,000 réplicas, ninguna fallida. La verificación reproduce `tabla_final` y confirma que el ATT se
mueve exactamente lo inyectado.

| Escenario | Sucursales (media) | Efecto sorteado | Detecta: reasignadas / reales | "Nulo informativo": reasignadas / reales |
|---|---|---|---|---|
| Sin efecto | 0 | 0 | 27% (falsos positivos) / — | 98.5% / — |
| Atracción 2.8% | 74 | +2.8% | 100% / 100% | 1% / 34% |
| Atracción 5% | 132 | +5.0% | 100% / 100% | 0% / 0% |
| Atracción 7.6% | 200 | +7.6% | 100% / 100% | 0% / 0% |
| Atracción 5% gradual | 132 | +3.5% | 100% / 100% | 0% / 3% |
| Desplazamiento 2.8% | 96 | −2.8% | 0.5% / 25% | 99.5% / 93% |
| Desplazamiento 5% | 170 | −4.9% | 72% / 100% | 41.5% / 4% |

**Contra los criterios fijados antes de correr (fechas reasignadas):**
- **Falsos positivos: reprueba.** 27%, contra el 5% esperado y el límite de 10%; todos positivos.
- **Detección de ±5%: pasa en atracción (100%), reprueba en desplazamiento (72%).**
- **"Nulo informativo" por error con ±5%: pasa en atracción (0%), reprueba en desplazamiento (41.5%).**
- **Cobertura del IC95: reprueba.** 73% sin efecto; entre 82.5% y 97% con efecto.

**Diagnóstico (después de ver los resultados, no preregistrado; solo con las salidas existentes).**
- Las fallas vienen del centro, no de la dispersión. Sin efecto inyectado, las fechas barajadas dan
  +1.87% en promedio (de 0.59; mínimo +0.30%; las 200 réplicas son positivas). El ee medio (1.13%) es
  mayor que esa dispersión, así que no hay evidencia de que los ee se queden cortos, como anticipaba
  la regla. La dispersión tampoco incluye el ruido entre tratadas y nunca tratadas, que quedaron fijas.
- El +0.71% real está por debajo del 97% de las fechas barajadas (6 de 200 réplicas son iguales o
  menores). Va en la misma dirección que solo con municipios que abren (−1.9%, cota 4.2%).
- **La causa no está establecida.** Pueden ser una deriva de las tratadas frente a las nunca tratadas
  (brecha cruda de 0.613 en 2021T4 a 0.640 en 2024T4), que las fechas reales acompañen una caída
  pequeña, o un artefacto de barajar: las pseudocohortes mezclan periodos posteriores reales.
- **Lectura condicional.** Si el +1.87% fuera sesgo presente también en la estimación real, el efecto
  sería −1.2%, con IC90 entre −2.8% y +0.5%. El nulo seguiría dentro de ±5%, pero no dentro de ±2.4%,
  y lo que quedaría sin descartar es un desplazamiento pequeño, no una atracción.
- Restando ese centro, la detección de ±5% sube a 100% y la de ±2.8% queda en 66–68%. Es una cuenta
  posterior: el centro se resta por construcción, así que no prueba nada sobre los falsos positivos.

Por la regla fijada, "nulo informativo" debe matizarse si esto se confirma. El trabajo final y el deck
no se tocaron: falta separar la causa barajando también a los nunca tratados y barajando solo entre
los municipios que abren.

**Diagnóstico de la causa, con la lectura fijada antes de correrlo** (`15_poder_inyectado.R
diagnostico`; sin efecto inyectado, 200 réplicas por diseño, exploratorio):
- *Barajar entre todas las unidades de cada estado, nunca tratadas incluidas.* Si el centro cae cerca
  de cero, el +1.87% viene de comparar a las tratadas con las nunca tratadas. Aquí se lee la inferencia:
  si los falsos positivos quedan lejos de 5%, el problema sí es de errores estándar.
- *Barajar solo entre los municipios que abren, sin nunca tratados* (la muestra de H1c, hasta 2023T4).
  Si el centro es cercano a cero, el −1.9% real se compara contra esa distribución: con p de
  aleatorización menor a 0.05 hay señal de un desplazamiento pequeño ligado al calendario; si no, no.

**Resultado del diagnóstico** (`poder_inyectado_diagnostico.csv`; sin efecto inyectado, 200 réplicas):

| Fechas barajadas | Centro | De | ee medio | Falsos positivos | Cobertura IC95 | Estimación real | p de aleatorización |
|---|---|---|---|---|---|---|---|
| Entre tratadas, nunca tratadas fijas | +1.87% | 0.59 | 1.13 | 27% | 73% | +0.71% | 0.97 |
| Entre todas las unidades | +0.55% | 1.04 | 1.18 | 2% | 98% | +0.71% | 0.47 |
| Solo entre las que abren (H1c) | +0.00% | 1.31 | 1.23 | 4% | 96% | −1.95% | 0.14 |

- **Inferencia:** calibrada. Cuando el calendario y el grupo son de verdad aleatorios, los falsos
  positivos quedan en 2–4% y los ee no se quedan cortos.
- **El +1.87% viene de la comparación contra las nunca tratadas**, que quedaban fijas: al barajarlas
  baja a +0.55%, y sin ellas desaparece. El centro restante (+0.55%, distinto de cero) sugiere que
  también pesa la composición por estado, que barajar dentro del estado conserva.
- **Sin señal de desplazamiento por calendario:** el −1.95% tiene p = 0.14, arriba del 0.05 fijado.

**Potencia con el diseño calibrado, con la lectura fijada antes de correrla** (`15_poder_inyectado.R
calibrado`): se inyectan ±2.8% y ±5% con las fechas barajadas entre todas las unidades, 200 réplicas
por escenario, y se aplican los mismos criterios: detección de ±5% de al menos 80% y "nulo informativo"
por error con ±5% de máximo 5%.

**Resultado de la potencia calibrada** (`poder_inyectado_calibrado.csv`; fechas barajadas entre todas
las unidades, 200 réplicas por escenario, ninguna fallida):

| Efecto inyectado | Sucursales (media) | Detecta | "Nulo informativo" por error | Cobertura IC95 |
|---|---|---|---|---|
| +2.8% | 63 | 72.5% | 37.5% | 98.5% |
| +5% | 112 | 98.5% | 2.5% | 98.5% |
| −2.8% | 87 | 44% | 73.5% | 98.5% |
| −5% | 154 | 90% | 8% | 98.5% |

- **Detección de ±5%: pasa** (al menos 80%).
- **"Nulo informativo" por error con ±5%: pasa en +5% (2.5%); con −5% (8%) queda arriba del máximo de
  5%**, aunque debajo del 10% que fijamos para declarar la regla demasiado laxa.
- **El efecto mínimo detectable analítico de 2.8% es optimista** cuando el efecto se concentra en pocos
  municipios: en esa magnitud se detecta 72.5% y 44% de las veces, no 80%.

**Decisión (2026-11-05).** Lo que el diseño sostiene es que no hubo efectos mayores a ±5%. La cota de
±2.4% es la del intervalo de la especificación principal, depende en parte de la comparación contra los
nunca tratados y no se afirma como conclusión; solo por calendario, el intervalo va de −4.2% a +0.3%.
La afirmación de que una atracción pequeña estaba menos acotada que el desplazamiento se retira: el
+6.8% se apoya en esa misma comparación. Se cambió así el resumen, la introducción, las limitaciones y
las conclusiones del trabajo final, con un apéndice nuevo, y las láminas 10 y 14 del deck de PPII.
`entregables/03_presentacion/` no se tocó: lo reemplaza el deck de `06_politica_publica/`.

## Propuestas y pendientes

> **Nota del 2026-09-26.** El rediseño cierra P-1, P-2, P-6 y P-7 en el sentido que indica la
> columna "propuesta actual"; se conservan aquí porque las alternativas siguen corriéndose como
> robustez.

| # | Tema | Propuesta actual | Alternativas | Evidencia para decidir |
|---|---|---|---|---|
| P-1 | **Ventana y resultados por sector** | Panel 2019T1–2024T4 con sucursales (por sector todo el periodo) como resultado principal; contratos/cajeros/TPV/transacciones por sector solo 2022T4+ (NaN antes, sin imputar). | (a) Panel de contratos 2022T4–2025T4 (13 trimestres) con cohortes 2023T1–2024T1; (b) usar "banca" combinada 2019–2022T3 aceptando el efecto mecánico solo como secundario; (c) extender el panel base a 2025T4. | `docs/data_audit.md` P1: contratos por sector solo desde 2022T4. Cohortes 2022T1–2024T1 (P7). |
| P-2 | **Municipios ya tratados en 2019T1** (495, herencia Bansefi/Banjercito) | Excluirlos (CS los descarta como tratados). | Usarlos como control al estilo Fonseca y Matray (2024): ya tenían el canal de dispersión de programas; recodificar G = 0 en una especificación alterna. | P5: son grandes y urbanos (mediana 45 mil adultos, 80% con banca múltiple) → poco comparables con cohortes rurales. |
| P-3 | **Grupo de comparación** | Aún no tratados (`notyettreated`). | Nunca tratados (501; 20%) como robustez. | P6: nunca tratados mucho más pequeños (mediana 1,596 adultos), 83% rurales, 4% con banca múltiple. |
| P-4 | **Anticipación δ** | **Cerrada (2026-09-30):** δ = 0 base; δ = 1 robustez en el diseño escalonado (no cambia el nulo financiero). | δ = 2 (obra SEDENA visible meses antes). | ASF: sucursales construidas ≫ operando en 2022. |
| P-5 | **Covariables previas** | **Cerrada (2026-09-29):** log población 2020, índice de marginación 2020, banca múltiple municipal 2019T1 (BDIF), log(1 + establecimientos 2016S1). DR. | Agregar tipo de población CNBV, rezago social CONEVAL (solo 2023T1+). | `config/parametros.yaml`; diccionarios. |
| P-6 | **Denominador** | **Cerrada (2026-09-29):** población adulta CNBV fija en 2022T4. | Serie propia CONAPO (15+ exacto o 18+ aprox.) interpolada al trimestre, consistente en todo el panel. | P4: CNBV = 15+, salta de proyección CONAPO a Censo 2020 fijo en 2022T4 y a nueva vintage en 2025T1. |
| P-7 | **Crosswalk municipal** | Colapsar 22 hijos con su padre (`cve_estable`), sumando conteos. | Eliminar los 22 hijos y 21 padres; o dejar hijos como unidades desde su alta (panel desbalanceado). | `crosswalk_municipios.md`; Juan José Ríos tiene 3 donantes (77% del principal). |
| P-8 | **Banjército** | **Cerrada (2026-10-07, fase 2):** el modelo Power Pivot del Portafolio separa Banjército por municipio y mes 2022-01–2026-07; con el Banco del Bienestar observado cambian 9 municipios y ningún ATT financiero se mueve más de 0.73 ee (`fase2_tratamiento_obs.csv`). Antes: **Resuelto en lo principal (2026-09-15):** el Portafolio de Información CNBV separa Banjército por municipio (2016-01 – 2021-12). G se define con `suc_bienestar` (`sucursales_bienestar.parquet`). Pendiente menor: 8 municipios `sospechoso_banjercito_nuevo` (aperturas de Banjército 2022+ no observables) se excluyen en robustez. | Pedir a la CNBV/Banjército hojas planas 2022+ o el directorio; usar directorio BABIEN 2026 como respaldo. | `docs/data_audit.md` P2: 12 municipios 'solo Banjército', 5 cohortes con G falso, ya tratados 495→484, cohortes 1475→1485. |
| P-9 | **Cierres / irreversibilidad** | G = primera entrada; reaperturas como continuidad. Robustez sin los 41 municipios con cierres (2026-10-02). | Excluir los 21 municipios con salidas temporales. | P8: 21 municipios, 16 reabren. |
| P-10 | **Corresponsales** | **Cerrada (2026-09-29):** secundaria, estimada entre las rupturas 2020T4 y 2024T1 (2021T1–2023T4). | No usar. | P11. |
| P-11 | **Compartamos** | Sucursales de banca múltiple con escalón en 2019T1 (dejan de contarse los módulos). Como el panel inicia en 2019T1 no afecta la base; sí la robustez 2016–2018 (restar `modulos_compartamos`). | — | P12. |
| P-12 | **Distancia** | **Sustituida (2026-09-29):** `dist_bb_km` (distancia a la localidad con sucursal del Banco del Bienestar más cercana) define controles y derrame. | Borde a borde; usar coordenadas de sucursales (no disponibles para banca múltiple). | `variables/distancia.py`. |
| P-13 | **Formato de los entregables** | **Cerrada (2026-10-02):** Quarto → PDF (trabajo y metodología) y reveal.js (presentación). | Quarto / LaTeX / Word. | `entregables/*/README.md`. |

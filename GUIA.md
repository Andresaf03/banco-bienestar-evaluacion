# Guía del proyecto: Banco del Bienestar y actividad financiera y económica local

Guía de trabajo para el equipo (Álvarez, Barba, Islas). Resume qué se hizo, con qué datos, bajo qué
supuestos, qué se corrió y qué salió. Está escrita para leerse de corrido y para consultarse antes
de la presentación. El detalle técnico vive en `CLAUDE.md`, `docs/decisiones.md` y
`docs/data_audit.md`; aquí se enlaza en vez de repetir.

**Estado al 7 de octubre de 2026.** Análisis cerrado. La corrida final completa (3 de octubre)
reproduce exactamente todos los resultados. Entregables renderizados. Falta la revisión del equipo
antes de la entrega del **15 de octubre**.

## Índice

1. [La pregunta y la respuesta corta](#1-la-pregunta-y-la-respuesta-corta)
2. [La política](#2-la-política)
3. [Datos](#3-datos)
4. [Cómo se construyen tratamiento, muestras y resultados](#4-cómo-se-construyen-tratamiento-muestras-y-resultados)
5. [Diseño y supuestos](#5-diseño-y-supuestos)
6. [Inferencia y criterios de decisión](#6-inferencia-y-criterios-de-decisión)
7. [Qué se corrió, cuándo y con qué comando](#7-qué-se-corrió-cuándo-y-con-qué-comando)
8. [Resultados](#8-resultados)
9. [Preregistrado contra exploratorio](#9-preregistrado-contra-exploratorio)
10. [Problemas que tuvimos y cómo se resolvieron](#10-problemas-que-tuvimos-y-cómo-se-resolvieron)
11. [Limitaciones vigentes](#11-limitaciones-vigentes)
12. [Preguntas probables y cómo responderlas](#12-preguntas-probables-y-cómo-responderlas)
13. [Entregables](#13-entregables)
14. [Mapa del repositorio y comandos](#14-mapa-del-repositorio-y-comandos)
15. [Pendientes](#15-pendientes)
16. [Fase 2: fuentes nuevas (7 de octubre)](#16-fase-2-fuentes-nuevas-7-de-octubre)

---

## 1. La pregunta y la respuesta corta

**Pregunta (la de la propuesta).** ¿La llegada de la primera sucursal del Banco del Bienestar a un
municipio **atrajo o desplazó** la actividad financiera privada —banca múltiple y entidades de
ahorro y crédito popular (EACP: SOCAP y SOFIPO)— frente a municipios que la recibieron después? ¿Fue
mayor donde no había banca? Complementaria: ¿cambió la actividad económica del lugar?

**Respuesta corta.**

1. **El banco sí bancarizó donde abrió.** Unos 13 contratos de captación y 24 tarjetas de débito
   propios más por cada 100 adultos; las sucursales totales suben +2 por 10 mil adultos justo en
   la fecha de apertura, con previos planos.
2. **No atrajo ni desplazó a la banca privada.** Sucursales privadas +0.7% (el intervalo al 90%
   descarta más de ±2.4%); captación y crédito privados −0.2% y −0.1%. Nulo informativo, con
   tendencias previas planas, y el mismo resultado en un DiD apilado y con datos hasta 2025.
3. **En actividad económica no hay un efecto que podamos atribuir a la sucursal.** El DENUE registra
   ~10% más establecimientos en las localidades con sucursal en la actualización censal de 2024,
   pero sin dosis, extendido a las localidades vecinas y ausente en los Censos Económicos
   municipales y en el empleo formal.
4. **Sin heterogeneidad financiera por desierto bancario** (la segunda pregunta de la propuesta).

**Lectura de política.** La red funcionó como canal de dispersión de programas sociales, no como
palanca del sistema financiero local: un banco que no presta no cambia las condiciones que enfrentan
la banca privada ni las empresas.

---

## 2. La política

| Hecho | Fuente |
|---|---|
| 2019: Bansefi se convierte en Banco del Bienestar (<500 sucursales) | PND 2019–2024; ASF (2023) |
| Meta: 7,000 → 2,700 → **2,744** sucursales, construidas por la SEDENA en inmuebles federales | ASF (2023) |
| Ubicación: zonas prioritarias definidas por Bienestar, Coordinación de Programas y SEDENA | ASF (2023) |
| 15 dic 2022: 1,873 terminadas; **922 operando** al cierre de 2022 | ASF (2023) |
| 2022: **sin crédito** de primer ni segundo piso; prioridad dispersar programas | ASF (2023) |
| Rezago de 55% en 2022; los 26 municipios más pobres sin sucursal; 674 empleados para todas las sucursales | IMCO (2022) |
| Línea institucional: Pahnal (1949) → Bansefi (2001) → Banco del Bienestar (2019) | Aportela (1999); ASF (2023) |

Consecuencias para el diseño: la ubicación **no es aleatoria**; el tratamiento se fecha con
sucursales **operando**, no con obra; y como el banco dispersa programas en cuentas propias, sus
cuentas suben "por construcción" (efecto mecánico), así que los resultados principales **excluyen
al propio banco**.

---

## 3. Datos

Todo lo descargado está en `data/raw/` con su huella en `data/raw/MANIFEST.csv`; lo que tuvo que
bajarse a mano está en `data/manual/` y documentado en `docs/descarga_manual.md`.

| Fuente | Qué trae | Nivel y periodo | Uso |
|---|---|---|---|
| **BDIF, CNBV** | Sucursales, cajeros, TPV, corresponsales, contratos de captación y crédito, tarjetas, por sector | Municipio, trimestral, 2016T1–2025T4 (40 trimestres) | Tratamiento y resultados financieros |
| **Portafolio de Información, CNBV** | Operativa por institución y localidad | Mensual, 2016-01 – 2021-12 | Separar Banjército del Banco del Bienestar |
| **Directorio del Banco del Bienestar** | Sucursales georreferenciadas, sin fecha | Foto 2026T1 (manual) | Ubicar la sucursal en su localidad |
| **DENUE, INEGI** | Establecimientos georreferenciados con SCIAN y personal ocupado | 18 versiones semestrales 2016–2025 (no hay 2023S1) | Actividad local por localidad |
| **Censos Económicos, INEGI** | Unidades, personal, remuneraciones, VACB, producción | Municipio, 2004–2024 (5 censos) | Actividad sin depender del padrón |
| **IMSS (datos abiertos)** | Puestos afiliados por tamaño de patrón, salario | Municipio (catálogo propio), cierres de trimestre 2019–2025 | Empleo formal |
| **Banxico, CE166** | Remesas | Municipio (por nombre), trimestral | Canal de remesas (descriptivo) |
| **ENIF 2018, 2021, 2024** | Tenencia de cuenta | Nacional, por tamaño de localidad (tabulados) | Contraste descriptivo |
| **Censo 2020 (ITER) y 2010** | Población, escolaridad, viviendas | Localidad y municipio | Denominadores, covariables, crosswalk |
| **CONAPO** | Índice de marginación 2010–2020; proyecciones | Municipio | Covariable |
| **Marco Geoestadístico 2024** | Polígonos y catálogos | Municipio | Validación espacial |
| **Fase 2** (7 oct, §16) | | | |
| Portafolio CNBV, modelo Power Pivot | Sucursales por institución (Banco del Bienestar y Banjército por separado) | Municipio, mensual, 2022-01 – 2026-07 | Tratamiento observado (P-8) |
| EIC 2015, Censo 2020 (ampliado), EIC 2025 | Posición en el trabajo, ocupación, ingreso, programas, remesas, TIC | Municipio, 3 cortes | Emprendimiento medido en personas y mecanismo |
| VIIRS VNL V2 (Zenodo) | Luz nocturna anual, 500 m | Localidad (1 km y anillo de 1–3 km), 2016–2024 | Actividad continua y gradiente |
| EFIPEM | Impuestos, predial, derechos | Municipio, anual 2016–2024 | Actividad formal (no informativo) |
| ENOE / ENOE^N | Dueños de negocio, informalidad, ingreso | Municipio, trimestral 2019–2025 | Réplica de Bruhn y Love (sin potencia) |

---

## 4. Cómo se construyen tratamiento, muestras y resultados

**Tratamiento.**

- `G` = primer periodo con al menos una sucursal del Banco del Bienestar **en operación**, neta de
  Banjército (`data/interim/sucursales_bienestar.parquet`). `G = 0` = nunca tratado.
- Banjército: observado con el Portafolio hasta 2021 y extrapolado después; 8 municipios quedan como
  sospechosos y salen.
- **Ya tratados en 2019T1** (487 municipios con sucursal heredada de Bansefi): salen, porque el
  estimador no puede usarlos como tratados.
- **Localidad:** se combina la fecha municipal de la BDIF con el directorio. Donde el municipio tiene
  una sola sucursal (1,270 casos) la fecha identifica a la localidad; con dos o más se marca
  `fecha_ambigua` y sale.
- Validación: BDIF 2025T4 contra el directorio 2026T1, 99.9% de coincidencia municipal.
- El 86% de los municipios tratados abre una sola sucursal → el tratamiento es **binario**.

**Paneles** (`make panel`, `src/proyecto/construccion/panel.py`).

| Panel | Unidades × periodos | Para qué |
|---|---|---|
| `panel_localidad` | 69,137 localidades × 18 semestres | DENUE, especificación principal de actividad |
| `panel_municipio` | 2,456 municipios × 18 semestres | DENUE municipal (secundaria) |
| `panel_municipio_trim` | 2,456 × 28 trimestres (2019T1–2025T4) | BDIF, IMSS, remesas |
| `panel_municipio_trim_largo` | 2,456 × 40 trimestres (2016T1–2025T4) | Robustez con pre-periodo largo |
| `panel_municipio_ce` | 2,456 × 5 censos | Censos Económicos |
| `panel_anillo` | Radios de 1, 2, 5 y 10 km | Solo descriptivo |

**Resultados.**

- *Financieros (por 10 mil adultos, denominador fijo de 2022T4):* sucursales privadas (banca
  múltiple + EACP), de banca múltiple y de EACP; captación y crédito privados (solo desde 2022T4);
  captación, crédito y tarjetas de EACP (continuos); primera etapa con sucursales totales y cuentas
  del banco.
- *DENUE (por mil habitantes del Censo 2020):*
  - "emprendimiento" = todos los establecimientos, más micronegocios (0–5 personas) y empleo
    estimado;
  - "consumo" = comercio al por menor (46) y alimentos y bebidas (722);
  - "salud" = servicios médicos (62) y farmacias.
- *Censos Económicos:* unidades y personal por mil habitantes; logaritmo de remuneraciones, valor
  agregado (VACB) y producción.
- *IMSS:* puestos totales, micro (1–5) y pequeños (6–50) por 10 mil adultos; logaritmo del salario
  diario.

**Covariables previas** (las mismas en todo): logaritmo de la población 2020, índice de
marginación 2020, banca múltiple en el municipio en 2019T1 y logaritmo de los establecimientos del
DENUE en 2016S1.

**Controles de localidad.** Localidades **sin sucursal propia a ≥10 km** de cualquier localidad con
sucursal. Antes el 91% de los "nunca tratados" estaba en un municipio que abrió una sucursal; esos
controles estaban contaminados.

---

## 5. Diseño y supuestos

**Estimador.** Callaway y Sant'Anna (2021), doblemente robusto, con los municipios **aún no
tratados** como comparación (solo hay ~500 nunca tratados, más pequeños y rurales). En la BDIF se
reporta el efecto global y el estudio de evento.

**Supuestos y cómo se defienden.**

| Supuesto | Qué significa aquí | Cómo lo evaluamos |
|---|---|---|
| Irreversibilidad | Una vez abierta, la sucursal cuenta como tratamiento | 41 municipios con cierres: excluirlos no cambia nada (P-9) |
| Anticipación limitada | La sucursal no afecta antes de abrir | Robustez con anticipación de un trimestre; pero la obra de SEDENA es anterior y no observable |
| Tendencias paralelas condicionales | Sin sucursal, tratados y aún no tratados habrían evolucionado igual, dadas las covariables | Pre-prueba puntual y Wald conjunta; placebo; HonestDiD |
| Traslape | Para cada tipo de unidad hay comparables | Emparejamiento con diferencias estandarizadas < 0.06; régimen censal |
| SUTVA | La sucursal no afecta a los controles | Controles a ≥10 km; derrame y bandas de distancia por separado |

**Diseño del DENUE: entre actualizaciones.** El DENUE solo se actualiza por completo con los
Censos Económicos: las versiones 11/2019 y 11/2024, verificado en los comunicados del INEGI. Entre
ellas casi no se mueve: en 2022 cambia ~10% de las localidades tratadas por versión, contra 83% en
cada actualización.

- *Periodos:* 2016S1 y 2019S1 (antes), 2019S2 (actualización previa), 2024S1 y 2024S2
  (actualización posterior).
- *Cohorte:* todas las aperturas de 2020S1 a 2024S1 forman una sola, fechada en 2024S1.
- *Estimando:* el efecto en 2024S2. *Placebo:* el salto de la actualización de 2019, previo a toda
  apertura.

---

## 6. Inferencia y criterios de decisión

- **Errores estándar** agrupados por municipio, con la función de influencia. El bootstrap del
  paquete `did` los inflaba ~10× con municipios desiguales; se guarda solo como `ee_boot`.
- **Pre-tendencias** auditadas en cada especificación: coeficientes previos significativos y Wald
  conjunta.
- **HonestDiD** (Rambachan y Roth, 2023): intervalo robusto cuando la violación posterior es
  $\bar M$ veces la mayor previa.
- **Pruebas múltiples:** Romano–Wolf en familias preregistradas (DENUE, financiera, EACP, IMSS, CE);
  Benjamini–Hochberg en el resto.
- **Nulo informativo:** solo si el IC al 90% queda dentro de **±5%** de la media previa de las
  tratadas (prueba de equivalencia).
- **Regla de descarte:** si la Wald previa da p < 0.05, el resultado se reporta como descriptivo.

---

## 7. Qué se corrió, cuándo y con qué comando

| Fecha | Qué | Comando | Tiempo |
|---|---|---|---|
| 29 sep | Revisión de código; hallazgos C1–C3; **preregistro** de la corrida final | — | — |
| 30 sep | Batería principal preregistrada | `make bateria` | 13 min |
| 30 sep | Fase 0: BDIF hasta 2025, EACP, inclusión, primera etapa, desierto bancario | `make bateria-financiera` | ~32 min |
| 30 sep | Fase 1: Censos Económicos, IMSS, remesas, ENIF | `make bateria-fase1` | ~12 min |
| 2 oct | Diseños alternativos (DiD apilado, bandas de distancia) e intensidad | `make bateria-alternativos` | 25 s |
| 2 oct | Régimen censal (exploratorio) y robustez sin cierres | `08_disenos_alternativos.R regimen`, `05_robustez.R cierres` | 1.5 min |
| 2 oct | Entregables en Quarto | `make entregables` | 12 s |
| **3 oct** | **Corrida final completa**: de los paneles a los entregables | `make bateria` | **55 min** |

**Qué hace `make bateria`** (`scripts/bateria_final.sh`), en orden:

1. Pruebas (84) y lint.
2. Borra las salidas de estimación anteriores.
3. Construye los paneles.
4. Emparejamiento.
5. Descriptivos y ENIF.
6. Estimación: 77 especificaciones, 268 filas con todos los estimadores.
7. Robustez (~46 min, la parte pesada).
8. Heterogeneidad.
9. Inferencia múltiple y tabla final.
10. Diseños alternativos.
11. Reporte.
12. Entregables.

El registro queda en `outputs/logs/`. La corrida del 3 de octubre reproduce **exactamente** la tabla
final: mismo efecto, error estándar, Wald y Romano–Wolf en las 77 especificaciones.

---

## 8. Resultados

Tabla completa: `outputs/tablas/tabla_final.csv`. Reporte con todas las variantes:
`entregables/04_final/resultados_preliminares.md`.

**Primera etapa.**

| Resultado | Efecto | Previos |
|---|---|---|
| Sucursales totales | +2.00 por 10 mil adultos (ee 0.08) | planos |
| Contratos de captación del banco | +1,268 por 10 mil adultos | planos |
| Tarjetas de débito del banco | +2,412 por 10 mil adultos | planos |

**Actividad financiera privada (1,457 municipios tratados contra 500).**

| Resultado | Efecto | Se descarta más de | Wald previa p | DiD apilado |
|---|---|---|---|---|
| Sucursales privadas | +0.7% | ±2.4% | 0.29 | +0.8% (previos planos) |
| Banca múltiple | −0.2% | ±2.8% | 0.055 | +0.7% |
| EACP | +1.5% | ±4.3% | 0.52 | +0.8% |
| Captación privada (2022T4+) | −0.2% | ±4.2% | 0.68 | — |
| Crédito privado (2022T4+) | −0.1% | ±1.8% | 0.36 | — |
| Captación de ahorro EACP | +0.5% | ±2.5% | 0.51 | −0.2% |
| Crédito al consumo EACP | +4.3% (Romano–Wolf p = 0.008) | — | 0.18 | +3.9%, **previos reprueban** → descriptivo |

**Actividad económica.**

- **DENUE.** 1,106 localidades tratadas contra 21,719 controles.
  - *Establecimientos:* +10.4% (+7.24 por mil, ee 1.10); placebo de 2019 +1.71 (ee 1.25); Wald
    previa p = 0.057.
  - *Micronegocios y empleo estimado:* +10.9% y +10.6%.
  - *Comercio y salud:* +8.2% y +9.6%, pero reprueban la pre-prueba.
  - *Robustez:* aguanta controles a 5 y 20 km, piso de 1,000 habitantes, post en 2025S1, cluster
    estatal y emparejamiento (+9.7%).
  - *HonestDiD:* incluye el cero con $\bar M = 1$.
- **¿Es efecto de la sucursal? Cuatro pruebas dicen que no:**
  - *Sin dosis:* las aperturas de 2022 dan +11.2% y las de 2023–24 +10.0% (p = 0.68).
  - *Efecto de zona:* las vecinas sin sucursal a menos de 2 km ganan lo mismo (+11.7%, p = 0.53);
    a 5–10 km, +0.9%.
  - *Régimen censal (exploratorio):* los CE recorren completas las cabeceras y localidades de 2,500+
    y muestrean lo rural; el 82% de las tratadas está en el recorrido total contra el 2.2% de los
    controles. Dentro del recorrido total el efecto se mantiene (+9.8%, previos planos, robusto a
    $\bar M = 1$): el régimen **no** lo explica, pero sigue siendo de zona.
  - *Censos Económicos municipales:* unidades −0.9% (se descarta más de ±4%), con tres placebos
    planos.
- **IMSS.** El salario baja 1.9% (−1.4% en el apilado, significativo pero dentro de ±5%); los
  puestos no son informativos.
- **Remesas.** Reprueban la pre-prueba; son descriptivas.
- **ENIF.** La tenencia de cuenta sube casi igual en lo rural (38→51%) que en lo urbano (55→69%),
  2021–2024.

**Heterogeneidad.**

- *Desierto bancario:* sin diferencias en finanzas (q ≥ 0.6). En el DENUE el aumento es mayor en
  desiertos (12.3% contra 5.3%, q = 0.04).
- *Marginación:* mayor en media y alta (q ≈ 0.10).
- *Exposición:* sin diferencia.

**Lectura defendible del +10%.** Es un aumento robusto del padrón en la zona de la cabecera que
recibió sucursal. Es compatible con tres explicaciones: que las sucursales se ubicaran donde ya se
esperaba crecimiento, que lo cause la obra de SEDENA, o que los establecimientos se reubicaran dentro
del municipio. **No** lo leemos como efecto causal de la sucursal.

---

## 9. Preregistrado contra exploratorio

| Análisis | Estatus | Dónde |
|---|---|---|
| Especificación principal (DENUE entre actualizaciones; BDIF escalonada), familias de Romano–Wolf, umbral ±5% | Preregistrado 29 sep | `docs/decisiones.md` |
| Fase 0 (BDIF a 2025, EACP, primera etapa, desierto) | Preregistrado 30 sep | idem |
| Fase 1 (CE, IMSS, remesas, ENIF) | Preregistrado 30 sep | idem |
| DiD apilado, bandas de distancia, intensidad | Preregistrado 2 oct (con nota: la prueba de humo ya había mostrado emprendimiento por bandas y dos series apiladas; los parámetros no cambiaron) | idem |
| Régimen censal, robustez sin cierres | **Exploratorio** (plan escrito antes de estimar, pero después de ver el descriptivo) | idem |

---

## 10. Problemas que tuvimos y cómo se resolvieron

| Problema | Efecto | Solución |
|---|---|---|
| Bootstrap agrupado de `did` | Errores estándar ~10× más grandes | Varianza agrupada con la función de influencia |
| Controles contaminados | 91% de los "nunca tratados" en municipios que abrieron | Controles a ≥10 km |
| Ceros falsos en cajeros y TPV | Valían 0 en todo el país antes de 2022T4 | Relleno con 0 solo desde que la CNBV publica |
| "Nulo preciso" del DENUE | Era falta de medición entre censos | Diseño entre actualizaciones |
| Banjército en la banca de desarrollo | Fechas de tratamiento falsas | Portafolio de la CNBV |
| Población adulta con saltos (2020T4) | Escalones de −20% a +13% en las tasas | Denominador fijo 2022T4 |
| Captación y crédito por sector solo desde 2022T4 | Falso efecto de +177 por salto de cobertura | Regla 10: dos periodos previos con dato; panel corto |
| IMSS: codificación mixta y tamaños en mayúscula | Micro en 0 | Detección de codificación y nueva descarga |
| Resultados en logaritmo | % mal escalados en la tabla final | Puntos log × 100 |
| Agregaciones con una sola cohorte (CE) | Fallaban | Se calculan solo con varias cohortes |
| `bacondecomp` no cabía en memoria | — | Goodman-Bacon en forma cerrada, validado contra el TWFE |
| `didimputation` fuera de `renv.lock` | BJS se saltaba en una instalación limpia | Registrado |
| Lectura del régimen censal | El descriptivo bruto sugería medición | La estimación con covariables lo descartó; corregido en los documentos |

---

## 11. Limitaciones vigentes

**Tratamiento e identificación**

- Ubicación no aleatoria. Las pre-pruebas, los controles alejados, el emparejamiento y HonestDiD
  acotan el sesgo, pero no lo eliminan.
- Sin fechas de obra ni de apertura por sucursal: no se separa el efecto de la obra del de la
  apertura.
- Validez externa: los 487 municipios ya tratados (grandes, urbanos) salen. Los resultados valen
  para municipios más pequeños que abrieron después.
- Pocos nunca tratados; las cohortes de 2024 tienen poco periodo posterior.

**Localidades**

- Solo se fechan bien los municipios con una sola sucursal (1,270). El piso de 50 habitantes deja
  fuera 412 localidades con sucursal.
- El soporte común dentro del régimen censal es angosto (478 controles).
- El efecto del DENUE es de zona, así que la localidad no es una unidad aislada.

**Variables respuesta**

- *BDIF:* contratos y transacciones por sector solo desde 2022T4. Los corresponsales cambian de
  metodología (2019, 2020, 2024). Compartamos tiene un escalón en 2019. Las cuentas en celular del
  banco valen 0.
- *DENUE:* solo dos actualizaciones completas en la ventana; falta 2023S1. El sector financiero
  (SCIAN 52) tiene seis rupturas, así que no se usa. El empleo es estimado por rangos.
- *Censos Económicos:* solo municipales y cada cinco años, con año de referencia 2023. Personal
  ocupado no es informativo.
- *IMSS:* solo empleo formal; cruce por nombre; CDMX sin municipio (16% de los puestos).
- *Remesas:* reprueban la pre-prueba. *ENIF:* no es municipal.

**Escolaridad**

- *Disponible:*
  - grado promedio de escolaridad municipal del Censo 2020, ya en
    `data/interim/inegi_censo_2020.parquet`;
  - el mismo indicador por localidad en el ITER 2020 crudo (99.7% de las 69,137 localidades del
    panel, sin extraer);
  - analfabetismo y población sin básica completa de CONAPO, que entran solo dentro del índice de
    marginación.
- *No se usa* como covariable separada ni como dimensión de heterogeneidad.
- *No puede* ser variable respuesta: hay un solo corte, 2020, antes del tratamiento.
- *Por qué importaría:* Fonseca y Matray (2024) encuentran que los efectos crecen con la educación.
  Sería la prueba natural de ese mecanismo, pero como análisis exploratorio.

**Qué cambió con la fase 2 (7 de octubre, §16)**

- *Banjército (P-8):* cerrada. Se observa directamente desde 2022 y los resultados no cambian.
- *Fechas de obra o apertura por sucursal:* siguen sin existir en datos públicos. No hay versiones
  históricas del directorio para 2022–2024 (ni en Wayback ni en datos.gob.mx) y la cartera de la
  SHCP agrupa las sucursales en lotes. Solo una solicitud de información las resolvería.
- *El +10% del DENUE:* ahora hay dos medidas más que no lo reproducen. La proporción de dueños de
  negocio en las encuestas intercensales no aumenta (IC90 entre −10% y +1.8%) y la luz nocturna
  tampoco.
- *Validez externa:* la ENOE no alcanza. Solo 367 municipios aparecen en todos los trimestres y en
  la estimación quedan 146 tratados contra 12 controles.
- *Población por localidad:* no hubo Conteo 2025; la EIC 2025 solo es representativa por municipio.
  La hipótesis de "se ubicó donde se esperaba crecimiento" solo se puede ver a nivel municipal:
  población +2.3%, sin sobrevivir la corrección múltiple.

---

## 12. Preguntas probables y cómo responderlas

> La versión completa y vigente (2026-11-18), con las preguntas de la presentación de PPII, está en
> `docs/contexto/preguntas_defensa.md`. Lo de abajo es la versión de octubre, corregida donde la
> fase 6 cambió la lectura.

**¿Por qué no TWFE?** Con adopción escalonada y efectos heterogéneos, el TWFE promedia
comparaciones "prohibidas" con pesos que pueden ser negativos (Goodman-Bacon, 2021). Lo reportamos
como contraste. En el panel completo del DENUE, el 98.8% de su peso viene de comparar tratadas
contra no tratadas.

**¿Por qué aún no tratados y no nunca tratados?** Los nunca tratados son ~500, más pequeños y
rurales. Con nunca tratados como control el nulo financiero no cambia; está en la robustez.

**¿Por qué la localidad y no el municipio?** Una sucursal no mueve el agregado de un municipio
grande. Además, el municipio entre actualizaciones reprueba su placebo (−19.8, ee 6.9). La BDIF sí
es municipal porque así se publica.

**¿El +10% del DENUE no es un efecto?** Es un aumento robusto en el padrón, concentrado a menos de
3 km de la sucursal (más del 90%), pero:

- no crece con la exposición;
- no se concentra en el comercio, que ya crecía más antes de abrir;
- no es mayor donde viven más adultos mayores;
- no aparece en los Censos Económicos.

Con la regla preregistrada de la fase 6, no se distingue entre gasto de los programas y medición.

**¿Y si la diferencia es por cómo el INEGI levanta el censo?** Lo probamos: dentro del mismo régimen
de levantamiento el aumento se mantiene. No es eso.

**¿Por qué excluyen al propio banco?** Porque dispersa programas sociales en cuentas propias: sus
cuentas suben por construcción. Lo medimos aparte, como primera etapa.

**¿Cómo saben que el nulo no es falta de potencia?** Por la prueba de equivalencia y el efecto
inyectado. Los intervalos al 90% descartan efectos mayores a ±5%, por debajo del +7.6% de Bruhn y
Love (2014), y un efecto de ±5% inyectado en los datos se detecta entre 90% y 98% de las veces.

**¿Qué pasa con Banjército?** Se descuenta con el Portafolio de la CNBV. Los 8 municipios dudosos
salen; incluirlos no cambia nada.

**¿Escolaridad?** Ver §11: hay dato, no se usó, y solo serviría como heterogeneidad exploratoria.

**¿Y si el DENUE simplemente es más preciso que las encuestas?** La EIC mide algo distinto (personas
que son dueñas de un negocio, no establecimientos), pero es la medida más cercana a Bruhn y Love, y
su intervalo descarta aumentos mayores a +1.8%. Junto con los Censos Económicos y la luz nocturna,
tres fuentes independientes del padrón no ven el aumento.

**¿Por qué la luz nocturna "falla" la pre-prueba?** En estos datos el cambio anual de la luz depende
del brillo del lugar: las rancherías oscuras (los controles) y los pueblos iluminados (las tratadas)
no siguen la misma tendencia, y además el producto cambia de versión en 2022. Comparando solo
localidades con sucursal por su fecha de apertura, la pre-prueba pasa y el efecto es nulo.

**¿Qué pasó con Banjército?** Antes se extrapolaba después de 2021. Con el modelo del Portafolio
de la CNBV se observa directamente: cambian 9 municipios y ningún resultado se mueve.

**¿El banco amplió la cobertura de programas?** Los hogares con programas suben 2.1 puntos donde abrió,
pero la pre-prueba falla, así que no lo afirmamos como efecto. En febrero de 2023 la Coordinación de
Becas empezó a entregar tarjetas del Banco del Bienestar para pagar las becas Benito Juárez
(comunicado del 1 de febrero de 2023), lo que es consistente con el canal de dispersión.

---

## 13. Entregables

| Entrega | Fuente | Salida |
|---|---|---|
| 1. Propuesta | `entregables/01_propuesta/` | ya entregada (PDF versionado) |
| 2. Metodología | `entregables/02_metodologia/metodologia.qmd` | `metodologia.pdf` (6 págs.) |
| 3. Presentación | `entregables/03_presentacion/presentacion.qmd` | `presentacion.html` (14 láminas, autocontenido; para PDF: `?print-pdf` e imprimir) |
| 4. Trabajo final | `entregables/04_final/trabajo_final.qmd` | `trabajo_final.pdf` (14 págs.; desde el 7 de octubre con el anexo de la fase 2 y una lámina de respaldo en la presentación) |
| Anexo | `entregables/04_final/resultados_preliminares.md` | reporte completo de la batería |

`make entregables` regenera figuras (`outputs/figuras/fig_*.png`), tablas
(`entregables/_tablas/*.md`) y los tres documentos en ~15 s, sin volver a estimar. **Las tablas
salen de los datos; las cifras dentro del texto están escritas a mano**: si algo cambia en la
batería, hay que revisarlas. Los PDF y el HTML no se versionan.

---

## 14. Mapa del repositorio y comandos

```
config/              fuentes.yaml (URLs verificadas) · parametros.yaml (todo el diseño)
data/raw/            descargas inmutables + MANIFEST.csv     data/manual/  descargas a mano
data/interim/        limpieza por fuente (parquet)           data/processed/  paneles
src/proyecto/        descarga/ · limpieza/ · construccion/ (panel, tratamiento, matching) · utils/
analisis/            00_utils · 01_descriptivos · 02_cs_did · 03_twfe_comparacion
                     04_heterogeneidad · 05_robustez · 06_correr_todo · 07_inferencia
                     08_disenos_alternativos · 09_figuras_entregables
outputs/tablas/      tabla_final · maestra_resultados · rob_* · het_* · apilado_* · decaimiento_* · regimen_* · desc_*
outputs/figuras/     event_* · desc_* · fig_* (entregables)
docs/                decisiones.md (bitácora y preregistros) · data_audit.md · contexto/ · diccionarios/
entregables/         01–04 + _tablas/
```

| Comando | Qué hace |
|---|---|
| `make setup` | Entornos de Python (`uv`) y R (`renv`) |
| `make descargar` / `make limpiar` / `make panel` | Datos |
| `make bateria` | Todo, una vez (~55 min) |
| `make estimar`, `robustez`, `heterogeneidad`, `inferencia`, `alternativos` | Pasos sueltos |
| `make entregables` | Documentos |
| `make test` / `make lint` | 94 pruebas (10 de la fase 2) / ruff |

En esta Mac usa `/Library/Developer/CommandLineTools/usr/bin/make` y `.../git` (la licencia de Xcode
rompe `/usr/bin/make`). No edites `analisis/*.R` mientras corre un Rscript.

---

## 15. Pendientes

1. **Revisión del equipo** del trabajo final y la presentación, sobre todo la discusión y las
   implicaciones de política, que son interpretación nuestra.
2. **Decidir** si vale la pena sumar datos panel adicionales antes del 15 de octubre (hay un prompt
   preparado para que otro agente los explore; ver la conversación del 7 de octubre).
   *Hecho el 7 de octubre:* exploración en `docs/contexto/fuentes_panel_candidatas.md` e integración
   preregistrada en la fase 2 (§16). Falta decidir qué entra al trabajo final y a la presentación.
3. Opcional: heterogeneidad exploratoria por escolaridad (§11).
4. Siguen abiertas, sin efecto en los resultados: P-8 (Banjército residual) y P-11 (Compartamos).
   *Actualización del 7 de octubre:* P-8 quedó cerrada en la fase 2; solo sigue abierta P-11.
5. **Revisión del equipo del anexo de la fase 2** (trabajo final) y de la lámina de respaldo
   (presentación): las cifras del texto están escritas a mano a partir de
   `outputs/tablas/fase2_resumen.csv`.
6. Si se vuelve a correr `make bateria`, después hay que correr `make bateria-fase2` (la batería
   borra las salidas de estimación; `bateria-fase2` termina con el reporte y los entregables).

---

## 16. Fase 2: fuentes nuevas (7 de octubre)

**Qué es.** Cinco fuentes nuevas, cada una contra un hueco de §11. Salen del ranking de
`docs/contexto/fuentes_panel_candidatas.md` y se **preregistraron antes de estimar**
(`docs/decisiones.md`, "Preregistro de la fase 2", con una adenda sobre los datos de luz). Nada de
esto toca la maestra, la tabla final ni sus familias. Los resúmenes viven en `outputs/tablas/fase2_*`;
el resumen general es `fase2_resumen.csv`, con Romano–Wolf por familia y BH en toda la fase.

**Comandos.**

| Comando | Qué hace |
|---|---|
| `make descargar-fase2` | EIC/Censo y ENOE por streaming (solo queda su hash en MANIFEST); VIIRS (~650 MB) y EFIPEM se conservan en `data/raw/` |
| `make bateria-fase2` | limpieza → paneles (`construccion/panel_fase2.py`) → `analisis/10_fase2.R todo` → reporte (sección de la fase 2 al final) → entregables |

`make bateria` borra las salidas de estimación: después de una batería completa hay que volver a
correr `make bateria-fase2`.

**Resultados.**

| Fuente | Hueco | Resultado | Lectura |
|---|---|---|---|
| Portafolio CNBV, modelo Power Pivot 2022–2026 | fecha de tratamiento (P-8) | coincide con la BDIF en el 99.2%; con el Banco del Bienestar observado solo 9 municipios cambian de G; ningún ATT financiero se mueve más de 0.73 ee | **P-8 cerrada sin efecto** |
| EIC 2015 / Censo 2020 / EIC 2025 (municipio) | +10% del DENUE; mecanismo | dueños de negocio (patrón o cuenta propia): −1.2 puntos (ee 1.0), previos planos; el IC90 va de −10% a +1.8% de la media; sin dosis. Ocupación e ingreso por trabajo: nulos informativos | **el emprendimiento medido en personas no reproduce el +10% del DENUE** |
| EIC (mecanismo) | canal de dispersión | hogares con programas +2.1 puntos, pero la pre-prueba falla (p = 0.013); población +2.3%, trabajo en otro municipio +2.2 y celular −2.6, significativos solo sin corrección (BH q ≥ 0.11) | descriptivo |
| VIIRS (localidad, 2016–2024) | actividad continua, gradiente | luz a 1 km +0.3 puntos log (ee 0.9), pero la pre-prueba falla en casi todas las variantes. Por calendario entre localidades con sucursal pasa (p = 0.10) y da +0.15 (ee 0.83) | **no hay más luz donde abre el banco**; descriptivo |
| EFIPEM (municipio, 2016–2024) | actividad formal | impuestos −4.1 y derechos −6.4 puntos log (ee ~5); el predial reprueba la pre-prueba | no informativo |
| ENOE (municipio-trimestre) | validez externa (Bruhn y Love) | solo 146 tratados contra 12 controles en los 27 trimestres; negocio +2.1 puntos (ee 1.5); informalidad +3.9 (ee 1.6), frágil | no informativo |

**Problemas que aparecieron y cómo se resolvieron.**

- *VIIRS cambia de escala en 2022.* El entero ×10 de 2016–2021 pasa a enteros con `scale = 10`, y
  sin corregirlo la luz nacional caía 10×. Se corrigió antes de estimar.
- *VIIRS cambia de producto en 2022.* Pasa al VNL v2.2 de dos satélites y en 2023–2024 vuelve al
  v2 de SNPP. Además los cambios año a año dependen del brillo
  (`fase2_desc_viirs_ruptura.csv`): eso explica que la pre-prueba falle cuando se compara con
  rancherías oscuras.
- *Píxeles negativos* en 2016–2021: se excluyen.
- *ENOE.* El INEGI responde 200 con una página de error a los nombres que no existen; 2022T2 trae
  BOM y desde 2025T3 las claves se llaman `cve_ent`/`cve_mun`. Ya se maneja.
- *Contrastes entre bandas en logaritmos.* La función de `08_disenos_alternativos.R` divide entre
  la media (pensada para niveles); para logaritmos se usa una versión en puntos log
  (`diferencia_log`).

**Cómo cambia la lectura.**

- Refuerza la conclusión principal: el +10% del DENUE es un aumento del **padrón** en la zona de la
  cabecera, no más dueños de negocio ni más luz. Ni la EIC (personas) ni VIIRS (luz) lo reproducen,
  igual que los Censos Económicos.
- El canal de dispersión aparece (más hogares con programas donde abrió el banco), pero no está
  identificado: falla la pre-prueba.
- La validez externa sigue abierta: la ENOE no tiene potencia con la muestra balanceada.


## 17. Fase 6: programas, acceso y el DENUE (17 de noviembre)

Después de presentar en PPII nos preguntaron cuatro cosas. Preregistro, adenda y resultados en
`docs/decisiones.md`; código en `variables/accesibilidad.py`, `utils/fase6_descriptivos.py`,
`construccion/panel_fase6.py` y `analisis/16_fase6.R` (`make bateria-fase6`, unos 3 minutos).

| Pregunta | Respuesta | Tipo |
|---|---|---|
| ¿Más programas o más conveniencia? | Más cerca: los 65+ pasaron de 9.5 km a 2.9 km de una sucursal del banco; 91% de quienes reciben apoyos tienen cuenta para cobrarlos (63% en 2021). Si llegaron **más** programas no se puede saber: el padrón histórico por municipio solo existe como listas con nombre. | descriptivo |
| ¿Cumple su objetivo de dispersar mejor? | En acceso, sí: a ≤10 km de 68% a 92% de los 65+, y en marginación muy alta de 26% a 78%. Es el Objetivo 3 de su Programa Institucional. | descriptivo |
| Los radios del DENUE | En niveles, más del 90% del aumento está a menos de 3 km de la sucursal (93% ponderando por población). El perfil "plano" salía de medir cada banda en % de su propia media. | reexpresión causal |
| ¿Es gasto de los programas? | No se distingue: no se concentra en consumo, no crece con la proporción de 65+, el placebo de cabeceras es impreciso. | preregistrado |
| ¿Aguanta sin los nunca tratados? | Sí. Financiero: ninguna variante sale de ±5%. DENUE: con controles solo de municipios sin apertura, el mismo +10.4%. | causal |

**Cómo cambia la lectura.** Ya no decimos que el +10% del DENUE "no es de la sucursal" ni que "se
extiende a las vecinas": se concentra en la localidad con sucursal, pero no lo podemos atribuir al
gasto de los programas ni descartar como medición.

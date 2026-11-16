# investigacion_1 — Base de conocimiento

**Proyecto:** Evaluación del Plan de Expansión del Banco del Bienestar (sep 2021 – feb 2024) sobre la actividad financiera municipal. Panel municipio-trimestre, 2019T1–2024T4.
**Fecha de corte:** 14 sep 2026.
**Contenido:** hallazgos de los 4 papers leídos completos, las fuentes institucionales revisadas y las decisiones tomadas en el chat.

---

## 0. Resumen en 10 líneas

1. Hay tres antecedentes directos: Banco Azteca (México, 2002), Pahnal (México, 1993) y "Banco para Todos" (Brasil, 2004). Los tres encuentran efectos positivos de abrir sucursales para población de bajos ingresos.
2. El paper más parecido al nuestro es **Fonseca y Matray (2024)**: evalúa una política pública, con bancos públicos, a nivel municipal, con depósitos y crédito como resultados.
3. En Brasil, la expansión la hicieron los bancos públicos y **casi no desplazó a la banca privada**. Esto importa porque nosotros medimos solo banca múltiple y EACP, así que el efecto esperado ahí puede ser pequeño o incluso negativo.
4. Los efectos son mayores en **desiertos bancarios** y crecen con la distancia al banco más cercano. Esta es la heterogeneidad clave a probar.
5. El estimador es **Callaway y Sant'Anna (2021)**. Como casi no hay municipios nunca tratados, probablemente usemos como control a los **"aún no tratados"**.
6. No existe ninguna evaluación de impacto del plan. La ASF (2023) fiscaliza control interno y gobernanza, e IMCO (2022) revisa compras y avance de obra.
7. Metas del plan: el PND planteaba 7,000 sucursales, luego se fijaron 2,700 y finalmente 2,744. Al cierre de 2022 operaban 922. Las aperturas fueron escalonadas, lo que permite un diseño de diferencias en diferencias escalonado.
8. La ubicación no fue aleatoria. Dependió de zonas prioritarias definidas por Bienestar y SEDENA y de los inmuebles federales disponibles. Los 26 municipios más pobres no tenían sucursal (IMCO).
9. **Construida no es lo mismo que operando.** La ASF reporta 1,873 sucursales terminadas y 922 en operación. El tratamiento debe fecharse con la BDIF, que registra sucursales operando.
10. En 2022 el banco no otorgó crédito. Su función real fue dispersar programas sociales, lo que confirma el riesgo de efecto mecánico.

---

## 1. Papers núcleo

### 1.1 Bruhn y Love (2014): Banco Azteca

- **Cita:** Bruhn, M., y Love, I. (2014). The real impact of improved access to finance: Evidence from Mexico. *The Journal of Finance, 69*(3), 1347–1376. https://doi.org/10.1111/jofi.12091
- **Versión leída:** World Bank Policy Research Working Paper 4981 (junio 2009), *The Economic Impact of Banking the Unbanked*. La versión publicada en 2014 puede diferir en cifras o especificaciones; conviene verificar antes de citar números exactos.
- **Links:**
  - Working paper: https://openknowledge.worldbank.org/handle/10986/4173
  - SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2285013

**Contexto**
- En octubre de 2002, Grupo Elektra abrió Banco Azteca con **815 sucursales a la vez**, dentro de todas sus tiendas existentes. Se convirtió en la segunda red de sucursales del país.
- Atendía a segmentos de ingreso bajo y medio. Pedía poca documentación (a menudo un aval) y usaba unos 3,000 cobradores en moto.
- Las cuentas de ahorro se abrían con unos 5 dólares. Hubo 157 mil cuentas en el primer mes y más de 250 mil a diciembre de 2002.
- Los créditos promedio eran de unos 250 dólares, con tasas cercanas al 50% anual. La banca comercial cobraba entre 20% y 40%, pero rechazaba a casi todos.

**Identificación**
- La ubicación estaba predeterminada: las sucursales abrieron donde ya había tiendas Elektra.
- Es un diseño de diferencias en diferencias con efectos fijos de municipio y trimestre, controles individuales y errores agrupados por municipio.
- **Tratados:** 249 municipios con sucursal Azteca en 2002T4.
- **Controles:** 327 municipios sin Azteca pero con otro banco. Excluyeron los municipios sin ningún banco por considerarlos poco comparables.
- **Datos:** Encuesta Nacional de Empleo (ENE), 2000T2–2004T4 (10 trimestres antes y 9 después), unas 4.7 millones de observaciones individuales de 20 a 65 años.
- Usan datos de la **CNBV a nivel municipal** para ubicar sucursales y para mostrar que las cuentas de ahorro crecieron más en municipios con Azteca. Esto es un precedente de uso de datos CNBV municipales.

**Pruebas de validez**
- Había tendencias previas distintas en asalariados, no empleados e ingreso, que iban en contra de encontrar efecto. Las corrigen con tendencias lineales por grupo y por municipio.
- Hacen verificación gráfica de que el cambio coincide con la apertura.

**Resultados**

| Resultado | Efecto |
|---|---|
| Dueños de negocio informal | +0.0062, es decir **+7.6%** sobre la base de 8.2%; solo significativo en hombres |
| Dueños de negocio formal | Sin efecto robusto |
| Empleo total | **+1.4%** |
| Mujeres asalariadas | Aumentan |
| Ingreso | **Alrededor de +7%** con tendencias; +0.09 en mujeres y +0.048 en hombres (log(1+ingreso)) |
| Ingreso sobre el salario mínimo | Sin efecto |

- **Mecanismo:** los dueños de negocio informal previos tuvieron más probabilidad de seguir operando. Los no empleados pasaron a ser dueños de negocio o asalariados y su ingreso subió.

**Limitaciones reconocidas**
- No pueden separar el efecto directo del efecto por competencia con microfinancieras y cajas.
- No tienen datos de crédito municipal antes y después.
- Los datos de ingreso de la ENE son débiles.

**Uso para nosotros**
- Es el paper espejo y contra él se define el mérito intelectual.
- **Diferencias con nuestro caso:** banco público y no privado; aperturas escalonadas y no simultáneas; resultados de oferta financiera (BDIF) y no laborales; tratamiento de 2021–2024.

---

### 1.2 Fonseca y Matray (2024): "Banco para Todos", Brasil

- **Cita:** Fonseca, J., y Matray, A. (2024). Financial inclusion, economic development, and inequality: Evidence from Brazil. *Journal of Financial Economics, 156*.
- **Versión leída:** Griswold Center WP 308 (septiembre 2022). Circuló antes como NBER WP 30057.
- **Link:** https://gceps.princeton.edu/wp-content/uploads/2023/03/wp308_FonsecaMatray_Brazil_unbanked.pdf

**Contexto**
- Los bancos públicos hacían casi la mitad del crédito en Brasil, pero cerca del 60% de los municipios no tenía banco público antes de 2004. Alrededor del 40% de los brasileños no estaba bancarizado.
- El programa federal "Banco para Todos" (2004) usó a Caixa Econômica Federal y Banco do Brasil para llegar a ciudades sin banco público.
- La proporción de municipios sin banco público pasó de 60% a 44% en 2014.
- La evaluación del gobierno reportó 7.8 millones de cuentas abiertas y 1.46 millones de personas de bajos ingresos bancarizadas entre 2004 y 2007.
- El programa también usó **corresponsales**, pero los autores no pueden observarlos. Por eso sus efectos financieros son una cota inferior.

**Identificación**
- **Tratados:** ciudades sin banco público antes de 2004.
- **Controles:** ciudades que ya tenían banco público.
- Esta elección tiene dos ventajas:
  - Cualquier choque específico a los bancos públicos afecta por igual a tratados y controles.
  - Los grandes programas de transferencias (Bolsa Família) se pagan a través de bancos públicos que los controles ya tenían, así que la expansión de transferencias no sesga el resultado.
- **Emparejamiento:** por quintil de población y por crecimiento previo del Gini (3 controles por tratado). Queda balance en PIB, informalidad, gasto municipal, partido del alcalde, exposición a commodities, distancia a la capital, etc.
- **Muestra:** 1,415 tratados y 3,918 controles, sobre 4,260 áreas mínimas comparables (AMC).
- **Especificación:** efectos fijos de ciudad y de grupo emparejado por año; ponderada por población; errores agrupados por ciudad.
- **Robustez:**
  - Controles previos interactuados con año, para evitar "malos controles".
  - Efectos fijos de estado por año.
  - Diseño ciudad por industria con efectos fijos de industria por grupo por año.
  - Distintos criterios de emparejamiento.
  - Control por gasto municipal y afiliación política.
  - Prueba de que no es Bolsa Família: los resultados son más débiles cuando el control no tenía Caixa.
- **Datos:** RAIS (empleo formal), ESTBAN del Banco Central (balance por sucursal, separado en público y privado), IBGE y Censo 2000.

**Resultados financieros (Tabla 2)**

| Variable | Todos | Públicos | Privados |
|---|---|---|---|
| Tener sucursal (p.p.) | **+18.7** | +42.5 | **−2.2** (10%) |
| Depósitos nuevos per cápita (BRL 2010) | **+142** | +119 | +24 (10%) |
| Préstamos nuevos per cápita (BRL 2010) | **+155** | +182 | **−26** (5%) |

- Depósitos y crédito suben en la misma proporción. Es decir, el ahorro local financia el crédito local, sin que el capital venga de otras ciudades. El efecto no se revierte: la ciudad pasa a un nivel más alto de forma permanente.
- **Casi no hay desplazamiento de la banca privada.** La expansión la explican por completo los bancos públicos.
- Condicionando a los tratados que sí recibieron sucursal pública, los préstamos nuevos per cápita suben unos 312 BRL.
- ¿Por qué había desiertos bancarios si eran mercados rentables? Los autores dan tres razones: privatización y cierres en los 90, poder de mercado con incertidumbre sobre la rentabilidad, y costos fijos que hacen que las redes crezcan de forma gradual desde donde ya están.

**Resultados reales (Tabla 3)**
- Número de empresas: **+9.8%**. Suben tanto las entradas como las salidas.
- Empleo: **+10%**, con el doble de crecimiento en empresas pequeñas (+21.4%) que en grandes (+11.6%).
- Salario promedio: **+4.1%**.
- Número de industrias: +4.7%.
- El efecto es gradual y se estabiliza en unos 5 años. No hay tendencias previas.

**Mecanismos**
- **No es demanda local ni gasto fiscal.** El empleo en sectores comerciables crece casi el doble que en no comerciables.
- **Importa la distancia.**
  - Sin banco privado previo, el efecto es mucho mayor: empleo +13.9 p.p. adicionales y salario +7 p.p. adicionales.
  - El efecto crece con la distancia al banco más cercano; la distancia promedio previa era de 8.66 km.
- **No es por ser banco público.** El efecto de la distancia es igual si el banco cercano es público o privado.

**Desigualdad**
- El Gini sube 1.2 puntos en promedio y unos 2 puntos a los 10 años (+7%).
- Los salarios suben 1% en el cuartil más bajo y 5.5% en el más alto.
- La prima por calificación sube 8.3%, pero la proporción de trabajadores calificados casi no cambia (+0.2%).
- Hay poca migración interna. El aumento de desigualdad se concentra en ciudades con poca oferta de trabajadores calificados: la escasez de talento explica el resultado.

**Uso para nosotros**
- **Diseño:**
  - Tomar la definición de tratamiento como "municipio sin banco público previo".
  - Considerar como control a municipios con sucursal Bansefi o Banco del Bienestar previa. Esto absorbería el canal de dispersión de programas sociales, que es nuestro análogo de Bolsa Família.
- **Expectativa:** si medimos solo banca múltiple y EACP, el efecto puede ser pequeño o incluso ligeramente negativo por desplazamiento. Eso ya sería un hallazgo; conviene reportar también el total como resultado secundario.
- **Heterogeneidad:** desierto bancario (sin banca múltiple previa) y distancia a la sucursal más cercana.
- **Datos:** ellos no ven corresponsales; la BDIF sí los tiene, lo que es una ventaja nuestra.

---

### 1.3 Aportela (1999): expansión de Pahnal

- **Cita:** Aportela, F. (1999). *Effects of financial access on savings by low-income people* (Documento de Investigación). Banco de México. Semantic Scholar la fecha en 1998; hay que verificar.
- **Link:** http://users.nber.org/~rdehejia/!@$devo/Lecture%2006%20Microcredit/supplemental/Aportela.pdf

**Contexto institucional (linaje directo del Banco del Bienestar)**
- El Patronato del Ahorro Nacional (Pahnal) opera desde diciembre de 1949 y promueve el ahorro de personas de bajos ingresos.
- En los 80 no ajustó sus tasas a la inflación (alrededor de 65% anual), los ahorradores perdieron y sus depósitos cayeron.
- La reforma de 1993 tuvo dos partes:
  - **Nuevas sucursales** en oficinas de correos (95% de las nuevas), con unos 2 empleados cada una.
  - **Nuevos productos:** Tandahorro (depósito mensual obligatorio, mínimo 50 pesos, plazo de 12, 24 o 36 meses, con compensación si la tasa queda por debajo de la inflación) y Cuentahorro (líquida, mínimo 50 pesos). Ambos sin comisiones y con sorteos mensuales.
- **Expansión:** pasó de 96 oficinas en 67 localidades (1992) a 98 oficinas nuevas en 34 localidades (1993), 27 de ellas sin oficina previa. Se concentró en 8 estados y 60% de las nuevas quedaron en la CDMX. A junio de 1998 tenía 391 oficinas, 100 de ellas rurales.
- Las cuentas pasaron de 83 mil a 229 mil entre julio de 1993 y diciembre de 1994. Cuentahorro concentraba 74% de las cuentas, lo que muestra preferencia por la liquidez.
- La trayectoria sigue: Pahnal se convirtió en Bansefi en 2001 y Bansefi en Banco del Bienestar en 2019 (según ASF 2023).

**Identificación**
- Diferencias en diferencias con la ENIGH 1992 y 1994: hogares en localidades con expansión contra hogares en localidades sin ella.
- Distingue expansión en "localidad nueva" y en "localidad con oficina previa".
- Usa regresión robusta y regresión mediana con bootstrap, y dos definiciones de tasa de ahorro (con y sin gasto en vivienda).
- **Argumentos de exogeneidad:**
  - Ningún documento oficial describe un método de selección de ubicaciones.
  - La expansión no se correlaciona con la tasa de ahorro ni con el ingreso estatal.
  - Hace un "experimento inverso" (placebo) con ENIGH 1989–1992.
- **Advertencia crítica:** en el placebo algunos coeficientes sí son significativos (localidades nuevas, ahorro sin vivienda: −5.6 y −6.3 p.p.). Además, la expansión se concentró en localidades más grandes y urbanas.

**Resultados**
- Tasa de ahorro de los hogares expuestos: **+3 a +5 p.p.**; en localidades nuevas, +4.7 a +6.7 p.p. (ahorro con vivienda).
- Hogares con ingreso por miembro de hasta 1 salario mínimo: **+5.7 a +8 p.p.** Es el único grupo con efecto consistente.
- Hogares de ingreso alto: sin efecto.
- La exposición es relevante: en ciudades medianas, los depósitos de Pahnal equivalían al 21–29% del ahorro de las personas de bajos ingresos.
- No hay evidencia fuerte de que el ahorro formal desplazara al informal (tandas, préstamos, oro, animales). Probablemente es ahorro nuevo.

**Uso para nosotros**
- Es un antecedente de evaluación de esta misma institución y de expansión en infraestructura pública ya existente (correos entonces, inmuebles federales ahora).
- Refuerza la heterogeneidad por pobreza y marginación.
- Su placebo con datos previos es un modelo para nuestro análisis de tendencias previas.

---

### 1.4 Callaway y Sant'Anna (2021): el método

- **Cita:** Callaway, B., y Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics, 225*(2), 200–230. https://doi.org/10.1016/j.jeconom.2020.12.001
- **Link:** https://arxiv.org/abs/1803.09015
- **Software:** paquete `did` en R (CRAN).

**Idea central.** El análisis se hace en tres pasos separados:
1. Identificar efectos desagregados **ATT(g,t)**: el efecto promedio en el periodo t para el grupo g, donde g es el primer periodo tratado.
2. Agregarlos en resúmenes.
3. Estimar e inferir.

Así se evitan los problemas del TWFE con efectos heterogéneos: pesos negativos y comparaciones "prohibidas" contra unidades ya tratadas.

**Supuestos**

| # | Supuesto | Qué implica para nosotros |
|---|---|---|
| 1 | Tratamiento irreversible (adopción escalonada) | Una sucursal abierta cuenta como tratada para siempre. Revisar cierres en la BDIF. |
| 2 | Muestreo aleatorio (panel) | Hay versión para cortes transversales repetidos. |
| 3 | Anticipación limitada (δ conocido) | La construcción de SEDENA podría generar anticipación. Considerar δ=1 trimestre como robustez. |
| 4 | Tendencias paralelas condicionales con **nunca tratados** | Solo si hay suficientes municipios sin tratamiento. |
| 5 | Tendencias paralelas condicionales con **aún no tratados** | Probablemente sea nuestro caso. |
| 6 | Traslape | Probabilidad de ser tratado acotada lejos de 1. |

**Detalles clave**
- Las unidades **ya tratadas en el primer periodo se descartan**. Implicación: los municipios con sucursal Bansefi o Banco del Bienestar antes de 2019T1 no pueden ser tratados en este diseño. O se excluyen o se redefine el tratamiento, por ejemplo como "primera sucursal nueva del plan".
- El periodo de referencia es **g−δ−1**, el último periodo sin tratamiento.
- Si **todos terminan tratados**, solo se identifican los ATT(g,t) con t anterior al inicio del último grupo, y el último grupo no tiene efecto identificado.
- **Nunca tratados o aún no tratados.**
  - Nunca tratados conviene si ese grupo es grande y parecido a los tratados, y no restringe las tendencias previas.
  - Aún no tratados da más comparaciones, pero sí restringe las tendencias previas.
  - Los autores **recomiendan no elegir con pruebas estadísticas previas** (citan a Roth 2020), sino por el contexto.
- **Covariables:** solo previas al tratamiento, por ejemplo marginación 2020 y población. Pueden estimarse con regresión de resultados, ponderación inversa o **doblemente robusto (recomendado)**, que requiere acertar solo uno de los dos modelos.
- **Agregaciones:**
  - θ_es(e): estudio de evento por tiempo de exposición. Ojo: la composición de grupos cambia entre valores de e.
  - θ_es^bal(e; e'): estudio de evento balanceado, con grupos fijos.
  - θ_sel(g): efecto por cohorte.
  - θ_c(t) y su versión acumulada: efecto por periodo calendario.
  - **θ_sel^O:** efecto global recomendado, el promedio por grupo ponderado por tamaño. Se interpreta como el ATT canónico.
- **Inferencia:** bootstrap multiplicador con **bandas simultáneas** (no puntuales) y agrupación por municipio. Requiere muchos clusters, lo cual cumplimos con unos 2,470 municipios.
- **Aplicación del paper (salario mínimo):** el TWFE condicional da −0.8% (no significativo), mientras que su método da −3.1% (significativo). **La elección de estimador cambia la conclusión.**
- Los ATT(g,t) previos al tratamiento se estiman con diferencias cortas y sirven para evaluar el supuesto.

---

## 2. Fuentes institucionales y de contexto

### 2.1 ASF, Auditoría 2022-0018-A (Cuenta Pública 2022)

- **Link:** https://www.asf.gob.mx/Trans/Informes/IR2022c/Documentos/Auditorias/2022_0018_a.pdf
- **Tipo:** auditoría combinada de cumplimiento y desempeño sobre control interno y gobernanza. **No es evaluación de impacto.**

**Cronología del plan**

| Fecha | Hecho | Meta de sucursales |
|---|---|---|
| 12 jul 2019 | PND 2019–2024 crea el Banco del Bienestar sobre la base de Bansefi (menos de 500 sucursales) | 7,000 |
| 19 jul 2019 | Reforma a la Ley Orgánica del Banco del Bienestar | — |
| 17 ene 2020 | Convenio Marco SEDENA–Banco del Bienestar, vigente al 30 sep 2024 | 2,702 / 2,704 |
| 11 feb 2020 | Acuerdo presidencial: inmuebles federales para sucursales; Bienestar, Coordinación de Programas y SEDENA definen zonas prioritarias | 2,700 |
| 2020–2021 | 38 convenios específicos con SEDENA | 2,700 |
| feb 2022 | Nueva meta | 2,744 |
| 15 dic 2022 | Reporte del contratista: 2,409 sucursales, 1,873 terminadas y 536 en construcción | — |
| cierre 2022 | **922 en operación** (14 de 2021 y 908 de 2022) | — |
| 28 feb 2023 | Reprogramación: 1,822 sucursales para 2023 | 2,744 |

**Otros datos**
- Hacienda registró 37 proyectos de inversión para 2,617 sucursales: 2,573 de 65 m² y 44 de 197 m².
- Diez estados concentran 556 de las 922 sucursales operando: Oaxaca 87, Veracruz 81, Puebla 68, CDMX 64, Chiapas 61, Estado de México 53, Sinaloa 39, Guanajuato 36, Hidalgo 34, Michoacán 33.
- Los retrasos se explican por COVID, disponibilidad de inmuebles, escasez de equipo tecnológico, zonas de difícil acceso y cambios de proyecto.
- **En 2022 no se otorgó crédito** de primer ni segundo piso. La prioridad fue construir sucursales y dispersar recursos. Se castigó cartera por 507.5 millones de pesos.
- Productos de ahorro: Tanda Ahorro (inversión con protección contra inflación) y una cuenta infantil.
- Los consejeros independientes pidieron vigilar el riesgo de fraude por la expansión y una estrategia para que las sucursales sean autosostenibles. Esos temas no llegaron al Consejo.
- En 2022 los expedientes de obra estaban incompletos (solo 4 de 13 documentos solicitados) y ningún convenio específico se había finiquitado.

### 2.2 IMCO (2022), "Banco del Bienestar a la deriva"

- **Link:** https://imco.org.mx/banco-del-bienestar-a-la-deriva/
- Rezago del **55%**: a febrero de 2022 había 1,212 sucursales construidas contra una meta de 2,700 para finales de 2021.
- El rezago es desigual entre estados. Los más atrasados son Jalisco (80%), Quintana Roo (79%), Guerrero (78%) y Nayarit (70%); los más avanzados, Baja California Sur (0%), Sinaloa (22%), Zacatecas (22%) y Durango (26%).
- **No hay un criterio identificable** para evaluar la inclusión. **Los 26 municipios con mayor porcentaje de pobreza no tenían sucursal operando.**
- En 2021, 9 de cada 10 pesos se asignaron por adjudicación directa. Se cancelaron contratos de cajeros y transacciones por más de 27 mil millones de pesos. Se desconoce en qué se gastó el 74% del presupuesto de construcción.
- Había 674 personas para atender todas las sucursales, menos de una por sucursal operando.
- **Nota:** las cifras de IMCO y ASF usan cortes y definiciones distintas de "construida", así que no deben mezclarse.

### 2.3 OCDE (2022), Working Paper 1717 (Maravalle y González Pandiella)

- **Link:** https://www.oecd.org/en/publications/expanding-access-to-finance-to-boost-growth-and-reduce-inequalities-in-mexico_2de3cd7d-en.html
- **No se leyó completo** (el PDF bloquea el acceso automático). Los puntos vienen del resumen y de fragmentos.
- **Hallazgos:**
  - El acceso formal en México es bajo y desigual por ingreso, género, zona y región.
  - En lo rural domina el efectivo y el crédito informal.
  - Las regiones con más acceso tienen más crecimiento.
  - Menciona el plan de 2,700 sucursales y 13,500 cajeros en los Centros Integradores, y cita a Bruhn y Love.
  - Sus recomendaciones van por competencia, regulación, fintech y educación financiera.
- Puede entrar como referencia de contexto (es working paper).

### 2.4 CNBV, Base de Datos de Inclusión Financiera (BDIF)

- **Link:** https://www.gob.mx/cnbv/acciones-y-programas/bases-de-datos-de-inclusion-financiera
- **Cobertura:** trimestral desde diciembre de 2009, estatal y municipal, construida con reportes regulatorios. Incluye banca múltiple, banca de desarrollo, SOCAP y SOFIPO.
- **Contenido:** infraestructura (sucursales, cajeros, TPV, corresponsales), captación, crédito, cuentas ligadas a celular y transacciones.
- **Solo dos bancos de desarrollo:** Banco del Bienestar y Banjercito, porque son los únicos con productos de captación al menudeo (según BBVA Research con datos de 2023T2). Hay que **descontar Banjercito** del tratamiento.
- En los reportes, "Banca" junta múltiple y desarrollo. **La separación debe hacerse desde las bases municipales.**
- Desde 2019T1 cambió el método para contar módulos de corresponsal. Nuestro panel inicia justo ahí; verificar consistencia.
- **Dato clave para el diseño (diciembre 2024):** 99.6% de los adultos vive en un municipio con al menos un punto de acceso. **La banca de desarrollo tiene sucursal en 1,964 municipios y la banca múltiple en 912.** Hay pocos municipios nunca tratados.
- El reporte trimestral de 2023T1 también bloquea el acceso automático. Hay que revisarlo a mano.

---

## 3. Implicaciones para nuestro diseño

Esto es síntesis propia, **no son decisiones tomadas**.

**Tratamiento**
- Primer trimestre con sucursal de banca de desarrollo en la BDIF, sin contar Banjercito.
- Los municipios con sucursal previa a 2019T1 (herencia Bansefi) quedan como ya tratados y se excluyen, o se redefine el tratamiento.
- Alternativa inspirada en Fonseca y Matray: usar esos municipios como grupo de comparación que ya tenía el canal de dispersión.

**Grupo de comparación**
- Aún no tratados como principal, porque hay pocos nunca tratados.
- Nunca tratados como robustez, si el grupo alcanza.

**Anticipación**
- δ=0 como base y δ=1 como robustez, por obra visible y contratación local.

**Covariables previas**
- Índice de marginación 2020, población, presencia previa de banca múltiple y EACP, y distancia a la sucursal más cercana si se puede construir.
- Estimador doblemente robusto.

**Resultados**
- Contratos de captación y crédito por cada 10 mil adultos, TPV y transacciones, **solo banca múltiple y EACP**.
- El total como resultado secundario, reportando que incluye el efecto mecánico.

**Qué esperar**
- Fonseca y Matray encuentran que el crecimiento lo explican los bancos públicos, con desplazamiento privado leve.
- El efecto en banca múltiple y EACP podría ser nulo o negativo, y hay que saber interpretarlo.
- Aportela y Bruhn y Love sugieren efectos concentrados en la población más pobre.

**Heterogeneidad**
- Desierto bancario (sin banca múltiple previa), distancia, grado de marginación y cohorte de apertura (2021, 2022, 2023).

**Reportes**
- ATT(g,t) con bandas simultáneas, estudio de evento balanceado y efecto global θ_sel^O.
- Comparar contra TWFE para mostrar la diferencia.
- Tendencias previas: ATT previos y, como robustez adicional, Rambachan y Roth (2023).

**Amenazas a la identificación**
- Ubicación decidida por inmuebles disponibles y zonas prioritarias (IMCO, ASF).
- Otros programas sociales dispersados por el banco.
- COVID (2020–2021).
- Diferencia entre construida y operando.
- Posibles cierres o reubicaciones de sucursales.

---

## 4. Mérito intelectual (borrador de argumentos)

1. **No existe evaluación de impacto del Plan de Expansión.** Lo que hay es fiscalización (ASF) y seguimiento de compras y avance (IMCO).
2. Es la primera evaluación de una **expansión pública masiva y escalonada** en México con datos administrativos municipales. Bruhn y Love estudian un banco privado con apertura simultánea; Aportela, una expansión pequeña (98 oficinas) con encuestas de hogares.
3. Extiende a México la evidencia de Fonseca y Matray para Brasil, en un contexto donde el banco público **no otorga crédito** y funciona sobre todo como **dispersor de transferencias**, a diferencia de los bancos públicos brasileños, rentables y activos en crédito.
4. Usa estimadores robustos a heterogeneidad (Callaway y Sant'Anna), no TWFE.
5. Pregunta de fondo: ¿la presencia de un banco público de dispersión atrae o desplaza la actividad de la banca privada y de las EACP?

---

## 5. Pendientes

- [ ] Confirmar cifras de Bruhn y Love en la versión publicada en el *Journal of Finance* (2014); se leyó el working paper de 2009.
- [ ] Fonseca y Matray (2024): el volumen 156 está confirmado; falta el número de artículo (en referencias.md aparece 103854; verificar).
- [ ] Aportela: confirmar año (1999 o 1998) y formato de cita del Banco de México.
- [ ] BDIF: confirmar separación por tipo de institución en captación y crédito, cómo aparece Banjercito, si trae población adulta y si registra cierres.
- [ ] Contar municipios con sucursal Bansefi antes de 2019T1 (ya tratados).
- [ ] Revisar a mano el reporte trimestral BDIF 2023T1 y el documento completo de la OCDE.
- [ ] Referencias confirmadas en esta sesión:
  - Bruhn y Love, JoF 69(3), 1347–1376.
  - Célerier y Matray, RFS 32(12), 4767–4809, doi 10.1093/rfs/hhz046.
  - Callaway y Sant'Anna, JoE 225(2), 200–230.

---

## 6. Decisiones del chat

- **Lista de lectura:** solo papers o reviews. ASF, IMCO, BDIF y el Programa Institucional son contexto y datos, no lectura obligatoria.
- **Los 4 papers necesarios:**
  1. Bruhn y Love (2014)
  2. Fonseca y Matray (2024)
  3. Callaway y Sant'Anna (2021)
  4. Aportela (1999)
- **Siguientes en prioridad:**
  - Dupas et al. (2018): acceso no es uso; clave para interpretar resultados.
  - Burgess y Pande (2005): clásico de banca pública rural.
  - Célerier y Matray (2019): se cita, pero no hace falta leerlo completo.
- **Reparto original de lecturas (16):**
  - Andrés, método y datos: CS21, CNBV corresponsales, Goodman-Bacon, Sun y Abraham, Rambachan y Roth, Borusyak et al.
  - Compañero A, literatura cercana: Bruhn y Love, Célerier y Matray, Aportela, Burgess y Pande, Fonseca y Matray.
  - Compañero B, contexto y uso: IMCO, ASF, Dupas et al., Programa Institucional, Muralidharan et al.
- **Sustitución:** Fonseca y Matray reemplaza a Célerier y Matray en el top 4.

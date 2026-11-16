# Revisión de la propuesta (v1, 2026-09-15)

Borrador revisado: `propuesta_v1.md`. Especificación: título (1 línea); pregunta (1 párrafo);
mérito intelectual (9–31 fuentes, qué aporta; 1–2 párrafos); diseño (causal/predictivo, método;
1–2 párrafos); fuentes (qué, dónde, disponibilidad; 1 párrafo).

## 1. Cumplimiento de la especificación

| Sección | Estado | Problema |
|---|---|---|
| Título | ✅ | Bien. Opcional: "…sobre la actividad financiera **privada** municipal" deja claro que se excluye al propio banco. |
| Pregunta | ⚠️ | Son **dos preguntas en lista**, no un párrafo. La 2 (dónde poner las siguientes X sucursales) es de focalización/predicción y no se responde con el diseño causal; conviértela en la pregunta de heterogeneidad o pásala al final del diseño como extensión. |
| Mérito | ⚠️ | Dos párrafos ✅, pero **no nombra ningún paper** en el texto (la especificación pide "decir qué aporta a la conversación"). Hay que anclar en Bruhn–Love, Fonseca–Matray, Aportela, Burgess–Pande, Célerier–Matray y en CS/Goodman-Bacon. |
| Diseño | ⚠️ | No dice estimador, unidad, periodo, grupo de control ni resultados. Hay dos afirmaciones incorrectas (ver §2). |
| Fuentes | ⚠️ | Un párrafo ✅, pero sobreafirma lo que trae la BDIF y atribuye al directorio una función que no tiene (ver §2). |
| Referencias | ✅ | 29 (dentro de 9–31), APA, alfabéticas. Falta el Portafolio de Información CNBV. |

## 2. Errores de fondo (verificados en los datos, `docs/data_audit.md`)

1. **"contratos de captación y crédito y transacciones, desagregados por tipo de institución"** —
   solo desde 2022T4. Entre 2016T1 y 2022T3 la BDIF trae **sucursales** por sector, pero
   captación, crédito, cajeros, TPV y transacciones como "Banca" (múltiple + desarrollo) combinada.
   Corregir: "las sucursales vienen por tipo de institución en todo el periodo; contratos y
   transacciones por tipo de institución desde 2022T4".
2. **"directorio de sucursales … para fechar y validar aperturas"** — el directorio (foto 1T 2026)
   no tiene fechas. Las aperturas se fechan con el conteo trimestral de la BDIF; el directorio solo
   valida ubicación (coincidencia 99.9%).
3. **Banjército.** La banca de desarrollo de la BDIF incluye a Banjército. Sin corregirlo, 5
   municipios tendrían tratamiento falso y 8 estarían mal clasificados como ya tratados. Se
   corrige con el Portafolio de Información de la CNBV (operativa por institución, 2016–2021).
   Mencionarlo en fuentes y citarlo.
4. **"Esto se debe a que la implementación de las sucursales … siguió está metodología"** — la
   política no "siguió" el método; el despliegue fue escalonado y eso permite el diseño. Reescribir.
5. **"experimento natural"** — la ubicación no fue aleatoria (zonas prioritarias de Bienestar y
   SEDENA; inmuebles federales disponibles; IMCO: los 26 municipios más pobres sin sucursal). Es
   cuasi-experimental; hay que decir cómo se defiende la identificación (tendencias previas,
   controles aún no tratados, covariables previas, Rambachan–Roth).
6. **"literatura de microfinanzas"** — el Banco del Bienestar no es una microfinanciera: es un
   banco de desarrollo que casi no otorga crédito (ASF: cero crédito en 2022) y dispersa
   transferencias. Ese hecho es justo lo que motiva medir el efecto **sobre el resto del sistema**
   (efecto mecánico si se incluyeran sus propias cuentas). Explotarlo, no confundirlo.
7. **"no se ha utilizado DiD escalonado en ningún estudio de bancarización en México"** —
   sobreafirmación difícil de sostener. Suavizar: "hasta donde sabemos, ninguna evaluación del
   Plan de Expansión usa estimadores robustos a heterogeneidad (Callaway y Sant'Anna 2021)".
8. **Dirección del efecto.** La pregunta presupone "incrementó". Fonseca y Matray (2024) encuentran
   que la banca privada casi no reacciona (incluso −2.2 p.p. en presencia). Plantear "atrajo o
   desplazó".
9. **ENIF** — no es municipal; sirve solo como contraste descriptivo. Decirlo así o quitarla.

## 3. Forma

- "dónde se abre" → "donde"; "municipo" → "municipio"; "está metodología" → "esta"; "estás
  sucursales" → "estas"; "en el grupo (municipo) i en el tiempo t" — en CS el grupo g es la
  **cohorte** (trimestre de primera apertura), no el municipio.
- "Tópicos de políticas públicas II" → nombre oficial del curso.
- Sangrías inconsistentes en el segundo párrafo de mérito.

## 4. Texto propuesto (sustituir; ajustar voz)

**2. Pregunta.** ¿La llegada de la primera sucursal del Banco del Bienestar a un municipio
(aperturas escalonadas 2022–2024) atrajo o desplazó la actividad de la banca múltiple y de las
entidades de ahorro y crédito popular —sucursales, cajeros, terminales, contratos de captación y
crédito por cada 10 mil adultos—, frente a municipios comparables que la recibieron después? Y, si
hubo efecto, ¿fue mayor en los municipios sin ninguna sucursal bancaria previa, más lejanos a una
sucursal de banca múltiple o con mayor marginación? La respuesta a lo segundo es lo que permitiría
orientar dónde abrir las siguientes sucursales.

**3. Mérito (párrafo 2, reemplazar).** Tres antecedentes directos estudian aperturas masivas para
población de bajos ingresos: Banco Azteca en México (Bruhn y Love, 2014; 815 sucursales
simultáneas, efectos en empleo e ingreso informal), Pahnal —antecesor institucional del Banco del
Bienestar— (Aportela, 1999; ahorro de hogares pobres) y "Banco para Todos" en Brasil (Fonseca y
Matray, 2024), el más cercano al nuestro: bancos públicos, nivel municipal, depósitos y crédito
como resultados, y el hallazgo de que la expansión pública casi no desplazó a la banca privada.
Burgess y Pande (2005) y Célerier y Matray (2019) muestran que la oferta de sucursales importa más
donde no había ninguna. Nuestro aporte es triple: (i) hasta donde sabemos, no existe evaluación de
impacto del Plan de Expansión —la ASF (2023) fiscaliza control interno e IMCO (2022) documenta
rezagos y opacidad—; (ii) el caso es distinto al brasileño porque el banco casi no otorga crédito
y funciona como dispersor de transferencias, así que la pregunta relevante es qué pasa con el
**resto** del sistema; (iii) el despliegue escalonado con cohortes trimestrales exige los
estimadores robustos a heterogeneidad (Callaway y Sant'Anna, 2021; Goodman-Bacon, 2021), que
contrastaremos con el TWFE convencional.

**4. Diseño.** Causal, con una extensión de heterogeneidad para la focalización. Panel
municipio-trimestre 2019T1–2024T4 con diferencias en diferencias escalonadas de Callaway y
Sant'Anna (2021). El tratamiento es el primer trimestre en que el municipio tiene una sucursal del
Banco del Bienestar en operación según la BDIF, descontando las de Banjército con el Portafolio de
Información de la CNBV; los 487 municipios con sucursal heredada de Bansefi en 2019T1 se excluyen
(o se usan como control, como en Fonseca y Matray). El grupo de comparación son los municipios
**aún no tratados** (casi todos —1,482 de 2,475— reciben sucursal entre 2022T1 y 2024T1; solo 502
nunca la reciben y son sistemáticamente más pequeños y rurales). Los resultados excluyen al propio
banco para evitar el efecto mecánico de dispersar programas sociales. Estimador doblemente robusto
con covariables previas (marginación 2020, población, presencia previa de banca múltiple y EACP,
distancia a la sucursal bancaria más cercana), bootstrap multiplicador agrupado por municipio y
bandas simultáneas; reportamos ATT(g,t), estudio de evento, efecto por cohorte y el efecto global.
La ubicación de sucursales no fue aleatoria (zonas prioritarias e inmuebles federales disponibles),
por lo que la identificación descansa en tendencias paralelas condicionales, que evaluamos con los
coeficientes previos al tratamiento y con el análisis de sensibilidad de Rambachan y Roth (2023).
Heterogeneidad por desierto bancario, distancia, marginación y cohorte.

**5. Fuentes.** La fuente principal es la Base de Datos de Inclusión Financiera de la CNBV,
trimestral y municipal desde 2009, de descarga libre (ya descargados 2016T1–2025T4): sucursales por
tipo de institución (banca múltiple, banca de desarrollo, SOCAP, SOFIPO) en todo el periodo, y
cajeros, TPV, transacciones y contratos de captación y crédito por tipo de institución desde
2022T4; incluye población adulta (15+). Se complementa con el Portafolio de Información de la CNBV
(operativa mensual por institución, 2016–2021, para separar Banjército del Banco del Bienestar), el
directorio georreferenciado de sucursales del Banco del Bienestar (datos.gob.mx, para validar
ubicación), el Marco Geoestadístico 2024 y el Censo 2020 del INEGI (polígonos, distancias,
contigüidad y características municipales), y los índices de marginación y proyecciones de
población de CONAPO. La ENIF 2018–2024 no es municipal y solo se usa como contraste descriptivo.
Todas las fuentes son públicas.

## 5. Referencias a agregar

- Comisión Nacional Bancaria y de Valores. (2026). *Portafolio de Información: Banca de Desarrollo,
  información operativa* [Base de datos]. https://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/
- Instituto Nacional de Estadística y Geografía. (2024). *Marco Geoestadístico, diciembre 2024*
  [Conjunto de datos]. https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551132173
- Opcional: Roth, J., Sant'Anna, P. H. C., Bilinski, A., & Poe, J. (2023). What's trending in
  difference-in-differences? *Journal of Econometrics, 235*(2), 2218–2244 (verificar).

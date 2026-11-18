# Preguntas probables y cómo responderlas (versión del 2026-11-18)

Para defender el trabajo final ante el profesor, sinodales o compañeros. Cada respuesta trae la cifra, dónde
está en el PDF (`entregables/04_final/trabajo_final.pdf`) y, cuando hay, la debilidad que conviene
admitir antes de que la señalen. Las cifras vienen de `outputs/tablas/` y están cotejadas.

Numeración del PDF:
- Tablas: 1 descriptivas · 2 primera etapa · 3 acceso · 4 banca privada · 5 grupos de control · 6
  actividad · 7 desierto bancario · 8 calendario · 9–11 DENUE por distancia y fase 6 · 12
  decisiones · 13–16 fases 2–4.
- Figuras: 1 evento · 2 acceso · 3 resumen · 4 radios en niveles · 5 radios en %.

---

## A. Diseño e identificación

**¿Por qué la primera sucursal y no el número de sucursales?**
El 86% de los municipios tratados abrió una sola. El tratamiento es binario en la práctica; la
intensidad se revisó aparte y no cambia nada (`docs/decisiones.md`, 2026-10-02).

**¿Por qué fechan con la sucursal en operación y no con la obra?**
Al cierre de 2022 había 1,873 sucursales terminadas y solo 922 operando (ASF 2023). Fechar con la
obra mezclaría sucursales que no atendían a nadie. La anticipación de un trimestre no cambia el
nulo (Tabla 12).
- *Debilidad:* sin las fechas de obra no separamos un efecto de la construcción.

**La ubicación no fue aleatoria. ¿Cómo saben que no abrieron donde la banca ya iba a crecer?**
Cuatro piezas:
1. Las covariables explican solo el 5% del calendario de apertura (15% con efectos fijos de
   estado), y el nivel previo de sucursales privadas no predice la fecha dentro del estado
   (Tabla 8).
2. El estimador es doblemente robusto sobre esas covariables.
3. Los previos son planos (Wald p = 0.29 en privadas) y el placebo de fecha da −0.6%.
4. La permutación da p = 0.32; quitando un estado a la vez, el efecto va de +0.3% a +1.6%.
- *Debilidad:* HonestDiD aguanta violaciones de hasta un cuarto de la mayor tendencia previa
  ($\bar M$ = 0.25), no del mismo tamaño ($\bar M$ = 1). Las limitaciones lo dicen.

**¿Por qué Callaway y Sant'Anna y no TWFE?**
Con adopción escalonada y efectos heterogéneos, el TWFE usa a las ya tratadas como control. Aun
así, casi todas las regresiones con efectos fijos dan lo mismo (Tabla 15). La excepción es el TWFE
extendido con covariables (+6.8%), que se apoya en comparar contra los nunca tratados; ver la
pregunta siguiente. Goodman-Bacon: 11.9% del peso del TWFE en comparaciones prohibidas.

**¿El resultado depende de los municipios que nunca abren?** (pregunta de la presentación)
No (Tabla 5). Con otros grupos de control, el centro va de −1.9% a +2.3% en sucursales privadas:
- solo nunca tratados: +0.9%;
- solo los que abren, es decir, solo calendario: −1.9%, con IC90 de −4.2% a +0.3%;
- nunca tratados emparejados: +2.3%;
- sin vecinos que abran: +0.6%.

En el DENUE, con controles solo de municipios sin apertura, sale el mismo +10.4%.
- *Lo que hay que admitir:* comparar contra los nunca tratados tiene una deriva de +1.9% aun con
  fechas al azar (efecto inyectado). Por eso afirmamos ±5% y no ±2.4%. La muestra emparejada (320
  contra 320) es menos precisa: su intervalo no cabe en ±5%.

**¿Y en las EACP (cooperativas y financieras populares)?**
Con la especificación principal, +1.5% (cota 4.3%). Pero la comparación contra los nunca tratados
tiene ahí la deriva más grande (+2.6% con fechas al azar, 15% de falsos positivos). Solo por
calendario el efecto es −3.3% (p = 0.14), con cota de 7.0%.
- *Lo que hay que admitir:* en EACP no se descarta un desplazamiento pequeño, de hasta 7%. En banca
  múltiple, en cambio, el nulo aguanta también solo por calendario (cota 1.9%).

**¿El nulo no será falta de potencia?**
No. El intervalo al 90% queda dentro de ±5% de la media previa, el umbral preregistrado y menor que
el +7.6% de Bruhn y Love (2014). Un efecto de ±5% inyectado en los datos reales se detecta entre
90% y 98% de las veces. ±5% equivale a unas 132 sucursales privadas en los municipios tratados.
- *Debilidad:* con ±2.8% la detección baja a 44–72%, así que no afirmamos cotas más finas.

**¿Por qué excluyen al propio banco?**
Porque paga programas en cuentas propias: sus cuentas suben por construcción. Lo reportamos como
primera etapa (Tabla 2): +2.00 sucursales y +3,284 tarjetas por 10 mil adultos.

**¿Y Banjército, que la CNBV cuenta junto con el banco?**
Se descuenta con el Portafolio de la CNBV, que lo separa. Con el banco observado directamente
(2022–2026) cambian 9 municipios y ningún resultado se mueve más de 0.73 ee.

**¿Por qué un denominador fijo de 2022T4?**
Porque la población adulta de la CNBV cambia de fuente en 2020T4, con saltos municipales de −20% a
+13%. Un denominador que se mueve aparecería como efecto.

---

## B. Programas sociales y acceso (preguntas de la presentación)

**¿El banco aumentó la cantidad de programas o solo la conveniencia?**
La conveniencia, sí, y mucho. La cantidad no se puede saber con datos públicos.
- *Conveniencia* (Tabla 3, Figura 2):
  - los adultos de 65 o más pasaron de 9.5 km a 2.9 km de una sucursal del banco;
  - los que viven a 10 km o menos, de 68% a 92%;
  - entre quienes reciben apoyos, los que tienen cuenta para cobrarlos pasaron de 63% a 91% (ENIF).
- *Cantidad:* el padrón de Bienestar no publica beneficiarios por municipio y periodo para los
  programas que paga el banco.
  - Lo que existe por periodo son listas de personas con nombre, que decidimos no usar.
  - La proporción de hogares con programas (Encuesta Intercensal) sube 2.1 puntos, pero reprueba
    la pre-prueba.
  - En la foto de octubre de 2026, los municipios con sucursal nueva tienen 5.2 beneficiarios más
    por cada 100 habitantes (ee 1.7), condicional en covariables y estado. Es descriptivo: no hay
    dato previo.

**¿Cumple el banco su objetivo de distribuir mejor que antes?**
En acceso, sí. Su Programa Institucional 2020–2024 pide asegurar los pagos bajando tiempos y costos
de traslado. En los municipios de marginación muy alta, los adultos mayores a 10 km o menos pasaron
de 26% a 78%, y en localidades de menos de 2,500 habitantes, de 25% a 70%.

**¿Por qué el acceso no es una estimación causal?**
Porque describe la red misma: dónde quedó una sucursal es el producto del programa, no un resultado
que necesite contrafactual. Lo que sí sería causal (más cobertura, menos tiempo de traslado de cada
hogar) no tiene datos municipales con periodo previo.

**¿Cómo fecharon las sucursales de los municipios que tienen varias?**
La CNBV solo fecha la primera del municipio. Usamos el conteo de la BDIF: las localidades abren en
orden de población cuando el número de sucursales del municipio alcanza la suya.
- Cotas: si todas abren con la primera, la distancia de 2019 es de 8.0 km; si solo la principal,
  de 9.8 km. La conclusión no cambia.

**Antes de 2019 los programas se pagaban en Telecomm, en mesas de atención o con tarjetas de otros
bancos. ¿No exageran la mejora?**
Sí, puede exagerarse. Solo medimos sucursales del Banco del Bienestar; los demás puntos de pago no
tienen fechas ni coordenadas públicas. La tabla lo dice en su nota. La ENIF ayuda a acotarlo: en
localidades de menos de 2,500 habitantes, la mediana de tiempo a la sucursal que usan es de 40
minutos en 2021 y en 2024.

**¿Por qué no bajaron las listas del padrón para agregarlas?**
Traen nombre e importe de cada persona: unos 200 MB por bimestre, unos 9 GB solo de la pensión. Lo
fijamos en el preregistro y la adenda. La salida es pedir el agregado por transparencia (borrador en
`docs/contexto/solicitud_transparencia.md`).

**¿Se usan las cuentas?**
Para cobrar, sí; para algo más, casi no. Por cada 100 cuentas nuevas hay menos de medio crédito y
menos de medio depósito a plazo. En los cajeros del banco hay unos 1.5 retiros por tarjeta al
trimestre, el ritmo del pago bimestral. Saldos y cuentas activas no son públicos.

---

## C. DENUE

**¿El +10% del DENUE es un efecto de la sucursal o no?**
No lo podemos distinguir, y eso es lo que fijamos antes de estimar.
- *A favor de un efecto:*
  - aguanta otros controles y otros radios, y sale +9.7% en la muestra emparejada;
  - se concentra a menos de 3 km de la sucursal;
  - dentro del régimen de levantamiento completo de los Censos da +9.8%, con previos planos.
- *En contra del canal de gasto de los programas:*
  - no se concentra en el comercio, que además ya crecía más antes de abrir;
  - no es mayor donde viven más adultos mayores (tercil alto menos bajo: +1.0 puntos, p = 0.82);
  - no crece con el tiempo que lleva abierta la sucursal (2022: +11.2%; 2023–24: +10.0%);
  - no aparece en las unidades económicas de los Censos (−0.9%), en dueños de negocio de la
    Intercensal ni en la luz nocturna.
- Tablas 6 y 9–11; apéndice "¿Qué es el +10% del DENUE?".

**En la presentación dijeron que el aumento "aparece igual en las vecinas". ¿Ahora no?** (Fernando)
Era un artefacto de medir en porcentaje. Las vecinas a menos de 2 km suben +11.7% de su media, pero
su media es cinco veces menor. En establecimientos, más del 90% del aumento está a menos de 3 km de
la sucursal (93% ponderando por población, 98% sin ponderar), y más lejos no se distingue de cero
(Figura 4, Tabla 10).
- *Debilidad:* ponderado por población, el total es impreciso (la localidad con sucursal aporta 60%,
  con un ee grande). Por eso la cifra que defendemos es la de 3 km.

**¿Por qué no aparece en los Censos Económicos?**
Los Censos son municipales, y la mayor parte del aumento está en la localidad con sucursal y su
entorno inmediato. Probamos si la actividad se mudaba desde las localidades lejanas del mismo
municipio, lo que explicaría un total municipal plano, y no: las lejanas no pierden (sale positivo,
con pre-prueba fallida).

**¿Y si fue la obra y no la sucursal?**
No lo podemos descartar: sin fechas de obra por sucursal, el efecto de la construcción (SEDENA
construyó antes de abrir) se confunde con el de la apertura. Que no haya gradiente por exposición
es compatible con eso.

**¿Por qué sube tanto la manufactura?**
A dos dígitos del SCIAN, la manufactura incluye tortillerías y panaderías (3118), que son negocios
de barrio. No podemos separarlas con los datos guardados; dejarlas fuera del "consumo" juega en
contra del canal de gasto, y así lo preregistramos.

**¿Por qué el efecto es mayor en los desiertos bancarios (12.3% contra 5.3%)?**
Es compatible con que la sucursal importe más donde no había ninguna (Burgess y Pande 2005), pero
también con que esas localidades tuvieran menos registro previo en el padrón. No lo leemos como
mecanismo.

**¿Por qué el diseño entre actualizaciones y no escalonado en el DENUE?**
Entre actualizaciones el DENUE casi no se mueve: en 2022 cambia ~10% de las localidades tratadas por
versión, contra 83% en cada actualización integral. Con el escalonado se mide casi nada (+0.8%). La
lección metodológica del trabajo es esa: el diseño debe seguir el calendario de la medición.

---

## D. Generales

**¿Qué resultado cambiaría su conclusión principal?**
Que una variante creíble del grupo de control o del estimador moviera el centro fuera de ±5%, o que
la pre-prueba fallara. Ninguna lo hace. Para el DENUE: un placebo de cabeceras positivo y preciso
(sería medición) o un efecto concentrado en el consumo y creciente con los adultos mayores (sería
gasto). El placebo de cabeceras dio −2.7%, pero con un ee de 8.5%.

**¿El preregistro es real?**
Cada fase está en `docs/decisiones.md` con fecha, antes de estimar, y con lo que ya se había visto
(sección "Transparencia"). Lo exploratorio se declara así (régimen censal, fase 5, efecto inyectado).
Las correcciones posteriores también tienen fecha: la del 2026-11-05 retiró la afirmación de que una
atracción pequeña estaba menos acotada, y la del 2026-11-18 corrigió el acceso y los radios.

**¿Qué recomiendan?**
Si la meta es pagar programas y abrir cuentas, el banco cumple, sobre todo en lo marginado. Si la
meta es inclusión financiera con efectos reales o atraer a la banca privada, abrir sucursales no
basta: importa lo que ofrecen (crédito, ahorro, pagos). Para evaluarlo mejor: publicar el padrón
agregado por municipio y bimestre, las fechas de obra y las cuentas activas y saldos del banco.

**¿Validez externa?**
El resultado es de una red pública que no presta, en municipios pequeños y rurales, con 1 a 3 años
de seguimiento. No dice nada de una banca pública que sí preste, como la de Brasil (Fonseca y Matray
2024).

**¿Y la seguridad y el voto?**
- Delitos: previos planos y efectos cercanos a cero, pero sin precisión (cotas de 12% a 50%).
- Elecciones: la pre-prueba falla; es descriptivo (Tabla 14).

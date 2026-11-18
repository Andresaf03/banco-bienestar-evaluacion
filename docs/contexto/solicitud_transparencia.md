# Borradores de solicitudes de acceso a la información (2026-11-18)

Son los datos que el trabajo final pide en sus conclusiones y que hoy no son públicos. Se presentan
en la Plataforma Nacional de Transparencia (https://www.plataformadetransparencia.org.mx/). El plazo
legal de respuesta es de 20 días hábiles, prorrogable, así que **no llegarían antes del 7 de
diciembre**: sirven para la versión posterior del trabajo, no para la entrega.

Las tres piden solo **información agregada, sin datos personales**: así no hay causal de reserva
por protección de datos. Antes de enviar, revisar los nombres de los programas contra el catálogo
vigente del Padrón Único de Beneficiarios.

---

## 1. Secretaría de Bienestar: beneficiarios y montos por municipio y bimestre

**Sujeto obligado:** Secretaría de Bienestar.

> Solicito, en formato abierto y procesable (CSV o Excel), el número de personas beneficiarias y el
> monto total pagado, **agregados por municipio** (clave geoestadística del INEGI de cinco dígitos)
> y por **bimestre o periodo de pago**, de enero de 2019 a la fecha más reciente disponible, de los
> siguientes programas:
>
> - Pensión para el Bienestar de las Personas Adultas Mayores;
> - Pensión para el Bienestar de las Personas con Discapacidad Permanente;
> - Programa de Apoyo para el Bienestar de las Niñas y Niños, Hijos de Madres Trabajadoras;
> - Sembrando Vida.
>
> Para cada municipio y periodo, solicito además desagregar el número de personas beneficiarias
> según el **medio de pago**: depósito en cuenta o tarjeta del Banco del Bienestar, otra institución
> financiera, efectivo o mesa de atención, u otro.
>
> No solicito datos personales. La información agregada por municipio deriva de los padrones que la
> Secretaría ya integra en el Padrón Único de Beneficiarios y publica por persona.

## 2. Coordinación Nacional de Becas para el Bienestar Benito Juárez: lo mismo para las becas

**Sujeto obligado:** Coordinación Nacional de Becas para el Bienestar Benito Juárez.

> Solicito, en formato abierto (CSV o Excel), el número de personas becarias y el monto total
> pagado, agregados por municipio (clave del INEGI de cinco dígitos) y por bimestre o periodo de
> pago, de enero de 2019 a la fecha, de las becas de educación básica (Beca Universal "Rita
> Cetina" o su antecesora) y de educación media superior, y de Jóvenes Escribiendo el Futuro. Para
> cada municipio y periodo, solicito el número de becarios por medio de pago (tarjeta del Banco del
> Bienestar, otra institución, efectivo u otro). No solicito datos personales.

## 3. Banco del Bienestar: fechas de obra y de operación, uso de cuentas

**Sujeto obligado:** Banco del Bienestar, S.N.C., I.B.D.

> Solicito, en formato abierto (CSV o Excel), para cada sucursal del Banco del Bienestar:
>
> 1. identificador, municipio y localidad (claves del INEGI) y coordenadas;
> 2. fecha de terminación de la obra o de entrega del inmueble, y fecha de inicio de operación al
>    público;
> 3. en su caso, fecha de cierre o suspensión.
>
> Y, **agregado por sucursal o por municipio y por trimestre**, de 2019 a la fecha:
>
> 4. número de cuentas de captación y de ellas cuántas tuvieron al menos un movimiento en el
>    trimestre (cuentas activas);
> 5. saldo promedio y saldo total de captación;
> 6. número y monto de créditos otorgados;
> 7. número y monto de retiros en ventanilla y en cajeros automáticos.
>
> No solicito datos personales ni información de clientes individuales.

---

## Para qué sirve cada una en el trabajo

| Solicitud | Pregunta que respondería | Diseño |
|---|---|---|
| 1 y 2 | ¿Llegaron más programas donde abrió el banco? ¿Cambió el medio de pago? | DiD escalonado municipal con el mismo G (el bloque A preregistrado de la fase 6) |
| 3, fechas | ¿Es la sucursal o su construcción? | Separar la obra de la apertura en el DENUE (gradiente por exposición) |
| 3, uso | ¿Las cuentas se usan más allá de cobrar? | Uso por sucursal y trimestre (fase 5, sin la limitación de los conteos) |

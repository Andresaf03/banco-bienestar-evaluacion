Andrés Álvarez
Fernando Barba
Luis Islas
Tópicos de políticas públicas II
Jueves 17 de septiembre del 2026

# Propuesta (borrador v1, texto original del equipo)

## 1. Título

Efectos del Plan de Expansión del Banco del Bienestar sobre la actividad financiera municipal en México, 2021-2024.

## 2. Pregunta de investigación

1. ¿La apertura escalonada de sucursales del Banco del Bienestar incrementó la actividad financiera del resto del sistema en los municipios que recibieron una sucursal, frente a municipios comparables que la recibieron más tarde o nunca, y ese efecto fue mayor en los municipios que antes no tenían ninguna sucursal bancaria?
2. Si abrir más sucursales del Banco del Bienestar incrementa la actividad financiera del municipio dónde se abre y nuestro objetivo es incrementar la tasa de bancarización ¿cuáles serían los mejores municipios para poner las siguientes X sucursales?

## 3. Mérito intelectual

En la literatura, se ha estudiado extensivamente el efecto de la apertura de instituciones financieras o sucursales de estas en diversas variables de interés. Algunas de ellas son: bancarización, ahorro, depósitos, préstamos, empleo, riqueza, y PIB. Los resultados son diversos, pero es frecuente que los programas y políticas públicas sean dirigidos a zonas desbancarizadas y, en general, se ha observado una mejora en dichas variables de interés. Con esto en mente, hay aún un hueco que podemos cubrir. Hasta nuestro entendimiento, no existe ningún estudio que implemente una metodología de inferencia causal para analizar el efecto de la implementación de las sucursales del Banco del Bienestar en México en la actividad financiera. De la misma manera, no se ha utilizado la técnica de diferencia en diferencias con tratamiento escalonado en ningún estudio de bancarización o instituciones financieras en México.

Entonces, tanto la ausencia de un estudio causal en condiciones y la novedosa formalización de la técnica que encaja perfectamente con las condiciones del tratamiento, creemos que sería valioso evaluar la política pública que despliega el Banco del Bienestar. Una propuesta que, como se suele acostumbrar en esta literatura de microfinanzas, está dirigida a personas con baja penetración en el sistema financiero, usualmente por condiciones de alta marginación. Además, del acceso a servicios financieros, el programa fue pensado para facilitar la dispersión de apoyos económicos del gobierno y el acceso a las remesas. Es lógico imaginar que el aumento de la exposición de las personas a la banca puede aumentar su propensión de ahorro, su riqueza o su probabilidad de establecerse en un empleo. Pero, con la falta de transparencia en el uso de los recursos, las aperturas retrasadas y la falta de personal en estás sucursales, ¿realmente estas sucursales tuvieron algún efecto?

## 4. Diseño del análisis

El diseño está pensado primeramente como causal, aunque podría extenderse a un diseño predictivo si el hallazgo causal es significativo. Una vez establecido esto, con la información de la ubicación de las sucursales del Banco del Bienestar y su momento de inicio de actividades planeamos hacer un análisis con staggered difference in differences. Esto se debe a que la implementación de las sucursales del Banco del Bienestar siguió está metodología. Es decir, el tratamiento asignado (como experimento natural) fue escalonado, no todos los municipios recibieron una sucursal a la vez, sino que su apertura fue en distintos momentos del tiempo. Por esto, podemos medir el efecto de la apertura del Banco del Bienestar en el grupo (municipo) i en el tiempo t, para alguna de nuestras variables de interés.

## 5. Fuentes de datos

La fuente principal es la Base de Datos de Inclusión Financiera de la Comisión Nacional Bancaria y de Valores, trimestral y a nivel municipal desde 2009 y de descarga libre en gob.mx. Esta contiene número de sucursales, corresponsales, cajeros automáticos y terminales puntos de venta, contratos de captación y crédito y transacciones, desagregados por tipo de institución (banca múltiple, banca de desarrollo, sociedades cooperativas de ahorro y préstamo y sociedades financieras populares), lo que permite construir tanto la variable de tratamiento como los resultados excluyendo al propio Banco del Bienestar. Esta fuente se puede complementar con el directorio de sucursales del Banco del Bienestar y los informes de gobierno para fechar y validar aperturas, con las proyecciones de población y el índice de marginación del CONAPO para covariables, con el Censo de Población y Vivienda 2020 del INEGI para características municipales, y con la Encuesta Nacional de Inclusión Financiera 2018, 2021 y 2024 para contrastar a nivel de personas lo que observemos en los agregados. Todas las fuentes son públicas y descargables.

## Referencias

Ver `docs/contexto/referencias.md` (29 fuentes, APA 7). Faltan: Portafolio de Información CNBV y Marco Geoestadístico INEGI (ver `propuesta_v1_revision.md`).

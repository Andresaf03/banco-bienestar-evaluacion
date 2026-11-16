# Por qué Callaway–Sant'Anna y por qué esos controles (2026-10-14, con la fase 4)

Nota para el profesor y el equipo. Usa solo cifras ya corridas (fuentes al final). Resultado:
sucursales privadas (banca múltiple más EACP) por cada 10 mil adultos. Media previa de las tratadas:
0.929. Un efecto de ±5% equivale a ±0.046.

## 1. Por qué no basta una regresión con efectos fijos de municipio y trimestre

Las sucursales abren de forma escalonada: 9 cohortes entre 2022T1 y 2024T1. En ese caso, el TWFE
compara también a las que abren tarde contra las que abrieron antes, que ya están tratadas. Si el
efecto cambia con el tiempo que lleva abierta la sucursal, esas comparaciones lo sesgan, y el
coeficiente puede tener incluso el signo equivocado (Goodman-Bacon, 2021; de Chaisemartin y
D'Haultfœuille, 2020).

Callaway y Sant'Anna (2021) evitan eso. Calculan un DiD 2×2 por cohorte y trimestre, siempre contra
municipios que todavía no abren, y luego promedian. No es una caja negra: cada ATT(g, t) es una
diferencia de diferencias simple, reponderada por covariables.

**Aquí el sesgo del TWFE es chico:** solo el 11.9% de su peso está en comparaciones prohibidas.
Por eso todos los estimadores dicen lo mismo.

| Estimador | Efecto | ee |
|---|---|---|
| Callaway–Sant'Anna (DR, aún no tratados) | +0.0066 | 0.0094 |
| TWFE con efectos fijos de municipio y trimestre | +0.0091 | 0.0204 |
| Sun y Abraham | +0.0029 | 0.0135 |
| Borusyak, Jaravel y Spiess (imputación) | +0.0115 | 0.0247 |
| DiD apilado (efectos fijos de unidad × pila y de evento) | +0.8% de la media (IC90 ±2.7%) | — |

La fase 4 agregó las regresiones con efectos fijos que pide la crítica (`fase4_efectos_fijos.csv`):

| Regresión con efectos fijos | Efecto (% de la media) |
|---|---|
| Estudio de evento TWFE clásico (promedio e = 0…8; previos planos, p = 0.74) | −0.6% |
| TWFE extendido de Wooldridge (2021), sin covariables | +1.8% |
| DiD apilado con efectos fijos de estado × evento | +2.5% |
| TWFE con efectos fijos de estado × trimestre | +1.1% |
| TWFE con tendencias lineales por municipio | −0.5% |
| **TWFE extendido con covariables** | **+6.8% (ee 2.7%)** |

Casi todas las regresiones con efectos fijos dicen lo mismo que CS. **La excepción honesta** es el
TWFE extendido con covariables, que da +6.8% en privadas y +11% en EACP. Depende de comparar
contra los 500 municipios que nunca abren: si se compara solo a los que abren temprano contra los
que abren tarde (hasta 2023T4), baja a **+1.3% (ee 1.3%)**. Tampoco es el ajuste por covariables
en sí: CS con el mismo ajuste lineal (solo regresión de resultado) da +2.1% (ee 1.7%). Lo que no
cierra es que recortar al soporte común no lo baje (+7.7%), así que una atracción pequeña está
menos acotada que el desplazamiento.

Así que:
- **"No desplazó a la banca privada"** no depende del estimador en sucursales privadas: ninguno da
  un efecto negativo significativo. En banca múltiple sola, el TWFE, BJS y el TWFE extendido sin
  covariables dan entre −2.2% y −2.5%. Es pequeño (menor a 5%) y, en el extendido, con pre-prueba
  fallida; CS da −0.2%.
- **"Tampoco la atrajo"** depende de esa única especificación.

Las regresiones con efectos fijos son además menos precisas: el IC90 del TWFE llega a 4.6% de la
media y el de BJS a 5.6%. Por eso CS es el principal.

## 2. Por qué esos controles (grupo de comparación)

- **Aún no tratados, no nunca tratados.** Los 500 municipios que nunca abren son muy distintos:
  mediana de 1,596 adultos, 83% rurales y solo 4% con banca múltiple. Los que abren más tarde
  fueron elegidos por el mismo programa, así que se parecen más a los que abren antes.
- **El resultado no cambia con el otro grupo:** solo con nunca tratados, +0.0081 (ee 0.0106).
- **Fase 4:**
  - solo con municipios que alguna vez abren (sin nunca tratados; 1,248 tratadas hasta 2023T4,
    con la cohorte de 2024T1 como control), −1.9% (cota 4.2%);
  - nunca tratados emparejados por puntaje de propensión, +2.3%;
  - controles sin ningún vecino que abra, +0.6% (cota 2.0%).
- **Una advertencia que hay que decir:** el 92% de los nunca tratados colinda con un municipio que
  abre.

## 3. Por qué esas covariables

- Son tres, y todas se miden antes de casi todas las aperturas (2022–2024):
  - log de la población (Censo 2020);
  - índice de marginación 2020 (CONAPO);
  - si había banca múltiple en 2019T1.
- Se eligieron porque explican dónde y cuándo se abre: los municipios más poblados abren 1.4 meses
  antes por cada desviación estándar.
- **Sin covariables el resultado no cambia:** +0.0038 (ee 0.0102).
- **Balance.** Las covariables separan bien a tratados de controles (AUC 0.66–0.86). Tras
  reponderar quedan balanceadas (diferencia estandarizada ≤ 0.11), salvo las cohortes 2023T4 y
  2024T1. Sin esas dos cohortes: −0.0037 (ee 0.0128), y el nulo se sostiene.
- **Anticipación** (la obra era visible antes de abrir): con un trimestre de anticipación, +0.0067.
- **Fase 4, covariables una por una** (ninguna, población, + marginación, + banca 2019,
  + tendencia previa 2017–2018, + distancia a la banca, + región): entre +0.4% y +1.2%.

## 4. Lo que la crítica sí puede decir

1. **Las tendencias paralelas no se prueban, solo se apoyan.** Los previos son planos (Wald
   p = 0.29). La fase 4 suma más apoyo:
   - el placebo de fecha (2017–2021, apertura falsa 8 trimestres antes) da −0.6%;
   - HonestDiD con suavidad, que permite tendencias lineales, deja el efecto promedio de los tres
     primeros trimestres entre −4.0% y +2.2%;
   - la permutación dentro del estado da p = 0.32.
2. **Derrames.** Si la sucursal afecta también a los municipios vecinos que sirven de control, el
   efecto se sesga hacia cero. En los vecinos de los municipios que abren el efecto es +0.5% (cota
   4.0%), así que no hay señal de derrame.
3. **Horizonte corto y solo oferta:** de 1 a 3 años, y solo sucursales y cuentas.

## 5. Fase 4 (preregistrada; resultados en `docs/decisiones.md`)

Todo lo anterior está corrido. La figura `outputs/figuras/fig_fase4_estimadores.png` pone todos los
estimadores juntos, en % de la media, con la banda de ±5%.

## Fuentes

- `outputs/tablas/comp_municipio_trim_esc_sucursales_privado_pc.csv` (estimadores)
- `outputs/tablas/apilado_resumen.csv` (apilado)
- `outputs/tablas/rob_municipio_trim_esc_sucursales_privado_pc.csv` (nunca tratados, sin
  covariables, anticipación)
- `outputs/tablas/desc_soporte_comun.csv` y `desc_soporte_robustez.csv` (balance)
- `outputs/tablas/bacon_municipio_trim_esc_sucursales_privado_pc.csv` (Goodman-Bacon)
- `outputs/tablas/desc_calendario_aperturas.csv` (calendario)
- `docs/decisiones.md` P-3 (descripción de los nunca tratados)
- `outputs/tablas/tabla_final.csv` (HonestDiD y pre-prueba)

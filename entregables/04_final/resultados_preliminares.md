# Resultados

Generado por `python -m proyecto.utils.reporte` el 2026-10-08. La especificación principal, las familias de inferencia múltiple y el umbral de equivalencia están preregistrados en `docs/decisiones.md` (2026-09-29).

Convenciones: ATT de Callaway y Sant'Anna (DR) con error estándar agrupado por municipio (Liang–Zeger sobre la función de influencia). *Efecto %*, *MDE80 %* y *cota TOST %* están en porcentaje de la media de las tratadas en su último periodo previo. *Cota TOST* es el mayor valor absoluto del IC al 90%: si queda por debajo de 5% y el ATT no es significativo, el nulo es informativo. *Previos sig.* cuenta los coeficientes previos significativos al 5%; *Wald previa* prueba que todos sean cero; el *placebo 2019S2* es el salto de la actualización integral previa a todo tratamiento. Significancia: * 10%, ** 5%, *** 1%.

## Especificación principal

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Localidad | entre actualizaciones | estab_abarrotes_pc | 0.780 | 0.231 | *** | 4.790 | 3.977 | 7.125 | 1/2 | 0.004 | 0.725 | 0.004 | 0.001 |  | 1106/21719 |
| Localidad | entre actualizaciones | estab_consumo_pc | 2.952 | 0.559 | *** | 8.226 | 4.364 | 10.788 | 2/2 | 0.000 | 1.498 | 0.000 | 0.000 | [-1.757, 7.801] | 1106/21719 |
| Localidad | entre actualizaciones | estab_restaurantes_pc | 0.806 | 0.203 | *** | 10.458 | 7.378 | 14.790 | 1/2 | 0.013 | 0.288 | 0.001 | 0.000 |  | 1106/21719 |
| Localidad | entre actualizaciones | empleo_est_emprendimiento_pc | 33.786 | 6.912 | *** | 10.598 | 6.074 | 14.164 | 0/2 | 0.784 | -0.412 | 0.000 | 0.000 |  | 1106/21719 |
| Localidad | entre actualizaciones | estab_emprendimiento_pc | 7.242 | 1.104 | *** | 10.400 | 4.440 | 13.007 | 0/2 | 0.057 | 1.714 | 0.000 | 0.000 | [-0.611, 15.094] | 1106/21719 |
| Localidad | entre actualizaciones | micro_emprendimiento_pc | 6.940 | 1.068 | *** | 10.864 | 4.685 | 13.615 | 0/2 | 0.061 | 2.038 | 0.000 | 0.000 |  | 1106/21719 |
| Localidad | entre actualizaciones | estab_consultorios_pc | 0.159 | 0.038 | *** | 11.730 | 7.771 | 16.293 | 0/2 | 0.726 | 0.022 | 0.000 | 0.000 |  | 1106/21719 |
| Localidad | entre actualizaciones | estab_farmacia_pc | 0.256 | 0.067 | *** | 12.021 | 8.827 | 17.204 | 1/2 | 0.096 | 0.126 | 0.001 | 0.000 |  | 1106/21719 |
| Localidad | entre actualizaciones | estab_salud_pc | 0.334 | 0.060 | *** | 9.587 | 4.857 | 12.439 | 1/2 | 0.036 | 0.174 | 0.000 | 0.000 | [-0.274, 0.926] | 1106/21719 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_bm_pc | -0.001 | 0.006 |  | -0.242 | 4.365 | 2.805 | 0/19 | 0.055 |  | 0.948 | 0.879 | [-0.114, 0.118] | 1457/500 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_eacp_pc | 0.008 | 0.009 |  | 1.452 | 4.923 | 4.342 | 1/19 | 0.515 |  | 0.605 | 0.702 | [-0.174, 0.177] | 1457/500 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_privado_pc | 0.007 | 0.009 |  | 0.713 | 2.838 | 2.379 | 2/19 | 0.287 |  | 0.685 | 0.737 | [-0.228, 0.230] | 1457/500 |

Nulos informativos (±5%): sucursales_bm_pc, sucursales_eacp_pc, sucursales_privado_pc.

## ENIF: tenencia de cuenta por tamaño de localidad (descriptivo)

Tabulados oficiales, población de 18 a 70 años. La ENIF no es representativa por municipio: es contraste, no estimación causal.

| anio | bloque | pct_con_cuenta | pct_cuentahabientes_con_cuenta_apoyos | pct_adultos_con_cuenta_apoyos |
|---|---|---|---|---|
| 2018 | 15 mil y más | 51.4 | 8.3 | 4.2 |
| 2021 | 15 mil y más | 55.1 | 7.8 | 4.3 |
| 2024 | 15 mil y más | 69.1 | 12.5 | 8.7 |
| 2018 | menos de 15 mil | 39.0 | 39.8 | 15.6 |
| 2021 | menos de 15 mil | 38.1 | 27.8 | 10.6 |
| 2024 | menos de 15 mil | 51.4 | 33.7 | 17.3 |
| 2018 | nacional | 47.1 | 17.4 | 8.2 |
| 2021 | nacional | 49.1 | 13.2 | 6.5 |
| 2024 | nacional | 63.0 | 18.5 | 11.7 |

## Medición del DENUE entre versiones

Porcentaje de localidades cuyo conteo cambia respecto de la versión anterior y crecimiento del total. Las actualizaciones integrales son s = 8 (2019S2) y s = 18 (2024S2); entre ellas el resultado casi no se actualiza.

| tiempo | grupo | unidades | pct_con_cambio | cambio_abs_medio | total | crecimiento_pct | resultado |
|---|---|---|---|---|---|---|---|
| 2 | control (≥10 km) | 21719 | 2.035 | 0.066 | 110794 | 0.998 | estab_emprendimiento |
| 3 | control (≥10 km) | 21719 | 1.289 | 0.020 | 110800 | 0.005 | estab_emprendimiento |
| 4 | control (≥10 km) | 21719 | 2.426 | 0.073 | 110875 | 0.068 | estab_emprendimiento |
| 5 | control (≥10 km) | 21719 | 0.760 | 0.017 | 111144 | 0.243 | estab_emprendimiento |
| 6 | control (≥10 km) | 21719 | 0.787 | 0.009 | 111191 | 0.042 | estab_emprendimiento |
| 7 | control (≥10 km) | 21719 | 4.268 | 0.121 | 111425 | 0.210 | estab_emprendimiento |
| 8 | control (≥10 km) | 21719 | 10.627 | 1.053 | 124624 | 11.846 | estab_emprendimiento |
| 9 | control (≥10 km) | 21719 | 2.500 | 0.051 | 125403 | 0.625 | estab_emprendimiento |
| 10 | control (≥10 km) | 21719 | 3.485 | 0.101 | 126664 | 1.006 | estab_emprendimiento |
| 11 | control (≥10 km) | 21719 | 1.579 | 0.095 | 126679 | 0.012 | estab_emprendimiento |
| 12 | control (≥10 km) | 21719 | 0.322 | 0.016 | 126940 | 0.206 | estab_emprendimiento |
| 13 | control (≥10 km) | 21719 | 0.184 | 0.002 | 126924 | -0.013 | estab_emprendimiento |
| 14 | control (≥10 km) | 21719 | 0.723 | 0.008 | 127040 | 0.091 | estab_emprendimiento |
| 16 | control (≥10 km) | 21719 | 3.306 | 0.143 | 125430 | -1.267 | estab_emprendimiento |
| 17 | control (≥10 km) | 21719 | 4.061 | 0.069 | 126018 | 0.469 | estab_emprendimiento |
| 18 | control (≥10 km) | 21719 | 7.316 | 1.251 | 141710 | 12.452 | estab_emprendimiento |
| 19 | control (≥10 km) | 21719 | 7.666 | 0.548 | 143564 | 1.308 | estab_emprendimiento |
| 2 | tratada | 1106 | 25.045 | 1.202 | 467814 | 0.257 | estab_emprendimiento |
| 3 | tratada | 1106 | 27.939 | 0.637 | 468064 | 0.053 | estab_emprendimiento |
| 4 | tratada | 1106 | 21.248 | 0.656 | 468355 | 0.062 | estab_emprendimiento |
| 5 | tratada | 1106 | 30.561 | 1.222 | 469568 | 0.259 | estab_emprendimiento |
| 6 | tratada | 1106 | 17.450 | 0.259 | 469647 | 0.017 | estab_emprendimiento |
| 7 | tratada | 1106 | 40.597 | 2.664 | 472283 | 0.561 | estab_emprendimiento |
| 8 | tratada | 1106 | 83.816 | 56.819 | 524883 | 11.137 | estab_emprendimiento |
| 9 | tratada | 1106 | 47.378 | 2.571 | 527249 | 0.451 | estab_emprendimiento |
| 10 | tratada | 1106 | 50.904 | 4.634 | 531944 | 0.890 | estab_emprendimiento |
| 11 | tratada | 1106 | 26.221 | 5.320 | 530846 | -0.206 | estab_emprendimiento |
| 12 | tratada | 1106 | 15.009 | 1.569 | 532349 | 0.283 | estab_emprendimiento |
| 13 | tratada | 1106 | 8.680 | 0.118 | 532315 | -0.006 | estab_emprendimiento |
| 14 | tratada | 1106 | 14.557 | 0.193 | 532395 | 0.015 | estab_emprendimiento |
| 16 | tratada | 1106 | 64.286 | 2.176 | 533454 | 0.199 | estab_emprendimiento |
| 17 | tratada | 1106 | 48.463 | 2.863 | 535062 | 0.301 | estab_emprendimiento |
| 18 | tratada | 1106 | 83.002 | 69.945 | 601615 | 12.438 | estab_emprendimiento |
| 19 | tratada | 1106 | 76.492 | 6.929 | 605993 | 0.728 | estab_emprendimiento |
| 2 | control (≥10 km) | 21719 | 1.133 | 0.045 | 99369 | 0.821 | micro_emprendimiento |
| 3 | control (≥10 km) | 21719 | 1.216 | 0.020 | 99203 | -0.167 | micro_emprendimiento |
| 4 | control (≥10 km) | 21719 | 1.381 | 0.046 | 99178 | -0.025 | micro_emprendimiento |
| 5 | control (≥10 km) | 21719 | 0.695 | 0.016 | 99431 | 0.255 | micro_emprendimiento |
| 6 | control (≥10 km) | 21719 | 0.470 | 0.006 | 99402 | -0.029 | micro_emprendimiento |
| 7 | control (≥10 km) | 21719 | 2.845 | 0.088 | 99542 | 0.141 | micro_emprendimiento |
| 8 | control (≥10 km) | 21719 | 8.923 | 0.931 | 109406 | 9.909 | micro_emprendimiento |
| 9 | control (≥10 km) | 21719 | 3.159 | 0.063 | 110207 | 0.732 | micro_emprendimiento |
| 10 | control (≥10 km) | 21719 | 4.775 | 0.125 | 111755 | 1.405 | micro_emprendimiento |
| 11 | control (≥10 km) | 21719 | 1.229 | 0.079 | 111669 | -0.077 | micro_emprendimiento |
| 12 | control (≥10 km) | 21719 | 0.304 | 0.015 | 111947 | 0.249 | micro_emprendimiento |
| 13 | control (≥10 km) | 21719 | 0.101 | 0.001 | 111949 | 0.002 | micro_emprendimiento |
| 14 | control (≥10 km) | 21719 | 0.930 | 0.013 | 111866 | -0.074 | micro_emprendimiento |
| 16 | control (≥10 km) | 21719 | 1.819 | 0.101 | 110213 | -1.478 | micro_emprendimiento |
| 17 | control (≥10 km) | 21719 | 3.071 | 0.050 | 110669 | 0.414 | micro_emprendimiento |
| 18 | control (≥10 km) | 21719 | 6.142 | 1.143 | 125960 | 13.817 | micro_emprendimiento |
| 19 | control (≥10 km) | 21719 | 7.491 | 0.498 | 127915 | 1.552 | micro_emprendimiento |
| 2 | tratada | 1106 | 20.615 | 0.845 | 426832 | 0.194 | micro_emprendimiento |
| 3 | tratada | 1106 | 26.492 | 0.608 | 426632 | -0.047 | micro_emprendimiento |
| 4 | tratada | 1106 | 17.631 | 0.415 | 426693 | 0.014 | micro_emprendimiento |
| 5 | tratada | 1106 | 29.204 | 1.136 | 427827 | 0.266 | micro_emprendimiento |
| 6 | tratada | 1106 | 15.099 | 0.280 | 427647 | -0.042 | micro_emprendimiento |
| 7 | tratada | 1106 | 35.533 | 2.089 | 429643 | 0.467 | micro_emprendimiento |
| 8 | tratada | 1106 | 82.640 | 52.282 | 475685 | 10.716 | micro_emprendimiento |
| 9 | tratada | 1106 | 53.797 | 1.742 | 476222 | 0.113 | micro_emprendimiento |
| 10 | tratada | 1106 | 60.036 | 5.136 | 481568 | 1.123 | micro_emprendimiento |
| 11 | tratada | 1106 | 24.141 | 4.927 | 480435 | -0.235 | micro_emprendimiento |
| 12 | tratada | 1106 | 14.376 | 1.531 | 481994 | 0.324 | micro_emprendimiento |
| 13 | tratada | 1106 | 7.414 | 0.088 | 481987 | -0.001 | micro_emprendimiento |
| 14 | tratada | 1106 | 23.779 | 0.473 | 481654 | -0.069 | micro_emprendimiento |
| 16 | tratada | 1106 | 61.031 | 1.709 | 482394 | 0.154 | micro_emprendimiento |
| 17 | tratada | 1106 | 41.049 | 2.158 | 483337 | 0.195 | micro_emprendimiento |
| 18 | tratada | 1106 | 82.731 | 65.989 | 546467 | 13.061 | micro_emprendimiento |
| 19 | tratada | 1106 | 77.848 | 7.931 | 552929 | 1.183 | micro_emprendimiento |

## Régimen de levantamiento censal (descriptivo)

Los Censos Económicos que alimentan las actualizaciones integrales del DENUE recorren manzana por manzana las cabeceras municipales y las localidades de 2,500 habitantes o más; el resto del territorio rural va por muestra (INEGI, CE 2024, Metodología). Cambio medio del resultado en cada actualización por grupo y régimen, y su diferencia bruta contra los controles del mismo régimen (sin covariables).

| resultado | grupo | regimen | unidades | pct_unidades_grupo | base_2024S1 | cambio_2019S2 | cambio_2024S2 | dif_2019S2_vs_control | dif_2024S2_vs_control |
|---|---|---|---|---|---|---|---|---|---|
| estab_consumo_pc | 1 con sucursal | muestra rural | 203 | 18.35 | 2.86 | 0.08 | 0.74 | -0.01 | 0.56 |
| estab_consumo_pc | 1 con sucursal | recorrido total | 903 | 81.65 | 44.07 | 4.96 | 8.03 | 1.87 | 2.28 |
| estab_consumo_pc | 2 vecina 0–2 km | muestra rural | 2089 | 85.97 | 0.83 | -0.13 | 0.11 | -0.21 | -0.07 |
| estab_consumo_pc | 2 vecina 0–2 km | recorrido total | 341 | 14.03 | 43.61 | 5.28 | 8.86 | 2.19 | 3.10 |
| estab_consumo_pc | 3 vecina 2–5 km | muestra rural | 6705 | 93.93 | 0.87 | 0.27 | 0.10 | 0.18 | -0.08 |
| estab_consumo_pc | 3 vecina 2–5 km | recorrido total | 433 | 6.07 | 30.23 | 4.33 | 7.68 | 1.24 | 1.92 |
| estab_consumo_pc | 4 vecina 5–10 km | muestra rural | 9530 | 95.97 | 0.42 | 0.05 | 0.10 | -0.04 | -0.08 |
| estab_consumo_pc | 4 vecina 5–10 km | recorrido total | 400 | 4.03 | 32.77 | 3.84 | 5.93 | 0.75 | 0.17 |
| estab_consumo_pc | 5 control ≥10 km | muestra rural | 21241 | 97.80 | 0.91 | 0.09 | 0.18 | 0.00 | 0.00 |
| estab_consumo_pc | 5 control ≥10 km | recorrido total | 478 | 2.20 | 31.28 | 3.09 | 5.75 | 0.00 | 0.00 |
| estab_emprendimiento_pc | 1 con sucursal | muestra rural | 203 | 18.35 | 5.87 | -0.04 | 1.24 | -0.07 | 1.38 |
| estab_emprendimiento_pc | 1 con sucursal | recorrido total | 903 | 81.65 | 85.36 | 9.11 | 13.28 | 2.88 | 4.91 |
| estab_emprendimiento_pc | 2 vecina 0–2 km | muestra rural | 2089 | 85.97 | 2.47 | -0.01 | 0.16 | -0.04 | 0.30 |
| estab_emprendimiento_pc | 2 vecina 0–2 km | recorrido total | 341 | 14.03 | 79.40 | 9.24 | 13.65 | 3.01 | 5.29 |
| estab_emprendimiento_pc | 3 vecina 2–5 km | muestra rural | 6705 | 93.93 | 2.23 | 0.49 | 0.06 | 0.45 | 0.20 |
| estab_emprendimiento_pc | 3 vecina 2–5 km | recorrido total | 433 | 6.07 | 59.04 | 8.89 | 12.77 | 2.66 | 4.41 |
| estab_emprendimiento_pc | 4 vecina 5–10 km | muestra rural | 9530 | 95.97 | 1.30 | -0.12 | -0.09 | -0.15 | 0.05 |
| estab_emprendimiento_pc | 4 vecina 5–10 km | recorrido total | 400 | 4.03 | 71.06 | 8.09 | 9.28 | 1.86 | 0.92 |
| estab_emprendimiento_pc | 5 control ≥10 km | muestra rural | 21241 | 97.80 | 2.63 | 0.03 | -0.14 | 0.00 | 0.00 |
| estab_emprendimiento_pc | 5 control ≥10 km | recorrido total | 478 | 2.20 | 68.85 | 6.23 | 8.37 | 0.00 | 0.00 |
| estab_salud_pc | 1 con sucursal | muestra rural | 203 | 18.35 | 0.26 | 0.05 | 0.01 | 0.05 | 0.00 |
| estab_salud_pc | 1 con sucursal | recorrido total | 903 | 81.65 | 4.31 | 0.50 | 0.77 | 0.27 | 0.31 |
| estab_salud_pc | 2 vecina 0–2 km | muestra rural | 2089 | 85.97 | 0.05 | -0.01 | 0.00 | -0.01 | -0.01 |
| estab_salud_pc | 2 vecina 0–2 km | recorrido total | 341 | 14.03 | 4.20 | 0.58 | 0.80 | 0.35 | 0.33 |
| estab_salud_pc | 3 vecina 2–5 km | muestra rural | 6705 | 93.93 | 0.05 | 0.00 | 0.02 | 0.00 | 0.02 |
| estab_salud_pc | 3 vecina 2–5 km | recorrido total | 433 | 6.07 | 2.59 | 0.35 | 0.65 | 0.12 | 0.18 |
| estab_salud_pc | 4 vecina 5–10 km | muestra rural | 9530 | 95.97 | 0.03 | -0.00 | 0.01 | -0.00 | -0.00 |
| estab_salud_pc | 4 vecina 5–10 km | recorrido total | 400 | 4.03 | 3.32 | 0.33 | 0.57 | 0.10 | 0.10 |
| estab_salud_pc | 5 control ≥10 km | muestra rural | 21241 | 97.80 | 0.05 | -0.00 | 0.01 | 0.00 | 0.00 |
| estab_salud_pc | 5 control ≥10 km | recorrido total | 478 | 2.20 | 3.17 | 0.23 | 0.47 | 0.00 | 0.00 |

## EACP: captación, crédito y tarjetas, 2019T1–2025T4

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | capt_ahorro_eacp_pc | 7.443 | 19.276 |  | 0.484 | 3.509 | 2.544 | 1/19 | 0.510 |  | 0.837 | 0.707 | [-741.177, 737.544] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | capt_plazo_eacp_pc | -14.261 | 11.088 |  | -6.053 | 13.185 | 13.794 | 1/19 | 0.206 |  | 0.397 | 0.527 | [-156.105, 134.516] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | capt_vista_eacp_pc | -63.519 | 72.027 |  | -5.388 | 17.117 | 15.438 | 3/19 | 0.191 |  | 0.583 | 0.639 | [-1,057.853, 1,048.707] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | cred_consumo_eacp_pc | 16.869 | 5.795 | *** | 4.258 | 4.098 | 6.663 | 3/19 | 0.176 |  | 0.018 | 0.008 | [-398.015, 406.144] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | cred_vivienda_eacp_pc | -0.189 | 0.131 |  | -4.720 | 9.127 | 10.079 | 0/19 | 0.204 |  | 0.352 | 0.498 | [-17.188, 17.012] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | tarjetas_debito_eacp_pc | -77.295 | 42.867 | * | -113.277 | 176.001 | 216.611 | 5/19 | 0.001 |  | 0.211 | 0.258 | [-188.209, 157.304] | 1457/499 |

Nulos informativos (±5%): capt_ahorro_eacp_pc.

## Inclusión total (banca múltiple + desarrollo, incluye al Banco del Bienestar)

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | capt_ahorro_banca_pc | 2.404 | 3.705 |  | 15.127 | 65.319 | 53.477 | 0/19 | 0.155 |  | 0.708 |  |  | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | capt_plazo_banca_pc | 6.719 | 5.209 |  | 9.425 | 20.471 | 21.444 | 0/19 | 0.785 |  | 0.397 |  |  | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | cuentas_celular_total_pc | -179.814 | 119.306 |  | -4.922 | 9.149 | 10.294 | 5/19 | 0.000 |  | 0.336 |  |  | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | tarjetas_debito_banca_pc | 3,313.567 | 219.974 | *** | 101.519 | 18.881 | 112.604 | 2/19 | 0.188 |  | 0.000 |  |  | 1457/499 |

## Primera etapa: sucursales totales y cuentas del Banco del Bienestar

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | capt_total_bd_pc | 1,267.912 | 165.435 | *** | 2,664.366 | 973.950 | 3,236.187 | 0/4 | 0.510 |  |  |  |  | 766/499 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_total_pc | 2.002 | 0.083 | *** | 214.985 | 24.869 | 229.586 | 2/19 | 0.279 |  |  |  |  | 1457/500 |
| Municipio (trimestral, BDIF) | escalonado | tarjetas_debito_bd_pc | 2,411.501 | 296.054 | *** | 2,550.383 | 877.189 | 3,065.394 | 0/4 | 0.461 |  |  |  |  | 766/499 |

## Empleo formal (IMSS, cierres de trimestre 2019T1–2025T4)

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | log_salario_diario | -0.019 | 0.010 | * | -1.852 | 2.940 | 3.579 | 1/19 | 0.749 |  | 0.221 | 0.139 |  | 1437/445 |
| Municipio (trimestral, BDIF) | escalonado | ta_micro_pc | -1.099 | 2.476 |  | -1.978 | 12.486 | 9.309 | 2/19 | 0.021 |  | 0.824 | 0.706 | [-12.828, 13.082] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | ta_pc | -109.427 | 91.125 |  | -17.740 | 41.389 | 42.040 | 3/19 | 0.070 |  | 0.436 | 0.436 | [-222.055, 220.753] | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | ta_pequena_pc | -6.570 | 9.160 |  | -4.497 | 17.568 | 14.812 | 3/19 | 0.036 |  | 0.685 | 0.706 |  | 1457/499 |

## Censos Económicos 2004–2024 (una cohorte en el CE 2024, tres placebos)

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| municipio_ce | escalonado | log_produccion_bruta | 0.118 | 0.083 |  | 11.760 | 23.219 | 25.392 | 0/3 | 0.206 |  | 0.360 | 0.414 |  | 1252/499 |
| municipio_ce | escalonado | log_remuneraciones | 0.126 | 0.079 |  | 12.592 | 22.110 | 25.573 | 0/3 | 0.916 |  | 0.303 | 0.341 |  | 1251/491 |
| municipio_ce | escalonado | log_vacb | 0.231 | 0.066 | *** | 23.061 | 18.523 | 33.936 | 0/3 | 0.376 |  | 0.003 | 0.000 |  | 1252/499 |
| municipio_ce | escalonado | personal_ocupado_pc | 0.177 | 7.593 |  | 0.166 | 19.939 | 11.872 | 0/3 | 0.336 |  | 0.995 | 0.978 | [-19.361, 21.636] | 1252/499 |
| municipio_ce | escalonado | ue_pc | -0.323 | 0.686 |  | -0.899 | 5.343 | 4.036 | 0/3 | 0.210 |  | 0.822 | 0.880 | [-3.793, 2.339] | 1252/499 |

## Remesas por municipio (Banxico)

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | remesas_usd_adulto | 9.008 | 3.944 | ** | 5.423 | 6.652 | 9.329 | 1/19 | 0.001 |  | 0.083 |  | [-110.068, 118.797] | 1456/496 |

## Extensión a 2025T4 de la especificación financiera principal

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | sucursales_bm_pc | -0.010 | 0.009 |  | -2.572 | 6.389 | 6.323 | 1/19 | 0.054 |  | 0.451 |  |  | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_eacp_pc | 0.015 | 0.013 |  | 2.792 | 6.901 | 6.843 | 1/19 | 0.516 |  | 0.451 |  |  | 1457/499 |
| Municipio (trimestral, BDIF) | escalonado | sucursales_privado_pc | 0.004 | 0.014 |  | 0.453 | 4.220 | 2.930 | 2/19 | 0.291 |  | 0.869 |  |  | 1457/499 |

## Especificaciones secundarias

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Localidad | escalonado | estab_abarrotes_pc | 0.036 | 0.031 |  | 0.223 | 0.536 | 0.537 | 0/8 | 0.532 |  | 0.451 |  |  | 1105/21719 |
| Localidad | escalonado | estab_consumo_pc | 0.151 | 0.097 |  | 0.414 | 0.747 | 0.853 | 0/8 | 0.451 |  | 0.318 |  |  | 1105/21719 |
| Localidad | escalonado | estab_restaurantes_pc | 0.038 | 0.028 |  | 0.488 | 1.001 | 1.076 | 0/8 | 0.427 |  | 0.371 |  |  | 1105/21719 |
| Localidad | escalonado | empleo_est_emprendimiento_pc | 3.096 | 2.286 |  | 0.984 | 2.036 | 2.179 | 2/8 | 0.026 |  | 0.371 |  |  | 1105/21719 |
| Localidad | escalonado | estab_emprendimiento_pc | 0.543 | 0.179 | *** | 0.772 | 0.715 | 1.192 | 1/8 | 0.020 |  | 0.013 |  | [-0.971, 2.146] | 1105/21719 |
| Localidad | escalonado | micro_emprendimiento_pc | 0.528 | 0.151 | *** | 0.818 | 0.654 | 1.202 | 0/8 | 0.933 |  | 0.003 |  |  | 1105/21719 |
| Localidad | escalonado | estab_consultorios_pc | 0.003 | 0.003 |  | 0.205 | 0.633 | 0.576 | 0/8 | 0.868 |  | 0.574 |  |  | 1105/21719 |
| Localidad | escalonado | estab_farmacia_pc | 0.010 | 0.014 |  | 0.453 | 1.855 | 1.542 | 0/8 | 0.653 |  | 0.690 |  |  | 1105/21719 |
| Localidad | escalonado | estab_salud_pc | 0.010 | 0.010 |  | 0.273 | 0.788 | 0.736 | 0/8 | 0.242 |  | 0.545 |  |  | 1105/21719 |
| Municipio (semestral) | entre actualizaciones | estab_abarrotes_pc | -0.589 | 1.535 |  | -0.638 | 4.659 | 3.373 | 1/2 | 0.127 | -3.375 | 0.837 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | estab_consumo_pc | 2.793 | 3.239 |  | 1.342 | 4.359 | 3.901 | 1/2 | 0.040 | -3.408 | 0.587 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | estab_restaurantes_pc | 1.827 | 1.301 |  | 3.990 | 7.962 | 8.665 | 0/2 | 0.720 | 0.399 | 0.360 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | empleo_est_emprendimiento_pc | -0.914 | 38.217 |  | -0.048 | 5.564 | 3.314 | 0/2 | 0.714 | -27.742 | 0.995 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | estab_emprendimiento_pc | -0.012 | 6.359 |  | -0.003 | 4.363 | 2.564 | 1/2 | 0.012 | -19.769 | 0.998 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | micro_emprendimiento_pc | -1.845 | 6.120 |  | -0.493 | 4.580 | 3.182 | 1/2 | 0.016 | -19.346 | 0.869 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | estab_farmacia_pc | 0.877 | 0.373 | ** | 7.857 | 9.348 | 13.346 | 0/2 | 0.404 | -0.954 | 0.076 |  |  | 1460/500 |
| Municipio (semestral) | entre actualizaciones | estab_salud_pc | 1.118 | 0.421 | *** | 5.980 | 6.306 | 9.682 | 0/2 | 0.387 | -0.181 | 0.034 |  |  | 1460/500 |
| Municipio (semestral) | escalonado | estab_abarrotes_pc | 0.010 | 0.065 |  | 0.011 | 0.196 | 0.126 | 0/8 | 0.558 |  | 0.948 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | estab_consumo_pc | 0.157 | 0.130 |  | 0.075 | 0.172 | 0.176 | 0/8 | 0.476 |  | 0.436 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | estab_restaurantes_pc | 0.015 | 0.033 |  | 0.033 | 0.201 | 0.151 | 0/8 | 0.118 |  | 0.822 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | empleo_est_emprendimiento_pc | 16.067 | 14.333 |  | 0.846 | 2.115 | 2.088 | 1/8 | 0.138 |  | 0.451 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | estab_emprendimiento_pc | 0.713 | 0.310 | ** | 0.173 | 0.211 | 0.297 | 1/8 | 0.001 |  | 0.083 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | micro_emprendimiento_pc | 0.854 | 0.218 | *** | 0.226 | 0.162 | 0.321 | 1/8 | 0.191 |  | 0.001 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | estab_farmacia_pc | 0.077 | 0.040 | * | 0.674 | 0.982 | 1.250 | 1/8 | 0.241 |  | 0.176 |  |  | 1457/500 |
| Municipio (semestral) | escalonado | estab_salud_pc | 0.045 | 0.021 | ** | 0.235 | 0.317 | 0.421 | 1/8 | 0.448 |  | 0.134 |  |  | 1457/500 |
| Municipio (trimestral, BDIF) | escalonado | corresponsales_total_pc | -0.015 | 0.028 |  | -0.397 | 2.069 | 1.612 | 1/10 | 0.134 |  | 0.781 |  |  | 1248/709 |

## Derrame a localidades vecinas (<10 km)

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Localidad | entre actualizaciones | estab_consumo_pc | 0.083 | 0.057 |  | 3.192 | 6.128 | 6.790 | 1/2 | 0.000 | 0.143 | 0.352 |  |  | 19498/21719 |
| Localidad | entre actualizaciones | estab_emprendimiento_pc | 0.402 | 0.140 | *** | 7.114 | 6.943 | 11.190 | 1/2 | 0.001 | 0.249 | 0.019 |  |  | 19498/21719 |
| Localidad | entre actualizaciones | estab_salud_pc | 0.019 | 0.010 | * | 8.359 | 12.512 | 15.705 | 0/2 | 0.179 | 0.011 | 0.189 |  |  | 19498/21719 |

## BDIF, panel corto 2022T4–2024T4

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | cajeros_privado_pc | -0.072 | 0.069 |  | -2.890 | 7.684 | 7.401 | 0/4 | 0.467 |  | 0.491 |  |  | 766/500 |
| Municipio (trimestral, BDIF) | escalonado | tpv_privado_pc | -0.502 | 2.207 |  | -0.906 | 11.166 | 7.462 | 0/4 | 0.684 |  | 0.919 |  |  | 766/500 |
| Municipio (trimestral, BDIF) | escalonado | transacciones_tpv_privado_pc | -85.350 | 233.148 |  | -2.158 | 16.517 | 11.856 | 0/4 | 0.729 |  | 0.839 |  |  | 766/500 |
| Municipio (trimestral, BDIF) | escalonado | captacion_privado_pc | -12.657 | 120.847 |  | -0.249 | 6.671 | 4.166 | 0/4 | 0.684 |  | 0.969 |  |  | 766/500 |
| Municipio (trimestral, BDIF) | escalonado | credito_privado_pc | -4.441 | 30.399 |  | -0.145 | 2.790 | 1.783 | 0/4 | 0.363 |  | 0.948 |  |  | 766/500 |

## BDIF, panel corto 2022T4–2025T4

| panel | diseño | resultado | ATT | ee | sig | efecto % | MDE80 % | cota TOST % | previos sig. | Wald previa p | placebo 2019S2 | q BH | p Romano–Wolf | HonestDiD M̄=1 | n trat./ctrl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Municipio (trimestral, BDIF) | escalonado | cajeros_privado_pc | -0.200 | 0.102 | ** | -8.003 | 11.384 | 14.686 | 0/4 | 0.464 |  | 0.165 |  |  | 766/499 |
| Municipio (trimestral, BDIF) | escalonado | tpv_privado_pc | 1.922 | 2.045 |  | 3.471 | 10.346 | 9.545 | 0/4 | 0.684 |  | 0.559 |  |  | 766/499 |
| Municipio (trimestral, BDIF) | escalonado | transacciones_tpv_privado_pc | -214.015 | 519.421 |  | -5.412 | 36.797 | 27.016 | 0/4 | 0.730 |  | 0.837 |  |  | 766/499 |
| Municipio (trimestral, BDIF) | escalonado | captacion_privado_pc | -3.786 | 153.437 |  | -0.075 | 8.470 | 5.048 | 0/4 | 0.685 |  | 0.995 |  |  | 766/499 |
| Municipio (trimestral, BDIF) | escalonado | credito_privado_pc | -32.816 | 53.122 |  | -1.075 | 4.875 | 3.937 | 0/4 | 0.361 |  | 0.722 |  |  | 766/499 |

## Comparación de estimadores

| panel | diseno | variante | resultado | Callaway y Sant'Anna | Borusyak et al. | DiD 2x2 sin covariables | Sun y Abraham | TWFE estático |
|---|---|---|---|---|---|---|---|---|
| localidad | actualizaciones | principal | estab_abarrotes_pc | 0.780 |  | 1.188 |  |  |
| localidad | actualizaciones | principal | estab_consumo_pc | 2.952 |  | 6.926 |  |  |
| localidad | actualizaciones | principal | estab_restaurantes_pc | 0.806 |  | 1.996 |  |  |
| localidad | actualizaciones | principal | empleo_est_emprendimiento_pc | 33.786 |  | 39.057 |  |  |
| localidad | actualizaciones | principal | estab_emprendimiento_pc | 7.242 |  | 12.051 |  |  |
| localidad | actualizaciones | principal | micro_emprendimiento_pc | 6.940 |  | 11.362 |  |  |
| localidad | actualizaciones | principal | estab_consultorios_pc | 0.159 |  | 0.325 |  |  |
| localidad | actualizaciones | principal | estab_farmacia_pc | 0.256 |  | 0.605 |  |  |
| localidad | actualizaciones | principal | estab_salud_pc | 0.334 |  | 0.696 |  |  |
| municipio_trim | escalonado | principal | sucursales_bm_pc | -0.001 | -0.009 |  | 0.004 | -0.010 |
| municipio_trim | escalonado | principal | sucursales_eacp_pc | 0.008 | 0.021 |  | -0.001 | 0.019 |
| municipio_trim | escalonado | principal | sucursales_privado_pc | 0.007 | 0.012 |  | 0.003 | 0.009 |
| municipio_trim | escalonado | eacp | capt_ahorro_eacp_pc | 7.443 | -1.732 |  | -4.987 | -1.174 |
| municipio_trim | escalonado | eacp | capt_plazo_eacp_pc | -14.261 | 0.778 |  | 6.043 | -2.245 |
| municipio_trim | escalonado | eacp | capt_vista_eacp_pc | -63.519 | 138.251 |  | 203.835 | 71.001 |
| municipio_trim | escalonado | eacp | cred_consumo_eacp_pc | 16.869 | 12.746 |  | 19.501 | 7.561 |
| municipio_trim | escalonado | eacp | cred_vivienda_eacp_pc | -0.189 | -1.386 |  | -0.582 | -1.136 |
| municipio_trim | escalonado | eacp | tarjetas_debito_eacp_pc | -77.295 | 108.633 |  | 88.803 | 65.976 |
| municipio_trim | escalonado | inclusion_total | capt_ahorro_banca_pc | 2.404 | 16.402 |  | 10.403 | 12.597 |
| municipio_trim | escalonado | inclusion_total | capt_plazo_banca_pc | 6.719 | 0.514 |  | 8.815 | -3.140 |
| municipio_trim | escalonado | inclusion_total | cuentas_celular_total_pc | -179.814 | 496.210 |  | 261.334 | 370.191 |
| municipio_trim | escalonado | inclusion_total | tarjetas_debito_banca_pc | 3,313.567 | 3,922.563 |  | 3,803.091 | 2,496.068 |
| municipio_trim | escalonado | primera_etapa | capt_total_bd_pc | 1,267.912 | 1,274.362 |  | 1,262.268 | 965.988 |
| municipio_trim | escalonado | primera_etapa | sucursales_total_pc | 2.002 | 1.870 |  | 1.861 | 1.868 |
| municipio_trim | escalonado | primera_etapa | tarjetas_debito_bd_pc | 2,411.501 | 2,372.387 |  | 2,349.609 | 1,777.602 |
| municipio_trim | escalonado | imss | log_salario_diario | -0.019 | -0.021 |  | -0.021 | -0.013 |
| municipio_trim | escalonado | imss | ta_micro_pc | -1.099 | 5.648 |  | 1.619 | 4.664 |
| municipio_trim | escalonado | imss | ta_pc | -109.427 | 53.291 |  | 18.222 | 39.872 |
| municipio_trim | escalonado | imss | ta_pequena_pc | -6.570 | 8.991 |  | 2.442 | 7.031 |
| municipio_ce | escalonado | ce | log_produccion_bruta | 0.118 | -0.048 |  | 0.073 | -0.048 |
| municipio_ce | escalonado | ce | log_remuneraciones | 0.126 | 0.064 |  | 0.076 | 0.064 |
| municipio_ce | escalonado | ce | log_vacb | 0.231 | 0.001 |  | 0.138 | 0.001 |
| municipio_ce | escalonado | ce | personal_ocupado_pc | 0.177 | 10.912 |  | 8.223 | 10.915 |
| municipio_ce | escalonado | ce | ue_pc | -0.323 | -1.544 |  | 1.950 | -1.543 |
| municipio_trim | escalonado | remesas | remesas_usd_adulto | 9.008 | 25.522 |  | 11.760 | 20.428 |
| municipio_trim | escalonado | hasta_2025 | sucursales_bm_pc | -0.010 | -0.009 |  | 0.005 | -0.010 |
| municipio_trim | escalonado | hasta_2025 | sucursales_eacp_pc | 0.015 | 0.024 |  | 0.001 | 0.023 |
| municipio_trim | escalonado | hasta_2025 | sucursales_privado_pc | 0.004 | 0.015 |  | 0.006 | 0.013 |
| localidad | escalonado | secundaria | estab_abarrotes_pc | 0.036 | 0.066 |  | 0.029 | 0.065 |
| localidad | escalonado | secundaria | estab_consumo_pc | 0.151 | 0.223 |  | 0.084 | 0.218 |
| localidad | escalonado | secundaria | estab_restaurantes_pc | 0.038 | 0.027 |  | 0.011 | 0.028 |
| localidad | escalonado | secundaria | empleo_est_emprendimiento_pc | 3.096 | 1.267 |  | 2.539 | 0.950 |
| localidad | escalonado | secundaria | estab_emprendimiento_pc | 0.543 | 0.572 |  | 0.416 | 0.574 |
| localidad | escalonado | secundaria | micro_emprendimiento_pc | 0.528 | 0.548 |  | 0.372 | 0.553 |
| localidad | escalonado | secundaria | estab_consultorios_pc | 0.003 | 0.005 |  | 0.000 | 0.005 |
| localidad | escalonado | secundaria | estab_farmacia_pc | 0.010 | 0.036 |  | 0.015 | 0.037 |
| localidad | escalonado | secundaria | estab_salud_pc | 0.010 | 0.028 |  | 0.009 | 0.028 |
| municipio | actualizaciones | secundaria | estab_abarrotes_pc | -0.589 |  | 6.127 |  |  |
| municipio | actualizaciones | secundaria | estab_consumo_pc | 2.793 |  | 12.781 |  |  |
| municipio | actualizaciones | secundaria | estab_restaurantes_pc | 1.827 |  | 1.127 |  |  |
| municipio | actualizaciones | secundaria | empleo_est_emprendimiento_pc | -0.914 |  | 27.334 |  |  |
| municipio | actualizaciones | secundaria | estab_emprendimiento_pc | -0.012 |  | 15.537 |  |  |
| municipio | actualizaciones | secundaria | micro_emprendimiento_pc | -1.845 |  | 12.556 |  |  |
| municipio | actualizaciones | secundaria | estab_farmacia_pc | 0.877 |  | 0.960 |  |  |
| municipio | actualizaciones | secundaria | estab_salud_pc | 1.118 |  | 0.695 |  |  |
| municipio | escalonado | secundaria | estab_abarrotes_pc | 0.010 | 0.142 |  | 0.139 | 0.052 |
| municipio | escalonado | secundaria | estab_consumo_pc | 0.157 | 0.715 |  | 0.685 | 0.437 |
| municipio | escalonado | secundaria | estab_restaurantes_pc | 0.015 | -0.053 |  | 0.019 | -0.052 |
| municipio | escalonado | secundaria | empleo_est_emprendimiento_pc | 16.067 | -9.823 |  | -5.280 | -7.784 |
| municipio | escalonado | secundaria | estab_emprendimiento_pc | 0.713 | 1.743 |  | 1.380 | 1.218 |
| municipio | escalonado | secundaria | micro_emprendimiento_pc | 0.854 | 1.517 |  | 1.233 | 1.071 |
| municipio | escalonado | secundaria | estab_farmacia_pc | 0.077 | 0.107 |  | 0.093 | 0.068 |
| municipio | escalonado | secundaria | estab_salud_pc | 0.045 | -0.007 |  | 0.034 | -0.021 |
| municipio_trim | escalonado | secundaria | corresponsales_total_pc | -0.015 | 0.059 |  | 0.032 | 0.028 |
| localidad | actualizaciones | derrame | estab_consumo_pc | 0.083 |  | 0.243 |  |  |
| localidad | actualizaciones | derrame | estab_emprendimiento_pc | 0.402 |  | 0.730 |  |  |
| localidad | actualizaciones | derrame | estab_salud_pc | 0.019 |  | 0.034 |  |  |
| municipio_trim | escalonado | panel_corto | cajeros_privado_pc | -0.072 | -0.023 |  | -0.051 | 0.028 |
| municipio_trim | escalonado | panel_corto | tpv_privado_pc | -0.502 | 8.416 |  | 6.939 | 18.226 |
| municipio_trim | escalonado | panel_corto | transacciones_tpv_privado_pc | -85.350 | 574.113 |  | 525.963 | 477.388 |
| municipio_trim | escalonado | panel_corto | captacion_privado_pc | -12.657 | 343.754 |  | 314.750 | 254.224 |
| municipio_trim | escalonado | panel_corto | credito_privado_pc | -4.441 | 82.541 |  | 73.222 | 61.926 |
| municipio_trim | escalonado | panel_corto_2025 | cajeros_privado_pc | -0.200 | -0.019 |  | -0.051 | 0.044 |
| municipio_trim | escalonado | panel_corto_2025 | tpv_privado_pc | 1.922 | 12.316 |  | 8.027 | 23.121 |
| municipio_trim | escalonado | panel_corto_2025 | transacciones_tpv_privado_pc | -214.015 | 969.125 |  | 891.794 | 845.624 |
| municipio_trim | escalonado | panel_corto_2025 | captacion_privado_pc | -3.786 | 421.549 |  | 375.570 | 323.363 |
| municipio_trim | escalonado | panel_corto_2025 | credito_privado_pc | -32.816 | 217.900 |  | 206.860 | 168.098 |

## Contraste de diseños

| diseno | estimador | valor | ee | pre_sig | pre_n | pre_wald_p | resultado |
|---|---|---|---|---|---|---|---|
| B1 panel completo | Callaway y Sant'Anna | 1.531 | 0.290 | 1.000 | 15.000 | 0.023 | estab_consumo_pc |
| B2 panel completo + FE semestre × decil | TWFE estático | 4.147 | 0.240 |  |  |  | estab_consumo_pc |
| B2 panel completo + FE semestre × decil | Sun y Abraham | 2.426 | 0.170 |  |  |  | estab_consumo_pc |
| B2 panel completo + FE semestre × decil | Borusyak et al. | 4.414 | 0.233 |  |  |  | estab_consumo_pc |
| B1 panel completo | Callaway y Sant'Anna | 3.637 | 0.582 | 0.000 | 15.000 | 0.043 | estab_emprendimiento_pc |
| B2 panel completo + FE semestre × decil | TWFE estático | 7.456 | 0.405 |  |  |  | estab_emprendimiento_pc |
| B2 panel completo + FE semestre × decil | Sun y Abraham | 4.451 | 0.275 |  |  |  | estab_emprendimiento_pc |
| B2 panel completo + FE semestre × decil | Borusyak et al. | 7.954 | 0.398 |  |  |  | estab_emprendimiento_pc |
| B1 panel completo | Callaway y Sant'Anna | 0.154 | 0.031 | 2.000 | 15.000 | 0.037 | estab_salud_pc |
| B2 panel completo + FE semestre × decil | TWFE estático | 0.447 | 0.029 |  |  |  | estab_salud_pc |
| B2 panel completo + FE semestre × decil | Sun y Abraham | 0.256 | 0.022 |  |  |  | estab_salud_pc |
| B2 panel completo + FE semestre × decil | Borusyak et al. | 0.470 | 0.027 |  |  |  | estab_salud_pc |

Descomposición de Goodman-Bacon del TWFE (ventana escalonada):

| type | peso | estimacion | etiqueta | resultado | twfe |
|---|---|---|---|---|---|
| Treated vs Untreated | 0.988 | 0.221 | localidad_esc_estab_consumo_pc | estab_consumo_pc | 0.218 |
| Earlier vs Later Treated | 0.009 | 0.041 | localidad_esc_estab_consumo_pc | estab_consumo_pc | 0.218 |
| Later vs Earlier Treated | 0.003 | -0.086 | localidad_esc_estab_consumo_pc | estab_consumo_pc | 0.218 |
| Treated vs Untreated | 0.988 | 0.580 | localidad_esc_estab_emprendimiento_pc | estab_emprendimiento_pc | 0.574 |
| Earlier vs Later Treated | 0.009 | 0.161 | localidad_esc_estab_emprendimiento_pc | estab_emprendimiento_pc | 0.574 |
| Later vs Earlier Treated | 0.003 | -0.112 | localidad_esc_estab_emprendimiento_pc | estab_emprendimiento_pc | 0.574 |
| Treated vs Untreated | 0.988 | 0.029 | localidad_esc_estab_salud_pc | estab_salud_pc | 0.028 |
| Earlier vs Later Treated | 0.009 | -0.017 | localidad_esc_estab_salud_pc | estab_salud_pc | 0.028 |
| Later vs Earlier Treated | 0.003 | -0.008 | localidad_esc_estab_salud_pc | estab_salud_pc | 0.028 |

## DiD apilado (Wing, Freedman y Hollingsworth 2024)

Municipio trimestral 2019T1–2025T4; una pila por cohorte con ventana de evento e ∈ [−8, 7] y controles limpios ponderados; efectos fijos unidad × pila y evento; sin covariables; ee agrupado por municipio. *att* = promedio de δ_0…δ_7; la pre-prueba es la Wald de δ_−8…δ_−2. *cs_* es la estimación de Callaway y Sant'Anna de referencia.

| resultado | controles | pilas | tratadas | att | ee | efecto_pct | cota_equivalencia_pct | pre_sig | pre_n | pre_wald_p | cs_att | cs_ee | cs_efecto_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sucursales_privado_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 0.007 | 0.011 | 0.785 | 2.692 | 0 | 7 | 0.721 | 0.004 | 0.014 | 0.453 |
| sucursales_privado_pc | solo nunca tratados | 9 | 1457 | 0.007 | 0.011 | 0.723 | 2.703 | 0 | 7 | 0.647 | 0.004 | 0.014 | 0.453 |
| sucursales_bm_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 0.003 | 0.003 | 0.707 | 1.988 | 0 | 7 | 0.723 | -0.010 | 0.009 | -2.572 |
| sucursales_bm_pc | solo nunca tratados | 9 | 1457 | 0.003 | 0.003 | 0.723 | 2.050 | 0 | 7 | 0.661 | -0.010 | 0.009 | -2.572 |
| sucursales_eacp_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 0.004 | 0.010 | 0.844 | 4.095 | 0 | 7 | 0.939 | 0.015 | 0.013 | 2.792 |
| sucursales_eacp_pc | solo nunca tratados | 9 | 1457 | 0.004 | 0.011 | 0.723 | 4.095 | 0 | 7 | 0.913 | 0.015 | 0.013 | 2.792 |
| sucursales_total_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 2.000 | 0.083 | 214.747 | 229.344 | 0 | 7 | 0.716 | 2.002 | 0.083 | 214.985 |
| sucursales_total_pc | solo nunca tratados | 9 | 1457 | 1.999 | 0.083 | 214.685 | 229.292 | 0 | 7 | 0.641 | 2.002 | 0.083 | 214.985 |
| capt_ahorro_eacp_pc | limpios (nunca + aún no tratados) | 9 | 1457 | -3.487 | 15.789 | -0.227 | 1.914 | 0 | 7 | 0.883 | 7.443 | 19.276 | 0.484 |
| capt_ahorro_eacp_pc | solo nunca tratados | 9 | 1457 | -3.840 | 15.863 | -0.250 | 1.945 | 0 | 7 | 0.886 | 7.443 | 19.276 | 0.484 |
| cred_consumo_eacp_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 15.326 | 3.905 | 3.868 | 5.489 | 1 | 7 | 0.000 | 16.869 | 5.795 | 4.258 |
| cred_consumo_eacp_pc | solo nunca tratados | 9 | 1457 | 15.361 | 4.089 | 3.877 | 5.575 | 0 | 7 | 0.000 | 16.869 | 5.795 | 4.258 |
| ta_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 10.590 | 8.063 | 1.717 | 3.867 | 2 | 7 | 0.038 | -109.427 | 91.125 | -17.740 |
| ta_pc | solo nunca tratados | 9 | 1457 | 11.961 | 8.060 | 1.939 | 4.088 | 2 | 7 | 0.048 | -109.427 | 91.125 | -17.740 |
| ta_micro_pc | limpios (nunca + aún no tratados) | 9 | 1457 | 1.161 | 0.946 | 2.089 | 4.890 | 3 | 7 | 0.297 | -1.099 | 2.476 | -1.978 |
| ta_micro_pc | solo nunca tratados | 9 | 1457 | 1.295 | 0.981 | 2.331 | 5.235 | 3 | 7 | 0.213 | -1.099 | 2.476 | -1.978 |
| log_salario_diario | limpios (nunca + aún no tratados) | 9 | 1226 | -0.014 | 0.006 | -1.441 | 2.368 | 0 | 7 | 0.226 | -0.019 | 0.010 | -1.852 |
| log_salario_diario | solo nunca tratados | 9 | 1226 | -0.015 | 0.006 | -1.507 | 2.472 | 0 | 7 | 0.234 | -0.019 | 0.010 | -1.852 |

## Decaimiento espacial (DENUE, entre actualizaciones)

ATT(17, 18) por banda de distancia a la sucursal más cercana, cada banda contra los mismos controles a ≥10 km; la sucursal propia es la especificación principal. Los contrastes están en % de la media previa de cada banda, con covarianza agrupada por municipio.

| resultado | banda | tratadas | att | ee | media_base | efecto_pct | pre_sig | pre_n | pre_wald_p | placebo | placebo_ee |
|---|---|---|---|---|---|---|---|---|---|---|---|
| estab_consumo_pc | sucursal propia | 1,106.000 | 2.952 | 0.559 | 35.884 | 8.226 | 2.000 | 2.000 | 0.000 | 1.498 | 0.471 |
| estab_consumo_pc | 0–2 km | 2,430.000 | 0.477 | 0.129 | 6.673 | 7.143 | 1.000 | 2.000 | 0.000 | 0.136 | 0.288 |
| estab_consumo_pc | 2–5 km | 7,138.000 | 0.105 | 0.067 | 2.545 | 4.128 | 2.000 | 2.000 | 0.003 | 0.283 | 0.141 |
| estab_consumo_pc | 5–10 km | 9,930.000 | -0.019 | 0.057 | 1.655 | -1.162 | 0.000 | 2.000 | 0.282 | 0.044 | 0.045 |
| estab_emprendimiento_pc | sucursal propia | 1,106.000 | 7.242 | 1.104 | 69.634 | 10.400 | 0.000 | 2.000 | 0.057 | 1.714 | 1.247 |
| estab_emprendimiento_pc | 0–2 km | 2,430.000 | 1.507 | 0.270 | 12.893 | 11.691 | 1.000 | 2.000 | 0.030 | 0.406 | 0.398 |
| estab_emprendimiento_pc | 2–5 km | 7,138.000 | 0.490 | 0.166 | 5.475 | 8.946 | 2.000 | 2.000 | 0.001 | 0.581 | 0.261 |
| estab_emprendimiento_pc | 5–10 km | 9,930.000 | 0.036 | 0.134 | 4.000 | 0.890 | 0.000 | 2.000 | 0.392 | -0.043 | 0.237 |
| estab_salud_pc | sucursal propia | 1,106.000 | 0.334 | 0.060 | 3.482 | 9.587 | 1.000 | 2.000 | 0.036 | 0.174 | 0.072 |
| estab_salud_pc | 0–2 km | 2,430.000 | 0.049 | 0.016 | 0.620 | 7.832 | 1.000 | 2.000 | 0.000 | 0.043 | 0.016 |
| estab_salud_pc | 2–5 km | 7,138.000 | 0.032 | 0.023 | 0.195 | 16.276 | 0.000 | 2.000 | 0.522 | 0.009 | 0.008 |
| estab_salud_pc | 5–10 km | 9,930.000 | 0.002 | 0.006 | 0.156 | 1.432 | 0.000 | 2.000 | 0.759 | 0.004 | 0.007 |

| resultado | contraste | dif_pct | ee_dif_pct | p_dif |
|---|---|---|---|---|
| estab_consumo_pc | sucursal propia − 0–2 km | 1.083 | 2.026 | 0.593 |
| estab_consumo_pc | sucursal propia − 5–10 km | 9.388 | 3.548 | 0.008 |
| estab_consumo_pc | 0–2 km − 5–10 km | 8.305 | 3.271 | 0.011 |
| estab_emprendimiento_pc | sucursal propia − 0–2 km | -1.291 | 2.057 | 0.530 |
| estab_emprendimiento_pc | sucursal propia − 5–10 km | 9.509 | 3.438 | 0.006 |
| estab_emprendimiento_pc | 0–2 km − 5–10 km | 10.800 | 3.028 | 0.000 |
| estab_salud_pc | sucursal propia − 0–2 km | 1.755 | 2.621 | 0.503 |
| estab_salud_pc | sucursal propia − 5–10 km | 8.155 | 4.158 | 0.050 |
| estab_salud_pc | 0–2 km − 5–10 km | 6.400 | 4.084 | 0.117 |

## Régimen censal (exploratorio, no preregistrado)

Especificación principal del DENUE estimada dentro de cada régimen de levantamiento de los Censos Económicos: recorrido total (cabecera o 2,500+ habitantes) y muestra rural. Las diferencias están en % de la media previa de cada grupo.

| resultado | regimen | banda | contraste | tratadas | controles | att | ee | efecto_pct | pre_wald_p | placebo | placebo_ee | dif_pct | ee_dif_pct | p_dif |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| estab_consumo_pc | recorrido_total | sucursal propia | nan | 903.000 | 478.000 | 3.428 | 0.715 | 7.910 | 0.032 | 1.277 | 0.573 |  |  |  |
| estab_consumo_pc | recorrido_total | 0–2 km | nan | 341.000 | 478.000 | 4.180 | 0.786 | 9.713 | 0.003 | 2.064 | 0.642 |  |  |  |
| estab_consumo_pc | recorrido_total | 2–5 km | nan | 433.000 | 478.000 | 1.728 | 0.746 | 5.807 | 0.000 | 1.701 | 0.400 |  |  |  |
| estab_consumo_pc | recorrido_total | 5–10 km | nan | 400.000 | 478.000 | 0.121 | 0.818 | 0.374 | 0.406 | 0.842 | 0.659 |  |  |  |
| estab_consumo_pc | recorrido_total | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | -1.803 | 1.753 | 0.304 |
| estab_consumo_pc | recorrido_total | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 7.537 | 2.559 | 0.003 |
| estab_consumo_pc | recorrido_total | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 9.340 | 2.603 | 0.000 |
| estab_consumo_pc | muestra_rural | sucursal propia | nan | 203.000 | 21,241.000 | 0.295 | 0.308 | 10.888 | 0.114 | -0.056 | 0.290 |  |  |  |
| estab_consumo_pc | muestra_rural | 0–2 km | nan | 2,089.000 | 21,241.000 | 0.032 | 0.062 | 4.340 | 0.001 | -0.172 | 0.309 |  |  |  |
| estab_consumo_pc | muestra_rural | 2–5 km | nan | 6,705.000 | 21,241.000 | -0.009 | 0.050 | -1.134 | 0.013 | 0.209 | 0.145 |  |  |  |
| estab_consumo_pc | muestra_rural | 5–10 km | nan | 9,530.000 | 21,241.000 | -0.015 | 0.045 | -4.201 | 0.837 | -0.002 | 0.033 |  |  |  |
| estab_consumo_pc | muestra_rural | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | 6.549 | 13.299 | 0.622 |
| estab_consumo_pc | muestra_rural | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 15.089 | 14.704 | 0.305 |
| estab_consumo_pc | muestra_rural | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 8.540 | 12.579 | 0.497 |
| estab_consumo_pc | entre regímenes | nan | sucursal propia: recorrido total − muestra rural |  |  |  |  |  |  |  |  | -2.978 | 11.464 | 0.795 |
| estab_emprendimiento_pc | recorrido_total | sucursal propia | nan | 903.000 | 478.000 | 8.238 | 1.569 | 9.789 | 0.706 | 0.111 | 1.794 |  |  |  |
| estab_emprendimiento_pc | recorrido_total | 0–2 km | nan | 341.000 | 478.000 | 7.048 | 1.363 | 8.968 | 0.050 | 2.124 | 1.238 |  |  |  |
| estab_emprendimiento_pc | recorrido_total | 2–5 km | nan | 433.000 | 478.000 | 3.273 | 1.281 | 5.575 | 0.001 | 3.150 | 0.867 |  |  |  |
| estab_emprendimiento_pc | recorrido_total | 5–10 km | nan | 400.000 | 478.000 | 0.574 | 1.421 | 0.810 | 0.470 | 1.590 | 1.311 |  |  |  |
| estab_emprendimiento_pc | recorrido_total | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | 0.820 | 1.661 | 0.621 |
| estab_emprendimiento_pc | recorrido_total | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 8.979 | 2.205 | 0.000 |
| estab_emprendimiento_pc | recorrido_total | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 8.158 | 2.082 | 0.000 |
| estab_emprendimiento_pc | muestra_rural | sucursal propia | nan | 203.000 | 21,241.000 | 1.707 | 0.499 | 33.855 | 0.048 | -0.220 | 0.608 |  |  |  |
| estab_emprendimiento_pc | muestra_rural | 0–2 km | nan | 2,089.000 | 21,241.000 | 0.375 | 0.158 | 17.272 | 0.075 | -0.047 | 0.375 |  |  |  |
| estab_emprendimiento_pc | muestra_rural | 2–5 km | nan | 6,705.000 | 21,241.000 | 0.169 | 0.146 | 8.303 | 0.009 | 0.422 | 0.266 |  |  |  |
| estab_emprendimiento_pc | muestra_rural | 5–10 km | nan | 9,530.000 | 21,241.000 | -0.069 | 0.114 | -5.756 | 0.666 | -0.176 | 0.235 |  |  |  |
| estab_emprendimiento_pc | muestra_rural | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | 16.583 | 10.864 | 0.127 |
| estab_emprendimiento_pc | muestra_rural | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 39.611 | 11.742 | 0.001 |
| estab_emprendimiento_pc | muestra_rural | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 23.027 | 9.760 | 0.018 |
| estab_emprendimiento_pc | entre regímenes | nan | sucursal propia: recorrido total − muestra rural |  |  |  |  |  |  |  |  | -24.066 | 10.046 | 0.017 |
| estab_salud_pc | recorrido_total | sucursal propia | nan | 903.000 | 478.000 | 0.430 | 0.073 | 10.179 | 0.045 | 0.196 | 0.084 |  |  |  |
| estab_salud_pc | recorrido_total | 0–2 km | nan | 341.000 | 478.000 | 0.346 | 0.094 | 8.310 | 0.003 | 0.300 | 0.088 |  |  |  |
| estab_salud_pc | recorrido_total | 2–5 km | nan | 433.000 | 478.000 | 0.152 | 0.078 | 5.972 | 0.184 | 0.070 | 0.076 |  |  |  |
| estab_salud_pc | recorrido_total | 5–10 km | nan | 400.000 | 478.000 | 0.069 | 0.111 | 2.116 | 0.648 | 0.109 | 0.123 |  |  |  |
| estab_salud_pc | recorrido_total | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | 1.869 | 2.284 | 0.413 |
| estab_salud_pc | recorrido_total | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 8.062 | 3.384 | 0.017 |
| estab_salud_pc | recorrido_total | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 6.193 | 3.473 | 0.075 |
| estab_salud_pc | muestra_rural | sucursal propia | nan | 203.000 | 21,241.000 | 0.056 | 0.070 | 28.268 | 0.271 | 0.045 | 0.029 |  |  |  |
| estab_salud_pc | muestra_rural | 0–2 km | nan | 2,089.000 | 21,241.000 | 0.010 | 0.008 | 25.225 | 0.271 | -0.004 | 0.010 |  |  |  |
| estab_salud_pc | muestra_rural | 2–5 km | nan | 6,705.000 | 21,241.000 | 0.024 | 0.024 | 57.081 | 0.738 | 0.002 | 0.006 |  |  |  |
| estab_salud_pc | muestra_rural | 5–10 km | nan | 9,530.000 | 21,241.000 | -0.002 | 0.005 | -8.579 | 0.734 | -0.001 | 0.005 |  |  |  |
| estab_salud_pc | muestra_rural | nan | sucursal propia − 0–2 km |  |  |  |  |  |  |  |  | 3.043 | 40.161 | 0.940 |
| estab_salud_pc | muestra_rural | nan | sucursal propia − 5–10 km |  |  |  |  |  |  |  |  | 36.848 | 37.879 | 0.331 |
| estab_salud_pc | muestra_rural | nan | 0–2 km − 5–10 km |  |  |  |  |  |  |  |  | 33.805 | 23.875 | 0.157 |
| estab_salud_pc | entre regímenes | nan | sucursal propia: recorrido total − muestra rural |  |  |  |  |  |  |  |  | -18.090 | 35.503 | 0.610 |

## Intensidad del tratamiento municipal (descriptivo)

Sucursales del Banco del Bienestar (netas de Banjército) por municipio que abrió en la ventana, al cierre de 2024T4.

| sucursales | municipios | pct | por_10mil_p10 | por_10mil_mediana | por_10mil_p90 | periodo |
|---|---|---|---|---|---|---|
| 0 (cerró) | 2 | 0.14 | 0.00 | 0.00 | 0.00 | 2024Q4 |
| 1 | 1263 | 85.98 | 0.33 | 1.17 | 4.36 | 2024Q4 |
| 2 | 162 | 11.03 | 0.30 | 0.94 | 2.21 | 2024Q4 |
| 3 o más | 42 | 2.86 | 0.25 | 0.69 | 1.53 | 2024Q4 |

## Robustez (con la auditoría de pre-tendencias de cada variante)

| panel | diseno | resultado | variante | tratadas | controles | att | ee | pre_sig | pre_n | pre_wald_p |
|---|---|---|---|---|---|---|---|---|---|---|
| localidad | actualizaciones | estab_consumo_pc | base (≥10 km, DR, cluster municipal) | 1106 | 21719 | 2.952 | 0.559 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | controles: dist5 | 1106 | 43896 | 3.855 | 1.054 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | controles: dist20 | 1106 | 6214 | 3.266 | 1.224 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | controles: municipal | 1106 | 3044 | 2.140 | 0.450 | 1 | 2 | 0.088 |
| localidad | actualizaciones | estab_consumo_pc | controles: todos | 1106 | 66669 | 1.223 | 0.381 | 1 | 2 | 0.015 |
| localidad | actualizaciones | estab_consumo_pc | controles: solo_sucursal | 313 | 174 | 1.705 | 1.131 | 0 | 2 | 0.117 |
| localidad | actualizaciones | estab_consumo_pc | sin nivel previo del resultado | 1106 | 21719 | 4.160 | 0.488 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | sin covariables | 1106 | 21719 | 6.926 | 0.305 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | piso simétrico de 1,000 habitantes | 835 | 1677 | 3.594 | 0.828 | 1 | 2 | 0.014 |
| localidad | actualizaciones | estab_consumo_pc | post en 2025S1 | 1106 | 21719 | 3.407 | 0.650 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | incluye fechas ambiguas y sospechosas | 1312 | 21719 | 3.143 | 0.571 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | cluster por estado | 1106 | 21719 | 2.952 | 0.565 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_consumo_pc | muestra emparejada (matching) | 550 | 695 | 2.840 | 0.646 | 1 | 2 | 0.012 |
| localidad | actualizaciones | estab_emprendimiento_pc | base (≥10 km, DR, cluster municipal) | 1106 | 21719 | 7.242 | 1.104 | 0 | 2 | 0.057 |
| localidad | actualizaciones | estab_emprendimiento_pc | controles: dist5 | 1106 | 43896 | 6.948 | 1.366 | 0 | 2 | 0.061 |
| localidad | actualizaciones | estab_emprendimiento_pc | controles: dist20 | 1106 | 6214 | 7.266 | 1.943 | 0 | 2 | 0.679 |
| localidad | actualizaciones | estab_emprendimiento_pc | controles: municipal | 1106 | 3044 | 3.638 | 0.813 | 1 | 2 | 0.061 |
| localidad | actualizaciones | estab_emprendimiento_pc | controles: todos | 1106 | 66669 | 3.411 | 0.642 | 1 | 2 | 0.015 |
| localidad | actualizaciones | estab_emprendimiento_pc | controles: solo_sucursal | 313 | 174 | 3.100 | 1.547 | 1 | 2 | 0.007 |
| localidad | actualizaciones | estab_emprendimiento_pc | sin nivel previo del resultado | 1106 | 21719 | 7.409 | 0.765 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_emprendimiento_pc | sin covariables | 1106 | 21719 | 12.051 | 0.510 | 2 | 2 | 0.000 |
| localidad | actualizaciones | estab_emprendimiento_pc | piso simétrico de 1,000 habitantes | 835 | 1677 | 7.956 | 1.668 | 0 | 2 | 0.409 |
| localidad | actualizaciones | estab_emprendimiento_pc | post en 2025S1 | 1106 | 21719 | 7.016 | 1.287 | 0 | 2 | 0.057 |
| localidad | actualizaciones | estab_emprendimiento_pc | incluye fechas ambiguas y sospechosas | 1312 | 21719 | 7.053 | 1.002 | 0 | 2 | 0.045 |
| localidad | actualizaciones | estab_emprendimiento_pc | cluster por estado | 1106 | 21719 | 7.242 | 1.485 | 1 | 2 | 0.039 |
| localidad | actualizaciones | estab_emprendimiento_pc | muestra emparejada (matching) | 562 | 724 | 5.735 | 1.222 | 0 | 2 | 0.288 |
| localidad | actualizaciones | estab_salud_pc | base (≥10 km, DR, cluster municipal) | 1106 | 21719 | 0.334 | 0.060 | 1 | 2 | 0.036 |
| localidad | actualizaciones | estab_salud_pc | controles: dist5 | 1106 | 43896 | 0.386 | 0.103 | 1 | 2 | 0.001 |
| localidad | actualizaciones | estab_salud_pc | controles: dist20 | 1106 | 6214 | 0.254 | 0.074 | 1 | 2 | 0.029 |
| localidad | actualizaciones | estab_salud_pc | controles: municipal | 1106 | 3044 | 0.206 | 0.058 | 0 | 2 | 0.156 |
| localidad | actualizaciones | estab_salud_pc | controles: todos | 1106 | 66669 | 0.144 | 0.045 | 0 | 2 | 0.441 |
| localidad | actualizaciones | estab_salud_pc | controles: solo_sucursal | 313 | 174 | 0.141 | 0.104 | 0 | 2 | 0.280 |
| localidad | actualizaciones | estab_salud_pc | sin nivel previo del resultado | 1106 | 21719 | 0.468 | 0.051 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_salud_pc | sin covariables | 1106 | 21719 | 0.696 | 0.039 | 1 | 2 | 0.000 |
| localidad | actualizaciones | estab_salud_pc | piso simétrico de 1,000 habitantes | 835 | 1677 | 0.409 | 0.083 | 1 | 2 | 0.070 |
| localidad | actualizaciones | estab_salud_pc | post en 2025S1 | 1106 | 21719 | 0.344 | 0.072 | 1 | 2 | 0.036 |
| localidad | actualizaciones | estab_salud_pc | incluye fechas ambiguas y sospechosas | 1312 | 21719 | 0.360 | 0.057 | 1 | 2 | 0.014 |
| localidad | actualizaciones | estab_salud_pc | cluster por estado | 1106 | 21719 | 0.334 | 0.075 | 1 | 2 | 0.020 |
| localidad | actualizaciones | estab_salud_pc | muestra emparejada (matching) | 472 | 685 | 0.237 | 0.088 | 0 | 2 | 0.754 |
| localidad | escalonado | estab_emprendimiento_pc | base (aún no tratados, δ=0, DR) | 1105 | 21719 | 0.543 | 0.179 | 1 | 8 | 0.020 |
| localidad | escalonado | estab_emprendimiento_pc | anticipación δ=1 | 1105 | 21719 | 0.646 | 0.264 | 1 | 8 | 0.022 |
| localidad | escalonado | estab_emprendimiento_pc | solo nunca tratados como control | 1105 | 21719 | 0.628 | 0.235 | 0 | 8 | 0.632 |
| localidad | escalonado | estab_emprendimiento_pc | sin covariables | 1105 | 21719 | 0.419 | 0.055 | 3 | 8 | 0.000 |
| localidad | escalonado | estab_emprendimiento_pc | cohortes de 30 unidades o más | 1105 | 21719 | 0.543 | 0.179 | 1 | 8 | 0.020 |
| localidad | escalonado | estab_emprendimiento_pc | incluye fechas ambiguas y sospechosas | 1308 | 21719 | 0.511 | 0.183 | 1 | 8 | 0.008 |
| localidad | escalonado | estab_emprendimiento_pc | cluster por estado | 1105 | 21719 | 0.543 | 0.183 | 1 | 8 | 0.000 |
| localidad | escalonado | estab_emprendimiento_pc | controles: todos | 1105 | 66669 | 0.343 | 0.065 | 1 | 8 | 0.007 |
| localidad | escalonado | estab_emprendimiento_pc | controles: solo con sucursal | 1105 | 0 | 0.526 | 0.121 | 0 | 7 | 0.318 |
| municipio_ce | escalonado | personal_ocupado_pc | base (aún no tratados, δ=0, DR) | 1252 | 499 | 0.177 | 7.593 | 0 | 3 | 0.336 |
| municipio_ce | escalonado | personal_ocupado_pc | anticipación δ=1 | 1252 | 499 | 5.298 | 9.854 | 0 | 3 | 0.336 |
| municipio_ce | escalonado | personal_ocupado_pc | solo nunca tratados como control | 1252 | 499 | 0.177 | 7.593 | 0 | 3 | 0.336 |
| municipio_ce | escalonado | personal_ocupado_pc | sin covariables | 1252 | 499 | 8.070 | 3.009 | 0 | 3 | 0.594 |
| municipio_ce | escalonado | personal_ocupado_pc | cohortes de 30 unidades o más | 1252 | 499 | 0.177 | 7.593 | 0 | 3 | 0.336 |
| municipio_ce | escalonado | personal_ocupado_pc | incluye fechas ambiguas y sospechosas | 1260 | 499 | 0.244 | 7.617 | 0 | 3 | 0.385 |
| municipio_ce | escalonado | personal_ocupado_pc | cluster por estado | 1252 | 499 | 0.177 | 8.409 | 0 | 3 | 0.142 |
| municipio_ce | escalonado | ue_pc | base (aún no tratados, δ=0, DR) | 1252 | 499 | -0.323 | 0.686 | 0 | 3 | 0.210 |
| municipio_ce | escalonado | ue_pc | anticipación δ=1 | 1252 | 499 | -1.765 | 1.212 | 0 | 3 | 0.210 |
| municipio_ce | escalonado | ue_pc | solo nunca tratados como control | 1252 | 499 | -0.323 | 0.686 | 0 | 3 | 0.210 |
| municipio_ce | escalonado | ue_pc | sin covariables | 1252 | 499 | 1.960 | 0.733 | 3 | 3 | 0.000 |
| municipio_ce | escalonado | ue_pc | cohortes de 30 unidades o más | 1252 | 499 | -0.323 | 0.686 | 0 | 3 | 0.210 |
| municipio_ce | escalonado | ue_pc | incluye fechas ambiguas y sospechosas | 1260 | 499 | -0.307 | 0.685 | 0 | 3 | 0.221 |
| municipio_ce | escalonado | ue_pc | cluster por estado | 1252 | 499 | -0.323 | 0.760 | 0 | 3 | 0.431 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | 7.443 | 19.276 | 1 | 19 | 0.510 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | anticipación δ=1 | 1457 | 499 | 11.375 | 20.265 | 1 | 19 | 0.552 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | solo nunca tratados como control | 1457 | 499 | 7.353 | 19.805 | 0 | 19 | 0.369 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | sin covariables | 1457 | 499 | -3.167 | 17.503 | 2 | 19 | 0.502 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | 7.443 | 19.276 | 1 | 19 | 0.510 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | 7.601 | 19.247 | 1 | 19 | 0.508 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | cluster por estado | 1457 | 499 | 7.443 | 22.658 | 0 | 19 | 0.000 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | 7.256 | 19.280 | 1 | 19 | 0.513 |
| municipio_trim | escalonado | capt_ahorro_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | 7.443 | 19.276 | 1 | 31 | 0.338 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -14.261 | 11.088 | 1 | 19 | 0.206 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | anticipación δ=1 | 1457 | 499 | -10.915 | 12.266 | 1 | 19 | 0.279 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | solo nunca tratados como control | 1457 | 499 | -12.706 | 11.589 | 1 | 19 | 0.024 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | sin covariables | 1457 | 499 | 2.705 | 6.766 | 2 | 19 | 0.022 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | -14.261 | 11.088 | 1 | 19 | 0.206 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -14.361 | 11.110 | 1 | 19 | 0.216 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | cluster por estado | 1457 | 499 | -14.261 | 8.616 | 0 | 19 | 0.000 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | -14.255 | 11.086 | 1 | 19 | 0.206 |
| municipio_trim | escalonado | capt_plazo_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | -14.261 | 11.088 | 2 | 31 | 0.352 |
| municipio_trim | escalonado | capt_vista_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -63.519 | 72.027 | 3 | 19 | 0.191 |
| municipio_trim | escalonado | capt_vista_eacp_pc | anticipación δ=1 | 1457 | 499 | -72.600 | 77.252 | 2 | 19 | 0.278 |
| municipio_trim | escalonado | capt_vista_eacp_pc | solo nunca tratados como control | 1457 | 499 | -57.678 | 75.693 | 2 | 19 | 0.070 |
| municipio_trim | escalonado | capt_vista_eacp_pc | sin covariables | 1457 | 499 | 176.511 | 25.047 | 4 | 19 | 0.001 |
| municipio_trim | escalonado | capt_vista_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | -63.519 | 72.027 | 3 | 19 | 0.191 |
| municipio_trim | escalonado | capt_vista_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -61.533 | 72.267 | 2 | 19 | 0.197 |
| municipio_trim | escalonado | capt_vista_eacp_pc | cluster por estado | 1457 | 499 | -63.519 | 74.611 | 1 | 19 | 0.000 |
| municipio_trim | escalonado | capt_vista_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | -63.553 | 71.990 | 3 | 19 | 0.185 |
| municipio_trim | escalonado | capt_vista_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | -63.519 | 72.027 | 4 | 31 | 0.360 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | 16.869 | 5.795 | 3 | 19 | 0.176 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | anticipación δ=1 | 1457 | 499 | 21.775 | 6.464 | 3 | 19 | 0.168 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | solo nunca tratados como control | 1457 | 499 | 19.411 | 6.047 | 2 | 19 | 0.004 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | sin covariables | 1457 | 499 | 17.965 | 5.376 | 4 | 19 | 0.029 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | 16.869 | 5.795 | 3 | 19 | 0.176 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | 17.014 | 5.788 | 3 | 19 | 0.177 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | cluster por estado | 1457 | 499 | 16.869 | 10.991 | 1 | 19 | 0.000 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | 16.905 | 5.799 | 2 | 19 | 0.152 |
| municipio_trim | escalonado | cred_consumo_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | 16.869 | 5.795 | 2 | 31 | 0.381 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -0.189 | 0.131 | 0 | 19 | 0.204 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | anticipación δ=1 | 1457 | 499 | -0.263 | 0.164 | 0 | 19 | 0.201 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | solo nunca tratados como control | 1457 | 499 | -0.254 | 0.140 | 3 | 19 | 0.048 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | sin covariables | 1457 | 499 | -0.524 | 0.199 | 1 | 19 | 0.177 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | -0.189 | 0.131 | 0 | 19 | 0.204 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -0.190 | 0.130 | 0 | 19 | 0.185 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | cluster por estado | 1457 | 499 | -0.189 | 0.121 | 0 | 19 | 0.000 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | -0.189 | 0.131 | 0 | 19 | 0.207 |
| municipio_trim | escalonado | cred_vivienda_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | -0.189 | 0.131 | 1 | 31 | 0.255 |
| municipio_trim | escalonado | remesas_usd_adulto | base (aún no tratados, δ=0, DR) | 1456 | 496 | 9.008 | 3.944 | 1 | 19 | 0.001 |
| municipio_trim | escalonado | remesas_usd_adulto | anticipación δ=1 | 1456 | 496 | 8.273 | 4.571 | 1 | 19 | 0.001 |
| municipio_trim | escalonado | remesas_usd_adulto | solo nunca tratados como control | 1456 | 496 | 8.252 | 4.207 | 6 | 19 | 0.002 |
| municipio_trim | escalonado | remesas_usd_adulto | sin covariables | 1456 | 496 | 9.464 | 3.032 | 1 | 19 | 0.000 |
| municipio_trim | escalonado | remesas_usd_adulto | cohortes de 30 unidades o más | 1456 | 496 | 9.008 | 3.944 | 1 | 19 | 0.001 |
| municipio_trim | escalonado | remesas_usd_adulto | incluye fechas ambiguas y sospechosas | 1464 | 496 | 8.972 | 3.941 | 1 | 19 | 0.001 |
| municipio_trim | escalonado | remesas_usd_adulto | cluster por estado | 1456 | 496 | 9.008 | 3.578 | 2 | 19 | 0.000 |
| municipio_trim | escalonado | remesas_usd_adulto | sin municipios con cierres (P-9) | 1454 | 496 | 9.017 | 3.947 | 1 | 19 | 0.001 |
| municipio_trim | escalonado | sucursales_bm_pc | base (aún no tratados, δ=0, DR) | 1457 | 500 | -0.001 | 0.006 | 0 | 19 | 0.055 |
| municipio_trim | escalonado | sucursales_bm_pc | anticipación δ=1 | 1457 | 500 | -0.009 | 0.006 | 1 | 19 | 0.048 |
| municipio_trim | escalonado | sucursales_bm_pc | solo nunca tratados como control | 1457 | 500 | -0.007 | 0.007 | 2 | 19 | 0.412 |
| municipio_trim | escalonado | sucursales_bm_pc | sin covariables | 1457 | 500 | 0.002 | 0.003 | 1 | 19 | 0.006 |
| municipio_trim | escalonado | sucursales_bm_pc | cohortes de 30 unidades o más | 1457 | 500 | -0.001 | 0.006 | 0 | 19 | 0.055 |
| municipio_trim | escalonado | sucursales_bm_pc | incluye fechas ambiguas y sospechosas | 1465 | 500 | -0.001 | 0.006 | 1 | 19 | 0.051 |
| municipio_trim | escalonado | sucursales_bm_pc | cluster por estado | 1457 | 500 | -0.001 | 0.008 | 2 | 19 | 0.000 |
| municipio_trim | escalonado | sucursales_bm_pc | sin municipios con cierres (P-9) | 1455 | 500 | -0.001 | 0.006 | 0 | 19 | 0.056 |
| municipio_trim | escalonado | sucursales_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 500 | 0.008 | 0.009 | 1 | 19 | 0.515 |
| municipio_trim | escalonado | sucursales_eacp_pc | anticipación δ=1 | 1457 | 500 | 0.016 | 0.013 | 1 | 19 | 0.573 |
| municipio_trim | escalonado | sucursales_eacp_pc | solo nunca tratados como control | 1457 | 500 | 0.015 | 0.011 | 2 | 19 | 0.248 |
| municipio_trim | escalonado | sucursales_eacp_pc | sin covariables | 1457 | 500 | 0.002 | 0.010 | 1 | 19 | 0.562 |
| municipio_trim | escalonado | sucursales_eacp_pc | cohortes de 30 unidades o más | 1457 | 500 | 0.008 | 0.009 | 1 | 19 | 0.515 |
| municipio_trim | escalonado | sucursales_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 500 | 0.008 | 0.009 | 1 | 19 | 0.515 |
| municipio_trim | escalonado | sucursales_eacp_pc | cluster por estado | 1457 | 500 | 0.008 | 0.009 | 2 | 19 | 0.000 |
| municipio_trim | escalonado | sucursales_eacp_pc | sin municipios con cierres (P-9) | 1455 | 500 | 0.008 | 0.009 | 1 | 19 | 0.515 |
| municipio_trim | escalonado | sucursales_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | 0.015 | 0.013 | 1 | 31 | 0.322 |
| municipio_trim | escalonado | sucursales_privado_pc | base (aún no tratados, δ=0, DR) | 1457 | 500 | 0.007 | 0.009 | 2 | 19 | 0.287 |
| municipio_trim | escalonado | sucursales_privado_pc | anticipación δ=1 | 1457 | 500 | 0.007 | 0.013 | 2 | 19 | 0.258 |
| municipio_trim | escalonado | sucursales_privado_pc | solo nunca tratados como control | 1457 | 500 | 0.008 | 0.011 | 0 | 19 | 0.258 |
| municipio_trim | escalonado | sucursales_privado_pc | sin covariables | 1457 | 500 | 0.004 | 0.010 | 2 | 19 | 0.143 |
| municipio_trim | escalonado | sucursales_privado_pc | cohortes de 30 unidades o más | 1457 | 500 | 0.007 | 0.009 | 2 | 19 | 0.287 |
| municipio_trim | escalonado | sucursales_privado_pc | incluye fechas ambiguas y sospechosas | 1465 | 500 | 0.007 | 0.009 | 2 | 19 | 0.281 |
| municipio_trim | escalonado | sucursales_privado_pc | cluster por estado | 1457 | 500 | 0.007 | 0.010 | 3 | 19 | 0.000 |
| municipio_trim | escalonado | sucursales_privado_pc | sin municipios con cierres (P-9) | 1455 | 500 | 0.007 | 0.009 | 2 | 19 | 0.288 |
| municipio_trim | escalonado | ta_micro_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -1.099 | 2.476 | 2 | 19 | 0.021 |
| municipio_trim | escalonado | ta_micro_pc | anticipación δ=1 | 1457 | 499 | -1.345 | 2.961 | 2 | 19 | 0.026 |
| municipio_trim | escalonado | ta_micro_pc | solo nunca tratados como control | 1457 | 499 | -1.078 | 2.901 | 1 | 19 | 0.373 |
| municipio_trim | escalonado | ta_micro_pc | sin covariables | 1457 | 499 | 1.041 | 1.277 | 3 | 19 | 0.053 |
| municipio_trim | escalonado | ta_micro_pc | cohortes de 30 unidades o más | 1457 | 499 | -1.099 | 2.476 | 2 | 19 | 0.021 |
| municipio_trim | escalonado | ta_micro_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -1.099 | 2.487 | 2 | 19 | 0.020 |
| municipio_trim | escalonado | ta_micro_pc | cluster por estado | 1457 | 499 | -1.099 | 2.610 | 3 | 19 | 0.000 |
| municipio_trim | escalonado | ta_micro_pc | sin municipios con cierres (P-9) | 1455 | 499 | -1.096 | 2.472 | 2 | 19 | 0.020 |
| municipio_trim | escalonado | ta_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -109.427 | 91.125 | 3 | 19 | 0.070 |
| municipio_trim | escalonado | ta_pc | anticipación δ=1 | 1457 | 499 | -131.645 | 101.504 | 3 | 19 | 0.063 |
| municipio_trim | escalonado | ta_pc | solo nunca tratados como control | 1457 | 499 | -119.764 | 102.128 | 0 | 19 | 0.469 |
| municipio_trim | escalonado | ta_pc | sin covariables | 1457 | 499 | 15.605 | 9.953 | 2 | 19 | 0.276 |
| municipio_trim | escalonado | ta_pc | cohortes de 30 unidades o más | 1457 | 499 | -109.427 | 91.125 | 3 | 19 | 0.070 |
| municipio_trim | escalonado | ta_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -111.074 | 91.545 | 3 | 19 | 0.054 |
| municipio_trim | escalonado | ta_pc | cluster por estado | 1457 | 499 | -109.427 | 99.091 | 3 | 19 | 0.000 |
| municipio_trim | escalonado | ta_pc | sin municipios con cierres (P-9) | 1455 | 499 | -109.237 | 90.992 | 3 | 19 | 0.067 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | base (aún no tratados, δ=0, DR) | 1457 | 499 | -77.295 | 42.867 | 5 | 19 | 0.001 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | anticipación δ=1 | 1457 | 499 | -83.258 | 47.989 | 5 | 19 | 0.008 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | solo nunca tratados como control | 1457 | 499 | -78.623 | 46.741 | 1 | 19 | 0.387 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | sin covariables | 1457 | 499 | 81.105 | 10.545 | 4 | 19 | 0.000 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | cohortes de 30 unidades o más | 1457 | 499 | -77.295 | 42.867 | 5 | 19 | 0.001 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | incluye fechas ambiguas y sospechosas | 1465 | 499 | -76.617 | 43.031 | 6 | 19 | 0.001 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | cluster por estado | 1457 | 499 | -77.295 | 43.800 | 6 | 19 | 0.000 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | sin municipios con cierres (P-9) | 1455 | 499 | -77.105 | 42.837 | 5 | 19 | 0.001 |
| municipio_trim | escalonado | tarjetas_debito_eacp_pc | pre-periodo desde 2016 (panel largo, hasta 2025T4) | 1457 | 499 | -77.295 | 42.867 | 7 | 31 | 0.000 |

## HonestDiD (magnitudes relativas, base universal)

| lb | ub | method | Delta | Mbar | etiqueta | panel | diseno | resultado | referencia_e |
|---|---|---|---|---|---|---|---|---|---|
| 1.897 | 4.006 | C-LF | DeltaRM | 0.000 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 1.195 | 4.709 | C-LF | DeltaRM | 0.250 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 0.351 | 5.693 | C-LF | DeltaRM | 0.500 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -1.757 | 7.801 | C-LF | DeltaRM | 1.000 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -3.866 | 9.910 | C-LF | DeltaRM | 1.500 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -6.115 | 12.159 | C-LF | DeltaRM | 2.000 | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 1.856 | 4.047 | Original | nan |  | localidad_act_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 5.404 | 9.079 | C-LF | DeltaRM | 0.000 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 4.401 | 10.082 | C-LF | DeltaRM | 0.250 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 2.731 | 11.419 | C-LF | DeltaRM | 0.500 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| -0.611 | 15.094 | C-LF | DeltaRM | 1.000 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| -4.286 | 18.770 | C-LF | DeltaRM | 1.500 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| -7.962 | 22.445 | C-LF | DeltaRM | 2.000 | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 5.078 | 9.405 | Original | nan |  | localidad_act_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 0.231 | 0.436 | C-LF | DeltaRM | 0.000 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.137 | 0.531 | C-LF | DeltaRM | 0.250 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.006 | 0.642 | C-LF | DeltaRM | 0.500 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.274 | 0.926 | C-LF | DeltaRM | 1.000 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.574 | 1.210 | C-LF | DeltaRM | 1.500 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.858 | 1.494 | C-LF | DeltaRM | 2.000 | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.216 | 0.452 | Original | nan |  | localidad_act_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 2.184 | 4.673 | C-LF | DeltaRM | 0.000 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 1.521 | 5.336 | C-LF | DeltaRM | 0.250 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 0.691 | 6.165 | C-LF | DeltaRM | 0.500 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -1.299 | 8.156 | C-LF | DeltaRM | 1.000 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -3.456 | 10.313 | C-LF | DeltaRM | 1.500 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| -5.612 | 12.469 | C-LF | DeltaRM | 2.000 | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 2.028 | 4.829 | Original | nan |  | localidad_act_regimen_total_estab_consumo_pc | localidad | actualizaciones | estab_consumo_pc | -9 |
| 5.293 | 11.183 | C-LF | DeltaRM | 0.000 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 4.900 | 11.575 | C-LF | DeltaRM | 0.250 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 4.507 | 12.361 | C-LF | DeltaRM | 0.500 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 1.759 | 15.109 | C-LF | DeltaRM | 1.000 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| -0.990 | 17.858 | C-LF | DeltaRM | 1.500 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| -4.131 | 20.607 | C-LF | DeltaRM | 2.000 | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 5.162 | 11.313 | Original | nan |  | localidad_act_regimen_total_estab_emprendimiento_pc | localidad | actualizaciones | estab_emprendimiento_pc | -9 |
| 0.299 | 0.560 | C-LF | DeltaRM | 0.000 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.198 | 0.661 | C-LF | DeltaRM | 0.250 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.058 | 0.802 | C-LF | DeltaRM | 0.500 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.264 | 1.103 | C-LF | DeltaRM | 1.000 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.586 | 1.425 | C-LF | DeltaRM | 1.500 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| -0.928 | 1.767 | C-LF | DeltaRM | 2.000 | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.287 | 0.572 | Original | nan |  | localidad_act_regimen_total_estab_salud_pc | localidad | actualizaciones | estab_salud_pc | -9 |
| 0.138 | 0.825 | C-LF | DeltaRM | 0.000 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| 0.033 | 1.089 | C-LF | DeltaRM | 0.250 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| -0.231 | 1.406 | C-LF | DeltaRM | 0.500 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| -0.971 | 2.146 | C-LF | DeltaRM | 1.000 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| -1.764 | 2.939 | C-LF | DeltaRM | 1.500 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| -2.503 | 3.678 | C-LF | DeltaRM | 2.000 | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| 0.116 | 0.847 | Original | nan |  | localidad_esc_estab_emprendimiento_pc | localidad | escalonado | estab_emprendimiento_pc | -1 |
| -14.877 | 15.230 | C-LF | DeltaRM | 0.000 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -15.518 | 16.511 | C-LF | DeltaRM | 0.250 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -16.799 | 17.793 | C-LF | DeltaRM | 0.500 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -19.361 | 21.636 | C-LF | DeltaRM | 1.000 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -22.564 | 26.761 | C-LF | DeltaRM | 1.500 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -26.408 | 31.885 | C-LF | DeltaRM | 2.000 | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -14.706 | 15.060 | Original | nan |  | municipio_ce_esc_ce_personal_ocupado_pc | municipio_ce | escalonado | personal_ocupado_pc | -1 |
| -1.695 | 1.048 | C-LF | DeltaRM | 0.000 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -2.018 | 1.210 | C-LF | DeltaRM | 0.250 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -2.502 | 1.371 | C-LF | DeltaRM | 0.500 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -3.793 | 2.339 | C-LF | DeltaRM | 1.000 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -5.084 | 3.630 | C-LF | DeltaRM | 1.500 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -6.375 | 4.921 | C-LF | DeltaRM | 2.000 | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -1.668 | 1.021 | Original | nan |  | municipio_ce_esc_ce_ue_pc | municipio_ce | escalonado | ue_pc | -1 |
| -20.456 | 16.823 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -181.997 | 178.364 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -368.390 | 364.757 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -741.177 | 737.544 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -1,126.390 | 1,122.757 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -1,499.177 | 1,495.544 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -29.709 | 26.076 | Original | nan |  | municipio_trim_esc_eacp_capt_ahorro_eacp_pc | municipio_trim | escalonado | capt_ahorro_eacp_pc | -1 |
| -17.476 | -2.443 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -47.540 | 27.621 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -84.285 | 62.696 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -156.105 | 134.516 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -227.925 | 206.336 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -301.415 | 279.826 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -18.985 | -0.934 | Original | nan |  | municipio_trim_esc_eacp_capt_plazo_eacp_pc | municipio_trim | escalonado | capt_plazo_eacp_pc | -1 |
| -22.629 | 13.483 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -263.379 | 254.233 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -528.204 | 519.058 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -1,057.853 | 1,048.707 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -1,587.503 | 1,578.357 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -2,117.152 | 2,108.007 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| -26.377 | 17.232 | Original | nan |  | municipio_trim_esc_eacp_capt_vista_eacp_pc | municipio_trim | escalonado | capt_vista_eacp_pc | -1 |
| 2.410 | 5.719 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -93.560 | 101.689 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -196.148 | 204.277 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -398.015 | 406.144 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -596.573 | 604.702 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -798.440 | 806.569 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| 1.052 | 7.076 | Original | nan |  | municipio_trim_esc_eacp_cred_consumo_eacp_pc | municipio_trim | escalonado | cred_consumo_eacp_pc | -1 |
| -0.157 | -0.019 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -4.311 | 4.135 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -8.603 | 8.428 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -17.188 | 17.012 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -25.911 | 25.735 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -34.496 | 34.320 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -0.218 | 0.042 | Original | nan |  | municipio_trim_esc_eacp_cred_vivienda_eacp_pc | municipio_trim | escalonado | cred_vivienda_eacp_pc | -1 |
| -29.273 | -8.542 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -70.735 | 26.009 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -105.286 | 67.471 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -188.209 | 157.304 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -278.043 | 240.228 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -360.966 | 323.151 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -30.705 | -7.110 | Original | nan |  | municipio_trim_esc_eacp_tarjetas_debito_eacp_pc | municipio_trim | escalonado | tarjetas_debito_eacp_pc | -1 |
| -0.499 | 0.752 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -3.179 | 3.433 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -6.395 | 6.649 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -12.828 | 13.082 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -19.261 | 19.515 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -25.694 | 25.948 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -0.608 | 0.861 | Original | nan |  | municipio_trim_esc_imss_ta_micro_pc | municipio_trim | escalonado | ta_micro_pc | -1 |
| -25.251 | -8.851 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -74.452 | 56.750 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -123.653 | 105.951 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -222.055 | 220.753 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -336.857 | 335.556 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -451.659 | 433.957 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| -38.627 | 4.525 | Original | nan |  | municipio_trim_esc_imss_ta_pc | municipio_trim | escalonado | ta_pc | -1 |
| 1.057 | 7.672 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -24.078 | 32.807 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -51.859 | 60.589 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -110.068 | 118.797 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -166.953 | 175.682 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -223.839 | 232.568 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| 0.684 | 8.045 | Original | nan |  | municipio_trim_esc_remesas_remesas_usd_adulto | municipio_trim | escalonado | remesas_usd_adulto | -1 |
| -0.005 | 0.006 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.029 | 0.029 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.056 | 0.057 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.114 | 0.118 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.172 | 0.176 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.230 | 0.234 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.006 | 0.007 | Original | nan |  | municipio_trim_esc_sucursales_bm_pc | municipio_trim | escalonado | sucursales_bm_pc | -1 |
| -0.011 | 0.010 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.043 | 0.046 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.088 | 0.087 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.174 | 0.177 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.263 | 0.266 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.353 | 0.352 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.013 | 0.012 | Original | nan |  | municipio_trim_esc_sucursales_eacp_pc | municipio_trim | escalonado | sucursales_eacp_pc | -1 |
| -0.013 | 0.012 | C-LF | DeltaRM | 0.000 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.058 | 0.060 | C-LF | DeltaRM | 0.250 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.113 | 0.115 | C-LF | DeltaRM | 0.500 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.228 | 0.230 | C-LF | DeltaRM | 1.000 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.342 | 0.344 | C-LF | DeltaRM | 1.500 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.456 | 0.458 | C-LF | DeltaRM | 2.000 | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |
| -0.015 | 0.014 | Original | nan |  | municipio_trim_esc_sucursales_privado_pc | municipio_trim | escalonado | sucursales_privado_pc | -1 |

## Heterogeneidad (q-values BH sobre las diferencias)

| resultado | dimension | grupo | tratadas | att | ee | dif_vs_ref | p_dif | q_dif |
|---|---|---|---|---|---|---|---|---|
| estab_consumo_pc | desierto_bancario | 0 | 339 | 0.629 | 0.916 |  |  |  |
| estab_consumo_pc | desierto_bancario | 1 | 767 | 3.950 | 0.687 | 3.321 | 0.004 | 0.037 |
| estab_consumo_pc | exposicion | tardía (2023S1–2024S1) | 793 | 2.925 | 0.588 |  |  |  |
| estab_consumo_pc | exposicion | temprana (hasta 2022S2) | 313 | 3.321 | 0.779 | 0.396 | 0.685 | 0.861 |
| estab_consumo_pc | grado_marginacion_2020 | alta marginación | 373 | 4.209 | 1.275 |  |  |  |
| estab_consumo_pc | grado_marginacion_2020 | baja marginación | 520 | 0.982 | 0.686 | -3.227 | 0.026 | 0.158 |
| estab_consumo_pc | grado_marginacion_2020 | marginación media | 213 | 4.646 | 1.394 | 0.438 | 0.817 | 0.915 |
| estab_consumo_pc | tamano_localidad | chica | 47 | -0.648 | 0.619 |  |  |  |
| estab_consumo_pc | tamano_localidad | grande | 996 | 3.270 | 0.639 | 3.918 | 0.000 | 0.001 |
| estab_consumo_pc | tamano_localidad | mediana | 63 | 0.283 | 1.851 | 0.931 | 0.633 | 0.861 |
| estab_emprendimiento_pc | desierto_bancario | 0 | 339 | 3.248 | 1.350 |  |  |  |
| estab_emprendimiento_pc | desierto_bancario | 1 | 767 | 9.031 | 1.553 | 5.783 | 0.005 | 0.040 |
| estab_emprendimiento_pc | exposicion | tardía (2023S1–2024S1) | 793 | 7.015 | 1.185 |  |  |  |
| estab_emprendimiento_pc | exposicion | temprana (hasta 2022S2) | 313 | 7.739 | 1.281 | 0.724 | 0.678 | 0.861 |
| estab_emprendimiento_pc | grado_marginacion_2020 | alta marginación | 373 | 10.611 | 3.320 |  |  |  |
| estab_emprendimiento_pc | grado_marginacion_2020 | baja marginación | 520 | 3.180 | 1.077 | -7.431 | 0.033 | 0.181 |
| estab_emprendimiento_pc | grado_marginacion_2020 | marginación media | 213 | 11.340 | 3.413 | 0.729 | 0.878 | 0.936 |
| estab_emprendimiento_pc | tamano_localidad | chica | 47 | 0.747 | 0.970 |  |  |  |
| estab_emprendimiento_pc | tamano_localidad | grande | 996 | 7.509 | 1.333 | 6.762 | 0.000 | 0.001 |
| estab_emprendimiento_pc | tamano_localidad | mediana | 63 | 6.875 | 2.777 | 6.127 | 0.037 | 0.183 |
| estab_salud_pc | desierto_bancario | 0 | 339 | 0.189 | 0.084 |  |  |  |
| estab_salud_pc | desierto_bancario | 1 | 767 | 0.415 | 0.079 | 0.226 | 0.050 | 0.224 |
| estab_salud_pc | exposicion | tardía (2023S1–2024S1) | 793 | 0.341 | 0.066 |  |  |  |
| estab_salud_pc | exposicion | temprana (hasta 2022S2) | 313 | 0.338 | 0.083 | -0.003 | 0.977 | 0.977 |
| estab_salud_pc | grado_marginacion_2020 | alta marginación | 373 | 0.472 | 0.111 |  |  |  |
| estab_salud_pc | grado_marginacion_2020 | baja marginación | 520 | 0.233 | 0.081 | -0.240 | 0.081 | 0.306 |
| estab_salud_pc | grado_marginacion_2020 | marginación media | 213 | 0.439 | 0.160 | -0.034 | 0.862 | 0.936 |
| estab_salud_pc | tamano_localidad | chica | 47 | 0.266 | 0.270 |  |  |  |
| estab_salud_pc | tamano_localidad | grande | 996 | 0.383 | 0.066 | 0.117 | 0.673 | 0.861 |
| estab_salud_pc | tamano_localidad | mediana | 63 | -0.123 | 0.193 | -0.388 | 0.242 | 0.598 |
| personal_ocupado_pc | desierto_bancario | 0 | 478 | -40.566 | 54.089 |  |  |  |
| personal_ocupado_pc | desierto_bancario | 1 | 774 | -2.506 | 3.925 | 38.060 | 0.483 | 0.792 |
| personal_ocupado_pc | exposicion_ce | tardía | 968 | -16.699 | 14.572 |  |  |  |
| personal_ocupado_pc | exposicion_ce | temprana | 284 | -18.724 | 20.617 | -2.024 | 0.936 | 0.956 |
| ue_pc | desierto_bancario | 0 | 478 | -1.592 | 2.750 |  |  |  |
| ue_pc | desierto_bancario | 1 | 774 | -0.025 | 0.897 | 1.567 | 0.588 | 0.861 |
| ue_pc | exposicion_ce | tardía | 968 | -1.365 | 0.977 |  |  |  |
| ue_pc | exposicion_ce | temprana | 284 | -0.941 | 1.353 | 0.423 | 0.800 | 0.915 |
| capt_ahorro_eacp_pc | desierto_bancario | 0 | 525 | 61.940 | 73.454 |  |  |  |
| capt_ahorro_eacp_pc | desierto_bancario | 1 | 932 | -0.290 | 16.420 | -62.230 | 0.408 | 0.758 |
| capt_ahorro_eacp_pc | grado_marginacion_2020 | alta marginación | 476 | -30.214 | 11.908 |  |  |  |
| capt_ahorro_eacp_pc | grado_marginacion_2020 | baja marginación | 703 | 17.596 | 36.551 | 47.810 | 0.214 | 0.598 |
| capt_ahorro_eacp_pc | grado_marginacion_2020 | marginación media | 278 | 9.592 | 28.128 | 39.806 | 0.193 | 0.590 |
| capt_ahorro_eacp_pc | tamano_localidad | chica | 246 | -124.488 | 52.685 |  |  |  |
| capt_ahorro_eacp_pc | tamano_localidad | grande | 634 | 65.674 | 27.273 | 190.162 | 0.001 | 0.022 |
| capt_ahorro_eacp_pc | tamano_localidad | mediana | 577 | 55.903 | 24.746 | 180.391 | 0.002 | 0.024 |
| cred_consumo_eacp_pc | desierto_bancario | 0 | 525 | 27.271 | 21.866 |  |  |  |
| cred_consumo_eacp_pc | desierto_bancario | 1 | 932 | 5.396 | 6.204 | -21.875 | 0.336 | 0.715 |
| cred_consumo_eacp_pc | grado_marginacion_2020 | alta marginación | 476 | -5.539 | 6.852 |  |  |  |
| cred_consumo_eacp_pc | grado_marginacion_2020 | baja marginación | 703 | 23.669 | 9.032 | 29.208 | 0.010 | 0.070 |
| cred_consumo_eacp_pc | grado_marginacion_2020 | marginación media | 278 | 10.434 | 11.878 | 15.973 | 0.244 | 0.598 |
| cred_consumo_eacp_pc | tamano_localidad | chica | 246 | 5.336 | 9.717 |  |  |  |
| cred_consumo_eacp_pc | tamano_localidad | grande | 634 | 29.345 | 10.240 | 24.009 | 0.089 | 0.309 |
| cred_consumo_eacp_pc | tamano_localidad | mediana | 577 | 11.826 | 6.405 | 6.490 | 0.577 | 0.861 |
| ta_micro_pc | desierto_bancario | 0 | 525 | -2.802 | 4.554 |  |  |  |
| ta_micro_pc | desierto_bancario | 1 | 932 | -0.750 | 0.602 | 2.052 | 0.655 | 0.861 |
| ta_pc | desierto_bancario | 0 | 525 | -87.101 | 78.091 |  |  |  |
| ta_pc | desierto_bancario | 1 | 932 | -8.796 | 22.640 | 78.305 | 0.336 | 0.715 |
| sucursales_bm_pc | desierto_bancario | 0 | 525 | 0.022 | 0.027 |  |  |  |
| sucursales_bm_pc | desierto_bancario | 1 | 932 | 0.001 | 0.001 | -0.020 | 0.455 | 0.792 |
| sucursales_bm_pc | grado_marginacion_2020 | alta marginación | 476 | 0.001 | 0.001 |  |  |  |
| sucursales_bm_pc | grado_marginacion_2020 | baja marginación | 703 | -0.002 | 0.008 | -0.003 | 0.685 | 0.861 |
| sucursales_bm_pc | grado_marginacion_2020 | marginación media | 278 | 0.008 | 0.004 | 0.007 | 0.064 | 0.261 |
| sucursales_bm_pc | tamano_localidad | chica | 246 | -0.003 | 0.003 |  |  |  |
| sucursales_bm_pc | tamano_localidad | grande | 634 | -0.004 | 0.008 | -0.001 | 0.909 | 0.948 |
| sucursales_bm_pc | tamano_localidad | mediana | 577 | 0.011 | 0.008 | 0.015 | 0.095 | 0.309 |
| sucursales_eacp_pc | desierto_bancario | 0 | 525 | 0.018 | 0.019 |  |  |  |
| sucursales_eacp_pc | desierto_bancario | 1 | 932 | 0.003 | 0.009 | -0.014 | 0.488 | 0.792 |
| sucursales_eacp_pc | grado_marginacion_2020 | alta marginación | 476 | -0.004 | 0.014 |  |  |  |
| sucursales_eacp_pc | grado_marginacion_2020 | baja marginación | 703 | 0.012 | 0.014 | 0.017 | 0.394 | 0.758 |
| sucursales_eacp_pc | grado_marginacion_2020 | marginación media | 278 | 0.017 | 0.018 | 0.021 | 0.353 | 0.722 |
| sucursales_eacp_pc | tamano_localidad | chica | 246 | 0.009 | 0.019 |  |  |  |
| sucursales_eacp_pc | tamano_localidad | grande | 634 | 0.003 | 0.013 | -0.005 | 0.822 | 0.915 |
| sucursales_eacp_pc | tamano_localidad | mediana | 577 | 0.015 | 0.015 | 0.006 | 0.794 | 0.915 |
| sucursales_privado_pc | desierto_bancario | 0 | 525 | 0.040 | 0.031 |  |  |  |
| sucursales_privado_pc | desierto_bancario | 1 | 932 | 0.005 | 0.009 | -0.035 | 0.283 | 0.661 |
| sucursales_privado_pc | grado_marginacion_2020 | alta marginación | 476 | -0.003 | 0.014 |  |  |  |
| sucursales_privado_pc | grado_marginacion_2020 | baja marginación | 703 | 0.010 | 0.014 | 0.013 | 0.501 | 0.792 |
| sucursales_privado_pc | grado_marginacion_2020 | marginación media | 278 | 0.025 | 0.018 | 0.028 | 0.221 | 0.598 |
| sucursales_privado_pc | tamano_localidad | chica | 246 | 0.005 | 0.020 |  |  |  |
| sucursales_privado_pc | tamano_localidad | grande | 634 | -0.001 | 0.012 | -0.006 | 0.788 | 0.915 |
| sucursales_privado_pc | tamano_localidad | mediana | 577 | 0.026 | 0.017 | 0.021 | 0.418 | 0.758 |

## Balance del emparejamiento

| resultado | variable | media_tratadas | media_controles | media_tratadas_emparejadas | media_controles_emparejados | dif_est_antes | dif_est_despues | tratadas_emparejadas | tratadas_elegibles |
|---|---|---|---|---|---|---|---|---|---|
| estab_consumo_pc | log_poblacion_2020 | 7.842 | 5.344 | 7.084 | 7.034 | 1.963 | 0.040 | 550 | 1106 |
| estab_consumo_pc | indice_marginacion_2020 | 53.753 | 53.203 | 53.450 | 53.334 | 0.114 | 0.024 | 550 | 1106 |
| estab_consumo_pc | log1p_estab_previos | 4.572 | 0.237 | 3.412 | 3.354 | 2.434 | 0.033 | 550 | 1106 |
| estab_consumo_pc | log1p_nivel_previo | 2.965 | 0.146 | 2.429 | 2.402 | 2.568 | 0.024 | 550 | 1106 |
| estab_emprendimiento_pc | log_poblacion_2020 | 7.842 | 5.344 | 7.054 | 7.016 | 1.963 | 0.030 | 562 | 1106 |
| estab_emprendimiento_pc | indice_marginacion_2020 | 53.753 | 53.203 | 53.443 | 53.388 | 0.114 | 0.011 | 562 | 1106 |
| estab_emprendimiento_pc | log1p_estab_previos | 4.572 | 0.237 | 3.373 | 3.337 | 2.434 | 0.020 | 562 | 1106 |
| estab_emprendimiento_pc | log1p_nivel_previo | 3.513 | 0.314 | 2.913 | 2.903 | 2.412 | 0.008 | 562 | 1106 |
| estab_salud_pc | log_poblacion_2020 | 7.842 | 5.344 | 6.928 | 6.853 | 1.963 | 0.059 | 472 | 1106 |
| estab_salud_pc | indice_marginacion_2020 | 53.753 | 53.203 | 53.473 | 53.291 | 0.114 | 0.038 | 472 | 1106 |
| estab_salud_pc | log1p_estab_previos | 4.572 | 0.237 | 3.056 | 3.003 | 2.434 | 0.030 | 472 | 1106 |
| estab_salud_pc | log1p_nivel_previo | 1.184 | 0.040 | 0.873 | 0.862 | 2.181 | 0.021 | 472 | 1106 |

# Fase 2: fuentes nuevas (preregistro del 2026-10-07)

Fuera de la maestra y de las familias de la especificación principal; criterios iguales. En los resultados en logaritmo, *efecto %* y *cota* están en puntos log × 100.

## Resumen de la fase 2

| familia | resultado | n_tratadas | n_controles | valor | ee | efecto_pct | cota_equivalencia_pct | pre_sig | pre_n | pre_wald_p | p | p_rw | q_bh_fase2 | lectura |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| efipem | log_derechos_pc | 1447 | 500 | -0.064 | 0.053 | -6.446 | 15.207 | 0 | 7 | 0.789 | 0.226 | 0.443 | 0.339 | no informativo |
| efipem | log_impuestos_pc | 1419 | 442 | -0.041 | 0.051 | -4.076 | 12.529 | 1 | 7 | 0.171 | 0.428 | 0.462 | 0.499 | no informativo |
| efipem | log_predial_pc | 1289 | 385 | 0.098 | 0.066 | 9.784 | 20.672 | 0 | 7 | 0.038 | 0.139 | 0.372 | 0.261 | descriptivo (pre-prueba falla) |
| eic | log_ingreso_trabajo | 1461 | 499 | 0.012 | 0.016 | 1.152 | 3.789 | 0 | 1 | 0.602 | 0.473 | 0.605 | 0.522 | nulo informativo |
| eic | pct_cuenta_propia | 1461 | 499 | -1.688 | 1.036 | -6.625 | 13.314 | 0 | 1 | 0.262 | 0.103 | 0.273 | 0.246 | no informativo |
| eic | pct_empleador | 1461 | 499 | 0.521 | 0.235 | 20.209 | 35.178 | 0 | 1 | 0.146 | 0.026 | 0.069 | 0.111 | significativo sin corrección (BH q ≥ 0.05) |
| eic | pct_negocio | 1461 | 499 | -1.168 | 1.013 | -4.161 | 10.097 | 0 | 1 | 0.614 | 0.249 | 0.605 | 0.348 | no informativo |
| eic | pct_ocupacion | 1461 | 499 | 0.538 | 0.552 | 1.165 | 3.133 | 0 | 1 | 0.906 | 0.330 | 0.605 | 0.408 | nulo informativo |
| eic_mecanismo | log_poblacion_est | 1461 | 499 | 0.023 | 0.011 | 2.250 | 4.072 | 0 | 1 | 0.416 | 0.042 |  | 0.127 | significativo sin corrección (BH q ≥ 0.05) |
| eic_mecanismo | pct_hog_programas | 1461 | 499 | 2.065 | 0.725 | 5.129 | 8.091 | 1 | 1 | 0.013 | 0.004 |  | 0.046 | descriptivo (pre-prueba falla) |
| eic_mecanismo | pct_hog_remesas | 1461 | 499 | -0.526 | 0.336 | -5.849 | 11.990 | 0 | 1 | 0.092 | 0.117 |  | 0.246 | no informativo |
| eic_mecanismo | pct_trabaja_otro_mun | 1461 | 499 | 2.167 | 1.029 | 13.201 | 23.510 | 0 | 1 | 0.844 | 0.035 |  | 0.123 | significativo sin corrección (BH q ≥ 0.05) |
| eic_mecanismo | pct_viv_celular | 1461 | 499 | -2.647 | 1.157 | -3.531 | 6.070 | 0 | 1 | 0.672 | 0.022 |  | 0.111 | significativo sin corrección (BH q ≥ 0.05) |
| eic_mecanismo | pct_viv_internet | 1461 | 499 | 2.648 | 1.652 | 9.735 | 19.721 | 0 | 1 | 0.720 | 0.109 |  | 0.246 | no informativo |
| enoe | log_ingreso | 146 | 12 | 0.033 | 0.033 | 3.303 | 8.688 | 2 | 19 | 0.047 | 0.313 | 0.545 | 0.408 | descriptivo (pre-prueba falla) |
| enoe | pct_informal | 146 | 12 | 3.939 | 1.602 | 13.047 | 21.772 | 2 | 19 | 0.080 | 0.014 | 0.035 | 0.097 | significativo sin corrección (BH q ≥ 0.05) |
| enoe | pct_negocio | 146 | 12 | 2.118 | 1.546 | 8.195 | 18.037 | 0 | 19 | 0.231 | 0.171 | 0.422 | 0.276 | no informativo |
| enoe | pct_ocupacion | 146 | 12 | 0.507 | 1.128 | 0.860 | 4.008 | 0 | 19 | 0.571 | 0.653 | 0.672 | 0.686 | nulo informativo |
| viirs | log1p_luz_1km | 1106 | 21719 | 0.003 | 0.009 | 0.325 | 1.844 | 2 | 7 | 0.000 | 0.725 | 0.732 | 0.725 | descriptivo (pre-prueba falla) |
| viirs | log1p_luz_anillo | 1106 | 21719 | -0.017 | 0.012 | -1.714 | 3.668 | 1 | 7 | 0.006 | 0.149 | 0.253 | 0.261 | descriptivo (pre-prueba falla) |
| viirs | luz_1km_pos | 1106 | 21719 | -0.006 | 0.002 | -0.623 | 0.875 | 4 | 7 | 0.000 | 0.000 | 0.000 | 0.001 | descriptivo (pre-prueba falla) |

## Tratamiento con el Banco del Bienestar observado (P-8)

| variante | termino | unidades | tratadas | controles | clusters | att | ee | ee_boot | media_base | pre_n | pre_sig | pre_wald_p | resultado | especificacion | efecto_pct | dif_en_ee |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G de la corrida final | ATT global | 1957 | 1457 | 500 | 1957 | 0.007 | 0.009 | 0.010 | 0.929 | 19 | 2 | 0.287 | sucursales_privado_pc | principal (2019T1–2024T4) | 0.713 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1965 | 1465 | 500 | 1965 | 0.008 | 0.009 | 0.010 | 0.932 | 19 | 2 | 0.272 | sucursales_privado_pc | principal (2019T1–2024T4) | 0.871 | 0.158 |
| G de la corrida final | ATT global | 1957 | 1457 | 500 | 1957 | -0.001 | 0.006 | 0.007 | 0.405 | 19 | 0 | 0.055 | sucursales_bm_pc | principal (2019T1–2024T4) | -0.242 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1965 | 1465 | 500 | 1965 | 0.002 | 0.006 | 0.007 | 0.408 | 19 | 1 | 0.051 | sucursales_bm_pc | principal (2019T1–2024T4) | 0.401 | 0.415 |
| G de la corrida final | ATT global | 1957 | 1457 | 500 | 1957 | 0.008 | 0.009 | 0.009 | 0.524 | 19 | 1 | 0.515 | sucursales_eacp_pc | principal (2019T1–2024T4) | 1.452 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1965 | 1465 | 500 | 1965 | 0.006 | 0.010 | 0.010 | 0.524 | 19 | 1 | 0.522 | sucursales_eacp_pc | principal (2019T1–2024T4) | 1.238 | -0.123 |
| G de la corrida final | ATT global | 1956 | 1457 | 499 | 1956 | 0.004 | 0.014 | 0.014 | 0.929 | 19 | 2 | 0.291 | sucursales_privado_pc | hasta_2025 | 0.453 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1964 | 1465 | 499 | 1964 | 0.010 | 0.014 | 0.014 | 0.932 | 19 | 2 | 0.276 | sucursales_privado_pc | hasta_2025 | 1.096 | 0.429 |
| G de la corrida final | ATT global | 1956 | 1457 | 499 | 1956 | -0.010 | 0.009 | 0.009 | 0.405 | 19 | 1 | 0.054 | sucursales_bm_pc | hasta_2025 | -2.572 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1964 | 1465 | 499 | 1964 | -0.004 | 0.008 | 0.008 | 0.408 | 19 | 1 | 0.050 | sucursales_bm_pc | hasta_2025 | -0.894 | 0.733 |
| G de la corrida final | ATT global | 1956 | 1457 | 499 | 1956 | 0.015 | 0.013 | 0.013 | 0.524 | 19 | 1 | 0.516 | sucursales_eacp_pc | hasta_2025 | 2.792 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1964 | 1465 | 499 | 1964 | 0.014 | 0.014 | 0.016 | 0.524 | 19 | 1 | 0.522 | sucursales_eacp_pc | hasta_2025 | 2.648 | -0.059 |
| G de la corrida final | ATT global | 1957 | 1457 | 500 | 1957 | 2.002 | 0.083 | 0.078 | 0.931 | 19 | 2 | 0.279 | sucursales_total_pc | primera etapa | 214.985 | 0.000 |
| G observado (modelo Portafolio 2022+) | ATT global | 1965 | 1465 | 500 | 1965 | 1.995 | 0.082 | 0.082 | 0.936 | 19 | 2 | 0.247 | sucursales_total_pc | primera etapa | 213.205 | -0.085 |

## Luz nocturna por banda de distancia (puntos log × 100)

| banda | tratadas | controles | att | ee | media_base | pre_n | pre_sig | pre_wald_p | placebo | placebo_ee | efecto_pct | contraste | dif_pct | ee_dif_pct | p_dif | resultado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sucursal propia | 1,106.000 | 21,719.000 | 0.003 | 0.009 | 4.157 | 7.000 | 2.000 | 0.000 |  |  | 0.078 | nan |  |  |  | log1p_luz_1km |
| 0–2 km | 2,430.000 | 21,719.000 | -0.016 | 0.007 | 3.634 | 7.000 | 5.000 | 0.000 |  |  | -0.427 | nan |  |  |  | log1p_luz_1km |
| 2–5 km | 7,138.000 | 21,719.000 | 0.003 | 0.009 | 2.800 | 7.000 | 1.000 | 0.046 |  |  | 0.123 | nan |  |  |  | log1p_luz_1km |
| 5–10 km | 9,935.000 | 21,719.000 | 0.013 | 0.008 | 2.303 | 7.000 | 1.000 | 0.006 |  |  | 0.572 | nan |  |  |  | log1p_luz_1km |
| nan |  |  |  |  |  |  |  |  |  |  |  | sucursal propia − 0–2 km | 1.876 | 0.991 | 0.058 | log1p_luz_1km |
| nan |  |  |  |  |  |  |  |  |  |  |  | sucursal propia − 5–10 km | -0.992 | 1.125 | 0.378 | log1p_luz_1km |
| nan |  |  |  |  |  |  |  |  |  |  |  | 0–2 km − 5–10 km | -2.868 | 0.800 | 0.000 | log1p_luz_1km |
| sucursal propia | 1,106.000 | 21,719.000 | -0.017 | 0.012 | 4.768 | 7.000 | 1.000 | 0.006 |  |  | -0.359 | nan |  |  |  | log1p_luz_anillo |
| 0–2 km | 2,430.000 | 21,719.000 | -0.097 | 0.009 | 5.202 | 7.000 | 7.000 | 0.000 |  |  | -1.861 | nan |  |  |  | log1p_luz_anillo |
| 2–5 km | 7,138.000 | 21,719.000 | -0.068 | 0.009 | 4.645 | 7.000 | 5.000 | 0.000 |  |  | -1.474 | nan |  |  |  | log1p_luz_anillo |
| 5–10 km | 9,935.000 | 21,719.000 | -0.008 | 0.009 | 3.498 | 7.000 | 3.000 | 0.000 |  |  | -0.236 | nan |  |  |  | log1p_luz_anillo |
| nan |  |  |  |  |  |  |  |  |  |  |  | sucursal propia − 0–2 km | 7.965 | 1.188 | 0.000 | log1p_luz_anillo |
| nan |  |  |  |  |  |  |  |  |  |  |  | sucursal propia − 5–10 km | -0.888 | 1.341 | 0.508 | log1p_luz_anillo |
| nan |  |  |  |  |  |  |  |  |  |  |  | 0–2 km − 5–10 km | -8.853 | 0.866 | 0.000 | log1p_luz_anillo |

## Luz nocturna: régimen censal y grupos de control

| variante | termino | unidades | tratadas | controles | clusters | att | ee | ee_boot | media_base | pre_n | pre_sig | pre_wald_p | resultado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| régimen de recorrido total | ATT global | 1381 | 903 | 478 | 1226 | -0.001 | 0.011 | 0.012 | 4.264 | 7 | 2 | 0.029 | log1p_luz_1km |
| controles: todos | ATT global | 67775 | 1106 | 66669 | 2455 | -0.007 | 0.005 | 0.037 | 4.157 | 7 | 3 | 0.000 | log1p_luz_1km |
| controles: solo con sucursal | ATT global | 1106 | 1106 | 0 | 1106 | 0.002 | 0.008 | 0.008 | 4.157 | 6 | 1 | 0.096 | log1p_luz_1km |
| controles: ≥20 km | ATT global | 7320 | 1106 | 6214 | 1413 | 0.023 | 0.015 | 0.039 | 4.157 | 7 | 2 | 0.000 | log1p_luz_1km |

## Luz nocturna: cambio anual de log(1 + luz) en los controles por decil de brillo de 2021

| decil | 2016→2017 | 2017→2018 | 2018→2019 | 2019→2020 | 2020→2021 | 2021→2022 | 2022→2023 | 2023→2024 |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.168 | -0.057 | -0.063 | -0.006 | -0.099 | 0.118 | 0.237 | 0.115 |
| 2 | 0.180 | -0.059 | -0.064 | -0.000 | -0.093 | 0.119 | 0.200 | 0.118 |
| 3 | 0.419 | -0.096 | -0.123 | 0.143 | 0.083 | -0.074 | 0.367 | 0.146 |
| 4 | 0.753 | -0.067 | -0.145 | 0.353 | 0.283 | -0.201 | 0.347 | 0.093 |
| 5 | 0.787 | -0.040 | -0.132 | 0.314 | 0.170 | -0.102 | 0.225 | 0.088 |
| 6 | 0.698 | -0.029 | -0.089 | 0.260 | 0.105 | -0.060 | 0.182 | 0.071 |
| 7 | 0.616 | -0.016 | -0.061 | 0.207 | 0.086 | -0.048 | 0.128 | 0.059 |
| 8 | 0.458 | -0.017 | -0.042 | 0.116 | 0.061 | -0.033 | 0.101 | 0.061 |
| 9 | 0.263 | -0.002 | -0.004 | 0.059 | 0.067 | -0.029 | 0.088 | 0.070 |
| 10 | 0.149 | -0.004 | 0.043 | 0.090 | 0.109 | -0.046 | 0.032 | 0.110 |

## EIC: dosis (aperturas tempranas contra tardías)

| variante | termino | unidades | tratadas | controles | clusters | att | ee | ee_boot | media_base | pre_n | pre_sig | pre_wald_p | panel | resultado | efecto_pct | dif_vs_ref | z_dif | p_dif |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| temprana | ATT global | 782 | 283 | 499 | 782 | 4.029 | 1.510 | 1.767 | 37.697 | 1 | 0 | 0.439 | municipio_eic | pct_hog_programas | 10.689 |  |  |  |
| tardía | ATT global | 1677 | 1178 | 499 | 1677 | 3.249 | 1.116 | 1.276 | 40.879 | 1 | 1 | 0.035 | municipio_eic | pct_hog_programas | 7.948 | -0.780 | -0.416 | 0.678 |
| temprana | ATT global | 782 | 283 | 499 | 782 | -1.522 | 1.173 | 1.418 | 27.396 | 1 | 0 | 0.275 | municipio_eic | pct_negocio | -5.555 |  |  |  |
| tardía | ATT global | 1677 | 1178 | 499 | 1677 | -1.076 | 0.951 | 1.067 | 28.223 | 1 | 0 | 0.782 | municipio_eic | pct_negocio | -3.812 | 0.446 | 0.295 | 0.768 |

## EIC: desierto bancario (el grupo con banca previa tiene solo 21 controles)

| variante | termino | unidades | tratadas | controles | clusters | att | ee | ee_boot | media_base | pre_n | pre_sig | pre_wald_p | panel | resultado | efecto_pct | dif_vs_ref | z_dif | p_dif |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ATT global | 1410 | 932 | 478 | 1410 | -0.007 | 0.659 | 0.683 | 45.882 | 1 | 0 | 0.059 | municipio_eic | pct_hog_programas | -0.016 |  |  |  |
| 0 | ATT global | 550 | 529 | 21 | 550 | 4.284 | 1.635 | 1.638 | 30.362 | 1 | 0 | 0.386 | municipio_eic | pct_hog_programas | 14.111 | 4.292 | 2.434 | 0.015 |
| 1 | ATT global | 1410 | 932 | 478 | 1410 | -1.675 | 1.634 | 2.174 | 29.142 | 1 | 0 | 0.894 | municipio_eic | pct_negocio | -5.747 |  |  |  |
| 0 | ATT global | 550 | 529 | 21 | 550 | 1.834 | 1.461 | 1.523 | 26.162 | 1 | 0 | 0.605 | municipio_eic | pct_negocio | 7.009 | 3.508 | 1.601 | 0.109 |

## Robustez de la fase 2

| panel | resultado | variante | tratadas | controles | att | ee | pre_sig | pre_n | pre_wald_p |
|---|---|---|---|---|---|---|---|---|---|
| localidad_viirs | log1p_luz_1km | base (aún no tratados, δ=0, DR) | 1106 | 21719 | 0.003 | 0.009 | 2 | 7 | 0.000 |
| localidad_viirs | log1p_luz_1km | anticipación δ=1 | 1106 | 21719 | 0.023 | 0.019 | 2 | 7 | 0.000 |
| localidad_viirs | log1p_luz_1km | solo nunca tratados como control | 1106 | 21719 | 0.009 | 0.013 | 2 | 7 | 0.037 |
| localidad_viirs | log1p_luz_1km | sin covariables | 1106 | 21719 | -0.028 | 0.007 | 6 | 7 | 0.000 |
| localidad_viirs | log1p_luz_1km | cohortes de 30 unidades o más | 1106 | 21719 | 0.003 | 0.009 | 2 | 7 | 0.000 |
| localidad_viirs | log1p_luz_1km | incluye fechas ambiguas y sospechosas | 1310 | 21719 | -0.002 | 0.012 | 3 | 7 | 0.000 |
| localidad_viirs | log1p_luz_1km | cluster por estado | 1106 | 21719 | 0.003 | 0.009 | 2 | 7 | 0.000 |
| municipio_efipem | log_impuestos_pc | base (aún no tratados, δ=0, DR) | 1419 | 442 | -0.041 | 0.051 | 1 | 7 | 0.171 |
| municipio_efipem | log_impuestos_pc | anticipación δ=1 | 1419 | 442 | -0.083 | 0.125 | 1 | 7 | 0.161 |
| municipio_efipem | log_impuestos_pc | solo nunca tratados como control | 1419 | 442 | -0.048 | 0.074 | 0 | 7 | 0.177 |
| municipio_efipem | log_impuestos_pc | sin covariables | 1419 | 442 | -0.013 | 0.031 | 1 | 7 | 0.037 |
| municipio_efipem | log_impuestos_pc | cohortes de 30 unidades o más | 1419 | 442 | -0.041 | 0.051 | 1 | 7 | 0.171 |
| municipio_efipem | log_impuestos_pc | incluye fechas ambiguas y sospechosas | 1426 | 442 | -0.041 | 0.051 | 1 | 7 | 0.165 |
| municipio_efipem | log_impuestos_pc | cluster por estado | 1419 | 442 | -0.041 | 0.035 | 1 | 7 | 0.314 |
| municipio_eic | pct_hog_programas | base (aún no tratados, δ=0, DR) | 1461 | 499 | 2.065 | 0.725 | 1 | 1 | 0.013 |
| municipio_eic | pct_hog_programas | anticipación δ=1 | 1461 | 499 | -1.128 | 1.139 | 1 | 1 | 0.013 |
| municipio_eic | pct_hog_programas | solo nunca tratados como control | 1461 | 499 | 2.065 | 0.725 | 1 | 1 | 0.013 |
| municipio_eic | pct_hog_programas | sin covariables | 1461 | 499 | 1.068 | 0.478 | 0 | 1 | 0.572 |
| municipio_eic | pct_hog_programas | cohortes de 30 unidades o más | 1461 | 499 | 2.065 | 0.725 | 1 | 1 | 0.013 |
| municipio_eic | pct_hog_programas | incluye fechas ambiguas y sospechosas | 1469 | 499 | 2.052 | 0.725 | 1 | 1 | 0.013 |
| municipio_eic | pct_hog_programas | cluster por estado | 1461 | 499 | 2.065 | 0.876 | 0 | 1 | 0.054 |
| municipio_eic | pct_negocio | base (aún no tratados, δ=0, DR) | 1461 | 499 | -1.168 | 1.013 | 0 | 1 | 0.614 |
| municipio_eic | pct_negocio | anticipación δ=1 | 1461 | 499 | -0.745 | 0.862 | 0 | 1 | 0.614 |
| municipio_eic | pct_negocio | solo nunca tratados como control | 1461 | 499 | -1.168 | 1.013 | 0 | 1 | 0.614 |
| municipio_eic | pct_negocio | sin covariables | 1461 | 499 | -0.470 | 0.635 | 0 | 1 | 0.630 |
| municipio_eic | pct_negocio | cohortes de 30 unidades o más | 1461 | 499 | -1.168 | 1.013 | 0 | 1 | 0.614 |
| municipio_eic | pct_negocio | incluye fechas ambiguas y sospechosas | 1469 | 499 | -1.156 | 1.011 | 0 | 1 | 0.612 |
| municipio_eic | pct_negocio | cluster por estado | 1461 | 499 | -1.168 | 0.659 | 0 | 1 | 0.595 |
| municipio_enoe | pct_negocio | base (aún no tratados, δ=0, DR) | 146 | 12 | 2.118 | 1.546 | 0 | 19 | 0.231 |
| municipio_enoe | pct_negocio | anticipación δ=1 | 146 | 12 | 2.487 | 1.772 | 0 | 19 | 0.129 |
| municipio_enoe | pct_negocio | solo nunca tratados como control | 146 | 12 | 1.386 | 1.487 | 4 | 19 | 0.000 |
| municipio_enoe | pct_negocio | sin covariables | 146 | 12 | 3.163 | 1.446 | 0 | 19 | 0.365 |
| municipio_enoe | pct_negocio | cohortes de 30 unidades o más | 31 | 12 | -5.433 | 2.770 | 2 | 10 | 0.000 |
| municipio_enoe | pct_negocio | incluye fechas ambiguas y sospechosas | 149 | 12 | 2.176 | 1.541 | 1 | 19 | 0.256 |
| municipio_enoe | pct_negocio | cluster por estado | 146 | 12 | 2.118 | 1.772 | 2 | 19 | 0.000 |

## HonestDiD de la fase 2

| lb | ub | method | Delta | Mbar | etiqueta | panel | diseno | resultado | referencia_e |
|---|---|---|---|---|---|---|---|---|---|
| -0.018 | 0.052 | C-LF | DeltaRM | 0.000 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.042 | 0.071 | C-LF | DeltaRM | 0.250 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.076 | 0.100 | C-LF | DeltaRM | 0.500 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.153 | 0.174 | C-LF | DeltaRM | 1.000 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.230 | 0.251 | C-LF | DeltaRM | 1.500 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.309 | 0.331 | C-LF | DeltaRM | 2.000 | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.019 | 0.052 | Original | nan |  | localidad_viirs_esc_viirs_log1p_luz_1km | localidad_viirs | escalonado | log1p_luz_1km | -1 |
| -0.215 | 0.132 | C-LF | DeltaRM | 0.000 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.272 | 0.214 | C-LF | DeltaRM | 0.250 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.335 | 0.302 | C-LF | DeltaRM | 0.500 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.468 | 0.504 | C-LF | DeltaRM | 1.000 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.619 | 0.718 | C-LF | DeltaRM | 1.500 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.833 | 0.933 | C-LF | DeltaRM | 2.000 | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| -0.218 | 0.134 | Original | nan |  | municipio_efipem_esc_efipem_log_impuestos_pc | municipio_efipem | escalonado | log_impuestos_pc | -1 |
| 0.732 | 3.399 | C-LF | DeltaRM | 0.000 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| 0.261 | 4.340 | C-LF | DeltaRM | 0.250 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| -0.680 | 5.595 | C-LF | DeltaRM | 0.500 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| -3.033 | 8.105 | C-LF | DeltaRM | 1.000 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| -5.543 | 10.771 | C-LF | DeltaRM | 1.500 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| -8.210 | 13.438 | C-LF | DeltaRM | 2.000 | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| 0.644 | 3.486 | Original | nan |  | municipio_eic_esc_eic_pct_hog_programas | municipio_eic | escalonado | pct_hog_programas | -1 |
| -3.132 | 0.797 | C-LF | DeltaRM | 0.000 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -3.394 | 0.884 | C-LF | DeltaRM | 0.250 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -3.656 | 0.971 | C-LF | DeltaRM | 0.500 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -4.354 | 1.233 | C-LF | DeltaRM | 1.000 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -5.227 | 1.582 | C-LF | DeltaRM | 1.500 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -6.013 | 2.019 | C-LF | DeltaRM | 2.000 | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -3.153 | 0.817 | Original | nan |  | municipio_eic_esc_eic_pct_negocio | municipio_eic | escalonado | pct_negocio | -1 |
| -1.102 | 1.961 | C-LF | DeltaRM | 0.000 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -7.784 | 8.921 | C-LF | DeltaRM | 0.250 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -15.858 | 16.995 | C-LF | DeltaRM | 0.500 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -32.284 | 33.422 | C-LF | DeltaRM | 1.000 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -48.432 | 49.848 | C-LF | DeltaRM | 1.500 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -64.858 | 65.996 | C-LF | DeltaRM | 2.000 | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |
| -1.329 | 2.188 | Original | nan |  | municipio_enoe_esc_enoe_pct_negocio | municipio_enoe | escalonado | pct_negocio | -1 |

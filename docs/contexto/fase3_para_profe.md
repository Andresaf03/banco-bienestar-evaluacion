# Avance para el martes 13: delitos y elecciones (fase 3)

**Pregunta.** Además del efecto financiero (nulo informativo) y del DENUE (+10% que leemos como
medición), ¿la primera sucursal del Banco del Bienestar cambió la **seguridad** o el **voto** del
municipio? Hay dos mecanismos propuestos:

- el efectivo de los programas sociales que se retira en la sucursal;
- la presencia militar y de la Guardia Nacional alrededor de una obra de la SEDENA.

**Diseño (preregistrado el 11 de octubre, antes de estimar; fuera de las familias del texto
principal).**

| | Delitos (SESNSP) | Elecciones (INE) |
|---|---|---|
| Datos | Carpetas de investigación municipales, 2015–2025 (metodología única; la nueva empieza en 2026) | Diputados federales de MR por casilla: 2015, 2018, 2021, 2024 |
| Unidad y periodo | Municipio × trimestre, 2019T1–2025T4 | Municipio × elección |
| Tratamiento | Escalonado, el mismo G que el bloque financiero | Una cohorte: primera sucursal entre las elecciones de 2021 y 2024 |
| Muestra | 1,457 tratados contra 499 | 1,375 contra 458 |
| Resultados | Robo a transeúnte (principal), robo a negocio, extorsión, robo total, homicidio doloso; placebo de denuncia: daño a la propiedad | Participación y voto Morena + PT + PVEM (composición fija); Morena sola y nulos |
| Estimador | CS DR, aún no tratados, cluster municipal | CS DR, ATT(2024), placebos 2015→18 y 2018→21; TWFE con efectos fijos estado × elección |

**Resultados preliminares.**

- **Delitos: sin efecto detectable, pero no informativo.**
  - Los previos son planos (Wald p entre 0.13 y 0.89) y todos los efectos son ≈ 0: robo a
    transeúnte −0.2%, homicidio +0.1%, robo total −0.1%.
  - Los intervalos al 90% no descartan cambios de 12% a 50% de la media. Robo a negocio da −22%
    (p = 0.10; Romano–Wolf 0.36).
  - El placebo de denuncia no se mueve.
- **Elecciones: la pre-prueba falla → descriptivo.**
  - Antes de 2021, los municipios que después recibieron sucursal ya cambiaban distinto: −5.0
    puntos de participación en 2015→2018 y +3.6 en 2018→2021.
  - Si se resta la media de cada estado en cada elección, los previos se aplanan y la participación
    queda dentro de ±4.5%. Pero el TWFE con efectos fijos estado × elección cambia de signo.
  - No hay efecto electoral identificado.
- **Ubicación (descriptivo).** Dentro del estado, donde el bloque tuvo más voto en 2018 la sucursal
  abrió un poco antes: 0.7 meses por desviación estándar, frente a una desviación estándar del
  calendario de 7.9 meses. La población pesa más: 1.8 meses.

**Preguntas para el profesor.**

1. ¿Vale la pena incluir un resultado "no informativo" (delitos) en el apéndice, o es mejor
   reportarlo solo como límite de potencia en Limitaciones?
2. En elecciones la pre-prueba falla con CS, pero pasa cuando restamos la media estado × elección
   (concurrencia con elecciones locales). ¿Es defendible tomar esa variante como principal, o eso
   sería escoger la especificación después de ver los previos? Por eso hoy la dejamos como
   robustez.
3. ¿Hay una fuente de delitos con menos subregistro a nivel municipal que debiéramos preferir, como
   las defunciones por homicidio de INEGI (EDR), para tener al menos un resultado con potencia?
4. Con un diagnóstico de ubicación que muestra un sesgo político pequeño (0.7 meses por desviación
   estándar), ¿cambia en algo la lectura del nulo financiero?
5. ¿Tiene sentido bajar a sección electoral con bandas de distancia (como en el DENUE), dado que a
   nivel municipal la pre-prueba ya falla? No la hicimos por eso.

*Detalle:* `docs/decisiones.md` (preregistro, adenda y filas del 2026-10-11), apéndice "Delitos y
elecciones (fase 3)" del trabajo final y `outputs/tablas/fase3_resumen.csv`.

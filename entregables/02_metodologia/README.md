# Entrega 2: descripción de la metodología

Requisitos (indicaciones del curso, sección III):

- 1 a 2 páginas máximo, a renglón seguido.
- Título y pregunta central.
- Identificación causal y, si hay objetivos predictivos, su implementación, validación y medidas de
  ajuste.
- Modelos con sus expresiones matemáticas, cada símbolo explicado, el subconjunto y las pruebas.
- Qué se aprenderá.
- Heterogeneidad.

Contenido (versión del 2026-10-19, tras los comentarios del equipo):

- Plan solo causal, en futuro y sin resultados. Título y pregunta sobre la **presencia** de la banca
  privada (sucursales), no "actividad financiera". El DENUE salió de esta entrega (queda en el
  trabajo final).
- Muestra explícita (2,456 − 487 − 8 − 4 = 1,457 tratados 2022T1–2024T1 y 500 controles), el
  resultado dicho como tasa, el tratamiento como primera sucursal y θ / θ(e) explicados en palabras.
- Ecuación (1) simplificada: cambio de los tratados menos el cambio esperado en los aún no tratados
  con las mismas covariables (la identificación de Callaway y Sant'Anna); (2) y (3) sin cambios.
- Todo en párrafos, sin listas, para pasarlo a Google Docs.
- Referencias en APA 7: las 13 citadas en el texto, ni una más.

## Generar

```bash
cd entregables/02_metodologia
quarto render metodologia.qmd --to pdf    # metodologia.pdf
quarto render metodologia.qmd --to docx   # metodologia.docx, para Google Docs
```

El PDF y el .docx no se versionan.

## El .docx (para Google Docs)

- **Estilos:** `referencia.docx` copia los del PDF: Lato 11, renglón seguido, carta con márgenes de
  2.5 cm, títulos de sección en negritas negras, sangría de primera línea, texto justificado con
  división de palabras y referencias con sangría francesa.
- **Cómo se construye:** con `referencia_docx.py`, una sola vez o cuando cambie el formato:

  ```bash
  quarto pandoc -o /tmp/pandoc_ref.docx --print-default-data-file reference.docx
  uv run --no-project --with python-docx python referencia_docx.py /tmp/pandoc_ref.docx
  ```

- **Ecuaciones:** las tres numeradas van como imagen (`ecuaciones/ecuacion_{1,2,3}.png`, 300 dpi, a
  tamaño natural de 11 pt), idénticas a las del PDF. Las ecuaciones de varios renglones de Word
  llegan rotas a Docs (el `&` de alineación aparece como texto). Las fórmulas cortas dentro del
  texto van como texto en cursivas con subíndices y superíndices (`texto_matematico.lua`, solo en
  el .docx): Docs agranda el renglón de cada objeto de ecuación, y el texto con formato casi no.
- **Origen de las imágenes:** se generaron con XeLaTeX (`standalone`, `unicode-math`, Lato 11) y
  `pdftoppm -r 300`. Si cambian las ecuaciones del `.qmd`, hay que regenerarlas. Plantilla:
  `\documentclass[11pt,border=6pt]{standalone}`, `\usepackage{unicode-math}`, `\setmainfont{Lato}` y
  el cuerpo `$\displaystyle <ecuación>$\hspace{2em}$(n)$`; el ancho en el `.qmd` es píxeles / 300.

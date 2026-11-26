# Presentación para Ciencia de Datos Aplicada II

Deck de 10 láminas (≤10 min) sobre el mismo proyecto: motivación, pregunta, aperturas, datos,
especificación (Callaway y Sant'Anna), resultados financieros y cierre con acceso al cobro y DENUE.
Formato **.pptx para importar a
Google Slides**, con notas del presentador en cada lámina. Firma: Andrés Álvarez Flores.

```bash
make presentacion-cdaii
```

1. `figuras.py` lee `outputs/tablas/` (no estima nada), el panel municipal y el Marco
   Geoestadístico; dibuja `outputs/figuras/cdaii_*.png` (mapa de aperturas, dos estudios de evento,
   resumen de efectos y la ecuación) y escribe `cifras.json`.
2. `presentacion.js` (pptxgenjs) arma `presentacion_cdaii.pptx` con las figuras y las cifras de
   `cifras.json`: ninguna cifra de resultados se copia a mano. Solo la meta de 2,744 sucursales
   (ASF 2023) está escrita en el script.

Estilo de la propuesta de Inferencia Causal: Lora (títulos) y Source Sans 3 (cuerpo), fondo
`FAFAFA`, azul `0B5FFF`, subrayado corto bajo el título y franja azul abajo, en los *layouts* del
deck. Para que las figuras usen Source Sans 3, la fuente debe estar instalada (en macOS,
`~/Library/Fonts`); si no, matplotlib usa la de omisión y lo avisa.

**Importar a Google Slides:** Archivo → Importar diapositivas (o subir el .pptx a Drive y abrirlo
con Slides). Las notas llegan. Si Slides no reconoce "Source Sans 3", seleccionar todo y asignarla
desde el menú de fuentes.

Requisitos: `uv` y Node ≥ 18. `node_modules/` y el .pptx no se versionan; `make` corre `npm ci`
la primera vez.

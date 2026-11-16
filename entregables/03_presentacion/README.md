# Entrega 3: presentación

Formato (P-13, cerrada el 2026-10-02): **Quarto → reveal.js**, un solo HTML autocontenido
(`embed-resources`), que se abre sin internet en cualquier navegador. Fuente: `presentacion.qmd`.

```bash
make entregables
```

14 láminas: política, pregunta, datos y diseño, primera etapa, banca privada, resumen de efectos,
medición del DENUE, +10% del DENUE, tres pruebas, heterogeneidad, robustez y conclusiones. Las
tablas se incluyen desde `entregables/_tablas/` y las figuras desde `outputs/figuras/`. Para
exportar a PDF: abrir el HTML, agregar `?print-pdf` a la URL e imprimir desde el navegador.

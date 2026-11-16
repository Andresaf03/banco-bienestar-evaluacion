# Entrega 4: trabajo final

Formato (P-13, cerrada el 2026-10-02): **Quarto → PDF**. Fuente: `trabajo_final.qmd`.

```bash
make entregables
```

Regenera las figuras (`analisis/09_figuras_entregables.R`), las tablas en Markdown
(`src/proyecto/utils/entregables.py` → `entregables/_tablas/`) y renderiza el PDF y la presentación.
Ninguna cifra de las tablas se copia a mano: salen de `outputs/tablas/`. Las cifras en el texto sí
están escritas a mano; si la batería cambia, hay que revisarlas contra las tablas.

- `trabajo_final.qmd`: el documento (≈13 páginas con referencias y apéndice).
- `resultados_preliminares.md`: reporte completo de la batería (`make reporte`), con todas las
  especificaciones, robustez, HonestDiD, heterogeneidad y balance; sirve de anexo.
- El PDF renderizado no se versiona (`.gitignore`).

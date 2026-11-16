# Entrega 1: propuesta

Requisitos de la entrega (formato del documento **por decidir**: ver `docs/decisiones.md` P-13):

1. **Título.**
2. **Pregunta de investigación.** ¿Qué efecto tuvo el Plan de Expansión del Banco del Bienestar
   (aperturas escalonadas 2021–2024) sobre la actividad financiera no pública de los municipios?
   ¿La primera sucursal atrajo o desplazó a la banca múltiple y a las EACP?
3. **Mérito intelectual.** Borrador de argumentos en `docs/contexto/investigacion_1.md` §4: no existe
   evaluación de impacto del plan (ASF e IMCO fiscalizan, no evalúan); primera evaluación de una
   expansión pública masiva y escalonada en México con datos administrativos municipales; extiende
   Fonseca y Matray (2024) a un banco público que no da crédito; estimador robusto a heterogeneidad.
4. **Diseño del análisis.** Panel municipio-trimestre, Callaway y Sant'Anna (2021), tratamiento =
   primera sucursal de banca de desarrollo en la BDIF, control = aún no tratados, resultados sin
   Banco del Bienestar. Resumen en `CLAUDE.md`; parámetros en `config/parametros.yaml`.
5. **Fuentes de datos.** `config/fuentes.yaml` y `docs/contexto/bases-de-datos.md`; estado y
   limitaciones en `docs/data_audit.md` (en particular P1: contratos por sector solo desde 2022T4).

Insumos ya disponibles: figura de cohortes (`outputs/figuras/cohortes.png`), tabla de balance
preliminar (`docs/data_audit.md` P6), referencias en APA (`docs/contexto/referencias.md`).

Cifras verificadas en los datos (2026-09-15) para citar en la propuesta:
- 2,478 municipios (MG 2024); 2,475 observados en la BDIF; 40 trimestres 2016T1–2025T4.
- Tratamiento neto de Banjército (`sucursales_bienestar.parquet`): 487 municipios ya tenían sucursal
  (Bansefi) en 2019T1, 1,482 reciben la primera en 2019T2–2024T4 (casi todas 2022T1–2024T1), 502 nunca.
- 1,516 municipios (62%) sin banca múltiple en 2019T1; 1,219 sin ninguna sucursal.
- Resultados por sector: sucursales en todo el panel; contratos, cajeros, TPV y transacciones por
  sector solo desde 2022T4 (antes "Banca" = múltiple + desarrollo). Población adulta CNBV = 15+.
- El directorio del Banco del Bienestar no tiene fechas: las aperturas se fechan con la BDIF.

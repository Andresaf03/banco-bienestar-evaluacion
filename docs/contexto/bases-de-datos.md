# Bases de datos — Proyecto Banco del Bienestar

Evaluación del Plan de Expansión del Banco del Bienestar (sep 2021 – feb 2024) sobre la actividad financiera municipal. Panel municipio-trimestre, 2019T1–2024T4.

---

## 1. CNBV — Base de Datos de Inclusión Financiera (BDIF)

**La fuente central. Es la única indispensable.**

- **Qué trae:** sucursales, corresponsales, cajeros automáticos, terminales punto de venta, contratos de captación, contratos de crédito, contratos de banca móvil, transacciones en cajeros y TPV, brechas de género.
- **Desagregación:** estatal y municipal (~2,470 municipios), por tipo de institución: banca múltiple, banca de desarrollo, SOCAP y SOFIPO.
- **Frecuencia:** trimestral, desde 2009.
- **Link:** https://www.gob.mx/cnbv/acciones-y-programas/bases-de-datos-de-inclusion-financiera
- **Uso en el diseño:**
  - *Tratamiento:* primer trimestre en que el municipio registra sucursal de banca de desarrollo.
  - *Resultados:* contratos de crédito y captación por cada 10 mil adultos, TPV y transacciones, **restringidos a banca múltiple y EACP** para evitar el efecto mecánico del propio Banco del Bienestar.
- **Verificar primero:** que la desagregación por tipo de institución permita separar banca de desarrollo del resto en las variables de resultado. Si no lo permite, el diseño cambia.
- **Nota:** la base suele incluir la población adulta usada como denominador. Confirmarlo antes de bajar CONAPO.

Documento de apoyo para entender el diccionario antes de descargar:
https://www.cnbv.gob.mx/Inclusi%C3%B3n/Anexos%20Inclusin%20Financiera/ReporteTrimestralBDIF_202303.pdf

---

## 2. Banco del Bienestar — Ubicación de sucursales

- **Qué trae:** domicilio y georreferencia de cada sucursal.
- **Frecuencia:** foto del trimestre vigente, **no serie histórica**.
- **Link:** https://www.datos.gob.mx/dataset/sucursales
- **Uso:** validar municipio y georreferencia. **No sirve para fechar aperturas**; las fechas de tratamiento salen del conteo trimestral de la BDIF.
- Consulta web complementaria: https://directoriodesucursales.bancodelbienestar.gob.mx/
- Mapa interactivo: https://programasparaelbienestar.gob.mx/mapa-banco-del-bienestar-sucursales-retiros/

---

## 3. CONAPO — Índices de marginación 2020

- **Qué trae:** índice y grado de marginación por municipio, más los indicadores socioeconómicos que lo componen.
- **Corte:** 2020, con base en el Censo. Comparable hacia atrás con 2015 y 2010.
- **Link:** https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372
- **Espejo en datos abiertos:** https://www.datos.gob.mx/dataset/indices_marginacion
- **Uso:** emparejamiento de municipios y análisis de heterogeneidad.

---

## 4. CONAPO — Proyecciones de población municipal

- **Qué trae:** población por municipio, sexo y grupos quinquenales de edad, 1990–2040.
- **Link:** https://www.datos.gob.mx/dataset/proyecciones-de-poblacion
- **Nota metodológica:** https://www.gob.mx/conapo/articulos/reconstruccion-y-proyecciones-de-la-poblacion-de-los-municipios-de-mexico
- **Uso:** denominadores para las tasas por cada 10 mil adultos. **Solo si la BDIF no lo trae ya.**

---

## 5. INEGI — Censo de Población y Vivienda 2020

- **Uso:** covariables municipales de línea base (población, urbanización, escolaridad, acceso a servicios).
- Opcional si el índice de marginación de CONAPO ya cubre lo necesario.

---

## 6. INEGI y CNBV — ENIF 2018, 2021 y 2024

- **Qué trae:** tenencia y uso de productos financieros a nivel de persona.
- **Desagregación:** nacional, regional y por tamaño de localidad. **No municipal.**
- **Frecuencia:** trienal.
- **Link:** https://www.gob.mx/cnbv/acciones-y-programas/medicion-de-inclusion-financiera
- **Reporte 2024:** https://www.cnbv.gob.mx/Inclusi%C3%B3n/Anexos%20Inclusin%20Financiera/Reporte_ENIF2024.pdf
- **Uso:** validación descriptiva a nivel de personas. **No entra en la estimación**, porque no se puede aparear a municipios tratados.

---

## Documentos de lectura (no son bases)

| Documento | Para qué sirve | Link |
|---|---|---|
| ASF, Auditoría 2022-0018-A | Evidencia de que lo existente es fiscalización, no evaluación | https://www.asf.gob.mx/Trans/Informes/IR2022c/Documentos/Auditorias/2022_0018_a.pdf |
| IMCO, "Banco del Bienestar a la deriva" | Opacidad en criterios de ubicación; argumento de identificación | https://imco.org.mx/banco-del-bienestar-a-la-deriva/ |
| Programa Institucional 2020-2024 | Población objetivo declarada del programa | https://sidof.segob.gob.mx/notas/docFuente/5612609 |
| CNBV, Impacto de los corresponsales bancarios | Antecedente metodológico con la misma base | https://www.cnbv.gob.mx/CNBV/Estudios-de-la-CNBV/Estudios%20de%20investigacion/Impacto_Corresponsales_Bancarios.pdf |

---

## Checklist de descarga

- [ ] BDIF trimestral, 2019T1 a 2024T4
- [ ] Confirmar que hay desagregación por tipo de institución en captación y crédito
- [ ] Confirmar si la BDIF trae población adulta (denominador)
- [ ] Sucursales del Banco del Bienestar (georreferencia)
- [ ] Índice de marginación 2020
- [ ] Proyecciones municipales de población (solo si hace falta)
- [ ] Censo 2020 (covariables)

## Riesgos conocidos de los datos

1. **Efecto mecánico.** Si las cuentas del propio Banco del Bienestar quedan dentro de la variable de resultado, el efecto estimado no significa nada: el banco dispersa transferencias sociales, así que sus cuentas suben por construcción.
2. **Cambio de metodología en corresponsales.** A partir de 2019T1 la CNBV modificó cómo determina el número máximo de módulos por administrador de corresponsal. Cuidado al usar corresponsales como resultado o control en series que crucen ese corte.
3. **Ubicación no aleatoria.** El plan priorizó municipios marginados y sin banca, pero IMCO documenta que los criterios no fueron transparentes y que los 26 municipios con mayor pobreza quedaron sin sucursal. Esto ayuda al argumento de identificación, pero hay que tratarlo explícitamente.
4. **Sin serie histórica de sucursales.** El único registro trimestral de aperturas es el conteo de la BDIF.

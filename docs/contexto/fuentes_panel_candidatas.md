# Fuentes panel candidatas para fortalecer la evaluación

Exploración del 7 de octubre de 2026. **Todo lo que no diga otra cosa se consultó ese día.** El
análisis sigue cerrado: este documento solo evalúa fuentes. No se tocaron código, configuración,
datos ni git.

## Objetivo y método

**Objetivo.** Encontrar paneles de municipio o localidad con datos antes y después de las aperturas
de 2022–2024 que ataquen los huecos de `GUIA.md` §8, §11 y §12:

1. **El +10% del DENUE.** No tiene dosis, es de zona y no aparece en los CE municipales. Falta una
   medida continua de actividad que no dependa de las actualizaciones del padrón.
2. **Fechas de obra o apertura por sucursal.** No existen; las localidades con `fecha_ambigua`
   salen.
3. **Validez externa.** Salen los ya tratados y no hay comparación con microdatos de personas, que
   es como trabajan Bruhn y Love.
4. **Mecanismo.** ¿El banco operó como red de dispersión o como intermediario?

**Método.**

- Búsqueda web en modo estándar o extendido.
- Confirmación en la página oficial con WebFetch o con `curl -I`.
- Navegador integrado **solo para leer** las páginas que devuelven 403 o exigen JavaScript.
- Lectura de diccionarios y notas metodológicas.
- Muestras de menos de 5 MB en el scratchpad, en `/private/tmp`.
- Cruce con los municipios tratados de `data/processed/panel_municipio_trim.parquet`, en solo
  lectura: 1,470 con `G > 0` y sin ya tratados, antes de los filtros de cohorte; 499 nunca
  tratados.

**Transparencia.**

- *EFIPEM:* para contar su cobertura se leyeron por *streaming* cuatro archivos anuales completos,
  unos 18 MB comprimidos en total, sin guardarlos. Cada uno pesa menos de 5 MB, pero la suma
  rebasa el límite pedido.
- *Zenodo:* respondió 429 (límite de peticiones) en la segunda lectura remota de un GeoTIFF.
- *Wayback Machine:* estuvo caído en los primeros intentos.
- *Muestras:* la lista completa está en §8.

**Discrepancia.** El encargo dice que `docs/decisiones.md` documenta el descarte de VIIRS por exigir
cuenta de Earthdata. **No aparece en ningún archivo del repo**: grep de `viirs`, `earthdata`,
`luz nocturna` y `nightlight`, sin resultados. Se evaluó desde cero (ficha A3).

---

## Resumen

| # | Fuente | Nivel y clave | Periodos útiles | Acceso | Hueco | Horas | Prioridad |
|---|---|---|---|---|---|---|---|
| A1 | INEGI, EIC 2015 + Censo 2020 (ampliado) + EIC 2025 | Municipio, CVEGEO de 5 dígitos | 2015, 2020 → 2025 | Automática (microdatos) | 1, 3, 4 | ~11 | **A** |
| A3 | VIIRS VNL V2 anual (Zenodo, sin cuenta) | Ráster de 500 m → localidad o anillo | 2012–2024 anual | Automática (COG, CC-BY) | 1 | ~9 | **A** |
| T4 | CNBV, Portafolio: modelo Power Pivot ya descargado | Municipio × institución × mes | 2016–2026 (por confirmar) | Ya en `data/raw`; extracción NO VERIFICADA | 2 | 3 (prueba) + 3 | **B** (con tope de horas) |
| M3 | INEGI, ENOE (microdatos con `mun`) | Municipio (persona → agregado) | Trimestral 2019–2026 | Automática | 3, 1 | 15–18 | B |
| M6 | INEGI, EFIPEM municipal | Municipio, CVEGEO | Anual 1989–2024 (2025 preliminar) | Automática | 1 (proxy) | 7–8 | B |
| M2 | INEGI, ENIGH (`ubica_geo`) | Municipio (muestra rotativa) | 2018, 2020 → 2022, 2024 | Automática | 3, 4 | ~12 | C |
| M7 | SEP, formato 911 por escuela | Localidad (`cv_loc`) | Ciclos 2019-20 a 2024-25 | Mixta (básica: descarga manual) | 4 | ~8 | C |
| A4 | INEGI, VMRC | Municipio, CVEGEO | Anual 1980–2025 | Automática | 1 (proxy) | ~5 | C |
| M5 | SESNSP, incidencia municipal | Municipio | Mensual 2015–2025 (ruptura en 2026) | Descarga manual (SharePoint) | 4 | ~6 | C |
| M8 | CONEVAL, pobreza municipal | Municipio | 2010, 2015, 2020 (2025 pendiente) | Automática | covariable | 1–2 | C |
| M1 | Padrones del Bienestar (PUB, becas) | Estado; becas por estado y trimestre | Desde 2021 | Mixta | 4 | — | C / descartar |
| A5 | Google Open Buildings 2.5D Temporal | Ráster de 4 m | 2016–2023 | GCS, cuenta NO VERIFICADA | 1 | >15 | Trabajo futuro |
| A2 | CFE: usuarios y consumo | Nacional (datos abiertos) | 2016–2025 mensual | — | — | — | Descartar |
| M4 | IFT, BIT | Municipio (internet fijo) | — | Dominio caído | — | — | Descartar por ahora |
| T1 | Directorio histórico de sucursales | Sucursal | Solo enero 2021 y 2026T1 | Wayback / datos.gob.mx | 2 | — | Descartar |
| T2 | SHCP, cartera de inversión y Cuenta Pública | Lotes de 72–115 sucursales | 2020–2024 | Automática | 2 | — | Descartar |
| T3 | PNT, SEDENA, comunicados | Sucursal (si se pide) | — | Captcha; solicitud tarda 20 días hábiles | 2 | — | Trabajo futuro |

Las horas incluyen descarga, limpieza, panel, preregistro, estimación y texto. Son estimación propia.

---

## 1. Fecha de tratamiento (hueco 2)

### T1. Versiones históricas del directorio de sucursales — descartar

- **Institución y URL.** Banco del Bienestar en datos.gob.mx,
  <https://www.datos.gob.mx/dataset/sucursales> (navegador, solo lectura).
- **Nivel y clave.** Sucursal con coordenadas; sin fecha de apertura.
- **Cobertura verificada.**
  - *datos.gob.mx:* un solo recurso, "Directorio de Ubicaciones (1er. trim. 2026)", con el conjunto
    creado el 6 de enero de 2026 y actualizado el 14 de julio de 2026. No hay versiones anteriores.
  - *Wayback Machine (API CDX):*
    - `repodatos.atdt.gob.mx/api_update/babien/*` solo tiene capturas de 2026
      (`Directorio_Sucursales_BABIEN.csv`, 7 de enero de 2026).
    - El buscador `directoriodesucursales.bancodelbienestar.gob.mx` tiene capturas de 2022 a 2026,
      pero es un formulario: la lista sale por POST a `conx/MunAlc.php` (código en `Scripts/suc-ent.js`
      de la captura del 15 de agosto de 2022) y Wayback no guarda esas respuestas.
    - En gob.mx hay páginas de "directorio de sucursales" de 2020 y 2021 que enlazan archivos
      mensuales de Bansefi (`bansefi.gob.mx/trans1/DIRECTORIOS DE SUCURSALES 2020/...xlsx`). Esos
      archivos no están archivados y el servidor responde 503.
    - El único archivo recuperable es `DIRECTORIO_ENERO_2021.pdf` (captura del 14 de febrero de
      2024, 171 KB). Es anterior a la expansión y redundante con el Portafolio CNBV, que llega a
      2021-12 por localidad.
- **Veredicto.** No hay fotos públicas del directorio entre 2022 y 2024. La limitación de §11 se
  mantiene.

### T2. SHCP: cartera de inversión y Cuenta Pública — descartar

- **URLs.**
  - Cuenta Pública 2023, tomo VII:
    <https://www.cuentapublica.hacienda.gob.mx/work/models/CP/2023/tomo/VII/Print.6HJO.04.INVREECI.pdf>.
  - Cuenta Pública 2022:
    <https://www.cuentapublica.hacienda.gob.mx/work/models/CP/2022/tomo/VII/MAT_Print.6HJO.03.AEPE_A.pdf>.
- **Qué hay.**
  - Hay 40 proyectos de inversión del Banco del Bienestar, por 16,228.7 millones de pesos.
  - Los proyectos de sucursales son **lotes de 72 a 115 sucursales**, según los resultados de
    búsqueda (portafolios de la SHCP replicados en un portal de Nayarit; NO VERIFICADO en el
    documento fuente). En los dos PDF leídos no hay localidad ni fecha por sucursal.
  - La Cuenta Pública 2023 dice textualmente que no se reportó avance financiero en obra civil de
    los 39 proyectos por falta de documentación de la SEDENA.
- **Veredicto.** No fecha sucursales.

### T3. PNT, SEDENA y comunicados — trabajo futuro

- **PNT.** El buscador <https://buscador.plataformadetransparencia.org.mx> pide **captcha**. Se
  anota como descarga manual y no se insistió.
- **Comunicados.** El Banco del Bienestar publica comunicados de inauguración con cifras agregadas.
  Por ejemplo, una galería de gob.mx titulada "Inaugura Banco del Bienestar 214 nuevas sucursales,
  ya hoy operan 1,223 en todo el país" (captura de Wayback del 13 de febrero de 2024; fecha de
  publicación NO VERIFICADA). No sirven para fechar por sucursal.
- **Salida.** Pedir por solicitud de información la lista de sucursales con fecha de término de obra
  y de inicio de operaciones. El plazo legal de respuesta (20 días hábiles) rebasa el 15 de octubre.

### T4. CNBV, Portafolio de Información: modelo Power Pivot — B, con tope de 3 horas (nueva)

- **Dónde.** `data/raw/cnbv_portafolio/BD_Operativa_202606.xlsx` y `BD_Operativa_202607.xlsx`, ya
  descargados. `docs/data_audit.md:136` los marca como "no se puede leer con herramientas
  abiertas".
- **Qué se encontró (solo lectura).**
  - El libro tiene la hoja "Vista Estado Municipio" y caches de tablas dinámicas con los campos
    `[LT_ubicacion].[descripcion_estado]`, `[LT_ubicacion].[descripcion_municipio]`,
    `[LT_instituciones].[nombre_entidad]`, `[LT_tipo_info_operativa]` y `[FT_datos].[periodo]`.
  - `xl/model/item.data` pesa 3.2 MB y empieza con `STREAM_STORAGE_SIGNATURE_)!@#$%^&*(` +
    `<BackupLog>`: es un respaldo de Analysis Services **sin la compresión XPress9 de los .pbix**.
  - Las cadenas internas incluyen `id_estado_municipio`: el modelo es **municipal**; no se vio un
    campo de localidad.
- **Qué daría.** Altas mensuales de sucursales del Banco del Bienestar **separadas de Banjército**
  de 2022 a 2026. Eliminaría la extrapolación de Banjército (P-8) y daría G mensual en vez de
  trimestral. **No** da obra ni localidad.
- **Acceso.** Hay dos vías, las dos NO VERIFICADAS:
  - Extraer el VertiPaq con un lector de ABF; `pbixray` lo hace para .pbix y habría que saltar la
    descompresión.
  - Abrir el libro en Excel para Windows con Power Pivot y exportar `FT_datos`.
- **Riesgo.** Puede no funcionar; con el tope de 3 horas el costo queda acotado. Si funciona, el
  efecto esperado en los resultados es nulo, porque P-8 ya se probó sin cambios.

---

## 2. Actividad continua (hueco 1)

### A1. INEGI: EIC 2015 + Censo 2020 (cuestionario ampliado) + EIC 2025 — **A**

**No hay Conteo 2025.** El INEGI levantó en su lugar la **Encuesta Intercensal 2025**.

- **Institución y URLs.**
  - Programa: <https://www.inegi.org.mx/programas/eic/2025/>.
  - Comunicado 54/26 del 22 de septiembre de 2026:
    <https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/ei/EIC2025-def_CP.pdf>.
  - Microdatos: `https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_{00..32}_{csv,dta,sas,sav}.zip`
    (nacional CSV: 762 MB).
  - Descriptor: `.../eic2025_micro_fd.xlsx`.
  - Relación de municipios creados de 2020 a 2025: `.../eic2025_micro_nvos_mun.pdf`.
  - EIC 2015: <https://www.inegi.org.mx/programas/intercensal/2015/>, microdatos por estado
    `.../intercensal/2015/microdatos/eic2015_{01..32}_csv.zip` (Aguascalientes 6.8 MB, Oaxaca
    81 MB), descriptor `.../intercensal/2015/doc/eic2015_fd.xls`.
  - Censo 2020, cuestionario ampliado:
    `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_{estado}_csv.zip`.
    Se verificaron `ags` (3.2 MB, revisado) y `eum` (nacional, 486 MB); el resto de las claves
    estatales sigue el patrón de los otros productos del Censo y no se probó.
- **Nivel y clave.**
  - EIC 2025: `CVEGEO` de 5 dígitos, más `CVE_ENT`, `CVE_MUN`, `LOC50K` (solo localidades de 50,000
    y más), `ESTRATO`, `UPM` y `FACTOR`.
  - EIC 2015 y Censo 2020: `ENT` + `MUN`.
  - Representatividad de la EIC 2025: 32 entidades, **2,478 municipios** y localidades de 50,000 y
    más, con una muestra de 7.3 millones de viviendas (comunicado).
- **Periodos.** Censo 2020 (marzo) y EIC 2015 antes; EIC 2025 (6 de octubre a 14 de noviembre de
  2025) después. Son dos previos y uno posterior a todas las aperturas de 2022–2024.
- **Variables, con los mismos mnemónicos en las tres (verificado en los descriptores y en la
  cabecera del Censo 2020 de Aguascalientes).**
  - *Viviendas:* `INGR_AYUGOB` (algún integrante recibe dinero de programas de gobierno),
    `INGR_PEROTROPAIS` (remesas), `INGR_PERDENTPAIS`, `INGR_JUBPEN`.
  - *EIC 2025, además:* `CELULAR`, `INTERNET` y `FINANCIAMIENTO1/2` (crédito de banco para la
    vivienda).
  - *Personas:* `CONACT`, `SITTRA` (2015: `SITUACION_TRAB`; en 2025 el código 5 es cuenta propia,
    sin verificar en 2015), `INGTRMEN`,
    `ACTIVIDADES_C` (SCIAN), `MUN_TRAB` (municipio de trabajo) y `MUN_RES_5A`.
  - **No hay pregunta de cuenta bancaria.**
- **Rupturas.**
  - Ninguna en los mnemónicos.
  - Cambia la lista de ejemplos de programas en la pregunta (2015 cita Prospera y PROCAMPO).
  - La EIC es muestra y el Censo ampliado también. Los municipios nuevos de 2020 a 2025 vienen
    documentados.
- **Formato y acceso.** CSV, descarga automática (HTTP 200 sin bloqueo).
- **Entrada al diseño.** Municipio con una cohorte, igual que los CE:
  - *Tratadas:* abiertas entre 2020 y 2025T3. *Control:* nunca tratados.
  - *Estimando:* 2020→2025. *Placebo:* 2015→2020. *Dosis:* 2022 contra 2023–24.
  - *Resultados:* % de ocupados por cuenta propia y empleadores (el análogo directo de Bruhn y
    Love, independiente del DENUE); % de hogares con programas (mecanismo de dispersión); remesas;
    internet y celular; población 2025/2020 (crecimiento esperado); trabajo en otro municipio
    (reubicación).
- **Limitación de §11 que ataca.**
  - Hueco 1: emprendimiento medido por personas y no por el padrón.
  - Hueco 4: mecanismo.
  - Hueco 3 en parte: microdatos de personas.
- **Horas.** ~11: descarga de ~2.5 GB en las tres fuentes (1 h); agregación ponderada por
  `FACTOR` (3 h); armonización 2015–2025 y municipios nuevos (1 h); preregistro (1 h); estimación
  copiando el patrón de los CE (3 h); texto (2 h).
- **Riesgos.**
  - *Dilución municipal:* los CE municipales ya dan nulo.
  - *Error de muestreo* en municipios chicos: hay que usar `ESTRATO` y `UPM`.
  - *Choque común:* entre 2020 y 2025 los hogares con programas pasaron de **25.0% a 41.4%**
    (comunicado 54/26) por la expansión de pensiones y becas, posiblemente correlacionada con la
    marginación. Hay que condicionar en el índice de marginación de 2020.
  - Hay un solo periodo posterior.

### A2. CFE: usuarios y consumo por municipio — descartar

- **URL.** <https://www.datos.gob.mx/dataset/consumo_final_energia_electrica> (navegador).
- **Qué hay.**
  - "Consumo final de energía eléctrica (2016 a 2025)" es **nacional mensual**: 120 registros,
    columnas `fecha` y `consumo_final_electricidad_gwh`.
  - Es el único conjunto de consumo entre los 9 de la CFE en datos.gob.mx.
  - El CSV (`repodatos.atdt.gob.mx/api_update/cfe/...`) responde 403 a clientes que no son
    navegador.
- **Municipal.** Los anuarios estatales del INEGI y portales estatales (por ejemplo IGECEM,
  2004–2014) traían usuarios por municipio. **No se encontró una serie municipal posterior a 2016**
  (NO VERIFICADO que no exista; requeriría solicitud a la CFE).
- **Veredicto.** Sin datos municipales después de 2022.

### A3. Luz nocturna VIIRS sin cuenta — **A**

- **Cuenta sí exigida (verificado).** `https://eogdata.mines.edu/nighttime_light/annual/v22/`
  redirige (302) a `eogauth.mines.edu` (OpenID). NASA Black Marble y Google Earth Engine también
  piden cuenta.
- **Alternativa sin cuenta (verificada).**
  - *Registro:* Zenodo 17294744 (versión v0.4, 8 de octubre de 2025; DOI conceptual
    10.5281/zenodo.7750174), <https://zenodo.org/records/17294744>, de T. Hengl (OpenGeoHub),
    licencia **CC-BY 4.0**.
  - *Archivos:* `nightlights.average_viirs.v21_m_500m_s_{AAAA}0101_{AAAA}1231_go_epsg4326_v20250904.tif`
    para 2000–2024. **De 2012 a 2024 son los valores observados del VNL V2 anual**, reescalados de
    0–200 a 0–2000. Los de 2000–2011 son extrapolación y no se usan.
  - *Archivo de 2024 (gdalinfo remoto):* Cloud-Optimized GeoTIFF Int16, escala 10, píxel de
    0.00417° (~460 m). El documento de origen es
    `VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average_masked.dat.tif`, es decir, el producto
    de EOG con el fondo enmascarado.
  - *Tamaños:* 59–84 MB por año. Las peticiones por rango funcionan (HTTP 206); se extrajo una
    ventana de Oaxaca de 2019 (120 × 97 píxeles).
- **Nivel y clave.** Ráster; se lleva a localidad con las coordenadas del ITER 2020 (buffers de
  500 m y 1 km) o a anillos con `dist_bb_km`.
- **Periodos.** Anual de 2012 a 2024: siete o más años antes y 2022–2024 después. **No hay 2025.**
- **Rupturas.**
  - Cambio de V2.1 a V2.2 dentro de la serie: NO VERIFICADO en qué año.
  - El enmascarado de fondo deja en 0 a muchas localidades rurales chicas.
- **Formato y acceso.** GeoTIFF COG, descarga automática. **Zenodo limita peticiones (429)**:
  conviene bajar los 9 archivos de 2016–2024 completos (~650 MB) en lugar de lecturas remotas.
- **Entrada al diseño.** Resultado anual por localidad: CS escalonado anual (cohortes 2022 y 2023;
  la de 2024 tiene exposición parcial), bandas de distancia, dosis y placebo de actualización (sin
  actualización censal de por medio).
- **Limitación de §11 que ataca.** Hueco 1 de forma directa: medida continua, local, con gradiente
  y sin depender del DENUE.
- **Horas.** ~9: descarga (1 h); extracción zonal para 69,137 localidades (3 h); panel y
  estimación (2 h); preregistro (1 h); texto (2 h).
- **Riesgos.**
  - *Efecto mecánico:* la sucursal es un edificio iluminado en su propio píxel. Hay que excluir el
    píxel de la sucursal o medir en anillo.
  - Ceros por el enmascarado.
  - Una pre-prueba fallida volvería descriptivo el resultado.

### A4. INEGI, vehículos de motor registrados (VMRC) — C

- **URL.** <https://www.inegi.org.mx/programas/vehiculosmotor/>. Datos abiertos:
  `https://www.inegi.org.mx/contenidos/programas/vehiculosmotor/datosabiertos/conjunto_de_datos_vmrc_anual_csv.zip`
  (4.0 MB, revisado). Publicación reciente: 14 de septiembre de 2026.
- **Nivel y clave.** `CVEGEO` de 5 dígitos, anual de 1980 a 2025 (cifras definitivas).
- **Variables.** Automóviles, camiones de pasajeros, camiones de carga y motocicletas, por
  servicio. Desde 2024 agrega año modelo, energía y origen.
- **Rupturas (metadatos y conteos propios).**
  - Guerrero pasa de 39 a 81 municipios con registro en 2021 y a 85 en 2024.
  - Tlaxcala pasa de 8 a 60 en 2021; Chiapas y Campeche cambian de cobertura.
  - 2022: decreto de regularización de autos usados extranjeros (sube el registro en la frontera).
  - Colima 2023 con corte a abril de 2024; Morelos 2024 reclasifica servicios.
  - Querétaro 2021 cuenta solo unidades sin adeudo.
  - Oaxaca no tiene desglose municipal antes de 2008.
  - El registro se ubica donde está la oficina recaudadora, no donde reside el dueño.
- **Entrada al diseño.** Proxy de riqueza o consumo, como descriptivo o robustez.
- **Horas.** ~5.
- **Riesgo.** Las rupturas por estado se confunden con el tratamiento si las aperturas se
  concentran por estado.

### A5. Google Open Buildings 2.5D Temporal — trabajo futuro

- **URL.** <https://sites.research.google/gr/open-buildings/temporal>.
- **Qué es.** Presencia, conteo fraccional y altura de edificios, **anual de 2016 a 2023**, con
  resolución efectiva de 4 m. Incluye México y es CC-BY 4.0 u ODbL.
- **Acceso.** Bucket de GCS `open-buildings-temporal-data/v1` mediante cuaderno de Colab. La página
  dice que se requiere cuenta de Google; NO VERIFICADO si hay acceso anónimo.
- **Valor.** Podría detectar la propia obra de la SEDENA (65 m²). La página advierte que las
  detecciones no son estables entre años.
- **Veredicto.** Termina en 2023, pesa mucho y el acceso es incierto: fuera de plazo.

---

## 3. Mecanismo, validez externa y covariables (huecos 3 y 4)

### M1. Padrones del Bienestar — C o descartar

- **PUB en datos.gob.mx.** <https://www.datos.gob.mx/dataset/padron_unico_beneficiarios_bienestar>
  trae solo el "Padrón único de beneficiarios **consolidado por entidad**", actualizado el 4 de
  junio de 2025: es estatal y una foto.
- **Portal de consulta.** <https://pub.bienestar.gob.mx/> es una consulta con JavaScript; la
  agregación por municipio y periodo es NO VERIFICADA.
- **Becas Benito Juárez.**
  - Conjuntos por año y programa en datos.gob.mx (S072, S311 y S283), con archivos **por estado y
    trimestre**. Por ejemplo `S072_EDO_01_Aguascalientes_4to_Trim2022.csv` en
    `repodatos.atdt.gob.mx/api_update/cnbbbj/...`.
  - Años vistos en el listado: 2021, 2022, 2024, 2025 y 2026.
  - Columnas NO VERIFICADAS: el CSV da 403 y CORS bloquea la lectura desde el navegador.
- **Dato de mecanismo (verificado).** El comunicado de la CNBBBJ del 1 de febrero de 2023
  (<https://www.gob.mx/cms/uploads/attachment/file/801569/20230201_CNBBBJ_DGOVAC_Comunicado_Bancarizacio_n.pdf>)
  anuncia la **bancarización de los becarios con tarjeta del Banco del Bienestar** a partir de
  febrero de 2023, atendidos solo en meses pares por la capacidad de las sucursales.
- **Veredicto.** Hay a lo más un periodo previo con municipio, y no confirmado. El canal de
  dispersión ya lo mide A1 (`INGR_AYUGOB`) con dos previos.

### M2. ENIGH con `ubica_geo` — C

- **URL.** <https://www.inegi.org.mx/programas/enigh/nc/2024/>. Microdatos:
  `https://www.inegi.org.mx/contenidos/programas/enigh/nc/{2018,2020,2022,2024}/microdatos/enigh{AAAA}_ns_viviendas_csv.zip`
  (1.6–1.8 MB cada uno, revisados).
- **Nivel y clave.** `ubica_geo` de 5 dígitos, más `tam_loc`, `est_dis`, `upm` y `factor`.
- **Cobertura propia (municipios en la muestra / tratados / nunca tratados).**

  | Año | Municipios | Tratados | Nunca tratados |
  |---|---|---|---|
  | 2018 | 996 | 597 | 49 |
  | 2020 | 1,090 | 643 | 78 |
  | 2022 | 1,132 | 678 | 80 |
  | 2024 | 1,112 | 661 | 67 |

  La muestra **rota** entre levantamientos: no es un panel de municipios.
- **Variables.** Ingreso por negocios propios, transferencias por programa e ingreso.
- **Entrada al diseño.** Cortes transversales repetidos con municipio aún no tratado como control
  (2022 contra cohortes 2023–24).
- **Horas.** ~12.
- **Veredicto.** C: A1 cubre lo mismo con más municipios.

### M3. ENOE con municipio — B (validez externa)

- **URL.** <https://www.inegi.org.mx/programas/enoe/15ymas/>. Microdatos trimestrales hasta 2026T2:
  `https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_{AAAA}_trim{T}_csv.zip`
  (2024T4: 43 MB) y `enoe_n_...` para la ENOE^N.
- **Nivel y clave (verificado).** La tabla SDEM trae `loc`, `mun`, `ent`, `ageb`, `upm`, `fac_tri`,
  `pos_ocu`, `tue1-3`, `ingocup`, `scian`, entre otras; cabecera leída por rango HTTP.
- **Cobertura propia.** Municipios en la tabla VIV:
  - 2024T4: 1,028, de ellos **620 tratados** y 34 nunca tratados.
  - 2021T4: 963, de ellos 563 tratados y 36 nunca tratados.
- **Rupturas.**
  - Cambio a ENOE^N en 2020T3; levantamiento telefónico (ETOE) en 2020T2.
  - Reemplazo de bases del 27 de mayo de 2025 (nota del zip).
  - Cambios de marco muestral: NO VERIFICADO.
- **Entrada al diseño.** Réplica de Bruhn y Love: dueños de negocio informal, cuenta propia,
  empleo e ingreso, agregados a municipio y trimestre, con CS escalonado y aún no tratados.
- **Horas.** 15–18.
- **Riesgos.** Pocos nunca tratados; ruido en municipios chicos; armonización de ENOE y ENOE^N.

### M4. IFT, Banco de Información de Telecomunicaciones — descartar por ahora

- `bit.ift.org.mx` **no resuelve** (DNS).
- El IFT se extinguió; la Comisión Reguladora de Telecomunicaciones existe desde el 17 de octubre
  de 2025 (Expansión, 14 de octubre de 2025; Wikipedia, "Telecommunications Regulatory
  Commission").
- La prensa reporta que el BIT lleva meses sin actualizarse y quedó repartido en dos sitios.
- Los accesos de internet fijo por municipio existían; la URL vigente es NO VERIFICADA.
- Internet y celular del hogar ya vienen en A1, a nivel municipal.

### M5. SESNSP, incidencia delictiva municipal — C

- **URL.** <https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva>
  (actualizada el 18 de septiembre de 2026).
- **Qué hay.** "2015 - 2025 (Fuero Común - Delitos). Incidencia delictiva municipal" con
  diccionario. Los archivos están en `sspcgob-my.sharepoint.com`: **descarga manual**.
- **Ruptura.** Hay **metodología nueva desde 2026** (RNID) con nota de comparación histórica. La
  ventana 2015–2025 queda dentro de una sola metodología.
- **Subtipo "robo a cuentahabiente".** NO VERIFICADO: el diccionario en Excel Online no se pudo
  leer. Las noticias locales hablan de él, pero no confirman que esté en el catálogo nacional.
- **Veredicto.** Mecanismo indirecto (manejo de efectivo) con conteos raros. C.

### M6. INEGI, EFIPEM municipal — B

- **URL.** <https://www.inegi.org.mx/programas/finanzas/>. Datos abiertos:
  `https://www.inegi.org.mx/contenidos/programas/finanzas/datosabiertos/conjunto_de_datos_efipem_municipal_csv.zip`
  (95.8 MB). Metadatos modificados el 13 de agosto de 2026.
- **Nivel y clave.** `CVEGEO` de 5 dígitos, anual de 1989 a 2025 (2025 preliminar).
- **Columnas.** `ANIO`, `CVEGEO`, `TEMA`, `CATEGORIA`, `DESCRIPCION_CATEGORIA`, `VALOR`,
  `ESTATUS`.
- **Cobertura propia.**

  | Año | Municipios | Con predial | Tratados |
  |---|---|---|---|
  | 2019 | 2,121 | 1,542 | 1,237 |
  | 2021 | 2,225 | — | 1,314 |
  | 2023 | 2,249 | — | 1,322 |
  | 2024 | 2,380 | 1,760 | 1,424 |
  | 2025 (preliminar) | 1,737 | — | 937 |

- **Entrada al diseño.** Ingresos propios (predial, derechos) per cápita como proxy de actividad
  formal local.
- **Horas.** 7–8.
- **Riesgo.** Panel desbalanceado por reporte voluntario; el resultado está lejos del tratamiento.

### M7. SEP, formato 911 por escuela — C

- **URL.**
  <https://www.datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911>.
- **Cobertura.** Ciclos 2019-2020 a 2024-2025 para básica, media superior y superior.
- **Acceso.**
  - Media superior: `.../download/media_superior_2019-2020.csv` en datos.gob.mx, legible (HTTP
    206).
  - Básica: `repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_AAAA-AAAA.csv`, responde 403 →
    **descarga manual**.
- **Nivel y clave (verificado en media superior).** `entidad`, `cv_mun`, `cv_loc`, `escuela` (CCT),
  `alumnos`, `nvo_ing`, `docentes`.
- **Entrada al diseño.** Matrícula por localidad: canal de becas (bancarizadas desde 2023) y proxy
  de población joven.
- **Horas.** ~8.
- **Riesgo.** Solo hay dos ciclos previos completos (2019-20 y 2020-21), con la pandemia en medio.

### M8. CONEVAL, pobreza municipal — C (covariable)

- **URL.** <https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx>,
  disponible.
- **Qué hay.** 2010, 2015 y 2020 comparables. Anexo:
  <https://coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/Concentrado_indicadores_de_pobreza_2020.zip>.
- **2025.** La medición pasó al INEGI por la reforma del 16 de julio de 2025. La pobreza municipal
  2025 se calculará con la EIC 2025; **fecha de publicación NO VERIFICADA** y no publicada al 7 de
  octubre de 2026.
- **Uso.** Covariable 2020 o heterogeneidad; sin periodo posterior todavía.

---

## 4. Ranking final: qué integrar antes del 15 de octubre (≤ 25 h)

| Orden | Fuente | Horas | Qué gana la credibilidad | Qué riesgo agrega |
|---|---|---|---|---|
| 1 | **A1. EIC 2015 / Censo 2020 / EIC 2025** | ~11 | Emprendimiento medido por personas (cuenta propia y empleadores), independiente del padrón: si da nulo, cierra la lectura de que el +10% es padrón o zona; si da positivo con dosis, la reabre. Además mide el canal de dispersión (hogares con programas) y el crecimiento de población 2020–2025, la hipótesis de "se ubicó donde se esperaba crecimiento". | Nivel municipal, como los CE (dilución); un solo posterior; expansión universal de programas en 2024–25; error de muestreo en municipios chicos. |
| 2 | **A3. VIIRS VNL V2 (Zenodo)** | ~9 | La única medida continua por localidad con gradiente de distancia y dosis anual. Prueba directa del hueco 1: si la luz sube solo en 0–2 km desde la apertura, hay actividad real; si no, el +10% queda como artefacto del padrón. | Luz de la propia sucursal (efecto mecánico); ceros en lo rural; no hay 2025; nueva pre-prueba que puede fallar. |
| 3 | **T4. Portafolio CNBV (Power Pivot), con tope de 3 h** | 3 (+3 si funciona) | Fecha G mensual neta de Banjército en 2022+; cierra P-8 y valida el tratamiento. | Puede no extraerse; si se extrae, no cambia resultados (P-8 ya probado). |
| 4 | M3. ENOE | 15–18 | Validez externa y comparación directa con Bruhn y Love. | No cabe con 1 y 2 en el presupuesto; pocos nunca tratados. |
| 5 | M6. EFIPEM | 7–8 | Otra medida anual de actividad formal. | Resultado lejano; panel desbalanceado. |

- **Recomendación.** Integrar 1 y 2 (~20 h) y probar 3 con tope de 3 horas (total ~23 h).
- **ENOE.** Queda como trabajo futuro, salvo que el equipo prefiera validez externa sobre el hueco 1.
  En ese caso, ENOE sustituye a VIIRS.
- **Preregistro.** Cualquier integración se preregistra en `docs/decisiones.md` **antes** de
  estimar: diseño, ventana, controles, estimando, placebo, familia de inferencia y regla de
  descarte. Es el mismo formato de las fases 0 y 1.
- **Texto.** Las cifras del texto de los entregables se escriben a mano y habría que actualizarlas.

---

## 5. Trabajo futuro y descartes

- **Trabajo futuro.**
  - Solicitud de información al Banco del Bienestar o la SEDENA: lista de sucursales con fecha de
    término de obra e inicio de operaciones (T3).
  - Google Open Buildings Temporal (A5).
  - ENOE (M3), ENIGH (M2), SEP 911 (M7), SESNSP (M5).
  - Pobreza municipal 2025 del INEGI cuando se publique (M8).
- **Descartados.**
  - Directorio histórico (T1): no existe para 2022–2024.
  - Cartera de la SHCP (T2): lotes, no sucursales.
  - CFE (A2): no hay datos municipales recientes.
  - BIT del IFT (M4): sitio caído tras la extinción del IFT.
  - Padrones (M1): estatales o sin columnas verificadas; A1 los sustituye.

---

## 6. Hallazgos que cambian o matizan la lectura actual

1. **No hay Conteo 2025, hay EIC 2025, y es solo municipal** (más localidades de 50,000 y más).
   - La hipótesis "las sucursales se ubicaron donde ya se esperaba crecimiento" **no puede
     probarse con población por localidad**.
   - Los denominadores del DENUE por localidad se quedan en el Censo 2020.
   - Sí se puede probar a nivel municipal (A1).
2. **El canal de dispersión creció en toda la ventana.** Hogares con programas: 25.0% (2020) →
   41.4% (2025), según el comunicado 54/26.
   - Refuerza la lectura de "red de dispersión".
   - También advierte que cualquier resultado municipal 2020–2025 con ingreso o consumo puede
     arrastrar la expansión de programas.
3. **Las becas se pagan con tarjeta del Banco del Bienestar desde febrero de 2023.**
   - La primera etapa (+2,412 tarjetas por 10 mil adultos) es, al menos en parte, bancarización
     administrativa de becarios.
   - Encaja con "acceso no es uso" y debería decirse así en la discusión.
4. **El Portafolio CNBV 2026 "ilegible" probablemente sí se puede leer.** Es un respaldo de
   Analysis Services sin la compresión de los .pbix, con tabla municipio × institución × periodo.
   Si se extrae, desaparece la extrapolación de Banjército (P-8). Extracción NO VERIFICADA.
5. **VIIRS ya no requiere cuenta** vía Zenodo (CC-BY, 2012–2024). El descarte previo no está
   documentado en el repo.
6. **No hay fechas públicas por sucursal para 2022–2024** (Wayback, datos.gob.mx, SHCP). La
   limitación "sin fechas de obra" de §11 queda confirmada como dura; solo la resuelve una
   solicitud de información.
7. **Cambios institucionales que afectan fuentes.**
   - El SESNSP cambió de metodología en 2026.
   - El IFT y el CONEVAL se extinguieron; la pobreza municipal 2025 está pendiente en el INEGI.
   - La CFE no publica datos municipales.

---

## 7. Plantilla usada en las fichas

Institución y URL (fecha de consulta) · nivel y clave · frecuencia y cobertura · variables ·
rupturas · formato y acceso · entrada al diseño · limitación que ataca · horas · riesgos.

## 8. Registro de verificación

**Muestras descargadas** en el scratchpad de la sesión, todas de menos de 5 MB y fuera del repo:

| Archivo | Tamaño |
|---|---|
| `censo2020_ca_ags.zip` | 3.2 MB |
| `vmrc_anual.zip` | 4.0 MB |
| `enigh{2018,2020,2022,2024}_viv.zip` | 1.6–1.8 MB c/u |
| `eic2025_fd.xlsx` | 0.13 MB |
| `eic2015_fd.xls` | 0.16 MB |
| `cp2022_aepe.pdf` | 0.40 MB |
| `cp2023_invreeci.pdf` | 0.27 MB |
| `becas_bancarizacion_2023.pdf` | 0.52 MB |
| `vnl_oax_2019.tif` | 24 KB |
| `zenodo_7750174.json` | 23 KB |

**Lecturas por rango o streaming sin guardar.**

- Cabecera de SDEM y tabla VIV de la ENOE 2024T4 y 2021T4: ~1.2 MB cada una.
- Cuatro archivos anuales de EFIPEM: ~18 MB en total (ver la nota de transparencia).
- Cabeceras del formato 911.

**Navegador en solo lectura.** datos.gob.mx (sucursales, CFE, PUB, becas, 911), INEGI (EIC,
Censo, ENIGH, ENOE, VMRC, EFIPEM), PNT (captcha), SESNSP y SharePoint.

**Sin descargas en `data/raw` ni `data/manual`.**

---

## 9. Estado de la integración (fase 2, 7 de octubre de 2026)

Se integraron las cinco fuentes del ranking, preregistradas en `docs/decisiones.md`. Resultados en
`GUIA.md` §16 y en `outputs/tablas/fase2_resumen.csv`.

| Ficha | Estado | Resultado | Lo que la integración enseñó sobre la ficha |
|---|---|---|---|
| T4. Power Pivot del Portafolio | integrada | P-8 cerrada: 99.2% de coincidencia con la BDIF; 9 municipios cambian de G; ATT sin cambio | `pbixray` 0.15.5 lee el modelo directamente: no hizo falta Excel |
| A1. EIC 2015 / Censo 2020 / EIC 2025 | integrada | dueños de negocio −1.2 puntos (ee 1.0), IC90 entre −10% y +1.8%; ocupación e ingreso, nulos informativos; programas +2.1 puntos, descriptivo | el zip nacional del Censo 2020 usa Deflate64 (Python no lo lee): se usan los 32 estatales |
| A3. VIIRS | integrada | sin efecto, pero la pre-prueba falla (salvo por calendario: nulo) | cambio de escala ×10 y de producto (VNL v2.2 de dos satélites) en 2022, píxeles negativos en 2016–2021 y ruido que depende del brillo: no compara bien pueblos con rancherías |
| M6. EFIPEM | integrada | no informativo | — |
| M3. ENOE | integrada | no informativo: 146 tratados contra 12 controles en el panel balanceado | la muestra de municipios rota: solo 367 aparecen en los 27 trimestres; nombres de archivo por era, BOM en 2022T2 y claves `cve_*` desde 2025T3 |

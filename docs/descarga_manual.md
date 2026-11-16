# Descargas manuales

Dos portales del gobierno federal (datos.gob.mx y repodatos.atdt.gob.mx, detrás de Akamai)
responden **403 Access Denied** a cualquier cliente que no sea un navegador, y el servidor de
CONAPO (`conapo.segob.gob.mx`) no respondía al construir el proyecto. Por la regla 5 del proyecto
(no evadir protecciones) esos archivos se bajan a mano con un navegador y se dejan en
`data/manual/<fuente>/`. El código (`python -m proyecto.descarga <fuente>`) intenta primero la
descarga automática y, si falla, registra la copia manual en `data/raw/MANIFEST.csv` con la nota
"descarga manual desde navegador".

Estado actual: las 7 copias manuales ya están en `data/manual/` y registradas en el manifiesto
(hechas el 2026-09-15 desde el navegador integrado de Claude Desktop). Estas instrucciones son para
reproducirlas o actualizarlas.

## 1. Banco del Bienestar — Directorio de sucursales (`babien`)

1. Abrir https://datos.gob.mx/dataset/sucursales en el navegador.
2. En "Directorio de Ubicaciones (1er. trim. 2026)" hacer clic en **Descargar**. El archivo viene de
   `https://repodatos.atdt.gob.mx/api_update/babien/sucursales/sucursalesbabien_1ertrim2026.csv`.
3. Guardar como `data/manual/babien/sucursalesbabien_1ertrim2026.csv` (si el portal publica un
   trimestre nuevo, actualizar `NOMBRE` en `src/proyecto/descarga/babien.py` y `url_recurso` en
   `config/fuentes.yaml`).
4. Correr `make descargar-babien` para registrar el hash.

Verificación: 3,151 líneas (3,150 sucursales + encabezado), 9 columnas
(`nombre_institucion, nombre_sucursal, domicilio, localidad, municipio_alcaldia, entidad, horario_publico, latitud, longitud`).

## 2. CONAPO — Índices de marginación municipal (`conapo_marginacion`)

Oficial (xlsx, servidor caído al construir): página https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372,
enlaces `https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xlsx`,
`IMM_DP2_2015.xlsx`, `IMM_DP2_2010.xlsx`. Si ese servidor vuelve, `make descargar-conapo_marginacion`
los baja solo a `data/raw/conapo_marginacion/`.

Espejo usado (CSV, mismos datos): https://www.datos.gob.mx/dataset/indices_marginacion
1. Descargar "Índice de marginación municipal 2020" → guardar como `data/manual/conapo_marginacion/imm_2020.csv`
   (el portal lo nombra `imm_2020-3.csv`).
2. "Índice de marginación municipal 2015" → `imm_dp2_2015.csv`.
3. "Índice de marginación municipal 2010" → `imm_dp2_2010.csv`.
4. `make descargar-conapo_marginacion`.

Verificación: 2,469 / 2,457 / 2,456 municipios respectivamente. Columnas `CVE_ENT, NOM_ENT, CVE_MUN, NOM_MUN, POB_TOT, ANALF, SBASC, OVSDE, OVSEE, OVSAE, OVPT, VHAC, PL.5000 (o PL_5000), PO2SM, IM_<año>, GM_<año>, IMN_<año>`.
El de 2015 trae BOM UTF-8 y claves con ceros a la izquierda; los otros dos, claves numéricas. La limpieza normaliza ambos.

## 3. CONAPO — Proyecciones de población municipal (`conapo_proyecciones`)

Página: https://datos.gob.mx/dataset/proyecciones-de-poblacion (CC BY 4.0). Descargar y guardar en
`data/manual/conapo_proyecciones/`:

| Recurso en la página | Archivo | Contenido |
|---|---|---|
| "Población a mitad de año por municipio y sexo, grupos quinquenales" | `pobproy_quinq1.csv` | 252,450 filas: municipio × sexo × año 1990–2040, grupos 0–4 … 85+ |
| "Indicadores demográficos para los municipios" | `pobproy_inddemo.csv` | 126,225 filas: municipio × año |
| "Población a mitad de año por municipio, sexo y grandes grupos" | `pobproy_ggrupos.csv` | 252,450 filas: grupos 0–11, 12–29, 30–59, 60+ |

Luego `make descargar-conapo_proyecciones`.

## 4. SESNSP — Incidencia delictiva municipal 2015–2025 (`sesnsp`, fase 3)

- **Página:** <https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva>,
  sección "Metodología 2015-2025", enlace "2015 - 2025 (Fuero Común - Delitos). Incidencia
  delictiva municipal". Lleva al OneDrive del SESNSP (`sspcgob-my.sharepoint.com`, enlace anónimo).
- **Por qué es manual:** SharePoint solo entrega el archivo con la cookie de invitado que da su
  visor web; un cliente sin ella recibe 403. El visor del navegador integrado de la sesión aborta la
  descarga, así que el 2026-10-11, con autorización del equipo, se usó el mismo enlace con
  `&download=1` y la cookie de invitado de esa visita. Fue una sola vez; no está en el pipeline
  automático.
- **Archivo:** `data/manual/sesnsp/Municipal-Delitos-2015-2025_ago2026.zip` (132,308,218 bytes;
  sha256 en `data/raw/MANIFEST.csv`).
  - Contiene `Municipal-Delitos-2015-2025_ago2026.csv`: 361 MB, latin-1, un mes por columna. El
    PDF del SESNSP advierte que no se abra en hoja de cálculo.
  - Contiene también un xlsx por año (2022–2023 con corte jun-26; 2024–2025 con ago-26) y
    `1. PARA_EVITAR_ERRORES_ANTES_DE_SU_USO.pdf`.
- **Diccionario:** `DD_SESNSP_Metodología_Actual.xlsx` (Excel Online, no carga en el visor). Las
  columnas se leen del encabezado del CSV.
- Luego `make descargar-sesnsp` (solo verifica y registra).

## Fuentes automáticas (para referencia)

CNBV BDIF y CNBV Portafolio de Información (`portafolioinfo.cnbv.gob.mx`, lista SharePoint paginada que
el módulo recorre solo), INEGI (MG por rangos HTTP, ITER 2010/2020, API wscatgeo) y literatura se bajan
sin intervención. Si el WAF de la CNBV cambia de criterio (hoy rechaza UA con `python-requests`), el
síntoma es `Bloqueado: 403` en `make descargar-cnbv_bdif`.

## Cómo saber si hace falta una descarga manual

`make descargar` termina con código 1 y un mensaje `Falta data/manual/<fuente>/<archivo>. Descárgalo a mano desde <url>`
cuando falta alguna copia. Todo lo demás (CNBV, INEGI, literatura) es automático.

## Nota sobre el user-agent

Las descargas automáticas usan `proyecto-ITAM-PPII/0.1 (trabajo académico; +mailto:<contacto>)`, con
el correo tomado de la variable de entorno `PROYECTO_CONTACTO` (sin ella, el UA omite el contacto).
El WAF de `cnbv.gob.mx` rechaza cadenas que contienen `python-requests`; por eso el UA no incluye ese
token, pero sigue identificando al proyecto y un contacto. TLS se verifica con el almacén de
certificados del sistema (`truststore`) porque `www.cnbv.gob.mx` no envía la cadena intermedia.

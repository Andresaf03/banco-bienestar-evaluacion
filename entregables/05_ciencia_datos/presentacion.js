// presentacion.js — Deck de Ciencia de Datos Aplicada II (.pptx para importar a Google Slides).
//
// Uso (desde la raíz del repo, después de figuras.py):
//   node entregables/05_ciencia_datos/presentacion.js
//
// Lee las figuras `outputs/figuras/cdaii_*.png` y las cifras de `cifras.json` (las escribe
// figuras.py desde las tablas de la batería): ninguna cifra de resultados se copia a mano. Estilo
// de la propuesta de Inferencia Causal: Lora (títulos) y Source Sans 3 (cuerpo), fondo casi blanco,
// azul 0B5FFF, subrayado corto bajo el título y franja azul inferior. Las notas del presentador
// van en cada lámina. Salida: entregables/05_ciencia_datos/presentacion_cdaii.pptx.

"use strict";

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));

const RAIZ = path.resolve(__dirname, "..", "..");
const FIGURAS = path.join(RAIZ, "outputs", "figuras");
const SALIDA = path.join(__dirname, "presentacion_cdaii.pptx");
const CIFRAS = JSON.parse(fs.readFileSync(path.join(__dirname, "cifras.json"), "utf8"));

const TEMA = {
  name: "Banco del Bienestar CDA II",
  headFontFace: "Lora",
  bodyFontFace: "Source Sans 3",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "404040", lt2: "FAFAFA",
    accent1: "0B5FFF", accent2: "0A2A66", accent3: "6F9BFF", accent4: "A9C4FF",
    accent5: "595959", accent6: "EEF3FF", hlink: "0B5FFF", folHlink: "0A2A66",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625", el tamaño nativo de Google Slides
pres.author = "Andrés Álvarez Flores";
pres.title = "¿Atrajo o desplazó? El Banco del Bienestar y la banca privada";
pres.theme = { headFontFace: TEMA.headFontFace, bodyFontFace: TEMA.bodyFontFace };
const C = pres.SchemeColor;

// --- Layouts ----------------------------------------------------------------------------------

const ANCHO = 10;
const MARGEN = 0.5;
const SUBRAYADO = { x: 0.39, y: 0.86, w: 2.76, h: 0.055 }; // medido en la propuesta
const FRANJA_Y = 5.35;

pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: C.background2 },
  objects: [
    { rect: { x: 0.8, y: 2.62, w: 8.4, h: 0.12, fill: { color: C.accent1 }, line: { type: "none" } } },
    { placeholder: { options: { name: "titulo", type: "title", x: MARGEN, y: 1.35, w: 9, h: 1.15,
      fontSize: 48, bold: true, color: C.text1, align: "center", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "subtitulo", type: "body", x: 1.0, y: 2.9, w: 8, h: 0.9,
      fontSize: 22, color: C.accent5, align: "center", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "autor", type: "body", x: 1.0, y: 4.15, w: 8, h: 0.7,
      fontSize: 16, color: C.accent5, align: "center", valign: "top", margin: 0 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "TITULO",
  background: { color: C.background2 },
  objects: [
    { rect: { ...SUBRAYADO, fill: { color: C.accent1 }, line: { type: "none" } } },
    { rect: { x: 0, y: FRANJA_Y, w: ANCHO, h: 5.625 - FRANJA_Y, fill: { color: C.accent1 },
      line: { type: "none" } } },
    { placeholder: { options: { name: "titulo", type: "title", x: MARGEN, y: 0.2, w: 9, h: 0.64,
      fontSize: 30, bold: true, color: C.text1, align: "left", valign: "bottom", margin: 0 },
      text: "" } },
  ],
  slideNumber: { x: 9.0, y: FRANJA_Y + 0.02, w: 0.75, h: 0.24, fontSize: 10, color: C.background1,
    align: "right", valign: "middle" },
});

// --- Piezas -----------------------------------------------------------------------------------

function tamanoPng(archivo) {
  const b = fs.readFileSync(archivo);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// Imagen a un ancho dado, con la altura que exige su proporción.
function figura(slide, nombre, { x, y, w }) {
  const archivo = path.join(FIGURAS, `${nombre}.png`);
  const { w: pw, h: ph } = tamanoPng(archivo);
  const h = (w * ph) / pw;
  slide.addImage({ path: archivo, x, y, w, h, objectName: nombre, altText: nombre });
  return y + h;
}

function lamina(titulo, seccion) {
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: seccion });
  s.addText(titulo, { placeholder: "titulo" });
  return s;
}

// Cifra grande en azul con su etiqueta debajo.
function cifra(slide, { x, y, w, valor, etiqueta, tamano = 36, alto = 0.75 }) {
  slide.addText(valor, { x, y, w, h: alto, fontSize: tamano, bold: true, color: C.accent1,
    margin: 0, valign: "bottom", isTextBox: true, objectName: `cifra ${valor}` });
  slide.addText(etiqueta, { x, y: y + alto + 0.05, w, h: 0.62, fontSize: 15, color: C.text1,
    margin: 0, valign: "top", isTextBox: true, objectName: `etiqueta ${valor}` });
}

function pie(slide, texto, y = 4.95) {
  slide.addText(texto, { x: MARGEN, y, w: 9, h: 0.3, fontSize: 11, color: C.accent5, margin: 0,
    valign: "middle", isTextBox: true, objectName: "nota al pie" });
}

// --- Láminas ----------------------------------------------------------------------------------

function portada() {
  pres.addSection({ title: "Portada" });
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Portada" });
  s.addText("¿Atrajo o desplazó?", { placeholder: "titulo" });
  s.addText("La expansión del Banco del Bienestar y la banca privada en los municipios de México",
    { placeholder: "subtitulo" });
  s.addText([
    { text: "Andrés Álvarez Flores", options: { breakLine: true } },
    { text: "Ciencia de Datos Aplicada II · ITAM · octubre de 2026" },
  ], { placeholder: "autor" });
  s.addNotes(
    "Este trabajo pregunta qué le pasó a la banca privada cuando el Banco del Bienestar abrió su " +
    "primera sucursal en un municipio. Es un proyecto de datos de punta a punta: junté y limpié las " +
    "fuentes de la CNBV, el INEGI y la CONAPO, construí un panel municipal trimestral y estimé el " +
    "efecto con diferencias en diferencias escalonadas. En diez minutos: la motivación, los datos, la " +
    "especificación y los resultados.");
}

function motivacion() {
  pres.addSection({ title: "Motivación" });
  const s = lamina("Motivación", "Motivación");
  const cols = [
    { valor: CIFRAS.sucursales_2024,
      etiqueta: `sucursales del banco en 2024 (${CIFRAS.sucursales_2019} en 2019)` },
    { valor: CIFRAS.pct_sin_bm_2019, etiqueta: "de los municipios sin banca múltiple en 2019" },
    { valor: "2,744", etiqueta: "sucursales nuevas como meta, construidas por la SEDENA" },
  ];
  const w = 2.75;
  cols.forEach((c, i) => cifra(s, { x: MARGEN + i * (w + 0.375), y: 1.35, w, ...c, tamano: 40,
    alto: 0.85 }));
  s.addText("Su función: pagar programas sociales. Casi no presta.", { x: MARGEN, y: 3.55, w: 9,
    h: 0.5, fontSize: 20, color: C.text1, margin: 0, isTextBox: true, objectName: "funcion" });
  pie(s, "Fuentes: CNBV (BDIF 2019T1 y 2024T4, sin Banjército); ASF (2023).");
  s.addNotes(
    `En 2019 Bansefi se convirtió en el Banco del Bienestar, con ${CIFRAS.sucursales_2019} ` +
    `sucursales. A finales de 2024 tenía ${CIFRAS.sucursales_2024}: la meta era construir 2,744 ` +
    "nuevas, a cargo de la SEDENA, sobre todo donde no había bancos. Y faltaban: en 2019, el " +
    `${CIFRAS.pct_sin_bm_2019} de los municipios no tenía una sola sucursal de banca múltiple. ` +
    "Pero no es un banco comercial típico: casi no presta y su función principal es pagar " +
    "programas sociales. Por eso la pregunta interesante no es si el banco llegó, sino qué le " +
    "hizo al resto del sistema financiero de esos municipios.");
}

function pregunta() {
  const s = lamina("Pregunta", "Motivación");
  s.addText("¿La primera sucursal del banco atrajo o desplazó a la banca privada?", {
    x: MARGEN, y: 1.2, w: 9, h: 0.9, fontSize: 26, color: C.text1, margin: 0, valign: "top",
    isTextBox: true, objectName: "pregunta" });
  const tarjetas = [
    { titulo: "Atracción", texto: "Revela demanda y abre cuentas: la banca privada llega después." },
    { titulo: "Desplazamiento", texto: "Un banco público con cuentas gratuitas compite: la banca privada se retira." },
  ];
  tarjetas.forEach((t, i) => {
    const x = MARGEN + i * 4.65;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 2.35, w: 4.35, h: 1.75, fill: { color: C.accent6 },
      line: { type: "none" }, objectName: `tarjeta ${t.titulo}` });
    s.addText([
      { text: t.titulo, options: { bold: true, color: C.accent1, fontSize: 22, breakLine: true } },
      { text: t.texto, options: { color: C.text1, fontSize: 17 } },
    ], { x: x + 0.3, y: 2.5, w: 3.75, h: 1.45, margin: 0, valign: "top", paraSpaceAfter: 6,
      isTextBox: true, objectName: `texto ${t.titulo}` });
  });
  s.addText("Resultado: sucursales privadas (banca múltiple + EACP) por 10 mil adultos.", {
    x: MARGEN, y: 4.4, w: 9, h: 0.45, fontSize: 17, color: C.text1, margin: 0, isTextBox: true,
    objectName: "resultado" });
  s.addNotes(
    "Hay dos predicciones opuestas. Atracción: una sucursal pública revela que hay demanda, la " +
    "gente abre cuentas y recibe depósitos, y eso puede volver rentable que lleguen bancos o " +
    "cooperativas privadas. Desplazamiento: un banco público con cuentas gratuitas y los pagos de " +
    "los programas compite por los mismos clientes, y la banca privada se retira o deja de crecer. " +
    "Mido la respuesta con las sucursales privadas —banca múltiple más cooperativas y financieras " +
    "populares, las EACP— por cada 10 mil adultos, la única medida por sector que la CNBV publica " +
    "en toda la ventana.");
}

function aperturas() {
  pres.addSection({ title: "Datos y diseño" });
  const s = lamina("Aperturas escalonadas", "Datos y diseño");
  figura(s, "cdaii_mapa_aperturas", { x: 0.35, y: 1.15, w: 6.2 });
  cifra(s, { x: 6.85, y: 1.2, w: 2.65, valor: CIFRAS.n_tratadas,
    etiqueta: "municipios tratados: primera sucursal entre 2022 y 2024" });
  cifra(s, { x: 6.85, y: 2.75, w: 2.65, valor: CIFRAS.n_controles,
    etiqueta: "sin sucursal a 2024T4" });
  s.addText("Fecha: la sucursal en operación (CNBV), no la obra.", { x: 6.85, y: 4.25, w: 2.65,
    h: 0.6, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true,
    objectName: "fecha" });
  const m = CIFRAS.mapa;
  s.addNotes(
    "El tratamiento es escalonado: cada municipio recibe su primera sucursal en un trimestre " +
    `distinto. Los tonos oscuros abrieron antes; los ${m["Ya tenía (Bansefi)"]} municipios en azul ` +
    "marino ya tenían sucursal de Bansefi en 2019 y no entran en la estimación. Casi todos los " +
    `demás abrieron entre 2022 y 2024. Estimo con ${CIFRAS.n_tratadas} municipios tratados y ` +
    `${CIFRAS.n_controles} que no tenían sucursal a finales de 2024 (salen las cohortes de menos de ` +
    "cinco municipios y ocho fechas que podrían ser de Banjército). Un detalle de datos que " +
    "importa: fecho la apertura con la sucursal en operación según la CNBV, no con la obra, porque " +
    "a finales de 2022 había casi el doble de sucursales terminadas que operando.");
}

function datos() {
  const s = lamina("Datos", "Datos y diseño");
  const fuentes = [
    ["BDIF (CNBV)", "sucursales por sector y municipio; 40 trimestres en 4 formatos de Excel"],
    ["Portafolio CNBV", "separa a Banjército de la banca de desarrollo"],
    ["Directorio del banco", `${CIFRAS.sucursales_directorio} sucursales georreferenciadas`],
    ["CONAPO e INEGI", "población, marginación y límites municipales"],
  ];
  s.addText(fuentes.flatMap(([f, d], i) => [
    { text: `${f}: `, options: { bold: true } },
    { text: d, options: { breakLine: i < fuentes.length - 1 } },
  ]), { x: MARGEN, y: 1.2, w: 5.2, h: 3.6, fontSize: 17, color: C.text1, margin: 0,
    valign: "top", paraSpaceAfter: 14, isTextBox: true, objectName: "fuentes" });
  const tiles = [
    { valor: CIFRAS.n_municipios, etiqueta: "municipios en un panel trimestral 2019–2024" },
    { valor: "Reproducible", etiqueta: "Batería principal y fases documentadas en el README" },
  ];
  tiles.forEach((t, i) => cifra(s, { x: 6.3, y: 1.2 + i * 1.75, w: 3.2, ...t }));
  pie(s, "Descargas con hash · Parquet · claves de 5 dígitos, nunca por nombre · pruebas con pytest");
  s.addNotes(
    "La fuente principal es la Base de Datos de Inclusión Financiera de la CNBV: 40 trimestres en " +
    "Excel con cuatro formatos distintos, que normalicé con un lector por formato. El Portafolio de " +
    "la CNBV me deja quitar a Banjército, que la base municipal mezcla con el Banco del Bienestar. " +
    "El directorio georreferenciado del banco confirma en qué municipios hay sucursal: coincide en " +
    "99.9% con la CNBV. Todo " +
    "corre como un pipeline: descargas idempotentes registradas con su hash, datos intermedios en " +
    "Parquet, claves municipales de cinco dígitos sin unir nunca por nombre, más de cien pruebas " +
    "automáticas. El README documenta la batería principal y las fases adicionales. El " +
    `resultado es un panel de ${CIFRAS.n_municipios} municipios por trimestre.`);
}

function especificacion() {
  const s = lamina("Especificación", "Datos y diseño");
  figura(s, "cdaii_ecuacion", { x: MARGEN, y: 1.1, w: 6.0 });
  s.addText("Callaway y Sant'Anna (2021), doblemente robusto", { x: 6.8, y: 1.2, w: 2.7, h: 1.0,
    fontSize: 17, bold: true, color: C.accent1, margin: 0, valign: "top", isTextBox: true,
    objectName: "estimador" });
  const defs = [
    ["Y", "sucursales privadas por 10 mil adultos (denominador fijo)"],
    ["G", "trimestre de la primera sucursal; control: aún no tratados y nunca tratados"],
    ["X", "población, marginación y banca múltiple en 2019"],
    ["Inferencia", `ee agrupados por municipio; nulo informativo si el IC90 cae dentro de ${CIFRAS.sesoi}`],
  ];
  const col = 4.4;
  defs.forEach(([k, v], i) => {
    s.addText([
      { text: `${k}: `, options: { bold: true } },
      { text: v },
    ], { x: MARGEN + (i % 2) * (col + 0.2), y: 3.55 + Math.floor(i / 2) * 0.75, w: col, h: 0.7,
      fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true,
      objectName: `definicion ${k}` });
  });
  s.addNotes(
    "Uso el estimador de Callaway y Sant'Anna, que evita el problema del TWFE con tratamientos " +
    "escalonados: nunca usa como control a un municipio ya tratado. Para cada cohorte g y trimestre " +
    "t compara el cambio de las tratadas desde el trimestre previo a la apertura con el cambio de " +
    "los municipios aún no tratados o nunca tratados. Es doblemente robusto: combina un puntaje de " +
    "propensión y una regresión del resultado con tres covariables, y es consistente si cualquiera " +
    "de los dos modelos es correcto. Después promedio los ATT en un efecto global, theta. Fijé de " +
    `antemano qué cuenta como nulo: que el IC al 90% quede dentro de ${CIFRAS.sesoi} de la media ` +
    `previa, ${CIFRAS.sesoi_nivel} sucursales por 10 mil adultos.`);
}

function primeraEtapa() {
  pres.addSection({ title: "Resultados" });
  const s = lamina("Primera etapa: el banco sí llegó", "Resultados");
  figura(s, "cdaii_evento_primera_etapa", { x: 0.35, y: 1.1, w: 5.6 });
  cifra(s, { x: 6.4, y: 1.15, w: 3.1, valor: `+${CIFRAS.pe_att}`,
    etiqueta: `sucursales por 10 mil adultos (ee\u00a0${CIFRAS.pe_ee}); previos planos` });
  cifra(s, { x: 6.4, y: 2.85, w: 3.1, valor: `+${CIFRAS.tarjetas}`,
    etiqueta: "tarjetas de débito del banco por 10 mil adultos" });
  pie(s, "Estudio de evento, Callaway y Sant'Anna; bandas simultáneas al 95%.");
  s.addNotes(
    "Primero, la primera etapa: ¿el tratamiento cambió algo? Sí. Al abrir, las sucursales totales " +
    `suben ${CIFRAS.pe_att} por cada 10 mil adultos (ee ${CIFRAS.pe_ee}), y los trimestres previos ` +
    `son planos (Wald p = ${CIFRAS.pe_wald_p}), lo que respalda tendencias paralelas. Los últimos ` +
    "trimestres solo los aportan las cohortes de 2022, por eso la banda se ensancha. Además, el " +
    `banco sí bancarizó: ${CIFRAS.tarjetas} tarjetas de débito del banco más por cada 10 mil ` +
    "adultos. Pero su uso sigue el calendario de pago de los programas: alrededor de una " +
    "transacción por tarjeta cada dos meses en sus cajeros.");
}

function bancaPrivada() {
  const s = lamina("Banca privada: sin cambio", "Resultados");
  figura(s, "cdaii_evento_privadas", { x: 0.35, y: 1.1, w: 5.6 });
  cifra(s, { x: 6.4, y: 1.15, w: 3.1, valor: CIFRAS.priv_pct,
    etiqueta: `sucursales privadas (ATT\u00a0${CIFRAS.priv_att}, ee\u00a0${CIFRAS.priv_ee})` });
  cifra(s, { x: 6.4, y: 2.75, w: 3.1, valor: CIFRAS.priv_cota,
    etiqueta: `cota del IC90, dentro de ${CIFRAS.sesoi}: nulo informativo` });
  s.addText(`Banca múltiple ${CIFRAS.bm_pct} · EACP ${CIFRAS.eacp_pct}`, { x: 6.4, y: 4.35,
    w: 3.1, h: 0.4, fontSize: 15, color: C.text1, margin: 0, isTextBox: true,
    objectName: "sectores" });
  pie(s, `Estudio de evento, Callaway y Sant'Anna; bandas simultáneas al 95%. Franja: ${CIFRAS.sesoi} de la media previa.`);
  s.addNotes(
    `El resultado principal. Las sucursales privadas cambian ${CIFRAS.priv_pct} respecto a su ` +
    `media previa: ${CIFRAS.priv_att} sucursales por 10 mil adultos, con error estándar ` +
    `${CIFRAS.priv_ee}. No es significativo, pero lo importante es que es un nulo informativo: el ` +
    `intervalo al 90% queda dentro de ${CIFRAS.priv_cota}, menos de la mitad del umbral de ` +
    `${CIFRAS.sesoi} que fijé antes de estimar. Los previos son planos (Wald p = ` +
    `${CIFRAS.priv_wald_p}). Por sector pasa lo mismo: banca múltiple ${CIFRAS.bm_pct} ` +
    `(${CIFRAS.bm_cota}) y EACP ${CIFRAS.eacp_pct} (${CIFRAS.eacp_cota}). Los puntos de la derecha ` +
    "son ruidosos porque solo los aportan las cohortes de 2022; el efecto global los promedia " +
    "todos. El banco no atrajo ni desplazó sucursales privadas.");
}

function robustez() {
  const s = lamina("¿Aguanta?", "Resultados");
  figura(s, "cdaii_efectos_financieros", { x: 0.35, y: 1.15, w: 6.2 });
  s.addText([
    { text: "Mismo nulo con:", options: { bold: true, breakLine: true } },
    { text: "DiD apilado", options: { breakLine: true } },
    { text: "Sun y Abraham", options: { breakLine: true } },
    { text: "Estudio de evento TWFE", options: { breakLine: true } },
    { text: "Placebo de fecha", options: { breakLine: true } },
    { text: `Permutación (p = ${CIFRAS.perm_p})`, options: {} },
  ], { x: 6.85, y: 1.2, w: 2.7, h: 2.9, fontSize: 16, color: C.text1, margin: 0, valign: "top",
    paraSpaceAfter: 6, isTextBox: true, objectName: "robustez" });
  pie(s, `Efecto en % de la media previa, IC al 90%; franja: ${CIFRAS.sesoi}. † Reprueba la pre-prueba en el DiD apilado.`);
  s.addNotes(
    "¿Depende de la especificación? Casi nada se mueve. La captación y el crédito privados, que la " +
    "CNBV separa por sector solo desde 2022, también son nulos informativos. La excepción es el " +
    `crédito al consumo de las EACP, ${CIFRAS.cred_eacp_pct}, pero reprueba la pre-prueba en el DiD ` +
    "apilado, así que no lo cuento como efecto. Con otros estimadores y con un placebo de fecha el " +
    "nulo se mantiene, y reasignar las fechas al azar dentro de cada estado da p = " +
    `${CIFRAS.perm_p}. Si preguntan: en sucursales privadas, la única especificación que da algo ` +
    `es el TWFE extendido de Wooldridge con covariables, ${CIFRAS.etwfe_cov_pct}, que baja a ` +
    `${CIFRAS.etwfe_abren_pct} con solo los municipios que alguna vez abren. En banca múltiple, el ` +
    `TWFE estático y Borusyak et al. dan ${CIFRAS.bm_twfe_pct} y ${CIFRAS.bm_bjs_pct}, ` +
    `significativos pero dentro de ${CIFRAS.sesoi}: si hay desplazamiento, es pequeño. Por eso una ` +
    "atracción pequeña está menos descartada que el desplazamiento.");
}

function conclusiones() {
  pres.addSection({ title: "Cierre" });
  const s = lamina("Conclusiones", "Cierre");
  const puntos = [
    `El banco acercó el cobro: de ${CIFRAS.acceso_km_2019} a ${CIFRAS.acceso_km_2024} km en promedio para adultos de 65 años o más.`,
    `Banca privada: el intervalo principal al 90% queda dentro de ${CIFRAS.priv_cota}.`,
    `DENUE: ${CIFRAS.denue_pct} en localidades con sucursal. No se distingue entre gasto y medición.`,
  ];
  puntos.forEach((p, i) => {
    const y = 1.3 + i * 1.0;
    s.addText(String(i + 1), { x: MARGEN, y, w: 0.6, h: 0.8, fontFace: TEMA.headFontFace,
      fontSize: 36, bold: true, color: C.accent1, margin: 0, valign: "top", isTextBox: true,
      objectName: `numero ${i + 1}` });
    s.addText(p, { x: 1.2, y: y + 0.08, w: 8.3, h: 0.8, fontSize: 20, color: C.text1, margin: 0,
      valign: "top", isTextBox: true, objectName: `conclusion ${i + 1}` });
  });
  s.addText("Gracias", { x: MARGEN, y: 4.6, w: 9, h: 0.5, fontFace: TEMA.headFontFace,
    fontSize: 22, bold: true, color: C.accent1, margin: 0, align: "right", isTextBox: true,
    objectName: "gracias" });
  s.addNotes(
    `Entre 2019 y 2024, la distancia media para adultos de 65 años o más bajó de ${CIFRAS.acceso_km_2019} ` +
    `a ${CIFRAS.acceso_km_2024} km. Es una medida descriptiva. En la especificación principal, ` +
    `el intervalo al 90% para las sucursales privadas queda dentro de ${CIFRAS.priv_cota}. ` +
    `El DENUE sube ${CIFRAS.denue_pct} en localidades con sucursal en la actualización de 2024. ` +
    "El aumento se concentra cerca de la sucursal, pero las pruebas no distinguen el gasto de los " +
    "programas de cambios de medición. La app muestra los resultados de acceso y del DENUE por radio.");
}

// --- Tema y salida ----------------------------------------------------------------------------

// pptxgenjs escribe la paleta de Office en el tema; aquí se reemplaza por la del deck para que
// los colores de esquema (C.accent1, …) resuelvan al azul y la tinta de la propuesta.
async function aplicarTema(archivo, tema) {
  const zip = await JSZip.loadAsync(fs.readFileSync(archivo));
  const parte = "ppt/theme/theme1.xml";
  const slots = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5",
    "accent6", "hlink", "folHlink"];
  const esquema = `<a:clrScheme name="${tema.name}">` +
    slots.map((k) => `<a:${k}><a:srgbClr val="${tema.colors[k]}"/></a:${k}>`).join("") +
    "</a:clrScheme>";
  const xml = await zip.file(parte).async("string");
  const nuevo = xml.replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => esquema);
  if (!nuevo.includes(esquema)) throw new Error(`${parte} no tiene <a:clrScheme>`);
  zip.file(parte, nuevo);
  fs.writeFileSync(archivo, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function main() {
  portada();
  motivacion();
  pregunta();
  aperturas();
  datos();
  especificacion();
  primeraEtapa();
  bancaPrivada();
  robustez();
  conclusiones();
  await pres.writeFile({ fileName: SALIDA });
  await aplicarTema(SALIDA, TEMA);
  console.log(`deck en ${path.relative(RAIZ, SALIDA)}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

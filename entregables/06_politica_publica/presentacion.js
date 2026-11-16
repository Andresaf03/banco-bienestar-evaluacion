// presentacion.js — Deck de Tópicos de Política Pública II (.pptx para importar a Google Slides).
//
// Uso (desde la raíz del repo, después de figuras.py):
//   node entregables/06_politica_publica/presentacion.js
//
// Lee las figuras `outputs/figuras/ppii_*.png` y las cifras de `cifras.json` (las escribe
// figuras.py desde las tablas de la batería): ninguna cifra de resultados se copia a mano. Tema,
// layouts y piezas copiados del deck de Ciencia de Datos Aplicada II (`05_ciencia_datos/`), para
// que los dos se vean iguales. El diagrama causal y las tablas son formas nativas, editables en
// Slides. Las notas del presentador marcan quién habla en cada bloque y el script falla si las
// notas de la exposición pasan de 1,500 palabras (12 minutos).
// Salida: entregables/06_politica_publica/presentacion_ppii.pptx.

"use strict";

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));

const RAIZ = path.resolve(__dirname, "..", "..");
const FIGURAS = path.join(RAIZ, "outputs", "figuras");
const SALIDA = path.join(__dirname, "presentacion_ppii.pptx");
const K = JSON.parse(fs.readFileSync(path.join(__dirname, "cifras.json"), "utf8"));
const MAX_PALABRAS_NOTAS = 1500;
const DPI = 200; // el de figuras.py: el tamaño natural de una figura es px / DPI pulgadas

const TEMA = {
  name: "Banco del Bienestar PPII",
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
pres.author = "Andrés Álvarez Flores, Fernando Barba y Luis Islas";
pres.title = "¿Atrajo o desplazó? El Banco del Bienestar y la actividad financiera de los municipios";
pres.theme = { headFontFace: TEMA.headFontFace, bodyFontFace: TEMA.bodyFontFace };
const C = pres.SchemeColor;
// La fuente del cuerpo va explícita en cada texto: Slides y PowerPoint resuelven la del tema, pero
// LibreOffice (el render a PDF) no, y sustituye por la de los títulos.
const CUERPO = TEMA.bodyFontFace;

// --- Layouts (los de CDA II) -------------------------------------------------------------------

const ANCHO = 10;
const MARGEN = 0.5;
const SUBRAYADO = { x: 0.39, y: 0.86, w: 2.76, h: 0.055 };
const FRANJA_Y = 5.35;

pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: C.background2 },
  objects: [
    { rect: { x: 0.8, y: 2.62, w: 8.4, h: 0.12, fill: { color: C.accent1 }, line: { type: "none" } } },
    { placeholder: { options: { name: "titulo", type: "title", x: MARGEN, y: 1.35, w: 9, h: 1.15,
      fontSize: 48, bold: true, color: C.text1, align: "center", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "subtitulo", type: "body", x: MARGEN, y: 2.9, w: 9, h: 0.9,
      fontFace: CUERPO, fontSize: 22, color: C.accent5, align: "center", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "autor", type: "body", x: 1.0, y: 4.15, w: 8, h: 0.7,
      fontFace: CUERPO, fontSize: 16, color: C.accent5, align: "center", valign: "top", margin: 0 }, text: "" } },
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

// --- Piezas -------------------------------------------------------------------------------------

function tamanoPng(archivo) {
  const b = fs.readFileSync(archivo);
  return { w: b.readUInt32BE(16) / DPI, h: b.readUInt32BE(20) / DPI };
}

// Figura a su tamaño natural (el texto queda al tamaño con que se dibujó), reducida solo si no
// cabe en `wMax` × `hMax`. Devuelve sus bordes derecho e inferior.
function figura(slide, nombre, { x, y, wMax = 9, hMax = 3.75 }) {
  const archivo = path.join(FIGURAS, `${nombre}.png`);
  const n = tamanoPng(archivo);
  const escala = Math.min(1, wMax / n.w, hMax / n.h);
  const w = n.w * escala;
  const h = n.h * escala;
  slide.addImage({ path: archivo, x, y, w, h, objectName: nombre, altText: nombre });
  return { derecha: x + w, abajo: y + h };
}

function lamina(titulo, seccion) {
  const s = pres.addSlide({ masterName: "TITULO", sectionTitle: seccion });
  s.addText(titulo, { placeholder: "titulo" });
  return s;
}

function texto(slide, contenido, opciones) {
  slide.addText(contenido, { fontFace: CUERPO, fontSize: 17, color: C.text1, margin: 0,
    valign: "top", isTextBox: true, ...opciones });
}

// Cifra grande en azul con su etiqueta debajo.
function cifra(slide, { x, y, w, valor, etiqueta, tamano = 36, alto = 0.75, altoEtiqueta = 0.62 }) {
  slide.addText(valor, { x, y, w, h: alto, fontFace: CUERPO, fontSize: tamano, bold: true,
    color: C.accent1,
    margin: 0, valign: "bottom", isTextBox: true, objectName: `cifra ${valor}` });
  slide.addText(etiqueta, { x, y: y + alto + 0.05, w, h: altoEtiqueta, fontFace: CUERPO,
    fontSize: 15,
    color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: `etiqueta ${valor}` });
}

function pie(slide, contenido, y = 4.95, h = 0.3) {
  slide.addText(contenido, { x: MARGEN, y, w: 9, h, fontFace: CUERPO, fontSize: 11, color: C.accent5, margin: 0,
    valign: "middle", isTextBox: true, objectName: "nota al pie" });
}

// Caja con relleno de tema y texto dentro (tarjetas, chips y recuadros).
function caja(slide, { x, y, w, h, relleno = C.accent6, contenido, opciones = {}, nombre }) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: relleno },
    line: { type: "none" }, objectName: `caja ${nombre}` });
  slide.addText(contenido, { x: x + 0.15, y, w: w - 0.3, h, fontFace: CUERPO, fontSize: 17,
    color: C.text1,
    margin: 0, valign: "middle", isTextBox: true, objectName: `texto ${nombre}`, ...opciones });
}

function flecha(slide, { x1, y1, x2, y2, nombre }) {
  const x = Math.min(x1, x2);
  const y = Math.min(y1, y2);
  slide.addShape(pres.shapes.LINE, { x, y, w: Math.abs(x2 - x1), h: Math.max(Math.abs(y2 - y1), 0.001),
    flipV: y2 < y1, line: { color: C.accent5, width: 1.5, endArrowType: "triangle" },
    objectName: `flecha ${nombre}` });
}

// Número grande en Lora con su texto, como en las conclusiones de CDA II.
function numerado(slide, { x, y, w, numero, contenido, tamano = 20 }) {
  slide.addText(String(numero), { x, y, w: 0.55, h: 0.7, fontFace: TEMA.headFontFace,
    fontSize: 32, bold: true, color: C.accent1, margin: 0, valign: "top", isTextBox: true,
    objectName: `numero ${numero}` });
  slide.addText(contenido, { x: x + 0.6, y: y + 0.07, w: w - 0.6, h: 0.7, fontFace: CUERPO,
    fontSize: tamano,
    color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: `punto ${numero}` });
}

// --- Notas --------------------------------------------------------------------------------------

// Cifra sin el signo, para la prosa ("subieron 7.6%").
const sinSigno = (v) => v.replace(/^\+/, "");
// Valor p con su operador: "p = 0.29" o "p < 0.001".
const pValor = (v) => (v.startsWith("<") ? `p < ${v.slice(1)}` : `p = ${v}`);

const conteoNotas = [];

function contarPalabras(t) {
  return t.split(/\s+/).filter((p) => /[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]/.test(p)).length;
}

function notas(slide, titulo, partes, { respaldo = false } = {}) {
  const t = partes.join(" ");
  slide.addNotes(t);
  conteoNotas.push({ titulo, palabras: contarPalabras(t), respaldo });
}

// --- Láminas: planteamiento (Andrés) ------------------------------------------------------------

function portada() {
  pres.addSection({ title: "Planteamiento" });
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Planteamiento" });
  s.addText("¿Atrajo o desplazó?", { placeholder: "titulo" });
  s.addText("El Banco del Bienestar y la actividad financiera de los municipios",
    { placeholder: "subtitulo" });
  s.addText([
    { text: "Andrés Álvarez Flores, Fernando Barba y Luis Islas", options: { breakLine: true } },
    { text: "Tópicos de Política Pública II · ITAM" },
  ], { placeholder: "autor" });
  notas(s, "Portada", [
    "[Andrés] Evaluamos el Plan de Expansión del Banco del Bienestar: qué le pasó a la banca",
    "privada y a la actividad económica de un municipio cuando abrió su primera sucursal.",
    "Vamos de la política a la pregunta, el diseño, los resultados y lo que implican.",
  ]);
}

function politica() {
  const s = lamina("De Bansefi al Banco del Bienestar", "Planteamiento");
  figura(s, "ppii_sucursales", { x: 0.35, y: 1.12, wMax: 5.7 });
  const x = 6.3;
  const w = 3.2;
  cifra(s, { x, y: 1.1, w, valor: `${K.operando_2022} de ${K.terminadas_2022}`, tamano: 32,
    alto: 0.65, etiqueta: "sucursales terminadas operaban al cierre de 2022" });
  cifra(s, { x, y: 2.55, w, valor: K.pct_sin_bm_2019, tamano: 32, alto: 0.65,
    etiqueta: "de los municipios sin banca múltiple en 2019" });
  texto(s, "Su función: dispersar programas sociales. Casi no presta.", { x, y: 3.95, w, h: 0.75,
    bold: true, objectName: "funcion" });
  pie(s, `Fuentes: CNBV (BDIF, sin Banjército); ASF (2023). Meta del plan: ${K.meta_sedena} ` +
    "sucursales nuevas, construidas por la SEDENA.");
  notas(s, "La política", [
    `En 2019 Bansefi se convirtió en el Banco del Bienestar, con ${K.sucursales_2019} sucursales.`,
    `El plan fue construir ${K.meta_sedena} nuevas, a cargo de la SEDENA, sobre todo donde no`,
    `había bancos; a finales de 2024 operaban ${K.sucursales_2024}. Dos datos condicionan lo que`,
    `sigue. Construida no es operando: al cierre de 2022 había ${K.terminadas_2022} terminadas y`,
    `solo ${K.operando_2022} abiertas, según la Auditoría Superior. Y la red llegó a lugares sin`,
    `banca: en 2019 el ${K.pct_sin_bm_2019} de los municipios no tenía sucursal de banca`,
    "múltiple. Además, el banco casi no presta: su función es dispersar programas sociales. En",
    `${K.periodo_razon} tiene ${K.creditos_100_banco} créditos por cada 100 cuentas.`,
  ]);
}

function pregunta() {
  const s = lamina("Pregunta y mérito", "Planteamiento");
  const preguntas = [
    "¿Atrajo o desplazó a la banca privada?",
    "¿Más en desiertos bancarios?",
    "¿Y la actividad local?",
  ];
  preguntas.forEach((p, i) => numerado(s, { x: MARGEN, y: 1.3 + i * 1.05, w: 5.3, numero: i + 1,
    contenido: p, tamano: 21 }));
  const x = 6.15;
  const w = 3.35;
  texto(s, "Primera evaluación causal", { x, y: 1.15, w, h: 0.4, fontSize: 19, bold: true,
    color: C.accent1, objectName: "merito" });
  const tarjetas = [
    { valor: K.azteca_pct, etiqueta: "Azteca, México" },
    { valor: K.brasil_pct, etiqueta: "Banca pública, Brasil" },
  ];
  tarjetas.forEach((t, i) => {
    const y = 1.7 + i * 1.2;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 1.05, fill: { color: C.accent6 },
      line: { type: "none" }, objectName: `tarjeta ${t.etiqueta}` });
    s.addText([
      { text: t.valor, options: { bold: true, color: C.accent1, fontSize: 30, breakLine: true } },
      { text: t.etiqueta, options: { color: C.text1, fontSize: 16 } },
    ], { x: x + 0.25, y: y + 0.08, w: w - 0.5, h: 0.9, fontFace: CUERPO, margin: 0,
      valign: "middle",
      isTextBox: true, objectName: `contraste ${t.etiqueta}` });
  });
  texto(s, "Ambos prestaban; este no.", { x, y: 4.2, w, h: 0.45, fontSize: 18, bold: true,
    objectName: "contraste" });
  pie(s, "Bruhn y Love (2014): dueños de negocio informal. Fonseca y Matray (2024): empresas y " +
    "empleo.");
  notas(s, "Pregunta y mérito", [
    "Nos hacemos tres preguntas. La principal: ¿la primera sucursal atrajo o desplazó a la banca",
    "privada, es decir, a la banca múltiple y a las cooperativas y financieras populares, las",
    "EACP? Segunda: ¿el efecto fue mayor en los desiertos bancarios? Tercera: ¿cambió la",
    "actividad económica local? La literatura dice que las sucursales importan cuando prestan.",
    `Con las ${K.azteca_sucursales} sucursales de Banco Azteca, los dueños de negocio informal`,
    `subieron ${sinSigno(K.azteca_pct)}. En Brasil, la banca pública prestó y las empresas y el empleo`,
    "subieron cerca de 10%, sin mover a la banca privada. Nuestro aporte: la primera evaluación",
    "causal de este plan, el caso de un banco público que no presta.",
  ]);
}

function historiaCausal() {
  const s = lamina("Historia causal", "Planteamiento");
  caja(s, { x: MARGEN, y: 2.2, w: 1.7, h: 1.0, relleno: C.accent1, nombre: "sucursal",
    contenido: "Primera sucursal",
    opciones: { color: C.background1, bold: true, fontSize: 18, align: "center" } });
  const canales = [
    { nombre: "Atracción", mecanismo: "revela demanda", resultado: "Más sucursales privadas" },
    { nombre: "Desplazamiento", mecanismo: "compite", resultado: "Menos sucursales privadas" },
    { nombre: "Crédito", mecanismo: "", resultado: "Más negocios y empleo" },
  ];
  canales.forEach((c, i) => {
    const y = 1.15 + i * 1.05;
    const centro = y + 0.4;
    const runs = [{ text: c.nombre, options: { bold: true, color: C.accent1, fontSize: 18,
      breakLine: Boolean(c.mecanismo) } }];
    if (c.mecanismo) runs.push({ text: c.mecanismo, options: { fontSize: 15 } });
    caja(s, { x: 2.75, y, w: 2.75, h: 0.8, nombre: c.nombre, contenido: runs });
    caja(s, { x: 6.0, y, w: 3.5, h: 0.8, relleno: C.background1, nombre: c.resultado,
      contenido: c.resultado });
    flecha(s, { x1: MARGEN + 1.7, y1: 2.7, x2: 2.75, y2: centro, nombre: `a ${c.nombre}` });
    flecha(s, { x1: 5.5, y1: centro, x2: 6.0, y2: centro, nombre: `de ${c.nombre}` });
  });
  caja(s, { x: MARGEN, y: 4.4, w: 9, h: 0.65, relleno: C.accent2, nombre: "prediccion",
    contenido: "Si no presta: solo cuentas; privadas y actividad sin cambio",
    opciones: { color: C.background1, bold: true, fontSize: 18 } });
  notas(s, "Historia causal", [
    "¿Por qué esperaríamos algo? Hay tres canales. Atracción: la sucursal abre cuentas y revela",
    "que hay demanda; si eso vuelve rentable el municipio, la banca privada llega después y",
    "veríamos más sucursales privadas. Desplazamiento: un banco público con cuentas gratuitas y",
    "los pagos de los programas compite por los mismos clientes; veríamos menos sucursales y",
    "menos captación privada. Crédito: si la sucursal presta, financia negocios y veríamos más",
    "establecimientos y empleo. Pero sabíamos de antemano que este banco casi no presta. La",
    "predicción es concreta: una primera etapa grande en cuentas, poco o ningún movimiento en la",
    "banca privada y ningún efecto en la actividad local. Eso es lo que contrastamos.",
  ]);
}

// --- Láminas: datos y método (Fernando) --------------------------------------------------------

function aperturas() {
  pres.addSection({ title: "Datos y método" });
  const s = lamina("Aperturas escalonadas", "Datos y método");
  figura(s, "ppii_mapa_aperturas", { x: 0.35, y: 1.15, wMax: 6.2, hMax: 3.7 });
  cifra(s, { x: 6.85, y: 1.15, w: 2.65, valor: K.n_tratadas,
    etiqueta: "municipios tratados: primera sucursal entre 2022 y 2024" });
  cifra(s, { x: 6.85, y: 2.7, w: 2.65, valor: K.n_controles, etiqueta: "sin sucursal a 2024T4" });
  texto(s, "Fecha: sucursal en operación (CNBV), no la obra.", { x: 6.85, y: 3.9, w: 2.65,
    h: 0.65, fontSize: 16, objectName: "fecha" });
  pie(s, `Los ${K.mapa["Ya tenía (Bansefi)"]} municipios que ya tenían sucursal de Bansefi en ` +
    "2019 quedan fuera de la estimación.");
  notas(s, "Aperturas escalonadas", [
    "[Fernando] El tratamiento es escalonado: cada municipio recibe su primera sucursal en un",
    "trimestre distinto, casi todos entre 2022 y 2024. Los",
    `${K.mapa["Ya tenía (Bansefi)"]} que ya tenían sucursal de Bansefi en 2019 quedan fuera.`,
    `Estimamos con ${K.n_tratadas} municipios tratados y ${K.n_controles} que no tenían sucursal`,
    "a finales de 2024. Fechamos la apertura con la sucursal en operación según la CNBV, no con",
    "la obra, porque en 2022 había el doble de sucursales terminadas que abiertas.",
  ]);
}

function datosVariables() {
  const s = lamina("Datos y variables", "Datos y método");
  const filas = [
    ["Y", "Sucursales privadas por 10 mil adultos", "BDIF"],
    ["G", "Trimestre de apertura", "BDIF, Portafolio"],
    ["X", "Población, marginación, banca previa", "Censo 2020, CONAPO"],
    ["Control", "Aún no y nunca tratados", "BDIF"],
  ];
  const celda = (t, extra) => ({ text: t, options: { valign: "middle", margin: [0, 0.12, 0, 0.12],
    border: [{ type: "none" }, { type: "none" }, { pt: 1, color: "D6E3FF" }, { type: "none" }],
    ...extra } });
  const filasTabla = filas.map(([rol, variable, fuente]) => [
    celda(rol, { bold: true, color: C.accent1, fontSize: 20 }),
    celda(variable, { color: C.text1, fontSize: 19 }),
    celda(fuente, { color: C.accent5, fontSize: 16 }),
  ]);
  s.addTable(filasTabla, { x: MARGEN, y: 1.2, w: 9, colW: [1.4, 5.0, 2.6], rowH: 0.8,
    fontFace: CUERPO,
    objectName: "variables" });
  pie(s, `${K.n_municipios} municipios, 2019T1–2024T4. Denominador fijo: adultos en 2022T4. ` +
    "Claves y límites: Marco Geoestadístico 2024 (INEGI).");
  notas(s, "Datos y variables", [
    "La fuente principal es la Base de Datos de Inclusión Financiera de la CNBV, municipal y",
    "trimestral. El resultado, Y, son las sucursales privadas por cada 10 mil adultos, la única",
    "medida por sector en toda la ventana: los contratos por sector solo existen desde 2022T4.",
    "El denominador es fijo, los adultos de 2022T4, porque la CNBV cambia de fuente de",
    "población en 2020T4. El tratamiento, G, es el trimestre de apertura; al Banco del Bienestar",
    "le quitamos Banjército con el Portafolio de la CNBV. Las covariables, X, son la población",
    "del Censo 2020, la marginación de CONAPO y la banca múltiple de 2019. El control son los",
    `aún no tratados y los nunca tratados. En total, ${K.n_municipios} municipios.`,
  ]);
}

function estrategia() {
  const s = lamina("Estrategia empírica", "Datos y método");
  figura(s, "ppii_ecuacion", { x: MARGEN, y: 1.2, wMax: 6.2 });
  texto(s, "Callaway y Sant'Anna (2021), doblemente robusto", { x: 6.95, y: 1.15, w: 2.55,
    h: 0.9, bold: true, color: C.accent1, objectName: "estimador" });
  texto(s, "Control: aún no y nunca tratados", { x: 6.95, y: 2.1, w: 2.55, h: 0.55, fontSize: 16,
    objectName: "control" });
  texto(s, "Supuestos", { x: MARGEN, y: 2.75, w: 3, h: 0.35, fontSize: 16, bold: true,
    objectName: "supuestos" });
  ["Tendencias paralelas", "Sin anticipación", "Sin derrames"].forEach((t, i) => caja(s, {
    x: MARGEN + i * 3.1, y: 3.15, w: 2.8, h: 0.6, nombre: t, contenido: t,
    opciones: { align: "center" } }));
  caja(s, { x: MARGEN, y: 4.1, w: 9, h: 0.65, relleno: C.accent1, nombre: "regla",
    contenido: `Preregistrado. Nulo informativo: IC90 dentro de ${K.sesoi}.`,
    opciones: { color: C.background1, bold: true, fontSize: 18 } });
  notas(s, "Estrategia empírica", [
    "Usamos el estimador de Callaway y Sant'Anna. Para cada cohorte g y trimestre t compara el",
    "cambio de las tratadas desde el trimestre anterior a la apertura con el cambio de los",
    "municipios que todavía no abren. Así evita el sesgo del TWFE clásico, que con aperturas",
    "escalonadas usa como control a municipios ya tratados. Es doblemente robusto: combina un",
    "puntaje de propensión con una regresión del resultado y es consistente si cualquiera de los",
    "dos es correcto. Descansa en tres supuestos: tendencias paralelas, que probamos con los",
    "trimestres previos y un placebo de fecha; sin anticipación; y sin derrames, que revisamos en",
    "los vecinos. Todo se preregistró antes de estimar, incluida la regla del nulo: el",
    `intervalo al 90% debe quedar dentro de ${K.sesoi} de la media previa, ${K.sesoi_nivel}`,
    `sucursales por 10 mil adultos, unas ${K.sesoi_sucursales} sucursales. Es menos que el`,
    `${sinSigno(K.azteca_pct)} de Banco Azteca.`,
  ]);
}

// --- Láminas: resultados (Luis) -----------------------------------------------------------------

function primeraEtapa() {
  pres.addSection({ title: "Resultados" });
  const s = lamina("Primera etapa: el banco sí llegó", "Resultados");
  figura(s, "ppii_evento_primera_etapa", { x: 0.35, y: 1.12, wMax: 5.7 });
  cifra(s, { x: 6.3, y: 1.15, w: 3.2, valor: `+${K.pe_att}`,
    etiqueta: `sucursales por 10 mil adultos (ee ${K.pe_ee}); previos planos` });
  cifra(s, { x: 6.3, y: 2.8, w: 3.2, valor: `+${K.tarjetas}`,
    etiqueta: "tarjetas de débito del banco por 10 mil adultos" });
  pie(s, "Estudio de evento, Callaway y Sant'Anna; bandas simultáneas al 95%. Tarjetas: " +
    `Portafolio CNBV, ${K.n_tratadas} municipios.`);
  notas(s, "Primera etapa", [
    "[Luis] Primero, ¿el tratamiento cambió algo? Sí. Al abrir, las sucursales totales suben",
    `${K.pe_att} por cada 10 mil adultos, con error estándar de ${K.pe_ee}, y los trimestres`,
    `previos son planos (Wald ${pValor(K.pe_wald_p)}). Y el banco sí bancarizó: ${K.tarjetas}`,
    "tarjetas de débito propias por cada 10 mil adultos, también con previos planos",
    `(${pValor(K.tarjetas_wald_p)}).`,
  ]);
}

function bancaPrivada() {
  const s = lamina("Banca privada: ni atrae ni desplaza", "Resultados");
  figura(s, "ppii_efectos_financieros", { x: 0.3, y: 1.1, wMax: 6.35, hMax: 3.75 });
  cifra(s, { x: 6.85, y: 1.15, w: 2.65, valor: K.priv_pct,
    etiqueta: `sucursales privadas; IC90 dentro de ${K.priv_cota}` });
  cifra(s, { x: 6.85, y: 2.8, w: 2.65, valor: K.cred_pct,
    etiqueta: "crédito privado desde 2022T4" });
  pie(s, `Efecto en % de la media previa, IC al 90%; franja: ${K.sesoi}. † Reprueba la ` +
    "pre-prueba en el DiD apilado.");
  notas(s, "Banca privada", [
    `El resultado principal. Las sucursales privadas cambian ${K.priv_pct} respecto a su media`,
    `previa: ${K.priv_att} por 10 mil adultos, con error estándar de ${K.priv_ee}. No es`,
    `significativo y es un nulo informativo: el intervalo al 90% queda dentro de ${K.priv_cota},`,
    `menos de la mitad del umbral. Comparando solo por calendario queda entre ${K.solo_abren_bajo} y`,
    `${K.solo_abren_alto}: lo que sostenemos es ${K.sesoi}. Por sector, banca múltiple ${K.bm_pct} y EACP ${K.eacp_pct}.`,
    `Desde 2022T4 vemos captación y crédito privados: ${K.capt_pct} y ${K.cred_pct}, con`,
    `${K.corto_tratadas} tratados contra ${K.corto_controles}. Las tarjetas de crédito de la`,
    `banca múltiple, ${K.tc_pct}. Lo único fuera de la franja es el crédito al consumo de las`,
    `EACP, ${K.cred_eacp_pct}, pero en el DiD apilado sus previos ya venían subiendo, así que no`,
    "lo contamos como efecto.",
  ]);
}

function aguanta() {
  const s = lamina("¿Aguanta?", "Resultados");
  figura(s, "ppii_evento_privadas", { x: 0.3, y: 1.12, wMax: 5.2 });
  const pruebas = [
    ["Previos (Wald)", `${pValor(K.priv_wald_p)}`],
    ["Placebo de fecha", K.placebo_pct],
    ["Permutación", `${pValor(K.perm_p)}`],
    ["HonestDiD", `${K.honest_sd_bajo} a ${K.honest_sd_alto}`],
    [`Otros ${K.est_n} estimadores`, `${K.est_min} a ${K.est_max}`],
    ["Solo por calendario", K.solo_abren_pct],
    [`Detecta ${K.sesoi}`, `${K.detecta_5_min} a ${K.detecta_5_max}`],
  ];
  const borde = [{ type: "none" }, { type: "none" }, { pt: 1, color: "D6E3FF" }, { type: "none" }];
  s.addTable(pruebas.map(([prueba, valor]) => [
    { text: prueba, options: { fontSize: 16, color: C.text1, border: borde } },
    { text: valor, options: { fontSize: 16, bold: true, color: C.accent1, align: "right",
      border: borde } },
  ]), { x: 5.7, y: 1.2, w: 3.8, colW: [2.2, 1.6], rowH: 0.48, valign: "middle", fontFace: CUERPO,
    margin: [0, 0.05, 0, 0.05], objectName: "pruebas" });
  pie(s, "Estudio de evento, Callaway y Sant'Anna; bandas simultáneas al 95%; franja: " +
    `${K.sesoi}. HonestDiD con suavidad (M = 0), tres primeros trimestres. Solo por calendario: sin ` +
    `nunca tratados, ${pValor(K.solo_abren_p)} al barajar fechas. Inyectado: fechas barajadas, exploratorio.`,
  4.85, 0.4);
  notas(s, "¿Aguanta?", [
    `¿Depende de supuestos? Los trimestres previos son planos (Wald ${pValor(K.priv_wald_p)}). Un`,
    `placebo que finge aperturas en 2017–2021 da ${K.placebo_pct}. Reasignar las fechas al azar`,
    `dentro de cada estado da ${pValor(K.perm_p)}. HonestDiD, permitiendo tendencias lineales, deja`,
    `el efecto de los primeros trimestres entre ${K.honest_sd_bajo} y ${K.honest_sd_alto}.`,
    `Otros ${K.est_n} estimadores, entre ellos el TWFE con efectos fijos, dan entre ${K.est_min} y`,
    `${K.est_max}. Solo por calendario, sin nunca tratados, da ${K.solo_abren_pct}, con`,
    `${pValor(K.solo_abren_p)} al barajar fechas: no alcanza a ser señal de desplazamiento. Y si`,
    `inyectamos sucursales ficticias, un efecto de ${K.sesoi} se detecta entre ${K.detecta_5_min} y`,
    `${K.detecta_5_max} de las veces; uno de ±2.8%, entre ${K.detecta_28_min} y ${K.detecta_28_max}.`,
    `Por eso sostenemos ${K.sesoi}. La única excepción, el TWFE extendido con covariables, está en el`,
    "respaldo.",
  ]);
}

function usoCuentas() {
  const s = lamina("¿Se usan las cuentas?", "Resultados");
  const fig = figura(s, "ppii_uso_creditos", { x: 0.35, y: 1.25, wMax: 6.1 });
  texto(s, "Menos de un crédito por cada 100 cuentas nuevas.", { x: MARGEN, y: fig.abajo + 0.25,
    w: 6, h: 0.45, fontSize: 18, bold: true, objectName: "lectura" });
  cifra(s, { x: 6.85, y: 1.15, w: 2.65, valor: `+${K.uso_capt}`,
    etiqueta: "contratos de captación del banco por 10 mil adultos" });
  cifra(s, { x: 6.85, y: 2.85, w: 2.65, valor: `+${K.uso_cred}`,
    etiqueta: "créditos por 10 mil adultos" });
  pie(s, `Exploratorio, no preregistrado: CS en 2022T4–2025T4, ${K.uso_tratadas} municipios ` +
    `contra ${K.uso_controles}. Barras: BDIF ${K.periodo_razon}, municipios sin Banjército.`);
  notas(s, "¿Se usan las cuentas?", [
    "Si el banco abrió cuentas, ¿se usan? Esta parte es exploratoria. Desde 2022T4, con",
    `${K.uso_tratadas} municipios tratados contra ${K.uso_controles}, la sucursal suma`,
    `${K.uso_capt} contratos de captación por 10 mil adultos, pero solo ${K.uso_cred} créditos:`,
    `menos de uno por cada 100 cuentas nuevas. En ${K.periodo_razon}, el banco tiene`,
    `${K.creditos_100_banco} créditos por cada 100 cuentas; la banca múltiple de los mismos`,
    `municipios, ${K.creditos_100_bm}. Sus cajeros son solo de retiro: ahí la sucursal suma`,
    `${K.transacciones} transacciones al trimestre y ${K.tarjetas} tarjetas por 10 mil adultos, con`,
    `previos planos. Son ${K.transacciones_por_tarjeta} por tarjeta, cerca del pago bimestral de`,
    "los programas.",
  ]);
}

function actividad() {
  const s = lamina("El aumento del DENUE no es de la sucursal", "Resultados");
  figura(s, "ppii_decaimiento", { x: 0.35, y: 1.15, wMax: 5.6 });
  cifra(s, { x: 6.3, y: 1.15, w: 3.2, valor: K.denue_pct,
    etiqueta: "establecimientos del DENUE en localidades con sucursal" });
  cifra(s, { x: 6.3, y: 2.75, w: 3.2, valor: K.ce_pct,
    etiqueta: `unidades económicas en los Censos (${K.ce_cota})` });
  texto(s, "Sin dosis: 2022 ≈ 2023–24", { x: 6.3, y: 4.25, w: 3.2, h: 0.45, bold: true,
    objectName: "dosis" });
  pie(s, `DENUE, actualización de 2024: ${K.denue_tratadas} localidades contra ` +
    `${K.denue_controles} a ≥10 km; IC al 90%; † reprueba la pre-prueba. Censos: ` +
    `${K.ce_tratadas} municipios.`);
  notas(s, "Actividad económica", [
    `En actividad económica, el DENUE muestra ${sinSigno(K.denue_pct)} más establecimientos en las`,
    "localidades con sucursal en la actualización censal de 2024. Pero no se comporta como",
    `efecto de la sucursal. Las vecinas sin sucursal a menos de 2 km ganan lo mismo, ${K.dec_0_2};`,
    `a 5–10 km, ${K.dec_5_10}. No hay dosis: las aperturas de 2022 dan ${K.expo_temprana} y las`,
    `de 2023–24, ${K.expo_tardia}. Y no aparece en los Censos Económicos, ${K.ce_pct}, ni en los`,
    `dueños de negocio de la Encuesta Intercensal, ${K.eic_negocio} puntos. Lo leemos como un`,
    "aumento del padrón en la zona de la cabecera, no como efecto de la sucursal.",
  ]);
}

// --- Láminas: interpretación y cierre (Luis) ----------------------------------------------------

function interpretacion() {
  pres.addSection({ title: "Política" });
  const s = lamina("Interpretación y política", "Política");
  const lecturas = ["Red de dispersión, no banco", "Acceso no es uso",
    "Importa qué ofrece, no dónde está"];
  lecturas.forEach((t, i) => {
    const x = MARGEN + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 2.8, h: 1.65, fill: { color: C.accent6 },
      line: { type: "none" }, objectName: `tarjeta ${i + 1}` });
    s.addText([
      { text: String(i + 1), options: { fontFace: TEMA.headFontFace, fontSize: 28, bold: true,
        color: C.accent1, breakLine: true } },
      { text: t, options: { fontSize: 19, bold: true, color: C.text1 } },
    ], { x: x + 0.2, y: 1.32, w: 2.4, h: 1.4, fontFace: CUERPO, margin: 0, valign: "top",
      isTextBox: true,
      objectName: `lectura ${i + 1}` });
  });
  caja(s, { x: MARGEN, y: 3.2, w: 9, h: 0.75, relleno: C.accent1, nombre: "recomendacion",
    contenido: "Publicar fechas de obra, cuentas activas y saldos",
    opciones: { color: C.background1, bold: true, fontSize: 19 } });
  caja(s, { x: MARGEN, y: 4.2, w: 9, h: 0.6, nombre: "limites",
    contenido: "Límites: ubicación no aleatoria" });
  notas(s, "Interpretación y política", [
    "¿Qué aprendemos? Primero, el banco funcionó como red de dispersión, no como banco: abrió",
    "cuentas para recibir transferencias, pero sin crédito no hay canal que transmita la",
    "expansión a la banca privada ni a la actividad local. Brasil es el contraste: allí la banca",
    "pública prestó y los municipios crecieron. Segundo, acceso no es uso: las cuentas existen,",
    "pero se usan para retirar los apoyos. Tercero, si el objetivo es inclusión con efectos",
    "reales, importa qué ofrece la sucursal, crédito y ahorro en buenas condiciones, más que",
    "dónde está. Recomendamos publicar las fechas de obra y de apertura, las cuentas activas y",
    "los saldos: separarían el efecto de la sucursal del de su ubicación y medirían el uso, que",
    "hoy no es público. Límites: la ubicación no fue aleatoria. Si permitimos violaciones de",
    "tendencias paralelas de un cuarto de la mayor previa, el intervalo sigue dentro de",
    `${K.honest_rm025}; del mismo tamaño, ya no.`,
    `En banca múltiple, tres regresiones de efectos fijos dan entre ${K.bm_fe_min} y`,
    `${K.bm_fe_max}: si hay desplazamiento, es menor a 5%. Y los contratos por sector solo`,
    "existen desde 2022T4.",
  ]);
}

function conclusiones() {
  const s = lamina("Conclusiones", "Política");
  const puntos = [
    `Bancarizó, pero casi no presta: +${K.uso_cred} créditos por +${K.uso_capt} cuentas.`,
    `No atrajo ni desplazó a la banca privada: se descarta más de ${K.sesoi}.`,
    "El +10% del DENUE no es de la sucursal.",
  ];
  puntos.forEach((p, i) => numerado(s, { x: MARGEN, y: 1.3 + i * 1.0, w: 9, numero: i + 1,
    contenido: p }));
  s.addText("Gracias", { x: MARGEN, y: 4.3, w: 9, h: 0.55, fontFace: TEMA.headFontFace,
    fontSize: 24, bold: true, color: C.accent1, margin: 0, align: "right", isTextBox: true,
    objectName: "gracias" });
  pie(s, `Créditos y cuentas por 10 mil adultos. Exploratorio: Callaway y Sant'Anna, ` +
    `${K.uso_tratadas} municipios contra ${K.uso_controles}.`);
  notas(s, "Conclusiones", [
    "Cerramos con tres frases. El banco bancarizó, pero casi no presta: donde abre suma",
    `${K.uso_capt} cuentas y solo ${K.uso_cred} créditos por 10 mil adultos. No atrajo ni desplazó a`,
    `la banca privada: descartamos cambios mayores a ${K.sesoi} en sucursales privadas. Y el`,
    "aumento de 10% en el DENUE no es de la sucursal. Para la política: abrir sucursales no",
    "basta; importa lo que ofrecen. Gracias.",
  ]);
}

// --- Respaldo -----------------------------------------------------------------------------------

function respaldoEmparejamiento() {
  pres.addSection({ title: "Respaldo" });
  const s = lamina("Respaldo: emparejamiento y balance", "Respaldo");
  figura(s, "ppii_balance", { x: 0.35, y: 1.12, wMax: 5.5 });
  const filas = [
    { valor: K.emp_fin_pct,
      etiqueta: `nunca tratados emparejados, ${K.emp_fin_n} contra ${K.emp_fin_n} (${K.emp_fin_cota})` },
    { valor: K.emp_denue_pct,
      etiqueta: `DENUE, localidades emparejadas (${K.emp_denue_tratadas} contra ${K.emp_denue_controles})` },
    { valor: K.sin_desbalanceadas_pct,
      etiqueta: `sin 2023T4 y 2024T1 (${K.sin_desbalanceadas_cota})` },
  ];
  filas.forEach((f, i) => cifra(s, { x: 6.1, y: 1.1 + i * 1.25, w: 3.4, tamano: 28, alto: 0.55,
    altoEtiqueta: 0.55, ...f }));
  pie(s, "Propensión 1:1 dentro de la región; diferencia estandarizada máxima por cohorte. " +
    `DENUE: diferencias ≤ ${K.emp_denue_smd}, previos ${pValor(K.emp_denue_wald_p)}.`);
  notas(s, "Respaldo: emparejamiento", [
    "Si preguntan por la comparabilidad de los controles. Al reponderar, las cohortes de 2022T1",
    `a 2023T3 quedan balanceadas (diferencia máxima ${K.balance_max_hasta_19}); 2023T4 y 2024T1`,
    `no (${K.balance_20} y ${K.balance_21}), y sin ellas el efecto es ${K.sin_desbalanceadas_pct}.`,
    `Con ${K.emp_fin_n} nunca tratados emparejados 1:1, ${K.emp_fin_pct}. En el DENUE, la muestra`,
    `emparejada da ${K.emp_denue_pct}, con previos planos: el aumento no viene de comparar`,
    "localidades distintas.",
  ], { respaldo: true });
}

function respaldoEfectosFijos() {
  const s = lamina("Respaldo: efectos fijos", "Respaldo");
  figura(s, "ppii_estimadores", { x: 0.3, y: 1.1, wMax: 6.2, hMax: 3.75 });
  const filas = [
    { valor: K.etwfe_cov_pct, etiqueta: "TWFE extendido con covariables: la excepción" },
    { valor: K.etwfe_abren_pct, etiqueta: "el mismo, solo municipios que abren" },
    { valor: K.cs_reg_pct, etiqueta: "CS con el mismo ajuste lineal" },
  ];
  filas.forEach((f, i) => cifra(s, { x: 6.75, y: 1.1 + i * 1.25, w: 2.75, tamano: 28, alto: 0.55,
    altoEtiqueta: 0.55, ...f }));
  pie(s, "Sucursales privadas, % de la media previa, IC al 90%. ◆ TWFE extendido con covariables " +
    "contra los nunca tratados.");
  notas(s, "Respaldo: efectos fijos", [
    "La regresión de efectos fijos que no se sesga con efectos heterogéneos, el TWFE extendido de",
    `Wooldridge, da ${K.etwfe_cov_pct} con covariables (ee ${K.etwfe_cov_ee_pct}). Solo con los`,
    `municipios que alguna vez abren baja a ${K.etwfe_abren_pct}; Callaway y Sant'Anna con el`,
    `mismo ajuste lineal da ${K.cs_reg_pct}; con soporte común sigue en ${K.etwfe_soporte_pct}.`,
    "Por la regla preregistrada manda Callaway y Sant'Anna. Esa comparación se apoya en los nunca",
    `tratados, y contra ellos da ${K.centro_nunca} aun con fechas barajadas al azar.`,
  ], { respaldo: true });
}

function respaldoDesierto() {
  const s = lamina("Respaldo: desierto bancario", "Respaldo");
  figura(s, "ppii_heterogeneidad", { x: 0.35, y: 1.3, wMax: 5.7 });
  cifra(s, { x: 6.1, y: 1.15, w: 3.4, valor: `q = ${K.het_q_fin_min}`, tamano: 28, alto: 0.55,
    etiqueta: "financiero: sin diferencia" });
  cifra(s, { x: 6.1, y: 2.6, w: 3.4, valor: `q = ${K.het_q_denue}`, tamano: 28, alto: 0.55,
    etiqueta: `DENUE: ${K.het_denue_sin} en desiertos contra\u00a0${K.het_denue_con}` });
  pie(s, "Desierto bancario: municipio sin banca múltiple en 2019T1. q de Benjamini–Hochberg " +
    "sobre todas las diferencias. ◆ desierto.");
  notas(s, "Respaldo: desierto bancario", [
    "La segunda pregunta. En lo financiero no hay diferencias entre municipios con y sin banca",
    `múltiple previa (q ≥ ${K.het_q_fin_min}). En el DENUE el aumento es mayor en los desiertos,`,
    `${K.het_denue_sin} contra ${K.het_denue_con} (q = ${K.het_q_denue}), la dirección que`,
    "predice la literatura, pero el aumento mismo no es de la sucursal.",
  ], { respaldo: true });
}

function respaldoFases() {
  const s = lamina("Respaldo: fases 2 y 3", "Respaldo");
  const filas = [
    ["EIC", "Dueños de negocio", K.eic_negocio, "Sin aumento"],
    ["VIIRS", "Luz nocturna", K.viirs, "Nulo por calendario"],
    ["SESNSP", "Robo a transeúnte, homicidio", `${K.robo_transeunte_pct}, ${K.homicidio_pct}`,
      "No informativo"],
    ["INE", "Participación electoral", K.participacion, "Pre-prueba falla"],
  ];
  const borde = [{ type: "none" }, { type: "none" }, { pt: 1, color: "D6E3FF" }, { type: "none" }];
  const color = [C.accent5, C.text1, C.accent1, C.text1];
  s.addTable(filas.map((f) => f.map((t, j) => ({ text: t, options: { fontSize: 18,
    color: color[j], bold: j !== 1, border: borde } }))),
  { x: MARGEN, y: 1.25, w: 9, colW: [1.3, 3.2, 1.9, 2.6], rowH: 0.75, valign: "middle",
    fontFace: CUERPO,
    margin: [0, 0.08, 0, 0.08], objectName: "fases" });
  pie(s, "Preregistradas. EIC e INE en puntos; VIIRS en puntos log; delitos en %. La EIC " +
    `descarta más de ${K.eic_alto}; delitos no descartan ${K.delitos_cota_min}–` +
    `${K.delitos_cota_max}. Elecciones: Wald previa ${pValor(K.participacion_wald_p)}.`, 4.85,
  0.4);
  notas(s, "Respaldo: fases 2 y 3", [
    "Fuentes adicionales, preregistradas. Los dueños de negocio medidos en personas no suben. La",
    "luz nocturna reprueba la pre-prueba contra localidades lejanas; comparando por calendario",
    `entre localidades con sucursal da ${K.viirs} puntos log (ee ${K.viirs_ee}). Delitos: efectos`,
    "cercanos a cero, pero los",
    `intervalos no descartan cambios de ${K.delitos_cota_min} a ${K.delitos_cota_max}. En`,
    "elecciones la pre-prueba falla: no hay efecto identificado.",
  ], { respaldo: true });
}

// --- Tema y salida ------------------------------------------------------------------------------

// pptxgenjs escribe la paleta de Office en el tema; aquí se reemplaza por la del deck para que
// los colores de esquema (C.accent1, …) resuelvan al azul y la tinta de CDA II.
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

function reportarNotas() {
  const expo = conteoNotas.filter((n) => !n.respaldo);
  const total = expo.reduce((a, n) => a + n.palabras, 0);
  conteoNotas.forEach((n, i) => console.log(
    `${String(i + 1).padStart(2)}  ${String(n.palabras).padStart(4)}  ${n.respaldo ? "(respaldo) " : ""}${n.titulo}`));
  console.log(`notas de la exposición: ${total} palabras (tope ${MAX_PALABRAS_NOTAS})`);
  if (total > MAX_PALABRAS_NOTAS) {
    throw new Error(`las notas pasan de ${MAX_PALABRAS_NOTAS} palabras: recorta`);
  }
}

async function main() {
  [portada, politica, pregunta, historiaCausal, aperturas, datosVariables, estrategia,
    primeraEtapa, bancaPrivada, aguanta, usoCuentas, actividad, interpretacion, conclusiones,
    respaldoEmparejamiento, respaldoEfectosFijos, respaldoDesierto, respaldoFases]
    .forEach((f) => f());
  reportarNotas();
  await pres.writeFile({ fileName: SALIDA });
  await aplicarTema(SALIDA, TEMA);
  console.log(`deck en ${path.relative(RAIZ, SALIDA)}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

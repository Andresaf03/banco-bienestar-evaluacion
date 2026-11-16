"""Construye `referencia.docx`, el documento de referencia de estilos para el .docx de la metodología.

Copia los estilos del PDF (Lato 11, renglón seguido, carta con márgenes de 2.5 cm, títulos de sección
en negritas negras del mismo tamaño, sangría de primera línea, texto justificado y referencias con
sangría francesa) sobre el `reference.docx` por defecto de pandoc. Se corre una vez, o cuando cambie
el formato:

    quarto pandoc -o /tmp/pandoc_ref.docx --print-default-data-file reference.docx
    uv run --no-project --with python-docx python referencia_docx.py /tmp/pandoc_ref.docx

`python-docx` no es dependencia del proyecto: el `--with` lo instala en un entorno efímero.
"""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

FUENTE = "Lato"
TAMANO = Pt(11)
SANGRIA = Pt(16.5)  # 1.5em a 11 pt, como `\parindent` del PDF
SALIDA = Path(__file__).with_name("referencia.docx")


def fijar_fuente(rpr_padre) -> None:
    """Fuente explícita en todas las escrituras (sin las del tema, que tienen prioridad)."""
    rpr = rpr_padre.get_or_add_rPr() if hasattr(rpr_padre, "get_or_add_rPr") else rpr_padre
    fuentes = rpr.find(qn("w:rFonts"))
    if fuentes is None:
        fuentes = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, fuentes)
    for atributo in list(fuentes.attrib):
        if atributo.endswith("Theme"):
            del fuentes.attrib[atributo]
    for clave in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fuentes.set(qn(clave), FUENTE)


def sin_color_de_tema(estilo) -> None:
    rpr = estilo.element.get_or_add_rPr()
    color = rpr.find(qn("w:color"))
    if color is not None:
        for atributo in list(color.attrib):
            if atributo.endswith("themeColor") or atributo.endswith("themeShade"):
                del color.attrib[atributo]


CERO = Pt(0)


def parrafo(
    estilo,
    *,
    sangria=None,
    colgante=False,
    alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY,
    antes=CERO,
    despues=CERO,
) -> None:
    fmt = estilo.paragraph_format
    fmt.space_before = antes
    fmt.space_after = despues
    fmt.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fmt.alignment = alineacion
    if colgante:
        fmt.left_indent = SANGRIA
        fmt.first_line_indent = -SANGRIA
    else:
        fmt.left_indent = Pt(0)
        fmt.first_line_indent = sangria
    estilo.font.size = TAMANO
    estilo.font.color.rgb = RGBColor(0, 0, 0)
    fijar_fuente(estilo.element)
    sin_color_de_tema(estilo)


def estilo(doc, nombre, base="Normal"):
    from docx.enum.style import WD_STYLE_TYPE

    try:
        return doc.styles[nombre]
    except KeyError:
        nuevo = doc.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        nuevo.base_style = doc.styles[base]
        return nuevo


def main(entrada: str) -> None:
    doc = Document(entrada)

    # Valores por defecto del documento: Lato 11.
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    rpr_default = defaults.find(qn("w:rPrDefault")).find(qn("w:rPr"))
    fijar_fuente(rpr_default)

    parrafo(doc.styles["Normal"], sangria=Pt(0))
    for nombre in ("Body Text", "First Paragraph"):
        parrafo(estilo(doc, nombre), sangria=SANGRIA)
    parrafo(estilo(doc, "Compact"), sangria=SANGRIA)

    # Títulos de sección: negritas negras, mismo tamaño, poco espacio (como `titlesec` en el PDF).
    titulo = doc.styles["Heading 1"]
    parrafo(titulo, sangria=Pt(0), alineacion=WD_ALIGN_PARAGRAPH.LEFT, antes=Pt(5), despues=Pt(1))
    titulo.font.bold = True
    titulo.font.italic = False
    titulo.paragraph_format.keep_with_next = True

    # Encabezado centrado y ecuaciones en imagen.
    parrafo(
        estilo(doc, "Centrado"),
        sangria=Pt(0),
        alineacion=WD_ALIGN_PARAGRAPH.CENTER,
        antes=Pt(2),
        despues=Pt(2),
    )
    # Referencias APA: sangría francesa y 4 pt entre entradas.
    parrafo(estilo(doc, "Referencias"), colgante=True, despues=Pt(4))

    # División automática de palabras (como el PDF justificado); Word la respeta, Google Docs no.
    ajustes = doc.settings.element
    if ajustes.find(qn("w:autoHyphenation")) is None:
        ajustes.append(ajustes.makeelement(qn("w:autoHyphenation"), {}))

    for seccion in doc.sections:
        seccion.page_width = Inches(8.5)
        seccion.page_height = Inches(11)
        for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(seccion, lado, Cm(2.5))

    doc.save(SALIDA)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main(sys.argv[1])

-- Solo para el .docx: convierte las fórmulas en línea en texto (cursivas, subíndices y
-- superíndices). Google Docs agranda el renglón de cada objeto de ecuación; el texto con formato no.
-- Pandoc ya sabe escribir fórmulas simples como texto en HTML ("plain math"): se escribe la fórmula
-- en HTML y se lee de vuelta como texto con formato.

-- Símbolos que Lato no tiene y que en el PDF son decorativos.
local SUSTITUCIONES = {
  { "\\mathbb{E}", "E" },
  { "\\mathcal{T}", "T" },
  { "\\mid", "|" },
}

-- Espacios finos de la fórmula (U+2004 a U+2006) → espacio duro, para que no se corte en dos renglones.
local ESPACIO_DURO = "\u{00A0}"

local function literal(texto)
  return (texto:gsub("%p", "%%%0"))
end

local function espacios_duros(elemento)
  return pandoc.walk_inline(elemento, {
    Str = function(s)
      local texto = s.text
        :gsub("\u{2004}", ESPACIO_DURO)
        :gsub("\u{2005}", ESPACIO_DURO)
        :gsub("\u{2006}", ESPACIO_DURO)
      return pandoc.Str(texto)
    end,
  })
end

function Math(el)
  if el.mathtype ~= "InlineMath" then
    return nil
  end
  local tex = el.text
  for _, par in ipairs(SUSTITUCIONES) do
    tex = tex:gsub(literal(par[1]), par[2])
  end
  local html = pandoc.write(pandoc.Pandoc({ pandoc.Plain({ pandoc.Math("InlineMath", tex) }) }), "html")
  local texto = pandoc.utils.blocks_to_inlines(pandoc.read(html, "html").blocks)
  return espacios_duros(pandoc.Span(texto))
end

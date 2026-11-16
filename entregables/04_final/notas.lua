-- Notas al pie de tablas y figuras: `::: {.notas}` → entorno `notas` (renglón seguido, letra chica,
-- sin sangría), definido en el encabezado de trabajo_final.qmd. Solo en PDF.
function Div(el)
  if not el.classes:includes("notas") or not FORMAT:match("latex") then
    return nil
  end
  local bloques = { pandoc.RawBlock("latex", "\\begin{notas}") }
  for _, b in ipairs(el.content) do
    table.insert(bloques, b)
  end
  table.insert(bloques, pandoc.RawBlock("latex", "\\end{notas}"))
  return bloques
end

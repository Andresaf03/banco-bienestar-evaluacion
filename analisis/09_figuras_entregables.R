# 09_figuras_entregables.R — Figuras del trabajo final y de la presentación.
#
# Uso:
#   Rscript analisis/09_figuras_entregables.R
#
# No estima nada: lee las tablas que dejan 06–08 y dibuja:
#   1. fig_resumen_efectos: efecto en % de la media previa con IC al 90% de los resultados
#      principales de cada fuente, contra la banda de equivalencia de ±sesoi_pct.
#   2. fig_evento_financiero: estudio de evento de la primera etapa (sucursales totales) y de las
#      sucursales privadas (BDIF, CS, bandas simultáneas). En el panel municipal el cluster es la
#      unidad, así que el bootstrap de `did` coincide con el ee agrupado.
#   3. fig_decaimiento: efecto del DENUE en % por banda de distancia, con todas las localidades y
#      solo dentro del régimen de recorrido total de los Censos Económicos.
#   4. fig_radios (fase 6, C5): el mismo efecto **en niveles** por bandas finas, por mil habitantes
#      y en establecimientos implicados.
#   5. fig_acceso (fase 6, B1): adultos de 65 o más a 10 km o menos de una sucursal del banco, por
#      grado de marginación del municipio.
# Las figuras de la fase 6 se omiten si sus tablas no existen (`make bateria-fase6`).
#
# Salidas: outputs/figuras/fig_*.png. Sin título dentro de la imagen: el título, las notas y la fuente
# van en el pie de cada figura del documento. Ejes con unidades, sin líneas punteadas y colores que se
# distinguen en blanco y negro (Nikolov 2022).

source(here::here("analisis", "00_utils.R"))
suppressPackageStartupMessages(library(ggplot2))

tabla <- function(nombre) {
  ruta <- file.path(RUTA_TABLAS, paste0(nombre, ".csv"))
  if (!file.exists(ruta)) stop("falta ", ruta, ": corre la batería antes de las figuras")
  fread(ruta)
}

tema <- theme_minimal(base_size = 11) +
  theme(panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.title.position = "plot", strip.text = element_text(face = "bold"))

# Resultados del resumen: (variante, panel, resultado, etiqueta legible, bloque).
RESUMEN <- rbindlist(list(
  list("principal", "municipio_trim", "sucursales_privado_pc", "Sucursales privadas", "Financiero (BDIF)"),
  list("principal", "municipio_trim", "sucursales_bm_pc", "Sucursales de banca múltiple", "Financiero (BDIF)"),
  list("principal", "municipio_trim", "sucursales_eacp_pc", "Sucursales de EACP", "Financiero (BDIF)"),
  list("panel_corto", "municipio_trim", "captacion_privado_pc", "Captación privada (2022T4+)", "Financiero (BDIF)"),
  list("panel_corto", "municipio_trim", "credito_privado_pc", "Crédito privado (2022T4+)", "Financiero (BDIF)"),
  list("eacp", "municipio_trim", "capt_ahorro_eacp_pc", "Captación de ahorro EACP", "Financiero (BDIF)"),
  list("eacp", "municipio_trim", "cred_consumo_eacp_pc", "Crédito al consumo EACP †", "Financiero (BDIF)"),
  list("principal", "localidad", "estab_emprendimiento_pc", "Establecimientos (DENUE)", "Actividad local"),
  list("principal", "localidad", "estab_consumo_pc", "Comercio y alimentos (DENUE) †", "Actividad local"),
  list("principal", "localidad", "estab_salud_pc", "Salud (DENUE) †", "Actividad local"),
  list("ce", "municipio_ce", "ue_pc", "Unidades económicas (CE)", "Actividad local"),
  list("ce", "municipio_ce", "personal_ocupado_pc", "Personal ocupado (CE)", "Actividad local"),
  list("imss", "municipio_trim", "log_salario_diario", "Salario diario (IMSS)", "Actividad local")
))
setnames(RESUMEN, c("variante", "panel", "resultado", "nombre", "fuente"))

fig_resumen_efectos <- function() {
  t <- tabla("tabla_final")
  d <- merge(RESUMEN, t[, !"bloque"], by = c("variante", "panel", "resultado"), sort = FALSE)
  d[, escala := fifelse(startsWith(resultado, "log_"), 1, abs(media_base))]
  d[, `:=`(bajo = 100 * ic90_bajo / escala, alto = 100 * ic90_alto / escala)]
  d[, nombre := factor(nombre, levels = rev(RESUMEN$nombre))]
  d[, fuente := factor(fuente, levels = unique(RESUMEN$fuente))]
  sesoi <- PARAMS$estimacion$sesoi_pct
  p <- ggplot(d, aes(x = efecto_pct, y = nombre)) +
    annotate("rect", xmin = -sesoi, xmax = sesoi, ymin = -Inf, ymax = Inf, alpha = 0.12,
             fill = "#2a6f97") +
    geom_vline(xintercept = 0, linetype = "dashed", colour = "grey40") +
    geom_errorbar(aes(xmin = bajo, xmax = alto), width = 0.25, colour = "grey30",
                  orientation = "y") +
    geom_point(size = 2.2, colour = "#c1121f") +
    facet_grid(fuente ~ ., scales = "free_y", space = "free_y") +
    labs(x = "Efecto (% de la media previa de las tratadas)", y = NULL) +
    tema
  guardar_figura(p, "fig_resumen_efectos", ancho = 9, alto = 6.5)
  invisible(d)
}

fig_evento_financiero <- function() {
  series <- c(primera_etapa_sucursales_total_pc = "Primera etapa: sucursales totales",
              sucursales_privado_pc = "Sucursales privadas (banca múltiple + EACP)")
  d <- rbindlist(lapply(names(series), function(s) {
    x <- tabla(paste0("cs_agg_municipio_trim_esc_", s))[tipo == "dynamic"]
    x[, serie := series[[s]]]
  }))
  d[, e := as.integer(termino)]
  d <- d[e >= -12 & e <= 11]
  d[, serie := factor(serie, levels = series)]
  p <- ggplot(d, aes(x = e, y = valor)) +
    geom_hline(yintercept = 0, linetype = "dashed", colour = "grey40") +
    geom_vline(xintercept = -0.5, linetype = "longdash", colour = "grey55") +
    geom_ribbon(aes(ymin = ic_bajo, ymax = ic_alto), fill = "#2a6f97", alpha = 0.2) +
    geom_point(colour = "#2a6f97", size = 1.6) +
    facet_wrap(~ serie, scales = "free_y") +
    labs(x = "Trimestres desde la primera sucursal",
         y = "Efecto (sucursales por 10 mil adultos)") +
    tema
  guardar_figura(p, "fig_evento_financiero", ancho = 10, alto = 4.2)
  invisible(d)
}

fig_decaimiento <- function() {
  nombres <- c(estab_emprendimiento_pc = "Establecimientos", estab_consumo_pc = "Comercio y alimentos",
               estab_salud_pc = "Salud")
  bandas <- c("sucursal propia", "0–2 km", "2–5 km", "5–10 km")
  etiquetas <- c("Con sucursal", "Vecina\n0–2 km", "Vecina\n2–5 km", "Vecina\n5–10 km")
  # Las filas de contrastes traen la banda vacía.
  es_banda <- function(x) !is.na(x) & nzchar(x)
  todas <- rbindlist(lapply(names(nombres), function(r) {
    tabla(paste0("decaimiento_", r))[es_banda(banda)][, muestra := "Todas las localidades"]
  }), fill = TRUE)
  regimen <- rbindlist(lapply(names(nombres), function(r) {
    tabla(paste0("regimen_", r))[regimen == "recorrido_total" & es_banda(banda)][
      , muestra := "Solo recorrido total del CE (exploratorio)"]
  }), fill = TRUE)
  d <- rbindlist(list(todas, regimen), fill = TRUE)
  d[, `:=`(pct = 100 * att / media_base, bajo = 100 * (att - 1.96 * ee) / media_base,
           alto = 100 * (att + 1.96 * ee) / media_base)]
  d[, `:=`(banda = factor(banda, levels = bandas, labels = etiquetas),
           nombre = factor(nombres[resultado], nombres),
           muestra = factor(muestra, c("Todas las localidades",
                                       "Solo recorrido total del CE (exploratorio)")),
           previos = fifelse(pre_wald_p < 0.05, "reprueba pre-prueba", "previos planos"))]
  p <- ggplot(d, aes(x = banda, y = pct, colour = muestra, shape = previos)) +
    geom_hline(yintercept = 0, linetype = "dashed", colour = "grey40") +
    geom_pointrange(aes(ymin = bajo, ymax = alto), position = position_dodge(width = 0.5)) +
    scale_shape_manual(values = c("previos planos" = 16, "reprueba pre-prueba" = 1)) +
    scale_colour_manual(values = c("#1b4965", "#e09f3e")) +
    facet_wrap(~ nombre) +
    labs(x = "Localidad", y = "Efecto (% de la media previa de cada grupo)", colour = NULL,
         shape = NULL) +
    tema + theme(legend.box = "vertical")
  guardar_figura(p, "fig_decaimiento", ancho = 10, alto = 5)
  invisible(d)
}

existe_tabla <- function(nombre) file.exists(file.path(RUTA_TABLAS, paste0(nombre, ".csv")))

fig_radios <- function(resultado = "estab_emprendimiento_pc") {
  nombre <- paste0("fase6_radios_", resultado)
  if (!existe_tabla(nombre)) return(message("sin ", nombre, ": se omite fig_radios"))
  d <- tabla(nombre)
  d[, banda := factor(banda, levels = banda,
                      labels = c("Con\nsucursal", sub(" km", "", banda[-1])))]
  d[, previos := fifelse(pre_wald_p < 0.05, "reprueba pre-prueba", "previos planos")]
  largo <- rbindlist(list(
    d[, .(banda, previos, medida = "Por mil habitantes (sin ponderar)", valor = att, ee)],
    d[, .(banda, previos, medida = "Establecimientos implicados (miles, ponderado)",
          valor = estab_implicados / 1000, ee = estab_implicados_ee / 1000)]
  ))
  largo[, medida := factor(medida, c("Por mil habitantes (sin ponderar)",
                                      "Establecimientos implicados (miles, ponderado)"))]
  p <- ggplot(largo, aes(x = banda, y = valor, shape = previos)) +
    geom_hline(yintercept = 0, colour = "grey40") +
    geom_pointrange(aes(ymin = valor - 1.96 * ee, ymax = valor + 1.96 * ee), colour = "#1b4965") +
    scale_shape_manual(values = c("previos planos" = 16, "reprueba pre-prueba" = 1)) +
    facet_wrap(~ medida, scales = "free_y") +
    labs(x = "Localidad con sucursal y vecinas sin sucursal, por km de distancia",
         y = "Efecto en la actualización de 2024", shape = NULL) +
    tema
  guardar_figura(p, "fig_radios", ancho = 10, alto = 4.5)
  invisible(d)
}

fig_acceso <- function() {
  if (!existe_tabla("fase6_accesibilidad")) return(message("sin fase6_accesibilidad: se omite"))
  d <- tabla("fase6_accesibilidad")[poblacion_tipo == "65 y más" & cota == "central" &
                                      grupo_tipo %in% c("nacional", "marginacion")]
  niveles <- c("Muy bajo", "Bajo", "Medio", "Alto", "Muy alto")
  femenino <- c("Muy bajo" = "muy baja", "Bajo" = "baja", "Medio" = "media", "Alto" = "alta",
                "Muy alto" = "muy alta")
  d[, grupo := fifelse(grupo_tipo == "nacional", "Nacional", paste("Marginación", femenino[grupo]))]
  d[, grupo := factor(grupo, c("Nacional", paste("Marginación", femenino[niveles])))]
  d[, fecha := factor(corte, levels = sort(unique(corte)), labels = sub("Q", "T", sort(unique(corte))))]
  p <- ggplot(d, aes(x = fecha, y = pct_a_10km, group = grupo, colour = grupo)) +
    geom_line(linewidth = 0.8) +
    geom_point(size = 1.8) +
    scale_colour_manual(values = c("black", "#cfe1ec", "#8fb8d3", "#4f8fba", "#1f6391", "#0b3954")) +
    scale_y_continuous(limits = c(0, 100)) +
    labs(x = NULL, y = "% de los adultos de 65 o más a 10 km o menos", colour = NULL) +
    tema
  guardar_figura(p, "fig_acceso", ancho = 9, alto = 4.8)
  invisible(d)
}

figuras_todo <- function() {
  fig_resumen_efectos()
  fig_evento_financiero()
  fig_decaimiento()
  fig_radios()
  fig_acceso()
  message("figuras en ", RUTA_FIGURAS)
}

if (sys.nframe() == 0) figuras_todo()

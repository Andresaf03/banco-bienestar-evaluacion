# 10_fase2.R — Fase 2: fuentes nuevas (preregistro en docs/decisiones.md, 2026-10-07).
#
# Uso:
#   Rscript analisis/10_fase2.R todo           # todo lo que tenga panel construido
#   Rscript analisis/10_fase2.R tratamiento    # 1. G con el Banco del Bienestar observado (P-8)
#   Rscript analisis/10_fase2.R eic            # 2. EIC 2015 / Censo 2020 / EIC 2025
#   Rscript analisis/10_fase2.R viirs          # 3. luz nocturna por localidad
#   Rscript analisis/10_fase2.R efipem         # 4. finanzas públicas municipales
#   Rscript analisis/10_fase2.R enoe           # 5. ENOE municipal (réplica de Bruhn y Love)
#   Rscript analisis/10_fase2.R resumen        # tabla de la fase con Romano–Wolf y BH
#
# No toca la maestra, la tabla final ni las familias de las fases anteriores: los paneles nuevos se
# registran aquí (no en 00_utils.R), los resúmenes se guardan como `fase2_*` y la heterogeneidad
# como `fase2_het_*` (para que 07_inferencia.R no la mezcle con la suya). Las tablas por
# especificación (`cs_*`, `rob_*`, `if_*`) llevan el nombre del panel nuevo en la etiqueta.
#
# Salidas: outputs/tablas/fase2_tratamiento_obs.csv, fase2_resumen.csv, fase2_dosis_*.csv,
# fase2_het_*.csv, fase2_decaimiento_*.csv y las de cada especificación.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
source(here::here("analisis", "05_robustez.R"))          # variante(), robustez_escalonado(), honest()
source(here::here("analisis", "07_inferencia.R"))        # romano_wolf()
source(here::here("analisis", "08_disenos_alternativos.R"))  # estimar_banda(), diferencia()

# Paneles de la fase 2 (src/proyecto/construccion/panel_fase2.py).
PANELES$municipio_trim_obs <- list(archivo = "panel_municipio_trim_obs.parquet", id = "cve_mun",
                                   tiempo = "t", per_capita = TRUE, periodicidad = "trimestral",
                                   ventana = "ventana_trimestral")
PANELES$municipio_eic <- list(archivo = "panel_municipio_eic.parquet", id = "cve_mun",
                              tiempo = "t", per_capita = TRUE, periodicidad = "censal")
PANELES$localidad_viirs <- list(archivo = "panel_localidad_viirs.parquet", id = "cve_loc",
                                tiempo = "t", per_capita = TRUE, periodicidad = "anual")
PANELES$municipio_efipem <- list(archivo = "panel_municipio_efipem.parquet", id = "cve_mun",
                                 tiempo = "t", per_capita = TRUE, periodicidad = "anual")
PANELES$municipio_enoe <- list(archivo = "panel_municipio_enoe.parquet", id = "cve_mun",
                               tiempo = "t", per_capita = TRUE, periodicidad = "trimestral")

F2 <- PARAMS$fase2
FINANCIERA <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
VENTANA_2025 <- c(1L, 28L)

existe_panel <- function(nombre) file.exists(file.path(RUTA_PANELES, PANELES[[nombre]]$archivo))

#' Corre CS para una lista de resultados y devuelve las filas resumen con la familia.
correr_bloque <- function(panel, resultados, variante, familia, ...) {
  filas <- lapply(resultados, function(r) {
    message("\n#### ", panel, " / ", r)
    tryCatch({
      out <- correr(panel, r, variante = variante, ...)$fila
      out[, `:=`(variante = variante, familia = familia)]
    }, error = function(e) { message("  falló: ", conditionMessage(e)); NULL })
  })
  rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
}

#' Subgrupos (dosis o heterogeneidad) con la especificación principal; la diferencia contra el
#' primer grupo se prueba con z (conservadora cuando comparten controles).
subgrupos <- function(panel, resultado, columna, grupos, comparten_controles, ...) {
  dt <- con_resultado(leer_panel(panel, resultado = resultado, ...), resultado)
  dt[, grupo := as.character(get(columna))]
  filas <- lapply(grupos, function(g) {
    sub <- if (comparten_controles) dt[grupo %in% c("control", g)] else dt[grupo == g]
    for (a in c("panel_nombre", "panel_id", "diseno")) setattr(sub, a, attr(dt, a))
    f <- variante(g, sub, resultado)
    if (is.null(f)) {
      f <- variante(paste(g, "(sin covariables)"), sub, resultado, covariables = FALSE)
    }
    f
  })
  out <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
  if (!nrow(out)) return(out)
  ref <- out[1]
  out[, `:=`(panel = panel, resultado = resultado, efecto_pct = 100 * att / escala_pct(resultado, media_base),
             dif_vs_ref = att - ref$att, z_dif = (att - ref$att) / sqrt(ee^2 + ref$ee^2))]
  out[1, `:=`(dif_vs_ref = NA_real_, z_dif = NA_real_)]
  out[, p_dif := 2 * stats::pnorm(-abs(z_dif))]
  out[]
}

# 1. Tratamiento observado (P-8) --------------------------------------------------------------------

tratamiento_obs <- function() {
  especs <- list(
    list(resultados = FINANCIERA, ventana = NULL, nombre = "principal (2019T1–2024T4)"),
    list(resultados = FINANCIERA, ventana = VENTANA_2025, nombre = "hasta_2025"),
    list(resultados = "sucursales_total_pc", ventana = NULL, nombre = "primera etapa")
  )
  filas <- list()
  for (e in especs) for (r in e$resultados) {
    message("\n#### tratamiento observado: ", r, " | ", e$nombre)
    base <- variante("G de la corrida final",
                     leer_panel("municipio_trim", diseno = "escalonado", resultado = r,
                                ventana = e$ventana), r)
    obs <- variante("G observado (modelo Portafolio 2022+)",
                    leer_panel("municipio_trim_obs", diseno = "escalonado", resultado = r,
                               ventana = e$ventana, excluir_sospechosos = FALSE), r)
    if (is.null(base) || is.null(obs)) next
    filas[[length(filas) + 1]] <- rbindlist(list(base, obs))[, `:=`(resultado = r,
                                                                     especificacion = e$nombre)]
  }
  out <- rbindlist(filas, fill = TRUE)
  out[, efecto_pct := 100 * att / abs(media_base)]
  out[, dif_en_ee := (att - att[1]) / ee[1], by = .(resultado, especificacion)]
  guardar_tabla(out, "fase2_tratamiento_obs")
  print(out[, .(especificacion, resultado, variante, tratadas, att = round(att, 4),
                ee = round(ee, 4), dif_en_ee = round(dif_en_ee, 2), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# 2. EIC 2015 / Censo 2020 / EIC 2025 ---------------------------------------------------------------

eic <- function() {
  if (!existe_panel("municipio_eic")) return(message("sin panel_municipio_eic: se salta"))
  principales <- correr_bloque("municipio_eic", F2$eic$familia_rw, "eic", "eic")
  mecanismo <- correr_bloque("municipio_eic", F2$eic$mecanismo, "eic", "eic_mecanismo")
  guardar_tabla(rbindlist(list(principales, mecanismo), fill = TRUE), "fase2_eic")
  # Dosis (temprana ≤ 2022T2 contra tardía) y desierto bancario, en la principal y en programas.
  for (r in c("pct_negocio", "pct_hog_programas")) {
    message("\n#### EIC dosis: ", r)
    dosis <- subgrupos("municipio_eic", r, "exposicion_ce", c("temprana", "tardía"), TRUE)
    guardar_tabla(dosis, paste0("fase2_dosis_eic_", r))
    message("\n#### EIC desierto bancario: ", r)
    het <- subgrupos("municipio_eic", r, "desierto_bancario", c("1", "0"), FALSE)
    guardar_tabla(het, paste0("fase2_het_eic_", r, "_desierto"))
  }
  # Robustez preregistrada: sin covariables y HonestDiD (un solo previo).
  for (r in c("pct_negocio", "pct_hog_programas")) {
    robustez_escalonado("municipio_eic", r)
    honest("municipio_eic", r, "escalonado", periodos_post = 1, variante = "eic")
  }
}

# 3. VIIRS -----------------------------------------------------------------------------------------

#' Diagnóstico de la ruptura de producto (adenda del preregistro): cambio medio de log(1 + luz) entre
#' años consecutivos en los controles (sin sucursal, a ≥10 km), por decil de luz de 2021. Si el paso
#' 2021→2022 (VNL v2.1 → v2.2 de dos satélites) o 2022→2023 (→ VNL v2 SNPP) cambia distinto por
#' brillo que los pasos sin cambio de producto, la comparación tratadas (iluminadas) contra
#' controles (oscuros) hereda la ruptura.
ruptura_viirs <- function() {
  dt <- leer_panel("localidad_viirs", diseno = "completo", resultado = "log1p_luz_1km")
  ctrl <- dt[G == 0]
  setorder(ctrl, id, tiempo)
  ctrl[, delta := log1p_luz_1km - shift(log1p_luz_1km), by = id]
  base21 <- ctrl[tiempo == 2021 - 2015, .(id, luz21 = log1p_luz_1km)]
  ctrl <- merge(ctrl, base21, by = "id")
  ctrl[, decil := cut(frank(luz21, ties.method = "random") / .N, breaks = seq(0, 1, 0.1),
                      labels = FALSE, include.lowest = TRUE)]
  out <- ctrl[!is.na(delta), .(delta_media = mean(delta), n = .N), by = .(decil, paso = paste0(tiempo + 2014, "→", tiempo + 2015))]
  ancho <- dcast(out, decil ~ paso, value.var = "delta_media")
  guardar_tabla(ancho, "fase2_desc_viirs_ruptura")
  print(ancho[, lapply(.SD, function(x) if (is.numeric(x)) round(x, 3) else x)])
  invisible(ancho)
}

#' Contraste entre bandas para resultados en logaritmo: en puntos log (×100), sin dividir entre la
#' media (`diferencia()` de 08 expresa los contrastes en % de la media de cada banda, que solo tiene
#' sentido en niveles). Misma covarianza agrupada por municipio de las funciones de influencia.
diferencia_log <- function(a, b) {
  claves <- union(names(a$psi), names(b$psi))
  pa <- a$psi[claves]; pa[is.na(pa)] <- 0
  pb <- b$psi[claves]; pb[is.na(pb)] <- 0
  dif <- 100 * (a$fila$att - b$fila$att)
  ee <- 100 * sqrt(sum((pa - pb)^2))
  data.table(contraste = paste(a$fila$banda, "−", b$fila$banda), dif_pct = dif, ee_dif_pct = ee,
             p_dif = 2 * stats::pnorm(-abs(dif / ee)))
}

#' Decaimiento espacial: localidad con sucursal contra vecinas por banda, con los mismos controles.
viirs_bandas <- function(res) {
  message("\n#### VIIRS decaimiento: ", res)
  lee <- function(...) con_resultado(leer_panel("localidad_viirs", diseno = "escalonado",
                                                resultado = res, ...), res)
  bandas <- lapply(PARAMS$estimacion$bandas_derrame_km, unlist)
  nombres <- c("sucursal propia", vapply(bandas, function(b) sprintf("%g–%g km", b[1], b[2]), ""))
  muestras <- c(list(lee()), lapply(bandas, function(b) lee(derrame = TRUE, banda = b)))
  est <- Map(function(n, d) estimar_banda(n, d, res), nombres, muestras)
  filas <- rbindlist(lapply(est, `[[`, "fila"))
  filas[, efecto_pct := 100 * att / escala_pct(res, media_base)]
  contraste <- if (startsWith(res, "log")) diferencia_log else diferencia
  ultima <- length(est)
  difs <- rbindlist(list(contraste(est[[1]], est[[2]]), contraste(est[[1]], est[[ultima]]),
                         contraste(est[[2]], est[[ultima]])))
  out <- rbindlist(list(filas, difs), fill = TRUE)[, resultado := res]
  guardar_tabla(out, paste0("fase2_decaimiento_viirs_", res))
  print(out[, .(banda, contraste, tratadas, att = round(att, 4), ee = round(ee, 4),
                wald_p = signif(pre_wald_p, 3), dif = round(dif_pct, 2), p_dif = signif(p_dif, 3))])
  invisible(out)
}

viirs <- function() {
  if (!existe_panel("localidad_viirs")) return(message("sin panel_localidad_viirs: se salta"))
  ruptura_viirs()
  principales <- correr_bloque("localidad_viirs", F2$viirs$familia_rw, "viirs", "viirs")
  guardar_tabla(principales, "fase2_viirs")
  r <- F2$viirs$familia_rw[1]
  for (res in c(r, "log1p_luz_anillo")) viirs_bandas(res)
  # Robustez preregistrada: variantes escalonadas, régimen de recorrido total y HonestDiD.
  robustez_escalonado("localidad_viirs", r)
  lee <- function(...) leer_panel("localidad_viirs", diseno = "escalonado", resultado = r, ...)
  extra <- rbindlist(Filter(Negate(is.null), list(
    variante("régimen de recorrido total", lee(regimen = "recorrido_total"), r),
    variante("controles: todos", lee(controles = "todos"), r),
    variante("controles: solo con sucursal", lee(controles = "solo_sucursal"), r),
    variante("controles: ≥20 km", lee(controles = "dist20"), r)
  )), fill = TRUE)
  if (nrow(extra)) guardar_tabla(extra[, resultado := r], paste0("fase2_rob_extra_viirs_", r))
  honest("localidad_viirs", r, "escalonado", variante = "viirs")
}

# 4. EFIPEM ----------------------------------------------------------------------------------------

efipem <- function() {
  if (!existe_panel("municipio_efipem")) return(message("sin panel_municipio_efipem: se salta"))
  principales <- correr_bloque("municipio_efipem", F2$efipem$familia_rw, "efipem", "efipem")
  guardar_tabla(principales, "fase2_efipem")
  r <- F2$efipem$familia_rw[1]
  robustez_escalonado("municipio_efipem", r)
  honest("municipio_efipem", r, "escalonado", variante = "efipem")
}

# 5. ENOE ------------------------------------------------------------------------------------------

enoe <- function() {
  if (!existe_panel("municipio_enoe")) return(message("sin panel_municipio_enoe: se salta"))
  principales <- correr_bloque("municipio_enoe", F2$enoe$familia_rw, "enoe", "enoe")
  guardar_tabla(principales, "fase2_enoe")
  r <- F2$enoe$familia_rw[1]
  robustez_escalonado("municipio_enoe", r)
  honest("municipio_enoe", r, "escalonado", variante = "enoe")
}

# Resumen de la fase: potencia, equivalencia, Romano–Wolf por familia y BH en toda la fase ----------

resumen <- function() {
  partes <- lapply(c("fase2_eic", "fase2_viirs", "fase2_efipem", "fase2_enoe"), function(n) {
    ruta <- file.path(RUTA_TABLAS, paste0(n, ".csv"))
    if (file.exists(ruta)) fread(ruta) else NULL
  })
  cs <- rbindlist(Filter(Negate(is.null), partes), fill = TRUE)
  if (!nrow(cs)) return(message("sin resultados de la fase 2"))
  z90 <- stats::qnorm(0.95)
  cs[, escala := fifelse(startsWith(resultado, "log"), 1, abs(media_base))]
  cs[, `:=`(p = 2 * stats::pnorm(-abs(valor / ee)),
            efecto_pct = 100 * valor / escala,
            mde80_pct = 100 * (stats::qnorm(0.975) + stats::qnorm(0.80)) * ee / escala,
            cota_equivalencia_pct = 100 * (abs(valor) + z90 * ee) / escala)]
  cs[, escala := NULL]
  cs[, nulo_informativo := p >= 0.05 & cota_equivalencia_pct <= PARAMS$estimacion$sesoi_pct]
  cs[, pre_falla := !is.na(pre_wald_p) & pre_wald_p < 0.05]
  cs[, q_bh_fase2 := stats::p.adjust(p, method = "BH")]
  rw <- rbindlist(lapply(c("eic", "viirs", "efipem", "enoe"), function(f) {
    sub <- cs[familia == f]
    if (nrow(sub) < 1) return(NULL)
    romano_wolf(sub$etiqueta, sub$valor)[, familia := f]
  }))
  if (nrow(rw)) cs <- merge(cs, rw[, .(etiqueta, p_rw)], by = "etiqueta", all.x = TRUE)
  cs[, lectura := fcase(pre_falla, "descriptivo (pre-prueba falla)",
                        nulo_informativo, "nulo informativo",
                        p < 0.05 & q_bh_fase2 < 0.05, "significativo (sobrevive BH)",
                        p < 0.05, "significativo sin corrección (BH q ≥ 0.05)",
                        default = "no informativo")]
  guardar_tabla(cs, "fase2_resumen")
  print(cs[, .(familia, resultado, tratadas = n_tratadas, att = round(valor, 4), ee = round(ee, 4),
               efecto_pct = round(efecto_pct, 1), cota = round(cota_equivalencia_pct, 1),
               wald_p = round(pre_wald_p, 3), p_rw = round(p_rw, 3), lectura)])
  invisible(cs)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { tratamiento_obs(); eic(); viirs(); efipem(); enoe(); resumen() },
         tratamiento = tratamiento_obs(),
         eic = eic(),
         viirs = viirs(),
         viirs_bandas = for (res in c(F2$viirs$familia_rw[1], "log1p_luz_anillo")) viirs_bandas(res),
         efipem = efipem(),
         enoe = enoe(),
         resumen = resumen(),
         stop("uso: Rscript analisis/10_fase2.R todo | tratamiento | eic | viirs | efipem | enoe | ",
              "resumen"))
}

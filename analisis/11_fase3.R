# 11_fase3.R — Fase 3: delitos (SESNSP) y elecciones federales (INE). Preregistro en
# docs/decisiones.md (2026-10-11), con su adenda de datos.
#
# Uso:
#   Rscript analisis/11_fase3.R todo         # todo lo que tenga panel construido
#   Rscript analisis/11_fase3.R delitos      # A. incidencia delictiva municipal, escalonado
#   Rscript analisis/11_fase3.R elecciones   # B. diputados federales, una cohorte (G = 4)
#   Rscript analisis/11_fase3.R ubicacion    # B. diagnóstico descriptivo de la fecha de apertura
#   Rscript analisis/11_fase3.R resumen      # tabla de la fase con Romano–Wolf y BH
#
# Como la fase 2: no toca la maestra, la tabla final ni las familias anteriores. Los paneles se
# registran aquí (no en 00_utils.R) y los resúmenes se guardan como `fase3_*`; las tablas por
# especificación (`cs_*`, `rob_*`, `if_*`) llevan el nombre del panel en la etiqueta.
#
# Salidas: outputs/tablas/fase3_delitos.csv, fase3_elecciones.csv, fase3_rob_extra_*.csv,
# fase3_twfe_elecciones_*.csv, fase3_dosis_elecciones_*.csv, fase3_desc_ubicacion.csv y
# fase3_resumen.csv.

# 10_fase2.R trae 00_utils, 02, 05, 07 y 08, y define correr_bloque() y subgrupos(); su guard
# `sys.nframe()` evita que corra.
source(here::here("analisis", "10_fase2.R"))

# Paneles de la fase 3 (src/proyecto/construccion/panel_fase3.py).
for (nombre in c("municipio_delitos", "municipio_delitos_largo", "municipio_delitos_obs")) {
  PANELES[[nombre]] <- list(archivo = paste0("panel_", nombre, ".parquet"), id = "cve_mun",
                            tiempo = "t", per_capita = TRUE, periodicidad = "trimestral")
}
for (nombre in c("municipio_elecciones", "municipio_elecciones_todos",
                 "municipio_elecciones_obs")) {
  PANELES[[nombre]] <- list(archivo = paste0("panel_", nombre, ".parquet"), id = "cve_mun",
                            tiempo = "t", per_capita = TRUE, periodicidad = "censal")
}

F3 <- PARAMS$fase3
# El pre-periodo extendido arranca en 2017T1 (t = 5 del panel largo, que empieza en 2016T1): en
# 2015–2016 el SESNSP cubre solo 1,921 de los 2,456 municipios estables (regla 10).
VENTANA_LARGA <- c(5L, 40L)

#' Variantes extra de la fase con su tabla (`fase3_rob_extra_<panel>_<resultado>`).
guardar_extra <- function(filas, panel, resultado) {
  extra <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
  if (!nrow(extra)) return(invisible(extra))
  extra[, `:=`(panel = panel, resultado = resultado,
               efecto_pct = 100 * att / escala_pct(resultado, media_base))]
  guardar_tabla(extra, paste0("fase3_rob_extra_", panel, "_", resultado))
  print(extra[, .(variante, tratadas, controles, att = round(att, 4), ee = round(ee, 4),
                  efecto_pct = round(efecto_pct, 1), wald_p = round(pre_wald_p, 3))])
  invisible(extra)
}

# A. Delitos ---------------------------------------------------------------------------------------

delitos_robustez <- function(r) {
  robustez_escalonado("municipio_delitos", r)
  lee <- function(...) leer_panel("municipio_delitos", diseno = "escalonado", resultado = r, ...)
  crudo <- panel_crudo("municipio_delitos")
  con_registro <- unique(crudo[con_registro_2019 == TRUE, cve_mun])
  guardar_extra(list(
    variante("G observado (modelo Portafolio 2022+)",
             leer_panel("municipio_delitos_obs", diseno = "escalonado", resultado = r,
                        excluir_sospechosos = FALSE), r),
    variante("pre-periodo desde 2017T1",
             leer_panel("municipio_delitos_largo", diseno = "escalonado", resultado = r,
                        ventana = VENTANA_LARGA), r),
    variante("piso de 5,000 habitantes", lee(piso_poblacion = F3$delitos$piso_robustez), r),
    variante("solo municipios con algún robo registrado en 2019", lee(ids = con_registro), r)
  ), "municipio_delitos", r)
}

delitos <- function() {
  if (!existe_panel("municipio_delitos")) return(message("sin panel_municipio_delitos: se salta"))
  principales <- correr_bloque("municipio_delitos", F3$delitos$familia_rw, "delitos", "delitos")
  secundarios <- correr_bloque("municipio_delitos", F3$delitos$secundarios, "delitos",
                               "delitos_secundarios")
  guardar_tabla(rbindlist(list(principales, secundarios), fill = TRUE), "fase3_delitos")
  # Robustez preregistrada: en todos los de la familia; HonestDiD en el principal.
  for (r in F3$delitos$familia_rw) delitos_robustez(r)
  honest("municipio_delitos", F3$delitos$familia_rw[1], "escalonado", variante = "delitos")
}

# B. Elecciones ------------------------------------------------------------------------------------

#' TWFE con efectos fijos de municipio y de estado × elección (con una sola cohorte no hay
#' comparaciones prohibidas): estudio de evento con base en 2021 (t = 3) y el DiD de un coeficiente.
twfe_elecciones <- function(r) {
  dt <- con_resultado(leer_panel("municipio_elecciones", resultado = r), r)
  dt[, `:=`(cve_ent = substr(cve_mun, 1, 2), trat = as.integer(G > 0))]
  evento <- fixest::feols(
    stats::as.formula(paste(r, "~ i(tiempo, trat, ref = 3) | id + cve_ent^tiempo")), dt,
    cluster = ~cve_mun)
  did_simple <- fixest::feols(stats::as.formula(paste(r, "~ tratado | id + cve_ent^tiempo")), dt,
                              cluster = ~cve_mun)
  ct <- fixest::coeftable(evento)
  w <- fixest::wald(evento, keep = "^tiempo::[12]:trat$", print = FALSE)
  cs <- fixest::coeftable(did_simple)
  out <- rbind(
    data.table(termino = rownames(ct), coef = ct[, 1], ee = ct[, 2], p = ct[, 4],
               modelo = "estudio de evento (base 2021)"),
    data.table(termino = rownames(cs), coef = cs[, 1], ee = cs[, 2], p = cs[, 4],
               modelo = "DiD, efectos fijos estado × elección")
  )
  out[, `:=`(resultado = r, n = stats::nobs(evento), tratadas = uniqueN(dt[G > 0]$id),
             controles = uniqueN(dt[G == 0]$id), wald_previos_p = w$p,
             media_base = media_base(dt, r))]
  guardar_tabla(out, paste0("fase3_twfe_elecciones_", r))
  print(out[, .(modelo, termino, coef = round(coef, 3), ee = round(ee, 3), p = signif(p, 3),
                wald_previos_p = signif(wald_previos_p, 3))])
  invisible(out)
}

elecciones_robustez <- function(r) {
  robustez_escalonado("municipio_elecciones", r)
  lee <- function(panel = "municipio_elecciones", res = r, ...) {
    leer_panel(panel, diseno = "escalonado", resultado = res, ...)
  }
  neto <- paste0(r, "_neto")
  nivel <- paste0(r, "_2015")
  filas <- list(
    variante("resultado neto de la media estado × elección", lee(res = neto), neto),
    variante("con el nivel de 2015 como covariable", lee(res = c(r, nivel)), r,
             covs = c(PARAMS$covariables_previas, nivel)),
    variante("sin el filtro de lista nominal (todos los municipios)",
             lee(panel = "municipio_elecciones_todos"), r),
    variante("G observado (modelo Portafolio 2022+)",
             lee(panel = "municipio_elecciones_obs", excluir_sospechosos = FALSE), r)
  )
  # La variante neta tiene media ≈ 0: su porcentaje se expresa sobre la media del original.
  if (!is.null(filas[[1]])) filas[[1]]$media_base <- media_base(con_resultado(lee(), r), r)
  guardar_extra(filas, "municipio_elecciones", r)
  twfe_elecciones(r)
  message("\n#### elecciones dosis: ", r)
  dosis <- subgrupos("municipio_elecciones", r, "exposicion_ce", c("temprana", "tardía"), TRUE)
  guardar_tabla(dosis, paste0("fase3_dosis_elecciones_", r))
  honest("municipio_elecciones", r, "escalonado", periodos_post = 1, variante = "elecciones")
}

elecciones <- function() {
  if (!existe_panel("municipio_elecciones")) {
    return(message("sin panel_municipio_elecciones: se salta"))
  }
  principales <- correr_bloque("municipio_elecciones", F3$elecciones$familia_rw, "elecciones",
                               "elecciones")
  secundarios <- correr_bloque("municipio_elecciones", F3$elecciones$secundarios, "elecciones",
                               "elecciones_secundarios")
  guardar_tabla(rbindlist(list(principales, secundarios), fill = TRUE), "fase3_elecciones")
  for (r in F3$elecciones$familia_rw) elecciones_robustez(r)
}

#' Diagnóstico descriptivo preregistrado (no causal): entre los municipios tratados, ¿la fecha de
#' apertura se adelanta donde el bloque o la participación eran altos en 2018? Año decimal de
#' apertura contra los niveles de 2018 estandarizados y las covariables previas, sin y con efectos
#' fijos de estado; ee robustos (una fila por municipio).
ubicacion <- function() {
  if (!existe_panel("municipio_elecciones")) return(message("sin panel electoral: se salta"))
  d <- leer_panel("municipio_elecciones",
                  resultado = c("pct_bloque_gobierno", "pct_participacion", "G_trimestre"))
  x <- d[G > 0 & tiempo == 2, .(cve_mun, G_trimestre, pct_bloque_gobierno, pct_participacion,
                                log_poblacion_2020, indice_marginacion_2020,
                                banca_mun_2019 = as.numeric(banca_mun_2019))]
  x[, `:=`(anio_apertura = as.numeric(substr(G_trimestre, 1, 4)) +
             (as.numeric(substr(G_trimestre, 6, 6)) - 1) / 4,
           estado = substr(cve_mun, 1, 2))]
  predictores <- c("pct_bloque_gobierno", "pct_participacion", "log_poblacion_2020",
                   "indice_marginacion_2020", "banca_mun_2019")
  x <- x[stats::complete.cases(x[, ..predictores])]
  for (v in predictores) set(x, j = v, value = as.numeric(scale(x[[v]])))
  lado <- paste(predictores, collapse = " + ")
  modelos <- list(
    "sin efectos fijos" = fixest::feols(stats::as.formula(paste("anio_apertura ~", lado)), x,
                                        vcov = "hetero"),
    "efectos fijos de estado" = fixest::feols(
      stats::as.formula(paste("anio_apertura ~", lado, "| estado")), x, vcov = "hetero")
  )
  out <- rbindlist(lapply(names(modelos), function(m) {
    f <- modelos[[m]]
    ct <- fixest::coeftable(f)
    w <- fixest::wald(f, keep = "pct_bloque_gobierno|pct_participacion", print = FALSE)
    data.table(modelo = m, termino = rownames(ct), coef = ct[, 1], ee = ct[, 2], p = ct[, 4],
               meses = 12 * ct[, 1], n = stats::nobs(f), r2 = fixest::r2(f, "r2"),
               wald_electoral_p = w$p)
  }))
  out <- out[termino != "(Intercept)"]
  out[, de_anio := stats::sd(x$anio_apertura)]
  guardar_tabla(out, "fase3_desc_ubicacion")
  print(out[, .(modelo, termino, meses = round(meses, 2), ee_meses = round(12 * ee, 2),
                p = signif(p, 3), wald_electoral_p = signif(wald_electoral_p, 3))])
  invisible(out)
}

# Resumen: potencia, equivalencia, Romano–Wolf por familia y BH en toda la fase -------------------

resumen <- function() {
  partes <- lapply(c("fase3_delitos", "fase3_elecciones"), function(n) {
    ruta <- file.path(RUTA_TABLAS, paste0(n, ".csv"))
    if (file.exists(ruta)) fread(ruta) else NULL
  })
  cs <- rbindlist(Filter(Negate(is.null), partes), fill = TRUE)
  if (!nrow(cs)) return(message("sin resultados de la fase 3"))
  z90 <- stats::qnorm(0.95)
  cs[, escala := abs(media_base)]
  cs[, `:=`(p = 2 * stats::pnorm(-abs(valor / ee)),
            efecto_pct = 100 * valor / escala,
            mde80_pct = 100 * (stats::qnorm(0.975) + stats::qnorm(0.80)) * ee / escala,
            cota_equivalencia_pct = 100 * (abs(valor) + z90 * ee) / escala)]
  cs[, escala := NULL]
  cs[, nulo_informativo := p >= 0.05 & cota_equivalencia_pct <= PARAMS$estimacion$sesoi_pct]
  cs[, pre_falla := !is.na(pre_wald_p) & pre_wald_p < 0.05]
  cs[, q_bh_fase3 := stats::p.adjust(p, method = "BH")]
  rw <- rbindlist(lapply(c("delitos", "elecciones"), function(f) {
    sub <- cs[familia == f]
    if (nrow(sub) < 1) return(NULL)
    romano_wolf(sub$etiqueta, sub$valor)[, familia := f]
  }))
  if (nrow(rw)) cs <- merge(cs, rw[, .(etiqueta, p_rw)], by = "etiqueta", all.x = TRUE)
  cs[, lectura := fcase(pre_falla, "descriptivo (pre-prueba falla)",
                        nulo_informativo, "nulo informativo",
                        p < 0.05 & q_bh_fase3 < 0.05, "significativo (sobrevive BH)",
                        p < 0.05, "significativo sin corrección (BH q ≥ 0.05)",
                        default = "no informativo")]
  guardar_tabla(cs, "fase3_resumen")
  print(cs[, .(familia, resultado, tratadas = n_tratadas, att = round(valor, 4), ee = round(ee, 4),
               efecto_pct = round(efecto_pct, 1), cota = round(cota_equivalencia_pct, 1),
               wald_p = round(pre_wald_p, 3), p_rw = round(p_rw, 3), lectura)])
  invisible(cs)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { delitos(); elecciones(); ubicacion(); resumen() },
         delitos = delitos(),
         elecciones = elecciones(),
         ubicacion = ubicacion(),
         resumen = resumen(),
         stop("uso: Rscript analisis/11_fase3.R todo | delitos | elecciones | ubicacion | resumen"))
}

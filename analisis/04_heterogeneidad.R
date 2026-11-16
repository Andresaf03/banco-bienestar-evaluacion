# 04_heterogeneidad.R — Heterogeneidad del efecto.
#
# Uso:
#   Rscript analisis/04_heterogeneidad.R todo                          # lo preregistrado
#   Rscript analisis/04_heterogeneidad.R <panel> <resultado> [dimension]
#
# Dimensiones (preregistro en docs/decisiones.md, 2026-09-29):
#   desierto_bancario        municipio sin sucursal de banca múltiple en 2019T1 (BDIF; antes salía
#                            del SCIAN 52 del DENUE, con rupturas de cobertura de hasta +41%)
#   grado_marginacion_2020   CONAPO: Muy bajo/Bajo vs Medio vs Alto/Muy alto
#   tamano_localidad         terciles de población del Censo 2020
#   exposicion               (diseño entre actualizaciones) aperturas hasta 2022S2 contra 2023S1–
#                            2024S1: si hay efecto, debería crecer con el tiempo de exposición antes
#                            de la actualización 2024S2. Las dos submuestras comparten controles, así
#                            que la prueba de la diferencia (que ignora esa covarianza positiva) es
#                            conservadora.
#
# Método: la misma especificación de 02_cs_did.R por submuestra, con el estimando principal y su ee
# agrupado por municipio. Cada submuestra conserva su propio contrafactual. La diferencia de cada
# grupo contra el primero se prueba con z; los q-values de Benjamini–Hochberg sobre todas las
# diferencias los calcula 07_inferencia.R.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
suppressPackageStartupMessages({
  library(did)
  library(ggplot2)
})

DIMENSIONES <- c("desierto_bancario", "grado_marginacion_2020", "tamano_localidad", "exposicion")
DENUE_PRINCIPALES <- c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")
# Pregunta 2 de la propuesta: ¿el efecto financiero es mayor donde no había banca? (fase 0)
DIMENSIONES_FINANCIERAS <- c("desierto_bancario", "grado_marginacion_2020", "tamano_localidad")
FINANCIERA_PRINCIPALES <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
EACP_HETEROGENEIDAD <- c("capt_ahorro_eacp_pc", "cred_consumo_eacp_pc")
# Fase 1: dosis en los Censos Económicos (aperturas hasta 2022T2 contra 2022T3–2023T4) y
# desierto bancario en el empleo formal y en los censos.
CE_HETEROGENEIDAD <- c("ue_pc", "personal_ocupado_pc")
IMSS_HETEROGENEIDAD <- c("ta_pc", "ta_micro_pc")

#' Grupo de cada fila según la dimensión pedida.
grupos_de <- function(dt, dimension) {
  if (dimension == "exposicion") {
    g <- dt$G_original
    return(fcase(g == 0, "control",
                 g <= PARAMS$estimacion$actualizaciones$temprana_max, "temprana (hasta 2022S2)",
                 default = "tardía (2023S1–2024S1)"))
  }
  if (dimension == "exposicion_ce") return(as.character(dt$exposicion_ce))
  if (dimension == "tamano_localidad") {
    # Localidad: población del Censo 2020; municipio trimestral: la del municipio.
    pob <- if ("pobtot" %in% names(dt)) dt$pobtot else dt$poblacion_2020
    u <- unique(data.table(id = dt$id, pob = pob))
    cortes <- stats::quantile(u$pob, probs = c(0, 1/3, 2/3, 1), names = FALSE)
    return(as.character(cut(pob, breaks = cortes, include.lowest = TRUE,
                            labels = c("chica", "mediana", "grande"))))
  }
  if (dimension == "grado_marginacion_2020") {
    v <- dt[[dimension]]
    return(fcase(v %in% c("Muy bajo", "Bajo"), "baja marginación",
                 v == "Medio", "marginación media",
                 v %in% c("Alto", "Muy alto"), "alta marginación",
                 default = NA_character_))
  }
  if (!dimension %in% names(dt)) stop("el panel no tiene la columna '", dimension, "'")
  as.character(dt[[dimension]])
}

por_subgrupo <- function(panel, resultado, dimension, diseno = NULL, min_tratadas = 20,
                         ventana = NULL, variante = NULL) {
  dt <- con_resultado(leer_panel(panel, diseno = diseno, resultado = resultado, ventana = ventana),
                      resultado)
  diseno <- attr(dt, "diseno")
  if (dimension == "exposicion" && !identical(diseno, "actualizaciones")) {
    stop("la heterogeneidad por exposición solo aplica al diseño entre actualizaciones")
  }
  dt[, grupo_het := grupos_de(dt, dimension)]
  grupos <- setdiff(sort(unique(na.omit(dt$grupo_het))), "control")

  filas <- list()
  for (g in grupos) {
    # En las dimensiones de exposición los controles son comunes a ambos grupos de tratadas.
    sub <- if (dimension %in% c("exposicion", "exposicion_ce")) {
      dt[grupo_het %in% c("control", g)]
    } else {
      dt[grupo_het == g]
    }
    for (a in c("panel_nombre", "panel_id", "diseno")) setattr(sub, a, attr(dt, a))
    n_trat <- uniqueN(sub[G > 0]$id)
    if (n_trat < min_tratadas) {
      message(sprintf("  grupo '%s': %d tratadas — muy pocas, se omite", g, n_trat))
      next
    }
    # En submuestras chicas el logit de propensión puede quedarse sin controles suficientes (did:
    # "singular matrix"); entonces se reintenta sin covariables y la fila queda marcada.
    estima <- function(covariables) {
      fit <- estimar_attgt(sub, resultado, covariables = covariables)
      est <- estimando_principal(fit, sub)
      data.table(dimension = dimension, grupo = g, unidades = uniqueN(sub$id), tratadas = n_trat,
                 att = est$att, ee = est$ee, media_base = media_base(sub, resultado),
                 covariables = covariables)
    }
    res <- tryCatch(estima(TRUE), error = function(e) {
      message(sprintf("  grupo '%s' falló con covariables (%s); se reintenta sin ellas",
                      g, conditionMessage(e)))
      tryCatch(estima(FALSE), error = function(e2) {
        message(sprintf("  grupo '%s' falló: %s", g, conditionMessage(e2))); NULL
      })
    })
    if (!is.null(res)) filas[[length(filas) + 1]] <- res
  }
  out <- rbindlist(filas, fill = TRUE)
  if (!nrow(out)) return(invisible(out))
  ref <- out[1]
  out[, `:=`(panel = panel, diseno = diseno, resultado = resultado,
             ic_bajo = att - stats::qnorm(0.975) * ee, ic_alto = att + stats::qnorm(0.975) * ee,
             referencia = ref$grupo,
             dif_vs_ref = att - ref$att,
             z_dif = (att - ref$att) / sqrt(ee^2 + ref$ee^2))]
  out[1, `:=`(dif_vs_ref = NA_real_, z_dif = NA_real_)]
  out[, p_dif := 2 * stats::pnorm(-abs(z_dif))]
  etiqueta <- paste0(etiqueta_de(panel, diseno, resultado, variante), "_", dimension)
  guardar_tabla(out, paste0("het_", etiqueta))
  print(out[, .(grupo, tratadas, att = round(att, 4), ee = round(ee, 4), p_dif = round(p_dif, 3))])
  invisible(out)
}

heterogeneidad_denue <- function() {
  for (r in DENUE_PRINCIPALES) {
    for (d in DIMENSIONES) {
      message("\n== heterogeneidad ", r, " por ", d)
      try(por_subgrupo("localidad", r, d, "actualizaciones"), silent = FALSE)
    }
  }
}

heterogeneidad_financiera <- function() {
  for (d in DIMENSIONES_FINANCIERAS) {
    for (r in FINANCIERA_PRINCIPALES) {
      message("\n== heterogeneidad ", r, " por ", d)
      try(por_subgrupo("municipio_trim", r, d, "escalonado"), silent = FALSE)
    }
    for (r in EACP_HETEROGENEIDAD) {
      message("\n== heterogeneidad ", r, " por ", d)
      try(por_subgrupo("municipio_trim", r, d, "escalonado", ventana = c(1L, 28L),
                       variante = "eacp"), silent = FALSE)
    }
  }
}

heterogeneidad_fase1 <- function() {
  for (r in CE_HETEROGENEIDAD) {
    for (d in c("exposicion_ce", "desierto_bancario")) {
      message("\n== heterogeneidad ", r, " por ", d)
      try(por_subgrupo("municipio_ce", r, d, "escalonado", variante = "ce"), silent = FALSE)
    }
  }
  for (r in IMSS_HETEROGENEIDAD) {
    message("\n== heterogeneidad ", r, " por desierto_bancario")
    try(por_subgrupo("municipio_trim", r, "desierto_bancario", "escalonado",
                     ventana = c(1L, 28L), variante = "imss"), silent = FALSE)
  }
}

heterogeneidad_todo <- function() {
  heterogeneidad_denue()
  heterogeneidad_financiera()
  heterogeneidad_fase1()
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) >= 1 && args[1] %in% c("todo", "denue", "financiero", "fase1")) {
    switch(args[1], todo = heterogeneidad_todo(), denue = heterogeneidad_denue(),
           financiero = heterogeneidad_financiera(), fase1 = heterogeneidad_fase1())
  } else {
    if (length(args) < 2) {
      stop("uso: Rscript analisis/04_heterogeneidad.R todo | <panel> <resultado> [dimension]")
    }
    dims <- if (length(args) >= 3) args[3] else DIMENSIONES
    for (d in dims) try(por_subgrupo(args[1], args[2], d), silent = FALSE)
  }
}

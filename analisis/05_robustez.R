# 05_robustez.R — Robustez, contraste de diseños y sensibilidad de Rambachan y Roth.
#
# Uso:
#   Rscript analisis/05_robustez.R todo                              # lo preregistrado
#   Rscript analisis/05_robustez.R <panel> <resultado> [diseno]      # una especificación
#
# Todo lo que corre `todo` está preregistrado en docs/decisiones.md (2026-09-29):
#   1. Variantes de la especificación principal (DENUE, localidad, entre actualizaciones) para los
#      tres resultados principales: grupo de control (≥5 km, ≥20 km, municipal, todos, solo con
#      sucursal), covariables (sin nivel previo, sin covariables), piso de 1,000 habitantes, post en
#      2025S1, fechas ambiguas incluidas, cluster por estado y muestra emparejada.
#   2. Contraste de diseños para esos tres resultados: panel completo con CS (B1) y con TWFE, Sun y
#      Abraham y Borusyak et al. con efectos fijos semestre × decil de tamaño (B2); Goodman-Bacon
#      del TWFE en la ventana escalonada.
#   3. Variantes del diseño escalonado (localidad y BDIF): anticipación δ = 1, nunca tratados como
#      control, cohortes de 30 o más y cluster por estado; en la BDIF, sin los municipios con
#      cierres (P-9, 2026-10-02).
#   4. HonestDiD (Rambachan y Roth 2023) con periodo base **universal**: con base "varying" los
#      coeficientes previos son diferencias consecutivas y la restricción de magnitudes relativas no
#      se interpreta. Σ es la varianza agrupada por municipio de la función de influencia.
#
# Salidas: outputs/tablas/rob_<etiqueta>.csv, rob_disenos_<resultado>.csv, bacon_<etiqueta>.csv y
# rob_honest_<etiqueta>.csv.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
source(here::here("analisis", "03_twfe_comparacion.R"))
suppressPackageStartupMessages({
  library(did)
  library(HonestDiD)
})

DENUE_PRINCIPALES <- c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")
FINANCIERA_PRINCIPALES <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
EACP_LARGAS <- c("capt_ahorro_eacp_pc", "capt_plazo_eacp_pc", "capt_vista_eacp_pc",
                 "cred_consumo_eacp_pc", "cred_vivienda_eacp_pc", "tarjetas_debito_eacp_pc")
VENTANA_2025 <- c(1L, 28L)
# Fase 1: principales de cada fuente nueva.
FASE1 <- list(
  list(panel = "municipio_trim", resultado = "ta_pc", ventana = VENTANA_2025, variante = "imss"),
  list(panel = "municipio_trim", resultado = "ta_micro_pc", ventana = VENTANA_2025,
       variante = "imss"),
  list(panel = "municipio_trim", resultado = "remesas_usd_adulto", ventana = VENTANA_2025,
       variante = "remesas"),
  list(panel = "municipio_ce", resultado = "ue_pc", ventana = NULL, variante = "ce"),
  list(panel = "municipio_ce", resultado = "personal_ocupado_pc", ventana = NULL, variante = "ce")
)

#' Una variante: estima CS sobre `dt` y devuelve el estimando principal con su ee agrupado.
variante <- function(nombre, dt, resultado, ...) {
  tryCatch({
    dt <- con_resultado(dt, resultado)
    fit <- estimar_attgt(dt, resultado, ...)
    est <- estimando_principal(fit, dt)
    previa <- prueba_previa(fit, dt)
    data.table(variante = nombre, termino = est$termino,
               unidades = uniqueN(dt$id), tratadas = uniqueN(dt[G > 0]$id),
               controles = uniqueN(dt[G == 0]$id), clusters = uniqueN(dt$cluster),
               att = est$att, ee = est$ee, ee_boot = est$ee_boot,
               media_base = media_base(dt, resultado),
               pre_n = previa$n, pre_sig = previa$n_sig, pre_wald_p = previa$wald_p)
  }, error = function(e) {
    message("  '", nombre, "' falló: ", conditionMessage(e)); NULL
  })
}

#' Muestra emparejada que deja `make matching` (tratadas emparejadas y sus controles).
ids_emparejados <- function(panel, resultado) {
  ruta <- file.path(RUTA_PANELES, paste0("matching_", panel, "_", resultado, ".parquet"))
  if (!file.exists(ruta)) return(NULL)
  m <- as.data.table(arrow::read_parquet(ruta))
  unique(m[[PANELES[[panel]]$id]])
}

guardar_variantes <- function(filas, panel, diseno, resultado) {
  out <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
  if (!nrow(out)) return(invisible(out))
  out[, `:=`(panel = panel, diseno = diseno, resultado = resultado,
             ic_bajo = att - stats::qnorm(0.975) * ee, ic_alto = att + stats::qnorm(0.975) * ee)]
  etiqueta <- etiqueta_de(panel, diseno, resultado)
  guardar_tabla(out, paste0("rob_", etiqueta))
  print(out[, .(variante, tratadas, controles, att = round(att, 4), ee = round(ee, 4),
                pre = paste0(pre_sig, "/", pre_n), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

#' 1. Variantes de la especificación principal (diseño entre actualizaciones, localidad).
robustez_actualizaciones <- function(resultado, panel = "localidad") {
  lee <- function(...) leer_panel(panel, diseno = "actualizaciones", resultado = resultado, ...)
  sin_previo <- setdiff(PARAMS$covariables_previas, "log1p_estab_previos")
  alternativas <- PARAMS$estimacion$controles$alternativas
  emparejados <- ids_emparejados(panel, resultado)
  filas <- c(
    list(variante("base (≥10 km, DR, cluster municipal)", lee(), resultado)),
    lapply(alternativas, function(k) {
      variante(paste("controles:", k), lee(controles = k), resultado)
    }),
    list(
      variante("sin nivel previo del resultado", lee(), resultado, covs = sin_previo),
      variante("sin covariables", lee(), resultado, covariables = FALSE),
      variante("piso simétrico de 1,000 habitantes", lee(piso_poblacion = 1000), resultado),
      variante("post en 2025S1",
               lee(periodos_act = PARAMS$estimacion$actualizaciones$periodos_robustez), resultado),
      variante("incluye fechas ambiguas y sospechosas",
               lee(excluir_ambiguas = FALSE, excluir_sospechosos = FALSE), resultado),
      variante("cluster por estado", lee(cluster_por = "cve_ent"), resultado),
      if (!is.null(emparejados)) {
        variante("muestra emparejada (matching)", lee(ids = emparejados), resultado)
      } else {
        message("  sin muestra emparejada para ", resultado, ": corre `make matching`"); NULL
      }
    )
  )
  guardar_variantes(filas, panel, "actualizaciones", resultado)
}

#' 3. Variantes del diseño escalonado (ventana en el DENUE; en la BDIF la ventana de la
#' especificación, que para las series de la fase 0 llega a 2025T4). En la BDIF se agrega el
#' pre-periodo desde 2016 (panel largo) para las series sin el escalón de Compartamos: EACP.
robustez_escalonado <- function(panel, resultado, ventana = NULL) {
  lee <- function(...) {
    leer_panel(panel, diseno = "escalonado", resultado = resultado, ventana = ventana, ...)
  }
  largo <- panel == "municipio_trim" && (resultado %in% EACP_LARGAS ||
                                           resultado == "sucursales_eacp_pc")
  filas <- list(
    variante("base (aún no tratados, δ=0, DR)", lee(), resultado),
    variante("anticipación δ=1", lee(), resultado, anticipacion = 1),
    variante("solo nunca tratados como control", lee(), resultado, control = "nevertreated"),
    variante("sin covariables", lee(), resultado, covariables = FALSE),
    variante("cohortes de 30 unidades o más", lee(min_cohorte = 30), resultado),
    variante("incluye fechas ambiguas y sospechosas",
             lee(excluir_ambiguas = FALSE, excluir_sospechosos = FALSE), resultado),
    variante("cluster por estado", lee(cluster_por = "cve_ent"), resultado),
    if (panel == "localidad") variante("controles: todos", lee(controles = "todos"), resultado),
    if (panel == "localidad") {
      variante("controles: solo con sucursal", lee(controles = "solo_sucursal"), resultado)
    },
    if (panel == "municipio_trim") {
      variante("sin municipios con cierres (P-9)", lee(ids = municipios_sin_cierre()), resultado)
    },
    if (panel == "municipio_trim") {
      variante("incluye cohortes de menos de 5 unidades", lee(min_cohorte = NULL), resultado)
    },
    if (largo) {
      variante("pre-periodo desde 2016 (panel largo, hasta 2025T4)",
               leer_panel("municipio_trim_largo", diseno = "escalonado", resultado = resultado),
               resultado)
    }
  )
  guardar_variantes(filas, panel, "escalonado", resultado)
}

#' 2. Contraste de diseños para un resultado del DENUE: ¿están justificadas las alternativas a la
#' principal? B1 = panel completo con CS (su agregación por calendario queda en cs_agg_*_comp_*);
#' B2 = panel completo con efectos fijos semestre × decil de tamaño; Goodman-Bacon del TWFE de la
#' ventana escalonada. La ventana escalonada (A) ya está en la maestra.
contraste_disenos <- function(resultado, panel = "localidad") {
  completo <- con_resultado(leer_panel(panel, diseno = "completo", resultado = resultado), resultado)
  b1 <- correr(panel, resultado, dt = completo, figura = TRUE)
  b2 <- resumir(panel, resultado, dt = completo, cs = b1$fila, fe_tamano = TRUE)
  esc <- con_resultado(leer_panel(panel, diseno = "escalonado", resultado = resultado), resultado)
  bacon_resumen(esc, resultado, etiqueta_de(panel, "escalonado", resultado))
  out <- rbindlist(list(
    b1$fila[, .(diseno = "B1 panel completo", estimador, valor, ee, pre_sig, pre_n, pre_wald_p)],
    b2[estimador != "Callaway y Sant'Anna",
       .(diseno = "B2 panel completo + FE semestre × decil", estimador, valor, ee)]
  ), fill = TRUE)
  out[, resultado := resultado]
  guardar_tabla(out, paste0("rob_disenos_", panel, "_", resultado))
  print(out)
  invisible(out)
}

#' 4. Sensibilidad de Rambachan y Roth sobre el estudio de evento con periodo base universal.
#'
#' `Mbar` acota la violación de tendencias paralelas en el post como múltiplo de la mayor violación
#' entre periodos previos consecutivos. En el diseño entre actualizaciones los previos son 2016S1 y
#' 2019S1 contra la referencia 2019S2, así que la violación de referencia incluye el salto de la
#' actualización 2019S2: justo la amenaza (composición de la actualización) que importa acotar.
#' El objetivo es ATT(g, post) en ese diseño y el promedio de los tres primeros post en el
#' escalonado.
honest <- function(panel, resultado, diseno = NULL, periodos_post = 3,
                   mbar = c(0, 0.25, 0.5, 1, 1.5, 2), ventana = NULL, variante = NULL, ...) {
  # `...` pasa filtros a leer_panel() (p. ej. `regimen` en 08_disenos_alternativos.R).
  dt <- con_resultado(leer_panel(panel, diseno = diseno, resultado = resultado, ventana = ventana,
                                 ...),
                      resultado)
  diseno <- attr(dt, "diseno")
  etiqueta <- etiqueta_de(panel, diseno, resultado, variante)
  fit <- estimar_attgt(dt, resultado, base_period = "universal")
  ag <- did::aggte(fit, type = "dynamic", na.rm = TRUE, cband = FALSE)
  cl <- cluster_if(fit, dt)
  e <- ag$egt
  if (identical(diseno, "actualizaciones")) {
    g <- PARAMS$estimacion$actualizaciones$g
    referencia <- max(dt$tiempo[dt$tiempo < g]) - g
  } else {
    referencia <- -1
  }
  conservar <- e != referencia
  beta <- ag$att.egt[conservar]
  sigma <- varianza_cluster(ag$inf.function$dynamic.inf.func.e[, conservar, drop = FALSE], cl)
  e <- e[conservar]
  pre <- sum(e < 0)
  post <- sum(e >= 0)
  if (pre < 1 || post < 1) {
    message("  HonestDiD necesita al menos un periodo previo y uno posterior")
    return(invisible(NULL))
  }
  l_vec <- if (identical(diseno, "actualizaciones")) {
    as.numeric(e[e >= 0] == max(dt$tiempo) - PARAMS$estimacion$actualizaciones$g)
  } else {
    usar <- min(periodos_post, post)
    c(rep(1 / usar, usar), rep(0, post - usar))
  }
  # La malla por defecto de HonestDiD se queda corta cuando M̄ crece y el IC sale "abierto": se
  # amplía en proporción al ee del objetivo y al tamaño de los coeficientes previos.
  ee_objetivo <- sqrt(drop(crossprod(l_vec, sigma[-(1:pre), -(1:pre)] %*% l_vec)))
  objetivo <- sum(l_vec * beta[-(1:pre)])
  mitad <- 10 * max(mbar, 1) * (ee_objetivo + max(abs(beta)))
  res <- tryCatch(
    HonestDiD::createSensitivityResults_relativeMagnitudes(
      betahat = beta, sigma = sigma, numPrePeriods = pre, numPostPeriods = post,
      l_vec = l_vec, Mbarvec = mbar, grid.lb = objetivo - mitad, grid.ub = objetivo + mitad
    ),
    error = function(err) { message("  HonestDiD falló: ", conditionMessage(err)); NULL }
  )
  if (is.null(res)) return(invisible(NULL))
  original <- HonestDiD::constructOriginalCS(
    betahat = beta, sigma = sigma, numPrePeriods = pre, numPostPeriods = post, l_vec = l_vec
  )
  out <- rbind(as.data.table(res), as.data.table(original), fill = TRUE)
  out[, `:=`(etiqueta = etiqueta, panel = panel, diseno = diseno, resultado = resultado,
             referencia_e = referencia)]
  guardar_tabla(out, paste0("rob_honest_", etiqueta))
  print(out)
  invisible(out)
}

#' Lo preregistrado para el DENUE.
robustez_denue <- function() {
  for (r in DENUE_PRINCIPALES) {
    message("\n#### robustez principal: ", r)
    robustez_actualizaciones(r)
    message("\n#### contraste de diseños: ", r)
    contraste_disenos(r)
    honest("localidad", r, "actualizaciones")
  }
  message("\n#### escalonado: localidad / emprendimiento")
  robustez_escalonado("localidad", DENUE_PRINCIPALES[1])
  honest("localidad", DENUE_PRINCIPALES[1], "escalonado")
}

#' Lo preregistrado para el bloque financiero, con la ampliación de la fase 0 (EACP hasta 2025T4).
robustez_financiera <- function() {
  for (r in FINANCIERA_PRINCIPALES) {
    message("\n#### financiera: ", r)
    robustez_escalonado("municipio_trim", r)
    honest("municipio_trim", r, "escalonado")
  }
  for (r in EACP_LARGAS) {
    message("\n#### EACP: ", r)
    robustez_escalonado("municipio_trim", r, ventana = VENTANA_2025)
    honest("municipio_trim", r, "escalonado", ventana = VENTANA_2025, variante = "eacp")
  }
}

robustez_fase1 <- function() {
  for (e in FASE1) {
    message("\n#### fase 1: ", e$panel, " / ", e$resultado)
    robustez_escalonado(e$panel, e$resultado, ventana = e$ventana)
    honest(e$panel, e$resultado, "escalonado", ventana = e$ventana, variante = e$variante)
  }
}

#' Solo la robustez escalonada de los tres resultados financieros principales (incluye la variante
#' sin cierres, P-9): `Rscript analisis/05_robustez.R cierres`.
robustez_cierres <- function() {
  for (r in FINANCIERA_PRINCIPALES) {
    message("\n#### financiera (con la variante sin cierres): ", r)
    robustez_escalonado("municipio_trim", r)
  }
}

robustez_todo <- function() {
  robustez_denue()
  robustez_financiera()
  robustez_fase1()
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) >= 1 && args[1] %in% c("todo", "denue", "financiero", "fase1", "cierres")) {
    switch(args[1], todo = robustez_todo(), denue = robustez_denue(),
           financiero = robustez_financiera(), fase1 = robustez_fase1(),
           cierres = robustez_cierres())
  } else {
    if (length(args) < 2) stop("uso: Rscript analisis/05_robustez.R todo | <panel> <resultado> [diseno]")
    diseno <- if (length(args) >= 3) args[3] else diseno_por_defecto(args[1])
    if (diseno == "actualizaciones") robustez_actualizaciones(args[2], args[1])
    else robustez_escalonado(args[1], args[2])
    honest(args[1], args[2], diseno)
  }
}

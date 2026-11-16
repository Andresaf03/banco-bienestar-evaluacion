# 02_cs_did.R — Estimación principal: Callaway y Sant'Anna (2021) con el paquete `did`.
#
# Uso:
#   Rscript analisis/02_cs_did.R <panel> <resultado> [diseno]
#   Rscript analisis/02_cs_did.R localidad estab_emprendimiento_pc               # principal
#   Rscript analisis/02_cs_did.R localidad estab_emprendimiento_pc escalonado
#   Rscript analisis/02_cs_did.R municipio_trim sucursales_privado_pc
#
# Diseño (config/parametros.yaml, preregistro en docs/decisiones.md):
#   - Unidad: localidad / municipio, según el panel.
#   - G: primer periodo con sucursal del Banco del Bienestar (neta de Banjército); 0 = nunca.
#   - DENUE: diseño entre actualizaciones integrales (una cohorte, estimando ATT(g, post)); BDIF:
#     escalonado (estimando: ATT global θ^O_sel).
#   - Control: aún no tratados; en localidades, solo las que están lejos de toda sucursal.
#   - Estimador doblemente robusto con covariables PREVIAS al tratamiento.
#   - Inferencia: error estándar de Liang–Zeger por municipio sobre la función de influencia. El
#     bootstrap agrupado de `did` promedia la función de influencia **por cluster** y con
#     municipios de tamaños muy distintos no coincide con la varianza agrupada del estimador; se
#     conserva como `ee_boot` y para las bandas simultáneas de las figuras.
#
# Salidas: outputs/tablas/cs_{attgt,agg}_<etiqueta>.csv, outputs/figuras/event_<etiqueta>.png y la
# función de influencia agrupada en outputs/intermedios/if_<etiqueta>.csv (Romano–Wolf).

source(here::here("analisis", "00_utils.R"))
suppressPackageStartupMessages({
  library(did)
  library(ggplot2)
})

ABREVIATURA_DISENO <- c(actualizaciones = "act", escalonado = "esc", completo = "comp")

etiqueta_de <- function(panel, diseno, resultado, variante = NULL, radio = NULL) {
  paste(c(panel, ABREVIATURA_DISENO[[diseno]], variante, resultado,
          if (!is.null(radio)) paste0("r", radio)), collapse = "_")
}

#' Estima ATT(g,t) con la especificación base del proyecto.
estimar_attgt <- function(dt, resultado, control = "notyettreated", anticipacion = 0,
                          covariables = TRUE, covs = NULL, base_period = "varying",
                          metodo = PARAMS$estimacion$metodo) {
  xformla <- if (covariables) formula_covariables(dt, covs) else ~1
  # did 2.3 (modo rápido) admite un solo nombre en `clustervars`: el del cluster, o el id cuando la
  # unidad ya es el municipio. La ruta clásica (`faster_mode = FALSE`) falla en este entorno dentro
  # de DRDID/fastglm.
  clustervars <- if (any(dt$cluster != dt$id)) "cluster" else "id"
  did::att_gt(
    yname                  = resultado,
    tname                  = "tiempo",
    idname                 = "id",
    gname                  = "G",
    xformla                = xformla,
    data                   = as.data.frame(dt),
    panel                  = TRUE,
    allow_unbalanced_panel = FALSE,
    control_group          = control,
    anticipation           = anticipacion,
    est_method             = metodo,
    base_period            = base_period,
    bstrap                 = PARAMS$estimacion$bootstrap,
    biters                 = PARAMS$estimacion$n_boot,
    cband                  = PARAMS$estimacion$bandas_simultaneas,
    clustervars            = clustervars,
    alp                    = 0.05,
    print_details          = FALSE
  )
}

# Inferencia sobre la función de influencia ------------------------------------------------------

#' Cluster de cada fila de la función de influencia. Replica lo que hace el bootstrap de `did`
#' (`did:::mboot`): las filas siguen el orden de las unidades en el primer periodo de
#' `DIDparams$data`.
cluster_if <- function(fit, dt) {
  d <- as.data.frame(fit$DIDparams$data)
  primero <- d[d$tiempo == min(d$tiempo), "id"]
  if (length(primero) != nrow(fit$inffunc)) {
    stop("la función de influencia no tiene una fila por unidad del primer periodo")
  }
  mapa <- unique(dt[, .(id, cluster)])
  mapa[match(primero, mapa$id), cluster]
}

#' Varianza de Liang–Zeger: θ̂ − θ ≈ (1/n) Σ ψ_i, así que V = Σ_c (Σ_{i∈c} ψ_i)(·)' / n².
varianza_cluster <- function(psi, cluster) {
  psi <- as.matrix(psi)
  s <- rowsum(psi, cluster)
  crossprod(s) / nrow(psi)^2
}

#' Estimando principal de la especificación, con su función de influencia.
#'   - diseño entre actualizaciones: ATT(g, post), la celda de la actualización posterior;
#'   - escalonado o completo: ATT global θ^O_sel (`aggte(type = "group")`).
estimando_principal <- function(fit, dt, ag_grupo = NULL) {
  diseno <- attr(dt, "diseno")
  cl <- cluster_if(fit, dt)
  if (identical(diseno, "actualizaciones")) {
    g <- PARAMS$estimacion$actualizaciones$g
    post <- max(dt$tiempo)
    k <- which(fit$group == g & fit$t == post)
    if (length(k) != 1) stop("no se estimó ATT(", g, ",", post, ")")
    att <- fit$att[k]
    psi <- as.matrix(fit$inffunc[, k, drop = FALSE])
    ee_boot <- fit$se[k]
    termino <- sprintf("ATT(%d,%d)", g, post)
  } else {
    ag_grupo <- ag_grupo %||% did::aggte(fit, type = "group", na.rm = TRUE)
    att <- ag_grupo$overall.att
    psi <- as.matrix(ag_grupo$inf.function$selective.inf.func)
    ee_boot <- ag_grupo$overall.se
    termino <- "ATT global"
  }
  list(termino = termino, att = att, ee = sqrt(drop(varianza_cluster(psi, cl))),
       ee_boot = ee_boot, psi_c = rowsum(psi, cl)[, 1], n = nrow(psi))
}

#' Pre-prueba de tendencias paralelas con varianza agrupada: cuántos coeficientes previos son
#' significativos uno por uno (5%) y la prueba de Wald conjunta. En el diseño entre actualizaciones
#' los previos son ATT(g, 7) (deriva 2016S1→2019S1) y ATT(g, 8) (salto de la actualización 2019S2,
#' el placebo); en el escalonado, los coeficientes e < 0 del estudio de evento.
prueba_previa <- function(fit, dt, ag_dinamico = NULL) {
  cl <- cluster_if(fit, dt)
  if (identical(attr(dt, "diseno"), "actualizaciones")) {
    g <- PARAMS$estimacion$actualizaciones$g
    k <- which(fit$group == g & fit$t < g & is.finite(fit$se) & fit$se > 0)
    b <- fit$att[k]
    psi <- as.matrix(fit$inffunc[, k, drop = FALSE])
    termino <- as.character(fit$t[k])
  } else {
    ag_dinamico <- ag_dinamico %||% did::aggte(fit, type = "dynamic", na.rm = TRUE)
    k <- which(ag_dinamico$egt < 0 & is.finite(ag_dinamico$se.egt) & ag_dinamico$se.egt > 0)
    b <- ag_dinamico$att.egt[k]
    psi <- as.matrix(ag_dinamico$inf.function$dynamic.inf.func.e[, k, drop = FALSE])
    termino <- as.character(ag_dinamico$egt[k])
  }
  if (!length(b)) {
    return(list(n = 0L, n_sig = NA_integer_, wald_p = NA_real_, coefs = data.table()))
  }
  V <- varianza_cluster(psi, cl)
  ee <- sqrt(diag(V))
  W <- tryCatch(drop(crossprod(b, solve(V, b))), error = function(e) NA_real_)
  list(n = length(b), n_sig = sum(abs(b / ee) > stats::qnorm(0.975)),
       wald_p = stats::pchisq(W, df = length(b), lower.tail = FALSE),
       coefs = data.table(termino = termino, att = b, ee = ee))
}

#' Media del resultado de las tratadas en su último periodo previo: la línea base contra la que se
#' expresan el MDE y la cota de equivalencia en porcentaje.
media_base <- function(dt, resultado) {
  previas <- dt[G > 0 & tiempo < G]
  if (!nrow(previas)) return(NA_real_)
  ultimo <- previas[previas[, .I[which.max(tiempo)], by = id]$V1]
  mean(ultimo[[resultado]], na.rm = TRUE)
}

# Agregaciones y salidas --------------------------------------------------------------------------

#' Agregaciones estándar. `dynamic` es el event study que pidió el asesor. En el diseño entre
#' actualizaciones hay una sola cohorte: el balanceado y el calendario no agregan nada.
agregar <- function(attgt, diseno = "escalonado") {
  seguro <- function(expr) tryCatch(expr, error = function(e) {
    message("  agregación fallida: ", conditionMessage(e)); NULL
  })
  # Con una sola cohorte (diseño entre actualizaciones o Censos Económicos) el evento balanceado y
  # el calendario no agregan nada, y `did` falla al calcularlos.
  escalonado <- !identical(diseno, "actualizaciones") && length(unique(attgt$group)) > 1
  list(
    simple      = seguro(did::aggte(attgt, type = "simple",   na.rm = TRUE)),
    group       = seguro(did::aggte(attgt, type = "group",    na.rm = TRUE)),
    dynamic     = seguro(did::aggte(attgt, type = "dynamic",  na.rm = TRUE)),
    dynamic_bal = if (escalonado) seguro(did::aggte(attgt, type = "dynamic", na.rm = TRUE,
                                                    balance_e = PARAMS$estimacion$balance_e)),
    calendar    = if (escalonado) seguro(did::aggte(attgt, type = "calendar", na.rm = TRUE))
  )
}

#' Convierte un objeto aggte en data.table (bandas simultáneas del bootstrap de `did`).
tabla_aggte <- function(ag, tipo) {
  if (is.null(ag)) return(NULL)
  if (tipo == "simple") {
    data.table(tipo = tipo, termino = "ATT", valor = ag$overall.att,
               ee = ag$overall.se,
               ic_bajo = ag$overall.att - stats::qnorm(0.975) * ag$overall.se,
               ic_alto = ag$overall.att + stats::qnorm(0.975) * ag$overall.se)
  } else {
    data.table(tipo = tipo, termino = as.character(ag$egt), valor = ag$att.egt,
               ee = ag$se.egt,
               ic_bajo = ag$att.egt - ag$crit.val.egt * ag$se.egt,
               ic_alto = ag$att.egt + ag$crit.val.egt * ag$se.egt)
  }
}

#' Corre la especificación completa para un panel y un resultado y guarda todo.
#'
#' `...` pasa a `leer_panel()` (diseno, controles, derrame, ventana, ids…). Devuelve el ajuste, las
#' agregaciones, la muestra y una fila resumen con el estimando principal, su ee agrupado, la
#' pre-prueba y la línea base: esa fila es la que alimenta la tabla maestra.
correr <- function(panel, resultado, radio = NULL, etiqueta = NULL, dt = NULL, variante = NULL,
                   figura = TRUE, ...) {
  dt <- con_resultado(dt %||% leer_panel(panel, radio = radio, resultado = resultado, ...),
                     resultado)
  diseno <- attr(dt, "diseno")
  etiqueta <- etiqueta %||% etiqueta_de(panel, diseno, resultado, variante, radio)
  n_trat <- uniqueN(dt[G > 0]$id)
  message(sprintf("== %s | %d unidades (%d tratadas), %d periodos, %d clusters", etiqueta,
                  uniqueN(dt$id), n_trat, uniqueN(dt$tiempo), uniqueN(dt$cluster)))

  fit <- estimar_attgt(dt, resultado)
  ag  <- agregar(fit, diseno)
  principal <- estimando_principal(fit, dt, ag$group)
  previa <- prueba_previa(fit, dt, ag$dynamic)

  guardar_tabla(data.table(grupo = fit$group, tiempo = fit$t, att = fit$att, ee_boot = fit$se),
                paste0("cs_attgt_", etiqueta))
  resumen <- rbindlist(lapply(names(ag), function(k) tabla_aggte(ag[[k]], k)), fill = TRUE)
  if (nrow(resumen)) {
    resumen[, `:=`(panel = panel, diseno = diseno, resultado = resultado)]
    guardar_tabla(resumen, paste0("cs_agg_", etiqueta))
  }
  if (nrow(previa$coefs)) guardar_tabla(previa$coefs, paste0("cs_previos_", etiqueta))
  guardar_intermedio(data.table(cluster = as.integer(names(principal$psi_c)),
                                psi = unname(principal$psi_c), n = principal$n),
                     paste0("if_", etiqueta))

  if (figura && !is.null(ag$dynamic)) {
    p <- did::ggdid(ag$dynamic) +
      labs(title = paste("Estudio de evento:", resultado),
           subtitle = paste("Panel", panel, "· diseño", diseno),
           x = "Periodos desde la apertura", y = "ATT")
    guardar_figura(p, paste0("event_", etiqueta))
  }

  # Sin coeficientes previos estimables (p. ej. una serie que vale cero antes del tratamiento) no hay
  # placebo que buscar.
  placebo <- if (nrow(previa$coefs)) previa$coefs[termino == "8"] else data.table()
  fila <- data.table(
    etiqueta = etiqueta, panel = panel, diseno = diseno, resultado = resultado,
    estimador = "Callaway y Sant'Anna", termino = principal$termino,
    valor = principal$att, ee = principal$ee, ee_boot = principal$ee_boot,
    n_unidades = uniqueN(dt$id), n_tratadas = n_trat, n_controles = uniqueN(dt[G == 0]$id),
    n_clusters = uniqueN(dt$cluster), media_base = media_base(dt, resultado),
    pre_n = previa$n, pre_sig = previa$n_sig, pre_wald_p = previa$wald_p,
    placebo = if (identical(diseno, "actualizaciones") && nrow(placebo)) placebo$att else NA_real_,
    placebo_ee = if (identical(diseno, "actualizaciones") && nrow(placebo)) placebo$ee else NA_real_
  )
  invisible(list(attgt = fit, agg = ag, dt = dt, fila = fila))
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) < 2) {
    stop("uso: Rscript analisis/02_cs_did.R <panel> <resultado> [diseno]")
  }
  diseno <- if (length(args) >= 3) args[3] else NULL
  print(correr(args[1], args[2], diseno = diseno)$fila)
}

# 03_twfe_comparacion.R — Estimadores alternativos y comparación con TWFE.
#
# Uso:
#   Rscript analisis/03_twfe_comparacion.R <panel> <resultado> [diseno]
#
# Qué compara y por qué:
#   1. TWFE estático: y_it = a_i + b_t + d·D_it + e_it. Con adopción escalonada y efectos
#      heterogéneos, `d` es un promedio con pesos que pueden ser negativos (Goodman-Bacon 2021;
#      de Chaisemartin y D'Haultfœuille 2020): sirve de contraste, no de estimación creíble.
#   2. Sun y Abraham (2021) vía `fixest::sunab()`: interacciones cohorte × tiempo relativo,
#      robusto a heterogeneidad.
#   3. Borusyak, Jaravel y Spiess (2024) por imputación: ATT global (término `treat`).
# En el diseño entre actualizaciones hay una sola cohorte y los tres coinciden con la diferencia en
# diferencias 2×2 sin covariables entre 2019S2 y la actualización posterior; se reporta solo esa.
# Todos agrupan los errores por municipio (`cluster`), igual que el estimador principal.
#
# Salida: outputs/tablas/comp_<etiqueta>.csv con todos los estimadores lado a lado.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
suppressPackageStartupMessages({
  library(fixest)
  library(ggplot2)
})

#' Prepara tiempo y cohorte para `sunab` en posiciones consecutivas de los periodos observados.
#'
#' 2023S1 no existe en el DENUE, así que en la escala semestral la cohorte 16 (la más grande) no
#' tiene periodo relativo −1: `sunab` se quedaba sin referencia para ella y fixest tiraba un
#' coeficiente arbitrario por colinealidad. En posiciones, el periodo previo de cada cohorte es el
#' último observado (2022S2 para la 16), igual que la base de CS. Los nunca tratados reciben un
#' valor fuera del rango.
preparar_cohorte <- function(dt) {
  d <- copy(dt)
  posicion <- setNames(seq_along(sort(unique(d$tiempo))), sort(unique(d$tiempo)))
  d[, tiempo_sa := posicion[as.character(tiempo)]]
  d[, cohorte := fifelse(G > 0, posicion[as.character(G)], 10000)]
  if (anyNA(d$cohorte)) stop("hay cohortes fuera de los periodos observados")
  d[]
}

#' Decil de población de la unidad, para los efectos fijos semestre × tamaño del panel completo:
#' las actualizaciones integrales del DENUE suman más establecimientos donde hay más actividad, y
#' esos efectos fijos permiten que cada tramo de tamaño tenga su propio salto.
con_decil_tamano <- function(dt) {
  u <- unique(dt[, .(id, pobtot)])
  u[, decil_tamano := as.integer(cut(frank(pobtot, ties.method = "first"), 10, labels = FALSE))]
  merge(dt, u[, .(id, decil_tamano)], by = "id")
}

efectos_fijos <- function(fe_tamano) if (fe_tamano) "id + tiempo^decil_tamano" else "id + tiempo"

twfe_estatico <- function(dt, resultado, fe_tamano = FALSE) {
  f <- as.formula(paste(resultado, "~ tratado |", efectos_fijos(fe_tamano)))
  fixest::feols(f, data = dt, cluster = ~cluster)
}

sun_abraham <- function(dt, resultado, fe_tamano = FALSE) {
  d <- preparar_cohorte(dt)
  fe <- sub("tiempo", "tiempo_sa", efectos_fijos(fe_tamano), fixed = TRUE)
  f <- as.formula(paste(resultado, "~ sunab(cohorte, tiempo_sa) |", fe))
  fixest::feols(f, data = d, cluster = ~cluster)
}

bjs_imputacion <- function(dt, resultado, fe_tamano = FALSE) {
  if (!requireNamespace("didimputation", quietly = TRUE)) {
    message("  didimputation no está instalado; se omite Borusyak et al.")
    return(NULL)
  }
  d <- copy(dt)
  d[, g_bjs := fifelse(G > 0, G, NA_real_)]
  # Sin `horizon` el resultado es el ATT global (término `treat`); con `horizon = TRUE` serían los
  # efectos por horizonte y el primero es el de e = 0, que no se compara con el ATT global de CS.
  tryCatch(
    didimputation::did_imputation(
      data = as.data.frame(d), yname = resultado, gname = "g_bjs",
      tname = "tiempo", idname = "id", cluster_var = "cluster",
      first_stage = as.formula(paste("~ 0 |", efectos_fijos(fe_tamano)))
    ),
    error = function(e) { message("  BJS falló: ", conditionMessage(e)); NULL }
  )
}

fila_fixest <- function(modelo, estimador, agg = FALSE) {
  if (is.null(modelo)) return(NULL)
  obj <- if (agg) tryCatch(summary(modelo, agg = "att"), error = function(e) NULL) else modelo
  if (is.null(obj)) return(NULL)
  ct <- as.data.table(coeftable(obj), keep.rownames = "termino")
  fila <- if (agg) ct[termino == "ATT"] else ct[1]
  data.table(estimador = estimador, valor = fila$Estimate, ee = fila$`Std. Error`)
}

#' Los estimadores alternativos de una especificación, en una tabla común.
#'
#' `cs` es la fila que devuelve `correr()`: CS no se vuelve a estimar (antes se estimaba dos veces
#' por especificación, con bootstraps distintos y errores estándar que no coincidían).
#' `fe_tamano = TRUE` agrega efectos fijos semestre × decil de tamaño (contraste B2 del panel
#' completo).
resumir <- function(panel, resultado, dt = NULL, cs = NULL, etiqueta = NULL, fe_tamano = FALSE,
                    ...) {
  dt <- con_resultado(dt %||% leer_panel(panel, resultado = resultado, ...), resultado)
  diseno <- attr(dt, "diseno")
  etiqueta <- etiqueta %||% etiqueta_de(panel, diseno, resultado)
  if (fe_tamano) dt <- con_decil_tamano(dt)
  message(sprintf("== comparación %s | %d unidades", etiqueta, uniqueN(dt$id)))

  filas <- list()
  if (identical(diseno, "actualizaciones")) {
    act <- PARAMS$estimacion$actualizaciones
    base <- max(dt$tiempo[dt$tiempo < act$g])
    d2 <- dt[tiempo %in% c(base, max(tiempo))]
    d2[, tratado := as.integer(G > 0 & tiempo > base)]
    filas[[1]] <- fila_fixest(twfe_estatico(d2, resultado), "DiD 2x2 sin covariables")
  } else {
    filas[[1]] <- fila_fixest(twfe_estatico(dt, resultado, fe_tamano), "TWFE estático")
    sa <- tryCatch(sun_abraham(dt, resultado, fe_tamano), error = function(e) {
      message("  Sun y Abraham falló: ", conditionMessage(e)); NULL
    })
    filas[[2]] <- fila_fixest(sa, "Sun y Abraham", agg = TRUE)
    bjs <- bjs_imputacion(dt, resultado, fe_tamano)
    if (!is.null(bjs) && nrow(bjs)) {
      b <- as.data.table(bjs)[term == "treat"]
      filas[[3]] <- data.table(estimador = "Borusyak et al.", valor = b$estimate, ee = b$std.error)
    }
  }
  if (!is.null(cs)) {
    filas[[length(filas) + 1]] <- cs[, .(estimador, valor, ee)]
  }

  out <- rbindlist(filas, fill = TRUE)
  out[, `:=`(etiqueta = etiqueta, panel = panel, diseno = diseno, resultado = resultado,
             fe_tamano = fe_tamano,
             ic_bajo = valor - stats::qnorm(0.975) * ee,
             ic_alto = valor + stats::qnorm(0.975) * ee)]
  guardar_tabla(out, paste0("comp_", etiqueta, if (fe_tamano) "_fetam"))
  print(out[, .(estimador, valor = round(valor, 5), ee = round(ee, 5))])
  invisible(out)
}

#' Descomposición de Goodman-Bacon (2021, Teorema 1) del TWFE estático.
#'
#' Qué parte del coeficiente viene de comparar tratadas contra nunca tratadas y qué parte de
#' comparaciones "prohibidas" (tratadas tarde contra tratadas antes), que es lo que aparta al TWFE
#' de CS en el diseño escalonado. Se calcula en forma cerrada con las medias cohorte × periodo: en
#' un panel balanceado con efectos fijos de unidad y periodo, cada DiD 2×2 depende solo de esas
#' medias y los pesos solo de los tamaños de cohorte y de la fracción de periodos tratados.
#' `bacondecomp` estima una regresión con una dummy por unidad y no cabe en memoria con 22 mil
#' localidades. La suma ponderada debe reproducir el TWFE; si no, se detiene.
bacon_resumen <- function(dt, resultado, etiqueta) {
  periodos <- sort(unique(dt$tiempo))
  medias <- dcast(dt[, .(m = mean(get(resultado))), by = .(G, tiempo)], G ~ tiempo,
                  value.var = "m")
  M <- as.matrix(medias[, -1])
  rownames(M) <- medias$G
  tam <- dt[!duplicated(id), .N, by = G]
  n <- setNames(tam$N / sum(tam$N), tam$G)
  cohortes <- sort(setdiff(as.numeric(rownames(M)), 0))
  D <- setNames(vapply(cohortes, function(g) mean(periodos >= g), 0), cohortes)
  did2x2 <- function(a, b, ventana, post) {
    fila <- function(g) M[as.character(g), as.character(periodos)]
    dif <- fila(a) - fila(b)
    mean(dif[ventana & post]) - mean(dif[ventana & !post])
  }
  filas <- list()
  if ("0" %in% rownames(M)) {
    for (k in cohortes) {
      nk <- n[[as.character(k)]]; nu <- n[["0"]]; nku <- nk / (nk + nu)
      filas[[length(filas) + 1]] <- data.table(
        type = "Treated vs Untreated", treated = k, untreated = 0,
        estimate = did2x2(k, 0, rep(TRUE, length(periodos)), periodos >= k),
        peso = (nk + nu)^2 * nku * (1 - nku) * D[[as.character(k)]] * (1 - D[[as.character(k)]]))
    }
  }
  for (k in cohortes) for (l in cohortes[cohortes > k]) {
    nk <- n[[as.character(k)]]; nl <- n[[as.character(l)]]; nkl <- nk / (nk + nl)
    Dk <- D[[as.character(k)]]; Dl <- D[[as.character(l)]]
    filas[[length(filas) + 1]] <- data.table(
      type = "Earlier vs Later Treated", treated = k, untreated = l,
      estimate = did2x2(k, l, periodos < l, periodos >= k),
      peso = ((nk + nl) * (1 - Dl))^2 * nkl * (1 - nkl) * ((Dk - Dl) / (1 - Dl)) *
        ((1 - Dk) / (1 - Dl)))
    filas[[length(filas) + 1]] <- data.table(
      type = "Later vs Earlier Treated", treated = l, untreated = k,
      estimate = did2x2(l, k, periodos >= k, periodos >= l),
      peso = ((nk + nl) * Dk)^2 * nkl * (1 - nkl) * (Dl / Dk) * ((Dk - Dl) / Dk))
  }
  b <- rbindlist(filas)
  b[, weight := peso / sum(peso)]
  twfe <- unname(coef(fixest::feols(as.formula(paste(resultado, "~ tratado | id + tiempo")),
                                    data = dt))["tratado"])
  reconstruido <- sum(b$estimate * b$weight)
  if (abs(reconstruido - twfe) > 1e-6 * max(1, abs(twfe))) {
    stop(sprintf("Goodman-Bacon no reproduce el TWFE (%.6f contra %.6f)", reconstruido, twfe))
  }
  out <- b[, .(peso = sum(weight), estimacion = sum(estimate * weight) / sum(weight)), by = type]
  out[, `:=`(etiqueta = etiqueta, resultado = resultado, twfe = twfe)]
  guardar_tabla(b, paste0("bacon_detalle_", etiqueta))
  guardar_tabla(out, paste0("bacon_", etiqueta))
  print(out)
  invisible(out)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) < 2) stop("uso: Rscript analisis/03_twfe_comparacion.R <panel> <resultado> [diseno]")
  diseno <- if (length(args) >= 3) args[3] else NULL
  resumir(args[1], args[2], diseno = diseno)
}

# 07_inferencia.R — Inferencia múltiple, potencia y tabla final con la auditoría de pre-tendencias.
#
# Uso:
#   Rscript analisis/07_inferencia.R
#
# Lee lo que dejan 06_correr_todo.R, 04_heterogeneidad.R y 05_robustez.R, y no estima nada nuevo:
#   - Romano–Wolf (step-down) dentro de cada familia preregistrada (`estimacion.familias_rw`), con
#     bootstrap multiplicador de Rademacher sobre la función de influencia **agrupada por
#     municipio** y pesos comunes a todos los resultados de la familia. Así respeta la correlación
#     entre resultados medidos en las mismas unidades.
#   - q-values de Benjamini–Hochberg sobre todas las especificaciones de la maestra y, aparte, sobre
#     las diferencias de heterogeneidad.
#   - Potencia: MDE al 80% (2.80·ee) y equivalencia (TOST al 5%): la cota del IC al 90% como % de la
#     media previa de las tratadas. "Nulo informativo" solo si esa cota queda dentro de ±sesoi_pct.
#   - Auditoría de pre-tendencias: coeficientes previos significativos (5%, ee agrupado), Wald
#     conjunta y, en el diseño entre actualizaciones, el placebo de la actualización 2019S2.
#   - HonestDiD: IC robusto con M̄ = 1 y el menor M̄ con el que el IC incluye el cero.
#
# Salidas: outputs/tablas/tabla_final.csv, inferencia_romano_wolf.csv, het_q.csv.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))

leer_tablas <- function(patron) {
  archivos <- list.files(RUTA_TABLAS, pattern = patron, full.names = TRUE)
  if (!length(archivos)) return(data.table())
  rbindlist(lapply(archivos, fread), fill = TRUE)
}

#' Romano–Wolf step-down para una familia de estimaciones sobre la misma muestra de clusters.
#'
#' Cada estimación trae θ_k, su función de influencia agrupada ψ_kc y n_k: θ̂_k − θ_k ≈ Σ_c ψ_kc / n_k.
#' Las réplicas son θ*_bk = Σ_c w_bc ψ_kc / n_k con w_bc ∈ {−1, 1} comunes a toda la familia, y el
#' estadístico es |θ*_bk| / ee_k. Romano y Wolf (2005, 2016).
romano_wolf <- function(etiquetas, valores, B = PARAMS$estimacion$n_boot_rw, bloque = 500L) {
  ifs <- lapply(etiquetas, function(e) {
    x <- fread(file.path(RUTA_INTERMEDIOS, paste0("if_", e, ".csv")))
    x[, etiqueta := e]
  })
  ifs <- rbindlist(ifs)
  n <- ifs[, .(n = n[1]), by = etiqueta][match(etiquetas, etiqueta), n]
  psi <- dcast(ifs, cluster ~ etiqueta, value.var = "psi", fill = 0)
  Psi <- as.matrix(psi[, etiquetas, with = FALSE])
  ee <- sqrt(colSums(Psi^2)) / n
  t_obs <- abs(valores) / ee
  set.seed(PARAMS$semillas$r)
  maximos <- matrix(NA_real_, B, length(etiquetas))
  orden <- order(t_obs, decreasing = TRUE)
  hechas <- 0L
  while (hechas < B) {
    m <- min(bloque, B - hechas)
    W <- matrix(sample(c(-1, 1), m * nrow(Psi), replace = TRUE), m, nrow(Psi))
    t_boot <- abs(sweep(W %*% Psi, 2, n, "/")) / rep(ee, each = m)
    # Para el paso j del step-down: máximo de |t*| sobre las hipótesis j..K (en orden de |t|).
    ordenado <- t_boot[, orden, drop = FALSE]
    acumulado <- t(apply(ordenado, 1, function(f) rev(cummax(rev(f)))))
    if (length(etiquetas) == 1) acumulado <- t(acumulado)
    maximos[(hechas + 1):(hechas + m), ] <- acumulado
    hechas <- hechas + m
  }
  p_orden <- vapply(seq_along(orden), function(j) mean(maximos[, j] >= t_obs[orden[j]]), 0)
  p_orden <- cummax(p_orden)  # monotonía del step-down
  p_rw <- numeric(length(etiquetas))
  p_rw[orden] <- p_orden
  data.table(etiqueta = etiquetas, ee_if = ee, t = t_obs, p_rw = p_rw)
}

#' IC robusto con M̄ = 1 y menor M̄ del grid con el que el IC incluye el cero.
resumen_honest <- function(h) {
  if (!nrow(h)) return(data.table())
  h[, Mbar := as.numeric(Mbar)]
  h[!is.na(Mbar), .(
    honest_lb_m1 = lb[Mbar == 1][1], honest_ub_m1 = ub[Mbar == 1][1],
    mbar_quiebre = {
      incluye <- Mbar[lb <= 0 & ub >= 0]
      if (length(incluye)) min(incluye) else NA_real_
    }
  ), by = etiqueta]
}

tabla_final <- function() {
  maestra <- fread(file.path(RUTA_TABLAS, "maestra_resultados.csv"))
  cs <- maestra[estimador == "Callaway y Sant'Anna"]
  sesoi <- PARAMS$estimacion$sesoi_pct

  # Potencia y equivalencia.
  z90 <- stats::qnorm(0.95)
  cs[, `:=`(mde80 = (stats::qnorm(0.975) + stats::qnorm(0.80)) * ee,
            ic90_bajo = valor - z90 * ee, ic90_alto = valor + z90 * ee)]
  # En porcentaje de la media previa de las tratadas; para los resultados en logaritmo (`log_…`)
  # el efecto ya es proporcional: 100 × puntos log (dividir entre la media del logaritmo no tiene
  # sentido).
  cs[, escala := fifelse(startsWith(resultado, "log_"), 1, abs(media_base))]
  cs[, `:=`(mde80_pct = 100 * mde80 / escala,
            efecto_pct = 100 * valor / escala,
            cota_equivalencia_pct = 100 * pmax(abs(ic90_bajo), abs(ic90_alto)) / escala)]
  cs[, escala := NULL]
  cs[, nulo_informativo := p >= 0.05 & cota_equivalencia_pct <= sesoi]

  # Benjamini–Hochberg sobre toda la batería. La primera etapa no es una hipótesis de interés sino
  # la validación de la fecha de tratamiento: queda fuera de la familia.
  cs[variante != "primera_etapa", q_bh := stats::p.adjust(p, method = "BH")]

  # Romano–Wolf por familia preregistrada.
  familias <- PARAMS$estimacion$familias_rw
  rw <- rbindlist(lapply(names(familias), function(f) {
    etiquetas <- paste0(familias[[f]]$prefijo, familias[[f]]$resultados)
    presentes <- etiquetas[etiquetas %in% cs$etiqueta]
    if (length(presentes) < length(etiquetas)) {
      message("  familia ", f, ": faltan ", paste(setdiff(etiquetas, presentes), collapse = ", "))
    }
    if (!length(presentes)) return(NULL)
    out <- romano_wolf(presentes, cs[match(presentes, etiqueta), valor])
    out[, familia := f]
  }))
  if (nrow(rw)) {
    guardar_tabla(rw, "inferencia_romano_wolf")
    cs <- merge(cs, rw[, .(etiqueta, familia, p_rw)], by = "etiqueta", all.x = TRUE)
  }

  # HonestDiD.
  honest <- resumen_honest(leer_tablas("^rob_honest_.*\\.csv$"))
  if (nrow(honest)) cs <- merge(cs, honest, by = "etiqueta", all.x = TRUE)

  # Los demás estimadores, lado a lado.
  otros <- dcast(maestra[estimador != "Callaway y Sant'Anna"], etiqueta ~ estimador,
                 value.var = c("valor", "ee"))
  cs <- merge(cs, otros, by = "etiqueta", all.x = TRUE)

  orden_variante <- c("principal", "eacp", "inclusion_total", "primera_etapa", "imss", "ce",
                      "remesas", "hasta_2025", "secundaria", "derrame", "panel_corto",
                      "panel_corto_2025")
  cs[, orden := match(variante, orden_variante)]
  setorder(cs, orden, panel, diseno, bloque, resultado)
  cs[, orden := NULL]
  guardar_tabla(cs, "tabla_final")

  # Heterogeneidad: BH sobre todas las diferencias contra el grupo de referencia.
  het <- leer_tablas("^het_(localidad|municipio)_.*\\.csv$")
  if (nrow(het) && "p_dif" %in% names(het)) {
    het[!is.na(p_dif), q_dif := stats::p.adjust(p_dif, method = "BH")]
    guardar_tabla(het, "het_q")
  }

  message("\n== tabla final (principales)")
  print(cs[variante == "principal",
           .(resultado, diseno, att = round(valor, 3), ee = round(ee, 3),
             efecto_pct = round(efecto_pct, 1), mde80_pct = round(mde80_pct, 1),
             pre = paste0(pre_sig, "/", pre_n), wald_p = round(pre_wald_p, 3),
             placebo = round(placebo, 3), q_bh = round(q_bh, 3), p_rw = round(p_rw, 3))])
  invisible(cs)
}

if (sys.nframe() == 0) {
  tabla_final()
}

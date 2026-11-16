# 12_diagnosticos.R — Diagnósticos de la especificación financiera principal que promete la
# descripción de la metodología (2026-10-12; descriptivos, no preregistrados):
#   1. soporte común y balance del puntaje de propensión del estimador doblemente robusto, y si
#      las cohortes con peor balance mueven el resultado;
#   2. descomposición de Goodman-Bacon del TWFE estático en el panel municipal trimestral (hasta
#      ahora solo existía para el DENUE).
#
# Uso:
#   Rscript analisis/12_diagnosticos.R todo
#   Rscript analisis/12_diagnosticos.R soporte   # 1 (diagnóstico + reestimación, ~10 s)
#   Rscript analisis/12_diagnosticos.R bacon     # 2 (forma cerrada, segundos)
#
# Salidas: outputs/tablas/desc_soporte_comun.csv, desc_soporte_robustez.csv y
# bacon_municipio_trim_esc_<resultado>.csv (con su bacon_detalle_*). `make bateria` borra `desc_*`:
# después de una batería completa hay que volver a correr `make diagnosticos`.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
source(here::here("analisis", "05_robustez.R"))  # variante()
source(here::here("analisis", "03_twfe_comparacion.R"))  # bacon_resumen()

FINANCIERA <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
COVARIABLES <- c("log_poblacion_2020", "indice_marginacion_2020", "banca_mun_2019")
# Una cohorte está desbalanceada si, ya reponderados los controles, alguna covariable queda con una
# diferencia estandarizada mayor a este umbral (el convencional es 0.1; se usa 0.2 para no
# confundir desbalance moderado con falta de soporte).
UMBRAL_DESBALANCE <- 0.2

#' Diferencia estandarizada de `x` entre tratadas (`t == 1`) y controles con pesos `w`.
diferencia_estandarizada <- function(x, t, w) {
  mt <- mean(x[t == 1])
  mc <- stats::weighted.mean(x[t == 0], w[t == 0])
  vc <- sum(w[t == 0] * (x[t == 0] - mc)^2) / sum(w[t == 0])
  (mt - mc) / sqrt((stats::var(x[t == 1]) + vc) / 2)
}

#' Área bajo la curva ROC del puntaje `p` para separar `t == 1` de `t == 0` (Mann–Whitney).
area_roc <- function(p, t) {
  r <- rank(p)
  n1 <- sum(t == 1)
  n0 <- sum(t == 0)
  (sum(r[t == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0)
}

#' Por cohorte g: logit de pertenecer a g contra los aún no tratados en g (G = 0 o G > g) sobre las
#' covariables previas, como el que estima `did` para ATT(g, g). El grupo de comparación de `did`
#' cambia con t; aquí se usa el del trimestre de apertura (simplificación).
diagnostico <- function(resultado = FINANCIERA[1]) {
  d <- leer_panel("municipio_trim", resultado = c(resultado, "poblacion_adulta_fija"))
  u <- unique(d[, c("id", "cve_mun", "G", COVARIABLES, "poblacion_adulta_fija"), with = FALSE])
  u[, banca_mun_2019 := as.numeric(banca_mun_2019)]
  filas <- rbindlist(lapply(sort(setdiff(unique(u$G), 0)), function(g) {
    s <- u[G == g | G == 0 | G > g]
    s[, trat := as.integer(G == g)]
    m <- stats::glm(stats::reformulate(COVARIABLES, "trat"), data = s, family = stats::binomial())
    s[, p := stats::fitted(m)]
    s[, w := fifelse(trat == 1, 1, p / (1 - p))]
    rango <- range(s[trat == 0, p])
    bruta <- vapply(COVARIABLES, function(v) diferencia_estandarizada(s[[v]], s$trat, rep(1, nrow(s))), 0)
    ponderada <- vapply(COVARIABLES, function(v) diferencia_estandarizada(s[[v]], s$trat, s$w), 0)
    data.table(cohorte = g, tratadas = sum(s$trat), controles = sum(1 - s$trat),
               auc = area_roc(s$p, s$trat),
               fuera_soporte = mean(s[trat == 1, p] > rango[2] | s[trat == 1, p] < rango[1]),
               dif_max_bruta = max(abs(bruta)), dif_max_ponderada = max(abs(ponderada)),
               peor_covariable = COVARIABLES[which.max(abs(ponderada))])
  }))
  pondera <- function(x) stats::weighted.mean(x, filas$tratadas)
  out <- rbindlist(list(filas, data.table(
    cohorte = NA_real_, tratadas = sum(filas$tratadas), auc = pondera(filas$auc),
    fuera_soporte = pondera(filas$fuera_soporte), dif_max_bruta = pondera(filas$dif_max_bruta),
    dif_max_ponderada = pondera(filas$dif_max_ponderada),
    peor_covariable = "promedio ponderado por cohorte")), fill = TRUE)
  # Umbral de equivalencia en unidades del resultado: ±5% de la media previa de las tratadas.
  media <- media_base(con_resultado(d, resultado), resultado)
  adultos <- sum(u[G > 0, poblacion_adulta_fija])
  umbral <- PARAMS$estimacion$sesoi_pct / 100 * media
  out[, `:=`(resultado = resultado, media_base = media, umbral_por_10mil = umbral,
             adultos_tratados = adultos, umbral_sucursales_total = umbral * adultos / 1e4)]
  guardar_tabla(out, "desc_soporte_comun")
  print(out[, .(cohorte, tratadas, controles, auc = round(auc, 3), fuera = round(fuera_soporte, 3),
                bruta = round(dif_max_bruta, 3), ponderada = round(dif_max_ponderada, 3),
                peor_covariable)])
  message(sprintf("±%g%% de %.3f = ±%.4f sucursales por 10 mil adultos (±%.0f en %s adultos)",
                  PARAMS$estimacion$sesoi_pct, media, umbral, umbral * adultos / 1e4,
                  format(adultos, big.mark = ",")))
  invisible(out)
}

#' Reestima los tres resultados financieros sin las cohortes que el diagnóstico marca como
#' desbalanceadas: salen como tratadas y como controles aún no tratados de las cohortes anteriores.
#' (Quitar solo a las tratadas fuera del soporte no vale la pena: son menos del 1%.)
robustez <- function(diag) {
  malas <- diag[!is.na(cohorte) & dif_max_ponderada > UMBRAL_DESBALANCE, cohorte]
  message("cohortes desbalanceadas (dif. ponderada > ", UMBRAL_DESBALANCE, "): ",
          paste(malas, collapse = ", "))
  filas <- lapply(FINANCIERA, function(r) {
    base <- leer_panel("municipio_trim", diseno = "escalonado", resultado = r)
    ids <- unique(base[!(G %in% malas), cve_mun])
    rbindlist(Filter(Negate(is.null), list(
      variante("base", base, r),
      variante(paste("sin las cohortes", paste(malas, collapse = " y ")),
               leer_panel("municipio_trim", diseno = "escalonado", resultado = r, ids = ids), r)
    )))[, resultado := r]
  })
  out <- rbindlist(filas, fill = TRUE)
  out[, `:=`(efecto_pct = 100 * att / media_base,
             cota_ic90_pct = 100 * (abs(att) + stats::qnorm(0.95) * ee) / media_base,
             cohortes_fuera = paste(malas, collapse = ","))]
  guardar_tabla(out, "desc_soporte_robustez")
  print(out[, .(resultado, variante, tratadas, controles, att = round(att, 4), ee = round(ee, 4),
                efecto_pct = round(efecto_pct, 2), cota = round(cota_ic90_pct, 2),
                wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

#' Goodman-Bacon del TWFE estático en la ventana financiera principal: qué peso tienen las
#' comparaciones contra nunca tratados y cuánto las "prohibidas" (tardías contra tempranas).
bacon_financiero <- function() {
  for (r in FINANCIERA) {
    message("\n#### Goodman-Bacon: ", r)
    esc <- con_resultado(leer_panel("municipio_trim", diseno = "escalonado", resultado = r), r)
    bacon_resumen(esc, r, etiqueta_de("municipio_trim", "escalonado", r))
  }
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { robustez(diagnostico()); bacon_financiero() },
         soporte = robustez(diagnostico()),
         bacon = bacon_financiero(),
         stop("uso: Rscript analisis/12_diagnosticos.R todo | soporte | bacon"))
}

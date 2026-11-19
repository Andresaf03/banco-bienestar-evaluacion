# 17_preguntas.R — Robusteces para las preguntas previsibles de los evaluadores (2026-11-18).
#
# Exploratorio, después de ver todos los resultados (se declara así en docs/decisiones.md). No toca
# la maestra, la tabla final ni sus familias. Responde tres preguntas sobre el nulo financiero:
#   1. ¿Y ponderando por población? El ATT de Callaway y Sant'Anna promedia municipios; con la
#      población adulta como peso es el efecto sobre el adulto promedio, que pesa más a los grandes.
#   2. ¿Y si la banca privada reacciona a la obra con más de un trimestre de anticipación? δ = 2.
#   3. ¿Y a más largo plazo? Efecto promedio de e = 0 a 8 trimestres solo con las cohortes que se
#      observan los nueve trimestres (composición fija, `balance_e`), para que el horizonte largo no
#      mezcle cohortes distintas.
#
# Uso: Rscript analisis/17_preguntas.R
# Salida: outputs/tablas/rev_preguntas_financiero.csv

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))

RESULTADOS <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
PESO <- "poblacion_adulta_fija"
E_MAX <- 8L

#' CS con la especificación base y un peso por unidad.
estimar_ponderado <- function(dt, resultado) {
  clustervars <- if (any(dt$cluster != dt$id)) "cluster" else "id"
  did::att_gt(
    yname = resultado, tname = "tiempo", idname = "id", gname = "G",
    xformla = formula_covariables(dt), data = as.data.frame(dt), panel = TRUE,
    allow_unbalanced_panel = FALSE, control_group = "notyettreated", anticipation = 0,
    est_method = PARAMS$estimacion$metodo, base_period = "varying", weightsname = PESO,
    bstrap = PARAMS$estimacion$bootstrap, biters = PARAMS$estimacion$n_boot,
    cband = PARAMS$estimacion$bandas_simultaneas, clustervars = clustervars, alp = 0.05,
    print_details = FALSE
  )
}

fila <- function(resultado, variante, att, ee, media, tratadas, wald_p = NA_real_) {
  data.table(resultado = resultado, variante = variante, att = att, ee = ee, media_base = media,
             tratadas = tratadas, pre_wald_p = wald_p,
             efecto_pct = 100 * att / abs(media),
             cota_pct = 100 * (abs(att) + stats::qnorm(0.95) * ee) / abs(media))
}

una <- function(resultado) {
  dt <- con_resultado(leer_panel("municipio_trim", resultado = c(resultado, PESO)), resultado)
  media <- media_base(dt, resultado)
  n_trat <- uniqueN(dt[G > 0]$id)
  message("== ", resultado, ": ", n_trat, " tratados")

  # 1. Ponderado por población adulta.
  fit_w <- estimar_ponderado(dt, resultado)
  est_w <- estimando_principal(fit_w, dt)
  pre_w <- prueba_previa(fit_w, dt)

  # 2. Anticipación de dos trimestres.
  fit_a <- estimar_attgt(dt, resultado, anticipacion = 2)
  est_a <- estimando_principal(fit_a, dt)
  pre_a <- prueba_previa(fit_a, dt)

  # 3. Horizonte de dos años con composición fija.
  fit <- estimar_attgt(dt, resultado)
  ag <- did::aggte(fit, type = "dynamic", balance_e = E_MAX, min_e = 0, max_e = E_MAX,
                   na.rm = TRUE)
  cl <- cluster_if(fit, dt)
  # Función de influencia del promedio sobre e (did la guarda como `dynamic.inf.func`).
  psi <- as.matrix(ag$inf.function$dynamic.inf.func %||%
                     rowMeans(as.matrix(ag$inf.function$dynamic.inf.func.e)))
  ee_largo <- sqrt(drop(varianza_cluster(psi, cl)))
  cohortes <- sort(unique(fit$group[fit$group + E_MAX <= max(dt$tiempo)]))
  n_largo <- uniqueN(dt[G %in% cohortes]$id)

  rbindlist(list(
    fila(resultado, "ponderado por población adulta", est_w$att, est_w$ee, media, n_trat,
         pre_w$wald_p),
    fila(resultado, "anticipación de dos trimestres", est_a$att, est_a$ee, media, n_trat,
         pre_a$wald_p),
    fila(resultado, sprintf("promedio e = 0…%d, composición fija", E_MAX), ag$overall.att, ee_largo,
         media, n_largo)
  ))
}

if (sys.nframe() == 0) {
  out <- rbindlist(lapply(RESULTADOS, una))
  guardar_tabla(out, "rev_preguntas_financiero")
  print(out[, .(resultado, variante, tratadas, efecto_pct = round(efecto_pct, 2),
                cota = round(cota_pct, 2), wald_p = round(pre_wald_p, 3))])
}

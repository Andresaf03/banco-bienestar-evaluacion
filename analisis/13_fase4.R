# 13_fase4.R — Fase 4: efectos fijos, grupo de control y covariables, validez del nulo,
# bancarización y uso. Preregistro y adenda de datos en docs/decisiones.md (2026-10-14); plan en
# docs/contexto/plan_fase4.md.
#
# Uso:
#   Rscript analisis/13_fase4.R todo
#   Rscript analisis/13_fase4.R efectos_fijos  # 0.1–0.4: evento TWFE, TWFE extendido, apilado, sensibilidad
#   Rscript analisis/13_fase4.R diagnostico_etwfe  # exploratorio: por qué el TWFE extendido se separa de CS
#   Rscript analisis/13_fase4.R diagnostico_cs_metodo  # exploratorio: CS con regresión, IPW y DR
#   Rscript analisis/13_fase4.R controles      # H1 (c, d, e) y H2 (covariables una por una)
#   Rscript analisis/13_fase4.R validez        # A1(b) derrames, A2 placebo, A3 permutación, A4, A5
#   Rscript analisis/13_fase4.R bancarizacion  # B1, C1 y B2 (traslado de cuentas)
#   Rscript analisis/13_fase4.R uso            # C4 y C3 (privado con panel largo)
#   Rscript analisis/13_fase4.R enigh          # C2, B3 y D: forma de pago, ahorro, programas, ingreso
#   Rscript analisis/13_fase4.R resumen        # Romano–Wolf por familia, BH y triangulación (0.5)
#
# Como las fases 2 y 3: no toca la maestra, la tabla final ni las familias anteriores. Los paneles
# se registran aquí y las salidas llevan el prefijo `fase4_` (las de CS, `cs_*`/`if_*` con el panel
# `municipio_trim_f4` en la etiqueta).

source(here::here("analisis", "10_fase2.R"))             # 00, 02, 05, 07, 08; correr_bloque()
source(here::here("analisis", "03_twfe_comparacion.R"))  # sun_abraham(), bjs_imputacion()

PANELES$municipio_trim_f4 <- list(archivo = "panel_municipio_trim_f4.parquet", id = "cve_mun",
                                  tiempo = "t", per_capita = TRUE, periodicidad = "trimestral",
                                  ventana = "ventana_trimestral")
PANELES$municipio_placebo_f4 <- list(archivo = "panel_municipio_placebo_f4.parquet",
                                     id = "cve_mun", tiempo = "t", per_capita = TRUE,
                                     periodicidad = "trimestral")
# ENIGH (adenda del 2026-10-14): municipio × ola (cinco olas o, para forma de pago, 2020–2024) y
# hogar × ola con el municipio como unidad de los efectos fijos y del cluster.
for (nombre in c("municipio_enigh", "municipio_enigh_pagos", "hogar_enigh")) {
  PANELES[[nombre]] <- list(archivo = paste0("panel_", nombre, ".parquet"), id = "cve_mun",
                            tiempo = "t", per_capita = TRUE, periodicidad = "bienal")
}
ENIGH_PAGOS <- c("pct_gasto_electronico", "pct_hog_pago_electronico")

F4 <- PARAMS$fase4
APIL <- PARAMS$estimacion$apilado
PANEL <- "municipio_trim_f4"
PRIMERA_ETAPA <- "sucursales_total_pc"
TENDENCIA <- c(sucursales_privado_pc = "tendencia_privado", sucursales_bm_pc = "tendencia_bm",
               sucursales_eacp_pc = "tendencia_eacp")
EXTRA <- c("G_vecino_mun", "vecino_heredado", "region", "log1p_dist_bm", unname(TENDENCIA))

#' Panel de la fase con las columnas nuevas (vecinos, región, distancia, tendencias).
leer_f4 <- function(resultado, ...) {
  con_resultado(leer_panel(PANEL, resultado = c(resultado, EXTRA), ...), resultado)
}

#' Copia los atributos del panel (`leer_panel()`) a un subconjunto.
con_atributos <- function(sub, dt) {
  for (a in c("panel_nombre", "panel_id", "diseno")) setattr(sub, a, attr(dt, a))
  sub
}

#' `correr()` guarda la función de influencia con el cluster como entero de `factor()` dentro de
#' su muestra; en familias con muestras distintas (C4 y C3) el mismo entero sería otro municipio.
#' Se reescribe con la clave del municipio para que Romano–Wolf alinee bien los clusters.
correr_f4 <- function(resultado, ventana = NULL, variante) {
  correr_con_municipio(PANEL, leer_f4(resultado, ventana = ventana), resultado, variante)
}

correr_con_municipio <- function(panel, dt, resultado, variante) {
  out <- correr(panel, resultado, dt = dt, variante = variante)
  etiqueta <- out$fila$etiqueta
  ruta <- file.path(RUTA_INTERMEDIOS, paste0("if_", etiqueta, ".csv"))
  psi <- fread(ruta)
  claves <- unique(out$dt[, .(cluster, cve_mun)])
  if (anyDuplicated(claves$cluster)) stop("el cluster no es el municipio en ", etiqueta)
  psi[, cluster := claves$cve_mun[match(cluster, claves$cluster)]]
  if (anyNA(psi$cluster)) stop("clusters sin municipio en ", etiqueta)
  fwrite(psi, ruta)
  out$fila
}

#' Fila estándar de la fase (mismas columnas que la `fila` de `correr()`).
fila_fase <- function(etiqueta, estimador, variante, familia, dt, resultado, att, ee,
                      previa = list(n = NA_integer_, n_sig = NA_integer_, wald_p = NA_real_)) {
  data.table(etiqueta = etiqueta, panel = attr(dt, "panel_nombre") %||% PANEL,
             diseno = "escalonado", resultado = resultado, estimador = estimador,
             termino = "ATT global", valor = att, ee = ee, n_unidades = uniqueN(dt$id),
             n_tratadas = uniqueN(dt[G > 0]$id), n_controles = uniqueN(dt[G == 0]$id),
             n_clusters = uniqueN(dt$cluster), media_base = media_base(dt, resultado),
             pre_n = previa$n, pre_sig = previa$n_sig, pre_wald_p = previa$wald_p,
             variante = variante, familia = familia)
}

#' Wald conjunta de un subconjunto de coeficientes de un modelo fixest (varianza agrupada).
wald_fixest <- function(m, nombres) {
  if (!length(nombres)) return(list(n = 0L, n_sig = NA_integer_, wald_p = NA_real_))
  b <- coef(m)[nombres]
  V <- vcov(m)[nombres, nombres, drop = FALSE]
  W <- tryCatch(drop(crossprod(b, solve(V, b))), error = function(e) NA_real_)
  list(n = length(b), n_sig = sum(abs(b / sqrt(diag(V))) > stats::qnorm(0.975)),
       wald_p = stats::pchisq(W, df = length(b), lower.tail = FALSE))
}

# 0. Regresión con efectos fijos -------------------------------------------------------------------

#' 0.1 Estudio de evento TWFE clásico: efectos fijos de municipio y trimestre, e binned en
#' [min, max], referencias e = −1 y "nunca tratado" (−1000).
estudio_evento_twfe <- function(dt, resultado, fe = "id + tiempo") {
  lo <- F4$evento_twfe$min
  hi <- F4$evento_twfe$max
  d <- copy(dt)
  d[, e := fifelse(G > 0, pmin(pmax(tiempo - G, lo), hi), -1000)]
  f <- as.formula(paste(resultado, "~ i(e, ref = c(-1, -1000)) |", fe))
  m <- fixest::feols(f, data = d, cluster = ~cluster)
  ct <- as.data.table(fixest::coeftable(m), keep.rownames = "coef")
  setnames(ct, c("coef", "att", "ee", "t", "p"))
  ct[, e := as.integer(sub("^e::(-?[0-9]+)$", "\\1", coef))]
  post <- ct[e >= 0]$coef
  l <- setNames(rep(1 / length(post), length(post)), post)
  att <- sum(l * coef(m)[post])
  ee <- sqrt(drop(crossprod(l, vcov(m)[post, post] %*% l)))
  list(evento = rbind(ct[, .(e, att, ee)], data.table(e = -1L, att = 0, ee = 0))[order(e)],
       att = att, ee = ee, previa = wald_fixest(m, ct[e <= -2]$coef))
}

#' Celdas (cohorte, trimestre) post y, con covariables, sus interacciones con las covariables
#' centradas en la media de la cohorte (Wooldridge, 2021): así β_gt es el efecto en la covariable
#' media de la cohorte y las pendientes de trimestre no absorben la heterogeneidad del efecto.
#' `interacciones = FALSE` deja solo las pendientes de trimestre (la versión del preregistro).
disenar_celdas <- function(dt, covariables, interacciones) {
  d <- copy(dt)
  d[, celda := fifelse(G > 0 & tiempo >= G, paste0(G, "_", tiempo), "0")]
  covs <- if (covariables) all.vars(formula_covariables(d)) else character()
  rhs <- "i(celda, ref = '0')"
  if (length(covs) && interacciones) {
    for (x in covs) {
      xc <- paste0(".c_", x)
      d[, (xc) := get(x) - mean(get(x)[!duplicated(id)]), by = G]
      rhs <- paste0(rhs, sprintf(" + i(celda, %s, ref = '0')", xc))
    }
  }
  fe_t <- if (length(covs)) sprintf("tiempo[%s]", paste(covs, collapse = ", ")) else "tiempo"
  list(d = d, rhs = rhs, fe_t = fe_t)
}

#' 0.2 TWFE extendido (Wooldridge, 2021): una regresión con efectos fijos y un indicador por celda
#' (cohorte, trimestre) post. `pesos = "grupo"` reproduce la agregación "group" de CS;
#' `"observaciones"`, la de BJS. Covariables: pendientes de trimestre (`tiempo[x]`) e interacciones
#' celda × covariable centrada (`disenar_celdas`). Devuelve el ATT, su ee agrupado y la función de
#' influencia por cluster (para Romano–Wolf).
twfe_extendido <- function(dt, resultado, covariables = TRUE, fe_extra = NULL,
                           tendencias = FALSE, pesos = "grupo", interacciones = TRUE,
                           ponderador = NULL) {
  dis <- disenar_celdas(dt, covariables, interacciones)
  d <- dis$d
  fe <- paste(c(if (tendencias) "id[tiempo]" else "id", dis$fe_t, fe_extra), collapse = " + ")
  w_obs <- if (is.null(ponderador)) NULL else as.formula(paste0("~", ponderador))
  m <- fixest::feols(as.formula(paste(resultado, "~", dis$rhs, "|", fe)),
                     data = d, cluster = ~cluster, weights = w_obs)
  b <- coef(m)
  celdas <- data.table(coef = grep("^celda::[0-9]+_[0-9]+$", names(b), value = TRUE))
  celdas[, c("g", "t") := tstrsplit(sub("^celda::", "", coef), "_", type.convert = TRUE)]
  n_g <- d[!duplicated(id) & G > 0, .N, by = G]
  celdas <- merge(celdas, n_g, by.x = "g", by.y = "G")
  if (pesos == "grupo") {
    total <- celdas[!duplicated(g), sum(N)]
    celdas[, w := (N / total) / .N, by = g]
  } else {
    celdas[, w := N / sum(N)]
  }
  w <- setNames(celdas$w, celdas$coef)[names(b)]
  w[is.na(w)] <- 0
  att <- sum(w * b)
  ee <- sqrt(drop(crossprod(w, vcov(m) %*% w)))
  # ψ_i = n · s_i' H⁻¹ w: Σ_c ψ_c² / n² es la varianza agrupada sin corrección (CR0). H⁻¹ sale de
  # `cov.iid / sigma2`, que (a diferencia de `hessian`) ya no trae los coeficientes colineales.
  psi <- drop(m$scores %*% ((m$cov.iid / m$sigma2) %*% w))
  obs <- d[fixest::obs(m)]
  n <- nrow(obs)
  psi_c <- rowsum(n * psi, obs$cve_mun)[, 1]
  list(att = att, ee = ee, psi_c = psi_c, n = n, modelo = m, celdas = nrow(celdas),
       fe = fe)
}

#' Pre-prueba del TWFE extendido: indicadores de tiempo de evento previo (e ≤ −2, binned en el
#' mínimo) para las tratadas, junto con las celdas post; Wald de los previos (como BJS).
previa_extendido <- function(dt, resultado, covariables = TRUE, interacciones = TRUE,
                             ponderador = NULL) {
  dis <- disenar_celdas(dt, covariables, interacciones)
  d <- dis$d
  d[, e_pre := fifelse(G > 0 & tiempo - G <= -2, pmax(tiempo - G, F4$evento_twfe$min), 0L)]
  w_obs <- if (is.null(ponderador)) NULL else as.formula(paste0("~", ponderador))
  m <- fixest::feols(
    as.formula(paste(resultado, "~", dis$rhs, "+ i(e_pre, ref = 0) | id +", dis$fe_t)),
    data = d, cluster = ~cluster, weights = w_obs
  )
  wald_fixest(m, grep("^e_pre::", names(coef(m)), value = TRUE))
}

#' Copia de `estimar_apilado()` (08) con efectos fijos configurables.
estimar_apilado_fe <- function(st, resultado, fe) {
  f <- as.formula(paste(resultado, "~ i(e, tratada, ref = -1) |", fe))
  m <- fixest::feols(f, data = st, weights = ~peso, cluster = ~cluster)
  b <- coef(m)
  e <- as.integer(sub("^e::(-?[0-9]+):tratada$", "\\1", names(b)))
  post <- which(e >= 0 & e <= APIL$k_post)
  l <- rep(1 / length(post), length(post))
  list(att = sum(l * b[post]), ee = sqrt(drop(crossprod(l, vcov(m)[post, post] %*% l))),
       previa = wald_fixest(m, names(b)[e < -1]))
}

#' Pesos de Wing et al. dentro de cada pila (recalculados tras quitar controles).
reponderar <- function(st) {
  st[, peso := NULL]
  st[, q := NULL]
  st <- st[, if (.N == APIL$k_pre + APIL$k_post + 1L) .SD, by = .(pila, id)]
  tam <- st[e == 0, .(n_trat = sum(tratada), n_ctrl = sum(1L - tratada)), by = pila]
  tam <- tam[n_trat > 0 & n_ctrl > 0]
  tam[, q := (n_trat / sum(n_trat)) / (n_ctrl / sum(n_ctrl))]
  st <- merge(st[pila %in% tam$pila], tam[, .(pila, q)], by = "pila")
  st[, peso := fifelse(tratada == 1L, 1, q)]
  st[]
}

#' Pila genérica: `trat_g` (G de la exposición) y una regla de elegibilidad por pila.
apilar_generico <- function(dt, resultado, g_exposicion, elegible = function(d, g) rep(TRUE, nrow(d))) {
  d0 <- copy(dt)
  d0[, g_x := get(g_exposicion)]
  cohortes <- sort(setdiff(unique(d0$g_x), 0))
  cohortes <- cohortes[cohortes - APIL$k_pre >= min(d0$tiempo) & cohortes + APIL$k_post <= max(d0$tiempo)]
  pilas <- lapply(cohortes, function(g) {
    fin <- g + APIL$k_post
    d <- d0[elegible(d0, g)]
    d <- d[(g_x == g | g_x == 0 | g_x > fin) & tiempo >= g - APIL$k_pre & tiempo <= fin]
    d[, `:=`(pila = g, e = tiempo - g, tratada = as.integer(g_x == g))]
  })
  st <- rbindlist(pilas)
  st <- st[is.finite(get(resultado))]
  st[, `:=`(peso = 1, q = 1)]
  reponderar(st)
}

efectos_fijos_uno <- function(resultado, familia) {
  dt <- leer_f4(resultado)
  filas <- list()
  agregar_fila <- function(...) filas[[length(filas) + 1]] <<- fila_fase(..., dt = dt, resultado = resultado)
  etq <- function(x) paste(PANEL, "esc", x, resultado, sep = "_")

  ev <- estudio_evento_twfe(dt, resultado)
  guardar_tabla(ev$evento[, resultado := resultado], paste0("fase4_evento_twfe_", resultado))
  agregar_fila(etq("evento_twfe"), "TWFE estudio de evento (promedio e = 0…8)", "0.1", NA,
               att = ev$att, ee = ev$ee, previa = ev$previa)

  for (cov in c(TRUE, FALSE)) {
    x <- twfe_extendido(dt, resultado, covariables = cov)
    nombre <- if (cov) "etwfe" else "etwfe_sincov"
    if (cov) {
      guardar_intermedio(data.table(cluster = names(x$psi_c), psi = unname(x$psi_c), n = x$n),
                         paste0("if_", etq(nombre)))
    }
    agregar_fila(etq(nombre), paste("TWFE extendido (Wooldridge)", if (!cov) "sin covariables" else ""),
                 "0.2", if (cov) familia else NA, att = x$att, ee = x$ee,
                 previa = previa_extendido(dt, resultado, covariables = cov))
  }
  pre <- twfe_extendido(dt, resultado, covariables = TRUE, interacciones = FALSE)
  agregar_fila(etq("etwfe_solo_pendientes"),
               "TWFE extendido, solo pendientes de trimestre (versión del preregistro)", "0.2", NA,
               att = pre$att, ee = pre$ee,
               previa = previa_extendido(dt, resultado, covariables = TRUE, interacciones = FALSE))
  obs <- twfe_extendido(dt, resultado, covariables = FALSE, pesos = "observaciones")
  agregar_fila(etq("etwfe_pesos_bjs"), "TWFE extendido, pesos por observación (= BJS)", "0.2", NA,
               att = obs$att, ee = obs$ee)

  # 0.3 Apilado con efectos fijos estado × evento × pila (ventana del apilado de 08).
  dtv <- leer_f4(resultado, ventana = unlist(APIL$ventana))
  st <- apilar(dtv, resultado, APIL$k_pre, APIL$k_post)
  st[, cve_ent := substr(cve_mun, 1, 2)]
  for (fe in c("id^pila + e", "id^pila + e^cve_ent^pila")) {
    est <- estimar_apilado_fe(st, resultado, fe)
    agregar_fila(etq(paste0("apilado_", if (grepl("cve_ent", fe)) "estado" else "base")),
                 paste("DiD apilado,", fe), "0.3", NA, att = est$att, ee = est$ee,
                 previa = est$previa)
  }

  # 0.4 Sensibilidad de los efectos fijos (TWFE estático y extendido sin covariables).
  d4 <- copy(dt)
  d4[, cve_ent := substr(cve_mun, 1, 2)]
  u <- unique(d4[, .(id, poblacion_2020)])
  u[, decil := as.integer(cut(frank(poblacion_2020, ties.method = "first"), 10, labels = FALSE))]
  d4 <- con_atributos(merge(d4, u[, .(id, decil)], by = "id"), dt)
  covs <- all.vars(formula_covariables(d4))
  variantes <- list(
    "estado × trimestre" = list(fe = "id + cve_ent^tiempo", extra = "cve_ent^tiempo", tend = FALSE),
    "decil de tamaño × trimestre" = list(fe = "id + decil^tiempo", extra = "decil^tiempo", tend = FALSE),
    "tendencias lineales municipales" = list(fe = "id[tiempo] + tiempo", extra = NULL, tend = TRUE),
    "covariables × trimestre" = list(fe = sprintf("id + tiempo[%s]", paste(covs, collapse = ", ")),
                                     extra = NULL, tend = FALSE, cov = TRUE, inter = FALSE)
  )
  for (nombre in names(variantes)) {
    v <- variantes[[nombre]]
    m <- fixest::feols(as.formula(paste(resultado, "~ tratado |", v$fe)), data = d4, cluster = ~cluster)
    agregar_fila(etq(paste0("twfe_", make.names(nombre))), paste("TWFE estático,", nombre), "0.4", NA,
                 att = unname(coef(m)["tratado"]), ee = unname(se(m)["tratado"]))
    x <- twfe_extendido(d4, resultado, covariables = isTRUE(v$cov), fe_extra = v$extra,
                        tendencias = v$tend, interacciones = !isFALSE(v$inter))
    agregar_fila(etq(paste0("etwfe_", make.names(nombre))), paste("TWFE extendido,", nombre), "0.4",
                 NA, att = x$att, ee = x$ee)
  }
  rbindlist(filas, fill = TRUE)
}

#' Exploratorio (adenda 2026-10-14, después de la prueba de humo): por qué el TWFE extendido con
#' covariables se separa de CS. Ventana hasta la última cohorte (2024T1), solo municipios que
#' alguna vez abren, y soporte común (puntaje de propensión entre 0.1 y 0.9, Crump et al. 2009).
#' Sin nunca tratados, desde 2024T1 todos están tratados y las celdas son colineales con el efecto
#' fijo de trimestre: la muestra de los que abren termina en 2023T4 y la última cohorte solo es
#' control (como hace `did`).
MUESTRA_ABREN <- "solo municipios que alguna vez abren (hasta 2023T4)"
diagnostico_etwfe <- function() {
  ultima <- max(leer_f4(FINANCIERA[1])[G > 0]$G)
  out <- rbindlist(lapply(FINANCIERA, function(r) {
    dt <- leer_f4(r)
    u <- dt[!duplicated(id)]
    covs <- all.vars(formula_covariables(dt))
    u[, tratada := as.integer(G > 0)]
    ps <- stats::glm(as.formula(paste("tratada ~", paste(covs, collapse = " + "))),
                     data = u, family = stats::binomial())
    u[, ps := stats::predict(ps, type = "response")]
    muestras <- setNames(list(
      dt,
      con_atributos(dt[tiempo <= ultima], dt),
      con_atributos(dt[G > 0 & tiempo < ultima], dt),
      con_atributos(dt[id %in% u[ps >= 0.1 & ps <= 0.9]$id], dt)
    ), c("completa", "hasta 2024T1 (hay aún no tratados)", MUESTRA_ABREN,
         "soporte común (0.1 ≤ PS ≤ 0.9)"))
    rbindlist(lapply(names(muestras), function(nombre) {
      d <- muestras[[nombre]]
      rbindlist(lapply(c(TRUE, FALSE), function(cov) {
        x <- tryCatch(twfe_extendido(d, r, covariables = cov), error = function(e) NULL)
        if (is.null(x)) return(NULL)
        data.table(resultado = r, muestra = nombre, covariables = cov, att = x$att, ee = x$ee,
                   tratadas = uniqueN(d[G > 0 & G <= max(tiempo)]$id),
                   controles_nunca = uniqueN(d[G == 0]$id),
                   media_base = media_base(dt, r))
      }))
    }))
  }), fill = TRUE)
  out[, efecto_pct := 100 * att / abs(media_base)]
  guardar_tabla(out, "fase4_diagnostico_etwfe")
  print(out[, .(resultado, muestra, covariables, tratadas, controles_nunca, att = round(att, 4),
                ee = round(ee, 4), efecto_pct = round(efecto_pct, 1))])
  invisible(out)
}

#' Exploratorio (revisión del 2026-10-15): CS con cada método de `did` (doblemente robusto, solo
#' regresión de resultado y solo ponderación por propensión). Si CS con el mismo ajuste lineal que el
#' TWFE extendido diera ~+6.8%, la diferencia vendría del ajuste y no del estimador.
diagnostico_cs_metodo <- function() {
  out <- rbindlist(lapply(FINANCIERA, function(r) {
    dt <- leer_f4(r)
    rbindlist(lapply(c("dr", "reg", "ipw"), function(m) {
      v <- variante(paste("CS,", m), dt, r, metodo = m)
      if (!is.null(v)) v[, `:=`(resultado = r, metodo = m)]
      v
    }))
  }), fill = TRUE)
  out[, efecto_pct := 100 * att / abs(media_base)]
  guardar_tabla(out, "fase4_diagnostico_cs_metodo")
  print(out[, .(resultado, metodo, att = round(att, 4), ee = round(ee, 4),
                efecto_pct = round(efecto_pct, 1), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

bloque_efectos_fijos <- function() {
  out <- rbindlist(lapply(c(FINANCIERA, PRIMERA_ETAPA), function(r) {
    message("\n#### efectos fijos / ", r)
    efectos_fijos_uno(r, if (r %in% F4$familias$financiero_fe) "financiero_fe" else NA)
  }), fill = TRUE)
  guardar_tabla(out, "fase4_efectos_fijos")
  print(out[, .(resultado, variante, estimador, att = round(valor, 4), ee = round(ee, 4),
                wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# H. Grupo de control y covariables -----------------------------------------------------------------

#' H1(d): nunca tratados emparejados 1:1 sin reemplazo por puntaje de propensión, dentro de la
#' región, con calibre de `calibre_ps` de del logit. Devuelve los `id` de la muestra emparejada.
emparejar_nunca <- function(dt) {
  u <- dt[!duplicated(id)]
  covs <- all.vars(formula_covariables(dt))
  u[, tratada := as.integer(G > 0)]
  m <- stats::glm(as.formula(paste("tratada ~", paste(covs, collapse = " + "))),
                  data = u, family = stats::binomial())
  u[, logit := stats::predict(m, type = "link")]
  calibre <- F4$calibre_ps * stats::sd(u$logit)
  set.seed(F4$semilla)
  elegidos <- integer()
  for (reg in unique(u$region)) {
    t_ids <- u[tratada == 1 & region == reg][order(-logit)]
    c_pool <- u[tratada == 0 & region == reg]
    for (i in seq_len(nrow(t_ids))) {
      if (!nrow(c_pool)) break
      dist <- abs(c_pool$logit - t_ids$logit[i])
      k <- which.min(dist)
      if (dist[k] <= calibre) {
        elegidos <- c(elegidos, t_ids$id[i], c_pool$id[k])
        c_pool <- c_pool[-k]
      }
    }
  }
  elegidos
}

controles_uno <- function(resultado) {
  dt <- leer_f4(resultado)
  filas <- list(variante("base (aún no tratados, covariables base)", dt, resultado))
  # H1(c): solo municipios que alguna vez abren. Sin nunca tratados, `did` corta la ventana antes
  # de la última cohorte (2024T1) y la deja solo como control: se reporta así.
  ultima <- max(dt[G > 0]$G)
  solo <- con_atributos(dt[G > 0 & tiempo < ultima], dt)
  h1c <- variante("H1c solo municipios que alguna vez abren", solo, resultado)
  if (!is.null(h1c)) {
    h1c[, `:=`(tratadas = uniqueN(solo[G < ultima]$id), controles = uniqueN(solo[G == ultima]$id))]
  }
  filas[[length(filas) + 1]] <- h1c
  # H1(d): nunca tratados emparejados.
  ids <- emparejar_nunca(dt)
  emp <- con_atributos(dt[id %in% ids], dt)
  filas[[length(filas) + 1]] <- variante("H1d nunca tratados emparejados (PS 1:1, región)", emp,
                                         resultado, control = "nevertreated")
  # H2: covariables una por una.
  secuencia <- list(
    "H2 población" = "log_poblacion_2020",
    "H2 + marginación" = c("log_poblacion_2020", "indice_marginacion_2020"),
    "H2 + tendencia previa" = c(PARAMS$covariables_previas, TENDENCIA[[resultado]]),
    "H2 + distancia a la banca" = c(PARAMS$covariables_previas, TENDENCIA[[resultado]], "log1p_dist_bm"),
    "H2 + región" = c(PARAMS$covariables_previas, TENDENCIA[[resultado]], "log1p_dist_bm", "region")
  )
  filas[[length(filas) + 1]] <- variante("H2 ninguna", dt, resultado, covariables = FALSE)
  for (nombre in names(secuencia)) {
    filas[[length(filas) + 1]] <- variante(nombre, dt, resultado, covs = secuencia[[nombre]])
  }
  out <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)

  # H1(e): apilado con controles sin vecino con apertura nueva en la ventana (regla de los 100).
  dtv <- leer_f4(resultado, ventana = unlist(APIL$ventana))
  st <- apilar(dtv, resultado, APIL$k_pre, APIL$k_post)
  st <- st[tratada == 1L | !(G_vecino_mun > 0 & G_vecino_mun <= pila + APIL$k_post)]
  st <- reponderar(st)
  est <- estimar_apilado(st, resultado, APIL$k_pre, APIL$k_post)
  out <- rbind(out, data.table(
    variante = "H1e apilado, controles sin vecino con apertura nueva",
    termino = "ATT apilado", unidades = uniqueN(st$id), tratadas = uniqueN(st[tratada == 1L]$id),
    controles = uniqueN(st[tratada == 0L]$id), att = est$att, ee = est$ee,
    media_base = st[tratada == 1L & e == -1L, mean(get(resultado))],
    pre_n = est$pre_n, pre_sig = est$pre_sig, pre_wald_p = est$pre_wald_p
  ), fill = TRUE)
  out[, `:=`(resultado = resultado, mueve_mas_de_1ee = abs(att - out$att[1]) > out$ee[1])]
  out
}

controles <- function() {
  out <- rbindlist(lapply(FINANCIERA, function(r) {
    message("\n#### controles / ", r)
    controles_uno(r)
  }), fill = TRUE)
  guardar_tabla(out, "fase4_controles")
  print(out[, .(resultado, variante, tratadas, controles, att = round(att, 4), ee = round(ee, 4),
                wald_p = round(pre_wald_p, 3), mueve_mas_de_1ee)])
  invisible(out)
}

# A. Validez del nulo -------------------------------------------------------------------------------

#' A1(b): efecto en municipios cuyo primer vecino abre en g, sin sucursal propia en la ventana.
derrames <- function() {
  r <- "sucursales_privado_pc"
  dtv <- leer_f4(r, ventana = unlist(APIL$ventana))
  sin_propia <- function(d, g) d$G == 0 | d$G > g + APIL$k_post
  st <- apilar_generico(dtv, r, "G_vecino_mun", sin_propia)
  est <- estimar_apilado(st, r, APIL$k_pre, APIL$k_post)
  out <- data.table(
    etiqueta = paste(PANEL, "apilado_vecinos", r, sep = "_"), panel = PANEL, resultado = r,
    estimador = "DiD apilado, exposición = primer vecino que abre", termino = "ATT apilado",
    valor = est$att, ee = est$ee, n_tratadas = uniqueN(st[tratada == 1L]$id),
    n_controles = uniqueN(st[tratada == 0L]$id), pilas = uniqueN(st$pila),
    media_base = st[tratada == 1L & e == -1L, mean(get(r))],
    pre_n = est$pre_n, pre_sig = est$pre_sig, pre_wald_p = est$pre_wald_p,
    variante = "A1b", familia = "derrames"
  )
  print(out)
  out
}

placebo <- function() {
  out <- correr_bloque("municipio_placebo_f4", FINANCIERA, "A2_placebo", NA)
  print(out[, .(resultado, n_tratadas, att = round(valor, 4), ee = round(ee, 4),
                wald_p = round(pre_wald_p, 3))])
  out
}

permutacion <- function() {
  r <- "sucursales_privado_pc"
  dt <- leer_f4(r)
  obs <- twfe_extendido(dt, r, covariables = FALSE)$att
  u <- dt[!duplicated(id), .(id, cve_ent = substr(cve_mun, 1, 2), G)]
  set.seed(F4$semilla)
  perm <- vapply(seq_len(F4$permutaciones), function(b) {
    u[, G_p := G[sample.int(.N)], by = cve_ent]
    d <- merge(dt[, !"G"], u[, .(id, G = G_p)], by = "id")
    twfe_extendido(d, r, covariables = FALSE)$att
  }, numeric(1))
  out <- data.table(resultado = r, att_observado = obs, permutaciones = length(perm),
                    p_permutacion = (1 + sum(abs(perm) >= abs(obs))) / (1 + length(perm)),
                    perm_p05 = stats::quantile(perm, 0.05), perm_p95 = stats::quantile(perm, 0.95))
  guardar_tabla(data.table(att = perm), "fase4_permutacion_distribucion")
  print(out)
  out
}

#' A4: HonestDiD con restricción de suavidad (Δ^SD). Misma preparación que `honest()` (05).
honest_sd <- function(resultado) {
  dt <- leer_f4(resultado)
  fit <- estimar_attgt(dt, resultado, base_period = "universal")
  ag <- did::aggte(fit, type = "dynamic", na.rm = TRUE, cband = FALSE)
  cl <- cluster_if(fit, dt)
  conservar <- ag$egt != -1
  beta <- ag$att.egt[conservar]
  sigma <- varianza_cluster(ag$inf.function$dynamic.inf.func.e[, conservar, drop = FALSE], cl)
  e <- ag$egt[conservar]
  pre <- sum(e < 0)
  post <- sum(e >= 0)
  usar <- min(3, post)
  l_vec <- c(rep(1 / usar, usar), rep(0, post - usar))
  res <- tryCatch(
    HonestDiD::createSensitivityResults(betahat = beta, sigma = sigma, numPrePeriods = pre,
                                        numPostPeriods = post, l_vec = l_vec,
                                        Mvec = unlist(F4$honest_sd_m), method = "C-LF"),
    error = function(err) { message("  HonestDiD (SD) falló: ", conditionMessage(err)); NULL }
  )
  if (is.null(res)) return(NULL)
  objetivo <- sum(l_vec * beta[-(1:pre)])
  as.data.table(res)[, `:=`(resultado = resultado, objetivo = objetivo,
                            media_base = media_base(dt, resultado))]
}

honest_sd_todo <- function() {
  sd <- rbindlist(lapply(FINANCIERA, honest_sd), fill = TRUE)
  if (!nrow(sd)) return(invisible(NULL))
  sd[, `:=`(lb_pct = 100 * lb / abs(media_base), ub_pct = 100 * ub / abs(media_base))]
  guardar_tabla(sd, "fase4_honest_sd")
  print(sd[, .(resultado, M, lb = round(lb, 4), ub = round(ub, 4), lb_pct = round(lb_pct, 1),
               ub_pct = round(ub_pct, 1))])
  invisible(sd)
}

#' A5: ATT por cohorte (de la corrida principal) y CS sin un estado a la vez (privadas).
por_cohorte_estado <- function() {
  cohortes <- rbindlist(lapply(FINANCIERA, function(r) {
    ruta <- file.path(RUTA_TABLAS, paste0("cs_agg_municipio_trim_esc_", r, ".csv"))
    if (!file.exists(ruta)) return(NULL)
    fread(ruta)[tipo == "group"][, resultado := r]
  }), fill = TRUE)
  r <- "sucursales_privado_pc"
  dt <- leer_f4(r)
  dt[, cve_ent := substr(cve_mun, 1, 2)]
  estados <- rbindlist(lapply(sort(unique(dt$cve_ent)), function(ent) {
    variante(paste("sin", ent), con_atributos(dt[cve_ent != ent], dt), r)
  }), fill = TRUE)
  list(cohortes = cohortes, estados = estados[, resultado := r])
}

validez <- function() {
  filas <- list(derrames(), placebo())
  guardar_tabla(rbindlist(filas, fill = TRUE), "fase4_validez")
  guardar_tabla(permutacion(), "fase4_permutacion")
  honest_sd_todo()
  a5 <- por_cohorte_estado()
  guardar_tabla(a5$cohortes, "fase4_por_cohorte")
  guardar_tabla(a5$estados, "fase4_sin_un_estado")
  message(sprintf("A5 sin un estado: ATT entre %.4f y %.4f", min(a5$estados$att), max(a5$estados$att)))
  invisible(NULL)
}

# B. Bancarización y C1 ----------------------------------------------------------------------------

bancarizacion <- function() {
  ventana <- c(1L, 28L)
  cs <- rbindlist(lapply(F4$familias$bancarizacion, function(r) {
    message("\n#### bancarización / ", r)
    tryCatch({
      out <- correr_f4(r, ventana = ventana, variante = "hasta_2025")
      out[, `:=`(variante = "B1_C1", familia = "bancarizacion")]
    }, error = function(e) { message("  falló: ", conditionMessage(e)); NULL })
  }), fill = TRUE)

  # C1 descriptivo: transacciones por tarjeta entre las tratadas, por tiempo de evento.
  d <- leer_panel(PANEL, resultado = c("tarjetas_debito_bb_pc", "transacciones_cajero_bb_pc"),
                  ventana = ventana)
  desc <- d[G > 0 & tarjetas_debito_bb_pc > 0,
            .(transacciones_por_tarjeta = sum(transacciones_cajero_bb_pc) / sum(tarjetas_debito_bb_pc),
              municipios = uniqueN(id)), by = .(e = tiempo - G)][order(e)]
  guardar_tabla(desc, "fase4_desc_transacciones_por_tarjeta")

  # B2: municipios con sucursal heredada; exposición = primer vecino con apertura nueva.
  r <- "tarjetas_debito_bb_pc"
  her <- leer_panel(PANEL, resultado = c(r, EXTRA), ventana = ventana, excluir_ya_tratados = FALSE,
                    min_pre = NULL, min_cohorte = NULL)
  her <- con_resultado(con_atributos(her[ya_tratado_inicio == TRUE], her), r)
  st <- apilar_generico(her, r, "G_vecino_mun")
  est <- estimar_apilado(st, r, APIL$k_pre, APIL$k_post)
  b2 <- data.table(
    etiqueta = paste(PANEL, "apilado_traslado", r, sep = "_"), panel = PANEL, resultado = r,
    estimador = "DiD apilado, heredadas con vecino que abre", termino = "ATT apilado",
    valor = est$att, ee = est$ee, n_tratadas = uniqueN(st[tratada == 1L]$id),
    n_controles = uniqueN(st[tratada == 0L]$id), pilas = uniqueN(st$pila),
    media_base = st[tratada == 1L & e == -1L, mean(get(r))],
    pre_n = est$pre_n, pre_sig = est$pre_sig, pre_wald_p = est$pre_wald_p,
    variante = "B2", familia = "derrames"
  )
  out <- rbindlist(list(cs, b2), fill = TRUE)
  guardar_tabla(out, "fase4_bancarizacion")
  print(out[, .(resultado, variante, n_tratadas, n_controles, att = round(valor, 2),
                ee = round(ee, 2), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# C. Uso privado con panel largo -------------------------------------------------------------------

uso <- function() {
  especificaciones <- list(
    list(r = "tarjetas_credito_bm_pc", ventana = NULL, variante = "C4", familia = "privado_largo"),
    list(r = "tarjetas_credito_bm_pc", ventana = c(1L, 28L), variante = "C4_hasta_2025", familia = NA),
    # C3 después del quiebre de la BDIF en 2022T1 (adenda): t = 13…28.
    list(r = "establecimientos_tpv_privado_pc", ventana = c(13L, 28L), variante = "C3",
         familia = "privado_largo"),
    list(r = "establecimientos_tpv_privado_pc", ventana = NULL, variante = "C3_con_quiebre",
         familia = NA)
  )
  out <- rbindlist(lapply(especificaciones, function(s) {
    message("\n#### uso / ", s$r, " / ", s$variante)
    tryCatch({
      f <- correr_f4(s$r, ventana = s$ventana, variante = s$variante)
      f[, `:=`(variante = s$variante, familia = s$familia)]
    }, error = function(e) { message("  falló: ", conditionMessage(e)); NULL })
  }), fill = TRUE)
  guardar_tabla(out, "fase4_uso")
  print(out[, .(resultado, variante, n_tratadas, att = round(valor, 3), ee = round(ee, 3),
                wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# ENIGH: uso y bienestar de los hogares (adenda del 2026-10-14) ----------------------------------

#' CS DR por municipio × ola (principal) y TWFE extendido con hogares ponderados (robustez). La
#' forma de pago solo se mide de forma comparable desde 2020 (panel `municipio_enigh_pagos`).
enigh <- function() {
  familia_de <- function(r) {
    if (r %in% c("pct_gasto_electronico", "pct_hog_deposito")) return("enigh_uso")
    if (r %in% c("log_ing_cor_pc", "pct_hog_bene_gob")) return("enigh_bienestar")
    NA_character_
  }
  resultados <- c("pct_gasto_electronico", "pct_hog_pago_electronico", "pct_hog_deposito",
                  "pct_hog_bene_gob", "log_ing_cor_pc", "log_gasto_mon_pc")
  filas <- lapply(resultados, function(r) {
    message("\n#### ENIGH / ", r)
    panel <- if (r %in% ENIGH_PAGOS) "municipio_enigh_pagos" else "municipio_enigh"
    cs <- tryCatch({
      dt <- con_resultado(leer_panel(panel, resultado = r), r)
      f <- correr_con_municipio(panel, dt, r, "enigh")
      f[, `:=`(variante = "enigh_municipio", familia = familia_de(r))]
    }, error = function(e) { message("  CS falló: ", conditionMessage(e)); NULL })
    # Robustez: hogares de todos los municipios, ponderados; la forma de pago desde 2020 (t = 3).
    ventana <- if (r %in% ENIGH_PAGOS) c(3L, 5L) else NULL
    hog <- tryCatch({
      dh <- con_resultado(leer_panel("hogar_enigh", resultado = c(r, "factor"), ventana = ventana), r)
      x <- twfe_extendido(dh, r, covariables = TRUE, ponderador = "factor")
      pv <- previa_extendido(dh, r, covariables = TRUE, ponderador = "factor")
      u <- dh[!duplicated(id)]
      data.table(etiqueta = paste("hogar_enigh_etwfe", r, sep = "_"), panel = "hogar_enigh",
                 diseno = "escalonado", resultado = r,
                 estimador = "TWFE extendido, hogares ponderados", termino = "ATT global",
                 valor = x$att, ee = x$ee, n_unidades = nrow(u), n_tratadas = u[G > 0, .N],
                 n_controles = u[G == 0, .N], n_clusters = uniqueN(dh$cluster),
                 media_base = dh[G > 0 & tiempo == G - 1, stats::weighted.mean(get(r), factor,
                                                                              na.rm = TRUE)],
                 pre_n = pv$n, pre_sig = pv$n_sig, pre_wald_p = pv$wald_p,
                 variante = "enigh_hogar", familia = NA_character_)
    }, error = function(e) { message("  hogares falló: ", conditionMessage(e)); NULL })
    rbindlist(list(cs, hog), fill = TRUE)
  })
  out <- rbindlist(filas, fill = TRUE)
  guardar_tabla(out, "fase4_enigh")
  print(out[, .(resultado, variante, n_tratadas, n_controles, att = round(valor, 3),
                ee = round(ee, 3), media = round(media_base, 2), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# Resumen y triangulación (0.5) -------------------------------------------------------------------

resumen <- function() {
  partes <- lapply(c("fase4_efectos_fijos", "fase4_bancarizacion", "fase4_uso", "fase4_validez",
                     "fase4_enigh"),
                   function(n) {
                     ruta <- file.path(RUTA_TABLAS, paste0(n, ".csv"))
                     if (file.exists(ruta)) fread(ruta) else NULL
                   })
  cs <- rbindlist(Filter(Negate(is.null), partes), fill = TRUE)
  if (!nrow(cs)) return(message("sin resultados de la fase 4"))
  z90 <- stats::qnorm(0.95)
  # En logaritmos el efecto ya es proporcional: ×100 son puntos log (como `escala_pct()` de 08).
  cs[, escala := fifelse(startsWith(resultado, "log_"), 1, abs(media_base))]
  cs[, `:=`(p = 2 * stats::pnorm(-abs(valor / ee)),
            efecto_pct = 100 * valor / escala,
            mde80_pct = 100 * (stats::qnorm(0.975) + stats::qnorm(0.80)) * ee / escala,
            cota_equivalencia_pct = 100 * (abs(valor) + z90 * ee) / escala)]
  cs[, escala := NULL]
  cs[, nulo_informativo := p >= 0.05 & cota_equivalencia_pct <= PARAMS$estimacion$sesoi_pct]
  cs[, pre_falla := !is.na(pre_wald_p) & pre_wald_p < 0.05]
  con_familia <- !is.na(cs$familia) & cs$familia != ""
  cs[con_familia, q_bh_fase4 := stats::p.adjust(p, method = "BH")]
  rw <- rbindlist(lapply(c("financiero_fe", "bancarizacion", "privado_largo", "enigh_uso",
                           "enigh_bienestar"), function(f) {
    sub <- cs[familia == f]
    if (nrow(sub) < 1) return(NULL)
    tryCatch(romano_wolf(sub$etiqueta, sub$valor)[, familia := f],
             error = function(e) { message("  Romano–Wolf ", f, ": ", conditionMessage(e)); NULL })
  }), fill = TRUE)
  if (nrow(rw)) cs <- merge(cs, rw[, .(etiqueta, p_rw)], by = "etiqueta", all.x = TRUE)
  # ENIGH (regla fijada antes de descargar): con MDE80 mayor a 10% de la media, descriptivo.
  sin_potencia <- grepl("^enigh", cs$variante) & cs$mde80_pct > 10
  cs[, lectura := fcase(pre_falla, "descriptivo (pre-prueba falla)",
                        sin_potencia, "descriptivo (MDE80 > 10%)",
                        nulo_informativo, "nulo informativo",
                        p < 0.05, "significativo",
                        default = "no informativo")]
  guardar_tabla(cs, "fase4_resumen")
  print(cs[, .(familia, resultado, variante, estimador, att = round(valor, 4), ee = round(ee, 4),
               efecto_pct = round(efecto_pct, 1), cota = round(cota_equivalencia_pct, 1),
               wald_p = round(pre_wald_p, 3), lectura)])
  triangulacion(cs)
  invisible(cs)
}

#' 0.5 Un renglón por estimador: CS (maestra) más lo de la fase, en % de la media previa.
triangulacion <- function(cs) {
  maestra <- fread(file.path(RUTA_TABLAS, "maestra_resultados.csv"))
  principales <- c(paste0("municipio_trim_esc_", FINANCIERA),
                   "municipio_trim_esc_primera_etapa_sucursales_total_pc")
  base <- maestra[etiqueta %in% principales, .(resultado, estimador, valor, ee)]
  medias <- maestra[etiqueta %in% principales & estimador == "Callaway y Sant'Anna",
                    .(resultado, media_base)]
  base <- merge(base, medias, by = "resultado")
  fase <- cs[variante %in% c("0.1", "0.2", "0.3"), .(resultado, estimador, valor, ee)]
  fase <- merge(fase, medias, by = "resultado")
  ruta_diag <- file.path(RUTA_TABLAS, "fase4_diagnostico_etwfe.csv")
  if (file.exists(ruta_diag)) {
    diag <- fread(ruta_diag)[muestra == MUESTRA_ABREN & covariables == TRUE]
    diag <- diag[, .(resultado, valor = att, ee,
                     estimador = "TWFE extendido con covariables, solo municipios que abren")]
    fase <- rbind(fase, merge(diag, medias, by = "resultado"), use.names = TRUE)
  }
  tri <- unique(rbind(base, fase, use.names = TRUE), by = c("resultado", "estimador"))
  tri[, `:=`(efecto_pct = 100 * valor / abs(media_base),
             ic90_bajo = 100 * (valor - stats::qnorm(0.95) * ee) / abs(media_base),
             ic90_alto = 100 * (valor + stats::qnorm(0.95) * ee) / abs(media_base))]
  guardar_tabla(tri, "fase4_estimadores")
  p <- ggplot(tri, aes(x = efecto_pct, y = estimador)) +
    geom_vline(xintercept = 0, linetype = "dashed") +
    geom_vline(xintercept = c(-5, 5), linetype = "dotted", color = "grey50") +
    geom_pointrange(aes(xmin = ic90_bajo, xmax = ic90_alto), size = 0.3) +
    facet_wrap(~resultado, scales = "free_x") +
    labs(title = "El mismo resultado con distintos estimadores",
         subtitle = "Efecto en % de la media previa de las tratadas · IC 90% · líneas punteadas: ±5%",
         x = "% de la media previa", y = NULL)
  guardar_figura(p, "fig_fase4_estimadores", ancho = 11, alto = 6)
  invisible(tri)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { bloque_efectos_fijos(); diagnostico_etwfe(); diagnostico_cs_metodo(); controles();
                  validez(); bancarizacion(); uso(); enigh(); resumen() },
         enigh = enigh(),
         efectos_fijos = bloque_efectos_fijos(),
         honest_sd = honest_sd_todo(),
         diagnostico_etwfe = diagnostico_etwfe(),
         diagnostico_cs_metodo = diagnostico_cs_metodo(),
         controles = controles(),
         validez = validez(),
         bancarizacion = bancarizacion(),
         uso = uso(),
         resumen = resumen(),
         stop("uso: Rscript analisis/13_fase4.R todo | efectos_fijos | diagnostico_etwfe | ",
              "diagnostico_cs_metodo | ",
              "controles | validez | honest_sd | enigh | ",
              "bancarizacion | uso | resumen"))
}

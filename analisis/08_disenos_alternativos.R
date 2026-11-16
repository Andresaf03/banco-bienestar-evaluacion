# 08_disenos_alternativos.R — Diseños alternativos (preregistrados en docs/decisiones.md, 2026-10-02).
#
# Uso:
#   Rscript analisis/08_disenos_alternativos.R todo          # los dos diseños
#   Rscript analisis/08_disenos_alternativos.R apilado
#   Rscript analisis/08_disenos_alternativos.R decaimiento
#   Rscript analisis/08_disenos_alternativos.R regimen       # exploratorio
#
# 1. DiD apilado (Cengiz, Dube, Lindner y Zipperer 2019) con los pesos de Wing, Freedman y
#    Hollingsworth (2024), en el panel municipal trimestral 2019T1–2025T4. Una pila por cohorte g con
#    sus tratadas y sus controles **limpios** (nunca tratados o aún no tratados al cierre de la
#    ventana, G > g + k_post), en una ventana de evento balanceada e ∈ [−k_pre, k_post]. Los
#    controles de la pila a pesan Q_a = (N^D_a / N^D) / (N^C_a / N^C): así la regresión agrupada
#    identifica el ATT agregado "recortado" con pesos iguales a la participación de cada cohorte en
#    las tratadas, sin comparaciones prohibidas ni pesos negativos. Regresión:
#       y_iae = α_ia + λ_e + Σ_{e ≠ −1} δ_e · 1{tratada} · 1{e}   (FE unidad × pila y evento)
#    El estimando es el promedio de δ_0 … δ_k_post; la pre-prueba es la Wald conjunta de δ_−k_pre …
#    δ_−2. Errores agrupados por municipio (una unidad entra en varias pilas como control). Sin
#    covariables: es un contraste transparente del CS doblemente robusto, no un reemplazo.
#    Variante: solo nunca tratados como control.
# 2. Decaimiento espacial en el DENUE (diseño entre actualizaciones, localidad). Las localidades sin
#    sucursal por banda de distancia a la sucursal más cercana (0–2, 2–5 y 5–10 km), fechadas con la
#    G de esa sucursal, contra los mismos controles a ≥10 km. Si el +10% en la actualización de 2024
#    es efecto de la sucursal, debe ser mayor en la localidad con sucursal y caer con la distancia;
#    un perfil plano señala un choque regional (o de incorporación del padrón) que el control lejano
#    no absorbe. Las diferencias entre bandas usan la covarianza agrupada por municipio de las
#    funciones de influencia (comparten controles y municipios).
# 3. Régimen censal (exploratorio, no preregistrado: se propuso después de ver el descriptivo
#    `medicion_por_regimen()`; docs/decisiones.md, 2026-10-02). Los Censos Económicos que alimentan
#    las actualizaciones integrales del DENUE recorren manzana por manzana las cabeceras y las
#    localidades de 2,500+ habitantes y muestrean el resto de lo rural; el 82% de las tratadas está en
#    el primer régimen y el 98% de los controles en el segundo. Se reestima la especificación
#    principal y las bandas **dentro** de cada régimen, con placebo y HonestDiD, y la diferencia
#    entre regímenes.
#
# Salidas: outputs/tablas/apilado_resumen.csv, apilado_evento_<resultado>.csv,
# outputs/figuras/event_apilado_<resultado>.png, outputs/tablas/decaimiento_<resultado>.csv,
# regimen_<resultado>.csv y rob_honest_localidad_act_regimen_total_<resultado>.csv.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
source(here::here("analisis", "05_robustez.R"))  # honest()
suppressPackageStartupMessages({
  library(fixest)
  library(ggplot2)
})

# Qué se apila y contra qué especificación de CS se compara (etiqueta de la maestra).
APILADO <- list(
  list(variante_cs = "hasta_2025",
       resultados = c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")),
  list(variante_cs = "primera_etapa", resultados = "sucursales_total_pc"),
  list(variante_cs = "eacp", resultados = c("capt_ahorro_eacp_pc", "cred_consumo_eacp_pc")),
  list(variante_cs = "imss", resultados = c("ta_pc", "ta_micro_pc", "log_salario_diario"))
)
DENUE_PRINCIPALES <- c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")

#' Escala del efecto porcentual: la media previa de las tratadas, o 1 en los resultados en
#' logaritmo (el efecto ya es proporcional: ×100 = puntos log).
escala_pct <- function(resultado, media) if (startsWith(resultado, "log_")) 1 else abs(media)

# 1. DiD apilado ----------------------------------------------------------------------------------

#' Construye la pila: una sub-muestra por cohorte con ventana de evento completa y controles
#' limpios, balanceada dentro de cada pila, con los pesos de Wing et al.
apilar <- function(dt, resultado, k_pre, k_post, solo_nunca = FALSE) {
  cohortes <- sort(setdiff(unique(dt$G), 0))
  cohortes <- cohortes[cohortes - k_pre >= min(dt$tiempo) & cohortes + k_post <= max(dt$tiempo)]
  if (!length(cohortes)) stop("ninguna cohorte tiene la ventana de evento completa")
  pilas <- lapply(cohortes, function(g) {
    limpio <- if (solo_nunca) dt$G == 0 else dt$G == 0 | dt$G > g + k_post
    d <- dt[(G == g | limpio) & tiempo >= g - k_pre & tiempo <= g + k_post]
    d[, `:=`(pila = g, e = tiempo - g, tratada = as.integer(G == g))]
  })
  st <- rbindlist(pilas)
  st <- st[is.finite(get(resultado))]
  # Balance dentro de la pila: cada unidad con todos los periodos de evento.
  st <- st[, if (.N == k_pre + k_post + 1L) .SD, by = .(pila, id)]
  tam <- st[e == 0, .(n_trat = sum(tratada), n_ctrl = sum(1L - tratada)), by = pila]
  tam <- tam[n_trat > 0 & n_ctrl > 0]
  tam[, q := (n_trat / sum(n_trat)) / (n_ctrl / sum(n_ctrl))]
  st <- merge(st[pila %in% tam$pila], tam[, .(pila, q)], by = "pila")
  st[, peso := fifelse(tratada == 1L, 1, q)]
  st[]
}

#' Estudio de evento apilado ponderado, promedio post y pre-prueba con varianza agrupada.
estimar_apilado <- function(st, resultado, k_pre, k_post) {
  f <- as.formula(paste(resultado, "~ i(e, tratada, ref = -1) | id^pila + e"))
  m <- fixest::feols(f, data = st, weights = ~peso, cluster = ~cluster)
  b <- coef(m)
  V <- vcov(m)
  e <- as.integer(sub("^e::(-?[0-9]+):tratada$", "\\1", names(b)))
  if (anyNA(e)) stop("nombres de coeficientes inesperados: ", paste(names(b), collapse = ", "))
  post <- which(e >= 0 & e <= k_post)
  pre <- which(e < -1)
  l <- rep(1 / length(post), length(post))
  att <- sum(l * b[post])
  ee <- sqrt(drop(crossprod(l, V[post, post] %*% l)))
  bp <- b[pre]
  Vp <- V[pre, pre, drop = FALSE]
  wald <- tryCatch(drop(crossprod(bp, solve(Vp, bp))), error = function(err) NA_real_)
  list(
    att = att, ee = ee,
    pre_n = length(pre), pre_sig = sum(abs(bp / sqrt(diag(Vp))) > stats::qnorm(0.975)),
    pre_wald_p = stats::pchisq(wald, df = length(pre), lower.tail = FALSE),
    evento = data.table(e = c(e, -1L), att = c(unname(b), 0), ee = c(sqrt(diag(V)), 0))[order(e)]
  )
}

#' Fila de CS de la maestra para comparar (misma serie, especificación más cercana).
cs_de_maestra <- function(etq) {
  vacia <- data.table(cs_etiqueta = etq, cs_att = NA_real_, cs_ee = NA_real_,
                      cs_media_base = NA_real_)
  ruta <- file.path(RUTA_TABLAS, "maestra_resultados.csv")
  if (!file.exists(ruta)) return(vacia)
  m <- fread(ruta)[etiqueta == etq & estimador == "Callaway y Sant'Anna"]
  if (!nrow(m)) return(vacia)
  data.table(cs_etiqueta = etq, cs_att = m$valor[1], cs_ee = m$ee[1],
             cs_media_base = m$media_base[1])
}

apilado_uno <- function(resultado, variante_cs) {
  cfg <- PARAMS$estimacion$apilado
  dt <- con_resultado(leer_panel("municipio_trim", diseno = "escalonado", resultado = resultado,
                                 ventana = unlist(cfg$ventana)), resultado)
  cs <- cs_de_maestra(etiqueta_de("municipio_trim", "escalonado", resultado, variante_cs))
  filas <- list()
  eventos <- list()
  for (solo_nunca in c(FALSE, TRUE)) {
    controles <- if (solo_nunca) "solo nunca tratados" else "limpios (nunca + aún no tratados)"
    st <- apilar(dt, resultado, cfg$k_pre, cfg$k_post, solo_nunca)
    est <- estimar_apilado(st, resultado, cfg$k_pre, cfg$k_post)
    media <- st[tratada == 1L & e == -1L, mean(get(resultado))]
    escala <- escala_pct(resultado, media)
    z90 <- stats::qnorm(0.95)
    filas[[length(filas) + 1]] <- data.table(
      resultado = resultado, controles = controles, pilas = uniqueN(st$pila),
      tratadas = uniqueN(st[tratada == 1L]$id), controles_unicos = uniqueN(st[tratada == 0L]$id),
      filas = nrow(st), att = est$att, ee = est$ee, p = 2 * stats::pnorm(-abs(est$att / est$ee)),
      media_base = media, efecto_pct = 100 * est$att / escala,
      cota_equivalencia_pct = 100 * (abs(est$att) + z90 * est$ee) / escala,
      pre_n = est$pre_n, pre_sig = est$pre_sig, pre_wald_p = est$pre_wald_p,
      variante_cs = variante_cs, cs
    )
    eventos[[length(eventos) + 1]] <- est$evento[, controles := controles]
  }
  out <- rbindlist(filas, fill = TRUE)
  escala_cs <- escala_pct(resultado, cs$cs_media_base)  # `resultado` es columna dentro de `out`
  out[, cs_efecto_pct := 100 * cs_att / escala_cs]
  evento <- rbindlist(eventos)
  evento[, resultado := resultado]
  guardar_tabla(evento, paste0("apilado_evento_", resultado))
  p <- ggplot(evento, aes(x = e, y = att, color = controles)) +
    geom_hline(yintercept = 0, linetype = "dashed") +
    geom_vline(xintercept = -0.5, linetype = "dotted") +
    geom_pointrange(aes(ymin = att - 1.96 * ee, ymax = att + 1.96 * ee),
                    position = position_dodge(width = 0.4), size = 0.3) +
    labs(title = paste("DiD apilado (Wing et al. 2024):", resultado),
         subtitle = "Municipio trimestral 2019T1–2025T4 · IC 95% agrupado por municipio · e = −1 base",
         x = "Trimestres desde la apertura", y = "δ_e", color = NULL) +
    theme(legend.position = "bottom")
  guardar_figura(p, paste0("event_apilado_", resultado))
  print(out[, .(resultado, controles, pilas, tratadas, att = round(att, 4), ee = round(ee, 4),
                efecto_pct = round(efecto_pct, 1), wald_p = round(pre_wald_p, 3),
                cs_att = round(cs_att, 4))])
  out
}

apilado_todo <- function() {
  filas <- lapply(APILADO, function(b) {
    rbindlist(lapply(b$resultados, function(r) {
      message("\n#### apilado: ", r)
      tryCatch(apilado_uno(r, b$variante_cs),
               error = function(err) { message("  apilado falló: ", conditionMessage(err)); NULL })
    }), fill = TRUE)
  })
  out <- rbindlist(filas, fill = TRUE)
  if (nrow(out)) guardar_tabla(out, "apilado_resumen")
  invisible(out)
}

# 2. Decaimiento espacial -------------------------------------------------------------------------

#' CS de una muestra con su función de influencia por municipio (clave cve_mun, no el código del
#' cluster, que depende de la muestra).
estimar_banda <- function(nombre, dt, resultado) {
  fit <- estimar_attgt(dt, resultado)
  est <- estimando_principal(fit, dt)
  previa <- prueba_previa(fit, dt)
  claves <- unique(dt[, .(cluster, cve_mun)])
  placebo <- if (nrow(previa$coefs)) previa$coefs[termino == "8"] else data.table()
  list(
    fila = data.table(
      banda = nombre, tratadas = uniqueN(dt[G > 0]$id), controles = uniqueN(dt[G == 0]$id),
      att = est$att, ee = est$ee, media_base = media_base(dt, resultado),
      pre_n = previa$n, pre_sig = previa$n_sig, pre_wald_p = previa$wald_p,
      placebo = if (nrow(placebo)) placebo$att else NA_real_,
      placebo_ee = if (nrow(placebo)) placebo$ee else NA_real_
    ),
    psi = setNames(unname(est$psi_c) / est$n,
                   claves$cve_mun[match(as.integer(names(est$psi_c)), claves$cluster)])
  )
}

#' Diferencia del efecto **en % de la media previa de cada banda** (en niveles no se comparan: la
#' base va de ~13 establecimientos por mil en las vecinas a ~70 en las localidades con sucursal),
#' con la covarianza agrupada por municipio y la media previa tratada como fija:
#' 100·(θ̂_a/m_a − θ̂_b/m_b) − (·) ≈ 100·Σ_c (ψ_ac/(n_a m_a) − ψ_bc/(n_b m_b)).
diferencia <- function(a, b) {
  claves <- union(names(a$psi), names(b$psi))
  pa <- a$psi[claves] / abs(a$fila$media_base); pa[is.na(pa)] <- 0
  pb <- b$psi[claves] / abs(b$fila$media_base); pb[is.na(pb)] <- 0
  dif <- 100 * (a$fila$att / abs(a$fila$media_base) - b$fila$att / abs(b$fila$media_base))
  ee <- 100 * sqrt(sum((pa - pb)^2))
  data.table(contraste = paste(a$fila$banda, "−", b$fila$banda), dif_pct = dif, ee_dif_pct = ee,
             p_dif = 2 * stats::pnorm(-abs(dif / ee)))
}

decaimiento <- function(resultado, regimen = NULL, guardar = TRUE) {
  lee <- function(...) {
    con_resultado(leer_panel("localidad", diseno = "actualizaciones", resultado = resultado,
                             regimen = regimen, ...),
                  resultado)
  }
  bandas <- lapply(PARAMS$estimacion$bandas_derrame_km, unlist)
  nombres <- c("sucursal propia", vapply(bandas, function(b) sprintf("%g–%g km", b[1], b[2]), ""))
  muestras <- c(list(lee()), lapply(bandas, function(b) lee(derrame = TRUE, banda = b)))
  est <- Map(function(n, d) {
    message("  banda ", n, ": ", uniqueN(d[G > 0]$id), " tratadas")
    estimar_banda(n, d, resultado)
  }, nombres, muestras)
  filas <- rbindlist(lapply(est, `[[`, "fila"))
  filas[, efecto_pct := 100 * att / abs(media_base)]
  ultima <- length(est)
  difs <- rbindlist(list(diferencia(est[[1]], est[[2]]), diferencia(est[[1]], est[[ultima]]),
                         diferencia(est[[2]], est[[ultima]])))
  out <- rbindlist(list(filas, difs), fill = TRUE)
  out[, resultado := resultado]
  if (!guardar) return(invisible(list(tabla = out, est = est)))
  guardar_tabla(out, paste0("decaimiento_", resultado))
  print(out[, .(banda, contraste, tratadas, att = round(att, 3), ee = round(ee, 3),
                efecto_pct = round(efecto_pct, 1), wald_p = round(pre_wald_p, 3),
                placebo = round(placebo, 3), dif_pct = round(dif_pct, 1), p_dif = round(p_dif, 3))])
  invisible(out)
}

# 3. Régimen censal -------------------------------------------------------------------------------

#' Especificación principal y bandas dentro de cada régimen de levantamiento del CE, la diferencia
#' de la localidad con sucursal entre regímenes (en % de la media de cada uno) y HonestDiD dentro del
#' régimen de recorrido total.
regimen_censal <- function(resultado) {
  por_regimen <- lapply(c(recorrido_total = "recorrido_total", muestra_rural = "muestra_rural"),
                        function(r) {
    message("  régimen ", r)
    decaimiento(resultado, regimen = r, guardar = FALSE)
  })
  tablas <- rbindlist(lapply(names(por_regimen), function(r) {
    por_regimen[[r]]$tabla[, regimen := r]
  }), fill = TRUE)
  entre <- diferencia(por_regimen$recorrido_total$est[[1]], por_regimen$muestra_rural$est[[1]])
  entre[, `:=`(contraste = "sucursal propia: recorrido total − muestra rural",
               regimen = "entre regímenes", resultado = resultado)]
  out <- rbindlist(list(tablas, entre), fill = TRUE)
  setcolorder(out, c("resultado", "regimen", "banda", "contraste"))
  guardar_tabla(out, paste0("regimen_", resultado))
  print(out[, .(regimen, banda, contraste, tratadas, controles, att = round(att, 3),
                ee = round(ee, 3), efecto_pct = round(efecto_pct, 1),
                wald_p = round(pre_wald_p, 3), placebo = round(placebo, 3),
                dif_pct = round(dif_pct, 1), p_dif = round(p_dif, 3))])
  honest("localidad", resultado, "actualizaciones", variante = "regimen_total",
         regimen = "recorrido_total")
  invisible(out)
}

regimen_todo <- function() {
  for (r in DENUE_PRINCIPALES) {
    message("\n#### régimen censal: ", r)
    tryCatch(regimen_censal(r),
             error = function(err) message("  régimen censal falló: ", conditionMessage(err)))
  }
}

decaimiento_todo <- function() {
  for (r in DENUE_PRINCIPALES) {
    message("\n#### decaimiento: ", r)
    tryCatch(decaimiento(r),
             error = function(err) message("  decaimiento falló: ", conditionMessage(err)))
  }
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { apilado_todo(); decaimiento_todo(); regimen_todo() },
         apilado = apilado_todo(),
         decaimiento = decaimiento_todo(),
         regimen = regimen_todo(),
         stop("uso: Rscript analisis/08_disenos_alternativos.R todo | apilado | decaimiento | regimen"))
}

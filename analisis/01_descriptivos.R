# 01_descriptivos.R — Descriptivos y validación visual de los paneles.
#
# Uso:
#   Rscript analisis/01_descriptivos.R todo
#   Rscript analisis/01_descriptivos.R intensidad
#   Rscript analisis/01_descriptivos.R regimen
#   Rscript analisis/01_descriptivos.R calendario
#   Rscript analisis/01_descriptivos.R estadisticas
#   Rscript analisis/01_descriptivos.R <panel> <resultado>
#
# Produce:
#   1. Tabla de balance en el periodo base por grupo (nunca tratados / cohortes / ya tratados).
#   2. Distribución de cohortes de tratamiento.
#   3. Series del resultado por grupo: la inspección visual de tendencias previas.
#   4. `medicion_denue()`: cuánto cambia el DENUE de una versión a otra en tratadas y controles.
#      Es la evidencia de que entre actualizaciones integrales el resultado casi no se mide
#      (hallazgo C1 de la revisión del 2026-09-29).
#   5. `anillos_descriptivo()`: conteos alrededor de cada localidad por radio. Los anillos salieron
#      de la batería de estimación (fallan tendencias paralelas, se traslapan entre sí y violan
#      SUTVA); quedan como descriptivo del alcance espacial.
#   6. `intensidad_municipal()`: cuántas sucursales del Banco del Bienestar abrió cada municipio
#      tratado y cuántas hay por 10 mil adultos. Justifica no usar un tratamiento continuo: casi
#      todos abren una sola (diseño alternativo 4, descriptivo; docs/decisiones.md, 2026-10-02).
#   7. `medicion_por_regimen()`: salto de cada actualización integral del DENUE según el régimen de
#      levantamiento de los Censos Económicos que la alimenta. Los CE recorren manzana por manzana
#      todas las cabeceras municipales y las localidades de 2,500 habitantes o más; el resto del
#      territorio rural va por muestra probabilística (INEGI, CE 2024, Metodología, 2025).
#   8. `calendario_aperturas()`: qué predice el orden de apertura entre los municipios tratados
#      (diagnóstico descriptivo de la revisión del 2026-10-08).
#   9. `estadisticas_descriptivas()`: media y desviación estándar en 2019T1 de los resultados y las
#      covariables, para tratados y controles de la muestra de estimación financiera (tabla de
#      estadísticas descriptivas del trabajo final; revisión del 2026-10-31).

source(here::here("analisis", "00_utils.R"))
suppressPackageStartupMessages({
  library(ggplot2)
})

descriptivos <- function(panel, resultado) {
  dt <- leer_panel(panel, diseno = "completo", excluir_ya_tratados = FALSE,
                   excluir_ambiguas = FALSE, excluir_sospechosos = FALSE, min_cohorte = NULL,
                   min_pre = NULL, controles = if (panel == "localidad") "todos" else
                     PARAMS$estimacion$controles$principal)
  dt <- con_resultado(dt, resultado)
  base_t <- min(dt$tiempo)

  dt[, grupo := fcase(
    G == 0, "nunca tratado",
    G == base_t, "ya tratado al inicio",
    default = "cohorte tratada"
  )]

  covs <- intersect(c("poblacion_2020", "pobtot", "log_poblacion_2020", "indice_marginacion_2020",
                      "estab_previos", "banca_mun_2019", "desierto_bancario", "dist_bb_km"),
                    names(dt))
  balance <- dt[tiempo == base_t, c(
    list(unidades = .N, resultado_base = mean(get(resultado), na.rm = TRUE)),
    lapply(.SD, mean, na.rm = TRUE)
  ), by = grupo, .SDcols = covs]
  guardar_tabla(balance, paste0("desc_balance_", panel, "_", resultado))
  print(balance)

  cohortes <- dt[tiempo == base_t & G > 0, .N, by = G][order(G)]
  guardar_tabla(cohortes, paste0("desc_cohortes_", panel))

  series <- dt[, .(media = mean(get(resultado), na.rm = TRUE)), by = .(tiempo, grupo)]
  p <- ggplot(series, aes(x = tiempo, y = media, color = grupo)) +
    geom_line(linewidth = 0.8) +
    geom_point(size = 1.2) +
    labs(title = paste("Trayectoria de", resultado),
         subtitle = paste("Panel", panel, "— inspección visual de tendencias previas"),
         x = if (panel == "municipio_trim") "Trimestre (2019T1 = 1)" else "Semestre (2016S1 = 1)",
         y = "Media del grupo", color = NULL) +
    theme(legend.position = "bottom")
  guardar_figura(p, paste0("desc_series_", panel, "_", resultado))

  p2 <- ggplot(cohortes, aes(x = factor(G), y = N)) +
    geom_col(fill = "#2a6f97") +
    labs(title = "Tamaño de cada cohorte de tratamiento",
         subtitle = paste("Panel", panel), x = "Periodo de la primera sucursal", y = "Unidades")
  guardar_figura(p2, paste0("desc_cohortes_", panel))

  invisible(list(balance = balance, cohortes = cohortes))
}

#' Cambio del DENUE entre versiones consecutivas, por grupo: tratadas (aperturas 2020S1–2024S1) y
#' controles de la especificación principal. Si entre actualizaciones integrales casi ninguna
#' localidad cambia, un efecto que ocurra ahí no puede aparecer en los datos hasta la siguiente.
medicion_denue <- function(resultado = "estab_emprendimiento") {
  dt <- leer_panel("localidad", diseno = "completo", resultado = resultado, min_cohorte = NULL,
                   min_pre = NULL)
  act <- PARAMS$estimacion$actualizaciones
  dt[, grupo := fifelse(G == 0, "control (≥10 km)",
                        fifelse(G >= act$g_min & G <= act$g, "tratada", NA_character_))]
  dt <- dt[!is.na(grupo)]
  setorder(dt, id, tiempo)
  dt[, cambio := get(resultado) - shift(get(resultado)), by = id]
  out <- dt[!is.na(cambio), .(
    unidades = .N,
    pct_con_cambio = 100 * mean(cambio != 0),
    cambio_abs_medio = mean(abs(cambio)),
    total = sum(get(resultado))
  ), by = .(tiempo, grupo)]
  totales <- dt[, .(total = sum(get(resultado))), by = .(tiempo, grupo)]
  setorder(totales, grupo, tiempo)
  totales[, crecimiento_pct := 100 * (total / shift(total) - 1), by = grupo]
  out <- merge(out, totales[, .(tiempo, grupo, crecimiento_pct)], by = c("tiempo", "grupo"))
  out[, resultado := resultado]
  setorder(out, grupo, tiempo)
  guardar_tabla(out, paste0("desc_medicion_denue_", resultado))
  p <- ggplot(out, aes(x = tiempo, y = pct_con_cambio, color = grupo)) +
    geom_line(linewidth = 0.8) + geom_point() +
    geom_vline(xintercept = c(8, 18), linetype = "dashed") +
    labs(title = "Localidades cuyo conteo del DENUE cambia respecto de la versión anterior",
         subtitle = "Líneas punteadas: actualizaciones integrales (2019S2 y 2024S2)",
         x = "Semestre (2016S1 = 1)", y = "% de localidades con algún cambio", color = NULL) +
    theme(legend.position = "bottom")
  guardar_figura(p, paste0("desc_medicion_denue_", resultado))
  print(out)
  invisible(out)
}

#' Conteos del DENUE alrededor de cada localidad por radio, tratadas contra no tratadas.
anillos_descriptivo <- function(resultado = "estab_emprendimiento") {
  dt <- as.data.table(arrow::read_parquet(file.path(RUTA_PANELES, PANELES$anillo$archivo)))
  dt <- dt[ya_tratado_inicio == FALSE & fecha_ambigua == FALSE & sospechoso_banjercito == FALSE]
  dt[, grupo := fifelse(G > 0, "con sucursal", "sin sucursal")]
  out <- dt[, .(media = mean(get(resultado), na.rm = TRUE), unidades = uniqueN(cve_loc)),
            by = .(radio_km, s, grupo)]
  guardar_tabla(out, paste0("desc_anillos_", resultado))
  p <- ggplot(out, aes(x = s, y = media, color = grupo)) +
    geom_line(linewidth = 0.8) +
    facet_wrap(~ radio_km, scales = "free_y", labeller = label_both) +
    labs(title = "Establecimientos del DENUE alrededor de cada localidad, por radio",
         subtitle = "Descriptivo: los anillos no identifican (fallan tendencias paralelas)",
         x = "Semestre (2016S1 = 1)", y = "Media de establecimientos", color = NULL) +
    theme(legend.position = "bottom")
  guardar_figura(p, paste0("desc_anillos_", resultado), ancho = 10, alto = 6)
  invisible(out)
}

#' Sucursales del Banco del Bienestar (netas de Banjército) por municipio tratado al cierre de la
#' ventana: distribución del número de sucursales y de sucursales por 10 mil adultos (denominador
#' fijo de 2022T4). Solo municipios que abrieron en la ventana (sin los ya tratados en 2019T1).
intensidad_municipal <- function(corte = PARAMS$periodo$fin) {
  sb <- as.data.table(arrow::read_parquet(here("data", "interim", "sucursales_bienestar.parquet")))
  crudo <- panel_crudo("municipio_trim")
  t_corte <- crudo[periodo == corte, t[1]]
  if (is.na(t_corte)) stop("el panel trimestral no tiene el periodo ", corte)
  mun <- unique(crudo[, .(cve_mun, G, ya_tratado_inicio, poblacion_adulta_fija)])
  x <- merge(sb[periodo == corte, .(cve_mun, suc_bienestar)],
             mun[G > 0 & G <= t_corte & ya_tratado_inicio == FALSE], by = "cve_mun")
  x[, por_10mil := 1e4 * suc_bienestar / poblacion_adulta_fija]
  x[, sucursales := fcase(suc_bienestar <= 0, "0 (cerró)", suc_bienestar == 1, "1",
                          suc_bienestar == 2, "2", default = "3 o más")]
  out <- x[, .(municipios = .N, pct = 100 * .N / nrow(x),
               por_10mil_p10 = stats::quantile(por_10mil, 0.10, na.rm = TRUE),
               por_10mil_mediana = stats::median(por_10mil, na.rm = TRUE),
               por_10mil_p90 = stats::quantile(por_10mil, 0.90, na.rm = TRUE)),
           by = sucursales][order(sucursales)]
  out[, periodo := corte]
  guardar_tabla(out, "desc_intensidad_municipal")
  print(out)
  invisible(out)
}

#' Cambio medio del resultado en las dos actualizaciones integrales (2019S2 y 2024S2) por grupo de
#' la especificación principal (con sucursal, vecinas por banda, controles a ≥10 km) y por régimen
#' de levantamiento del CE: "recorrido total" (cabecera o 2,500+ habitantes) o "muestra rural".
#' Descriptivo: no estima efectos. Si el salto de 2024 depende del régimen y los grupos difieren en
#' régimen, el contraste tratadas–controles mezcla tratamiento y cobertura censal.
medicion_por_regimen <- function(resultado = "estab_emprendimiento_pc") {
  lee <- function(...) leer_panel("localidad", diseno = "actualizaciones", resultado = resultado, ...)
  bandas <- lapply(PARAMS$estimacion$bandas_derrame_km, unlist)
  principal <- lee()
  muestras <- c(
    list(principal[G > 0][, grupo := "1 con sucursal"],
         principal[G == 0][, grupo := "5 control ≥10 km"]),
    Map(function(b, k) lee(derrame = TRUE, banda = b)[G > 0][, grupo := k], bandas,
        sprintf("%d vecina %g–%g km", seq_along(bandas) + 1L,
                vapply(bandas, `[`, 0, 1), vapply(bandas, `[`, 0, 2)))
  )
  d <- rbindlist(muestras, use.names = TRUE)
  d[, regimen := fifelse(es_cabecera | pobtot >= 2500, "recorrido total", "muestra rural")]
  ancho <- dcast(d, id + grupo + regimen ~ tiempo, value.var = resultado)
  out <- ancho[, .(unidades = .N, base_2019S1 = mean(`7`), base_2024S1 = mean(`17`),
                   cambio_2019S2 = mean(`8` - `7`), cambio_2024S2 = mean(`18` - `17`)),
               by = .(grupo, regimen)]
  out[, `:=`(pct_2019S2 = 100 * cambio_2019S2 / base_2019S1,
             pct_2024S2 = 100 * cambio_2024S2 / base_2024S1)]
  out[, pct_unidades_grupo := 100 * unidades / sum(unidades), by = grupo]
  # Diferencia bruta contra los controles del mismo régimen (sin covariables).
  ctrl <- out[grupo == "5 control ≥10 km", .(regimen, c19 = cambio_2019S2, c24 = cambio_2024S2)]
  out <- merge(out, ctrl, by = "regimen")
  out[, `:=`(dif_2019S2_vs_control = cambio_2019S2 - c19,
             dif_2024S2_vs_control = cambio_2024S2 - c24, c19 = NULL, c24 = NULL)]
  out[, resultado := resultado]
  setorder(out, grupo, regimen)
  guardar_tabla(out, paste0("desc_regimen_censal_", resultado))
  print(out)
  invisible(out)
}

#' Predictores del calendario de aperturas: año decimal de apertura (2022.0 = 2022T1) contra las
#' covariables previas estandarizadas y el nivel de sucursales privadas en 2019T1, sin y con efectos
#' fijos de estado. Muestra: municipios tratados de la especificación financiera principal.
#' Diagnóstico descriptivo agregado tras la revisión del 2026-10-08 (no preregistrado): si el orden
#' de apertura fuera casi aleatorio respecto de lo observable, las cohortes tardías son controles
#' creíbles de las tempranas; ee robustos a heterocedasticidad (una fila por municipio).
calendario_aperturas <- function(resultado = "sucursales_privado_pc") {
  d <- leer_panel("municipio_trim", resultado = resultado)
  t0 <- min(d$t)
  x <- unique(d[G > 0, .(cve_mun, G, log_poblacion_2020, indice_marginacion_2020,
                         banca_mun_2019 = as.numeric(banca_mun_2019))])
  x <- merge(x, d[t == t0, .(cve_mun, nivel_2019 = get(resultado))], by = "cve_mun")
  x[, `:=`(anio_apertura = 2019 + (G - 1) / 4, estado = substr(cve_mun, 1, 2))]
  predictores <- c("log_poblacion_2020", "indice_marginacion_2020", "banca_mun_2019", "nivel_2019")
  x <- x[stats::complete.cases(x[, ..predictores])]
  for (v in predictores) set(x, j = v, value = as.numeric(scale(x[[v]])))
  lado_derecho <- paste(predictores, collapse = " + ")
  modelos <- list(
    "sin efectos fijos" = fixest::feols(
      stats::as.formula(paste("anio_apertura ~", lado_derecho)), x, vcov = "hetero"),
    "efectos fijos de estado" = fixest::feols(
      stats::as.formula(paste("anio_apertura ~", lado_derecho, "| estado")), x, vcov = "hetero")
  )
  out <- rbindlist(lapply(names(modelos), function(m) {
    f <- modelos[[m]]
    ct <- fixest::coeftable(f)
    w <- fixest::wald(f, keep = paste(predictores, collapse = "|"), print = FALSE)
    data.table(modelo = m, termino = rownames(ct), coef = ct[, 1], ee = ct[, 2], p = ct[, 4],
               meses = 12 * ct[, 1], n = stats::nobs(f), r2 = fixest::r2(f, "r2"),
               r2_within = if (m == "sin efectos fijos") NA_real_ else fixest::r2(f, "wr2"),
               wald_p = w$p)
  }))
  out <- out[termino != "(Intercept)"]
  out[, `:=`(resultado = resultado, media_anio = mean(x$anio_apertura),
             de_anio = stats::sd(x$anio_apertura))]
  guardar_tabla(out, "desc_calendario_aperturas")
  print(out)
  invisible(out)
}

descriptivos_todo <- function() {
  for (r in c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")) {
    descriptivos("localidad", r)
  }
  descriptivos("municipio_trim", "sucursales_privado_pc")
  medicion_denue("estab_emprendimiento")
  medicion_denue("micro_emprendimiento")
  anillos_descriptivo("estab_emprendimiento")
  intensidad_municipal()
  for (r in c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")) {
    medicion_por_regimen(r)
  }
  calendario_aperturas()
  estadisticas_descriptivas()
}

estadisticas_descriptivas <- function() {
  variables <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc",
                 "poblacion_2020", "poblacion_adulta_fija", "indice_marginacion_2020",
                 "banca_mun_2019")
  dt <- leer_panel("municipio_trim", diseno = "escalonado", resultado = variables[1:5])
  base <- dt[tiempo == min(tiempo)]
  base[, grupo := fifelse(G > 0, "tratados", "controles")]
  out <- rbindlist(lapply(variables, function(v) {
    base[, .(variable = v, n = .N, media = mean(get(v), na.rm = TRUE),
             de = stats::sd(get(v), na.rm = TRUE)), by = grupo]
  }))
  guardar_tabla(out, "desc_estadisticas_municipio_trim")
  print(dcast(out, variable ~ grupo, value.var = c("media", "de")))
  invisible(out)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) >= 1 && args[1] == "todo") {
    descriptivos_todo()
  } else if (length(args) >= 1 && args[1] == "intensidad") {
    intensidad_municipal()
  } else if (length(args) >= 1 && args[1] == "calendario") {
    calendario_aperturas()
  } else if (length(args) >= 1 && args[1] == "estadisticas") {
    estadisticas_descriptivas()
  } else if (length(args) >= 1 && args[1] == "regimen") {
    for (r in c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")) {
      medicion_por_regimen(r)
    }
  } else {
    if (length(args) < 2) stop("uso: Rscript analisis/01_descriptivos.R todo | <panel> <resultado>")
    descriptivos(args[1], args[2])
  }
}

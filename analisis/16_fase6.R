# 16_fase6.R — Fase 6: programas, conveniencia y el DENUE con más detalle. Preregistro y adenda de
# datos en docs/decisiones.md (2026-11-17).
#
# Uso:
#   Rscript analisis/16_fase6.R todo        # todo
#   Rscript analisis/16_fase6.R sectores    # C1 por sector y prueba de composición; C2 sin 52 ni 93
#   Rscript analisis/16_fase6.R reubicacion # C3 y C3b
#   Rscript analisis/16_fase6.R dosis       # C4 por tercil de la proporción de 65+
#   Rscript analisis/16_fase6.R radios      # C5 bandas finas en niveles
#   Rscript analisis/16_fase6.R cabeceras   # C6 y C6b
#   Rscript analisis/16_fase6.R foto        # A-foto: padrón de octubre de 2026 (descriptivo)
#   Rscript analisis/16_fase6.R controles   # D: tabla de grupos de control (ya estimados)
#   Rscript analisis/16_fase6.R resumen     # Romano–Wolf, BH y la lectura preregistrada del DENUE
#
# Como las fases 2–4: no toca la maestra, la tabla final ni sus familias. Los paneles se registran
# aquí y las salidas se llaman `fase6_*`; las tablas por especificación (`cs_*`, `if_*`) llevan el
# panel `localidad_f6` en la etiqueta.

source(here::here("analisis", "10_fase2.R"))  # 00_utils, 02, 05, 07 y 08; correr_bloque()

PANELES$localidad_f6 <- list(archivo = "panel_localidad_f6.parquet", id = "cve_loc", tiempo = "s",
                             per_capita = TRUE, periodicidad = "semestral",
                             ventana = "ventana_semestral")

PANEL_F6 <- "localidad_f6"
BASE <- "estab_emprendimiento_pc"
SECTORES <- c("estab_s46_pc", "estab_s72_pc", "estab_s81_pc", "estab_s3133_pc", "estab_resto_pc")
EXTRAS <- c("G_mun", "mun_ya_tratado", "prop_65_mas", "es_cabecera", "mun_con_apertura")
ACT <- PARAMS$estimacion$actualizaciones
UMBRAL_RECORRIDO <- PARAMS$estimacion$regimen_censal$umbral_poblacion
MITAD_EFECTO_PCT <- 5.2  # mitad del +10.4% de la especificación principal (regla de C6)
BANDAS_FINAS <- list(c(0, 1), c(1, 2), c(2, 3), c(3, 5), c(5, 7.5), c(7.5, 10))

#' Panel de localidades de la fase 6 con el diseño entre actualizaciones y las columnas extra.
leer_f6 <- function(resultado = BASE, ...) {
  dt <- leer_panel(PANEL_F6, diseno = "actualizaciones", resultado = c(resultado, EXTRAS), ...)
  con_resultado(dt, resultado)
}

#' Copia una muestra modificada conservando los atributos que necesita `correr()`.
con_atributos <- function(nuevo, viejo) {
  for (a in c("panel_nombre", "panel_id", "diseno")) setattr(nuevo, a, attr(viejo, a))
  nuevo[, G := as.numeric(G)]
  nuevo[, tratado := as.integer(G > 0 & tiempo >= G)]
  nuevo[]
}

guardar_filas <- function(filas, nombre) {
  out <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
  if (nrow(out)) guardar_tabla(out, nombre)
  invisible(out)
}

# C1 y C2. Sectores ---------------------------------------------------------------------------------

sectores <- function() {
  filas <- lapply(c(SECTORES, "estab_consumo_amplio_pc", "estab_sin_52_93_pc"), function(r) {
    message("\n#### C1/C2 ", r)
    familia <- if (r %in% SECTORES) "denue_sectores" else if (r == "estab_sin_52_93_pc") "c2" else
      "composicion"
    correr(PANEL_F6, r, dt = leer_f6(r), figura = FALSE)$fila[, `:=`(bloque = "C1",
                                                                       familia = familia)]
  })
  out <- guardar_filas(filas, "fase6_sectores")
  # Prueba de composición: consumo amplio (46 + 72 + 81) contra el resto, en % de cada media previa.
  consumo <- estimar_banda("consumo amplio", leer_f6("estab_consumo_amplio_pc"),
                           "estab_consumo_amplio_pc")
  resto <- estimar_banda("resto", leer_f6("estab_resto_pc"), "estab_resto_pc")
  comp <- diferencia(consumo, resto)
  comp[, `:=`(pre_wald_p_consumo = consumo$fila$pre_wald_p, pre_wald_p_resto = resto$fila$pre_wald_p,
              efecto_pct_consumo = 100 * consumo$fila$att / abs(consumo$fila$media_base),
              efecto_pct_resto = 100 * resto$fila$att / abs(resto$fila$media_base))]
  guardar_tabla(comp, "fase6_composicion")
  print(comp)
  invisible(out)
}

# C3. Reubicación dentro del municipio -------------------------------------------------------------

reubicacion <- function() {
  base <- leer_f6()
  controles <- base[G == 0]
  limpio <- controles$mun_con_apertura == FALSE & controles$mun_ya_tratado == FALSE
  en_ventana <- controles$G_mun >= ACT$g_min & controles$G_mun <= ACT$g & !controles$mun_ya_tratado
  c3 <- controles[limpio | en_ventana]
  c3[G_mun >= ACT$g_min & G_mun <= ACT$g & mun_ya_tratado == FALSE, G := ACT$g]
  c3 <- con_atributos(c3, base)
  message("C3: ", uniqueN(c3[G > 0]$id), " lejanas en municipios que abren contra ",
          uniqueN(c3[G == 0]$id), " en municipios sin apertura")
  c3b <- con_atributos(base[G > 0 | (mun_con_apertura == FALSE & mun_ya_tratado == FALSE)], base)
  filas <- list(
    correr(PANEL_F6, BASE, dt = c3, variante = "c3_reubicacion", figura = FALSE)$fila[
      , `:=`(bloque = "C3", familia = "c3")],
    correr(PANEL_F6, BASE, dt = c3b, variante = "c3b_controles_municipio_sin_apertura",
           figura = FALSE)$fila[, `:=`(bloque = "C3b", familia = "c3")]
  )
  guardar_filas(filas, "fase6_reubicacion")
}

# C4. Dosis por intensidad (proporción de 65+, Censo 2020) ----------------------------------------

dosis <- function(resultado = BASE) {
  base <- leer_f6(resultado)
  municipios <- unique(base[, .(cve_mun, prop_65_mas)])
  cortes <- stats::quantile(municipios$prop_65_mas, c(1 / 3, 2 / 3), na.rm = TRUE)
  base[, tercil := fcase(prop_65_mas <= cortes[[1]], "T1", prop_65_mas <= cortes[[2]], "T2",
                         is.finite(prop_65_mas), "T3")]
  filas <- lapply(c("T1", "T2", "T3"), function(t) {
    sub <- con_atributos(base[tercil == t], base)
    f <- variante(t, sub, resultado)
    if (!is.null(f)) f[, municipios := uniqueN(sub$cve_mun)]
    f
  })
  out <- rbindlist(Filter(Negate(is.null), filas), fill = TRUE)
  out[, `:=`(resultado = resultado, corte_t1 = cortes[[1]], corte_t2 = cortes[[2]],
             efecto_pct = 100 * att / abs(media_base),
             ee_pct = 100 * ee / abs(media_base))]
  t1 <- out[variante == "T1"]
  out[, `:=`(dif_pct_vs_t1 = efecto_pct - t1$efecto_pct,
             ee_dif_pct = sqrt(ee_pct^2 + t1$ee_pct^2))]
  out[variante == "T1", `:=`(dif_pct_vs_t1 = NA_real_, ee_dif_pct = NA_real_)]
  out[, p_dif := 2 * stats::pnorm(-abs(dif_pct_vs_t1 / ee_dif_pct))]
  guardar_tabla(out, paste0("fase6_dosis_", resultado))
  print(out[, .(variante, tratadas, controles, efecto_pct = round(efecto_pct, 1),
                wald_p = round(pre_wald_p, 3), dif = round(dif_pct_vs_t1, 1), p_dif = round(p_dif, 3))])
  invisible(out)
}

# C5. Radios en niveles ----------------------------------------------------------------------------

#' CS con la población de cada localidad como peso: el ATT ponderado es el que, multiplicado por la
#' población del grupo, da los establecimientos implicados (revisión del 2026-11-18; el ATT sin
#' ponderar promedia localidades y solo da el total si el efecto por mil no depende del tamaño).
estimar_ponderado <- function(dt, resultado) {
  dt <- copy(dt)
  dt[, peso_pob := pobtot]
  clustervars <- if (any(dt$cluster != dt$id)) "cluster" else "id"
  fit <- did::att_gt(
    yname = resultado, tname = "tiempo", idname = "id", gname = "G",
    xformla = formula_covariables(dt), data = as.data.frame(dt), panel = TRUE,
    allow_unbalanced_panel = FALSE, control_group = "notyettreated", anticipation = 0,
    est_method = PARAMS$estimacion$metodo, base_period = "varying", weightsname = "peso_pob",
    bstrap = PARAMS$estimacion$bootstrap, biters = PARAMS$estimacion$n_boot,
    cband = PARAMS$estimacion$bandas_simultaneas, clustervars = clustervars, alp = 0.05,
    print_details = FALSE
  )
  est <- estimando_principal(fit, dt)
  list(att = est$att, ee = est$ee)
}

radios <- function(resultado = BASE) {
  lee <- function(...) con_resultado(leer_panel(PANEL_F6, diseno = "actualizaciones",
                                                resultado = resultado, ...), resultado)
  nombres <- c("sucursal propia", vapply(BANDAS_FINAS, function(b) sprintf("%g–%g km", b[1], b[2]), ""))
  muestras <- c(list(lee()), lapply(BANDAS_FINAS, function(b) lee(derrame = TRUE, banda = b)))
  filas <- rbindlist(Map(function(n, d) {
    f <- estimar_banda(n, d, resultado)$fila
    pob <- sum(unique(d[G > 0, .(id, pobtot)])$pobtot)
    w <- estimar_ponderado(d, resultado)
    f[, `:=`(poblacion_tratada = pob, att_pond = w$att, ee_pond = w$ee,
             estab_implicados = w$att * pob / 1000, estab_implicados_ee = w$ee * pob / 1000,
             estab_implicados_sin_ponderar = att * pob / 1000)]
  }, nombres, muestras))
  filas[, `:=`(resultado = resultado, efecto_pct = 100 * att / abs(media_base),
               pre_falla = !is.na(pre_wald_p) & pre_wald_p < 0.05,
               pct_del_total = 100 * estab_implicados / sum(estab_implicados),
               pct_del_total_sin_ponderar = 100 * estab_implicados_sin_ponderar /
                 sum(estab_implicados_sin_ponderar))]
  guardar_tabla(filas, paste0("fase6_radios_", resultado))
  print(filas[, .(banda, tratadas, att = round(att, 2), att_pond = round(att_pond, 2),
                  implicados = round(estab_implicados), pct = round(pct_del_total, 1),
                  pct_sin_pond = round(pct_del_total_sin_ponderar, 1),
                  wald_p = round(pre_wald_p, 3))])
  invisible(filas)
}

# C6. Placebo de cabeceras -------------------------------------------------------------------------

cabeceras <- function() {
  base <- leer_f6()
  controles <- base[G == 0]
  falsa <- controles$es_cabecera & !controles$mun_con_apertura & !controles$mun_ya_tratado
  c6 <- copy(controles[falsa | !controles$es_cabecera])
  c6[es_cabecera == TRUE, G := ACT$g]
  c6 <- con_atributos(c6, base)
  c6b <- con_atributos(c6[G > 0 | pobtot >= UMBRAL_RECORRIDO], base)
  message("C6: ", uniqueN(c6[G > 0]$id), " cabeceras sin sucursal contra ",
          uniqueN(c6[G == 0]$id), " controles; C6b: ", uniqueN(c6b[G == 0]$id), " controles")
  filas <- list(
    correr(PANEL_F6, BASE, dt = c6, variante = "c6_placebo_cabeceras", figura = FALSE)$fila[
      , `:=`(bloque = "C6", familia = "c6")],
    correr(PANEL_F6, BASE, dt = c6b, variante = "c6b_placebo_cabeceras_recorrido",
           figura = FALSE)$fila[, `:=`(bloque = "C6b", familia = "c6")]
  )
  guardar_filas(filas, "fase6_cabeceras")
}

# A-foto. Padrón de octubre de 2026 (descriptivo) ----------------------------------------------------

foto <- function() {
  d <- as.data.table(arrow::read_parquet(file.path(RUTA_PANELES, "pub_municipio_f6.parquet")))
  d <- d[!fcoalesce(sospechoso_banjercito, FALSE) & is.finite(benef_100hab) &
           grupo != "otras_aperturas"]
  d[, grupo := factor(grupo, levels = c("sin_apertura", "tratado_2022_2024", "ya_tratado"))]
  d[, monto_miles_pc := monto_pc / 1000]
  medias <- d[, .(municipios = .N, benef_100hab = mean(benef_100hab),
                  monto_miles_pc = mean(monto_miles_pc), prop_65_mas = mean(prop_65_mas)),
              by = grupo][order(grupo)]
  ajustes <- rbindlist(lapply(c("benef_100hab", "monto_miles_pc"), function(y) {
    f <- as.formula(paste(y, "~ grupo + log_poblacion_2020 + indice_marginacion_2020 +",
                          "banca_mun_2019 + prop_65_mas | cve_ent"))
    m <- fixest::feols(f, data = d, vcov = "hetero")
    ct <- as.data.table(fixest::coeftable(m), keep.rownames = "termino")
    ct[startsWith(termino, "grupo"), .(resultado = y, termino, dif = Estimate, ee = `Std. Error`,
                                       p = `Pr(>|t|)`, n = stats::nobs(m))]
  }))
  guardar_tabla(medias, "fase6_pub_medias")
  guardar_tabla(ajustes, "fase6_pub_ajuste")
  print(medias)
  print(ajustes)
  invisible(list(medias = medias, ajustes = ajustes))
}

# D. Grupos de control (ya estimados) --------------------------------------------------------------

controles_tabla <- function() {
  lee <- function(n) {
    ruta <- file.path(RUTA_TABLAS, paste0(n, ".csv"))
    if (file.exists(ruta)) fread(ruta) else data.table()
  }
  fin <- rbindlist(lapply(c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc"),
                          function(r) {
    rob <- lee(paste0("rob_municipio_trim_esc_", r))
    rob <- rob[startsWith(variante, "base") | variante == "solo nunca tratados como control"]
    f4 <- lee("fase4_controles")[resultado == r & startsWith(variante, "H1")]
    ap <- lee("apilado_resumen")[resultado == r]
    rbindlist(list(
      rob[, .(resultado = r, fuente = "rob", variante, tratadas, controles, att, ee, media_base,
              pre_wald_p)],
      f4[, .(resultado = r, fuente = "fase4", variante, tratadas, controles, att, ee, media_base,
             pre_wald_p)],
      ap[, .(resultado = r, fuente = "apilado", variante = paste("apilado:", controles), tratadas,
             controles = controles_unicos, att, ee, media_base, pre_wald_p)]
    ), fill = TRUE)
  }), fill = TRUE)
  fin[, `:=`(efecto_pct = 100 * att / abs(media_base),
             cota_pct = 100 * (abs(att) + stats::qnorm(0.95) * ee) / abs(media_base))]
  denue <- lee("rob_localidad_act_estab_emprendimiento_pc")
  if (nrow(denue)) {
    denue <- denue[, .(resultado = BASE, fuente = "rob", variante, tratadas, controles, att, ee,
                       media_base, pre_wald_p)]
    denue[, `:=`(efecto_pct = 100 * att / abs(media_base),
                 cota_pct = 100 * (abs(att) + stats::qnorm(0.95) * ee) / abs(media_base))]
  }
  out <- rbindlist(list(fin, denue), fill = TRUE)
  guardar_tabla(out, "fase6_controles")
  guardar_tabla(lee("poder_inyectado_diagnostico"), "fase6_deriva_nunca_tratados")
  print(out[, .(resultado, variante, tratadas, controles, efecto_pct = round(efecto_pct, 1),
                cota = round(cota_pct, 1), wald_p = round(pre_wald_p, 3))])
  invisible(out)
}

# Resumen y lectura preregistrada -----------------------------------------------------------------

resumen <- function() {
  lee <- function(n) {
    ruta <- file.path(RUTA_TABLAS, paste0(n, ".csv"))
    if (file.exists(ruta)) fread(ruta) else data.table()
  }
  cs <- rbindlist(lapply(c("fase6_sectores", "fase6_reubicacion", "fase6_cabeceras"), lee),
                  fill = TRUE)
  if (!nrow(cs)) return(message("sin resultados de la fase 6"))
  z90 <- stats::qnorm(0.95)
  cs[, escala := abs(media_base)]
  cs[, `:=`(p = 2 * stats::pnorm(-abs(valor / ee)), efecto_pct = 100 * valor / escala,
            ic90_alto_pct = 100 * (valor + z90 * ee) / escala,
            mde80_pct = 100 * (stats::qnorm(0.975) + stats::qnorm(0.80)) * ee / escala,
            cota_equivalencia_pct = 100 * (abs(valor) + z90 * ee) / escala)]
  cs[, escala := NULL]
  cs[, nulo_informativo := p >= 0.05 & cota_equivalencia_pct <= PARAMS$estimacion$sesoi_pct]
  cs[, pre_falla := !is.na(pre_wald_p) & pre_wald_p < 0.05]
  cs[, q_bh_fase6 := stats::p.adjust(p, method = "BH")]
  sect <- cs[familia == "denue_sectores"]
  if (nrow(sect)) {
    cs <- merge(cs, romano_wolf(sect$etiqueta, sect$valor)[, .(etiqueta, p_rw)], by = "etiqueta",
                all.x = TRUE)
  }
  cs[, lectura := fcase(pre_falla, "descriptivo (pre-prueba falla)",
                        nulo_informativo, "nulo informativo",
                        p < 0.05 & q_bh_fase6 < 0.05, "significativo (sobrevive BH)",
                        p < 0.05, "significativo sin corrección (BH q ≥ 0.05)",
                        default = "no informativo")]
  guardar_tabla(cs, "fase6_resumen")
  print(cs[, .(bloque, resultado, variante = etiqueta, tratadas = n_tratadas,
               efecto_pct = round(efecto_pct, 1), cota = round(cota_equivalencia_pct, 1),
               wald_p = round(pre_wald_p, 3), lectura)])
  lectura_denue(cs, lee("fase6_composicion"), lee(paste0("fase6_dosis_", BASE)))
}

#' Regla preregistrada para leer el +10% del DENUE.
lectura_denue <- function(cs, comp, dos) {
  c6 <- cs[bloque == "C6"]
  t3 <- dos[variante == "T3"]
  cond <- data.table(
    condicion = c("C1 consumo amplio > resto (p < 0.05, ambos con previos planos)",
                  "C4 T3 > T1 en % (p < 0.05)",
                  "C6 placebo no significativo y con IC90 < +5.2%",
                  "C6 placebo significativo y de +5.2% o más (medición)"),
    cumple = c(
      nrow(comp) == 1 && comp$dif_pct > 0 && comp$p_dif < 0.05 &&
        comp$pre_wald_p_consumo >= 0.05 && comp$pre_wald_p_resto >= 0.05,
      nrow(t3) == 1 && t3$dif_pct_vs_t1 > 0 && t3$p_dif < 0.05,
      nrow(c6) == 1 && c6$p >= 0.05 && c6$ic90_alto_pct < MITAD_EFECTO_PCT,
      nrow(c6) == 1 && c6$p < 0.05 && c6$efecto_pct >= MITAD_EFECTO_PCT
    )
  )
  lectura <- if (all(cond$cumple[1:3])) {
    "efecto de zona compatible con el gasto de los programas"
  } else if (cond$cumple[4]) {
    "medición o efecto de cabecera"
  } else {
    "no se distingue entre gasto y medición"
  }
  cond[, lectura := lectura]
  guardar_tabla(cond, "fase6_lectura_denue")
  print(cond)
  invisible(cond)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  que <- if (length(args)) args[1] else "todo"
  switch(que,
         todo = { sectores(); reubicacion(); dosis(); radios(); cabeceras(); foto();
                  controles_tabla(); resumen() },
         sectores = sectores(),
         reubicacion = reubicacion(),
         dosis = dosis(),
         radios = radios(),
         cabeceras = cabeceras(),
         foto = foto(),
         controles = controles_tabla(),
         resumen = resumen(),
         stop("uso: Rscript analisis/16_fase6.R todo | sectores | reubicacion | dosis | radios | ",
              "cabeceras | foto | controles | resumen"))
}

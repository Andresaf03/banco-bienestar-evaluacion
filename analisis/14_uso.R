# 14_uso.R — Fase 5 (exploratoria, no preregistrada): ¿se usan las cuentas del banco?
#
# Uso:
#   Rscript analisis/14_uso.R
#
# Callaway y Sant'Anna con la especificación base (doblemente robusto, aún no tratados, covariables
# base) en la ventana 2022T4–2025T4, la única en que la BDIF separa a la banca de desarrollo. Por la
# regla 10 entran solo las cohortes con dos trimestres previos en esa ventana (aperturas de 2023T2 en
# adelante). Salen los municipios donde Banjército tuvo sucursal: fuera de ellos la banca de
# desarrollo de la BDIF es solo el Banco del Bienestar (adenda de la fase 4).
#
# Resultados por diez mil adultos de la banca de desarrollo: contratos de captación, de depósitos a
# plazo y de crédito (total y personal), tarjetas de débito y transacciones en cajeros. Los niveles de
# cuenta (N1–N4) no se estiman: la CNBV los reclasificó en 2025T2 (de N4 a N2 en todo el país) y ese
# salto se leería como efecto; quedan como descriptivo. Las cuentas de ahorro y las asociadas a un
# celular no se estiman: la BDIF las reporta en cero para el banco en toda la ventana.
#
# Sensibilidad: sin 2024T2, el trimestre en que la captación del banco cae 74% en todo el país y luego
# se recupera (cambio de reporte, no de comportamiento).
#
# No entra en la maestra, la tabla final ni las familias de inferencia múltiple.
#
# Salidas: outputs/tablas/uso_{resumen,sensibilidad}.csv y las de cada especificación
# (cs_*_municipio_uso_esc_*).

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))

# Panel de la fase 5 (src/proyecto/construccion/panel_uso.py).
PANELES$municipio_uso <- list(archivo = "panel_municipio_uso.parquet", id = "cve_mun",
                              tiempo = "t", per_capita = TRUE, periodicidad = "trimestral")
VENTANA_USO <- c(16L, 28L)  # 2022T4–2025T4
RESULTADOS_USO <- c("capt_total_bd_pc", "cred_total_bd_pc", "tarjetas_debito_bd_pc",
                    "capt_plazo_bd_pc", "cred_personal_bd_pc", "transacciones_cajeros_bd_pc")
SENSIBILIDAD_USO <- c("capt_total_bd_pc", "capt_plazo_bd_pc", "cred_total_bd_pc")
T_2024T2 <- 22L

#' Muestra de la fase: ventana 2022T4–2025T4 sin los municipios con Banjército.
leer_uso <- function(resultado, ids, sin_2024t2 = FALSE) {
  dt <- leer_panel("municipio_uso", resultado = resultado, ventana = VENTANA_USO, ids = ids)
  if (!sin_2024t2) return(dt)
  sub <- dt[tiempo != T_2024T2]
  for (a in c("panel_nombre", "panel_id", "diseno")) setattr(sub, a, attr(dt, a))
  sub
}

completar <- function(filas) {
  z90 <- stats::qnorm(0.95)
  filas[, `:=`(p = 2 * stats::pnorm(-abs(valor / ee)),
               ic90_bajo = valor - z90 * ee, ic90_alto = valor + z90 * ee,
               pre_falla = !is.na(pre_wald_p) & pre_wald_p < 0.05)]
}

uso <- function() {
  crudo <- panel_crudo("municipio_uso")
  ids <- unique(crudo[con_banjercito == FALSE]$cve_mun)
  message(sprintf("municipios sin Banjército: %d de %d", length(ids), uniqueN(crudo$cve_mun)))
  filas <- rbindlist(lapply(RESULTADOS_USO, function(r) {
    message("\n#### municipio_uso / ", r)
    correr("municipio_uso", r, dt = leer_uso(r, ids), variante = "uso", figura = FALSE)$fila
  }), fill = TRUE)
  guardar_tabla(completar(filas), "uso_resumen")
  print(filas[, .(resultado, valor, ee, media_base, pre_wald_p, n_tratadas, n_controles)])

  sens <- rbindlist(lapply(SENSIBILIDAD_USO, function(r) {
    message("\n#### municipio_uso sin 2024T2 / ", r)
    correr("municipio_uso", r, dt = leer_uso(r, ids, sin_2024t2 = TRUE),
           variante = "uso_sin2024t2", figura = FALSE)$fila
  }), fill = TRUE)
  guardar_tabla(completar(sens), "uso_sensibilidad")
  print(sens[, .(resultado, valor, ee, pre_wald_p)])
  invisible(filas)
}

if (sys.nframe() == 0) uso()

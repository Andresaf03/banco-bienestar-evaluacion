# 06_correr_todo.R — Batería de estimación: especificaciones × estimadores.
#
# Uso:
#   Rscript analisis/06_correr_todo.R                  # todo el registro
#   Rscript analisis/06_correr_todo.R emprendimiento   # un bloque
#   Rscript analisis/06_correr_todo.R emprendimiento localidad
#
# Cada fila del registro `ESPECIFICACIONES` es una estimación: bloque, panel, diseño, variante y
# resultado, con la ventana del resultado cuando la fuente no lo publica en todo el panel. Produce
# el ATT (Callaway y Sant'Anna) con su pre-prueba y los estimadores de comparación, y consolida todo
# en outputs/tablas/maestra_resultados.csv. La especificación principal está preregistrada en
# docs/decisiones.md (2026-09-29).
#
# Una columna del registro que no exista en el panel es un error, no un aviso: así fue como el
# margen de empleo (`empleo_est_*`) se saltó en silencio durante toda la batería anterior.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))
source(here::here("analisis", "03_twfe_comparacion.R"))

DENUE_EMPRENDIMIENTO <- c("estab_emprendimiento_pc", "micro_emprendimiento_pc",
                          "empleo_est_emprendimiento_pc")
DENUE_CONSUMO <- c("estab_consumo_pc", "estab_abarrotes_pc", "estab_restaurantes_pc")
DENUE_SALUD <- c("estab_salud_pc", "estab_farmacia_pc", "estab_consultorios_pc")
# Los tres resultados principales de cada bloque del DENUE: los que llevan derrame, matching,
# robustez y heterogeneidad.
DENUE_PRINCIPALES <- c("estab_emprendimiento_pc", "estab_consumo_pc", "estab_salud_pc")

# Trimestres de la BDIF (t = 1 en 2019T1). Cajeros, TPV, transacciones, captación y crédito por
# sector solo existen desde 2022T4 (t = 16): se estiman en ese panel corto, con las cohortes que
# tienen al menos dos trimestres previos (2023T2 en adelante). Los corresponsales cambian de
# metodología en 2020T4 y en 2024T1: se estiman entre las dos rupturas (2021T1–2023T4).
T_2022Q4 <- 16L
T_2024Q4 <- 24L
T_2025Q4 <- 28L
VENTANA_CORRESPONSALES <- c(9L, 20L)

# Ampliación financiera (fase 0, preregistrada en docs/decisiones.md el 2026-09-30).
FINANCIERA_PRINCIPALES <- c("sucursales_privado_pc", "sucursales_bm_pc", "sucursales_eacp_pc")
PANEL_CORTO_FINANCIERO <- c("captacion_privado_pc", "credito_privado_pc")
PANEL_CORTO_CONSUMO <- c("cajeros_privado_pc", "tpv_privado_pc", "transacciones_tpv_privado_pc")
# Captación y crédito de las EACP (SOCAP + SOFIPO), continuos 2016T1–2025T4: "¿desplazó a las EACP?"
# sin depender del panel corto.
EACP_LARGAS <- c("capt_ahorro_eacp_pc", "capt_plazo_eacp_pc", "capt_vista_eacp_pc",
                 "cred_consumo_eacp_pc", "cred_vivienda_eacp_pc", "tarjetas_debito_eacp_pc")
# Inclusión total: banca múltiple + banca de desarrollo, **con** el Banco del Bienestar adentro
# (efecto mecánico: el banco dispersa programas sociales en cuentas propias).
INCLUSION_TOTAL <- c("capt_ahorro_banca_pc", "capt_plazo_banca_pc", "tarjetas_debito_banca_pc",
                     "cuentas_celular_total_pc")
# Primera etapa de inclusión: cuentas del propio banco (banca de desarrollo), solo desde 2022T4. Las
# cuentas en celular de la banca de desarrollo no entran: valen cero en todo el panel.
INCLUSION_BANCO <- c("capt_total_bd_pc", "tarjetas_debito_bd_pc")

# Fase 1 (preregistrada en docs/decisiones.md el 2026-09-30): actividad medida de forma continua.
# Empleo formal del IMSS (cierres de trimestre) y remesas de Banxico en el panel trimestral;
# Censos Económicos 2004–2024 en su propio panel (una cohorte en el CE 2024, tres placebos).
IMSS <- c("ta_pc", "ta_micro_pc", "ta_pequena_pc", "log_salario_diario")
REMESAS <- c("remesas_usd_adulto")
CENSOS_ECONOMICOS <- c("ue_pc", "personal_ocupado_pc", "log_remuneraciones", "log_vacb",
                       "log_produccion_bruta")

especificacion <- function(bloque, panel, resultado, diseno, variante = "principal",
                           controles = NULL, derrame = FALSE, desde = NA_integer_,
                           hasta = NA_integer_) {
  data.table(bloque = bloque, panel = panel, resultado = resultado, diseno = diseno,
             variante = variante, controles = controles %||% NA_character_, derrame = derrame,
             desde = desde, hasta = hasta)
}

ESPECIFICACIONES <- rbindlist(list(
  # DENUE, localidad: principal (entre actualizaciones) y secundaria (ventana escalonada).
  especificacion("emprendimiento", "localidad", DENUE_EMPRENDIMIENTO, "actualizaciones"),
  especificacion("consumo",        "localidad", DENUE_CONSUMO,        "actualizaciones"),
  especificacion("salud",          "localidad", DENUE_SALUD,          "actualizaciones"),
  especificacion("emprendimiento", "localidad", DENUE_EMPRENDIMIENTO, "escalonado", "secundaria"),
  especificacion("consumo",        "localidad", DENUE_CONSUMO,        "escalonado", "secundaria"),
  especificacion("salud",          "localidad", DENUE_SALUD,          "escalonado", "secundaria"),
  # Derrame: localidades sin sucursal a menos de 10 km de una que abrió, contra las lejanas.
  especificacion("emprendimiento", "localidad", DENUE_PRINCIPALES[1], "actualizaciones", "derrame",
                 derrame = TRUE),
  especificacion("consumo",        "localidad", DENUE_PRINCIPALES[2], "actualizaciones", "derrame",
                 derrame = TRUE),
  especificacion("salud",          "localidad", DENUE_PRINCIPALES[3], "actualizaciones", "derrame",
                 derrame = TRUE),
  # DENUE, municipio: mismos dos diseños.
  especificacion("emprendimiento", "municipio", DENUE_EMPRENDIMIENTO, "actualizaciones", "secundaria"),
  especificacion("consumo",        "municipio", DENUE_CONSUMO,        "actualizaciones", "secundaria"),
  especificacion("salud",          "municipio", DENUE_SALUD[1:2],     "actualizaciones", "secundaria"),
  especificacion("emprendimiento", "municipio", DENUE_EMPRENDIMIENTO, "escalonado", "secundaria"),
  especificacion("consumo",        "municipio", DENUE_CONSUMO,        "escalonado", "secundaria"),
  especificacion("salud",          "municipio", DENUE_SALUD[1:2],     "escalonado", "secundaria"),
  # BDIF: financiera principal, primera etapa y secundarias con su ventana.
  especificacion("financiero", "municipio_trim", FINANCIERA_PRINCIPALES, "escalonado"),
  especificacion("primera_etapa", "municipio_trim", "sucursales_total_pc", "escalonado",
                 "primera_etapa"),
  especificacion("financiero", "municipio_trim", "corresponsales_total_pc", "escalonado",
                 "secundaria", desde = VENTANA_CORRESPONSALES[1], hasta = VENTANA_CORRESPONSALES[2]),
  especificacion("financiero", "municipio_trim", PANEL_CORTO_FINANCIERO,
                 "escalonado", "panel_corto", desde = T_2022Q4, hasta = T_2024Q4),
  especificacion("consumo", "municipio_trim", PANEL_CORTO_CONSUMO,
                 "escalonado", "panel_corto", desde = T_2022Q4, hasta = T_2024Q4),
  # Ampliación financiera (fase 0): series nuevas con el panel hasta 2025T4 y extensiones a 2025T4
  # de las especificaciones preregistradas antes (que conservan su ventana original).
  especificacion("financiero", "municipio_trim", EACP_LARGAS, "escalonado", "eacp",
                 desde = 1L, hasta = T_2025Q4),
  especificacion("inclusion", "municipio_trim", INCLUSION_TOTAL, "escalonado", "inclusion_total",
                 desde = 1L, hasta = T_2025Q4),
  especificacion("primera_etapa", "municipio_trim", INCLUSION_BANCO, "escalonado",
                 "primera_etapa", desde = T_2022Q4, hasta = T_2025Q4),
  especificacion("financiero", "municipio_trim", FINANCIERA_PRINCIPALES, "escalonado",
                 "hasta_2025", desde = 1L, hasta = T_2025Q4),
  especificacion("financiero", "municipio_trim", PANEL_CORTO_FINANCIERO, "escalonado",
                 "panel_corto_2025", desde = T_2022Q4, hasta = T_2025Q4),
  especificacion("consumo", "municipio_trim", PANEL_CORTO_CONSUMO, "escalonado",
                 "panel_corto_2025", desde = T_2022Q4, hasta = T_2025Q4),
  # Fase 1.
  especificacion("empleo_formal", "municipio_trim", IMSS, "escalonado", "imss",
                 desde = 1L, hasta = T_2025Q4),
  especificacion("remesas", "municipio_trim", REMESAS, "escalonado", "remesas",
                 desde = 1L, hasta = T_2025Q4),
  especificacion("censos_economicos", "municipio_ce", CENSOS_ECONOMICOS, "escalonado", "ce")
))

# Presencia financiera privada según el DENUE: se conserva como **descriptivo** (no entra en la
# maestra) por las seis rupturas de cobertura del SCIAN 52, varias en el pre-periodo. Ver
# docs/decisiones.md (2026-09-26). Correr a mano si se quiere:
#   Rscript analisis/02_cs_did.R localidad estab_banca_pc
DENUE_FINANCIERO_DESCRIPTIVO <- c("estab_financiero_pc", "estab_banca_pc", "estab_cajas_pc")

`%|na|%` <- function(a, b) if (is.null(a) || is.na(a)) b else a

#' Verifica el registro contra el esquema de los paneles **antes** de estimar nada.
validar_registro <- function(especificaciones) {
  for (p in unique(especificaciones$panel)) {
    columnas <- names(arrow::read_parquet(file.path(RUTA_PANELES, PANELES[[p]]$archivo),
                                          as_data_frame = FALSE))
    faltan <- setdiff(especificaciones[panel == p]$resultado, columnas)
    if (length(faltan)) {
      stop("el registro pide columnas que el panel '", p, "' no tiene: ",
           paste(faltan, collapse = ", "))
    }
  }
  invisible(TRUE)
}

#' Corre una especificación: CS una sola vez y los estimadores de comparación sobre la misma
#' muestra. Devuelve las filas de la maestra (NULL si ninguna cohorte tiene periodos previos).
corre_uno <- function(spec) {
  ventana <- if (is.na(spec$desde)) NULL else c(spec$desde, spec$hasta)
  controles <- spec$controles %|na|% PARAMS$estimacion$controles$principal
  dt <- leer_panel(spec$panel, diseno = spec$diseno, resultado = spec$resultado,
                   controles = controles,
                   derrame = spec$derrame, ventana = ventana)
  dt <- con_resultado(dt, spec$resultado)
  if (!nrow(dt[G > 0])) {
    message("  (salta) ", spec$panel, "/", spec$resultado, ": ninguna cohorte con ",
            "periodos previos suficientes en la ventana")
    return(NULL)
  }
  variante <- if (spec$variante %in% c("principal", "secundaria")) NULL else spec$variante
  etiqueta <- etiqueta_de(spec$panel, spec$diseno, spec$resultado, variante)
  message("\n== ", spec$bloque, " | ", etiqueta)
  cs <- tryCatch(correr(spec$panel, spec$resultado, dt = dt, etiqueta = etiqueta),
                 error = function(e) { message("  CS falló: ", conditionMessage(e)); NULL })
  if (is.null(cs)) return(NULL)
  comp <- tryCatch(resumir(spec$panel, spec$resultado, dt = dt, cs = cs$fila, etiqueta = etiqueta),
                   error = function(e) {
                     message("  comparación falló: ", conditionMessage(e))
                     cs$fila[, .(estimador, valor, ee)]
                   })
  otros <- comp[estimador != "Callaway y Sant'Anna", .(estimador, valor, ee)]
  otros[, etiqueta := etiqueta]
  filas <- rbindlist(list(cs$fila, otros), fill = TRUE)
  filas[, `:=`(bloque = spec$bloque, variante = spec$variante,
               controles = if (spec$panel == "localidad") controles else NA_character_,
               panel = spec$panel, diseno = spec$diseno, resultado = spec$resultado)]
  filas[]
}

correr_todo <- function(bloques = NULL, paneles = NULL) {
  especs <- ESPECIFICACIONES
  if (!is.null(bloques)) especs <- especs[bloque %in% bloques]
  if (!is.null(paneles)) especs <- especs[panel %in% paneles]
  validar_registro(especs)
  filas <- lapply(seq_len(nrow(especs)), function(i) corre_uno(especs[i]))
  filas <- Filter(Negate(is.null), filas)
  if (!length(filas)) {
    message("no se produjo ningún resultado: ¿están construidos los paneles? (`make panel`)")
    return(invisible(NULL))
  }
  maestra <- rbindlist(filas, fill = TRUE)
  # Con un subconjunto del registro (un bloque o un panel), la maestra existente se conserva y solo
  # se reemplazan las especificaciones que se volvieron a estimar.
  ruta_maestra <- file.path(RUTA_TABLAS, "maestra_resultados.csv")
  if ((!is.null(bloques) || !is.null(paneles)) && file.exists(ruta_maestra)) {
    previa <- fread(ruta_maestra)
    maestra <- rbindlist(list(previa[!etiqueta %in% maestra$etiqueta], maestra), fill = TRUE)
  }
  maestra[, `:=`(ic_bajo = valor - stats::qnorm(0.975) * ee,
                 ic_alto = valor + stats::qnorm(0.975) * ee,
                 p = 2 * stats::pnorm(-abs(valor / ee)))]
  setcolorder(maestra, c("bloque", "panel", "diseno", "variante", "controles", "resultado",
                         "estimador", "valor", "ee"))
  guardar_tabla(maestra, "maestra_resultados")
  message("\n== resumen (Callaway y Sant'Anna)")
  print(maestra[estimador == "Callaway y Sant'Anna",
                .(panel, diseno, variante, resultado, att = round(valor, 4), ee = round(ee, 4),
                  pre = paste0(pre_sig, "/", pre_n), wald_p = round(pre_wald_p, 3))])
  invisible(maestra)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  bloques <- if (length(args) >= 1) args[1] else NULL
  paneles <- if (length(args) >= 2) args[2] else NULL
  correr_todo(bloques, paneles)
}

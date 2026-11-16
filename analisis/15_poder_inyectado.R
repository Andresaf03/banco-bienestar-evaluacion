# 15_poder_inyectado.R — ¿El DiD detecta un efecto chico cuando sí existe? (exploratoria)
#
# Uso:
#   Rscript analisis/15_poder_inyectado.R              # corrida completa
#   Rscript analisis/15_poder_inyectado.R verificar    # comprueba el código, sin réplicas
#   Rscript analisis/15_poder_inyectado.R medir 12     # segundos por réplica; no muestra estimaciones
#   Rscript analisis/15_poder_inyectado.R diagnostico  # de dónde sale el centro de las fechas barajadas
#   Rscript analisis/15_poder_inyectado.R calibrado    # potencia con fechas barajadas entre todas
#
# Se agregan sucursales privadas ficticias a los datos y se estima con la especificación base del
# bloque financiero (Callaway y Sant'Anna, doblemente robusto, aún no tratados, 2019T1–2024T4), como
# en Bertrand, Duflo y Mullainathan (2004). Los escenarios están en `poder_inyectado` de
# config/parametros.yaml.
#
#   - Atracción: cada municipio tratado recibe Poisson(λ · adultos / 10 mil) sucursales desde su
#     apertura. El efecto esperado es λ en todos los municipios, pero llega en sucursales enteras:
#     unos pocos municipios cargan con todo, como pasaría con un efecto real.
#   - Desplazamiento: cada sucursal privada que ya existía cierra con probabilidad igual al efecto.
#     En los desiertos bancarios no hay nada que cerrar.
#
# Dos formas de correrlo, porque el estimador es lineal en el resultado y sumar δ a las tratadas
# mueve el ATT exactamente en el promedio de δ (`verificar` lo comprueba):
#   - `reales`: las fechas verdaderas. La estimación es la real más lo inyectado, así que solo cambian
#     el efecto sorteado y el ee: responde qué habríamos visto en estos datos.
#   - `reasignadas`: las fechas se barajan entre los municipios tratados de cada estado, y cada réplica
#     trae su propio ruido. Da la potencia propiamente dicha y, sin efecto, la tasa de falsos positivos.
#
# No entra en la maestra, la tabla final ni las familias de inferencia múltiple.
#
# Salidas: outputs/tablas/poder_inyectado_{resumen,replicas}.csv y, por escenario,
# outputs/intermedios/poder_<fechas>_<escenario>_r<réplicas>.csv (una corrida interrumpida sigue desde
# ahí). El diagnóstico (exploratorio, después de ver la corrida; `docs/decisiones.md`) deja
# outputs/tablas/poder_inyectado_{diagnostico,calibrado}.csv.

source(here::here("analisis", "00_utils.R"))
source(here::here("analisis", "02_cs_did.R"))

CFG <- PARAMS$poder_inyectado
RESULTADO <- "sucursales_privado_pc"
CONTEO <- "sucursales_privado"
ADULTOS <- "poblacion_adulta_fija"
POR_ADULTOS <- 1e4
Z90 <- stats::qnorm(0.95)
Z95 <- stats::qnorm(0.975)
UMBRAL_NULO <- PARAMS$estimacion$sesoi_pct

# El ee de Liang–Zeger sale de la función de influencia; el bootstrap solo alimenta `ee_boot` y las
# bandas de las figuras, y aquí costaría 999 réplicas por estimación.
PARAMS$estimacion$bootstrap <- FALSE
PARAMS$estimacion$bandas_simultaneas <- FALSE
setDTthreads(1L)

panel_base <- function() {
  con_resultado(leer_panel("municipio_trim", resultado = c(RESULTADO, CONTEO, ADULTOS)), RESULTADO)
}

estimar <- function(dt) {
  p <- estimando_principal(estimar_attgt(dt, RESULTADO), dt)
  list(att = p$att, ee = p$ee)
}

#' Baraja las fechas entre los municipios tratados de cada estado: conserva qué municipios abren, cuántos
#' por cohorte en cada estado y la comparación contra los nunca tratados.
reasignar_fechas <- function(dt) {
  u <- dt[!duplicated(id) & G > 0, .(id, ent = substr(cve_mun, 1, 2), G)]
  u[, G_r := G[sample.int(.N)], by = ent]
  d <- copy(dt)
  d[u, on = "id", G := i.G_r]
  d
}

#' Sucursales ficticias por municipio tratado (k, con signo) y el trimestre en que aparecen.
sortear <- function(d, esc, media) {
  u <- d[G > 0 & tiempo == G - 1, .(id, G, adultos = get(ADULTOS), previas = get(CONTEO))]
  n <- nrow(u)
  u[, k := switch(esc$tipo,
    ninguno = rep(0, n),
    atraccion = as.numeric(stats::rpois(n, esc$pct / 100 * media * adultos / POR_ADULTOS)),
    desplazamiento = -as.numeric(stats::rbinom(n, previas, esc$pct / 100)),
    stop("tipo de escenario desconocido: ", esc$tipo)
  )]
  rezago <- if (isTRUE(esc$gradual)) sample.int(CFG$rezago_gradual_max + 1L, n, TRUE) - 1L else 0L
  u[, inicio := G + rezago]
  u[, .(id, k, inicio)]
}

#' Efecto verdadero del sorteo: el mismo promedio que calcula `aggte(type = "group")`, por trimestre
#' dentro de cada cohorte y por tamaño de cohorte entre cohortes.
efecto_verdadero <- function(d) {
  por_g <- d[G > 0 & tiempo >= G, .(m = mean(delta_)), by = .(G, tiempo)][, .(t_g = mean(m)), by = G]
  tam <- d[!duplicated(id) & G > 0, .N, by = G]
  por_g[tam, on = "G"][, sum(t_g * N) / sum(N)]
}

#' Aplica el sorteo a la serie de conteos (nunca baja de cero) y vuelve a la tasa por 10 mil adultos.
inyectar <- function(d, u) {
  out <- copy(d)
  out[, `:=`(k_ = 0, inicio_ = Inf)]
  out[u, on = "id", `:=`(k_ = i.k, inicio_ = as.numeric(i.inicio))]
  nuevo <- pmax(out[[CONTEO]] + out$k_ * (out$tiempo >= out$inicio_), 0)
  tasa <- POR_ADULTOS * nuevo / out[[ADULTOS]]
  out[, delta_ := tasa - get(RESULTADO)]
  theta <- efecto_verdadero(out)
  set(out, j = RESULTADO, value = out[[RESULTADO]] + out$delta_)
  out[, c("k_", "inicio_", "delta_") := NULL]
  list(dt = out, theta = theta)
}

#' Una réplica. La semilla depende solo de `b`: el resultado no cambia con el número de núcleos y los
#' escenarios comparten las mismas fechas barajadas.
replica <- function(b, esc, base, fechas) {
  tryCatch({
    set.seed(CFG$semilla + b)
    d <- switch(fechas, reales = base, reasignadas = reasignar_fechas(base),
                todas = reasignar_todas(base), stop("fechas desconocidas: ", fechas))
    media <- media_base(d, RESULTADO)
    u <- sortear(d, esc, media)
    iny <- inyectar(d, u)
    est <- estimar(iny$dt)
    data.table(replica = b, media_base = media, municipios = sum(u$k != 0),
               sucursales = sum(abs(u$k)), theta = iny$theta, att = est$att, ee = est$ee,
               error = NA_character_)
  }, error = function(e) {
    data.table(replica = b, media_base = NA_real_, municipios = NA_integer_,
               sucursales = NA_real_, theta = NA_real_, att = NA_real_, ee = NA_real_,
               error = conditionMessage(e))
  })
}

resumir <- function(x) {
  x[, {
    ok <- is.finite(att) & is.finite(ee)
    z <- att[ok] / ee[ok]
    cota <- pmax(abs(att[ok] - Z90 * ee[ok]), abs(att[ok] + Z90 * ee[ok])) / media_base[ok] * 100
    signo <- if (pct[1] == 0) rep(TRUE, sum(ok)) else sign(att[ok]) == sign(theta[ok])
    .(replicas = .N, fallidas = sum(!ok),
      municipios_media = mean(municipios[ok]), sucursales_media = mean(sucursales[ok]),
      efecto_pct_media = mean(theta[ok] / media_base[ok] * 100),
      att_pct_media = mean(att[ok] / media_base[ok] * 100),
      att_pct_de = stats::sd(att[ok] / media_base[ok] * 100),
      ee_pct_media = mean(ee[ok] / media_base[ok] * 100),
      detecta = mean(abs(z) > Z95 & signo),
      nulo_informativo = mean(cota < UMBRAL_NULO),
      cobertura_ic95 = mean(abs(att[ok] - theta[ok]) <= Z95 * ee[ok]))
  }, by = .(fechas, escenario, tipo, pct, gradual)]
}

#' Comprueba el código antes de gastar réplicas; se detiene si algo no cuadra.
verificar <- function(tol = 1e-6) {
  base <- panel_base()
  est <- estimar(base)
  ref <- fread(file.path(RUTA_TABLAS, "tabla_final.csv"))[
    variante == "principal" & panel == "municipio_trim" & resultado == RESULTADO]
  if (nrow(ref) == 1L) {
    message(sprintf("base: ATT %.6f (tabla_final %.6f), ee %.6f (%.6f)", est$att, ref$valor, est$ee,
                    ref$ee))
    if (abs(est$att - ref$valor) > tol || abs(est$ee - ref$ee) > tol) {
      stop("sin bootstrap no se reproduce tabla_final")
    }
  } else {
    message("sin tabla_final en ", RUTA_TABLAS, ": no se compara la base")
  }
  constante <- 0.05
  d <- copy(base)
  set(d, j = RESULTADO, value = d[[RESULTADO]] + constante * (d$G > 0 & d$tiempo >= d$G))
  dif <- estimar(d)$att - est$att
  message(sprintf("constante %.3f: el ATT se mueve %.6f", constante, dif))
  if (abs(dif - constante) > tol) stop("una constante no mueve el ATT en la constante")
  set.seed(CFG$semilla)
  esc <- list(tipo = "atraccion", pct = 5)
  iny <- inyectar(base, sortear(base, esc, media_base(base, RESULTADO)))
  dif <- estimar(iny$dt)$att - est$att
  message(sprintf("sorteo: efecto %.6f, el ATT se mueve %.6f", iny$theta, dif))
  if (abs(dif - iny$theta) > tol) stop("el ATT no se mueve en el efecto sorteado")
  message("verificación completa")
  invisible(TRUE)
}

#' Mide cuánto tarda una réplica con los núcleos configurados, sin mostrar estimaciones.
medir <- function(n) {
  base <- panel_base()
  esc <- CFG$escenarios[[3]]
  for (fechas in c("reales", "reasignadas")) {
    t0 <- proc.time()[["elapsed"]]
    res <- rbindlist(parallel::mclapply(seq_len(n), replica, esc = esc, base = base,
                                        fechas = fechas, mc.cores = CFG$nucleos))
    dt_s <- proc.time()[["elapsed"]] - t0
    message(sprintf("%s: %d réplicas en %.0f s con %d núcleos (%.1f s por réplica); fallidas: %d",
                    fechas, n, dt_s, CFG$nucleos, dt_s / n, sum(!is.na(res$error))))
    if (any(!is.na(res$error))) message("error: ", res$error[!is.na(res$error)][1])
  }
  invisible(TRUE)
}

#' Baraja las fechas entre todas las unidades de cada estado, nunca tratadas incluidas.
reasignar_todas <- function(dt) {
  u <- dt[!duplicated(id), .(id, ent = substr(cve_mun, 1, 2), G)]
  u[, G_r := G[sample.int(.N)], by = ent]
  d <- copy(dt)
  d[u, on = "id", G := i.G_r]
  d
}

#' Solo los municipios que alguna vez abren, como H1(c) de la fase 4: la muestra termina antes de la
#' última cohorte, que queda como control.
solo_abren <- function(dt) {
  ultima <- max(dt[G > 0]$G)
  sub <- dt[G > 0 & tiempo < ultima]
  for (a in c("panel_nombre", "panel_id", "diseno")) setattr(sub, a, attr(dt, a))
  sub
}

#' Fechas barajadas sin efecto inyectado: lo que da el diseño cuando el calendario no significa nada.
replica_diagnostico <- function(b, muestra, barajar) {
  tryCatch({
    set.seed(CFG$semilla + b)
    d <- barajar(muestra)
    est <- estimar(d)
    data.table(replica = b, media_base = media_base(d, RESULTADO), att = est$att, ee = est$ee,
               error = NA_character_)
  }, error = function(e) {
    data.table(replica = b, media_base = NA_real_, att = NA_real_, ee = NA_real_,
               error = conditionMessage(e))
  })
}

#' Compara la estimación real con la distribución de sus fechas barajadas.
fila_diagnostico <- function(nombre, muestra, x) {
  real <- estimar(muestra)
  mb <- media_base(muestra, RESULTADO)
  x <- x[is.finite(att) & is.finite(ee)]
  z <- x$att / x$ee
  data.table(
    diseno = nombre, unidades = uniqueN(muestra$id), tratadas = uniqueN(muestra[G > 0]$id),
    replicas = nrow(x), real_pct = 100 * real$att / mb, real_ee_pct = 100 * real$ee / mb,
    centro_pct = mean(100 * x$att / x$media_base), de_pct = stats::sd(100 * x$att / x$media_base),
    ee_pct_media = mean(100 * x$ee / x$media_base),
    falsos_positivos = mean(abs(z) > Z95), fp_negativos = mean(z < -Z95), fp_positivos = mean(z > Z95),
    cobertura_ic95 = mean(abs(z) <= Z95),
    p_real_menor = mean(x$att <= real$att),
    p_randomizacion = (1 + sum(abs(x$att) >= abs(real$att))) / (1 + nrow(x))
  )
}

diagnostico <- function() {
  base <- panel_base()
  abren <- solo_abren(base)
  casos <- list(
    list(nombre = "barajadas_todas", muestra = base, barajar = reasignar_todas),
    list(nombre = "barajadas_solo_abren", muestra = abren, barajar = reasignar_fechas)
  )
  filas <- lapply(casos, function(k) {
    ruta <- sprintf("poder_diagnostico_%s_r%d", k$nombre, CFG$replicas$reasignadas)
    archivo <- file.path(RUTA_INTERMEDIOS, paste0(ruta, ".csv"))
    if (file.exists(archivo)) {
      x <- fread(archivo)
    } else {
      x <- rbindlist(parallel::mclapply(seq_len(CFG$replicas$reasignadas), replica_diagnostico,
                                        muestra = k$muestra, barajar = k$barajar,
                                        mc.cores = CFG$nucleos))
      guardar_intermedio(x, ruta)
    }
    message(sprintf("%s: %d fallidas", k$nombre, sum(!is.na(x$error))))
    fila_diagnostico(k$nombre, k$muestra, x)
  })
  # La de la corrida principal: fechas barajadas entre tratadas, con las nunca tratadas fijas.
  previa <- fread(file.path(RUTA_INTERMEDIOS,
                            sprintf("poder_reasignadas_sin_efecto_r%d.csv", CFG$replicas$reasignadas)))
  filas[[3]] <- fila_diagnostico("barajadas_entre_tratadas", base, previa)
  res <- rbindlist(filas)
  guardar_tabla(res, "poder_inyectado_diagnostico")
  print(res)
  invisible(res)
}

correr_escenario <- function(esc, base, fechas) {
  n <- CFG$replicas[[fechas]]
  nombre <- sprintf("poder_%s_%s_r%d", fechas, esc$nombre, n)
  ruta <- file.path(RUTA_INTERMEDIOS, paste0(nombre, ".csv"))
  if (file.exists(ruta)) {
    message("ya estaba: ", nombre)
    return(fread(ruta))
  }
  t0 <- proc.time()[["elapsed"]]
  res <- rbindlist(parallel::mclapply(seq_len(n), replica, esc = esc, base = base,
                                      fechas = fechas, mc.cores = CFG$nucleos))
  res[, `:=`(fechas = fechas, escenario = esc$nombre, tipo = esc$tipo, pct = esc$pct,
             gradual = isTRUE(esc$gradual))]
  guardar_intermedio(res, nombre)
  message(sprintf("%s: %.0f s, %d fallidas", nombre, proc.time()[["elapsed"]] - t0,
                  sum(!is.na(res$error))))
  res
}

poder_inyectado <- function() {
  verificar()
  base <- panel_base()
  todo <- list()
  for (fechas in c("reasignadas", "reales")) {
    for (esc in CFG$escenarios) {
      # Con las fechas reales y sin efecto todas las réplicas serían la misma estimación.
      if (fechas == "reales" && esc$tipo == "ninguno") next
      todo[[length(todo) + 1L]] <- correr_escenario(esc, base, fechas)
    }
  }
  replicas <- rbindlist(todo, fill = TRUE)
  guardar_tabla(replicas, "poder_inyectado_replicas")
  res <- resumir(replicas)
  guardar_tabla(res, "poder_inyectado_resumen")
  print(res)
  invisible(res)
}

#' Potencia con las fechas barajadas entre todas las unidades: el diagnóstico mostró que así el diseño
#' base queda calibrado, mientras que con las nunca tratadas fijas hereda el centro de esa comparación.
calibrado <- function() {
  base <- panel_base()
  elegidos <- Filter(function(e) e$nombre %in% CFG$escenarios_todas, CFG$escenarios)
  res <- resumir(rbindlist(lapply(elegidos, correr_escenario, base = base, fechas = "todas"),
                           fill = TRUE))
  guardar_tabla(res, "poder_inyectado_calibrado")
  print(res)
  invisible(res)
}

if (sys.nframe() == 0) {
  args <- commandArgs(trailingOnly = TRUE)
  accion <- if (length(args)) args[1] else "todo"
  switch(accion,
    verificar = verificar(),
    medir = medir(if (length(args) >= 2) as.integer(args[2]) else 12L),
    diagnostico = diagnostico(),
    calibrado = calibrado(),
    todo = poder_inyectado(),
    stop("uso: Rscript analisis/15_poder_inyectado.R [verificar|medir <n>|diagnostico|calibrado]")
  )
}

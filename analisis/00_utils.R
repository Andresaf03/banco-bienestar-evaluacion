# 00_utils.R — utilidades compartidas del análisis en R.
# Todos los scripts de analisis/ hacen source() de este archivo.
# Los paneles los construye Python (src/proyecto/construccion/panel.py) y se leen con arrow.

suppressPackageStartupMessages({
  library(here)
  library(arrow)
  library(data.table)
  library(yaml)
})

# Rutas ---------------------------------------------------------------------
# `PROYECTO_SALIDAS` redirige tablas, figuras e intermedios a otra carpeta: las pruebas de humo
# corren el mismo código sin pisar los resultados vigentes de outputs/.
RUTA_PARAMS  <- here("config", "parametros.yaml")
RUTA_SALIDAS <- Sys.getenv("PROYECTO_SALIDAS", here("outputs"))
RUTA_FIGURAS <- file.path(RUTA_SALIDAS, "figuras")
RUTA_TABLAS  <- file.path(RUTA_SALIDAS, "tablas")
RUTA_INTERMEDIOS <- file.path(RUTA_SALIDAS, "intermedios")
RUTA_PANELES <- here("data", "processed")

# Lectura explícita en UTF-8: si R corre en locale "C" (p. ej. Rscript sin LANG), readLines falla
# con los acentos del YAML.
leer_yaml_utf8 <- function(ruta) {
  txt <- readLines(ruta, encoding = "UTF-8", warn = FALSE)
  yaml::yaml.load(paste(enc2utf8(txt), collapse = "\n"))
}
PARAMS <- leer_yaml_utf8(RUTA_PARAMS)
# `PROYECTO_NBOOT` baja las réplicas del bootstrap en las pruebas de humo.
if (nzchar(Sys.getenv("PROYECTO_NBOOT"))) {
  PARAMS$estimacion$n_boot <- as.integer(Sys.getenv("PROYECTO_NBOOT"))
  PARAMS$estimacion$n_boot_rw <- as.integer(Sys.getenv("PROYECTO_NBOOT"))
}
set.seed(PARAMS$semillas$r)

`%||%` <- function(a, b) if (is.null(a)) b else a

# Paneles ---------------------------------------------------------------------
# Cada panel trae: identificador de unidad, índice de tiempo, G (0 = nunca tratado) y resultados.
# `per_capita` dice si los resultados del panel son tasas por habitante de la propia unidad. En el
# panel de anillos **no** lo son: el resultado es el conteo crudo dentro del radio alrededor de la
# sucursal, y la población de la columna `pobtot` es la de la localidad central, no la del disco.
# `periodicidad` distingue el DENUE semestral de la BDIF trimestral. `ventana` es el parámetro de
# `estimacion` con la ventana por defecto del diseño escalonado (NULL = todo el panel): el panel
# trimestral llega a 2025T4 pero la ventana preregistrada del bloque financiero es 2019T1–2024T4.
# `municipio_trim_largo` arranca en 2016T1 (t = 1) para la robustez con pre-periodo extendido.
PANELES <- list(
  localidad      = list(archivo = "panel_localidad.parquet",      id = "cve_loc", tiempo = "s",
                        per_capita = TRUE,  periodicidad = "semestral",
                        ventana = "ventana_semestral"),
  municipio      = list(archivo = "panel_municipio.parquet",      id = "cve_mun", tiempo = "s",
                        per_capita = TRUE,  periodicidad = "semestral",
                        ventana = "ventana_semestral"),
  anillo         = list(archivo = "panel_anillo.parquet",         id = "cve_loc", tiempo = "s",
                        per_capita = FALSE, periodicidad = "semestral"),
  municipio_trim = list(archivo = "panel_municipio_trim.parquet", id = "cve_mun", tiempo = "t",
                        per_capita = TRUE,  periodicidad = "trimestral",
                        ventana = "ventana_trimestral"),
  municipio_trim_largo = list(archivo = "panel_municipio_trim_largo.parquet", id = "cve_mun",
                              tiempo = "t", per_capita = TRUE, periodicidad = "trimestral"),
  # Censos Económicos 2004–2024 (fase 1): t = 1…5, una cohorte en el último censo.
  municipio_ce   = list(archivo = "panel_municipio_ce.parquet",   id = "cve_mun", tiempo = "t",
                        per_capita = TRUE,  periodicidad = "censal")
)

DISENOS <- c("actualizaciones", "escalonado", "completo")

#' Diseño por defecto de un panel: el DENUE usa el diseño entre actualizaciones integrales; la BDIF,
#' que sí se mide cada trimestre, el escalonado.
diseno_por_defecto <- function(nombre) {
  if (identical(PANELES[[nombre]]$periodicidad, "semestral")) {
    PARAMS$estimacion$diseno_principal
  } else {
    "escalonado"
  }
}

#' Qué unidades sin sucursal propia sirven de control (solo en el panel de localidades).
#'
#' El 91% de los "nunca tratados" estaba en un municipio que abrió una sucursal del Banco del
#' Bienestar (revisión del 2026-09-29, hallazgo C2), así que el control por defecto excluye a las
#' localidades cercanas a cualquier sucursal.
#'   distK          sin sucursal propia y a K km o más de cualquier localidad con sucursal
#'   municipal      sin sucursal propia en un municipio que no abrió ninguna en la ventana BDIF
#'   todos          cualquier localidad sin sucursal (la definición anterior, contaminada)
#'   solo_sucursal  ninguna: solo localidades con sucursal (identificación por calendario)
#' Una localidad con sucursal propia nunca es control, aunque su G sea 0: las secundarias de un
#' municipio con 2+ sucursales no tienen fecha propia y quedan con G = 0.
control_valido <- function(dt, controles) {
  sin_sucursal <- dt$n_sucursales_loc == 0
  if (grepl("^dist[0-9.]+$", controles)) {
    km <- as.numeric(sub("^dist", "", controles))
    return(sin_sucursal & is.finite(dt$dist_bb_km) & dt$dist_bb_km >= km)
  }
  switch(controles,
         municipal     = sin_sucursal & !dt$mun_con_apertura,
         todos         = sin_sucursal,
         solo_sucursal = rep(FALSE, nrow(dt)),
         stop("controles desconocidos: ", controles))
}

# Columnas que usa `leer_panel()` además del resultado: identificador, tiempo, tratamiento,
# banderas de muestra, exposición espacial, covariables y dimensiones de heterogeneidad.
COLUMNAS_BASE <- c("G", "cve_mun", "ya_tratado_inicio", "fecha_ambigua", "sospechoso_banjercito",
                   "con_actividad", "pobtot", "radio_km", "dist_bb_km", "G_vecina",
                   "mun_con_apertura", "es_cabecera", "n_sucursales_loc",
                   "grado_marginacion_2020", "desierto_bancario", "poblacion_2020",
                   "apertura_posterior_ce", "exposicion_ce")

# Paneles en memoria: cada proceso lee cada parquet del disco una sola vez. `leer_panel()` copia
# solo las columnas que necesita, así que las modificaciones por referencia no tocan la caché.
.CACHE_PANELES <- new.env(parent = emptyenv())
panel_crudo <- function(nombre) {
  if (is.null(.CACHE_PANELES[[nombre]])) {
    ruta <- file.path(RUTA_PANELES, PANELES[[nombre]]$archivo)
    if (!file.exists(ruta)) stop("No existe ", ruta, ". Construye los paneles con `make panel`.")
    .CACHE_PANELES[[nombre]] <- as.data.table(arrow::read_parquet(ruta))
  }
  .CACHE_PANELES[[nombre]]
}

#' Lee un panel y lo deja listo para `did`: id numérico, tiempo entero, G double, cluster entero.
#'
#' @param nombre  clave de PANELES
#' @param radio   solo para el panel de anillos: km del radio a conservar
#' @param diseno  "actualizaciones" (principal del DENUE): periodos de
#'   `estimacion.actualizaciones.periodos` y una sola cohorte `g` con todas las aperturas entre
#'   `g_min` y `g`; "escalonado": la ventana `ventana`; "completo": todo el panel. `NULL` usa
#'   `diseno_por_defecto()`.
#' @param controles  ver `control_valido()`. Solo aplica al panel de localidades.
#' @param derrame  si es TRUE, las "tratadas" son las localidades **sin** sucursal a menos de
#'   `radio_derrame_km` de una sucursal con fecha identificable, fechadas en la G de esa sucursal;
#'   las localidades con sucursal salen y los controles son los de `controles`.
#' @param banda  con `derrame = TRUE`, par `c(desde, hasta)` en km: solo son "tratadas" las vecinas
#'   con `desde <= dist_bb_km < hasta` (decaimiento espacial, 08_disenos_alternativos.R). `NULL` usa
#'   `c(0, radio_derrame_km)`.
#' @param regimen  solo en localidades: "recorrido_total" (cabecera o `regimen_censal.umbral_poblacion`
#'   habitantes o más: el CE las recorre manzana por manzana) o "muestra_rural" (el resto). `NULL`
#'   no filtra. Se aplica a tratadas, vecinas y controles por igual.
#' @param periodos_act  periodos del diseño entre actualizaciones (la robustez cambia el post).
#' @param excluir_ya_tratados  quita las unidades con sucursal desde el primer periodo
#' @param excluir_ambiguas     quita las localidades cuya fecha de apertura no es identificable
#' @param min_cohorte  descarta cohortes con menos unidades que este umbral: una cohorte de una
#'   o dos unidades no tiene varianza utilizable y domina los rezagos largos del event study.
#' @param min_pre  periodos previos con dato que necesita una cohorte para entrar (regla 10 de
#'   CLAUDE.md): sin ellos el "efecto" confunde el salto de cobertura de la fuente con el
#'   tratamiento.
#' @param solo_con_actividad  restringe a localidades con al menos un establecimiento en algún
#'   periodo. Es una robustez, no la especificación principal: el cero es un dato válido.
#' @param piso_poblacion  población mínima de la unidad. `panel.py` ya aplica el piso de config a
#'   **todas** las localidades, así que aquí solo tiene efecto un piso más alto (la robustez de
#'   1,000 habitantes, que aproxima el soporte común con las cabeceras tratadas). Solo se aplica a
#'   los paneles con `per_capita = TRUE`.
#' @param ventana  par `c(primero, ultimo)` de índices de tiempo para el diseño escalonado. Por
#'   defecto, la de `PANELES[[nombre]]$ventana`: entre actualizaciones del DENUE en los paneles
#'   semestrales, 2019T1–2024T4 (preregistrada) en el trimestral y todo el panel en el largo.
#' @param cluster_por  columna con la que se agrupan los errores: la fecha de tratamiento es
#'   municipal, así que por defecto `cve_mun` (en los paneles municipales coincide con la unidad).
#' @param ids  claves de unidad a conservar (muestra emparejada); `NULL` las conserva todas.
#' @param resultado  resultado(s) a estimar: se copian solo esas columnas y las de `COLUMNAS_BASE`
#'   y las covariables. `NULL` copia el panel completo (descriptivos).
leer_panel <- function(nombre, radio = NULL, diseno = NULL, resultado = NULL,
                       controles = PARAMS$estimacion$controles$principal,
                       derrame = FALSE, banda = NULL, regimen = NULL,
                       periodos_act = PARAMS$estimacion$actualizaciones$periodos,
                       excluir_ya_tratados = TRUE, excluir_ambiguas = TRUE,
                       excluir_sospechosos = TRUE,
                       min_cohorte = PARAMS$estimacion$min_cohorte, min_pre = 2L,
                       solo_con_actividad = FALSE,
                       piso_poblacion = PARAMS$unidades$localidad_pob_minima,
                       ventana = NULL, cluster_por = PARAMS$estimacion$cluster,
                       ids = NULL) {
  cfg <- PANELES[[nombre]]
  if (is.null(cfg)) stop("panel desconocido: ", nombre)
  diseno <- diseno %||% diseno_por_defecto(nombre)
  diseno <- match.arg(diseno, DISENOS)
  semestral <- identical(cfg$periodicidad, "semestral")
  if (diseno == "actualizaciones" && !semestral) {
    stop("el diseño entre actualizaciones solo aplica a los paneles del DENUE")
  }
  crudo <- panel_crudo(nombre)
  columnas <- if (is.null(resultado)) names(crudo) else {
    faltan <- setdiff(resultado, names(crudo))
    if (length(faltan)) {
      stop("el panel '", nombre, "' no tiene la columna '", paste(faltan, collapse = "', '"), "'")
    }
    intersect(unique(c(cfg$id, cfg$tiempo, COLUMNAS_BASE, PARAMS$covariables_previas, resultado)),
              names(crudo))
  }
  dt <- crudo[, ..columnas]
  if (!is.null(radio)) dt <- dt[radio_km == radio]
  if (!is.null(ids)) dt <- dt[get(cfg$id) %in% ids]
  if (excluir_ya_tratados && "ya_tratado_inicio" %in% names(dt)) {
    dt <- dt[ya_tratado_inicio == FALSE]
  }
  if (excluir_ambiguas && "fecha_ambigua" %in% names(dt)) dt <- dt[fecha_ambigua == FALSE]
  if (excluir_sospechosos && "sospechoso_banjercito" %in% names(dt)) {
    dt <- dt[sospechoso_banjercito == FALSE]
  }
  # Censos Económicos: las aperturas posteriores al año de referencia del CE 2024 están expuestas
  # solo en parte; salen de la muestra (no son tratadas ni controles limpios).
  if ("apertura_posterior_ce" %in% names(dt)) dt <- dt[apertura_posterior_ce == FALSE]
  if (solo_con_actividad && "con_actividad" %in% names(dt)) {
    dt <- dt[con_actividad == TRUE]
  }
  if (isTRUE(cfg$per_capita) && !is.null(piso_poblacion) && piso_poblacion > 0 &&
      "pobtot" %in% names(dt)) {
    dt <- dt[is.finite(pobtot) & pobtot >= piso_poblacion]
  }
  if (!is.null(regimen)) {
    if (!all(c("es_cabecera", "pobtot") %in% names(dt))) {
      stop("el panel '", nombre, "' no permite separar por régimen censal")
    }
    total <- dt$es_cabecera | dt$pobtot >= PARAMS$estimacion$regimen_censal$umbral_poblacion
    dt <- dt[total == switch(regimen, recorrido_total = TRUE, muestra_rural = FALSE,
                             stop("régimen desconocido: ", regimen))]
  }

  # Grupo de control y derrame (solo el panel de localidades trae la exposición espacial).
  if ("dist_bb_km" %in% names(dt)) {
    valido <- control_valido(dt, controles)
    if (derrame) {
      rango <- banda %||% c(0, PARAMS$estimacion$radio_derrame_km)
      # Vecina: sin sucursal propia, con la sucursal más cercana dentro del rango y fechable. (Las
      # localidades con sucursal propia y G = 0 ya salen como ambiguas; la condición lo hace
      # explícito para las variantes que las incluyen.)
      en_rango <- function(d) {
        d$G == 0 & d$n_sucursales_loc == 0 & is.finite(d$dist_bb_km) &
          d$dist_bb_km >= rango[[1]] & d$dist_bb_km < rango[[2]] & d$G_vecina > 0
      }
      dt <- dt[en_rango(dt) | (dt$G == 0 & valido)]
      dt[en_rango(dt), G := G_vecina]
    } else {
      dt <- dt[G > 0 | valido]
    }
  } else if (derrame || !identical(controles, PARAMS$estimacion$controles$principal)) {
    stop("el panel '", nombre, "' no trae la exposición espacial: controles y derrame solo ",
         "aplican al panel de localidades")
  }

  dt[, tiempo := as.integer(get(cfg$tiempo))]
  dt[, G_original := G]
  if (diseno == "actualizaciones") {
    act <- PARAMS$estimacion$actualizaciones
    dt <- dt[tiempo %in% periodos_act]
    if (identical(controles, "solo_sucursal")) {
      # Dosis: las aperturas tempranas (hasta `temprana_max`, 2022S2) contra las del último
      # semestre antes de la actualización 2024S2, que casi no alcanzan a estar expuestas. Las
      # intermedias salen.
      tardia <- act$g
      dt <- dt[G == tardia | (G >= act$g_min & G <= act$temprana_max)]
      dt[, G := fifelse(G == tardia, 0, act$g)]
    } else {
      # Todas las aperturas entre la actualización 2019S2 y el fin de la ventana forman una sola
      # cohorte: el resultado solo se vuelve a medir en la actualización 2024S2.
      dt <- dt[G == 0 | (G >= act$g_min & G <= act$g)]
      dt[G > 0, G := act$g]
    }
  } else {
    ventana <- ventana %||% if (diseno == "escalonado" && !is.null(cfg$ventana)) {
      PARAMS$estimacion[[cfg$ventana]]
    } else NULL
    if (!is.null(ventana)) dt <- dt[tiempo >= ventana[[1]] & tiempo <= ventana[[2]]]
  }
  # Aperturas posteriores al último periodo de la muestra: no están tratadas dentro de ella. `did`
  # ya las recodifica así; hacerlo aquí evita que fixest les asigne dummies de cohorte sin post.
  dt[G > max(tiempo), G := 0]
  # Regla 10: una cohorte entra solo con `min_pre` periodos previos con dato en la muestra.
  if (!is.null(min_pre) && min_pre > 0) {
    tiempos <- sort(unique(dt$tiempo))
    cohortes <- setdiff(unique(dt$G), 0)
    suficientes <- cohortes[vapply(cohortes, function(g) sum(tiempos < g) >= min_pre, logical(1))]
    dt <- dt[G == 0 | G %in% suficientes]
  }
  if (!is.null(min_cohorte)) {
    # El tamaño de cohorte se recalcula **después** de todos los filtros: el `n_cohorte` del panel
    # se computó sobre todas las unidades.
    tam <- dt[!duplicated(get(cfg$id)), .N, by = G]
    setnames(tam, "N", "n_cohorte_efectivo")
    dt <- merge(dt, tam, by = "G", all.x = TRUE)
    dt <- dt[G == 0 | n_cohorte_efectivo >= min_cohorte]
  }
  dt[, id := as.integer(factor(get(cfg$id)))]
  columna_cluster <- if (cluster_por %in% names(dt)) cluster_por else cfg$id
  if (identical(cluster_por, "cve_ent") && !"cve_ent" %in% names(dt)) {
    dt[, cve_ent := substr(get(cfg$id), 1, 2)]
    columna_cluster <- "cve_ent"
  }
  dt[, cluster := as.integer(factor(get(columna_cluster)))]
  # `did` recodifica internamente los nunca tratados como Inf, así que G debe ser double.
  dt[, G := as.numeric(G)]
  dt[, tratado := as.integer(G > 0 & tiempo >= G)]
  setorder(dt, id, tiempo)
  setattr(dt, "panel_nombre", nombre)
  setattr(dt, "panel_id", cfg$id)
  setattr(dt, "diseno", diseno)
  dt[]
}

#' Municipios **sin** cierres (P-9): los que nunca vuelven a cero sucursales del Banco del Bienestar
#' (netas de Banjército) después de su primera apertura, entre `desde` y `hasta`. Sirve para la
#' robustez que quita a los municipios con salidas temporales o definitivas (`leer_panel(ids = …)`).
municipios_sin_cierre <- function(desde = PARAMS$periodo$inicio,
                                  hasta = PARAMS$periodo$fin_trimestral) {
  sb <- as.data.table(arrow::read_parquet(here("data", "interim", "sucursales_bienestar.parquet"),
                                          col_select = c("cve_mun", "periodo", "suc_bienestar")))
  sb <- sb[periodo >= desde & periodo <= hasta]
  setorder(sb, cve_mun, periodo)
  sb[, abierto := cummax(fcoalesce(suc_bienestar, 0)) > 0, by = cve_mun]
  con_cierre <- unique(sb[abierto & fcoalesce(suc_bienestar, 0) <= 0, cve_mun])
  setdiff(unique(sb$cve_mun), con_cierre)
}

#' Filas con dato del resultado, conservando los atributos del panel (`[.data.table` los pierde).
#'
#' Si el resultado no tiene dato en algún periodo de la muestra, se detiene: un periodo sin dato
#' para todas las unidades es un cambio de cobertura de la fuente, y hay que declarar la ventana del
#' resultado en el registro de 06_correr_todo.R (regla 10 de CLAUDE.md), no dejar que el panel
#' quede desbalanceado en silencio.
con_resultado <- function(dt, resultado) {
  if (!resultado %in% names(dt)) {
    stop("el panel '", attr(dt, "panel_nombre"), "' no tiene la columna '", resultado, "'")
  }
  atributos <- attributes(dt)[c("panel_nombre", "panel_id", "diseno")]
  periodos <- uniqueN(dt$tiempo)
  out <- dt[is.finite(get(resultado))]
  if (uniqueN(out$tiempo) < periodos) {
    stop("'", resultado, "' no tiene dato en ", periodos - uniqueN(out$tiempo),
         " periodo(s) de la muestra: declara su ventana en el registro")
  }
  for (a in names(atributos)) setattr(out, a, atributos[[a]])
  out
}

#' Covariables previas disponibles en el panel (algunas solo existen en ciertos niveles).
formula_covariables <- function(dt, covs = NULL) {
  if (is.null(covs)) covs <- PARAMS$covariables_previas
  covs <- intersect(covs, names(dt))
  # Solo covariables sin faltantes: `did` no admite NA en xformla.
  covs <- covs[vapply(covs, function(c) all(is.finite(dt[[c]]) | is.character(dt[[c]])),
                      logical(1))]
  # Y solo covariables que varían en la muestra que se está estimando: al partir el panel por
  # una dimensión de heterogeneidad, la covariable que define la partición queda constante, y una
  # categórica de un solo nivel rompe `model.matrix` ("contrasts can be applied only to factors
  # with 2 or more levels"); una numérica constante es colineal con el intercepto.
  covs <- covs[vapply(covs, function(c) data.table::uniqueN(dt[[c]]) > 1L, logical(1))]
  if (length(covs) == 0) return(~1)
  as.formula(paste("~", paste(covs, collapse = " + ")))
}

# Guardado --------------------------------------------------------------------
guardar_tabla <- function(x, nombre) {
  dir.create(RUTA_TABLAS, showWarnings = FALSE, recursive = TRUE)
  data.table::fwrite(as.data.table(x), file.path(RUTA_TABLAS, paste0(nombre, ".csv")))
  invisible(file.path(RUTA_TABLAS, paste0(nombre, ".csv")))
}

guardar_intermedio <- function(x, nombre) {
  dir.create(RUTA_INTERMEDIOS, showWarnings = FALSE, recursive = TRUE)
  data.table::fwrite(as.data.table(x), file.path(RUTA_INTERMEDIOS, paste0(nombre, ".csv")))
  invisible(file.path(RUTA_INTERMEDIOS, paste0(nombre, ".csv")))
}

guardar_figura <- function(p, nombre, ancho = 9, alto = 5) {
  dir.create(RUTA_FIGURAS, showWarnings = FALSE, recursive = TRUE)
  ggplot2::ggsave(file.path(RUTA_FIGURAS, paste0(nombre, ".png")), p,
                  width = ancho, height = alto, dpi = 150)
  invisible(file.path(RUTA_FIGURAS, paste0(nombre, ".png")))
}

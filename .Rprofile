# Perfil de R del proyecto: entorno reproducible con renv.
# Solo binarios de CRAN: la compilación desde fuente está bloqueada por la licencia de Xcode
# en la máquina de desarrollo.
options(
  repos = c(CRAN = "https://cloud.r-project.org"),
  pkgType = "binary",
  install.packages.compile.from.source = "never",
  renv.config.install.build.vignettes = FALSE
)
if (Sys.getlocale("LC_CTYPE") == "C") {
  # Rscript sin LANG cae en locale C y no lee UTF-8; forzar UTF-8 si el sistema lo tiene.
  invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8")))
}
if (file.exists("renv/activate.R")) source("renv/activate.R")

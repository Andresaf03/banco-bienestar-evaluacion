#!/usr/bin/env bash
# Corrida completa desde el DENUE ya descargado hasta el reporte de resultados.
#
#   bash scripts/pipeline_completo.sh
#
# Cada paso es idempotente: si algo falla, se corrige y se vuelve a lanzar sin repetir lo hecho.
# `make` viene de Command Line Tools porque /usr/bin/make falla por la licencia de Xcode.
set -euo pipefail

MAKE=${MAKE:-/Library/Developer/CommandLineTools/usr/bin/make}
cd "$(dirname "$0")/.."

echo "== 1/6 consolidando el DENUE"
$MAKE limpiar

echo "== 2/6 tratamiento a nivel localidad"
$MAKE tratamiento

echo "== 3/6 anillos alrededor de cada centro"
$MAKE anillos

echo "== 4/6 paneles"
$MAKE panel

echo "== 5/6 estimación (paneles × bloques × estimadores)"
$MAKE estimar

echo "== 6/6 reporte"
$MAKE reporte

echo
echo "Listo. Resultados en entregables/04_final/resultados_preliminares.md"

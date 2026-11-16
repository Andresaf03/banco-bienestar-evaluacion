#!/usr/bin/env bash
# Corrida final preregistrada (docs/decisiones.md, 2026-09-29): una sola vez, de los paneles al
# reporte. Cada paso queda en outputs/logs/bateria_<fecha>.log con su duración.
#
#   bash scripts/bateria_final.sh
#
# Antes de estimar borra las tablas y figuras de **estimación** de la corrida anterior: están
# versionadas en git (recuperables con `git checkout <commit> -- outputs/`), y si se quedaran,
# 07_inferencia.R y el reporte mezclarían resultados de especificaciones que ya no existen. Las de
# `make auditar` (auditoria_*, cohortes.png) no se tocan: la batería no las regenera.
set -euo pipefail

MAKE=${MAKE:-/Library/Developer/CommandLineTools/usr/bin/make}
cd "$(dirname "$0")/.."
mkdir -p outputs/logs
LOG="outputs/logs/bateria_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

paso() {
  local nombre=$1; shift
  local inicio=$SECONDS
  echo
  echo "== $(date +%H:%M:%S) $nombre"
  "$@"
  echo "== $nombre: $((SECONDS - inicio)) s"
}

# `Rscript` reemplaza su proceso por `.../bin/exec/R --file=...`: buscar solo "Rscript" no lo ve.
if pgrep -f "bin/exec/R|Rscript" > /dev/null; then
  echo "Hay procesos de R vivos: la batería no arranca (cargarían código viejo)." >&2
  exit 1
fi

paso "0/10 pruebas y lint" $MAKE test lint
limpiar_estimacion() {
  local familias=(cs_ comp_ rob_ het_ maestra_ tabla_final inferencia_ bacon_ balance_ desc_
                  apilado_ decaimiento_ regimen_)
  for f in "${familias[@]}"; do rm -f outputs/tablas/"$f"*.csv; done
  for f in event_ het_ desc_; do rm -f outputs/figuras/"$f"*.png; done
  rm -f outputs/intermedios/*.csv
}
paso "0/10 limpia salidas de estimación anteriores" limpiar_estimacion
paso "1/10 paneles" $MAKE panel
paso "2/10 matching" $MAKE matching
paso "3/10 descriptivos" $MAKE descriptivos
paso "4/10 estimación" $MAKE estimar
paso "5/10 robustez" $MAKE robustez
paso "6/10 heterogeneidad" $MAKE heterogeneidad
paso "7/10 inferencia" $MAKE inferencia
paso "8/10 diseños alternativos" $MAKE alternativos
paso "9/10 reporte" $MAKE reporte
paso "10/10 entregables" $MAKE entregables

echo
echo "Listo en $((SECONDS / 60)) min. Registro: $LOG"

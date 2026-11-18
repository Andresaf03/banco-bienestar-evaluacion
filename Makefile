# Makefile del proyecto. Todos los objetivos corren desde la raíz del repo.
# GIT: /usr/bin/git falla en esta máquina por la licencia de Xcode; se usa el de Command Line Tools.
GIT      ?= /Library/Developer/CommandLineTools/usr/bin/git
UV       ?= uv
PY       := $(UV) run python
RSCRIPT  ?= Rscript
QUARTO   ?= quarto

FUENTES  := cnbv_bdif cnbv_portafolio denue babien inegi_mg conapo_marginacion conapo_proyecciones inegi_censo literatura inegi_ce enif banxico_remesas imss

.PHONY: help setup descargar $(addprefix descargar-,$(FUENTES)) auditar limpiar tratamiento anillos panel matching descriptivos estimar robustez heterogeneidad inferencia alternativos bateria bateria-financiera bateria-fase1 bateria-alternativos reporte entregables test lint descargar-fase2 limpiar-fase2 panel-fase2 fase2 bateria-fase2 descargar-fase3 limpiar-fase3 panel-fase3 fase3 bateria-fase3 diagnosticos descargar-fase4 limpiar-fase4 panel-fase4 fase4 bateria-fase4 presentacion-cdaii presentacion-ppii uso poder-inyectado app-datos app app-build publicar-repo descargar-fase6 limpiar-fase6 panel-fase6 descriptivos-fase6 fase6 bateria-fase6

help:
	@echo "Objetivos:"
	@echo "  setup                 crea el entorno Python (uv) y restaura el entorno R (renv)"
	@echo "  descargar             descarga todas las fuentes (idempotente; FORCE=1 para forzar)"
	@echo "  descargar-<fuente>    una fuente: $(FUENTES)"
	@echo "  limpiar               genera data/interim/*.parquet y diccionarios"
	@echo "  auditar               corre la auditoría y escribe docs/data_audit.md"
	@echo "  tratamiento           asigna sucursales a localidades y fecha las aperturas"
	@echo "  anillos               cuenta establecimientos por radio alrededor de cada centro"
	@echo "  panel                 construye los cuatro paneles en data/processed/"
	@echo "  matching              empareja tratados y controles (balance)"
	@echo "  estimar[-<bloque>]    corre la batería de estimación en R"
	@echo "  descriptivos          balance, series, medición del DENUE, régimen censal, intensidad y ENIF"
	@echo "  robustez              variantes, contraste de diseños y HonestDiD"
	@echo "  heterogeneidad        submuestras de la especificación principal"
	@echo "  inferencia            Romano–Wolf, BH, MDE, equivalencia y tabla final"
	@echo "  alternativos          DiD apilado (BDIF/IMSS) y decaimiento espacial (DENUE)"
	@echo "  bateria               la corrida completa preregistrada (scripts/bateria_final.sh)"
	@echo "  bateria-financiera    solo el bloque financiero (BDIF), fusionado en la maestra"
	@echo "  bateria-fase1         IMSS, remesas y Censos Económicos, fusionados en la maestra"
	@echo "  bateria-alternativos  intensidad municipal, diseños alternativos y reporte"
	@echo "  diagnosticos          soporte común, balance y Goodman-Bacon de la especificación financiera"
	@echo "  reporte               consolida los resultados en entregables/04_final/"
	@echo "  entregables           figuras, tablas, metodología y trabajo final (PDF), presentación"
	@echo "  descargar-fase2       fase 2: EIC/Censo, VIIRS, EFIPEM y ENOE (streaming; FORCE=1)"
	@echo "  bateria-fase2         fase 2: limpieza, paneles, estimación (analisis/10_fase2.R), reporte y entregables"
	@echo "  descargar-fase3       fase 3: INE SICEE (automática) y SESNSP (manual, solo verifica)"
	@echo "  bateria-fase3         fase 3: delitos y elecciones (analisis/11_fase3.R) y entregables"
	@echo "  descargar-fase4       fase 4: ENIGH 2016–2024 (datos abiertos del INEGI; FORCE=1)"
	@echo "  bateria-fase4         fase 4: efectos fijos, controles, derrames, bancarización, uso y ENIGH (analisis/13_fase4.R)"
	@echo "  descargar-fase6       fase 6: consolidado municipal del padrón de Bienestar (agregados; FORCE=1)"
	@echo "  bateria-fase6         fase 6: acceso, cobro local, ENIF, DENUE por sector, radios, placebos (analisis/16_fase6.R)"
	@echo "  test                  pytest"
	@echo "  lint                  ruff check + format --check"

setup:
	$(UV) sync --all-groups
	$(RSCRIPT) -e 'options(pkgType="binary"); renv::restore(prompt = FALSE)'

FORCE_FLAG := $(if $(FORCE),--force,)

descargar:
	$(PY) -m proyecto.descarga todas $(FORCE_FLAG)

$(addprefix descargar-,$(FUENTES)): descargar-%:
	$(PY) -m proyecto.descarga $* $(FORCE_FLAG)

limpiar:
	$(PY) -m proyecto.limpieza todas

auditar:
	$(PY) -m proyecto.utils.auditoria

tratamiento:
	$(PY) -m proyecto.construccion.tratamiento_localidad

anillos:
	$(PY) -m proyecto.variables.anillos

panel: tratamiento
	$(PY) -m proyecto.construccion.panel

# Emparejamiento de la especificación principal (localidad, entre actualizaciones).
PRINCIPALES := estab_emprendimiento_pc estab_consumo_pc estab_salud_pc
matching:
	for r in $(PRINCIPALES); do $(PY) -m proyecto.construccion.matching localidad $$r || exit 1; done

descriptivos:
	$(RSCRIPT) analisis/01_descriptivos.R todo
	$(PY) -m proyecto.utils.enif_descriptivo

robustez:
	$(RSCRIPT) analisis/05_robustez.R todo

heterogeneidad:
	$(RSCRIPT) analisis/04_heterogeneidad.R todo

inferencia:
	$(RSCRIPT) analisis/07_inferencia.R

# Diseños alternativos (preregistrados el 2026-10-02) y el régimen censal (exploratorio): contrastes
# de identificación que no tocan la maestra ni la tabla final.
alternativos:
	$(RSCRIPT) analisis/08_disenos_alternativos.R todo

# Solo el bloque financiero (fase 0): las especificaciones de la BDIF se reestiman y se fusionan en la
# maestra existente; el DENUE no se toca.
bateria-financiera:
	for b in financiero inclusion primera_etapa consumo; do \
	  $(RSCRIPT) analisis/06_correr_todo.R $$b municipio_trim || exit 1; done
	$(RSCRIPT) analisis/05_robustez.R financiero
	$(RSCRIPT) analisis/04_heterogeneidad.R financiero
	$(RSCRIPT) analisis/07_inferencia.R
	$(PY) -m proyecto.utils.reporte

# Fase 1: IMSS, remesas y Censos Económicos (limpieza, paneles y estimación), fusionados en la maestra.
bateria-fase1:
	$(PY) -m proyecto.limpieza imss
	$(PY) -m proyecto.construccion.panel
	for b in empleo_formal remesas; do \
	  $(RSCRIPT) analisis/06_correr_todo.R $$b municipio_trim || exit 1; done
	$(RSCRIPT) analisis/06_correr_todo.R censos_economicos municipio_ce
	$(RSCRIPT) analisis/05_robustez.R fase1
	$(RSCRIPT) analisis/04_heterogeneidad.R fase1
	$(RSCRIPT) analisis/07_inferencia.R
	$(PY) -m proyecto.utils.reporte

# Diseños alternativos y la intensidad municipal del tratamiento, con el reporte (~1–2 min).
bateria-alternativos:
	$(RSCRIPT) analisis/01_descriptivos.R intensidad
	$(RSCRIPT) analisis/08_disenos_alternativos.R todo
	$(PY) -m proyecto.utils.reporte

# Diagnósticos de la especificación financiera que promete la metodología (2026-10-12, descriptivos):
# soporte común y balance del puntaje de propensión, reestimación sin las cohortes desbalanceadas y
# Goodman-Bacon del TWFE (~15 s). `make bateria` borra sus salidas `desc_*`: volver a correrlo.
diagnosticos:
	$(RSCRIPT) analisis/12_diagnosticos.R todo

# Corrida completa preregistrada (docs/decisiones.md): paneles, matching, estimación, robustez,
# heterogeneidad, inferencia y reporte, con registro en outputs/logs/.
bateria:
	bash scripts/bateria_final.sh

# Batería completa de estimación: paneles × bloques × estimadores.
estimar:
	$(RSCRIPT) analisis/06_correr_todo.R

estimar-%:
	$(RSCRIPT) analisis/06_correr_todo.R $*

reporte:
	$(PY) -m proyecto.utils.reporte

# Entregables en Quarto (P-13): figuras y tablas desde outputs/ (sin estimar), PDF y presentación.
entregables:
	$(RSCRIPT) analisis/09_figuras_entregables.R
	$(PY) -m proyecto.utils.entregables
	cd entregables/02_metodologia && $(QUARTO) render metodologia.qmd
	cd entregables/04_final && $(QUARTO) render trabajo_final.qmd
	cd entregables/03_presentacion && $(QUARTO) render presentacion.qmd

# Presentación de Ciencia de Datos Aplicada II (.pptx para Google Slides): figuras en la paleta del
# deck y cifras desde outputs/ (sin estimar); `npm install` solo la primera vez.
presentacion-cdaii:
	$(PY) entregables/05_ciencia_datos/figuras.py
	[ -d entregables/05_ciencia_datos/node_modules ] || npm ci --prefix entregables/05_ciencia_datos
	node entregables/05_ciencia_datos/presentacion.js

# Presentación de Tópicos de Política Pública II (.pptx para Google Slides, 14 láminas + respaldo):
# reutiliza el estilo de CDA II; figuras y cifras desde outputs/ (sin estimar). El PDF de revisión se
# hace a mano con LibreOffice (entregables/06_politica_publica/README.md).
presentacion-ppii:
	$(PY) entregables/06_politica_publica/figuras.py
	[ -d entregables/06_politica_publica/node_modules ] || npm ci --prefix entregables/06_politica_publica
	node entregables/06_politica_publica/presentacion.js

# Fase 5 (exploratoria, no preregistrada): ¿se usan las cuentas del banco? Panel con la banca de
# desarrollo de la BDIF (sobre el de la fase 4) y CS en 2022T4–2025T4 (analisis/14_uso.R, ~10 s).
uso:
	$(PY) -m proyecto.construccion.panel_uso
	$(RSCRIPT) analisis/14_uso.R

# Efecto inyectado (exploratorio): sucursales privadas ficticias para medir si el DiD detecta un
# efecto chico que sí existe (analisis/15_poder_inyectado.R, ~65 min con 6 núcleos). No toca la maestra.
poder-inyectado:
	$(RSCRIPT) analisis/15_poder_inyectado.R
	$(RSCRIPT) analisis/15_poder_inyectado.R diagnostico
	$(RSCRIPT) analisis/15_poder_inyectado.R calibrado

# Aplicación web (Ciencia de Datos Aplicada II, app/): exporta resultados y panel a JSON (sin
# estimar), corre la referencia de R para validar el laboratorio y simplifica el mapa.
app-datos: uso
	$(PY) app/datos/exportar.py
	$(RSCRIPT) app/datos/referencia_cs.R
	[ -d app/node_modules ] || npm ci --prefix app
	npm run geo --prefix app

app:
	[ -d app/node_modules ] || npm ci --prefix app
	npm run dev --prefix app

app-build:
	[ -d app/node_modules ] || npm ci --prefix app
	npm test --prefix app
	npm run build --prefix app

# Foto limpia del proyecto en el repo público Andresaf03/banco-bienestar-evaluacion: sale de HEAD,
# sin CLAUDE.md ni datos, con los PDF y .pptx renderizados; se detiene si encuentra datos, secretos o
# correos. `SOLO_REVISAR=1` la arma y la revisa sin subirla (scripts/publicar_repo.sh).
publicar-repo:
	bash scripts/publicar_repo.sh

test:
	$(UV) run pytest -q

lint:
	$(UV) run ruff check src tests
	$(UV) run ruff format --check src tests

# Fase 2 (preregistro del 2026-10-07, docs/decisiones.md): fuentes nuevas fuera de la maestra, la
# tabla final y sus familias. `make bateria` borra las salidas de estimación (cs_*, rob_*, if_*):
# después de una batería completa hay que volver a correr `make bateria-fase2`.
descargar-fase2:
	$(PY) -m proyecto.descarga fase2 $(FORCE_FLAG)

limpiar-fase2:
	$(PY) -m proyecto.limpieza fase2

panel-fase2:
	$(PY) -m proyecto.construccion.panel_fase2

fase2:
	$(RSCRIPT) analisis/10_fase2.R todo

bateria-fase2: limpiar-fase2 panel-fase2 fase2 reporte entregables

# Fase 3 (preregistro del 2026-10-11, docs/decisiones.md): delitos (SESNSP) y elecciones federales
# (INE), fuera de la maestra, la tabla final y sus familias. Como con la fase 2, `make bateria`
# borra sus salidas por especificación: después de una batería completa hay que volver a correr
# `make bateria-fase3` (los paneles de delitos parten de `panel_municipio_trim*`).
descargar-fase3:
	$(PY) -m proyecto.descarga fase3 $(FORCE_FLAG)

limpiar-fase3:
	$(PY) -m proyecto.limpieza fase3

panel-fase3:
	$(PY) -m proyecto.construccion.panel_fase3

fase3:
	$(RSCRIPT) analisis/11_fase3.R todo

bateria-fase3: limpiar-fase3 panel-fase3 fase3 entregables

# Fase 4 (preregistro 2026-10-14, docs/decisiones.md; plan en docs/contexto/plan_fase4.md):
# efectos fijos, grupo de control y covariables, validez del nulo, bancarización y uso. Parte de
# `panel_municipio_trim*` y del Portafolio CNBV; fuera de la maestra, la tabla final y sus familias.
descargar-fase4:
	$(PY) -m proyecto.descarga fase4 $(FORCE_FLAG)

limpiar-fase4:
	$(PY) -m proyecto.limpieza fase4

panel-fase4:
	$(PY) -m proyecto.variables.vecinos
	$(PY) -m proyecto.variables.distancia
	$(PY) -m proyecto.construccion.panel_fase4

fase4:
	$(RSCRIPT) analisis/13_fase4.R todo

bateria-fase4: limpiar-fase4 panel-fase4 fase4 entregables

# Fase 6 (preregistro y adenda 2026-11-17, docs/decisiones.md): programas, conveniencia y el DENUE
# con más detalle. Parte de `panel_localidad` y del padrón de Bienestar; fuera de la maestra.
descargar-fase6:
	$(PY) -m proyecto.descarga fase6 $(FORCE_FLAG)

limpiar-fase6:
	$(PY) -m proyecto.limpieza fase6

panel-fase6:
	$(PY) -m proyecto.construccion.panel_fase6

descriptivos-fase6:
	$(PY) -m proyecto.variables.accesibilidad
	$(PY) -m proyecto.utils.fase6_descriptivos

fase6:
	$(RSCRIPT) analisis/16_fase6.R todo

bateria-fase6: limpiar-fase6 panel-fase6 descriptivos-fase6 fase6 entregables

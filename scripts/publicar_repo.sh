#!/usr/bin/env bash
# Publica una foto limpia del proyecto en el repositorio público, sin el historial local ni datos.
#
#   scripts/publicar_repo.sh                 # arma la foto, la revisa y la sube
#   SOLO_REVISAR=1 scripts/publicar_repo.sh  # la arma y la revisa; deja la carpeta para inspeccionar
#
# La foto sale de HEAD (solo lo versionado, así que respeta .gitignore): los cambios sin commit no
# entran. Quita los archivos privados, agrega los PDF y .pptx renderizados en entregables/renderizados/
# y hace un commit con el correo noreply de GitHub, nunca con el correo local. Si la revisión encuentra
# datos, secretos, correos personales o rutas locales, se detiene sin subir nada.
set -euo pipefail

REPO="${REPO:-Andresaf03/banco-bienestar-evaluacion}"
DESCRIPCION="¿Atrajo o desplazó? Evaluación causal del Banco del Bienestar sobre la banca privada en los municipios (ITAM, Tópicos de Política Pública II y Ciencia de Datos Aplicada II)"
PAGINA="https://andresaf03.github.io/banco-bienestar/"
TEMAS="difference-in-differences,causal-inference,financial-inclusion,mexico,public-policy,r,python"
GIT="${GIT:-/Library/Developer/CommandLineTools/usr/bin/git}"
[ -x "$GIT" ] || GIT=git
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

PRIVADOS=(CLAUDE.md REVISAR.md)
RENDERIZADOS=(
  entregables/04_final/trabajo_final.pdf
  entregables/02_metodologia/metodologia.pdf
  entregables/06_politica_publica/presentacion_ppii.pdf
  entregables/06_politica_publica/presentacion_ppii.pptx
  entregables/05_ciencia_datos/presentacion_cdaii.pdf
  entregables/05_ciencia_datos/presentacion_cdaii.pptx
)
# Correos de terceros que sí pueden aparecer (mantenedores de paquetes en los lockfiles).
EXCLUIR_CORREOS=(--exclude=renv.lock --exclude=package-lock.json)

TRABAJO="$(mktemp -d)"
FOTO="$TRABAJO/foto"
CLON="$TRABAJO/clon"
if [ "${SOLO_REVISAR:-0}" != 1 ]; then trap 'rm -rf "$TRABAJO"' EXIT; fi

if [ -z "${REF:-}" ] && ! "$GIT" -C "$RAIZ" diff --quiet HEAD; then
  echo "aviso: hay cambios sin commit; la foto usa HEAD y no los incluye" >&2
fi

# 1. Foto de HEAD sin lo privado, más los renderizados.
mkdir -p "$FOTO/entregables/renderizados"
"$GIT" -C "$RAIZ" archive "${REF:-HEAD}" | tar -x -C "$FOTO"  # REF: otro commit o árbol, para probar
for f in "${PRIVADOS[@]}"; do rm -f "$FOTO/$f"; done
for f in "${RENDERIZADOS[@]}"; do
  [ -f "$RAIZ/$f" ] || { echo "falta $f: genéralo con make antes de publicar" >&2; exit 1; }
  cp "$RAIZ/$f" "$FOTO/entregables/renderizados/"
done

# 2. Revisión: si algo aparece, no se sube.
fallas=0
reportar() { echo "REVISIÓN: $1" >&2; printf '  %s\n' "${@:2}" >&2; fallas=1; }

datos=$(cd "$FOTO" && find . -type f \( -name '*.parquet' -o -name '*.xls' -o -name '*.xlsx' \
  -o -name '*.zip' -o -name '*.gz' -o -name '*.dta' -o -name '*.sav' -o -name '*.rds' \
  -o -name '*.RData' -o -name '*.feather' -o -name '*.tif' -o -name '*.tiff' -o -name '.env*' \
  -o -name '*.pem' -o -name '*.key' -o -name 'id_rsa*' \))
[ -z "$datos" ] || reportar "datos o llaves" $datos

grandes=$(cd "$FOTO" && find . -type f -size +10M)
[ -z "$grandes" ] || reportar "archivos de más de 10 MB" $grandes

secretos=$(grep -rIlE 'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[abpr]-|-----BEGIN [A-Z ]*PRIVATE KEY-----' "$FOTO" || true)
[ -z "$secretos" ] || reportar "posibles secretos" $secretos

patron_correo='[A-Za-z0-9._%+-]+@(gmail|hotmail|outlook|yahoo|icloud|live|itam)\.(com|mx|com\.mx)'
correos=$(grep -rIlE "${EXCLUIR_CORREOS[@]}" "$patron_correo" "$FOTO" || true)
[ -z "$correos" ] || reportar "correos personales" $correos
if command -v pdftotext >/dev/null; then
  while IFS= read -r pdf; do
    if pdftotext "$pdf" - 2>/dev/null | grep -qE "$patron_correo"; then reportar "correo en PDF" "$pdf"; fi
  done < <(find "$FOTO" -name '*.pdf')
fi

rutas=$(grep -rIlE '/Users/[a-z]|/home/[a-z]' "$FOTO" || true)
[ -z "$rutas" ] || reportar "rutas locales" $rutas

if [ "$fallas" = 1 ]; then echo "no se publicó nada" >&2; exit 1; fi
echo "revisión limpia: $(find "$FOTO" -type f | wc -l | tr -d ' ') archivos, $(du -sh "$FOTO" | cut -f1)"

if [ "${SOLO_REVISAR:-0}" = 1 ]; then echo "foto en $FOTO (sin subir)"; exit 0; fi

# 3. Crear el repositorio si no existe y reemplazar su contenido por la foto.
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --description "$DESCRIPCION" --homepage "$PAGINA"
  gh repo edit "$REPO" --add-topic "$TEMAS"
fi
gh repo clone "$REPO" "$CLON" -- --quiet
if "$GIT" -C "$CLON" rev-parse -q --verify HEAD >/dev/null; then
  NUEVO=0
  "$GIT" -C "$CLON" checkout -q main
else
  NUEVO=1  # repositorio vacío: la rama aún no nace
  "$GIT" -C "$CLON" symbolic-ref HEAD refs/heads/main
fi
rsync -a --delete --exclude .git "$FOTO"/ "$CLON"/
"$GIT" -C "$CLON" add -A
"$GIT" -C "$CLON" add -f entregables/renderizados
if "$GIT" -C "$CLON" diff --cached --quiet; then echo "el repositorio público ya está al día"; exit 0; fi

USUARIO="$(gh api user --jq '"\(.id)+\(.login)"')"
NOMBRE="$("$GIT" -C "$RAIZ" config user.name)"
if [ "$NUEVO" = 1 ]; then
  MENSAJE="${MENSAJE:-feat: proyecto del Banco del Bienestar (foto del $(date +%F))}"
else
  MENSAJE="${MENSAJE:-docs: actualiza la foto del proyecto ($(date +%F))}"
fi
"$GIT" -C "$CLON" -c user.name="$NOMBRE" -c user.email="$USUARIO@users.noreply.github.com" \
  commit -q -m "$MENSAJE"
"$GIT" -C "$CLON" push -q -u origin main
echo "publicado: https://github.com/$REPO"

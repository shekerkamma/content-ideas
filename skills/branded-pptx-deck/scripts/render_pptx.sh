#!/usr/bin/env bash
# Render a .pptx to PDF (and optionally per-slide PNGs) for visual QA.
#
# This is the working substitute for preview_pptx.py on hosts without
# matplotlib. It uses LibreOffice for the render and poppler for rasterizing.
#
# Requirements, and how to get them without root:
#   - LibreOffice on the Windows side + working WSL interop
#     (if .exe fails with "Exec format error": scripts/fix-wsl-interop.sh)
#   - poppler's pdftoppm. If absent, install user-local, no root needed:
#       apt-get download poppler-utils libpoppler134
#       dpkg -x <deb> ~/.local/  ... then wrapper scripts on PATH that set
#       LD_LIBRARY_PATH to wherever libpoppler landed.
#
# Two gotchas this script exists to encapsulate:
#   1. A Windows .exe launched from WSL inherits the WSL cwd, which Windows
#      renders as a \\wsl.localhost\... UNC path and cmd.exe rejects. So we
#      always stage into a real Windows directory and cd there first.
#   2. soffice --convert-to png on a presentation exports ONLY slide 1. Use
#      PDF as the intermediate and rasterize with pdftoppm instead.
#
# Usage:
#   render_pptx.sh DECK.pptx [OUTDIR]        # PDF only
#   render_pptx.sh DECK.pptx OUTDIR --png    # PDF + per-slide PNGs
set -euo pipefail

DECK="${1:?usage: render_pptx.sh DECK.pptx [OUTDIR] [--png]}"
OUTDIR="${2:-$(dirname "$DECK")}"
WANT_PNG="${3:-}"

SOFFICE="/mnt/c/Program Files/LibreOffice/program/soffice.exe"
[[ -x "$SOFFICE" ]] || { echo "error: LibreOffice not found at $SOFFICE" >&2; exit 1; }

BASE="$(basename "${DECK%.*}")"
WINDIR="/mnt/c/Users/${USER}/AppData/Local/Temp/pptxrender"
WINPATH="C:\\Users\\${USER}\\AppData\\Local\\Temp\\pptxrender"
mkdir -p "$WINDIR" "$OUTDIR"
rm -f "$WINDIR"/*.pptx "$WINDIR"/*.pdf
cp "$DECK" "$WINDIR/"

# cd into a real Windows path so the exe does not inherit a UNC cwd
cd "$WINDIR"
timeout 480 "$SOFFICE" --headless --norestore --convert-to pdf \
  --outdir "$WINPATH" "$WINPATH\\$(basename "$DECK")" >/dev/null 2>&1 || true

PDF="$WINDIR/$BASE.pdf"
[[ -f "$PDF" ]] || { echo "error: LibreOffice produced no PDF" >&2; exit 1; }
cp "$PDF" "$OUTDIR/$BASE.pdf"
echo "wrote $OUTDIR/$BASE.pdf"

if [[ "$WANT_PNG" == "--png" ]]; then
  command -v pdftoppm >/dev/null || {
    echo "error: pdftoppm not on PATH — see header for the user-local install" >&2
    exit 1; }
  mkdir -p "$OUTDIR/contact-sheets"
  rm -f "$OUTDIR/contact-sheets"/*.png
  pdftoppm -png -r 110 "$OUTDIR/$BASE.pdf" "$OUTDIR/contact-sheets/slide"
  echo "wrote $(ls "$OUTDIR/contact-sheets"/*.png | wc -l) PNGs to $OUTDIR/contact-sheets/"
fi

echo
echo "Review the PDF directly (Read supports PDF pages), or the PNGs."
echo "Mechanical checks: qa_geometry.py $DECK"

#!/usr/bin/env bash
# install_fonts.sh — make a deck's typography real on this machine.
#
#   ./install_fonts.sh "Space Grotesk" "IBM Plex Sans" "JetBrains Mono"
#   ./install_fonts.sh --from <deck-or-chrome.css>      # read families from CSS
#   ./install_fonts.sh --check "Space Grotesk"          # report only, install nothing
#
# WHY: the hybrid export writes each box's REAL font family into the PPTX. If the
# family is not installed, three things break at once — the PNG render silently
# substitutes, OfficeCLI's render lies about what the client will see, and
# PowerPoint substitutes again on their machine. Install before rendering, and
# ship the .ttf files beside the deck.
#
# NETWORK: downloads .ttf files from the google/fonts repo only, via the GitHub
# contents API (api.github.com -> raw.githubusercontent.com). Nothing is piped to
# a shell and nothing is executed — files are written to ./fonts/ and copied to
# ~/.fonts. Offline or air-gapped? Use --check and install the families by hand.
set -uo pipefail

CHECK_ONLY=0
FAMILIES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK_ONLY=1; shift ;;
    --from)
      [ -f "${2:-}" ] || { echo "--from: no such file: ${2:-}" >&2; exit 2; }
      # pull families out of font-family declarations and @import family= params
      mapfile -t FOUND < <(grep -ohE "font-family:[^;}]*|family=[^&'\")]*" "$2" \
        | sed -E "s/font-family:|family=//" \
        | tr ',' '\n' | tr '+' ' ' \
        | sed -E "s/[\"']//g; s/:[0-9;,.@wght]*$//; s/^ +| +$//g" \
        | grep -viE "^(system-ui|sans-serif|serif|monospace|ui-monospace|-apple-system|inherit|var\(|[0-9])" \
        | grep -vE "^$" | sort -u)
      FAMILIES+=("${FOUND[@]}")
      shift 2 ;;
    *) FAMILIES+=("$1"); shift ;;
  esac
done

[ ${#FAMILIES[@]} -gt 0 ] || { echo "usage: install_fonts.sh [--check] [--from <css>] \"Family Name\"..." >&2; exit 2; }

mkdir -p ./fonts
missing=0 installed=0

for fam in "${FAMILIES[@]}"; do
  if fc-list : family 2>/dev/null | tr ',' '\n' | grep -qiFx "$fam"; then
    printf "  %-22s present\n" "$fam"; continue
  fi
  if [ "$CHECK_ONLY" = "1" ]; then
    printf "  %-22s MISSING\n" "$fam"; missing=$((missing+1)); continue
  fi

  slug=$(echo "$fam" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
  got=0
  for lic in ofl apache ufl; do
    urls=$(curl -fsSL "https://api.github.com/repos/google/fonts/contents/$lic/$slug" 2>/dev/null \
      | python3 -c "
import sys,json
try: d=json.load(sys.stdin)
except Exception: sys.exit()
for f in d if isinstance(d,list) else []:
    if f.get('name','').endswith('.ttf'): print(f['download_url'])" 2>/dev/null)
    [ -n "$urls" ] || continue
    while IFS= read -r u; do
      [ -n "$u" ] || continue
      out="./fonts/$(basename "${u%%\?*}")"
      curl -fsSL "$u" -o "$out" && got=$((got+1))
    done <<< "$urls"
    break
  done

  if [ "$got" -gt 0 ]; then
    printf "  %-22s installed (%s file/s)\n" "$fam" "$got"; installed=$((installed+1))
  else
    printf "  %-22s NOT FOUND on google/fonts — source it manually\n" "$fam"; missing=$((missing+1))
  fi
done

if [ "$installed" -gt 0 ]; then
  mkdir -p ~/.fonts && cp ./fonts/*.ttf ~/.fonts/ 2>/dev/null
  fc-cache -f >/dev/null 2>&1
  echo "  → installed to ~/.fonts and refreshed the font cache"
fi

echo "  → .ttf files kept in ./fonts/ — ship these beside the deck"
[ "$missing" -eq 0 ] || echo "  WARNING: $missing family/families unresolved; the export will substitute." >&2
exit 0

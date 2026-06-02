#!/usr/bin/env bash
# Télécharge les polices manuscrites Google Fonts utilisées par le générateur OpenScanR
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="https://github.com/google/fonts/raw/main/ofl"

declare -A FONTS=(
  # Polices variables (un seul fichier TTF)
  ["Caveat-Regular.ttf"]="caveat/Caveat%5Bwght%5D.ttf"
  ["DancingScript-Regular.ttf"]="dancingscript/DancingScript%5Bwght%5D.ttf"
  # Polices statiques
  ["PatrickHand-Regular.ttf"]="patrickhand/PatrickHand-Regular.ttf"
  ["Sacramento-Regular.ttf"]="sacramento/Sacramento-Regular.ttf"
  ["Pacifico-Regular.ttf"]="pacifico/Pacifico-Regular.ttf"
  ["IndieFlower-Regular.ttf"]="indieflower/IndieFlower-Regular.ttf"
  ["Handlee-Regular.ttf"]="handlee/Handlee-Regular.ttf"
  ["SedgwickAve-Regular.ttf"]="sedgwickave/SedgwickAve-Regular.ttf"
  # Fichier nommé sans suffixe -Regular dans le dépôt
  ["GloriaHallelujah-Regular.ttf"]="gloriahallelujah/GloriaHallelujah.ttf"
  ["CoveredByYourGrace-Regular.ttf"]="coveredbyyourgrace/CoveredByYourGrace.ttf"
)
# Polices sous licence Apache dans le dépôt Google Fonts
declare -A FONTS_APACHE=(
  ["Satisfy-Regular.ttf"]="satisfy/Satisfy-Regular.ttf"
)

echo "=== Téléchargement des polices manuscrites ==="
echo "Destination : $SCRIPT_DIR"
echo ""

ok=0
fail=0

for filename in "${!FONTS[@]}"; do
  dest="$SCRIPT_DIR/$filename"
  if [[ -f "$dest" ]]; then
    echo "  [OK déjà présent] $filename"
    (( ok++ )) || true
    continue
  fi
  url="$BASE_URL/${FONTS[$filename]}"
  if curl -fsSL "$url" -o "$dest"; then
    echo "  [téléchargé] $filename"
    (( ok++ )) || true
  else
    echo "  [ERREUR]     $filename  ($url)"
    (( fail++ )) || true
  fi
done

BASE_APACHE="https://github.com/google/fonts/raw/main/apache"
for filename in "${!FONTS_APACHE[@]}"; do
  dest="$SCRIPT_DIR/$filename"
  if [[ -f "$dest" ]]; then
    echo "  [OK déjà présent] $filename"
    (( ok++ )) || true
    continue
  fi
  url="$BASE_APACHE/${FONTS_APACHE[$filename]}"
  if curl -fsSL "$url" -o "$dest"; then
    echo "  [téléchargé] $filename"
    (( ok++ )) || true
  else
    echo "  [ERREUR]     $filename  ($url)"
    (( fail++ )) || true
  fi
done

echo ""
echo "=== Résultat : $ok police(s) OK, $fail erreur(s) ==="

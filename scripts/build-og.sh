#!/usr/bin/env bash
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT/scripts/og-bio.html"
OUTPUT="$ROOT/assets/og-bio.png"

[ -x "$CHROME" ] || { echo "Chrome not found: $CHROME"; exit 1; }

"$CHROME" --headless=new --disable-gpu --no-sandbox \
    --window-size=1200,630 --hide-scrollbars --virtual-time-budget=3000 \
    --screenshot="$OUTPUT" "file://$TEMPLATE"

echo "Built $OUTPUT"

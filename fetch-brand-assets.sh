#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# IQ Homes — pull the brand creatives out of Bloom into this site.
# Run once from the site folder:   bash fetch-brand-assets.sh
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/img/photos assets/img/ads

echo "Fetching IQ Homes brand creatives…"

get () { curl -fsSL -o "$2" "$1" && echo "  ✓ $2" || echo "  ✗ $2 (failed — grab it manually from trybloom.ai)"; }

# Photoreal base creatives — used across the site
get "https://www.trybloom.ai/img/afa5d031-c600-4014-963b-908fee0e1499" "assets/img/photos/hero-dusk-unlock.jpg"
get "https://www.trybloom.ai/img/d48e7ee3-9489-439c-b3c7-4f2d4383cb0f" "assets/img/photos/app-control-phone.jpg"
get "https://www.trybloom.ai/img/a8527e66-6c5b-41dd-9bba-7cfe0b0a028c" "assets/img/photos/doorbell-night.jpg"
get "https://www.trybloom.ai/img/c6a6fe1a-09dd-48c0-9df4-1b312c9e1dda" "assets/img/photos/gta-street-daytime.jpg"

# Finished ad posters — shown in the gallery
get "https://www.trybloom.ai/img/f1073616-4655-4e64-84ef-0fcb6640c7d9" "assets/img/ads/ad-come-home-to-smarter.jpg"
get "https://www.trybloom.ai/img/08a20635-9b69-41fb-b16d-157071e4e117" "assets/img/ads/ad-one-app-every-room.jpg"
get "https://www.trybloom.ai/img/30792d25-78b8-48ac-ba35-58721710db5d" "assets/img/ads/ad-24-7-eyes.jpg"
get "https://www.trybloom.ai/img/629474ea-b9b2-4cce-ab21-5b77b366ae12" "assets/img/ads/ad-trusted-across-gta.jpg"

echo
echo "Done. Reload the site — the placeholders will be gone."

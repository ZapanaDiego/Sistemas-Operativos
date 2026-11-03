#!/usr/bin/env bash
# Verifica que dos ejecuciones del mismo escenario producen trazas idénticas.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p out

./entornoRTOS --scenario s1 --out out/.det_a.txt >/dev/null
cp out/s1_data.js out/.det_a.js

./entornoRTOS --scenario s1 --out out/.det_b.txt >/dev/null

cmp out/.det_a.txt out/.det_b.txt
cmp out/.det_a.js out/s1_data.js

rm -f out/.det_a.txt out/.det_b.txt out/.det_a.js
echo "determinism: PASS"

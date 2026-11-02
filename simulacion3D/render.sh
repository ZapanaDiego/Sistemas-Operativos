#!/usr/bin/env bash
# Render del film por planos.
#
# Uso:
#   ./render.sh build                 # construye y guarda el .blend
#   ./render.sh test                  # frame de prueba 1080p
#   ./render.sh draft                 # frame de prueba 720p
#   ./render.sh shot 03 1 312         # renderiza la escena shot_03
#
# El render por planos requiere que build_scene.py cree las escenas
# shot_01 ... shot_15. Mientras tanto, `build` y `test` funcionan.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLEND="$ROOT/blender/pathfinder_failure.blend"

usage() {
    sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
}

case "${1:-}" in
    build)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- --save
        ;;
    test)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- --test-frame
        ;;
    draft)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- --test-frame --draft
        ;;
    shot)
        shot="${2:?falta el número de plano}"
        start="${3:-1}"
        end="${4:-1}"
        blender -b "$BLEND" -S "shot_${shot}" -s "$start" -e "$end" -a
        ;;
    *)
        usage
        ;;
esac

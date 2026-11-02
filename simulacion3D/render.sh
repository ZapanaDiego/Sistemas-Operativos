#!/usr/bin/env bash
# Render del film y del animatic.
#
# Uso:
#   ./render.sh build                 # construye y guarda el .blend final
#   ./render.sh test                  # frame de prueba 1080p
#   ./render.sh preview               # previews de frontera a 480p
#   ./render.sh film                  # renderiza los 4320 frames
#   ./render.sh encode                # codifica el MP4 con fade
#   ./render.sh animatic              # renderiza el animatic de 18 s
#
# El render por planos individuales sigue disponible:
#   ./render.sh shot 03 1 312

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLEND="$ROOT/blender/pathfinder_failure.blend"
ANIM_BLEND="$ROOT/blender/animatic.blend"

usage() {
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
}

case "${1:-}" in
    build)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- \
            --save --samples 8 --no-motion-blur
        ;;
    test)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- \
            --test-frame --frame "${2:-1}" --samples 8 --no-motion-blur
        ;;
    preview)
        blender -b --factory-startup --python "$ROOT/build_scene.py" -- --preview
        ;;
    film)
        blender -b "$BLEND" -a
        ;;
    encode)
        ffmpeg -y -framerate 24 -i "$ROOT/out/frames/film/frame_%04d.png" \
            -vf "fade=t=in:st=0:d=1,fade=t=out:st=178:d=2" \
            -c:v libx264 -pix_fmt yuv420p -crf 18 \
            "$ROOT/out/pathfinder_failure.mp4"
        ;;
    animatic)
        blender -b --factory-startup --python "$ROOT/animatic.py" -- \
            --save --render --samples 8
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

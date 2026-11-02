# simulacion3D — Film del fallo de Mars Pathfinder

Documental 3D mudo sobre la inversión de prioridades no acotada en el RTOS del
lander Mars Pathfinder. El contrato de producción vive en `AGENTS.md`; la
secuencia canónica de 15 planos está en §4 de ese documento.

> **Estado:** film renderizado, codificado y verificado. El entregable es
> `out/pathfinder_failure.mp4`.

> **Aviso de honestidad:** el film es una reconstrucción visual del mecanismo,
> no una emulación de VxWorks. El código y la terminal de los planos 11–12
> provienen de `../entornoRTOS/`; no se inventan líneas ni salidas.

## Entregable

| Propiedad | Valor |
| :--- | :--- |
| Archivo | `out/pathfinder_failure.mp4` |
| Resolución | 1920 × 1080 |
| Frecuencia | 24 fps |
| Duración | 180,0 s (3:00) |
| Códec | H.264 High, yuv420p |
| Audio | Ninguno |
| Tamaño | 32.256.132 bytes (~30,8 MiB) |
| Verificación | `ffprobe` + decodificación completa sin errores |

## Requisitos

- Blender 5.2.3 LTS (EEVEE).
- ffmpeg 9.0.2 para la codificación.
- Python 3 con Pillow (probado con 13.0.0) para las texturas.
- DejaVu Sans Mono, incluida en `assets/fonts/`.

## Comandos

```bash
# Construir y guardar el .blend base
blender -b --factory-startup --python build_scene.py -- --save

# Frame de prueba 1080p (32 muestras)
blender -b --factory-startup --python build_scene.py -- --test-frame

# Frame de prueba 720p (16 muestras)
blender -b --factory-startup --python build_scene.py -- --test-frame --draft

# Animatic de 18 s (432 frames, 720p, 8 muestras)
blender -b --factory-startup --python animatic.py -- --save
blender -b --factory-startup --python animatic.py -- --test-frame --frame 288
blender -b --factory-startup --python animatic.py -- --render --samples 8

# Escena final: construir, guardar y renderizar 4320 frames
blender -b --factory-startup --python build_scene.py -- --save --samples 8 --no-motion-blur
blender -b blender/pathfinder_failure.blend -a

# Codificar el MP4 final con fade de entrada y salida
ffmpeg -framerate 24 -i out/frames/film/frame_%04d.png \
  -vf "fade=t=in:st=0:d=1,fade=t=out:st=178:d=2" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 out/pathfinder_failure.mp4

# Regenerar las texturas de código y terminal desde el demo real
python3 assets/code/make_textures.py
```

También se puede usar `./render.sh build`, `./render.sh test` y
`./render.sh draft`.

## Medición de render (I0)

Escena de prueba con terreno, marcadores emisivos, cerrojo y cámara. No es la
escena final; sirve para dimensionar el presupuesto de render.

| Configuración | Muestras | Tiempo por frame |
| :--- | :---: | :---: |
| Escena de prueba 1920 × 1080, primera ejecución | 32 | 7,64 s |
| Escena de prueba 1920 × 1080, con caché | 32 | 3,35 s |
| Escena de prueba 1280 × 720 | 16 | 1,24 s |
| Animatic 1280 × 720 | 8 | ~0,44 s |
| Escena final 1920 × 1080, sin motion blur | 8 | ~0,85 s |

El render final de 4320 frames tardó **59:42** (0,85 s/frame). El animatic de
432 frames tardó ~5 min y produjo un MP4 de 18,0 s. La codificación final
tardó ~68 s.

## Estructura

```
simulacion3D/
├── AGENTS.md
├── README.md
├── STORYBOARD.md
├── NARRACION.md
├── build_scene.py
├── animatic.py
├── render.sh
├── modules/
│   ├── cameras.py
│   ├── lander.py
│   ├── materials.py
│   ├── render.py
│   ├── rover.py
│   ├── tasks.py
│   └── terrain.py
├── assets/
│   ├── code/          # generador y texturas reales
│   ├── fonts/         # DejaVu Sans Mono
│   └── textures/
├── blender/           # pathfinder_failure.blend, animatic.blend
└── out/
    ├── frames/        # shot_01 ... shot_15
    ├── spike/         # frames de prueba
    ├── animatic/      # frames del animatic (ignorados)
    ├── animatic.mp4   # animatic de revisión
    └── pathfinder_failure.mp4  # entregable final
```

## Animatic

El animatic valida el lenguaje visual antes de modelar en detalle: terreno,
silueta del lander, rover de contexto, acercamiento de cámara y ciudad de
tareas con cerrojo. Dura 18 s (432 frames), se renderiza a 1280 × 720 con 8
muestras y se codifica en `out/animatic.mp4`. No es la escena final.

## Documentos de producción

- `AGENTS.md`: contrato local y secuencia canónica.
- `STORYBOARD.md`: 15 planos con tiempos, frames, cámara, FX y fuentes.
- `NARRACION.md`: guion en vivo de 387 palabras, alineado con los planos.

## Próximo hito

Construir el animatic de 15–20 s y validar el lenguaje visual con una persona
externa.

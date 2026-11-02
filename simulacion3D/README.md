# simulacion3D — Film del fallo de Mars Pathfinder

Documental 3D mudo sobre la inversión de prioridades no acotada en el RTOS del
lander Mars Pathfinder. El contrato de producción vive en `AGENTS.md`; la
secuencia canónica de 15 planos está en §4 de ese documento.

> **Estado:** iteración I0 completada. Existe la base técnica (escena de prueba,
> texturas reales y medición de render), pero todavía no hay storyboard,
> animatic ni planos animados.

> **Aviso de honestidad:** el film es una reconstrucción visual del mecanismo,
> no una emulación de VxWorks. El código y la terminal de los planos 11–12
> provienen de `../entornoRTOS/`; no se inventan líneas ni salidas.

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
| 1920 × 1080, EEVEE, primera ejecución | 32 | 7,64 s |
| 1920 × 1080, EEVEE, ejecución con caché | 32 | 3,35 s |
| 1280 × 720, EEVEE | 16 | 1,24 s |

Con 4320 frames, el render final a 1080p queda entre ~4 h y ~9 h según la
caché y la complejidad de la escena. El draft a 720p es del orden de 1,5 h.
La medición se repetirá con la escena completa antes del render final.

## Estructura

```
simulacion3D/
├── AGENTS.md
├── README.md
├── build_scene.py
├── render.sh
├── modules/
│   ├── cameras.py
│   ├── materials.py
│   └── render.py
├── assets/
│   ├── code/          # generador y texturas reales
│   ├── fonts/         # DejaVu Sans Mono
│   └── textures/
├── blender/           # pathfinder_failure.blend
└── out/
    ├── frames/        # shot_01 ... shot_15
    └── spike/         # frames de prueba
```

## Próximo hito

Escribir `STORYBOARD.md` y `NARRACION.md`, y construir el animatic de 15–20 s.

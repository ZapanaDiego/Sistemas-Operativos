# AGENTS.md — Simulación 3D del fallo de Mars Pathfinder

> **Estado:** vivo. Leer al iniciar. Actualizar al cerrar cada turno.
> **Última actualización:** 2026-11-02 · OpenCode (DeepSeek V4.1 Flash)
> **Documento maestro del repositorio:** `../AGENTS.md`.
> Este archivo es el contrato local de `simulacion3D/`.

## 0. Regla de actualización (R0 local)

Todo agente que cree, modifique, mueva o elimine un archivo en `simulacion3D/` debe:

1. Actualizar la bitácora §9.
2. Actualizar el inventario §8.
3. Ajustar los checkboxes §10.
4. Actualizar el estado §1.
5. Actualizar `../AGENTS.md` (§8.3 bitácora y §8.4 inventario), porque el repositorio es la fuente de verdad global.

Si el disco contradice este documento, prevalece el disco y se corrige el documento.

## 1. Estado actual

- **Fase:** preproducción.
- **Entregable único:** `out/pathfinder_failure.mp4`.
- **Próximo hito:** `STORYBOARD.md` + animatic de 15–20 s.
- **Bloqueos:** ninguno.
- **Riesgo principal:** tiempo de render y claridad del film sin texto.
- **Alcance:** solo el film. El artículo, el motor S0–S5 y el demo C viven fuera de este directorio.

## 2. Objetivo y alcance

### 2.1. Objetivo

Producir un documental 3D mudo de 2:45–3:00 que muestre, paso a paso, la inversión de prioridades no acotada en el RTOS VxWorks del lander Mars Pathfinder, su manifestación en el ciclo 1553, el reset del watchdog y la corrección con herencia de prioridad.

### 2.2. Entregable

- `out/pathfinder_failure.mp4`: 1920 × 1080, 24 fps, H.264, 2:45–3:00.
- Sin audio.
- Sin texto en pantalla, salvo el código y la terminal de los planos 11–12.
- La narración es en vivo, para la exposición.

### 2.3. Incluye

- Ares Vallis, lander y rover como contexto visual.
- Sensores/instrumento ASI/MET, cámara y tareas medias.
- Disección del ordenador de vuelo del lander: VME, CPU, bus 1553.
- Ciudad de tareas, mutex de `select()`, prioridades, deadline y watchdog.
- Transición al código y a la terminal del demo C.
- Corrección con PIP on.

### 2.4. No incluye

- El rover como objeto del fallo.
- Emulación bit a bit de VxWorks.
- Física de aterrizaje, protocolo 1553 detallado, caché/pipeline.
- Artículo, slides, corpus o demo C: viven fuera de este directorio.
- Audio o voice-over.

## 3. Hechos y fuentes

| Hecho | Fuente |
| :--- | :--- |
| Aterrizaje: 4/7/1997; rover en superficie: 6/7/1997 | NASA / NSSDC |
| Fallo en el ordenador de vuelo del lander, no en el rover | Reeves 1997 |
| `bc_sched` es la tarea de mayor prioridad (salvo `tExec`) | Reeves 1997 |
| `bc_dist` es la tercera prioridad | Reeves 1997 |
| `ASI/MET` es la tarea de menor prioridad | Reeves 1997 |
| Ciclo del bus 1553: 8 Hz = 125 ms | Reeves 1997 |
| El mutex interno de `select()` no tenía herencia de prioridad | Reeves 1997/1999 |
| Las tareas medias expropian a `ASI/MET` y bloquean a `bc_dist` | Reeves 1997 |
| El watchdog detecta el plazo incumplido y reinicia | Reeves 1997 |
| Corrección: `semMCreate(SEM_Q_PRIORITY \| SEM_INVERSION_SAFE)` | Reeves 1999 |
| Sin pérdida de datos si se mantiene la alimentación | Reeves 1997 |

**Reglas de integridad**

1. No atribuir el fallo a Sojourner.
2. No decir "el RTOS se cayó": VxWorks funcionó como estaba configurado.
3. No decir "pérdida de datos" sin matizar.
4. No presentar el film como emulación de VxWorks.
5. Las metáforas visuales (ciudad de tareas, cerrojo, anillos) son licencia artística declarada, no hardware real.

## 4. Storyboard: 15 planos, 2:45–3:00

| # | Tiempo | Plano | Qué se ve | Fuente |
| :---: | :--- | :--- | :--- | :--- |
| 1 | 0:00–0:12 | Ares Vallis | Vista aérea, polvo, lander y rover; amanecer | NASA |
| 2 | 0:12–0:25 | ASI/MET | Mástil, sensores, primeros pulsos de datos | Reeves, software |
| 3 | 0:25–0:38 | Disección | Carcasa transparente; chasis VME | Reeves, hardware |
| 4 | 0:38–0:52 | CPU y 1553 | Placas, bus, paquetes hacia el CPU | Reeves, hardware |
| 5 | 0:52–1:05 | Ciudad de tareas | Hilos verticales, prioridades como alturas | Reeves + modelo |
| 6 | 1:05–1:18 | El cerrojo | `ASI/MET` toma el mutex de `select()` | Reeves, "THE FAILURE" |
| 7 | 1:18–1:32 | Expropiación | Tareas medias empujan a `ASI/MET`; el cerrojo sigue tomado | Reeves, "THE FAILURE" |
| 8 | 1:32–1:45 | Bloqueo | `bc_dist` llega al cerrojo y se detiene | Reeves, "THE FAILURE" |
| 9 | 1:45–1:58 | Deadline | Anillo se llena; bus stutter; cámara lenta | Reeves, "THE FAILURE" |
| 10 | 1:58–2:08 | Watchdog | Anillo rojo, flash, reset; montaje de reinicios | Reeves, "THE FAILURE" |
| 11 | 2:08–2:20 | Código | Editor con `select()`, `pipe()`, `semMCreate` | Reeves 1999 |
| 12 | 2:20–2:30 | Terminal | `make run-pip-off` → `WATCHDOG: RESET` | Demo C |
| 13 | 2:30–2:40 | Corrección | PIP on; `ASI/MET` hereda prioridad | Reeves, corrección |
| 14 | 2:40–2:50 | Ciclo verde | `bc_dist` termina; bus fluye; sin reset | Reeves, corrección |
| 15 | 2:50–3:00 | Cierre | Pullback al lander y al rover | Síntesis |

## 5. Lenguaje visual

- **Sin texto** salvo el código/terminal de los planos 11–12.
- **Sin audio.** La narración va en `NARRACION.md` para la exposición.
- **Colores:** `bc_sched` blanco, `bc_dist` rojo, tareas medias naranja,
  `ASI/MET` azul, mutex ámbar, deadline rojo, watchdog blanco/rojo, PIP verde.
- **Formas:** cerrojo = toro/cilindro; deadline = anillo; watchdog = anillo
  pulsante; bus 1553 = autopista luminosa.
- **Cámara:** 24 fps, movimientos lentos, cortes en el pulso del bus.
- **El rover** es un guía visual, no la víctima del fallo.

## 6. Arquitectura técnica

- **Blender 5.2.3 LTS**, motor **EEVEE**, 1920 × 1080, 24 fps.
- Construcción procedural con Python (`build_scene.py` + `modules/`).
- Render a PNG y codificación con `ffmpeg` (libx264).
- Sin assets externos obligatorios; NASA es de dominio público si se usa.
- Semilla fija y escena reproducible.
- `assets/code/` se genera desde la salida real de `../demo/`; no se inventa.

```
simulacion3D/
├── AGENTS.md
├── STORYBOARD.md
├── NARRACION.md
├── README.md
├── build_scene.py
├── render.sh
├── modules/
│   ├── terrain.py
│   ├── lander.py
│   ├── rover.py
│   ├── tasks.py
│   ├── cameras.py
│   ├── materials.py
│   └── render.py
├── blender/
│   └── pathfinder_failure.blend
├── assets/
│   ├── textures/
│   ├── code/
│   └── fonts/
└── out/
    ├── frames/
    └── pathfinder_failure.mp4
```

## 7. Pipeline

```bash
# Construir y guardar el .blend
blender -b --factory-startup --python build_scene.py -- --save

# Frame de prueba (medir tiempo y confirmar EEVEE headless)
blender -b blender/pathfinder_failure.blend -f 1

# Render completo
blender -b blender/pathfinder_failure.blend -a

# Codificar
ffmpeg -framerate 24 -i out/frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 out/pathfinder_failure.mp4

# Verificar
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  out/pathfinder_failure.mp4
```

**Fallback:** si EEVEE falla headless, usar Workbench; si el tiempo es excesivo,
720p y reescalado. Documentar el tiempo por frame.

## 8. Inventario

| Ruta | Tipo | Propósito | Estado |
| :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento | Contrato local | Activo |
| `STORYBOARD.md` | Documento | 15 planos y fuentes | Pendiente |
| `NARRACION.md` | Documento | Guion en vivo | Pendiente |
| `README.md` | Documento | Build y render | Pendiente |
| `build_scene.py` | Python | Construcción de escena | Pendiente |
| `modules/` | Python | Terreno, lander, rover, tareas, cámaras | Pendiente |
| `blender/` | Blender | Proyecto editable | Pendiente |
| `assets/code/` | Imágenes | Código/terminal reales | Pendiente |
| `out/frames/` | PNG | Secuencia de render | Pendiente |
| `out/pathfinder_failure.mp4` | Video | Entregable final | Pendiente |

## 9. Bitácora

| Fecha | Agente | Archivos | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Creación del contrato local de `simulacion3D/` con alcance, storyboard, pipeline y R0. | Archivo creado; `ls -la simulacion3D`. |

## 10. Checklist

- [x] Crear `simulacion3D/AGENTS.md`.
- [ ] Escribir `STORYBOARD.md`.
- [ ] Escribir `NARRACION.md`.
- [ ] Construir animatic de 15–20 s.
- [ ] Modelar terreno, lander, rover y ciudad de tareas.
- [ ] Animar los 15 planos.
- [ ] Generar texturas de código/terminal desde `../demo/`.
- [ ] Render de prueba y medición de tiempo.
- [ ] Draft 720p.
- [ ] Render final 1080p.
- [ ] Codificar y verificar el MP4.
- [ ] Actualizar `../AGENTS.md` (§8.1, §8.3, §8.4).
- [ ] Commit.

## 11. Criterios de aceptación

1. MP4 1920 × 1080, 24 fps, 2:45–3:00, H.264, sin audio.
2. La cadena causal se entiende sin texto: sensores → `ASI/MET` → mutex →
   tareas medias → `bc_dist` bloqueado → watchdog → reset.
3. Con PIP on, la misma cadena termina en ciclo verde.
4. El código y la terminal muestran la salida real del demo C.
5. No hay afirmaciones factuales sin fuente en `STORYBOARD.md`.
6. El film se reconstruye con un comando y una semilla fija.
7. El tiempo de render está documentado.

## 12. Riesgos

| Riesgo | Mitigación |
| :--- | :--- |
| Render lento | Frame de prueba; 720p; Workbench; render nocturno |
| EEVEE headless falla | Workbench o Cycles CPU |
| Película muda confusa | Narración en vivo; prueba con alguien externo |
| Deriva factual | Storyboard con fuente por plano |
| Scope creep | Congelar features el 22/11 |
| Disco lleno | Render por secuencias; borrar frames intermedios |

## 13. Protocolo para agentes

1. Leer este archivo y `../AGENTS.md` antes de tocar nada.
2. No modificar `../main.tex`, `../references.bib`, `../fuentes/` ni `../demo/`
   salvo que la tarea lo requiera.
3. No añadir audio ni texto no previsto.
4. Usar semilla fija y rutas relativas.
5. Actualizar §8, §9 y §10 al cerrar cada turno.
6. Actualizar `../AGENTS.md` (§8.3 y §8.4) porque es la fuente global.
7. Si el disco contradice este documento, prevalece el disco.

## 14. Primeros pasos

1. Escribir `STORYBOARD.md` con los 15 planos, tiempos y fuentes.
2. Escribir `NARRACION.md` con el guion en vivo.
3. Construir un animatic de 15–20 s: terreno, silueta del lander, cámara que
   se acerca, ciudad de tareas y cerrojo.
4. Renderizar a 720p con pocas muestras y revisar el lenguaje visual.
5. Solo después, modelar el lander en detalle.

# STORYBOARD — Mars Pathfinder: la inversión de prioridades

> **Documento derivado.** Este storyboard es una copia imprimible de
> `AGENTS.md` §4.2–§4.3. No es una fuente paralela: cualquier cambio de
> secuencia, tiempo, fuente o criterio se backporta primero a §4.
>
> **Versión:** I1 · 2026-11-02
> **Formato:** 1920 × 1080, 24 fps, 4320 frames, 3:00, sin audio.
> **Regla de texto:** solo código y terminal en los planos 11–12. Nada de
> títulos, etiquetas, subtítulos ni créditos dentro del film.
> **Construcción:** `build_scene.py` + `modules/`, semilla fija, EEVEE.

## 1. Resumen de planos

| # | Entrada | Salida | Dur. | Frames | Título | Acto | Fuente |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| 1 | 0:00 | 0:12 | 12 s | 1–288 | Ares Vallis | I | NASA |
| 2 | 0:12 | 0:25 | 13 s | 289–600 | ASI/MET | I | Reeves |
| 3 | 0:25 | 0:38 | 13 s | 601–912 | Disección | II | Reeves |
| 4 | 0:38 | 0:52 | 14 s | 913–1248 | CPU y 1553 | II | Reeves |
| 5 | 0:52 | 1:05 | 13 s | 1249–1560 | Ciudad de tareas | II | Reeves + modelo |
| 6 | 1:05 | 1:18 | 13 s | 1561–1872 | El cerrojo | III | Reeves |
| 7 | 1:18 | 1:32 | 14 s | 1873–2208 | Expropiación | III | Reeves |
| 8 | 1:32 | 1:45 | 13 s | 2209–2520 | Bloqueo | III | Reeves |
| 9 | 1:45 | 1:58 | 13 s | 2521–2832 | Deadline | III | Reeves |
| 10 | 1:58 | 2:08 | 10 s | 2833–3072 | Watchdog | III | Reeves |
| 11 | 2:08 | 2:20 | 12 s | 3073–3360 | Código | IV | Reeves 1999 + demo |
| 12 | 2:20 | 2:30 | 10 s | 3361–3600 | Terminal | IV | Demo C |
| 13 | 2:30 | 2:40 | 10 s | 3601–3840 | Corrección | V | Reeves |
| 14 | 2:40 | 2:50 | 10 s | 3841–4080 | Ciclo verde | V | Reeves |
| 15 | 2:50 | 3:00 | 10 s | 4081–4320 | Cierre | V | Síntesis |

**Total:** 180 s = 4320 frames. Los rangos son inclusivos y usan frames
1-based, como Blender.

## 2. Código de color y formas

| Elemento | Color | Hex | Uso |
| :--- | :--- | :--- | :--- |
| `bc_sched` | Blanco | `#FFFFFF` | watchdog y prioridad 1 |
| `bc_dist` | Rojo | `#FF3B30` | tarea bloqueada |
| Tareas medias | Naranja | `#FF9500` | expropiación |
| `ASI/MET` | Azul | `#0A84FF` | prioridad 7 y `select()` |
| Mutex | Ámbar | `#FFB300` | cerrojo |
| Deadline | Rojo → verde | `#FF3B30` → `#34C759` | estado del plazo |
| PIP on | Verde | `#34C759` | herencia |
| Marte | Ocre | `#8B3A1E`, `#C1440E`, `#E27D60` | terreno y cielo |
| Metal | Gris | `#B0B0B0` | lander y rover |

Formas: cerrojo = toro con ojo central; deadline = anillo que se llena;
watchdog = anillo blanco en la cima; bus 1553 = autopista luminosa; ciudad de
tareas = hilos verticales cuya altura es la prioridad.

## 3. Planos

### Plano 1 — Ares Vallis (0:00–0:12)

- **Frames:** 1–288 (288).
- **Acto:** I.
- **Objetivo:** establecer Marte, el lander y el rover como contexto.
- **Visual:** llanura rojiza, rocas dispersas, colinas al fondo; lander a la
  izquierda con paneles y mástil; rover como punto metálico que avanza; polvo
  en suspensión; sol bajo.
- **Cámara:** 24 mm, grúa lenta de izquierda a derecha, 1,5 m sobre el suelo,
  ligera inclinación hacia abajo; parallax con las rocas; termina en el mástil
  contra el sol.
- **Acción:** el polvo se desplaza; el rover recorre una curva; la antena
  destella.
- **FX:** polvo volumétrico, heat shimmer, lens flare sutil.
- **Transición:** corte al mástil ASI/MET.
- **Assets:** `ENV_Terrain`, `ENV_Rocks`, `ENV_Sky`, `LANDER`, `ROVER`.
- **Fuente:** NASA.
- **Aceptación:** Marte, lander y rover reconocibles; cero texto.
- **Narración:** N1, 0:00–0:12.

### Plano 2 — ASI/MET (0:12–0:25)

- **Frames:** 289–600 (312).
- **Acto:** I.
- **Objetivo:** mostrar los sensores que alimentan el sistema e introducir el
  flujo de datos.
- **Visual:** macro del mástil ASI/MET; sensores de viento, temperatura y
  presión; pulsos azules bajan por el mástil hacia el lander; la cámara sigue
  un pulso.
- **Cámara:** 50 mm macro, poca profundidad de campo, dolly lento; inclinación
  hacia abajo; match cut al pulso entrando en el casco.
- **Acción:** los sensores muestrean la atmósfera; los pulsos se acumulan; uno
  viaja hacia el interior.
- **FX:** partículas emisivas, scanlines, emisión azul sutil.
- **Transición:** el pulso entra en el casco; match cut al X-ray.
- **Assets:** `LANDER_Mast`, `FX_DataPulse`, `MAT_Emissive_Blue`.
- **Fuente:** Reeves, arquitectura de software.
- **Aceptación:** la fuente de datos es clara; cero texto.
- **Narración:** N2, 0:12–0:25.

### Plano 3 — Disección (0:25–0:38)

- **Frames:** 601–912 (312).
- **Acto:** II.
- **Objetivo:** diseccionar el lander y revelar el ordenador de vuelo.
- **Visual:** la carcasa se vuelve transparente; se ven blanket térmico,
  paneles y antena; dentro, el chasis VME; el rover al fondo.
- **Cámara:** 35 mm, órbita de 180°, lenta; empieza fuera y termina dentro del
  chasis.
- **Acción:** las capas se pelan y desvanecen; el chasis brilla; la cámara entra.
- **FX:** shader X-ray/Fresnel, borde luminoso, transparencia, polvo.
- **Transición:** la cámara se sumerge en el chasis; la carcasa se desvanece.
- **Assets:** `LANDER_Shell`, `LANDER_Panels`, `LANDER_Chassis`, `MAT_XRay`.
- **Fuente:** Reeves, hardware.
- **Aceptación:** la disección se lee; el lander sigue siendo reconocible.
- **Narración:** N3, 0:25–0:38.

### Plano 4 — CPU y 1553 (0:38–0:52)

- **Frames:** 913–1248 (336).
- **Acto:** II.
- **Objetivo:** mostrar el CPU y el bus 1553 como escenario del fallo.
- **Visual:** backplane VME con placas; la CPU brilla; el bus es una autopista
  luminosa; los paquetes fluyen; un anillo/contador pulsa a 8 Hz.
- **Cámara:** tracking por el backplane, 24 mm; macro en el CPU; el bus pulsa.
- **Acción:** el bus cicla; llegan paquetes de ASI/MET y de la cámara; el CPU
  planifica.
- **FX:** emisión, bloom, partículas, shader de pulso.
- **Transición:** la cámara se sumerge en el CPU; el hardware se disuelve en la
  ciudad de tareas.
- **Assets:** `LANDER_CPU`, `LANDER_Bus1553`, `FX_BusPulse`.
- **Fuente:** Reeves, hardware/software.
- **Aceptación:** el ciclo 1553 y el CPU son claros.
- **Narración:** N4, 0:38–0:52.

### Plano 5 — Ciudad de tareas (0:52–1:05)

- **Frames:** 1249–1560 (312).
- **Acto:** II.
- **Objetivo:** introducir la ciudad de tareas, las prioridades y el recurso
  compartido.
- **Visual:** hilos verticales de luz que suben desde el CPU; la altura es la
  prioridad; `bc_sched` blanco arriba, `bc_dist` rojo tercero, medias naranja,
  `ASI/MET` azul abajo; cerrojo ámbar en el centro; anillo de deadline; pulso
  del bus al fondo.
- **Cámara:** 35 mm, plano general, push-in lento; termina en el hilo azul.
- **Acción:** los hilos pulsan; el cerrojo brilla; el anillo gira.
- **FX:** luz volumétrica, partículas, niebla de profundidad.
- **Transición:** push al hilo azul.
- **Assets:** `TASK_BC_SCHED`, `TASK_BC_DIST`, `TASK_MED_01..03`,
  `TASK_ASI_MET`, `FX_Lock`, `FX_Deadline`.
- **Fuente:** Reeves + modelo.
- **Aceptación:** la jerarquía se entiende sin etiquetas.
- **Narración:** N5, 0:52–1:05.

### Plano 6 — El cerrojo (1:05–1:18)

- **Frames:** 1561–1872 (312).
- **Acto:** III.
- **Objetivo:** mostrar a `ASI/MET` tomando el mutex de `select()`.
- **Visual:** el hilo azul llega al cerrojo ámbar; el cerrojo se cierra; el azul
  lo sostiene; llega un pulso de los sensores.
- **Cámara:** 85 mm, primer plano; rack focus del hilo azul al cerrojo.
- **Acción:** `ASI/MET` bloquea; el brillo se adhiere al hilo azul; el anillo de
  deadline arranca.
- **FX:** brillo ámbar, chispas, cámara lenta.
- **Transición:** corte a los hilos naranjas.
- **Assets:** `TASK_ASI_MET`, `FX_Lock`, `FX_Deadline`.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** se entiende que la tarea de baja prioridad tomó el recurso.
- **Narración:** N6, 1:05–1:18.

### Plano 7 — Expropiación (1:18–1:32)

- **Frames:** 1873–2208 (336).
- **Acto:** III.
- **Objetivo:** mostrar la expropiación y la inversión de prioridades.
- **Visual:** hilos naranjas suben y empujan al azul hacia abajo; el azul sigue
  con el cerrojo; los naranjas lo rodean; el azul se atenúa; el cerrojo sigue
  ámbar.
- **Cámara:** 50 mm, tracking lateral; los naranjas cruzan el cuadro; el azul
  queda enterrado.
- **Acción:** las tareas medias expropian; el cerrojo permanece tomado.
- **FX:** motion blur, estelas, pulso naranja.
- **Transición:** corte al hilo rojo.
- **Assets:** `TASK_MED_01..03`, `TASK_ASI_MET`, `FX_Lock`.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** la inversión es visible.
- **Narración:** N7, 1:18–1:32.

### Plano 8 — Bloqueo (1:32–1:45)

- **Frames:** 2209–2520 (312).
- **Acto:** III.
- **Objetivo:** mostrar a `bc_dist` bloqueada.
- **Visual:** el hilo rojo baja con un paquete; llega al cerrojo; se forma una
  cola; el cerrojo no se abre; el rojo pulsa.
- **Cámara:** 35 mm, contrapicado; push al cerrojo; la cola se extiende.
- **Acción:** `bc_dist` solicita; queda bloqueada; el anillo de deadline empieza
  a llenarse.
- **FX:** emisión roja, partículas de cola, vibración del cerrojo.
- **Transición:** match cut al anillo.
- **Assets:** `TASK_BC_DIST`, `FX_Lock`, `FX_Deadline`.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el bloqueo es claro.
- **Narración:** N8, 1:32–1:45.

### Plano 9 — Deadline (1:45–1:58)

- **Frames:** 2521–2832 (312).
- **Acto:** III.
- **Objetivo:** mostrar el incumplimiento del plazo y el atasco del bus.
- **Visual:** el anillo se llena; el bus 1553 stutter; los pulsos saltan; la
  ciudad se atenúa; cámara lenta; el rojo se tensa.
- **Cámara:** 100 mm macro en el anillo; pull back a la ciudad; glitch del bus.
- **Acción:** el tiempo se comprime; el anillo se pone rojo; el anillo del
  watchdog empieza a pulsar.
- **FX:** cámara lenta, aberración cromática, viñeta roja, glitch.
- **Transición:** corte al watchdog.
- **Assets:** `FX_Deadline`, `FX_Watchdog`, `LANDER_Bus1553`.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el deadline miss es visible.
- **Narración:** N9, 1:45–1:58.

### Plano 10 — Watchdog (1:58–2:08)

- **Frames:** 2833–3072 (240).
- **Acto:** III.
- **Objetivo:** mostrar el reset del watchdog y la repetición.
- **Visual:** el hilo blanco `bc_sched` revisa el rojo; el anillo del watchdog se
  pone rojo; onda de choque; la ciudad colapsa en partículas; flash; se
  recompone; montaje rápido de 2–3 reinicios.
- **Cámara:** 24 mm, plano general; cortes rápidos; shake.
- **Acción:** `bc_sched` detecta; reset; repetición.
- **FX:** onda de choque, partículas, flash, shake, glitch.
- **Transición:** el último flash disuelve al CPU/código.
- **Assets:** `TASK_BC_SCHED`, `FX_Watchdog`, `FX_ResetShock`.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el reset es dramático y claro.
- **Narración:** N10, 1:58–2:08.

### Plano 11 — Código (2:08–2:20)

- **Frames:** 3073–3360 (288).
- **Acto:** IV.
- **Objetivo:** pasar al código y mostrar la opción ausente.
- **Visual:** zoom al CPU; el hardware se disuelve; aparece un panel holográfico
  con `select()`, `pipe()` y `semMCreate`; se resaltan las líneas; el hueco de
  `SEM_INVERSION_SAFE` pulsa.
- **Cámara:** 50 mm macro, inmersión; el panel rota; la cámara se asienta.
- **Acción:** el código se desplaza a las líneas críticas; se resalta; el hueco
  pulsa.
- **FX:** scanlines holográficas, emisión, profundidad.
- **Transición:** corte a la terminal.
- **Assets:** `FX_CodePanel`, textura `assets/code/code_panel.png`.
- **Fuente:** Reeves 1999 + demo C.
- **Aceptación:** el código es legible, real, y el hueco es claro.
- **Narración:** N11, 2:08–2:20.

### Plano 12 — Terminal (2:20–2:30)

- **Frames:** 3361–3600 (240).
- **Acto:** IV.
- **Objetivo:** mostrar el demo ejecutable reproduciendo el error.
- **Visual:** panel de terminal en el mismo estilo holográfico; corre
  `make run-pip-off`; se imprime la traza; `WATCHDOG: RESET`; luego
  `make run-pip-on`; `OK`.
- **Cámara:** 85 mm, primer plano fijo.
- **Acción:** la salida se escribe; la línea de reset parpadea en rojo; la de OK
  en verde.
- **FX:** brillo de terminal, scanlines, cursor.
- **Transición:** el OK verde se expande en el aura de PIP.
- **Assets:** `FX_TerminalPanel`, texturas `terminal_off.png` y
  `terminal_on.png`.
- **Fuente:** demo C.
- **Aceptación:** la salida es la del demo real.
- **Narración:** N12, 2:20–2:30.

### Plano 13 — Corrección (2:30–2:40)

- **Frames:** 3601–3840 (240).
- **Acto:** V.
- **Objetivo:** mostrar la herencia de prioridad.
- **Visual:** vuelta a la ciudad; el cerrojo tiene aura verde; cuando el rojo
  espera, el azul hereda la prioridad roja, sube por encima de los naranjas,
  corre y libera el cerrojo.
- **Cámara:** 35 mm, órbita alrededor del cerrojo.
- **Acción:** PIP on; el azul se tiñe de rojo; corre; el cerrojo se abre.
- **FX:** aura verde, partículas de transferencia, cámara lenta.
- **Transición:** corte al ciclo verde.
- **Assets:** `TASK_ASI_MET`, `TASK_BC_DIST`, `FX_Lock`, `FX_PIP`.
- **Fuente:** Reeves, corrección.
- **Aceptación:** la herencia es visible.
- **Narración:** N13, 2:30–2:40.

### Plano 14 — Ciclo verde (2:40–2:50)

- **Frames:** 3841–4080 (240).
- **Acto:** V.
- **Objetivo:** mostrar el ciclo corregido.
- **Visual:** el rojo completa; el anillo de deadline se pone verde; el bus
  fluye; la ciudad se estabiliza; el watchdog calla.
- **Cámara:** 24 mm, pull back desde el cerrojo a la ciudad.
- **Acción:** `bc_dist` termina; no hay reset; el ciclo se repite.
- **FX:** emisión verde, pulsos suaves, bloom.
- **Transición:** pull back a través del CPU, el chasis y el lander.
- **Assets:** `FX_Deadline`, `LANDER_Bus1553`, `TASK_BC_DIST`.
- **Fuente:** Reeves, corrección.
- **Aceptación:** el contraste con el plano 9 es claro.
- **Narración:** N14, 2:40–2:50.

### Plano 15 — Cierre (2:50–3:00)

- **Frames:** 4081–4320 (240).
- **Acto:** V.
- **Objetivo:** cerrar el film y volver a Marte.
- **Visual:** pullback a través del lander; la carcasa se vuelve opaca; el rover
  avanza; atardecer; fade a negro.
- **Cámara:** 24 mm, grúa ascendente, lenta.
- **Acción:** el sistema es estable; el rover continúa; fade.
- **FX:** polvo, atardecer, flare.
- **Transición:** fade out.
- **Assets:** `LANDER`, `ROVER`, `ENV_Sky`.
- **Fuente:** síntesis.
- **Aceptación:** final tranquilo y seguro.
- **Narración:** N15, 2:50–3:00.

## 4. Continuidad y transiciones

| Corte | Recurso | Nota |
| :---: | :--- | :--- |
| 1 → 2 | corte al mástil | el mástil ocupa el mismo eje que el sol |
| 2 → 3 | match cut del pulso | el pulso entra en el casco y se vuelve X-ray |
| 3 → 4 | inmersión | la cámara atraviesa el chasis hasta el CPU |
| 4 → 5 | dissolve | el hardware se disuelve en hilos de luz |
| 5 → 6 | push al azul | el hilo azul llena el cuadro |
| 6 → 7 | corte | los hilos naranjas entran desde el fondo |
| 7 → 8 | corte | el rojo aparece en el mismo eje del cerrojo |
| 8 → 9 | match cut | el cerrojo se convierte en el anillo |
| 9 → 10 | corte | el anillo rojo llena el cuadro |
| 10 → 11 | flash/dissolve | el último reset disuelve la ciudad en código |
| 11 → 12 | corte | el panel de código se convierte en terminal |
| 12 → 13 | expansión del OK | el verde se convierte en aura de PIP |
| 13 → 14 | corte | el cerrojo se abre y el anillo se vuelve verde |
| 14 → 15 | pullback | la ciudad se aleja y se convierte en el lander |
| 15 | fade out | único fundido a negro del film |

## 5. Mapa de assets por iteración

| Iteración | Módulos | Planos |
| :--- | :--- | :--- |
| I3 | `terrain.py`, `lander.py` exterior, `rover.py`, `materials.py` | 1–3 |
| I4 | `lander.py` interior, `tasks.py`, paneles | 4–6, 10–13 |
| I5 | `cameras.py`, animación | 1–5, 11–12 |
| I6 | `tasks.py`, FX | 6–10 |
| I7 | continuidad, cierre | 13–15 |

## 6. Criterios de aceptación por acto

- **I:** Marte, lander y rover reconocibles; los sensores se entienden.
- **II:** la disección revela el CPU y el bus; la ciudad muestra la jerarquía.
- **III:** se ve la toma del cerrojo, la expropiación, el bloqueo, el deadline y
  el reset.
- **IV:** el código es legible y el demo reproduce el error.
- **V:** la herencia se ve y el ciclo termina en verde.

## 7. Reglas de producción

1. No hay texto fuera de los planos 11–12.
2. No hay audio.
3. No se atribuye el fallo al rover.
4. No se dice "el RTOS se cayó": el watchdog reinició el sistema.
5. No se dice "pérdida de datos" sin matizar: los datos en RAM se conservan si
   se mantiene la alimentación.
6. El film no es una emulación de VxWorks; es una reconstrucción visual.
7. Las metáforas visuales son licencia artística declarada.
8. Toda afirmación técnica se mapea a `AGENTS.md` §3.1 o §4.

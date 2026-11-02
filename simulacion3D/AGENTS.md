# AGENTS.md — Simulación 3D del fallo de Mars Pathfinder

> **Estado:** vivo. Leer al iniciar. Actualizar al cerrar cada turno.
> **Última actualización:** 2026-11-02 · OpenCode (DeepSeek V4.1 Flash)
> **Documento maestro del repositorio:** `../AGENTS.md`.
> **Este archivo es el contrato local y la biblia de producción de `simulacion3D/`.**
> La secuencia canónica del film está en §4. `STORYBOARD.md` será una copia
> imprimible/derivada de esa sección, no una fuente paralela.

## 0. Regla de actualización (R0 local)

Todo agente que cree, modifique, mueva o elimine un archivo en `simulacion3D/` debe:

1. Actualizar la bitácora §11.
2. Actualizar el inventario §10.
3. Ajustar los checkboxes §12.
4. Actualizar el estado §1.
5. Actualizar `../AGENTS.md` (§8.3 bitácora y §8.4 inventario), porque el repositorio es la fuente de verdad global.

Si el disco contradice este documento, prevalece el disco y se corrige el documento.

## 1. Estado actual

- **Fase:** preproducción; I0 (base técnica) completada.
- **Entregable único:** `out/pathfinder_failure.mp4`.
- **Próximo hito:** `STORYBOARD.md` derivado + `NARRACION.md` + animatic de 15–20 s.
- **Bloqueos:** ninguno; `../entornoRTOS/` reproduce S1/S2 y las texturas reales ya están generadas.
- **Riesgo principal:** tiempo de render (medido en la escena de prueba: 3,35–7,64 s/frame a 1080p) y claridad del film sin texto.
- **Alcance:** solo el film. El artículo, el motor S0–S5 y el demo C viven fuera de este directorio.

## 2. Objetivo, alcance y decisiones cerradas

### 2.1. Objetivo

Producir un **documental 3D mudo** de 2:45–3:00 que muestre, paso a paso, la
inversión de prioridades no acotada en el RTOS VxWorks del lander Mars
Pathfinder, su manifestación en el ciclo 1553, el reset del watchdog y la
corrección con herencia de prioridad.

### 2.2. Entregable

- `out/pathfinder_failure.mp4`: 1920 × 1080, 24 fps, H.264, 2:45–3:00.
- Sin audio.
- Sin texto en pantalla, salvo el código y la terminal de los planos 11–12.
- La narración es en vivo, para la exposición.
- Proyecto editable: `blender/pathfinder_failure.blend`.
- Construcción reproducible: `build_scene.py` + `modules/`.
- Documentación: `STORYBOARD.md`, `NARRACION.md`, `README.md`.

### 2.3. Decisiones cerradas

| Decisión | Valor |
| :--- | :--- |
| Motor 3D | Blender 5.2.3 LTS |
| Render | EEVEE, 1920 × 1080, 24 fps |
| Duración | 2:45–3:00 |
| Audio | Ninguno; narración en vivo |
| Texto | Ninguno salvo código/terminal (planos 11–12) |
| Objeto del fallo | Ordenador de vuelo del lander |
| Rover | Contexto visual, nunca víctima |
| Tipo de animación | Independiente del motor Python; guion propio con fuentes |
| Demo C | Modelo determinista, sin privilegios, fuera de este directorio |
| Cierre de features | 22/11/2026 |
| Entrega | 29/11/2026 |

### 2.4. Incluye

- Ares Vallis, lander y rover como contexto visual.
- Sensores/instrumento ASI/MET, cámara y tareas medias.
- Disección del ordenador de vuelo del lander: VME, CPU, bus 1553.
- Ciudad de tareas, mutex de `select()`, prioridades, deadline y watchdog.
- Transición al código y a la terminal del demo C.
- Corrección con PIP on.

### 2.5. No incluye

- El rover como objeto del fallo.
- Emulación bit a bit de VxWorks.
- Física de aterrizaje, protocolo 1553 detallado, caché/pipeline.
- Artículo, slides, corpus o demo C: viven fuera de este directorio.
- Audio o voice-over.
- Texto narrativo, títulos, subtítulos o etiquetas en la escena.

## 3. Hechos, fuentes y cadena causal

### 3.1. Hechos y fuentes

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

### 3.2. Cadena causal que el film debe mostrar

```
Datos de los sensores ASI/MET
        ↓
Tarea ASI/MET (prioridad 7) llama a select() y toma el mutex interno
        ↓
Tareas medias (prioridades 4–6) despiertan y expropian a ASI/MET
        ↓
bc_dist (prioridad 3) necesita el mismo mutex y queda bloqueada
        ↓
El ciclo 1553 de 125 ms avanza; bc_dist no termina
        ↓
bc_sched (prioridad 1) detecta el plazo incumplido
        ↓
Watchdog: reset del sistema
```

Con PIP on:

```
bc_dist espera → ASI/MET hereda la prioridad 3 → corre por encima de las
tareas medias → libera el mutex → bc_dist termina → no hay reset
```

### 3.3. Reglas de integridad

1. No atribuir el fallo a Sojourner.
2. No decir "el RTOS se cayó": VxWorks funcionó como estaba configurado.
3. No decir "pérdida de datos" sin matizar: se conservan si no se pierde la alimentación.
4. No presentar el film como emulación de VxWorks; es una reconstrucción visual.
5. Las metáforas visuales (ciudad de tareas, cerrojo, anillos) son licencia artística declarada, no hardware real.
6. Toda afirmación técnica del film debe poder mapearse a §3.1 o a §4.

## 4. Secuencia completa del film

### 4.1. Estructura en cinco actos

| Acto | Tiempo | Contenido | Emoción |
| :--- | :--- | :--- | :--- |
| I. Marte | 0:00–0:25 | Ares Vallis, lander, rover, sensores ASI/MET | Calma, escala, asombro |
| II. El sistema | 0:25–1:05 | Disección, VME, CPU, bus 1553, ciudad de tareas | Orden técnico, complejidad |
| III. La inversión | 1:05–2:08 | Cerrojo, expropiación, bloqueo, deadline, watchdog | Tensión, opresión, colapso |
| IV. El código | 2:08–2:30 | Código, terminal, demo C, error reproducible | Revelación, diagnóstico |
| V. La corrección | 2:30–3:00 | PIP on, herencia, ciclo verde, cierre | Alivio, control |

### 4.2. Storyboard compacto: 15 planos, 2:45–3:00

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

### 4.3. Guion técnico plano por plano

#### Plano 1 — Ares Vallis (0:00–0:12)

- **Objetivo narrativo:** establecer Marte, el lander y el rover como contexto.
- **Visual:** llanura rojiza de Ares Vallis, rocas dispersas, colinas al fondo;
  el lander a la izquierda con paneles solares y mástil; el rover como un punto
  metálico que avanza; polvo en suspensión; sol bajo.
- **Cámara:** 24 mm, grúa lenta de izquierda a derecha, 1,5 m sobre el suelo,
  ligera inclinación hacia abajo; parallax con las rocas; termina en el mástil
  del lander contra el sol.
- **Acción:** el polvo se desplaza; el rover recorre una curva; la antena
  destella; no hay texto.
- **FX:** polvo volumétrico, heat shimmer, lens flare sutil.
- **Transición:** corte al mástil ASI/MET.
- **Implementación Blender:** `ENV_Terrain` con desplazamiento; `ENV_Rocks`
  instanciadas; `LANDER` y `ROVER`; sol; gradiente de mundo; keyframes de cámara.
- **Fuente:** NASA.
- **Aceptación:** Marte, lander y rover reconocibles; cero texto.

#### Plano 2 — ASI/MET (0:12–0:25)

- **Objetivo narrativo:** mostrar los sensores/instrumento que alimentan el
  sistema e introducir el flujo de datos.
- **Visual:** macro del mástil ASI/MET: sensores de viento, temperatura y
  presión; pulsos azules bajan por el mástil hacia el lander; la cámara sigue
  un pulso.
- **Cámara:** 50 mm macro, poca profundidad de campo, dolly lento; inclinación
  hacia abajo; match cut al pulso entrando en el casco.
- **Acción:** los sensores muestrean la atmósfera; los pulsos se acumulan; uno
  viaja hacia el interior.
- **FX:** partículas emisivas, scanlines, emisión azul sutil.
- **Transición:** el pulso entra en el casco; match cut al X-ray.
- **Implementación Blender:** modelar mástil y sensores; curvas para pulsos;
  DOF; material emisivo.
- **Fuente:** Reeves, arquitectura de software.
- **Aceptación:** la fuente de datos es clara; cero texto.

#### Plano 3 — Disección (0:25–0:38)

- **Objetivo narrativo:** diseccionar el lander y revelar el ordenador de vuelo.
- **Visual:** la carcasa del lander se vuelve transparente; se ven el blanket
  térmico, los paneles solares y la antena; dentro, el chasis VME; el rover al
  fondo.
- **Cámara:** 35 mm, órbita de 180°, lenta; empieza fuera y termina dentro del
  chasis.
- **Acción:** las capas se pelan/desvanecen; el chasis brilla; la cámara entra.
- **FX:** shader X-ray/Fresnel, borde luminoso, transparencia, polvo.
- **Transición:** la cámara se sumerge en el chasis; la carcasa se desvanece.
- **Implementación Blender:** objetos separados para carcasa, paneles y chasis;
  animar alpha; material Fresnel; órbita de cámara.
- **Fuente:** Reeves, hardware.
- **Aceptación:** la disección se lee; el lander sigue siendo reconocible.

#### Plano 4 — CPU y 1553 (0:38–0:52)

- **Objetivo narrativo:** mostrar el CPU y el bus 1553 como escenario del fallo.
- **Visual:** backplane VME con placas; la placa CPU brilla; el bus 1553 es una
  autopista luminosa; los paquetes fluyen; un anillo/contador pulsa a 8 Hz.
- **Cámara:** tracking por el backplane, 24 mm; macro en el CPU; el bus pulsa.
- **Acción:** el bus cicla; llegan paquetes de ASI/MET y de la cámara; el CPU
  planifica.
- **FX:** emisión, bloom, partículas, shader de pulso.
- **Transición:** la cámara se sumerge en el CPU; el hardware se disuelve en la
  ciudad de tareas.
- **Implementación Blender:** placas, curvas del bus, emisión; animar pulso;
  recorrido de cámara; transición por dissolve de material.
- **Fuente:** Reeves, hardware/software.
- **Aceptación:** el ciclo 1553 y el CPU son claros.

#### Plano 5 — Ciudad de tareas (0:52–1:05)

- **Objetivo narrativo:** introducir la ciudad de tareas, las prioridades y el
  recurso compartido.
- **Visual:** hilos verticales de luz que suben desde el CPU; la altura es la
  prioridad; `bc_sched` blanco arriba, `bc_dist` rojo tercero, tareas medias
  naranja, `ASI/MET` azul abajo; cerrojo ámbar en el centro; anillo de deadline;
  el pulso del bus al fondo.
- **Cámara:** 35 mm, plano general, push-in lento; termina en el hilo azul.
- **Acción:** los hilos pulsan; el cerrojo brilla; el anillo gira.
- **FX:** luz volumétrica, partículas, niebla de profundidad.
- **Transición:** push al hilo azul.
- **Implementación Blender:** curvas/tubos con emisión; animar escala/posición;
  objeto cerrojo; anillo; cámara.
- **Fuente:** Reeves + modelo.
- **Aceptación:** la jerarquía se entiende sin etiquetas.

#### Plano 6 — El cerrojo (1:05–1:18)

- **Objetivo narrativo:** mostrar a `ASI/MET` tomando el mutex de `select()`.
- **Visual:** el hilo azul llega al cerrojo ámbar; el cerrojo se abre/cierra; el
  azul lo sostiene; llega un pulso de los sensores.
- **Cámara:** 85 mm, primer plano; rack focus del hilo azul al cerrojo.
- **Acción:** `ASI/MET` bloquea; el brillo se adhiere al hilo azul; el anillo de
  deadline arranca.
- **FX:** brillo ámbar, chispas, cámara lenta.
- **Transición:** corte a los hilos naranjas.
- **Implementación Blender:** animación del cerrojo; glow parentado al hilo;
  constraint; foco.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** se entiende que la tarea de baja prioridad tomó el recurso.

#### Plano 7 — Expropiación (1:18–1:32)

- **Objetivo narrativo:** mostrar la expropiación y la inversión de prioridades.
- **Visual:** hilos naranjas suben y empujan al hilo azul hacia abajo; el azul
  sigue con el cerrojo; los naranjas lo rodean; el azul se atenúa; el cerrojo
  sigue ámbar.
- **Cámara:** 50 mm, tracking lateral; los naranjas cruzan el cuadro; el azul
  queda enterrado.
- **Acción:** las tareas medias expropian; el cerrojo permanece tomado.
- **FX:** motion blur, estelas, pulso naranja.
- **Transición:** corte al hilo rojo.
- **Implementación Blender:** animar posiciones de hilos; multitud de naranjas;
  cámara.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** la inversión es visible.

#### Plano 8 — Bloqueo (1:32–1:45)

- **Objetivo narrativo:** mostrar a `bc_dist` bloqueada.
- **Visual:** el hilo rojo baja con un paquete; llega al cerrojo; se forma una
  cola; el cerrojo no se abre; el rojo pulsa.
- **Cámara:** 35 mm, contrapicado; push al cerrojo; la cola se extiende.
- **Acción:** `bc_dist` solicita; queda bloqueada; el anillo de deadline empieza
  a llenarse.
- **FX:** emisión roja, partículas de cola, vibración del cerrojo.
- **Transición:** match cut al anillo.
- **Implementación Blender:** hilo rojo, paquete, cola; animar resistencia.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el bloqueo es claro.

#### Plano 9 — Deadline (1:45–1:58)

- **Objetivo narrativo:** mostrar el incumplimiento del plazo y el atasco del bus.
- **Visual:** el anillo de deadline se llena; el bus 1553 stutter; los pulsos
  saltan; la ciudad se atenúa; cámara lenta; el rojo se tensa.
- **Cámara:** 100 mm macro en el anillo; pull back a la ciudad; glitch del bus.
- **Acción:** el tiempo se comprime; el anillo se pone rojo; el anillo del
  watchdog empieza a pulsar.
- **FX:** cámara lenta, aberración cromática, viñeta roja, glitch.
- **Transición:** corte al watchdog.
- **Implementación Blender:** shader/scale del anillo; emisión del bus;
  compositor.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el deadline miss es visible.

#### Plano 10 — Watchdog (1:58–2:08)

- **Objetivo narrativo:** mostrar el reset del watchdog y la repetición.
- **Visual:** el hilo blanco `bc_sched` revisa el rojo; el anillo del watchdog se
  pone rojo; onda de choque; la ciudad colapsa en partículas; flash; se
  recompone; montaje rápido de 2–3 reinicios.
- **Cámara:** 24 mm, plano general; cortes rápidos; shake.
- **Acción:** `bc_sched` detecta; reset; repetición.
- **FX:** onda de choque, partículas, flash, shake, glitch.
- **Transición:** el último flash disuelve al CPU/código.
- **Implementación Blender:** anillo, onda (esfera escalada), partículas, shake
  de cámara, compositor.
- **Fuente:** Reeves, "THE FAILURE".
- **Aceptación:** el reset es dramático y claro.

#### Plano 11 — Código (2:08–2:20)

- **Objetivo narrativo:** pasar al código y mostrar la opción ausente.
- **Visual:** zoom al CPU; el hardware se disuelve; aparece un panel holográfico
  con `select()`, `pipe()`, `semMCreate`; se resaltan las líneas; el hueco de
  `SEM_INVERSION_SAFE` pulsa.
- **Cámara:** 50 mm macro, inmersión; el panel rota; la cámara se asienta.
- **Acción:** el código se desplaza a las líneas críticas; se resalta; el hueco
  pulsa.
- **FX:** scanlines holográficas, emisión, profundidad.
- **Transición:** corte a la terminal.
- **Implementación Blender:** textura de código desde el fuente real; plano con
  emisión; animar resaltado; cámara.
- **Fuente:** Reeves 1999 + demo C.
- **Aceptación:** el código es legible, real, y el hueco es claro.

#### Plano 12 — Terminal (2:20–2:30)

- **Objetivo narrativo:** mostrar el demo ejecutable reproduciendo el error.
- **Visual:** panel de terminal en el mismo estilo holográfico; corre
  `make run-pip-off`; se imprime la traza; `WATCHDOG: RESET`; luego
  `make run-pip-on`; `OK`.
- **Cámara:** 85 mm, primer plano fijo.
- **Acción:** la salida se escribe; la línea de reset parpadea en rojo; la de OK
  en verde.
- **FX:** brillo de terminal, scanlines, cursor.
- **Transición:** el OK verde se expande en el aura de PIP.
- **Implementación Blender:** textura de salida real; animar revelado; máscara.
- **Fuente:** demo C.
- **Aceptación:** la salida es la del demo real.

#### Plano 13 — Corrección (2:30–2:40)

- **Objetivo narrativo:** mostrar la herencia de prioridad.
- **Visual:** vuelta a la ciudad; el cerrojo tiene aura verde; cuando el rojo
  espera, el azul hereda la prioridad roja, sube por encima de los naranjas,
  corre, libera el cerrojo.
- **Cámara:** 35 mm, órbita alrededor del cerrojo.
- **Acción:** PIP on; el azul se tiñe de rojo; corre; el cerrojo se abre.
- **FX:** aura verde, partículas de transferencia, cámara lenta.
- **Transición:** corte al ciclo verde.
- **Implementación Blender:** animar color/altura del hilo; cerrojo; cámara.
- **Fuente:** Reeves, corrección.
- **Aceptación:** la herencia es visible.

#### Plano 14 — Ciclo verde (2:40–2:50)

- **Objetivo narrativo:** mostrar el ciclo corregido.
- **Visual:** el rojo completa; el anillo de deadline se pone verde; el bus fluye;
  la ciudad se estabiliza; el watchdog calla.
- **Cámara:** 24 mm, pull back desde el cerrojo a la ciudad.
- **Acción:** `bc_dist` termina; no hay reset; el ciclo se repite.
- **FX:** emisión verde, pulsos suaves, bloom.
- **Transición:** pull back a través del CPU, el chasis y el lander.
- **Implementación Blender:** color del anillo, bus, cámara.
- **Fuente:** Reeves, corrección.
- **Aceptación:** el contraste con el plano 9 es claro.

#### Plano 15 — Cierre (2:50–3:00)

- **Objetivo narrativo:** cerrar el film y volver a Marte.
- **Visual:** pullback a través del lander; la carcasa se vuelve opaca; el rover
  avanza; atardecer; fade a negro.
- **Cámara:** 24 mm, grúa ascendente, lenta.
- **Acción:** el sistema es estable; el rover continúa; fade.
- **FX:** polvo, atardecer, flare.
- **Transición:** fade out.
- **Implementación Blender:** recorrido de cámara, iluminación, fade.
- **Fuente:** síntesis.
- **Aceptación:** final tranquilo y seguro.

### 4.4. Lo que el espectador debe entender al final

1. El fallo ocurrió en el ordenador de vuelo del lander, no en el rover.
2. Una tarea de baja prioridad (`ASI/MET`) retenía el mutex de `select()`.
3. Las tareas medias la expropiaban y impedían que liberara el mutex.
4. `bc_dist`, de mayor prioridad, quedaba bloqueada.
5. El ciclo 1553 de 125 ms se incumplía y el watchdog reiniciaba.
6. La herencia de prioridad acotó el bloqueo y eliminó los reinicios.
7. El error se reproduce en un demo C compilable; no es una emulación de VxWorks.

## 5. Lenguaje visual

### 5.1. Paleta y código de color

| Elemento | Color | Hex | Uso |
| :--- | :--- | :--- | :--- |
| `bc_sched` | Blanco | `#FFFFFF` | Tarea de mayor prioridad; watchdog |
| `bc_dist` | Rojo | `#FF3B30` | Tarea bloqueada; deadline |
| Tareas medias | Naranja | `#FF9500` | Expropiación; carga de CPU |
| `ASI/MET` | Azul | `#0A84FF` | Tarea de baja prioridad; sensores |
| Mutex | Ámbar | `#FFB300` | Cerrojo de `select()` |
| Deadline | Rojo → verde | `#FF3B30` → `#34C759` | Estado del plazo |
| Watchdog | Blanco/rojo | `#FFFFFF` / `#FF3B30` | Detección y reset |
| PIP on | Verde | `#34C759` | Herencia de prioridad |
| Marte | Rojos y ocres | `#8B3A1E`, `#C1440E`, `#E27D60` | Terreno y cielo |
| Metal | Gris | `#B0B0B0` | Lander y rover |
| Aislamiento | Dorado | `#D4A017` | Blanket térmico |

### 5.2. Formas y metáforas

- **Cerrojo:** toro/cilindro ámbar con un ojo central; se cierra cuando alguien
  toma el mutex.
- **Anillo de deadline:** anillo alrededor de la tarea; se llena de rojo.
- **Anillo de watchdog:** anillo blanco en la cima; pulsa y se pone rojo.
- **Bus 1553:** autopista luminosa que conecta las placas; los paquetes son
  chispas.
- **Ciudad de tareas:** hilos verticales; la altura es la prioridad; el color es
  el rol.
- **Herencia:** el hilo azul se tiñe de rojo y sube; partículas de transferencia.
- **Reset:** onda de choque y colapso en partículas; reconstrucción.

### 5.3. Cámara y montaje

- 24 fps; movimientos lentos; cortes en el pulso del bus.
- 24 mm para paisajes y planos generales; 35 mm para interiores; 50 mm para
  macro; 85–100 mm para detalles.
- Poca profundidad de campo en macro; foco profundo en paisajes.
- Sin cámara en mano, salvo el shake del reset.
- Transiciones: match cuts, dissolves y continuidad de movimiento.
- El film no usa fundidos a negro salvo el cierre.

### 5.4. Texto y audio

- **Texto:** solo el código y la terminal de los planos 11–12. Nada de títulos,
  etiquetas, subtítulos ni créditos dentro del film.
- **Audio:** ninguno. La narración es en vivo, con `NARRACION.md`.
- **Créditos:** si se usan imágenes NASA, se acreditan en `README.md` y en las
  slides, no en el film.

## 6. Dirección de arte

### 6.1. Marte

- Terreno procedural con ruido fractal; escala 200 × 200 m; rocas instanciadas.
- Paleta rojiza; cielo con gradiente de atardecer; polvo volumétrico.
- Sin vegetación, sin agua, sin signos de vida.
- El lander y el rover deben leerse a escala.

### 6.2. Lander

- Cuerpo principal, paneles solares, antena, mástil ASI/MET, cámara.
- Interior: chasis VME, backplane, placas, CPU, bus 1553.
- Materiales: metal gris, blanket dorado, paneles azul oscuro con emisión.
- La carcasa debe poder volverse transparente sin perder su silueta.

### 6.3. Rover

- Modelo simple: cuerpo, seis ruedas, panel solar, mástil de cámara.
- Escala ~0,7 m; se mueve por una curva; nunca falla.
- Es un guía visual, no el objeto del fallo.

### 6.4. Ciudad de tareas

- Hilos verticales con emisión; alturas y colores de §5.1.
- Cerrojo, anillo de deadline, anillo de watchdog.
- Fondo: el bus 1553 y el CPU desenfocados.
- La ciudad debe ser legible en plano general y en macro.

### 6.5. Código y terminal

- Fuente monoespaciada DejaVu Sans Mono.
- Fondo `#0B0F14`; ámbar `#FFB000`; verde `#33FF77`; rojo `#FF3B30`.
- El código se genera desde `../entornoRTOS/src/` y `../entornoRTOS/include/`; no se inventa.
- La terminal se genera desde `../entornoRTOS/out/s1_pip_off.txt` y
  `../entornoRTOS/out/s2_pip_on.txt`; el generador es
  `assets/code/make_textures.py`.
- Los paneles son holográficos, pero el texto debe ser nítido y legible.

### 6.6. Escala y unidades

- 1 unidad Blender = 1 metro.
- Lander ~2,5 m de altura; rover ~0,7 m; terreno 200 m.
- Cámara: clip start 0,01 m; clip end 1000 m.
- Profundidad de campo en macro: f/2.8–f/4; paisaje: f/8–f/11.

## 7. Arquitectura técnica

### 7.1. Stack

- Blender 5.2.3 LTS; EEVEE.
- Python 3.14.8 (el que trae Blender) + mathutils.
- ffmpeg 9.0.2 para codificar.
- PIL (Python del sistema) para generar texturas de código/terminal.
- Sin dependencias externas de Blender.

### 7.2. Estructura de archivos

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
    │   ├── shot_01/
    │   ├── ...
    │   └── shot_15/
    └── pathfinder_failure.mp4
```

### 7.3. Convenciones de nombres

- Objetos: `ENV_`, `LANDER_`, `ROVER_`, `TASK_`, `FX_`, `CAM_`, `LIGHT_`, `MAT_`.
- Colecciones: `00_ENV`, `01_LANDER`, `02_ROVER`, `03_TASKS`, `04_FX`,
  `05_CAMERAS`, `06_LIGHTS`.
- Planos: `shot_01` … `shot_15`.
- Frames: `frame_0001.png`, `frame_0002.png`, etc.
- Materiales: `MAT_Mars`, `MAT_Metal`, `MAT_Emissive_Blue`, `MAT_XRay`, etc.

### 7.4. Jerarquía de escena

```
SCENE
├── 00_ENV
│   ├── ENV_Terrain
│   ├── ENV_Rocks
│   └── ENV_Sky
├── 01_LANDER
│   ├── LANDER_Shell
│   ├── LANDER_Panels
│   ├── LANDER_Mast
│   ├── LANDER_Chassis
│   ├── LANDER_CPU
│   └── LANDER_Bus1553
├── 02_ROVER
├── 03_TASKS
│   ├── TASK_BC_SCHED
│   ├── TASK_BC_DIST
│   ├── TASK_MED_01 … TASK_MED_03
│   ├── TASK_ASI_MET
│   ├── FX_Lock
│   ├── FX_Deadline
│   └── FX_Watchdog
├── 04_FX
├── 05_CAMERAS
└── 06_LIGHTS
```

### 7.5. Materiales

- PBR para terreno, metal y paneles.
- Emisión para hilos, bus, cerrojo y anillos.
- Fresnel/transparencia para el X-ray de la carcasa.
- Shader de anillo con parámetro de llenado (0–1).
- Sin texturas externas obligatorias; las procedurales se generan con nodos.

### 7.6. Iluminación

- Sol cálido, bajo, 4500 K; luz de relleno azul fría; rim light.
- Volumétrico para polvo; sin HDRI externo.
- La ciudad de tareas es autoiluminada; bloom controlado.
- El código/terminal es autoiluminado y nítido.

### 7.7. Animación

- 24 fps; keyframes cada 2 s; interpolación Bezier con ease in/out.
- Sin física; movimiento determinista.
- Rover: `Follow Path`; cámaras: `Track To` + keyframes.
- Partículas con semilla fija.
- No usar simulaciones que dependan del tiempo real.

### 7.8. Render

- EEVEE; 1920 × 1080; 24 fps; samples 32 (draft 16); motion blur on;
  bloom on; ambient occlusion on.
- Color management: AgX o Filmic; exposición fija.
- Salida PNG RGB, compresión 15.
- Render por plano a `out/frames/shot_XX/`.
- Frame de prueba antes del render completo; medir tiempo por frame.

### 7.9. Postproducción

- Codificar con ffmpeg; sin audio.
- Revisar duración, fps y resolución con ffprobe.
- Sin títulos ni créditos dentro del film.
- El montaje final debe respetar los 15 planos y los tiempos de §4.2.

## 8. Pipeline y comandos

```bash
# Construir y guardar el .blend
blender -b --factory-startup --python build_scene.py -- --save

# Frame de prueba (medir tiempo y confirmar EEVEE headless)
blender -b blender/pathfinder_failure.blend -f 1

# Render de un plano (ejemplo: plano 3)
blender -b blender/pathfinder_failure.blend -S shot_03 -s 1 -e 312 -a

# Render completo
blender -b blender/pathfinder_failure.blend -a

# Codificar
ffmpeg -framerate 24 -i out/frames/shot_%02d/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 out/pathfinder_failure.mp4

# Verificar
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  out/pathfinder_failure.mp4
```

**Fallback:** si EEVEE falla headless, usar Workbench; si el tiempo es excesivo,
720p y reescalado. Documentar el tiempo por frame.

## 9. Integración del demo C

El demo C vive fuera de este directorio, en `../entornoRTOS/`. Es la evidencia
ejecutable del plano 12 y la fuente del código del plano 11.

### 9.1. Contrato esperado de `../entornoRTOS/`

- `make test`: verifica S0/S1/S2/S3 (S1 reset, S2 OK).
- `make run-pip-off`: imprime la traza y `WATCHDOG: RESET`.
- `make run-pip-on`: imprime la traza y `OK`.
- Salidas: `../entornoRTOS/out/s1_pip_off.txt`, `../entornoRTOS/out/s2_pip_on.txt`.
  El disco prevalece: no se renombran.
- Código: `../entornoRTOS/src/pipe.c`, `../entornoRTOS/src/scenario.c`,
  `../entornoRTOS/src/flight_sw.c`, `../entornoRTOS/include/vxworks_like.h`.

### 9.2. Generación de texturas

1. Ejecutar `make test`, `make run-pip-off` y `make run-pip-on` en `../entornoRTOS/`.
2. Ejecutar `python3 assets/code/make_textures.py`: lee el fuente real y captura
   la salida de consola del binario.
3. Generar `assets/code/code_panel.png`, `terminal_off.png` y `terminal_on.png`,
   con sus compañeras `.txt` para revisión.
4. Revisar la trazabilidad en `assets/code/SOURCES.md`.
5. Aplicar como textura emisiva en los planos 11–12.
6. No inventar líneas de código ni salidas.

### 9.3. Regla de honestidad

El film no dice "código original de VxWorks". Dice, visualmente, "modelo
ejecutable del patrón". La narración en vivo lo aclara.

## 10. Inventario

| Ruta | Tipo | Propósito | Estado |
| :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento | Contrato local y biblia de producción | Activo |
| `README.md` | Documento | Build, render y medición de I0 | Activo |
| `STORYBOARD.md` | Documento | Copia imprimible de §4 | Pendiente |
| `NARRACION.md` | Documento | Guion en vivo | Pendiente |
| `build_scene.py` | Python | Escena base y frame de prueba | Activo (I0) |
| `render.sh` | Script | Envoltorio de build, test y render por plano | Activo |
| `modules/cameras.py` | Python | Cámaras, luces y objetivos | Activo |
| `modules/materials.py` | Python | Paleta y materiales PBR/emisión | Activo |
| `modules/render.py` | Python | EEVEE, compositor, guardado y medición | Activo |
| `modules/terrain.py` | Python | Terreno, rocas y cielo | Pendiente |
| `modules/lander.py` | Python | Lander exterior e interior | Pendiente |
| `modules/rover.py` | Python | Rover de contexto | Pendiente |
| `modules/tasks.py` | Python | Ciudad de tareas, cerrojo y anillos | Pendiente |
| `blender/pathfinder_failure.blend` | Blender | Proyecto editable (escena base) | Activo (I0) |
| `assets/code/make_textures.py` | Python | Generador de texturas desde el demo | Activo |
| `assets/code/code_panel.png` | Imagen | Código real de `../entornoRTOS/` | Activo |
| `assets/code/terminal_off.png` | Imagen | Terminal S1 (`WATCHDOG: RESET`) | Activo |
| `assets/code/terminal_on.png` | Imagen | Terminal S2 (`OK`) | Activo |
| `assets/code/SOURCES.md` | Documento | Trazabilidad de las texturas | Activo |
| `assets/fonts/` | Fuentes | DejaVu Sans Mono | Activo |
| `out/frames/shot_01/` … `shot_15/` | Directorios | Secuencia de render | Vacíos |
| `out/spike/` | PNG | Frames de prueba (ignorados por git) | Activo |
| `out/pathfinder_failure.mp4` | Video | Entregable final | Pendiente |
| `.gitignore` | Git | Exclusiones de render y temporales | Activo |

## 11. Bitácora

| Fecha | Agente | Archivos | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `README.md`, `build_scene.py`, `render.sh`, `modules/`, `assets/code/`, `assets/fonts/`, `blender/pathfinder_failure.blend`, `out/spike/`, `.gitignore` | I0: base técnica del film; escena de prueba EEVEE; texturas reales de código/terminal desde `../entornoRTOS/`; medición de render y corrección de los nombres de salida en §9.1. | `blender -b ... -- --save --test-frame`: 1080p 7,64 s en frío y 3,35 s con caché; 720p 1,24 s; `python3 assets/code/make_textures.py` OK; `py_compile` OK. |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Actualizadas las referencias `../demo/` → `../entornoRTOS/`; desbloqueado el demo C para los planos 11–12. | `grep` sin `../demo/`; `../entornoRTOS/make test` PASS. |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Ampliación con la secuencia completa de 15 planos, guion técnico, dirección de arte, pipeline, integración del demo C y criterios de aceptación. | `wc -l`; 15 planos; tablas y secciones revisadas. |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Creación del contrato local de `simulacion3D/` con alcance, storyboard, pipeline y R0. | Archivo creado; `ls -la simulacion3D`. |

## 12. Checklist de producción

### 12.1. Preproducción
- [ ] Escribir `STORYBOARD.md` derivado de §4.
- [ ] Escribir `NARRACION.md` con tiempos.
- [ ] Construir animatic de 15–20 s.
- [ ] Validar el lenguaje visual con una persona externa.
- [ ] Congelar el guion el 8/11.

### 12.2. Modelado
- [ ] Terreno, rocas y cielo.
- [ ] Lander exterior (carcasa, paneles, antena, mástil).
- [ ] Lander interior (VME, CPU, bus 1553).
- [ ] Rover de contexto.
- [ ] Ciudad de tareas, cerrojo, anillos.
- [x] Texturas de código/terminal generadas desde el demo real.
- [ ] Paneles de código/terminal.

### 12.3. Animación
- [ ] Planos 1–5 (actos I–II).
- [ ] Planos 6–10 (acto III).
- [ ] Planos 11–12 (acto IV).
- [ ] Planos 13–15 (acto V).
- [ ] Revisión de continuidad y transiciones.

### 12.4. Render
- [x] Frame de prueba y medición (escena base de I0).
- [ ] Draft 720p de los 15 planos.
- [ ] Corrección de iluminación y cámara.
- [ ] Render final 1080p por planos.
- [ ] Codificación y verificación con ffprobe.

### 12.5. Postproducción
- [ ] Montaje final 2:45–3:00.
- [ ] Revisión sin narración: ¿se entiende la cadena causal?
- [ ] Revisión con narración: ¿sobra o falta algo?
- [ ] Exportar MP4 final.

### 12.6. Entrega
- [ ] MP4 en `out/`.
- [ ] `.blend` y scripts.
- [ ] `STORYBOARD.md` y `NARRACION.md`.
- [ ] Actualizar `../AGENTS.md` y commit.

## 13. Criterios de aceptación

### 13.1. Del film
1. MP4 1920 × 1080, 24 fps, 2:45–3:00, H.264, sin audio.
2. La cadena causal de §3.2 se entiende sin texto.
3. Con PIP on, la misma cadena termina en ciclo verde.
4. El código y la terminal muestran la salida real del demo C.
5. No hay afirmaciones factuales sin fuente en §3.1/§4.
6. El film se reconstruye con un comando y una semilla fija.
7. El tiempo de render está documentado.

### 13.2. Por acto
- **I:** Marte, lander y rover reconocibles; los sensores se entienden.
- **II:** la disección revela el CPU y el bus; la ciudad de tareas muestra la
  jerarquía.
- **III:** se ve la toma del cerrojo, la expropiación, el bloqueo, el deadline y
  el reset.
- **IV:** el código es legible y el demo reproduce el error.
- **V:** la herencia de prioridad se ve y el ciclo termina en verde.

### 13.3. Del demo C
- `make test` pasa.
- `run-pip-off` imprime `WATCHDOG: RESET`.
- `run-pip-on` imprime `OK`.
- Sin privilegios de root.
- Determinista.

## 14. Riesgos

| Riesgo | Mitigación |
| :--- | :--- |
| Render lento | Frame de prueba; 720p; Workbench; render nocturno |
| EEVEE headless falla | Workbench o Cycles CPU |
| Película muda confusa | Narración en vivo; prueba con alguien externo |
| Deriva factual | Storyboard con fuente por plano |
| Scope creep | Congelar features el 22/11 |
| Disco lleno | Render por secuencias; borrar frames intermedios |
| Demo C ausente | Construirlo antes de los planos 11–12 |

## 15. Protocolo para agentes

1. Leer este archivo y `../AGENTS.md` antes de tocar nada.
2. No modificar `../main.tex`, `../references.bib`, `../fuentes/` ni `../entornoRTOS/`
   salvo que la tarea lo requiera.
3. No añadir audio ni texto no previsto.
4. Usar semilla fija y rutas relativas.
5. Actualizar §10, §11 y §12 al cerrar cada turno.
6. Actualizar `../AGENTS.md` (§8.3 y §8.4) porque es la fuente global.
7. Si el disco contradice este documento, prevalece el disco.
8. No renderizar el film completo hasta que el animatic esté aprobado.
9. No inventar código, salidas ni tiempos de VxWorks.
10. Commit después de cada milestone.

## 16. Primeros pasos

1. Escribir `STORYBOARD.md` derivado de §4.
2. Escribir `NARRACION.md` con el guion en vivo.
3. Construir un animatic de 15–20 s: terreno, silueta del lander, cámara que
   se acerca, ciudad de tareas y cerrojo.
4. Renderizar a 720p con pocas muestras y revisar el lenguaje visual.
5. Construir `../entornoRTOS/` y verificar `make test`.
6. Solo después, modelar el lander en detalle.

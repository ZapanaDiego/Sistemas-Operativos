# NARRACIÓN — Mars Pathfinder: la inversión de prioridades

> **Uso:** guion de narración en vivo para la exposición. El film es mudo; este
> texto **no** se reproduce dentro del film.
>
> **Duración:** 2:45–3:00. **Ritmo objetivo:** 135–145 palabras por minuto.
> **Extensión:** 387 palabras (~2:46 a 140 ppm, con pausas ~2:55).
> **Fuente:** hechos de `AGENTS.md` §3.1; secuencia de §4; corrección de Reeves
> 1999. No se añaden afirmaciones sin ancla.

## 1. Mapa de bloques

| Bloque | Plano | Tiempo | Palabras | Cue visual |
| :---: | :---: | :--- | :---: | :--- |
| N1 | 1 | 0:00–0:12 | 25 | amanecer en Ares Vallis |
| N2 | 2 | 0:12–0:25 | 23 | mástil ASI/MET y pulsos |
| N3 | 3 | 0:25–0:38 | 27 | carcasa transparente y chasis |
| N4 | 4 | 0:38–0:52 | 28 | bus 1553 y CPU |
| N5 | 5 | 0:52–1:05 | 26 | ciudad de tareas |
| N6 | 6 | 1:05–1:18 | 23 | `ASI/MET` toma el cerrojo |
| N7 | 7 | 1:18–1:32 | 33 | tareas medias expropian |
| N8 | 8 | 1:32–1:45 | 30 | `bc_dist` bloqueada |
| N9 | 9 | 1:45–1:58 | 22 | anillo de deadline |
| N10 | 10 | 1:58–2:08 | 26 | watchdog y reinicios |
| N11 | 11 | 2:08–2:20 | 24 | panel de código |
| N12 | 12 | 2:20–2:30 | 26 | terminal: RESET y OK |
| N13 | 13 | 2:30–2:40 | 26 | herencia de prioridad |
| N14 | 14 | 2:40–2:50 | 22 | ciclo verde |
| N15 | 15 | 2:50–3:00 | 26 | pullback y fade |

## 2. Guion

### N1 — Ares Vallis (0:00–0:12)

Cuatro de julio de 1997: Mars Pathfinder aterriza en Ares Vallis. Dos días
después, Sojourner rueda sobre Marte. El fallo no ocurrirá en el rover.

### N2 — ASI/MET (0:12–0:25)

El lander lleva ASI/MET. Sus sensores miden viento, temperatura y presión. Cada
dato entra al ordenador de vuelo, un VxWorks de prioridad fija.

### N3 — Disección (0:25–0:38)

El chasis VME sostiene las placas. El ordenador de vuelo gobierna el lander y
sirve de repetidor al rover. Sus tareas deben cumplir plazos de tiempo real.

### N4 — CPU y 1553 (0:38–0:52)

Cada 125 milisegundos, el bus 1553 mueve datos entre la CPU y los instrumentos.
Es el reloj del sistema; si una tarea crítica no termina, el ciclo falla.

### N5 — Ciudad de tareas (0:52–1:05)

La altura es la prioridad: `bc_sched` arriba, planifica el ciclo; `bc_dist`
tercera, distribuye datos; `ASI/MET` abajo, recoge sensores. Entre ellas, tareas
medias de comunicaciones e imagen.

### N6 — El cerrojo (1:05–1:18)

`ASI/MET` llama a `select()` y toma el mutex interno. Ese cerrojo protege la
sección crítica. Lo sostiene, y `bc_dist` necesita ese mismo recurso.

### N7 — Expropiación (1:18–1:32)

Despiertan las tareas medias. Tienen más prioridad que `ASI/MET` y la expropian.
El azul sale de la CPU, pero retiene el mutex. Es una inversión de prioridades:
la baja bloquea a la alta.

### N8 — Bloqueo (1:32–1:45)

`bc_dist` llega al cerrojo y espera. El sistema no se ha caído: VxWorks hace lo
que se le pidió. Pero la cadena crítica está detenida y el ciclo sigue corriendo.

### N9 — Deadline (1:45–1:58)

El anillo se llena; el bus 1553 se atasca. Los 125 milisegundos se cumplen sin
que `bc_dist` termine. El plazo está perdido.

### N10 — Watchdog (1:58–2:08)

`bc_sched` lo detecta; el watchdog reinicia. Y se repite. Los datos en RAM se
conservan si no se pierde la alimentación, pero la misión se retrasa.

### N11 — Código (2:08–2:20)

`select()` toma el mutex; `pipe()` mueve datos; `semMCreate` crea el mutex.
Falta `SEM_INVERSION_SAFE`. Sin ella, el dueño no hereda la prioridad del que
espera.

### N12 — Terminal (2:20–2:30)

El demo reproduce el patrón. Con la herencia desactivada, la traza termina en
`WATCHDOG: RESET`. Con `SEM_INVERSION_SAFE`, `ASI/MET` hereda prioridad y el
ciclo termina en `OK`.

### N13 — Corrección (2:30–2:40)

La corrección: cuando `bc_dist` espera, `ASI/MET` hereda su prioridad, sube sobre
las tareas medias, completa la sección crítica y libera el cerrojo. El bloqueo
queda acotado.

### N14 — Ciclo verde (2:40–2:50)

`bc_dist` termina antes del siguiente ciclo. El anillo se pone verde, el bus
fluye y el watchdog calla. Misma cadena, otra opción.

### N15 — Cierre (2:50–3:00)

Pathfinder siguió operando. El fallo no fue del rover ni una caída del RTOS: fue
una inversión de prioridades no acotada, una lección que sigue vigente.

## 3. Indicaciones de lectura

- **Ritmo:** 135–145 palabras por minuto; dejar respirar los planos 9 y 10.
- **Énfasis:** «inversión de prioridades», «mutex interno», «125 milisegundos»,
  «watchdog», «herencia de prioridad».
- **Pausas:** después de N5 (entrada a la ciudad), después de N9 (deadline) y
  antes de N13 (corrección).
- **No leer:** el texto no debe sonar a lista de datos; el film ya muestra la
  cadena causal.
- **Ajuste:** si la exposición recorta el film, mantener N1, N6–N10 y N13–N15.

## 4. Límites de honestidad

1. El fallo ocurrió en el ordenador de vuelo del lander, no en Sojourner.
2. VxWorks no se cayó: el watchdog reinició el sistema al detectar el plazo
   incumplido.
3. Los datos en RAM se conservan si no se pierde la alimentación; hubo retraso
   de actividades, no una pérdida inevitable.
4. El demo C es un modelo del patrón, no una emulación de VxWorks.
5. La ciudad de tareas, el cerrojo y los anillos son metáforas visuales
   declaradas, no hardware real.
6. No se afirma que el código mostrado sea el código original de VxWorks.

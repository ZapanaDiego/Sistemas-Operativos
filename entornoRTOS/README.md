# entornoRTOS — Simulación C + ensamblador del fallo de Mars Pathfinder

Entorno RTOS determinista que reconstruye la **inversión de prioridades no
acotada** del mutex interno de `select()` en el ordenador de vuelo del lander
Mars Pathfinder, el incumplimiento del ciclo 1553 de 125 ms y el reset del
watchdog. Incluye un **visualizador HTML** que muestra, en paralelo, el código C,
el ensamblador y el estado de las tareas.

> **Aviso de honestidad:** esto **no es VxWorks**. Es una reconstrucción propia
> del mecanismo, escrita en C11 y ensamblador x86-64. El código fuente histórico
> de VxWorks es propietario y no está disponible. No es una emulación bit a bit
> ni usa telemetría de vuelo.
>
> El fallo ocurrió en el **ordenador de vuelo del lander**, no en el rover
> Sojourner. El rover es contexto de misión, no el objeto de la simulación.

## Requisitos

- Linux x86-64.
- GCC o Clang con C11 y GNU as.
- GNU Make.
- Navegador para abrir el visualizador (opcional).

Sin dependencias externas. Sin `root`. Sin reloj de pared ni aleatoriedad.

## Build

```bash
make
```

## Verificar

```bash
make test
```

Debe imprimir `PASS` en las pruebas de firmas, bus y contexto, y `determinism:
PASS`. Resultados actuales:

| Escenario | PIP | Mutex | Reinicios | Bloqueo máx. | Fallos de plazo |
| :--- | :---: | :--- | :---: | :---: | :---: |
| S0 | off | compartido | 0 | 17.000 ms | 0 |
| S1 | off | compartido | 3 | 125.000 ms | 3 |
| S2 | on | compartido | 0 | 5.000 ms | 0 |
| S3 | off | separados | 0 | 3.000 ms | 0 |

El bloqueo de S0 es 17 ms porque la sección crítica de `select()` se modela
completa (3 ms de CPU) y `bc_dist` espera a que `ASI/MET` termine. Sigue muy por
debajo del plazo de 125 ms.

## Ejecutar un escenario

```bash
make run-pip-off     # S1 -> out/s1_pip_off.txt
make run-pip-on      # S2 -> out/s2_pip_on.txt
make all-scenarios   # S0-S3
```

La salida por consola termina en `WATCHDOG: RESET` para S1 y en `OK` para S0,
S2 y S3.

## Visualizador

```bash
make view
```

Abre `out/viewer.html` en el navegador. El visualizador permite:

- recorrer la línea de tiempo de 0 a 2 s;
- ver el código C y la línea que produjo cada evento;
- ver el ensamblador del cambio de contexto y la desensamblación de la función
  actual;
- consultar tareas, prioridades base/efectivas, estados y esperas;
- consultar el dueño y los waiters del mutex;
- ver el ciclo 1553, los reinicios y los fallos de plazo;
- filtrar los eventos `SWITCH` para no saturar el registro.

Se puede abrir directamente en un punto concreto:

```text
out/viewer.html?scenario=S1&t=500100
```

El parámetro `t` está en microsegundos simulados. `make view` genera
`out/viewer.html` y los archivos `out/s0_data.js` … `out/s3_data.js`.

## Mecanismo

Sin PIP (S1):

1. `ASI/MET` (prioridad 7) toma el mutex de `select()` a los 499 ms.
2. `med_3` (prioridad 6) despierta a los 507,1 ms y ejecuta una ráfaga de CPU.
3. `bc_dist` (prioridad 3) llega al mismo mutex y se bloquea a los 500,1 ms.
4. `bc_sched` (prioridad 1) ve que `bc_dist` no terminó a los 625 ms y reinicia.
5. El patrón se repite a 1,125 s y 1,625 s: 3 reinicios.

Con PIP (S2):

1. `bc_dist` se bloquea en el mutex.
2. `ASI/MET` hereda la prioridad 3.
3. Corre por encima de las tareas medias, termina la sección crítica y libera.
4. `bc_dist` completa antes del siguiente ciclo: 0 reinicios.

S3 es el control: `ASI/MET` y `bc_dist` usan mutex separados, por lo que no hay
inversión.

## Arquitectura

```text
entornoRTOS/
├── AGENTS.md
├── README.md
├── Makefile
├── include/
│   ├── config.h
│   ├── rtos.h
│   ├── sem.h
│   ├── pipe.h
│   ├── bus1553.h
│   ├── vxworks_like.h
│   ├── flight_sw.h
│   ├── trace.h
│   └── scenario.h
├── src/
│   ├── switch.S       # cambio de contexto x86-64
│   ├── rtos.c         # scheduler, pilas, tiempo simulado
│   ├── sem.c          # mutex, colas, PIP
│   ├── pipe.c         # pipe + select()
│   ├── bus1553.c      # ciclo 8 Hz y bus_sem
│   ├── flight_sw.c    # tareas de vuelo
│   ├── trace.c        # traza de texto + datos del visualizador
│   ├── scenario.c
│   └── main.c
├── tests/
│   ├── test_signatures.c
│   ├── test_bus.c
│   ├── test_context.c
│   └── test_determinism.sh
├── viewer/
│   └── viewer.html
└── out/
```

### Cambio de contexto

`src/switch.S` implementa `rtos_switch(void **old_sp, void *new_sp)` para
x86-64 System V. Guarda `rbp`, `rbx`, `r12`–`r15`, cambia el stack pointer y
restaura los registros de la tarea destino. La primera ejecución de una tarea
entra por `task_trampoline` mediante un `ret` preparado en su pila inicial.

La pila inicial se alinea a 16 bytes. El layout es:

```text
[sp]      r15
          r14
          r13
          r12
          rbx
          rbp
          return address -> task_trampoline
          padding
```

### Bus 1553

`bus1553.c` encapsula el ciclo de 8 Hz: `bc_sched` llama a `bus1553_cycle()` cada
125 ms y `bc_dist` espera con `bus1553_wait()`. El semáforo binario `bus_sem`
representa la disponibilidad del bus.

### Watchdog

`bc_sched` comprueba `bc_dist_done` al inicio de cada ciclo. Si es 0, registra
`MISS`, llama a `rtos_reset()` y cuenta el reinicio. El reset libera los mutex,
despierta a los bloqueados y descarta la liberación pendiente del dueño anterior
(evento `UNWIND`), porque el sistema reiniciado ya no reconoce ese lock.

## Traza

Cada escenario produce:

- `out/sX_pip_*.txt`: traza legible con `SPAWN`, `LOCK`, `WAIT`, `INHERIT`,
  `MISS`, `RESET`, `UNWIND` y `SUMMARY`.
- `out/sX_data.js`: datos estructurados para el visualizador (eventos,
  instantáneas de tareas y mutex, fuentes C, `switch.S` y desensamblación).

Los eventos `SWITCH`, `BUS` y las instantáneas periódicas se guardan solo en
`out/sX_data.js` para no saturar la traza de texto.

## Pruebas

| Prueba | Qué verifica |
| :--- | :--- |
| `test_signatures` | S0–S3: 0, 3, 0, 0 reinicios |
| `test_bus` | El ciclo 1553 completa 15 ciclos en 2 s |
| `test_context` | Dos tareas se alternan; los stacks no se corrompen; el `ret` inicial funciona |
| `test_determinism.sh` | Dos ejecuciones de S1 producen traza y datos idénticos |

## Mapa VxWorks → modelo

| VxWorks | Modelo |
| :--- | :--- |
| `taskSpawn` | `task_spawn` |
| `taskDelay` | `task_delay` |
| `semMCreate(SEM_Q_PRIORITY)` | `sem_mcreate(name, 0)` |
| `semMCreate(... \| SEM_INVERSION_SAFE)` | `sem_mcreate(name, 1)` |
| `semTake` / `semGive` | `sem_take` / `sem_give` |
| `pipe` | `pipe_create` / `pipe_write` / `pipe_read` |
| `select()` | `rtos_select(mutex, pipe, ...)` |
| watchdog | chequeo de `bc_sched` |

## Límites

- Modelo determinista, no emulación de VxWorks.
- Tiempos sintéticos calibrados, no telemetría.
- `cpu_work()` modela tiempo de CPU en pasos de 50 µs; no ejecuta instrucciones
  reales de la CPU histórica.
- El visualizador es **a nivel de evento**, no un depurador instrucción por
  instrucción.
- No modela caché, pipeline, protocolo 1553 detallado ni física de la misión.
- El reset no reinicia los contextos de las tareas; libera recursos y descarta
  la liberación pendiente del dueño anterior. Es una abstracción declarada.
- La herencia de prioridad se propaga a los esperadores directos; no se modela
  una cadena transitiva de mutex anidados.
- El cambio de contexto guarda los registros callee-saved de System V; no guarda
  estado FPU/SSE porque las tareas no lo modifican.
- Solo x86-64 System V.

## Fuentes

- Reeves, G. E. (1997). *What really happened on Mars?*
- Reeves, G. E. (1999). *Priority Inversion: How We Found It, How We Fixed It.*
- NASA / NSSDC: datos de la misión.

Los detalles y anclas están en `../AGENTS.md` §4.1 y §4.6.

# entornoRTOS — Modelo ejecutable del fallo de Mars Pathfinder

Entorno RTOS simulado en C11 que aloja el software de vuelo del lander Mars
Pathfinder y reproduce la inversión de prioridades no acotada del mutex interno
de `select()`, el incumplimiento del ciclo 1553 y el reset del watchdog.

> **Aviso de honestidad:** esto **no es VxWorks**. Es un modelo determinista del
> mecanismo, escrito en C con una API de estilo VxWorks. No es una emulación bit
> a bit ni usa telemetría de vuelo.

## Requisitos

- GCC o Clang con C11.
- glibc con `ucontext.h`.
- GNU Make.
- Linux (probado en glibc 2.44).

Sin dependencias externas. Sin `root`.

## Build

```bash
make
```

## Ejecutar un escenario

```bash
make run-pip-off     # S1: PIP off, carga alta -> out/s1_pip_off.txt
make run-pip-on      # S2: PIP on,  carga alta -> out/s2_pip_on.txt
make all-scenarios   # S0-S3
```

También:

```bash
./entornoRTOS --scenario s1 --out out/s1_pip_off.txt
```

La salida por consola termina en `WATCHDOG: RESET` para S1 y en `OK` para S0,
S2 y S3.

## Verificar

```bash
make test
```

Debe imprimir `PASS` y verificar:

| Escenario | PIP | Mutex | Esperado |
| :--- | :---: | :--- | :--- |
| S0 | off | compartido | 0 reinicios |
| S1 | off | compartido | ≥ 1 reinicio |
| S2 | on | compartido | 0 reinicios |
| S3 | off | separados | 0 reinicios |

## Qué se simula

- Scheduler de prioridad fija con tareas cooperativas `ucontext`.
- Tiempo simulado en microsegundos; sin wall-clock.
- Mutex con `SEM_INVERSION_SAFE` opcional.
- `select()` con su mutex interno y una sección crítica de 3 ms.
- `pipe` de 4096 bytes.
- Watchdog de `bc_sched` cada 125 ms.
- Tareas: `bc_sched` (1), `bc_dist` (3), `med_1..3` (4–6), `ASI/MET` (7),
  `tExec` (99).

## El mecanismo

Sin PIP:

1. `ASI/MET` (prioridad 7) toma el mutex de `select()` a los 499 ms.
2. `med_3` (prioridad 6) despierta a los 500 ms y la expropia durante 150 ms.
3. `bc_dist` (prioridad 3) llega al mismo mutex y se bloquea.
4. A los 625 ms, `bc_sched` (prioridad 1) ve que `bc_dist` no terminó y reinicia.

Con PIP:

1. `bc_dist` se bloquea en el mutex.
2. `ASI/MET` hereda la prioridad 3.
3. Corre por encima de `med_3` (6), termina la sección crítica y libera.
4. `bc_dist` completa antes del próximo ciclo.

La corrección es una opción de configuración:

```c
select_mutex = semMCreate("select_mutex",
    SEM_Q_PRIORITY | SEM_INVERSION_SAFE);
```

## Estructura

```
entornoRTOS/
├── AGENTS.md
├── README.md
├── Makefile
├── include/
│   ├── config.h
│   ├── rtos.h
│   ├── sem.h
│   ├── pipe.h
│   ├── vxworks_like.h
│   ├── flight_sw.h
│   ├── trace.h
│   └── scenario.h
├── src/
│   ├── rtos.c
│   ├── sem.c
│   ├── pipe.c
│   ├── flight_sw.c
│   ├── trace.c
│   ├── scenario.c
│   └── main.c
├── tests/
│   └── test_signatures.c
└── out/
```

## Mapa VxWorks → modelo

| VxWorks | Modelo |
| :--- | :--- |
| `taskSpawn` | `task_spawn` |
| `taskDelay` | `task_delay` |
| `semMCreate(SEM_Q_PRIORITY)` | `sem_mcreate(name, 0)` |
| `semMCreate(... \| SEM_INVERSION_SAFE)` | `sem_mcreate(name, 1)` |
| `semTake` / `semGive` | `sem_take` / `sem_give` |
| `semBCreate` / `semTake` / `semGive` | `sem_bcreate` / `sem_take` / `sem_give` |
| `pipe` | `pipe_create` / `pipe_write` / `pipe_read` |
| `select()` | `rtos_select(mutex, pipe, ...)` |
| watchdog | chequeo de `bc_sched` |

## Integración con el film

`../simulacion3D/` usa:

- `out/s1_pip_off.txt` para la traza del fallo.
- `out/s2_pip_on.txt` para la traza de la corrección.
- `src/flight_sw.c` e `include/vxworks_like.h` para las texturas de código.

## Límites

- Modelo determinista, no emulación de VxWorks.
- Tiempos sintéticos calibrados, no telemetría.
- `ucontext` es cooperativo; la preeminencia se simula en `cpu_work()`.
- No modela caché, pipeline, protocolo 1553 detallado ni física de la misión.
- El reset libera mutex y despierta bloqueados; no reinicia los contextos de las
  tareas, porque el objetivo es contar y visualizar reinicios, no emular el
  arranque completo.

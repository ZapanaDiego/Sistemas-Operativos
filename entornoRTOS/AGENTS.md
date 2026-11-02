# AGENTS.md — Entorno RTOS y código de fallo de Mars Pathfinder

> **Estado:** vivo. Leer al iniciar. Actualizar al cerrar cada turno.
> **Última actualización:** 2026-11-02 · OpenCode (DeepSeek V4.1 Flash)
> **Documento maestro del repositorio:** `../AGENTS.md`.
> **Este archivo es el contrato local de `entornoRTOS/`.**

## 0. Regla de actualización (R0 local)

Todo agente que cree, modifique, mueva o elimine un archivo en `entornoRTOS/` debe:

1. Actualizar la bitácora §11.
2. Actualizar el inventario §10.
3. Ajustar los checkboxes §12.
4. Actualizar el estado §1.
5. Actualizar `../AGENTS.md` (§8.3 bitácora y §8.4 inventario), porque el repositorio es la fuente de verdad global.

Si el disco contradice este documento, prevalece el disco y se corrige el documento.

## 1. Estado actual

- **Fase:** implementación completa y verificada.
- **Entregable:** `entornoRTOS` compilable + `make test` con S0–S3 (PASS).
- **Próximo hito:** generar las texturas de código/terminal para el film.
- **Bloqueos:** ninguno.
- **Riesgo principal:** mantener el determinismo al ajustar parámetros.
- **Alcance:** solo el entorno RTOS y el software de vuelo. El film vive en `../simulacion3D/`.

### 1.1. Resultados verificados

| Escenario | Reinicios | Bloqueo máx. | Fallos de plazo |
| :--- | :---: | :---: | :---: |
| S0 | 0 | 15.000 ms | 0 |
| S1 | 3 | 125.000 ms | 3 |
| S2 | 0 | 4.900 ms | 0 |
| S3 | 0 | 3.000 ms | 0 |

`make test` imprime `PASS`. `make run-pip-off` imprime `WATCHDOG: RESET`;
`make run-pip-on` imprime `OK`. Las trazas son deterministas.

## 2. Objetivo y alcance

### 2.1. Objetivo

Construir un **entorno RTOS simulado y determinista** en C11 que aloje el
software de vuelo del lander Mars Pathfinder y reproduzca, paso a paso, la
inversión de prioridades no acotada del mutex interno de `select()`, el
incumplimiento del ciclo 1553 y el reset del watchdog, además de su corrección
con herencia de prioridad.

### 2.2. Entregable

- `entornoRTOS`: binario que ejecuta un escenario y escribe una traza.
- `test_signatures`: verifica S0–S3.
- `out/s0_pip_off.txt`, `out/s1_pip_off.txt`, `out/s2_pip_on.txt`,
  `out/s3_control.txt`.
- Código fuente documentado y reproducible.
- `README.md` con build, run, escenarios y límites.

### 2.3. Decisiones cerradas

| Decisión | Valor |
| :--- | :--- |
| Lenguaje | C11 |
| Concurrencia | `ucontext` cooperativo (POSIX/glibc) |
| Build | GNU Make + GCC/Clang |
| Dependencias | Ninguna externa |
| Privilegios | Ninguno; sin `root` |
| Determinismo | Total; tiempo simulado, sin wall-clock |
| Escenarios | S0–S3 |
| Código | Identificadores en inglés; comentarios y docs en español |
| Relación con VxWorks | Modelo, no emulación |

### 2.4. Incluye

- RTOS modelo: scheduler de prioridad fija, tareas, tiempo simulado.
- Mutex con y sin `SEM_INVERSION_SAFE`.
- `pipe`, `fd_set` y `select()` con su mutex interno.
- Watchdog de `bc_sched` cada 125 ms.
- Software de vuelo: `bc_sched`, `bc_dist`, `ASI/MET`, `med_1..3`, `tExec`.
- Traza legible y resumen de métricas.
- Pruebas S0–S3.

### 2.5. No incluye

- VxWorks real, su código fuente o su binario.
- Emulación bit a bit, caché, pipeline o protocolo 1553 detallado.
- Física de la misión o telemetría de vuelo.
- El film 3D (`../simulacion3D/`) o el artículo.
- Audio, texto narrativo o interfaz gráfica.

## 3. Hechos y fuentes

### 3.1. Hechos

| Hecho | Fuente |
| :--- | :--- |
| El fallo ocurrió en el ordenador de vuelo del lander, no en el rover | Reeves 1997 |
| `bc_sched` es la tarea de mayor prioridad (salvo `tExec`) | Reeves 1997 |
| `bc_dist` es la tercera prioridad | Reeves 1997 |
| `ASI/MET` es la tarea de menor prioridad | Reeves 1997 |
| Ciclo del bus 1553: 8 Hz = 125 ms | Reeves 1997 |
| El mutex interno de `select()` no tenía herencia de prioridad | Reeves 1997/1999 |
| Las tareas medias expropian a `ASI/MET` y bloquean a `bc_dist` | Reeves 1997 |
| El watchdog detecta el plazo incumplido y reinicia | Reeves 1997 |
| Corrección: `semMCreate(SEM_Q_PRIORITY \| SEM_INVERSION_SAFE)` | Reeves 1999 |
| Sin pérdida de datos si se mantiene la alimentación | Reeves 1997 |

### 3.2. Cadena causal

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
3. No decir "pérdida de datos" sin matizar.
4. No presentar el modelo como VxWorks real; es una reconstrucción del mecanismo.
5. Los tiempos son parámetros de calibración declarados, no telemetría.
6. La corrección es una opción de configuración, no un cambio del planificador.

## 4. Arquitectura del entorno

### 4.1. Stack

- C11, `-std=c11 -O2 -Wall -Wextra -Werror -D_GNU_SOURCE`.
- `ucontext` de glibc para tareas cooperativas.
- Make para build/test/run.
- `gdb` para depuración; `-fsanitize=address,undefined` opcional.
- Sin dependencias externas.

### 4.2. Estructura

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
    └── traces/
```

### 4.3. Scheduler y tiempo

- Tiempo simulado en microsegundos (`uint64_t`).
- Tareas cooperativas con `ucontext`; el scheduler elige la de mayor
  prioridad efectiva.
- `cpu_work(us)` avanza el tiempo en pasos de 50 µs y comprueba si hay una
  tarea de mayor prioridad lista; si la hay, cede el control.
- `task_delay(us)` duerme la tarea hasta `now + us`.
- Si no hay tareas listas, el scheduler avanza al siguiente despertar.
- `sim_stop` termina la simulación a los 2 s simulados.
- Sin wall-clock, sin números aleatorios.

### 4.4. Tareas

| Tarea | Prioridad | Período / activación | WCET | Rol | Recurso |
| :--- | :---: | :--- | :---: | :--- | :--- |
| `sim_stop` | 0 | 2 s | — | Termina la simulación | — |
| `bc_sched` | 1 | 125 ms | 100 µs | Ciclo 1553 y watchdog | — |
| `bc_dist` | 3 | Tras el bus | 2 ms | Distribuye datos; `select()`/`pipe()` | `select_mutex` |
| `med_1` | 4 | 20 ms | 3 ms | Carga de CPU | — |
| `med_2` | 5 | 25 ms | 4 ms | Carga de CPU | — |
| `med_3` | 6 | 500 ms | 150 ms (alta) / 5 ms (baja) | Ráfaga de compresión | — |
| `ASI/MET` | 7 | 500 ms (fase 499 ms) | 0,4 ms + 3 ms de `select()` | Sensores | `select_mutex` |
| `tExec` | 99 | — | — | CPU ociosa | — |

Los valores son parámetros de calibración. `med_3` es la carga que garantiza
la expropiación en S1; en S0 se reduce a 5 ms.

### 4.5. Mutex y herencia de prioridad

- `sem_t` con dueño, contador de recursión, cola de espera por prioridad y
  bandera `pip`.
- Sin PIP: el dueño conserva su prioridad base.
- Con PIP: al bloquearse una tarea, el dueño hereda la mayor prioridad de sus
  esperadores; al liberar, se recalcula su prioridad efectiva.
- La prioridad efectiva es la que usa el scheduler.
- La corrección es `semMCreate(SEM_Q_PRIORITY | SEM_INVERSION_SAFE)`.

### 4.6. `pipe` y `select()`

- `pipe_t` con buffer circular de 4096 bytes.
- `rtos_select(mutex, pipe, nfds, readfds, writefds, timeout)` modela
  `select()`:
  1. Toma el mutex interno.
  2. Ejecuta la sección crítica (`cpu_work(SELECT_WCET_US)`), donde puede ser
     expropiada.
  3. Escanea los descriptores.
  4. Libera el mutex.
- `bc_dist` y `ASI/MET` comparten el mutex en S0–S2. En S3 usan mutex
  separados (control).

### 4.7. Watchdog

- `bc_sched` despierta cada 125 ms.
- Si `bc_dist_done == 0`, registra `MISS`, incrementa el contador y llama a
  `rtos_reset()`.
- `rtos_reset()` libera mutex, despierta bloqueados y permite que el sistema
  continúe; el reinicio se cuenta y se registra.
- No se pierde el tiempo simulado; la misión continúa.

## 5. Código que falló

### 5.1. `src/flight_sw.c`

El software de vuelo se escribe como código secuencial:

```c
/* bc_dist: la tarea que queda bloqueada */
void bc_dist(void) {
    for (;;) {
        semTake(bus_sem, WAIT_FOREVER);
        rtos_select(dist_mutex, pipe, pipe->id + 1, NULL, &wfds, WAIT_FOREVER);
        pipe_write(pipe, packet, sizeof(packet));
        cpu_work(BC_DIST_WCET_US);
        bc_dist_done = 1;
    }
}

/* ASI/MET: la tarea de baja prioridad que retiene el mutex de select() */
void asi_met(void) {
    uint64_t next = ASI_PHASE_US;
    for (;;) {
        wait_until(next);
        next += ASI_PERIOD_US;
        rtos_select(asi_mutex, pipe, pipe->id + 1, &rfds, NULL, WAIT_FOREVER);
        pipe_read(pipe, data, sizeof(data));
    }
}

/* bc_sched: ciclo de 1553 y watchdog */
void bc_sched(void) {
    uint64_t next = CYCLE_US;
    for (;;) {
        wait_until(next);
        next += CYCLE_US;
        if (!bc_dist_done) {
            trace_event("MISS", rtos_current(), "bc_dist");
            rtos_reset();
            bc_dist_done = 1;
        }
        bc_dist_done = 0;
        semGive(bus_sem);
        cpu_work(BC_SCHED_WCET_US);
    }
}
```

### 5.2. La corrección

```c
select_mutex = semMCreate("select_mutex",
    SEM_Q_PRIORITY | SEM_INVERSION_SAFE);
```

Sin `SEM_INVERSION_SAFE`, `ASI/MET` no hereda prioridad. Con la opción,
`ASI/MET` hereda la prioridad 3 de `bc_dist`, corre por encima de `med_3` (6),
libera el mutex y `bc_dist` termina antes del próximo ciclo.

### 5.3. Mapa VxWorks → modelo

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

## 6. Escenarios S0–S3

| Escenario | PIP | Carga | Mutex | Esperado |
| :--- | :---: | :--- | :---: | :--- |
| S0 | off | baja (`med_3` 5 ms) | compartido | 0 reinicios |
| S1 | off | alta (`med_3` 150 ms) | compartido | ≥ 1 reinicio |
| S2 | on | alta | compartido | 0 reinicios |
| S3 | off | alta | separados | 0 reinicios |

`make test` verifica las cuatro firmas. S3 es el control: sin recurso
compartido, no hay inversión.

## 7. Traza y salidas

Formato:

```
# Pathfinder RTOS model — scenario S1
# pip=0 shared=1 duration=2.000000s
[0.000000] SPAWN ...
[0.499000] LOCK  ASI/MET prio=7 select_mutex
[0.500000] WAIT  bc_dist prio=3 select_mutex
[0.625000] MISS  bc_sched prio=1 bc_dist
[0.625000] RESET bc_sched prio=1 watchdog
# SUMMARY resets=3 max_block_ms=125.000 deadline_misses=3
```

Salidas:
- `out/s0_pip_off.txt`
- `out/s1_pip_off.txt`
- `out/s2_pip_on.txt`
- `out/s3_control.txt`

La traza es determinista y se usa como textura en los planos 11–12 de
`../simulacion3D/`.

## 8. Build, run y test

```bash
make                 # compila entornoRTOS
make test            # S0–S3
make run-pip-off     # S1 → out/s1_pip_off.txt
make run-pip-on      # S2 → out/s2_pip_on.txt
make all-scenarios   # S0–S3
make clean
```

Sin `sudo`. Sin variables de entorno especiales.

## 9. Integración con `simulacion3D`

- `../simulacion3D/` consume `out/s1_pip_off.txt` y `out/s2_pip_on.txt`.
- El código de `src/flight_sw.c` y `include/vxworks_like.h` se usa para
  generar las texturas de código del film.
- El film no modifica este directorio; solo lee sus salidas.
- Si cambia el formato de la traza, actualizar `../simulacion3D/AGENTS.md`.

## 10. Inventario

| Ruta | Tipo | Propósito | Estado |
| :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento | Contrato local | Activo |
| `README.md` | Documento | Build, run, escenarios y límites | Completo |
| `Makefile` | Build | Compilar, testear, ejecutar | Completo |
| `include/` | Cabeceras | API del RTOS y del software de vuelo | Completo |
| `src/` | C | Scheduler, mutex, pipe/select, vuelo, traza | Completo |
| `tests/` | C | S0–S3 | Completo |
| `out/` | Salidas | Trazas para el film | Completo |

## 11. Bitácora

| Fecha | Agente | Archivos | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `Makefile`, `include/`, `src/`, `tests/`, `out/` | Implementación completa del entorno RTOS: scheduler `ucontext`, mutex/PIP, `select()`, software de vuelo, traza y pruebas S0–S3. | `make test` PASS; S1 3 reinicios; S2 0; trazas deterministas; `run-pip-off` RESET; `run-pip-on` OK. |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Creación del contrato local de `entornoRTOS/`. | Archivo creado. |

## 12. Checklist

- [x] Crear `entornoRTOS/AGENTS.md`.
- [x] Escribir `README.md` y `Makefile`.
- [x] Implementar tipos y configuración.
- [x] Implementar scheduler + `ucontext` + tiempo simulado.
- [x] Implementar mutex con/sin PIP.
- [x] Implementar `pipe` y `select()`.
- [x] Escribir `flight_sw.c`.
- [x] Implementar traza y `main`.
- [x] Implementar `tests/test_signatures.c`.
- [x] `make test` pasa S0–S3.
- [x] Generar `out/s0_pip_off.txt` … `out/s3_control.txt`.
- [x] Actualizar `../AGENTS.md` y `../simulacion3D/AGENTS.md`.
- [x] Commit.

## 13. Criterios de aceptación

1. `make` compila sin warnings con `-Wall -Wextra -Werror`.
2. `make test` pasa:
   - S0: 0 reinicios.
   - S1: ≥ 1 reinicio.
   - S2: 0 reinicios.
   - S3: 0 reinicios.
3. `make run-pip-off` imprime `WATCHDOG: RESET`.
4. `make run-pip-on` imprime `OK`.
5. Las salidas son deterministas: dos ejecuciones producen el mismo archivo.
6. No se usa `root`, wall-clock ni aleatoriedad.
7. La traza muestra `LOCK`, `WAIT`, `INHERIT`, `MISS`, `RESET` cuando
   corresponde.
8. El código es legible y mapea a VxWorks según §5.3.

## 14. Riesgos

| Riesgo | Mitigación |
| :--- | :--- |
| `ucontext` no disponible | glibc 2.44 lo tiene; fallback a máquina de estados si hiciera falta |
| La inversión no se reproduce | Ajustar `med_3` y las fases; el test lo detecta |
| Traza no determinista | Sin wall-clock ni random; semilla fija |
| Demasiados eventos | Traza concisa: solo eventos significativos |
| El reset deja estados inconsistentes | `rtos_reset()` libera mutex y despierta bloqueados |
| El film espera otro formato | Documentar el formato en §7 y en `README.md` |

## 15. Protocolo para agentes

1. Leer este archivo y `../AGENTS.md` antes de tocar nada.
2. No modificar `../simulacion3D/`, `../main.tex`, `../references.bib` ni
   `../fuentes/` salvo que la tarea lo requiera.
3. No añadir dependencias externas.
4. Mantener el determinismo: sin wall-clock, sin random, sin hilos reales.
5. Actualizar §10, §11 y §12 al cerrar cada turno.
6. Actualizar `../AGENTS.md` (§8.3 y §8.4).
7. Si el disco contradice este documento, prevalece el disco.
8. Commit después de cada milestone.

## 16. Primeros pasos

1. Escribir `README.md` y `Makefile`.
2. Implementar `include/config.h`, `rtos.h`, `sem.h`, `pipe.h`.
3. Implementar `src/rtos.c`, `sem.c`, `pipe.c`.
4. Implementar `src/flight_sw.c`, `trace.c`, `scenario.c`, `main.c`.
5. Implementar `tests/test_signatures.c`.
6. Compilar y ajustar hasta que S1 falle y S2 no.
7. Generar las salidas y actualizar los `AGENTS.md`.

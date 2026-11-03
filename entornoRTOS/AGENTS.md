# AGENTS.md — Entorno RTOS C + ensamblador

> **Estado:** vivo. Leer al iniciar. Actualizar al cerrar cada turno.
> **Última actualización:** 2026-11-02 · OpenCode (DeepSeek V4.1 Flash)
> **Documento maestro del repositorio:** `../AGENTS.md`.
> **Este archivo es el contrato local de `entornoRTOS/`.**
> **Alcance de este turno:** solo este directorio. No se modifica
> `../AGENTS.md`, `simulacion3D/`, `main.tex`, `references.bib` ni `fuentes/`.

## 0. Regla de actualización (R0 local)

Todo agente que cree, modifique, mueva o elimine un archivo en `entornoRTOS/` debe:

1. Actualizar la bitácora §11.
2. Actualizar el inventario §10.
3. Ajustar los checkboxes §12.
4. Actualizar el estado §1.

La actualización de `../AGENTS.md` (§8.3 y §8.4) queda **pendiente y fuera del
alcance autorizado** en este turno. Si el usuario lo autoriza, se hará en un
turno separado.

Si el disco contradice este documento, prevalece el disco y se corrige el
documento.

## 1. Estado actual

- **Fase:** implementación completa y verificada del entorno C + ensamblador y
  del visualizador HTML.
- **Entregable:** `entornoRTOS` (C11 + x86-64 asm), pruebas S0–S3 y
  `out/viewer.html`.
- **Próximo hito:** revisión y mejoras opcionales (PIP transitivo, visor a nivel
  de instrucción). No hay bloqueos.
- **Riesgo principal:** mantener la fidelidad del mecanismo al migrar a
  ensamblador y no confundir el modelo con VxWorks.
- **Alcance:** solo el entorno RTOS y su visualizador. El film y el artículo
  están fuera de este directorio y fuera de este alcance.

### 1.1. Resultados verificados

| Escenario | Reinicios | Bloqueo máx. | Fallos de plazo |
| :--- | :---: | :---: | :---: |
| S0 | 0 | 17.000 ms | 0 |
| S1 | 3 | 125.000 ms | 3 |
| S2 | 0 | 5.000 ms | 0 |
| S3 | 0 | 3.000 ms | 0 |

`make test` imprime `PASS` en `test_signatures`, `test_bus` y `test_context`, y
`determinism: PASS`. `make run-pip-off` imprime `WATCHDOG: RESET`;
`make run-pip-on` imprime `OK`.

## 2. Objetivo y alcance

### 2.1. Objetivo

Construir un **entorno RTOS simulado y determinista** en C11 + ensamblador
x86-64 que reproduzca la inversión de prioridades no acotada del mutex interno
de `select()` en el ordenador de vuelo del lander Mars Pathfinder, el
incumplimiento del ciclo 1553 de 125 ms y el reset del watchdog, además de su
corrección con herencia de prioridad.

### 2.2. Entregable

- `entornoRTOS`: binario que ejecuta un escenario, escribe una traza y genera
  datos para el visualizador.
- `src/switch.S`: cambio de contexto x86-64.
- `out/s0_pip_off.txt` … `out/s3_control.txt`.
- `out/viewer.html` + `out/sX_data.js`: visualizador de C, ensamblador, tareas y
  mutex.
- `test_signatures`, `test_bus`, `test_context` y `tests/test_determinism.sh`.
- `README.md` con build, run, escenarios, visualizador y límites.

### 2.3. Decisiones cerradas

| Decisión | Valor |
| :--- | :--- |
| Lenguaje | C11 + ensamblador x86-64 System V |
| Contexto | `src/switch.S`, sin `ucontext` |
| Build | GNU Make + GCC/Clang + GNU as |
| Dependencias | Ninguna externa |
| Privilegios | Ninguno; sin `root` |
| Determinismo | Total; tiempo simulado, sin wall-clock |
| Escenarios | S0–S3 |
| Visualizador | HTML autocontenido, nivel de evento |
| Relación con VxWorks | Modelo, no emulación |

### 2.4. Incluye

- RTOS modelo: scheduler de prioridad fija, tareas, tiempo simulado.
- Mutex con y sin `SEM_INVERSION_SAFE`.
- `pipe`, `fd_set` y `select()` con su mutex interno.
- Bus 1553 de 8 Hz y watchdog de `bc_sched` cada 125 ms.
- Software de vuelo: `bc_sched`, `bc_dist`, `ASI/MET`, `med_1..3`, `tExec`.
- Traza legible y datos estructurados para el visualizador.
- Pruebas S0–S3, contexto y determinismo.

### 2.5. No incluye

- VxWorks real, su código fuente o su binario.
- Emulación bit a bit, caché, pipeline o protocolo 1553 detallado.
- Física de la misión o telemetría de vuelo.
- El film 3D, el artículo IEEE o las slides.
- Audio, texto narrativo o interfaz gráfica de escritorio.
- Visor instrucción por instrucción.

## 3. Hechos y fuentes

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

### 3.1. Cadena causal

```text
Datos de los sensores ASI/MET
        ↓
ASI/MET (prioridad 7) llama a select() y toma el mutex interno
        ↓
Tareas medias (4–6) despiertan y expropian a ASI/MET
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

```text
bc_dist espera → ASI/MET hereda la prioridad 3 → corre por encima de las
tareas medias → libera el mutex → bc_dist termina → no hay reset
```

### 3.2. Reglas de integridad

1. No atribuir el fallo a Sojourner.
2. No decir "el RTOS se cayó": VxWorks funcionó como estaba configurado.
3. No decir "pérdida de datos" sin matizar.
4. No presentar el modelo como VxWorks real; es una reconstrucción del mecanismo.
5. Los tiempos son parámetros de calibración declarados, no telemetría.
6. La corrección es una opción de configuración, no un cambio del planificador.

## 4. Arquitectura

### 4.1. Stack

- C11, `-std=c11 -O2 -Wall -Wextra -Werror -D_GNU_SOURCE`.
- Ensamblador x86-64 System V (GNU as).
- `src/switch.S` para el cambio de contexto.
- Make para build/test/run.
- Sin dependencias externas.

### 4.2. Estructura

```text
entornoRTOS/
├── AGENTS.md
├── README.md
├── Makefile
├── .gitignore
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
│   ├── switch.S
│   ├── rtos.c
│   ├── sem.c
│   ├── pipe.c
│   ├── bus1553.c
│   ├── flight_sw.c
│   ├── trace.c
│   ├── scenario.c
│   └── main.c
├── tests/
│   ├── test_signatures.c
│   ├── test_context.c
│   └── test_determinism.sh
├── viewer/
│   └── viewer.html
└── out/
```

### 4.3. Scheduler y tiempo

- Tiempo simulado en microsegundos (`uint64_t`).
- Tareas propias con `ucontext` sustituido por `rtos_switch`.
- `task_t` guarda `void *sp`; la pila inicial se prepara con alineación de 16
  bytes y un `ret` a `task_trampoline`.
- `cpu_work(us)` descuenta el trabajo restante de la tarea; si es expropiada,
  conserva su `remaining` y continúa al reanudarse.
- `task_delay(us)` duerme la tarea hasta `now + us`.
- Si no hay tareas listas, el scheduler avanza al siguiente despertar.
- `sim_stop` termina la simulación a los 2 s simulados.

### 4.4. Tareas

| Tarea | Prioridad | Período / activación | WCET | Rol | Recurso |
| :--- | :---: | :--- | :---: | :--- | :--- |
| `sim_stop` | 0 | 2 s | — | Termina la simulación | — |
| `bc_sched` | 1 | 125 ms | 100 µs | Ciclo 1553 y watchdog | `bus_sem` |
| `bc_dist` | 3 | Tras el bus | 2 ms | Distribuye datos; `select()`/`pipe()` | `select_mutex` |
| `med_1` | 4 | 20 ms | 3 ms | Carga de CPU | — |
| `med_2` | 5 | 25 ms | 4 ms | Carga de CPU | — |
| `med_3` | 6 | 500 ms | 150 ms (alta) / 5 ms (baja) | Ráfaga de compresión | — |
| `ASI/MET` | 7 | 500 ms (fase 499 ms) | 0,4 ms + 3 ms de `select()` | Sensores | `select_mutex` |
| `tExec` | 99 | — | — | CPU ociosa | — |

Los valores son parámetros de calibración. `med_3` es la carga que garantiza la
expropiación en S1; en S0 se reduce a 5 ms.

### 4.5. Mutex y herencia de prioridad

- `sem_t` con dueño, contador de recursión, cola de espera por prioridad y
  bandera `pip`.
- Sin PIP: el dueño conserva su prioridad base.
- Con PIP: al bloquearse una tarea, el dueño hereda la mayor prioridad de sus
  esperadores; al liberar, se recalcula su prioridad efectiva.
- La prioridad efectiva es la que usa el scheduler.
- La corrección es `semMCreate(SEM_Q_PRIORITY | SEM_INVERSION_SAFE)`.
- Límite: la herencia se propaga a los esperadores directos; no se modela una
  cadena transitiva de mutex anidados.

### 4.6. `pipe` y `select()`

- `pipe_t` con buffer circular de 4096 bytes.
- `rtos_select(mutex, pipe, nfds, readfds, writefds, timeout)` modela
  `select()`:
  1. Toma el mutex interno.
  2. Ejecuta la sección crítica (`cpu_work(SELECT_WCET_US)`), donde puede ser
     expropiada.
  3. Escanea los descriptores.
  4. Libera el mutex.
- `bc_dist` y `ASI/MET` comparten el mutex en S0–S2. En S3 usan mutex separados.

### 4.7. Bus 1553

- `bus1553.c` encapsula el ciclo de 8 Hz.
- `bc_sched` llama a `bus1553_cycle()` cada 125 ms.
- `bc_dist` espera con `bus1553_wait()`.
- `bus_sem` es un semáforo binario.
- `bus1553_cycle_count()` permite verificar 15 ciclos en 2 s.

### 4.8. Watchdog y reset

- `bc_sched` comprueba `bc_dist_done` al inicio de cada ciclo.
- Si es 0, registra `MISS`, llama a `rtos_reset()` y cuenta el reinicio.
- `rtos_reset()` libera los mutex, despierta a los bloqueados y marca a los
  dueños anteriores con `lost_mutex`.
- Cuando el dueño anterior intenta liberar, `sem_give()` registra `UNWIND` y
  descarta la operación: el sistema reiniciado ya no reconoce ese lock.
- No se reinician los contextos de las tareas; es una abstracción declarada.

## 5. Código y mapeo VxWorks

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

El código es propio. No se presenta como el fuente original de VxWorks.

## 6. Escenarios

| Escenario | PIP | Carga | Mutex | Esperado |
| :--- | :---: | :--- | :---: | :--- |
| S0 | off | baja (`med_3` 5 ms) | compartido | 0 reinicios |
| S1 | off | alta (`med_3` 150 ms) | compartido | 3 reinicios |
| S2 | on | alta | compartido | 0 reinicios |
| S3 | off | alta | separados | 0 reinicios |

S3 es el control: sin recurso compartido, no hay inversión.

## 7. Traza y visualizador

### 7.1. Traza de texto

Formato:

```text
[0.499000] LOCK    asi_met  prio=7 select_mutex
[0.500100] WAIT    bc_dist  prio=3 select_mutex
[0.625000] MISS    bc_sched prio=1 bc_dist
[0.625000] RESET   bc_sched prio=1 watchdog
[0.733200] UNWIND  asi_met  prio=7 select_mutex
# SUMMARY resets=3 max_block_ms=125.000 deadline_misses=3
```

Los eventos `SWITCH`, `BUS` y las instantáneas periódicas se guardan solo en
`out/sX_data.js`.

### 7.2. Visualizador

- `make view` genera `out/viewer.html` y `out/sX_data.js`.
- Paneles: C, ensamblador, tareas, mutex, bus/watchdog, contexto de misión,
  línea de tiempo y eventos.
- `?scenario=S1&t=500100` abre un punto concreto (microsegundos).
- El panel de ensamblador muestra `switch.S` en eventos `SWITCH` y la
  desensamblación de la función actual en el resto.
- El visualizador es de nivel de evento, no un depurador instrucción por
  instrucción.

## 8. Build, run y test

```bash
make                 # compila
make test            # firmas, contexto y determinismo
make run-pip-off     # S1 -> out/s1_pip_off.txt
make run-pip-on      # S2 -> out/s2_pip_on.txt
make all-scenarios   # S0-S3
make view            # genera el visualizador
make clean
```

Sin `sudo`. Sin variables de entorno especiales.

## 9. Límites

1. Modelo determinista, no emulación de VxWorks.
2. Tiempos sintéticos calibrados, no telemetría.
3. `cpu_work()` no ejecuta instrucciones de la CPU histórica.
4. El visualizador es de nivel de evento.
5. No modela caché, pipeline, protocolo 1553 detallado ni física.
6. El reset no reinicia los contextos; libera recursos y descarta la liberación
   pendiente.
7. La herencia de prioridad no es transitiva en cadenas de mutex.
8. El cambio de contexto guarda registros callee-saved; no guarda estado FPU/SSE
   porque las tareas no lo modifican.
9. Solo x86-64 System V.

## 10. Inventario

| Ruta | Tipo | Propósito | Estado |
| :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento | Contrato local | Activo |
| `README.md` | Documento | Build, run, escenarios, visualizador y límites | Completo |
| `Makefile` | Build | Compilar, testear, ejecutar, visualizar | Completo |
| `.gitignore` | Git | Excluir binarios y datos generados | Activo |
| `include/` | Cabeceras | API del RTOS, bus y vuelo | Completo |
| `src/switch.S` | Ensamblador | Cambio de contexto x86-64 | Completo |
| `src/` | C | Scheduler, mutex, pipe/select, bus, vuelo, traza | Completo |
| `tests/test_signatures.c` | C | Firmas S0–S3 | Completo |
| `tests/test_bus.c` | C | 15 ciclos 1553 en 2 s | Completo |
| `tests/test_context.c` | C | Cambio de contexto y canarios | Completo |
| `tests/test_determinism.sh` | Shell | Dos ejecuciones idénticas | Completo |
| `viewer/viewer.html` | HTML/JS | Visualizador C/asm/tareas | Completo |
| `out/s0_pip_off.txt` … `out/s3_control.txt` | Trazas | Evidencia legible | Completo |
| `out/disasm.txt` | Generado | Desensamblación para el visor | Generado |
| `out/sX_data.js` | Generado | Datos del visor | Generado |
| `out/viewer.html` | Generado | Copia del visor | Generado |

## 11. Bitácora

| Fecha | Agente | Archivos | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `src/switch.S`, `include/`, `src/`, `tests/`, `viewer/`, `Makefile`, `README.md`, `AGENTS.md`, `.gitignore` | Migración a C + ensamblador x86-64: contexto propio, bus 1553, traza estructurada, visualizador HTML y pruebas de bus/contexto/determinismo. | `make test` PASS; S0 0/17.000/0, S1 3/125.000/3, S2 0/5.000/0, S3 0/3.000/0; `test_bus` 15 ciclos PASS; `test_context` PASS; determinismo PASS; visor S1/S2 verificado con Firefox headless. |
| 2026-11-02 | OpenCode (DeepSeek V4.1 Flash) | `Makefile`, `include/`, `src/`, `tests/`, `out/` | Implementación previa del entorno RTOS con `ucontext`, mutex/PIP, `select()`, software de vuelo y pruebas S0–S3. | `make test` PASS; S1 3 reinicios; S2 0. |

## 12. Checklist

- [x] Implementar cambio de contexto en `src/switch.S`.
- [x] Eliminar `ucontext` de `rtos.h` y `rtos.c`.
- [x] Añadir `test_context` con canarios de pila.
- [x] Extraer el bus 1553 a `bus1553.c`.
- [x] Añadir `test_bus` (15 ciclos en 2 s).
- [x] Instrumentar la traza con archivo, línea y función.
- [x] Generar datos estructurados para el visualizador.
- [x] Implementar `viewer/viewer.html`.
- [x] Añadir `test_determinism.sh`.
- [x] Verificar S0–S3.
- [x] Actualizar README y AGENTS local.
- [ ] Revisar PIP transitivo (opcional).
- [ ] Visor instrucción por instrucción (opcional).
- [ ] Actualizar `../AGENTS.md` global (pendiente de autorización).

## 13. Criterios de aceptación

1. `make` compila C y ensamblador sin warnings.
2. `make test` pasa: firmas, bus, contexto y determinismo.
3. S0: 0 reinicios; S1: 3; S2: 0; S3: 0.
4. `grep -R ucontext include src` no devuelve nada.
5. Dos ejecuciones de S1 producen archivos idénticos.
6. El visualizador muestra S1 con `LOCK`, `WAIT`, `MISS`, `RESET` y S2 con
   `INHERIT`.
7. No se usa root, wall-clock ni aleatoriedad.

## 14. Riesgos

| Riesgo | Mitigación |
| :--- | :--- |
| Error de alineación de pila en asm | `test_context` con canarios y S0–S3 |
| Registros callee-saved mal restaurados | Pruebas con llamadas a `trace_event` |
| Traza no determinista | Sin wall-clock/random; comparación byte a byte |
| Confundir el modelo con VxWorks | Aviso en README y AGENTS; nombres de API explícitos |
| Reset deja estados inconsistentes | `lost_mutex` + evento `UNWIND`; documentado |
| Datos del visor no generados | `make view` los regenera |
| Documento global desactualizado | Pendiente de autorización; no se toca |

## 15. Protocolo para agentes

1. Leer este archivo y `../AGENTS.md` antes de tocar nada.
2. Trabajar solo en `entornoRTOS/` salvo autorización explícita.
3. No modificar `simulacion3D/`, `main.tex`, `references.bib` ni `fuentes/`.
4. No añadir dependencias externas.
5. Mantener el determinismo: sin wall-clock, sin random, sin hilos reales.
6. Actualizar §1, §10, §11 y §12 al cerrar cada turno.
7. Si el disco contradice este documento, prevalece el disco.
8. Commit después de cada milestone.

## 16. Primeros pasos

1. `make test` para verificar el entorno.
2. `make view` y abrir `out/viewer.html`.
3. Revisar S1 en `?scenario=S1&t=500100` y S2 en `?scenario=S2&t=500100`.
4. Decidir si se abordan las mejoras opcionales: PIP transitivo o visor
   instrucción por instrucción.

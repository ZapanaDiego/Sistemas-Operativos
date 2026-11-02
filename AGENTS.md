# AGENTS.md — Protocolo, contexto y guía maestra del proyecto

> **ESTADO DEL DOCUMENTO:** vivo y de actualización obligatoria.
> **LEER AL INICIAR. ACTUALIZAR AL CERRAR CADA TURNO.**
> Última actualización: 2026-11-02 · OpenCode (DeepSeek V4.1 Flash)

**Mapa de lectura rápida**
- Agente nuevo: §8.1 (estado) → §3 (qué se investiga) → §7.7 (próximos pasos).
- Vas a redactar: §6.
- Vas a programar la simulación: §7.
- Vas a cerrar el turno: §9.

---

## 0. Regla de actualización obligatoria (R0)

`AGENTS.md` es el registro operativo del proyecto y la única fuente de verdad sobre su estado. Su objetivo principal es mantenerse actualizado: **todo agente que cree, modifique, mueva, renombre o elimine un archivo del repositorio debe actualizar este documento antes de cerrar su turno.**

La actualización mínima comprende:

1. Una fila nueva en la bitácora (§8.3) con fecha, agente, archivos afectados, cambio realizado y verificación.
2. La actualización del inventario de archivos (§8.4).
3. El ajuste de los checkboxes de la fase correspondiente (§8.2).
4. La actualización del estado general (§8.1): fase, próximo hito y bloqueos.
5. Si el cambio altera el alcance, la tesis, las preguntas de investigación, la estructura del artículo o el presupuesto de palabras, la actualización de §3 y §6.

Un turno que modifica archivos sin actualizar `AGENTS.md` se considera **incompleto** y debe corregirse antes de cualquier otra acción.

**Regla de conflicto:** si lo que dice este documento no coincide con lo que existe en disco, **prevalece el disco** y `AGENTS.md` debe corregirse de inmediato.

**Alcance:** leer archivos, ejecutar comandos de solo lectura o hacer experimentos que no dejan archivos no obliga a actualizar el inventario, pero sí a registrar la decisión en la bitácora si cambia el estado del proyecto. La regla aplica también a subagentes: el agente principal responde por que quede registrada su intervención.

---

## 1. Manifiesto y directrices para agentes de IA

Estás colaborando como co-investigador y asistente técnico en el **Trabajo Final del curso de Sistemas Operativos**, dictado por la **Mg. Maribel Molina Barriga** (Universidad La Salle, Arequipa).

### 1.1. Reglas críticas

1. **R0 — Actualización obligatoria.** Ver §0. No hay excepciones.
2. **Integridad académica y cero alucinaciones.**
   - Toda afirmación técnica, fecha, cifra o comparación debe estar sustentada en una fuente identificable.
   - Toda cita `\cite{key}` debe existir en `references.bib` con metadatos reales y verificables (autores, título, año, volumen, número, páginas, DOI).
   - Distinguir siempre **fuente primaria** (Reeves, NASA) de **fuente secundaria** (prensa, resúmenes, el `.docx` interno).
3. **Rigor de formato.**
   - IEEE dos columnas (`IEEEtran`), 5–10 páginas de **solo texto** (sin figuras, tablas ni referencias).
   - Equivalencia: ~800–1000 palabras por página IEEE; 5 páginas ≈ 4 000–5 000 palabras; 10 páginas ≈ 8 500–10 000.
   - El objetivo de este proyecto es ~7 000–7 500 palabras de cuerpo (7–9 páginas de texto).
4. **Enfoque IMRyD.**
   - Introducción que justifica el problema; Método reproducible; Desarrollo que responde a las RQ; Discusión que contextualiza y reconoce límites.
   - Estilo impersonal o plural formal; pretérito en método y resultados; presente en hechos establecidos y conclusiones.
5. **Trazabilidad.**
   - Cada figura y tabla debe poder reconstruirse desde los datos de `sim/out/` o desde una fuente citada.
   - Los experimentos deben ser deterministas y reproducibles con un comando.

---

## 2. Marco académico y requisitos del trabajo final

### 2.1. Tópico definitivo

> **TÓPICO DEFINIDO (2026-11-02):** estudio de caso del fallo del RTOS **VxWorks** del módulo de aterrizaje **Mars Pathfinder** (aterrizaje el 4/7/1997; reinicios en los días posteriores), con **simulación de eventos discretos** de la inversión de prioridades.

Se enmarca en el tópico oficial **5. Sistemas operativos en plataformas especializadas — computación espacial**, con el eje técnico de **RTOS** que también cubre el tópico 2. El tema previo *FreeRTOS para IoT* quedó descartado como eje y su historial está en `docs/HISTORIAL.md`.

### 2.2. Entregables oficiales

1. **Investigación y corpus bibliográfico**
   - Bibliografía base (libros y manuales).
   - Mínimo **10 artículos arbitrados de los últimos 5 años**, directamente vinculados al tópico.
   - ZIP con los 10 artículos en PDF.
2. **Artículo científico IEEE**
   - Doble columna, 5–10 páginas de solo texto.
   - Secciones obligatorias: Resumen, Palabras clave, Introducción, Método, Desarrollo y Discusión, Conclusiones, Referencias.
   - Elaboración en entorno versionado para evidenciar trabajo colaborativo.
3. **Presentación**
   - PDF colaborativo, síntesis visual, diagramas y discusión crítica.
4. **Exposición**
   - Máximo 10 minutos + 5 minutos de preguntas.
   - 2 miembros elegidos al azar el día de la exposición.

### 2.3. Ponderación (20 puntos)

| Componente | Criterio | Puntos | Peso |
| :--- | :--- | :---: | :---: |
| Individual | Trabajo individual evidenciado en documentos compartidos / historial Git | 4.0 | 20 % |
| Grupal | Coevaluación de exposición y presentación (5 indicadores) | 4.0 | 20 % |
| Grupal | Artículo científico | 7.0 | 35 % |
| Grupal | Exposición | 5.0 | 25 % |
| **Total** | | **20.0** | **100 %** |

> Los contenidos de todos los artículos y exposiciones se evalúan en el examen final con peso **70 %**.

### 2.4. Cronograma y situación real

| Hito | Fecha oficial | Estado |
| :--- | :--- | :--- |
| Hito 1 — avance 40–50 % | 12/10/2026 | **Vencido**; no se registró entrega |
| Sorteo de expositores | 24/11/2026 | Pendiente |
| Entrega final (artículo + slides + ZIP) | 29/11/2026 | **Objetivo principal** |
| Exposiciones | 30/11, 01/12, 07/12/2026 | Pendiente |

Quedan **27 días** al 2026-11-02. El plan de cierre está en §7.7.

### 2.5. Rúbrica de coevaluación (4.0 pts)

1. La información de la presentación es suficiente y necesaria para entender el tema.
2. Las ideas expuestas fueron claras y facilitaron la comprensión.
3. Se evidencia que los presentadores conocen el tema.
4. Se evidencia que explican, más allá de leer.
5. La presentación evidencia organización y trabajo colaborativo.

---

## 3. Definición del proyecto: el fallo del RTOS de Mars Pathfinder

### 3.1. Objetivo general

Diseñar, implementar y documentar una **simulación de eventos discretos** que reproduzca el fallo del RTOS VxWorks del módulo de aterrizaje Mars Pathfinder —una inversión de prioridades no acotada en el mutex interno de `select()`— y analizar, con evidencia primaria y un contrafactual, **por qué falló, cómo falló y cómo se corrigió**.

### 3.2. Objeto de estudio

No es "los RTOS" en general ni la misión completa. Es el comportamiento temporal del conjunto de tareas del software de vuelo durante el ciclo de bus 1553 a **8 Hz (125 ms)**, y en particular la interacción `select()` / `pipe()` / mutex que bloqueó a `bc_dist`.

### 3.3. Tesis

> El fallo no fue un error del planificador ni una pérdida de datos, sino una **inversión de prioridades no acotada**, habilitada por la configuración por defecto del mutex interno de `select()` y agravada por una carga de tareas medias superior a la prevista. El watchdog convirtió el incumplimiento de plazo en un reinicio: recuperó el sistema, pero no corrigió la causa. Habilitar la herencia de prioridad acotó el bloqueo y eliminó los reinicios.

### 3.4. Preguntas de investigación

- **RQ1.** ¿Cuál fue la causa raíz del fallo y qué condiciones del sistema la hicieron posible?
- **RQ2.** ¿Cómo se manifestó en la temporización del ciclo de 1553 y qué papel jugó el watchdog?
- **RQ3.** ¿Qué corrección se aplicó, por qué ataca la causa y qué evidencia demuestra que funcionó?

### 3.5. Contribuciones esperadas

- **C1.** Reconstrucción causal del caso con cadena de evidencia primaria.
- **C2.** Simulación reproducible que reproduce el fallo y su contrafactual.
- **C3.** Lecciones de diseño y verificación para RTOS actuales.

### 3.6. Alcance y límites

**Incluye:** el ordenador de vuelo del lander, VxWorks, las tareas `bc_sched`, `bc_dist`, `ASI/MET` y las tareas medias, el mutex de `select()`, el ciclo 1553 y el reset.

**No incluye:** la misión completa, el rover Sojourner como objeto del fallo, la física del aterrizaje, el protocolo 1553 detallado, caché/pipeline ni una emulación bit a bit de VxWorks.

### 3.7. Relación con el corpus de 10 papers

Los diez artículos **no son el objeto**: son el estado del arte que enmarca el caso y demuestra que la clase de fallo sigue vigente. Se usan en §6.4, no como sustituto de la evidencia primaria. **Dong et al. (2020)** es el puente directo por su mecanismo de `priority-swapping`.

### 3.8. Productos entregables

Artículo IEEE, simulación reproducible (`sim/`), presentación (`slides/`), ZIP de los diez papers, `AGENTS.md` actualizado y repositorio Git con historial.

### 3.9. Criterios de éxito

- S1 reproduce al menos un reinicio; S2 y S3 no producen reinicios.
- El artículo responde RQ1–RQ3 con evidencia trazable.
- 5–10 páginas de texto y 10 papers citados y verificados.
- Simulación reproducible con un comando y resultados en `sim/out/`.

---

## 4. Corpus de fuentes

### 4.1. Fuentes primarias del caso

| Fuente | Contenido | Uso | Estado |
| :--- | :--- | :--- | :--- |
| **Reeves, G. E. (1997-12-15).** *What really happened on Mars?* Correo técnico. `fuentes/Mars_Pathfinder_Reeves_1997_cuenta_original.html` | Arquitectura, tareas, prioridades, secuencia del fallo, diagnóstico y corrección | Fuente principal de RQ1 y RQ2 | Local, HTML |
| **Reeves, G. E. (1999-11).** *Priority Inversion: How We Found It, How We Fixed It.* Dr. Dobb's Journal. `fuentes/Mars_Pathfinder_Reeves_1999_diagnostico_y_correccion.html` | Traza, réplica, <18 h de diagnóstico, `semMCreate`, parche | Fuente principal de RQ3 | Local, HTML |
| **NASA.** *Mars Pathfinder.* https://science.nasa.gov/mission/mars-pathfinder/ | Aterrizaje 4/7/1997; Sojourner 6/7/1997; distinción lander/rover | Datos de misión | Web oficial |
| **NSSDC.** *Mars Pathfinder Project Information.* https://nssdc.gsfc.nasa.gov/planetary/mesur.html | Ficha técnica y cronología | Datos de misión | Web oficial |
| **Associated Press (1997-07-18).** *Pathfinder Glitch Found.* The Spokesman-Review | Reinicios y parche previsto para el sábado 19/7 | Corroboración secundaria de fechas | Prensa |
| `fuentes/Mars_Pathfinder_reinicios_1997.docx` | Síntesis interna en español (910 palabras) | **No citable**; solo notas de estudio | Interno |

> Las fuentes de Reeves son de 1997/1999 y no son arbitradas: **no cuentan** dentro de los 10 papers 2020–2025. Se citan como fuentes primarias del caso.

### 4.2. Corpus científico 2020–2025 (10 papers)

Metadatos verificados contra Crossref el 2026-11-02.

| # | Autores | Año | Revista | Vol (Núm): pp. | DOI | Cuartil | Uso |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | Serra, Ara, Fara, Cucinotta | 2021 | Journal of Systems Architecture | 118: 102210 | 10.1016/j.sysarc.2021.102210 | Q1 | Mecanismos de acceso a scheduling POSIX |
| 2 | He, Sun, Jiang, Lv, Lee, Guan | 2024 | Real-Time Systems | 60(2): 291–327 | 10.1007/s11241-024-09421-9 | Q2 | Recuperación de recursos en tareas paralelas |
| 3 | Akesson, Nasri, Nelissen, Altmeyer, Davis | 2022 | Real-Time Systems | 58(3): 358–398 | 10.1007/s11241-021-09376-1 | Q2 | Práctica industrial (encuesta, 120 profesionales) |
| 4 | Salman, Papadopoulos, Mubeen, Nolte | 2022 | Journal of Systems Architecture | 122: 102358 | 10.1016/j.sysarc.2021.102358 | Q1 | Tareas elásticas y reservas MPS |
| 5 | Farina, Gala, Cinque, Fohler | 2023 | Journal of Systems Architecture | 137: 102848 | 10.1016/j.sysarc.2023.102848 | Q1 | Aislamiento de memoria (Intel RDT/MBA) |
| 6 | Minaeva, Hanzálek | 2021 | ACM Computing Surveys | 54(1): 1–32 | 10.1145/3431232 | Q1 | Planificación periódica time-triggered |
| 7 | Dong, Jiang, Burns, Ding, Ma | 2020 | Journal of Systems Architecture | 107: 101774 | 10.1016/j.sysarc.2020.101774 | Q1 | Comunicación RTOS–GPOS y `priority-swapping` |
| 8 | De Oliveira, Casini, Lelli, Cucinotta | 2025 | IEEE Transactions on Computers | 74(8): 2608–2620 | 10.1109/TC.2025.3566908 | Q1 | Timerlat: latencia y observabilidad |
| 9 | Manjunath, Baunach | 2024 | Journal of Systems Architecture | 154: 103220 | 10.1016/j.sysarc.2024.103220 | Q1 | Verificación estática de código RTOS |
| 10 | Guasque, Aceituno, Balbastre, Simó, Crespo | 2022 | The Journal of Supercomputing | 78(12): 14703–14725 | 10.1007/s11227-022-04446-y | Q1/Q2 | Planificabilidad con contención |

**Notas de metadatos**
- **Minaeva:** publicación online 2021-03-05; número impreso 2022-01-31. Se usa **2021** de forma consistente y se anota el número impreso.
- **Akesson:** PDF local es el manuscrito aceptado; la paginación final es 358–398.
- **Timerlat:** PDF local es la versión de autor con cabecera de plantilla; los datos reales son **74(8): 2608–2620, 2025**.
- **Dong (2020):** si el corte se lee estrictamente como 2021–2026, queda fuera del corpus; se conserva como referencia complementaria y se justifica en el método.

### 4.3. Bibliografía base (pendiente de recuperar)

| Obra | Aporte | Estado |
| :--- | :--- | :--- |
| Silberschatz, Galvin, Gagne — *Operating System Concepts* (10.ª ed., 2018) | Procesos, scheduling, sincronización, inversión de prioridades | **Pendiente** |
| Stallings — *Operating Systems: Internals and Design Principles* | Concurrencia, semáforos, monitores, interbloqueos | **Pendiente** |
| Brookshear & Brylow — *Computer Science: An Overview* (12.ª ed.) | Contexto de arquitectura y capas | **Pendiente** |
| Libro de Linux | Kernel, VFS, memoria, interrupciones | **Pendiente** |
| Sha, Rajkumar, Lehoczky (1990) — *Priority Inheritance Protocols* | Fundamento teórico de PIP/PCP | **Pendiente de verificar** |
| Liu & Layland (1973) — *Scheduling Algorithms for Multiprogramming* | Fundamento RM/EDF | **Pendiente de verificar** |
| Kopetz — *Real-Time Systems* | Fundamento de sistemas de tiempo real | **Pendiente de verificar** |

> Sin esta bibliografía no se puede sustentar la explicación de mutex, herencia de prioridad y planificación de prioridad fija sin depender solo de Reeves.

### 4.4. Fuentes metodológicas de la cátedra

Gastel & Day (2016); Slafer (2009); Wu (2011); Kumar (2023); LaPlaca, Lindgreen & Vanhamme; MVZ Córdoba (2010, 2011). Se usan para la estructura IMRyD, el título, el resumen y las palabras clave; no se citan como evidencia técnica.

### 4.5. Trazabilidad Scopus

- 8 de los 10 artículos están en `fuentes/analisis_bibliografico/scopus_10_original.csv`.
- 2 EID identificados fuera del CSV: `2-s2.0-85198027358` (Manjunath) y `2-s2.0-85127724315` (Guasque).
- **Pendiente:** exportación Scopus única por DOI con los 10 registros.
- **Advertencia:** el mapa de VOSviewer se construyó con los 10 resultados originales, dos de los cuales no están en el corpus final. **No usar la figura tal cual**; rehacer o descartar.

---

## 5. Arquitectura del repositorio y toolchain

### 5.1. Estructura

```
investigacion/
├── AGENTS.md                     # Reglas, definición y estado (este archivo)
├── docs/
│   └── HISTORIAL.md              # Bitácora anterior al 2026-11-02
├── main.tex                      # Carátula TikZ + artículo IEEE
├── references.bib                # BibTeX (vacío al 2026-11-02)
├── IEEEtran.cls / IEEEtran.bst   # Clase y estilo IEEE
├── build.sh                      # pdflatex + bibtex + pdflatex ×2
├── Makefile                      # make pdf / count / clean
├── img/
│   └── logoLaSalleUniversidad.png
├── fuentes/                      # 10 PDFs + copia ReTiF + 2 HTML Reeves + docx
│   └── analisis_bibliografico/   # Matriz, CSV, ZIP, RIS/BibTeX, VOSviewer
├── sim/                          # PLANIFICADO: motor y escenarios
│   ├── model.py
│   ├── scenarios.py
│   ├── run.py
│   ├── metrics.py
│   └── out/                      # CSV, trazas y SVG
├── slides/                       # PLANIFICADO: presentación
└── .vscode/
```

### 5.2. Herramientas disponibles

| Herramienta | Versión / estado | Uso |
| :--- | :--- | :--- |
| `pdflatex`, `bibtex`, `latexmk`, `texcount` | Instalados | Compilación y conteo |
| Python | 3.14.8 | Simulación |
| NumPy | 2.5.4 | Cálculo y estadística |
| Node.js | 26.12.1 | Visualizador HTML/JS (opcional) |
| SimPy, Matplotlib, Pandas, SciPy | **No instalados** | Si se necesitan, instalar en `.venv` y registrar en §8.4 |
| QEMU | **No instalado** | No se usará |

**Decisión:** el motor de simulación será Python puro + NumPy, sin dependencias externas, para garantizar reproducibilidad. Las figuras se generarán como SVG desde el propio código o con Matplotlib si se instala.

### 5.3. Compilación y verificación

```bash
./build.sh          # compilación completa
make count          # conteo de palabras
make clean          # limpieza de auxiliares
```

Medición de solo texto:

```bash
texcount -inc -sub=none main.tex
```

### 5.4. Convenciones de código

- Un solo archivo de modelo (`sim/model.py`) con scheduler, tareas y mutex.
- Escenarios declarativos en `sim/scenarios.py`.
- Semillas fijas y parámetros en un diccionario reproducible.
- Salidas en CSV + SVG; nada de valores escritos a mano en el artículo.
- Cada figura del artículo debe citar el archivo de `sim/out/` que la genera.

---

## 6. Diseño del artículo

### 6.1. Título y tesis

**Título:** *Inversión de prioridades en el RTOS de Mars Pathfinder: por qué falló, cómo falló y cómo se corrigió.*

**Tesis:** ver §3.3.

### 6.2. Estructura y presupuesto

| Sección | Palabras | Contenido |
| :--- | ---: | :--- |
| Resumen + keywords | 220 | Contexto, fallo, método, hallazgos, implicancia |
| I. Introducción | 900 | Misión, reinicios, brecha, RQ1–RQ3, contribuciones, organización |
| II. Marco teórico y estado del arte | 1 100 | RTOS y prioridad fija; inversión de prioridades y PIP; los 10 papers en 3 bloques |
| III. Método | 1 300 | Estudio de caso + simulación; fuentes; modelo; escenarios; métricas; validación |
| IV. Desarrollo y discusión | 3 300 | IV-A por qué falló; IV-B cómo falló; IV-C cómo se solucionó; IV-D validación; IV-E lecciones |
| V. Conclusiones | 500 | Respuestas a RQ1–RQ3, límites, trabajo futuro |
| **Total** | **≈ 7 300** | 7–9 páginas de texto |

### 6.3. Figuras y tablas

| Elemento | Contenido | Fuente |
| :--- | :--- | :--- |
| Fig. 1 | Arquitectura de Pathfinder (VME, 1553, lander/cruise, ASI/MET) | Redibujada desde Reeves 1997 |
| Fig. 2 | Tareas y prioridades | Modelo de simulación |
| Fig. 3 | Gantt S1: inversión y reset | `sim/out/s1_gantt.svg` |
| Fig. 4 | Gantt S2: herencia de prioridad | `sim/out/s2_gantt.svg` |
| Fig. 5 | Respuesta de `bc_dist` y barrido de carga | `sim/out/s4_barrido.svg` |
| Tabla I | Parámetros del modelo | Reeves + supuestos declarados |
| Tabla II | Escenarios S0–S5 | §7.3 |
| Tabla III | Resultados (bloqueo, misses, reinicios, overhead) | `sim/out/resultados.csv` |
| Tabla IV | Cadena de evidencia | §4.1 |

### 6.4. Mapa de citas por sección

| Sección | Citas previstas |
| :--- | :--- |
| I. Introducción | NASA; Reeves 1997; AP 1997; Akesson 2022 |
| II-A. RTOS y prioridad fija | Silberschatz; Stallings; Liu & Layland |
| II-B. Inversión y PIP | Sha et al. 1990; Silberschatz; Stallings |
| II-C. Estado del arte | Minaeva; Guasque; He; Salman; ReTiF; Dong; Manjunath; Farina; Timerlat; Akesson |
| III. Método | Reeves 1997/1999; NASA; matriz propia |
| IV-A. Por qué falló | Reeves 1997; teoría PIP |
| IV-B. Cómo falló | Reeves 1997; simulación S1 |
| IV-C. Cómo se solucionó | Reeves 1999; simulación S2/S3 |
| IV-D. Validación | Simulación S4/S5 |
| IV-E. Lecciones | Dong; Timerlat; ReTiF; Manjunath; Farina; Akesson |
| V. Conclusiones | Síntesis |

### 6.5. Reglas de integridad factual

1. **No inventar el sol del primer reinicio.** Reeves no lo fija; usar "en los días posteriores al aterrizaje" y anclar el 18/7 con la prensa.
2. **No atribuir el fallo a Sojourner.** Ocurrió en el ordenador de vuelo del lander, que además servía de relay.
3. **No decir "el RTOS se cayó".** VxWorks funcionó como estaba configurado; el reset fue la reacción del watchdog.
4. **No decir "pérdida de datos" sin matizar.** Los datos en RAM se conservan si no se pierde la alimentación; se retrasan actividades.
5. **No presentar la simulación como emulación.** Es un modelo abstracto calibrado, no una réplica de VxWorks.
6. **No usar el `.docx` interno como fuente.** Es una síntesis; se cita a Reeves.
7. **No usar la figura de VOSviewer actual.** Es inconsistente con el corpus final.

---

## 7. Diseño de la simulación

### 7.1. Qué se simula y qué no

**Se simula:** el mecanismo causal —tareas, prioridades, mutex, `select()`/`pipe()`, ciclo de 125 ms, watchdog— con tiempos sintéticos calibrados.

**No se simula:** VxWorks real, caché, pipeline, protocolo 1553, física de la misión ni la telemetría de vuelo.

### 7.2. Modelo de tareas

| Tarea | Prioridad | Período / activación | Rol | Recurso |
| :--- | :---: | :--- | :--- | :--- |
| `bc_sched` | 1 (más alta) | 125 ms (8 Hz) | Planifica el ciclo 1553 y comprueba a `bc_dist` | — |
| `entrada/aterrizaje` | 2 | Después del aterrizaje, baja actividad | Tarea intermedia del sistema | — |
| `bc_dist` | 3 | Tras el tráfico del bus | Distribuye datos; escribe en `pipe()` | `select_mutex` |
| Tareas medias | 4–6 | Periódicas / esporádicas | Comunicaciones, imagen, compresión | CPU |
| `ASI/MET` | 7 (más baja) | Periódica | Datos meteorológicos; llama a `select()` | `select_mutex` |
| `tExec` | idle | — | Tarea de ejecución de VxWorks | CPU ociosa |

**Mutex:** sección crítica que modela `selNodeAdd()`/`semGive()`; dos modos: `PIP=off` y `PIP=on`.

**Watchdog:** `bc_sched` verifica al inicio de cada ciclo que `bc_dist` haya terminado; si no, registra `reset`.

**Perfil de misión:** `carga(sol)` aumenta la carga de tareas medias a partir del sol 3, de forma ilustrativa y declarada como escenario, no como dato histórico.

### 7.3. Escenarios

| Escenario | Configuración | Resultado esperado | RQ |
| :--- | :--- | :--- | :---: |
| S0 | Carga baja, PIP off | Sin reinicios (pruebas pre-lanzamiento) | RQ1 |
| S1 | Carga alta, PIP off | Inversión y reinicios | RQ2 |
| S2 | Carga alta, PIP on | Sin reinicios | RQ3 |
| S3 | Control: sin mutex compartido | Sin reinicios | RQ2 |
| S4 | Barrido de carga 0–80 % | Curva de umbral PIP off/on | RQ3 |
| S5 | Sensibilidad: sección crítica, período ASI/MET, nº de tareas medias | Robustez | RQ3 |

### 7.4. Métricas

- Tiempo de respuesta de `bc_dist` por ciclo; máximo y percentil 99.
- Tiempo de bloqueo máximo de `bc_dist`.
- Fallos de plazo y reinicios por sol; primer sol con reinicio.
- Número y duración de inversiones.
- Utilización de CPU de las tareas medias.
- Sobrecarga de PIP (cambios de contexto o aumento del tiempo de respuesta en el caso común).

### 7.5. Validación

1. **Estructural:** cada parámetro se justifica con Reeves o se declara como supuesto.
2. **Conductual:** se cumplen las cuatro firmas (S0 no falla; S1 falla; S2 no falla; S3 no falla).
3. **Sensibilidad:** el resultado se mantiene en un rango de WCET y secciones críticas; se reporta la frontera.
4. **Limitaciones:** modelo abstracto, sin caché ni pipeline; tiempos sintéticos; no reproduce la telemetría exacta.

### 7.6. Entregables y reproducibilidad

```
sim/
├── model.py        # scheduler, tareas, mutex, watchdog
├── scenarios.py    # S0–S5 y perfiles de carga
├── run.py          # CLI: python3 sim/run.py --scenario s1
├── metrics.py      # cálculo y exportación
└── out/            # CSV + SVG + trazas
```

- Un comando debe regenerar todas las figuras: `python3 sim/run.py --all`.
- Semilla fija; resultados deterministas.
- `sim/README.md` con instrucciones y supuestos.

### 7.7. Plan de cierre (27 días)

| Semana | Fechas | Entregable |
| :--- | :--- | :--- |
| 1 | 2–8 nov | Motor + S1 (reproduce el reset) |
| 2 | 9–15 nov | S2/S3 + S4/S5 + figuras |
| 3 | 16–22 nov | Redacción completa del artículo |
| 4 | 23–28 nov | Revisión, compilación, slides, ZIP |
| Cierre | 29 nov | Entrega final |

---

## 8. Estado actual, checklists, bitácora e inventario

### 8.1. Estado general

**Actualización 2026-11-02 (OpenCode / DeepSeek V4.1 Flash):**

- **Tópico:** fallo del RTOS de Mars Pathfinder; estudio de caso + simulación.
- **Fase actual:** Fase 1 (definición) **completada**; Fase 2 (corpus) **completada** salvo bibliografía base y exportación Scopus única; Fase 3 (simulación) **pendiente**.
- **Próximo hito:** implementar `sim/model.py` y reproducir S1 (inversión + reset).
- **Bloqueos:** bibliografía base ausente; 2 EID fuera del CSV de Scopus; figura de VOSviewer inconsistente; `references.bib` vacío.
- **Plantilla:** `main.tex` compila en **2 páginas** (carátula + esqueleto), **0 palabras de cuerpo**, según la última compilación del 2026-10-30.
- **Git:** repositorio inicializado el 2026-11-02; primer commit de referencia en §8.3.
- **Riesgo principal:** 27 días para la entrega final; la simulación es la ruta crítica.

### 8.2. Checklists

#### Fase 0 — Reset y plantilla (completada)
- [x] Eliminación del desarrollo FreeRTOS/IoT y auxiliares.
- [x] Conservación de `IEEEtran.cls`, `IEEEtran.bst`, logo, `build.sh`, `Makefile`.
- [x] `main.tex` como esqueleto IEEE con carátula.
- [x] `references.bib` vacío con plantilla.
- [x] `AGENTS.md` actualizado al reset.

#### Fase 1 — Definición del proyecto (completada 2026-11-02)
- [x] Tema: fallo del RTOS de Mars Pathfinder.
- [x] Objetivo, tesis y RQ1–RQ3.
- [x] Contribuciones C1–C3 y criterios de éxito.
- [x] Estructura del artículo y presupuesto de palabras.
- [x] Regla R0 e inventario.
- [ ] Actualizar carátula, `\title`, abstract y keywords en `main.tex`.

#### Fase 2 — Corpus (completada salvo pendientes)
- [x] 10 PDFs 2020–2025 en `fuentes/`.
- [x] Matriz XLSX/CSV y ZIP del corpus.
- [x] Fuentes primarias de Pathfinder (2 HTML + docx).
- [x] EID de los 10 identificados.
- [ ] Recuperar bibliografía base (Silberschatz, Stallings, etc.).
- [ ] Exportación Scopus única de los 10.
- [ ] Registrar los 10 en `references.bib` con metadatos completos.
- [ ] Rehacer o descartar la figura de VOSviewer.

#### Fase 3 — Simulación (pendiente)
- [ ] I1: `model.py` + S0/S1.
- [ ] I2: S2/S3 (parche y control).
- [ ] I3: S4/S5 + figuras.
- [ ] I4: `sim/README.md` y reproducibilidad.
- [ ] I5: validación y límites.

#### Fase 4 — Redacción (pendiente)
- [ ] Introducción y Método.
- [ ] Desarrollo (por qué / cómo / solución) y validación.
- [ ] Discusión y Conclusiones.
- [ ] Resumen y keywords.
- [ ] Verificación de 5–10 páginas (`make count`).

#### Fase 5 — Presentación (pendiente)
- [ ] Slides en PDF.
- [ ] Guion de 10 minutos y banco de preguntas.
- [ ] Ensayo de los 5 indicadores de coevaluación.
- [ ] ZIP final y entrega del 29/11.

### 8.3. Bitácora

| Fecha | Agente | Archivos afectados | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md`, `docs/HISTORIAL.md`, `.gitignore`, `.git/`; eliminado `fuentes/analisis_bibliografico/Untitled Document` | Reestructuración de `AGENTS.md` en §0–§9: regla R0, definición del proyecto, corpus verificado, diseño del artículo, diseño de la simulación, inventario y protocolo. Historial anterior movido a `docs/HISTORIAL.md`. Repositorio Git inicializado (commit `b416dbd`) y eliminado archivo basura de 1 byte. | `AGENTS.md` con 9 secciones y referencias internas coherentes; `docs/HISTORIAL.md` con la tabla histórica; `./build.sh` sin errores; `main.pdf` = 2 páginas; `texcount` = 0 palabras de cuerpo. |
| **2026-10-31** | Codex | `fuentes/` | Descarga y lectura de las dos cuentas de Glenn E. Reeves (1997 y 1999); separadas del corpus Q1/Q2 por ser anteriores a 2020. | Fuentes locales verificadas. |
| **2026-10-31** | Codex | `fuentes/analisis_bibliografico/` | Cierre de trazabilidad: EID de Manjunath y Guasque; actualización de matriz; VOSviewer y RIS preparados. | 8/10 en CSV; 2 EID externos. |
| **2026-10-31** | Codex | `fuentes/`, `fuentes/analisis_bibliografico/` | Recopilación de 10 PDFs 2020–2025, matriz, ZIP, RIS/BibTeX y datos VOSviewer. | ZIP con 10 artículos; PDFs completos. |
| **2026-10-30** | OpenCode (DeepSeek V4.1 Flash) | Todo el repositorio | Reset integral del desarrollo FreeRTOS/IoT; esqueleto IEEE y `AGENTS.md` al estado de reinicio. | `main.pdf` = 2 páginas; 0 errores. |

> El historial anterior al 2026-10-30 está en `docs/HISTORIAL.md`.

### 8.4. Inventario de archivos

| Ruta | Tipo | Propósito | Estado | Última modificación |
| :--- | :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento maestro | Reglas, definición y estado | Activo | 2026-11-02 · OpenCode |
| `docs/HISTORIAL.md` | Archivo | Bitácora anterior | Activo | 2026-11-02 · OpenCode |
| `main.tex` | LaTeX | Carátula + artículo | Esqueleto | 2026-10-30 · OpenCode |
| `main.pdf` | PDF generado | Compilación de verificación | 2 páginas, 0 palabras de cuerpo | 2026-11-02 · OpenCode |
| `references.bib` | BibTeX | Citas | Vacío | 2026-10-30 · OpenCode |
| `IEEEtran.cls` / `.bst` | Clase/estilo | Formato IEEE | Estable | 2026-10-11 |
| `build.sh` / `Makefile` | Scripts | Compilación y conteo | Estable | 2026-10-30 |
| `img/logoLaSalleUniversidad.png` | Imagen | Logo de carátula | Estable | 2026-10-11 |
| `fuentes/*.pdf` | Corpus | 10 papers + copia ReTiF | Completo | 2026-11-01 |
| `fuentes/*.html` | Fuentes primarias | Reeves 1997/1999 | Completo | 2026-10-31 |
| `fuentes/Mars_Pathfinder_reinicios_1997.docx` | Notas | Síntesis interna (no citables) | Completo | 2026-10-31 |
| `fuentes/analisis_bibliografico/Matriz_Bibliografica_RTOS.xlsx` | Datos | Matriz bibliográfica | Completo | 2026-10-31 |
| `fuentes/analisis_bibliografico/Matriz_Rtos_10.csv` | Datos | Matriz en abierto | Completo | 2026-10-31 |
| `fuentes/analisis_bibliografico/scopus_10_original.csv` | Datos | Exportación Scopus (8/10) | Parcial | 2026-10-31 |
| `fuentes/analisis_bibliografico/RTOS_10_articulos_2020-2025.zip` | ZIP | Corpus final | Completo | 2026-10-31 |
| `fuentes/analisis_bibliografico/Referencias_Rtos.bib` | BibTeX | Borrador de citas | Parcial | 2026-10-31 |
| `fuentes/analisis_bibliografico/Referencias_Mendeley.ris` | RIS | Importación Mendeley | Completo | 2026-10-31 |
| `fuentes/analisis_bibliografico/VOSviewer_*` | Datos | Mapa bibliométrico | **Inconsistente** | 2026-10-31 |
| `sim/` | Código | Simulación | **Planificado** | — |
| `slides/` | Presentación | Slides | **Planificado** | — |
| `.gitignore` | Git | Exclusiones | Activo | 2026-11-02 · OpenCode |

---

## 9. Protocolo de actualización para futuros agentes

### 9.1. Antes de responder

1. Leer `AGENTS.md` completo, en especial §8.1 (estado) y §3 (definición).
2. Revisar el inventario §8.4 para no pisar trabajo existente.
3. Si hay conflicto entre el documento y el disco, corregir el documento.

### 9.2. Durante la ejecución

1. Respetar la tesis, las RQ y el presupuesto de §3 y §6.
2. No introducir afirmaciones sin fuente; distinguir primaria/secundaria.
3. No cambiar el alcance sin actualizar §3 y §6.
4. Mantener la simulación determinista y reproducible.

### 9.3. Al cerrar el turno (R0)

- [ ] ¿Creé, modifiqué, moví o eliminé archivos?
- [ ] ¿Añadí la fila en §8.3 con archivos y verificación?
- [ ] ¿Actualicé §8.4?
- [ ] ¿Actualicé §8.1 y §8.2?
- [ ] ¿Actualicé §3, §6 o §7 si cambió el alcance?
- [ ] ¿Compilé o verifiqué lo que corresponda?
- [ ] ¿Otro agente puede reproducir el turno con lo que quedó escrito?

### 9.4. Plantilla de entrada de bitácora

```markdown
| **AAAA-MM-DD** | Agente (modelo) | `ruta1`, `ruta2` | Qué se hizo y por qué | Cómo se verificó |
```

### 9.5. Plantilla de fila de inventario

```markdown
| `ruta` | Tipo | Propósito | Estado | AAAA-MM-DD · Agente |
```

---

*Fin del documento. Si estás leyendo esto y vas a modificar un archivo, la última sección que debes editar es §8.*

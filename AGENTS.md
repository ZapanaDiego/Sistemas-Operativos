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

> **CAMBIO DE ALCANCE (2026-11-02):** el entregable activo es el **film 3D** en `simulacion3D/` (documental mudo de 2:45–3:00). El artículo y el motor de simulación S0–S5 quedan **archivados**; el equipo asumió explícitamente el riesgo académico. La definición de §3.1–§3.9 se conserva como base factual del film. Ver `simulacion3D/AGENTS.md` y §8.1.

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

**Activo (2026-11-02):** film 3D en `simulacion3D/` (MP4 1080p, 2:45–3:00), entorno RTOS en `entornoRTOS/` y slides para la exposición. **Archivados:** artículo IEEE, motor S0–S5 y ZIP de los diez papers (este último se conserva como entregable oficial).

### 3.9. Criterios de éxito

**Activos (film):** MP4 1080p de 2:45–3:00; cadena causal comprensible sin texto; demo C reproduce reset y corrección; storyboard con fuentes por plano.

**Archivados:** S1–S3, respuestas RQ1–RQ3, 5–10 páginas y 10 papers citados.

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

### 4.6. Mapa de explotación del corpus

Este apartado responde, para cada fuente, tres preguntas: **cómo sirve al artículo**, **en qué páginas están las partes relevantes** y **con qué prioridad debe usarse**. Es la herramienta de consulta obligatoria antes de redactar cualquier sección.

#### 4.6.1. Escala de prioridad y convenciones

| Prioridad | Significado | Uso esperado |
| :---: | :--- | :--- |
| **5** | Imprescindible: sostiene una RQ o una sección central; sin ella el argumento queda incompleto | Cuerpo central (III, IV) |
| **4** | Muy importante: sostiene una lección o un dato clave; se cita en el cuerpo | Introducción, discusión |
| **3** | Apoyo: refuerza el marco teórico o el estado del arte; es sustituible | Sección II |
| **2** | Contextual: corroboración puntual o dato de misión | Introducción, notas |
| **1** | No citable: notas internas de estudio | Ninguna sección |

**Convención de páginas:** se indica `p. impresa / PDF N`. Cuando la revista paginan el artículo desde 1 (JSA), ambos coinciden y se escribe solo `p. N / PDF N`. En Springer, IEEE TC y *The Journal of Supercomputing* la página impresa no coincide con la del PDF y se dan ambos valores. En las fuentes HTML (Reeves) no hay páginas: se usa el encabezado de sección como ancla.

**Estado de lectura:** `Completo` = leído íntegro; `Secciones clave` = leídas las partes que el artículo usa; `Datos` = solo se verificaron datos puntuales.

**Verificación:** todas las anclas se comprobaron con `pdftotext` y `pdfinfo` el 2026-11-02. Si se descubre una página nueva, se actualiza la ficha correspondiente (R0).

#### 4.6.2. Tabla maestra

| ID | Fuente | Prioridad | Estado | Cómo sirve al artículo | Páginas / anclas | Sección |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| F01 | Reeves 1997 | **5** | Completo | Secuencia exacta del fallo, prioridades y reset | §"THE FAILURE" | IV-A, IV-B, IV-C |
| F02 | Reeves 1999 | **5** | Completo | Diagnóstico, corrección y parche | Párrafos "In less than 18 hours" y "In the end, we modified..." | IV-C |
| F03 | NASA | **4** | Datos | Aterrizaje, Sojourner y distinción lander/rover | Key Facts; Sojourner | I, III |
| F04 | NSSDC | **2** | Datos | Corroboración de fechas y masa | Launch/Arrival | I |
| F05 | AP 1997 | **2** | Datos | Fecha del parche (19/7) y reinicios | Párrafos 1–3 | I, IV-C |
| F06 | Dong et al. 2020 | **5** | Secciones clave | Único paper reciente sobre inversión de prioridades y `priority-swapping` | pp. 1, 4–6, 7–9 | II-C, IV-C, IV-E |
| F07 | Timerlat 2025 | **4** | Secciones clave | Observabilidad y descomposición de la latencia | pp. 2608, 2616–2618 | II-C, IV-E |
| F08 | Akesson et al. 2022 | **4** | Secciones clave | Brecha teoría-práctica (encuesta y quiz) | pp. 358, 367–371, 377–378, 385–391 | I, II-C, IV-E |
| F09 | ReTiF 2021 | **3** | Secciones clave | Acceso controlado al scheduling; configuración | pp. 1, 9–13, 15–16 | II-C, IV-E |
| F10 | Manjunath 2024 | **3** | Secciones clave | Verificación de código RTOS de bajo nivel | pp. 1, 3–10 | II-C, IV-E |
| F11 | Guasque et al. 2022 | **3** | Secciones clave | Cotas de planificabilidad con contención | pp. 14703, 14707–14723 | II-C |
| F12 | He et al. 2024 | **3** | Secciones clave | Trade-off garantía dura / recursos | pp. 291, 300–302, 318–322 | II-C, IV-E |
| F13 | Minaeva & Hanzálek 2021 | **3** | Secciones clave | Fundamento time-triggered y complejidad | pp. 1, 10, 15–22, 33–34 | II-A, II-C |
| F14 | Farina et al. 2023 | **3** | Secciones clave | Interferencia de memoria y aislamiento hardware | pp. 1, 3–12 | II-C, IV-E |
| F15 | Salman et al. 2022 | **2** | Secciones clave | Reservas y tareas elásticas | pp. 1–7 / PDF 1–7 | II-C |
| F16 | `Mars_Pathfinder_reinicios_1997.docx` | **1** | Completo | Notas internas; **no citable** | §1–§8 | Ninguna |

#### 4.6.3. Fichas detalladas

##### F01. Reeves, G. E. (1997-12-15). *What really happened on Mars?* — Prioridad 5

- **Qué es:** correo técnico del responsable del software de vuelo de JPL, escrito para corregir las versiones periodísticas del incidente.
- **Cómo sirve:** es la fuente primaria de RQ1 y RQ2. Describe la arquitectura, las prioridades, la secuencia exacta del bloqueo y la reacción del sistema.
- **Anclas:**
  - §"THE HARDWARE": VME, bus 1553, ciclo de 8 Hz.
  - §"THE SOFTWARE ARCHITECTURE": `bc_sched`, `bc_dist`, `ASI/MET`, ciclo t1–t5, uso de `select()`/`pipe()`.
  - §"THE FAILURE": mutex de `select()`, expropiación de `ASI/MET`, bloqueo de `bc_dist`, detección por `bc_sched`, reset.
  - §"HOW WE FOUND IT": traza, réplica de laboratorio, menos de 18 horas.
  - §"HOW WAS THE PROBLEM CORRECTED": opción de herencia de prioridad en `semMCreate`.
  - §"WHY DIDN'T WE CATCH IT BEFORE LAUNCH?": pruebas con el "mejor caso".
  - §"ANALYSIS AND LESSONS": lecciones sobre COTS y herramientas.
- **Claims citables:** `bc_sched` es la tarea de mayor prioridad (salvo `tExec`); `bc_dist` es la tercera; el ciclo es de 125 ms; el reset reinicializa hardware y software; los datos en RAM se conservan si no se pierde la alimentación; el fallo solo aparecía con `ASI/MET` activo y tareas medias cargadas.
- **Límite:** HTML sin paginación; no es un artículo arbitrado; no cubre el resto de la misión.
- **Sección destino:** IV-A, IV-B, IV-C.

##### F02. Reeves, G. E. (1999-11). *Priority Inversion: How We Found It, How We Fixed It.* — Prioridad 5

- **Qué es:** artículo de *Dr. Dobb's Journal* que amplía la cuenta de 1997 con el diagnóstico y la corrección.
- **Cómo sirve:** es la fuente primaria de RQ3. Explica la traza, la reproducción, la discusión interna y el parche.
- **Anclas (el HTML no tiene secciones; se citan párrafos):**
  - Párrafo "When the 'repeated reset problem'...": traza y reproducción en laboratorio.
  - Párrafo "In less than 18 hours...": aislamiento de `pipe()`/`select()`, diagnóstico y corrección.
  - Párrafo "The fix seemed straightforward...": opción de herencia en `semMCreate`.
  - Párrafo "In the end, we modified the global variable...": corrección, análisis de Wind River y pruebas.
- **Claims citables:** menos de 18 horas para reproducir y diagnosticar; la opción de herencia estaba desactivada por rendimiento; el cambio afectaba a todos los semáforos de `select()`; Wind River concluyó que el impacto era mínimo; la corrección resolvió el problema.
- **Límite:** HTML; versión resumida; no es arbitrado.
- **Sección destino:** IV-C.

##### F03. NASA. *Mars Pathfinder.* — Prioridad 4

- **Qué es:** página oficial de la misión.
- **Cómo sirve:** datos de contexto y la distinción entre el lander y el rover, necesaria para no atribuir el fallo a Sojourner.
- **Anclas:** *Key Facts* (aterrizaje 4/7/1997, Ares Vallis, fin de misión 27/9/1997); sección *Sojourner Rover* (despliegue el 5–6/7, sol 2).
- **Claims citables:** aterrizaje el 4 de julio de 1997; Sojourner rueda sobre la superficie el 6 de julio; el lander fue nombrado Carl Sagan Memorial Station.
- **Límite:** no describe el fallo del software.
- **Sección destino:** I, III.

##### F04. NSSDC. *Mars Pathfinder Project Information.* — Prioridad 2

- **Qué es:** ficha técnica de la NASA.
- **Cómo sirve:** corroboración de fechas y datos de la misión.
- **Anclas:** *Launch Date* (4/12/1996), *Arrival Date* (4/7/1997), párrafo del rover (6/7/1997, 05:40 UT).
- **Claims citables:** lanzamiento y llegada; el rover rueda el 6 de julio; masa del lander y del rover.
- **Límite:** no aporta al análisis del fallo.
- **Sección destino:** I.

##### F05. Associated Press (1997-07-18). *Pathfinder Glitch Found.* — Prioridad 2

- **Qué es:** nota de prensa contemporánea.
- **Cómo sirve:** ancla la fecha del parche y confirma que hubo varios reinicios.
- **Anclas:** titular y tres primeros párrafos.
- **Claims citables:** los ingenieros habían resuelto el problema el 17/7; el cambio se enviaría el sábado 19/7; dos reinicios habían retrasado el proyecto.
- **Límite:** fuente secundaria, sin detalle técnico.
- **Sección destino:** I, IV-C.

##### F06. Dong, P.; Jiang, Z.; Burns, A.; Ding, Y.; Ma, J. (2020). *Build real-time communication for hybrid dual-OS system.* — Prioridad 5

- **Qué es:** protocolo RTRG-RPC sobre TrustZone para un sistema dual-OS (RTOS en mundo seguro, GPOS en mundo normal).
- **Cómo sirve:** es el único artículo del corpus que aborda explícitamente la inversión de prioridades y propone un mecanismo concreto (`priority-swapping`) inspirado en herencia de prioridad. Es el puente entre Pathfinder y la literatura 2020–2025.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract y contribuciones; menciona la reducción de la inversión de prioridades.
  - `pp. 4–6 / PDF 4–6`: diseño de RTRG-RPC; descomposición del tiempo de respuesta; `priority-swapping`.
  - `pp. 7–9 / PDF 7–9`: evaluación (latencia, UnixBench).
  - `p. 9 / PDF 9`: conclusiones y límites.
- **Claims citables:** el `priority-swapping` intercambia la prioridad de la tarea llamadora con la tarea contenedora del GPOS; el mecanismo reduce la inversión; el tiempo de respuesta se descompone en `T_I + T_SS1 + T_G + T_SS2 + T_R`.
- **Límite:** prototipo ARM/TrustZone; no es un RTOS clásico; no reproduce Pathfinder.
- **Sección destino:** II-C, IV-C, IV-E.

##### F07. De Oliveira, D. B.; Casini, D.; Lelli, J.; Cucinotta, T. (2025). *Timerlat: Real-Time Linux Scheduling Latency Measurements, Tracing, and Analysis.* — Prioridad 4

- **Qué es:** herramienta integrada en *mainline* Linux para medir y diagnosticar latencia de planificación.
- **Cómo sirve:** sostiene la lección de observabilidad: sin descomponer la latencia no se puede diagnosticar el fallo. Es el equivalente moderno de la traza de Pathfinder.
- **Anclas:**
  - `p. 2608 / PDF 1`: abstract; tres latencias (IRQ, hilo, usuario); integración en mainline desde 5.17.
  - `pp. 2609–2612 / PDF 2–5`: análisis de latencia y arquitectura.
  - `pp. 2616–2617 / PDF 9–10`: resultados; máximos de 4454/26223/26229 µs sin PREEMPT_RT y 58 µs con RT; 10 µs en aislamiento.
  - `p. 2618 / PDF 11`: conclusiones; sobrecarga despreciable frente a cyclictest.
- **Claims citables:** la latencia se compone de IRQ, hilo y usuario; la configuración (PREEMPT_RT + aislamiento de núcleos) reduce los máximos de decenas de milisegundos a decenas de microsegundos; la sobrecarga es despreciable.
- **Límite:** Linux/PREEMPT_RT, no VxWorks; no integra contadores de hardware.
- **Sección destino:** II-C, IV-E.

##### F08. Akesson, B.; Nasri, M.; Nelissen, G.; Altmeyer, S.; Davis, R. I. (2022). *A comprehensive survey of industry practice in real-time systems.* — Prioridad 4

- **Qué es:** encuesta a 120 profesionales de sistemas de tiempo real.
- **Cómo sirve:** mide la brecha entre investigación y práctica; justifica por qué el caso de 1997 sigue siendo relevante.
- **Anclas:**
  - `p. 358 / PDF 1`: abstract; 120 profesionales.
  - `pp. 367–371 / PDF 10–14`: resultados; uso de SO (78,43 % RTOS/microkernel, 55,88 % Linux, 37,25 % bare metal, 62,7 % varios SO).
  - `pp. 377–378 / PDF 20–21`: políticas de planificación (prioridad fija 56,25 %, cíclico/tabla 54,17 %, EDF 16,67 %).
  - `pp. 385–389 / PDF 28–32`: quiz; académicos 27 %, industria 35,1 %, azar 33,3 %.
  - `pp. 390–391 / PDF 33–34`: conclusiones.
- **Claims citables:** la mayoría usa RTOS y varios SO; la prioridad fija domina; EDF es minoritario; los académicos rinden por debajo del azar en el quiz; no hay "bala de plata".
- **Límite:** muestra no probabilística; PDF local es el manuscrito aceptado.
- **Sección destino:** I, II-C, IV-E.

##### F09. Serra, G.; Ara, G.; Fara, P.; Cucinotta, T. (2021). *ReTiF: A declarative real-time scheduling framework for POSIX systems.* — Prioridad 3

- **Qué es:** framework declarativo para acceder al scheduling de tiempo real de un GPOS POSIX sin privilegios.
- **Cómo sirve:** muestra que el acceso al scheduling es un recurso mediado y configurable; apoya la lección de que la configuración forma parte de la corrección temporal.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract; API declarativa y plugins.
  - `pp. 9–12 / PDF 9–12`: modelo de control de acceso y políticas.
  - `p. 13 / PDF 13`: sobrecarga de IPC (~12 µs Intel, ~50 µs ARM).
  - `pp. 15–16 / PDF 15–16`: limitaciones (solo particionado; sin bloqueos, offsets ni dependencias; reutilización de TID).
  - `p. 16 / PDF 16`: conclusiones.
- **Claims citables:** permite acceso controlado a scheduling para aplicaciones sin privilegios; la sobrecarga es aceptable fuera de los bucles críticos; el framework no implementa análisis de bloqueo.
- **Límite:** POSIX/Linux; no VxWorks; modelo de tareas simplificado.
- **Sección destino:** II-C, IV-E.

##### F10. Manjunath, V.; Baunach, M. (2024). *A framework for static analysis and verification of low-level RTOS code.* — Prioridad 3

- **Qué es:** framework que reutiliza resultados de WCET/OTAWA para verificar código RTOS de bajo nivel.
- **Cómo sirve:** el fallo de Pathfinder vive en código de bajo nivel (sincronización, cambio de contexto); la verificación estática es una defensa complementaria a la herencia de prioridad.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract; OTAWA y efectos de hardware.
  - `pp. 3–7 / PDF 3–7`: metodología; CFG, resultados intermedios, restricciones.
  - `pp. 7–8 / PDF 7–8`: casos AUTOSAR (context switch) y FreeRTOS (arranque en AURIX TriCore).
  - `pp. 9–10 / PDF 9–10`: evaluación; relación lineal moderada entre tiempo de verificación y espacio de estados.
  - `p. 10 / PDF 10`: conclusión.
- **Claims citables:** detecta dependencias de sincronización fallidas y posibles carreras; verifica comportamiento libre de efectos secundarios; el análisis escala de forma lineal moderada.
- **Límite:** no modela caché/pipeline completo; depende de la ISA; no es una herramienta de producción.
- **Sección destino:** II-C, IV-E.

##### F11. Guasque, A.; Aceituno, J. M.; Balbastre, P.; Simó, J.; Crespo, A. (2022). *Schedulability analysis of dynamic priority real-time systems with contention.* — Prioridad 3

- **Qué es:** dos cotas de planificabilidad basadas en `dbf` para prioridades dinámicas y contención en multicore.
- **Cómo sirve:** la contención es la forma general del fenómeno que en Pathfinder aparece como inversión; muestra cuánto pesimismo introduce la cota.
- **Anclas:**
  - `p. 14703 / PDF 1`: abstract; dos aproximaciones.
  - `pp. 14707–14709 / PDF 5–7`: modelo de tareas y contención.
  - `pp. 14710–14716 / PDF 8–14`: `dbf'` y `dbf''`.
  - `pp. 14717–14722 / PDF 15–20`: evaluación; FFDU cae al 10 % desde 8 núcleos; WFDU ronda el 100 %; Wmin es el allocator más preciso.
  - `p. 14723 / PDF 21`: conclusiones.
- **Claims citables:** `dbf''` reduce el pesimismo de `dbf'`; la elección del allocator cambia la planificabilidad; Wmin es el más preciso porque considera la interferencia.
- **Límite:** modelo sintético; no mide el kernel.
- **Sección destino:** II-C.

##### F12. He, Q.; Sun, Y.; Jiang, X.; Lv, M.; Lee, J.; Guan, N. (2024). *Real-time scheduling for parallel tasks with resource reclamation.* — Prioridad 3

- **Qué es:** asignación tipo escalera para tareas DAG paralelas, con perfilado offline y monitorización online.
- **Cómo sirve:** cuantifica el costo de la garantía dura: la asignación rectangular desperdicia recursos; la escalera recupera parte sin romper el plazo.
- **Anclas:**
  - `p. 291 / PDF 1`: abstract; 48,3 % máximo y 37,8 % medio.
  - `pp. 292–294 / PDF 2–4`: introducción; federated scheduling y desperdicio.
  - `pp. 300–302 / PDF 10–12`: asignación tipo escalera.
  - `pp. 318–322 / PDF 28–32`: evaluación.
  - `p. 322 / PDF 32`: conclusión; una sola tarea dura; mixed-criticality como trabajo futuro.
- **Claims citables:** la asignación escalera recupera hasta 48,3 % más recursos que SAN y 37,8 % en promedio; mantiene las garantías duras; se limita a una tarea dura.
- **Límite:** simulación; una sola tarea dura; no aborda bloqueo.
- **Sección destino:** II-C, IV-E.

##### F13. Minaeva, A.; Hanzálek, Z. (2021). *Survey on Periodic Scheduling for Time-Triggered Hard Real-Time Systems.* — Prioridad 3

- **Qué es:** revisión de planificación periódica para sistemas *time-triggered*.
- **Cómo sirve:** da el fundamento del enfoque TT y su complejidad; es el contrapunto al enfoque event-triggered de VxWorks.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract; TT vs ET; notación de Graham; SMT.
  - `pp. 3–9 / PDF 3–9`: descripción y notación.
  - `p. 10 / PDF 10`: complejidad; NP-hard.
  - `pp. 15–22 / PDF 15–22`: soluciones (2D bin packing, ILP).
  - `pp. 33–34 / PDF 33–34`: conclusiones.
- **Claims citables:** la planificación TT es muy predecible pero la síntesis es NP-hard; la representación del problema y el tipo de recurso determinan la complejidad; SMT/ILP son las técnicas básicas.
- **Límite:** teoría; no un SO concreto; versión de autor con 45 pp. (paginación ACM 54(1):1–32).
- **Sección destino:** II-A, II-C.

##### F14. Farina, G.; Gala, G.; Cinque, M.; Fohler, G. (2023). *Enabling memory access isolation in real-time cloud systems using Intel's detection/regulation capabilities.* — Prioridad 3

- **Qué es:** detección y regulación de interferencia de memoria con Intel RDT (RPQ y MBA).
- **Cómo sirve:** muestra que la interferencia de hardware es otra fuente de fallo temporal y que el aislamiento se desplaza del scheduler al hardware.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract; interferencia de memoria.
  - `pp. 3–5 / PDF 3–5`: enfoque; ocupación de la RPQ.
  - `pp. 6–11 / PDF 6–11`: experimentos; 1/5 y 1/6 del periodo de regulación; MBA 70/80/90; peor caso reproducible.
  - `p. 12 / PDF 12`: conclusiones.
- **Claims citables:** la ocupación de la RPQ detecta el número de núcleos que acceden a memoria; en el mejor caso basta 1/5 del periodo; solo ciertos retardos MBA limitan de forma significativa; el peor caso es reproducible.
- **Límite:** un Xeon de 2.ª generación; cargas sintéticas; no es un RTOS.
- **Sección destino:** II-C, IV-E.

##### F15. Salman, S. M.; Papadopoulos, A. V.; Mubeen, S.; Nolte, T. (2022). *Multi-processor scheduling of elastic applications in compositional real-time systems.* — Prioridad 2

- **Qué es:** scheduling de tareas elásticas bajo reserva MPS en multiprocesador.
- **Cómo sirve:** aporta el concepto de reserva y de variación de carga, útil para el marco de aislamiento temporal, pero tangencial al caso.
- **Anclas:**
  - `p. 1 / PDF 1`: abstract; Q1–Q4.
  - `pp. 1–3 / PDF 1–3`: modelo elástico y MPS.
  - `pp. 4–6 / PDF 4–6`: evaluación.
  - `p. 7 / PDF 7`: conclusión; mejor en promedio, sin ganar en el peor caso.
- **Claims citables:** el enfoque es comparable al estado del arte en promedio; en el peor caso ninguno domina; falta evaluación en sistema real.
- **Límite:** sin sistema real; no aborda inversión de prioridades.
- **Sección destino:** II-C.

##### F16. `Mars_Pathfinder_reinicios_1997.docx` — Prioridad 1

- **Qué es:** síntesis interna en español, 910 palabras, con secciones §1–§8.
- **Cómo sirve:** notas de estudio y contraste; **no es una fuente citable**.
- **Anclas:** §3 (tareas), §4 (secuencia), §5 (mecanismos), §6 (diagnóstico).
- **Claims citables:** ninguno; se cita a Reeves.
- **Límite:** secundario, sin paginación, mezcla resumen y interpretación.
- **Sección destino:** ninguna.

#### 4.6.4. Matriz de cobertura por sección

| Sección del artículo | Fuentes principales | ¿Cobertura suficiente? |
| :--- | :--- | :--- |
| I. Introducción | F01, F03, F05, F08 | Sí |
| II-A. RTOS y prioridad fija | **bibliografía base pendiente**, F13 | **No** |
| II-B. Inversión y PIP | **bibliografía base pendiente**, F01, F06 | **No** |
| II-C. Estado del arte | F06–F15 | Sí |
| III. Método | F01, F02, F03, F05 | Sí |
| IV-A. Por qué falló | F01, F02, F06 | Sí |
| IV-B. Cómo falló | F01, F06, simulación S1 | Parcial (falta S1) |
| IV-C. Cómo se solucionó | F02, F06, simulación S2/S3 | Parcial (falta S2/S3) |
| IV-D. Validación | simulación S4/S5 | **No** (pendiente) |
| IV-E. Lecciones | F06, F07, F08, F09, F10, F12, F14 | Sí |
| V. Conclusiones | síntesis | Sí |

#### 4.6.5. Huecos y acciones

1. **Bibliografía base ausente:** sin Silberschatz, Stallings, Sha et al. (1990) y Liu & Layland (1973), las secciones II-A y II-B no tienen sustento teórico primario. **Acción:** recuperar y mapear páginas.
2. **Simulación no implementada:** IV-B, IV-C y IV-D dependen de S1–S5. **Acción:** ejecutar §7.7.
3. **Dos EID fuera de Scopus:** no afecta al texto, pero sí a la trazabilidad. **Acción:** exportación única por DOI.
4. **VOSviewer inconsistente:** no usar la figura actual. **Acción:** rehacer o descartar.
5. **Fuentes secundarias:** F04, F05 y F16 no deben sostener afirmaciones técnicas por sí solas.

#### 4.6.6. Regla de uso

Antes de redactar una sección, el agente debe:

1. Consultar la matriz de cobertura (§4.6.4) y elegir las fuentes con prioridad 5, 4 o 3.
2. Usar el ancla exacta de la ficha; **no citar de memoria**.
3. Si una afirmación no tiene ancla, no se escribe.
4. Si se descubre una página nueva o un claim nuevo, actualizar la ficha y la bitácora (R0).
5. No usar F16 como fuente; no usar F04/F05 como evidencia técnica.

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

> **ARCHIVADO (2026-11-02):** el artículo no es un entregable activo. Este apartado se conserva como referencia por si se retoma. El trabajo activo es el film 3D en `simulacion3D/`.

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

> **ARCHIVADO (2026-11-02):** el motor S0–S5 no es un entregable activo. La reproducción ejecutable del mecanismo se implementó en `entornoRTOS/` (C11) y el film en `simulacion3D/`. Este apartado se conserva como referencia.

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

- **Tópico:** fallo del RTOS de Mars Pathfinder; estudio de caso + reconstrucción visual.
- **Cambio de alcance:** el entregable activo es el **film 3D** en `simulacion3D/` (documental mudo de 2:45–3:00, 1080p, 24 fps). El artículo y el motor S0–S5 quedan **archivados**; el equipo asumió el riesgo académico (artículo 0/7). Ver `simulacion3D/AGENTS.md`.
- **Mapa de fuentes:** §4.6 se conserva como base factual del film (16 fichas con anclas verificadas).
- **Fase actual:** film en preproducción; entorno RTOS verificado (`make test` PASS); I0 (base técnica, texturas reales y medición de render) completada.
- **Próximo hito:** `simulacion3D/STORYBOARD.md` + `NARRACION.md` + animatic de 15–20 s.
- **Bloqueos:** ninguno.
- **Plantilla:** `main.tex` queda archivado (2 páginas, 0 palabras de cuerpo).
- **Git:** repositorio con historial; el nuevo directorio se registra en §8.3 y §8.4.
- **Riesgo principal:** tiempo de render (medido en la escena de prueba: 3,35–7,64 s/frame a 1080p) y claridad del film sin texto; riesgo académico asumido por ausencia de artículo.

### 8.2. Checklists

> **Nota 2026-11-02:** las fases 3 y 4 (simulación y redacción del artículo) quedan **archivadas** por el cambio de alcance. La Fase 5 (exposición) sigue vigente, con el film como pieza central. La fase activa es la **Fase 6 — Film 3D**.

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
- [x] Mapa de explotación del corpus (§4.6) con prioridades, páginas clave y matriz de cobertura.
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

#### Fase 5 — Presentación (adaptada: exposición con el film)
- [ ] Slides en PDF.
- [ ] Guion de 10 minutos y banco de preguntas.
- [ ] Ensayo de los 5 indicadores de coevaluación.
- [ ] ZIP final y entrega del 29/11.

#### Fase 6 — Film 3D (activa)
- [x] Crear `simulacion3D/AGENTS.md` con el contrato local.
- [x] Implementar `entornoRTOS/` y verificar S0–S3 con `make test`.
- [ ] Escribir `simulacion3D/STORYBOARD.md` con los 15 planos.
- [ ] Escribir `simulacion3D/NARRACION.md`.
- [ ] Construir animatic de 15–20 s.
- [ ] Modelar terreno, lander, rover y ciudad de tareas.
- [ ] Animar los 15 planos.
- [x] Generar texturas de código/terminal desde `entornoRTOS/`.
- [x] Render de prueba y medición de tiempo (escena base de I0).
- [ ] Draft 720p.
- [ ] Render final 1080p y MP4.
- [ ] Actualizar `AGENTS.md` global y hacer commit.

### 8.3. Bitácora

| Fecha | Agente | Archivos afectados | Cambio | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `simulacion3D/README.md`, `build_scene.py`, `render.sh`, `modules/`, `assets/code/`, `assets/fonts/`, `blender/pathfinder_failure.blend`, `out/spike/`, `simulacion3D/.gitignore`, `simulacion3D/AGENTS.md`, `AGENTS.md` | I0 del film: escena base EEVEE, texturas reales de código/terminal desde `entornoRTOS/`, medición de render y corrección de los nombres de salida. | 1080p 7,64 s en frío / 3,35 s con caché; 720p 1,24 s; `make_textures.py` OK; `py_compile` OK. |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `entornoRTOS/`, `simulacion3D/AGENTS.md`, `AGENTS.md` | Implementado el entorno RTOS determinista en C11 (`ucontext`), mutex con/sin PIP, `select()`, software de vuelo y pruebas S0–S3; `make test` PASS; actualizadas las referencias `../demo/` → `../entornoRTOS/`. | `make test`: S0 0, S1 3, S2 0, S3 0; trazas deterministas; `run-pip-off` RESET; `run-pip-on` OK. |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `simulacion3D/AGENTS.md`, `AGENTS.md` | Ampliado el contrato local con la secuencia completa del film (15 planos detallados), guion técnico, dirección de arte, pipeline, integración del demo C y criterios de aceptación. | `wc -l` = 803; 15 planos; tablas y secciones revisadas; `AGENTS.md` global sincronizado. |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `simulacion3D/AGENTS.md`, `AGENTS.md` | Creación del contrato local del film 3D y registro del cambio de alcance a "solo film" (artículo y motor S0–S5 archivados; riesgo académico asumido). | `ls -la simulacion3D`; contrato revisado; §3, §6, §7, §8.1, §8.2 y §8.4 actualizados. |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md` | Añadido §4.6 *Mapa de explotación del corpus*: escala 1–5, tabla maestra de 16 fuentes, fichas detalladas con anclas de página, matriz de cobertura por sección, huecos y regla de uso. | Anclas verificadas con `pdftotext` y `pdfinfo`; 16 fichas; matriz de cobertura; `./build.sh` sin cambios. |
| **2026-11-02** | OpenCode (DeepSeek V4.1 Flash) | `AGENTS.md`, `docs/HISTORIAL.md`, `.gitignore`, `.git/`; eliminado `fuentes/analisis_bibliografico/Untitled Document` | Reestructuración de `AGENTS.md` en §0–§9: regla R0, definición del proyecto, corpus verificado, diseño del artículo, diseño de la simulación, inventario y protocolo. Historial anterior movido a `docs/HISTORIAL.md`. Repositorio Git inicializado (commit `b416dbd`) y eliminado archivo basura de 1 byte. | `AGENTS.md` con 9 secciones y referencias internas coherentes; `docs/HISTORIAL.md` con la tabla histórica; `./build.sh` sin errores; `main.pdf` = 2 páginas; `texcount` = 0 palabras de cuerpo. |
| **2026-10-31** | Codex | `fuentes/` | Descarga y lectura de las dos cuentas de Glenn E. Reeves (1997 y 1999); separadas del corpus Q1/Q2 por ser anteriores a 2020. | Fuentes locales verificadas. |
| **2026-10-31** | Codex | `fuentes/analisis_bibliografico/` | Cierre de trazabilidad: EID de Manjunath y Guasque; actualización de matriz; VOSviewer y RIS preparados. | 8/10 en CSV; 2 EID externos. |
| **2026-10-31** | Codex | `fuentes/`, `fuentes/analisis_bibliografico/` | Recopilación de 10 PDFs 2020–2025, matriz, ZIP, RIS/BibTeX y datos VOSviewer. | ZIP con 10 artículos; PDFs completos. |
| **2026-10-30** | OpenCode (DeepSeek V4.1 Flash) | Todo el repositorio | Reset integral del desarrollo FreeRTOS/IoT; esqueleto IEEE y `AGENTS.md` al estado de reinicio. | `main.pdf` = 2 páginas; 0 errores. |

> El historial anterior al 2026-10-30 está en `docs/HISTORIAL.md`.

### 8.4. Inventario de archivos

| Ruta | Tipo | Propósito | Estado | Última modificación |
| :--- | :--- | :--- | :--- | :--- |
| `AGENTS.md` | Documento maestro | Reglas, definición, estado y mapa de fuentes | Activo; incluye §4.6 | 2026-11-02 · OpenCode |
| `docs/HISTORIAL.md` | Archivo | Bitácora anterior | Activo | 2026-11-02 · OpenCode |
| `main.tex` | LaTeX | Carátula + artículo | Archivado (alcance solo film) | 2026-10-30 · OpenCode |
| `main.pdf` | PDF generado | Compilación de verificación | Archivado; 2 páginas | 2026-11-02 · OpenCode |
| `references.bib` | BibTeX | Citas | Archivado; vacío | 2026-10-30 · OpenCode |
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
| `sim/` | Código | Motor S0–S5 | **Archivado** (sustituido por el film) | — |
| `entornoRTOS/` | Código | Entorno RTOS modelo + software de vuelo; S0–S3 | **Completo** | 2026-11-02 · OpenCode |
| `entornoRTOS/AGENTS.md` | Documento | Contrato local del entorno RTOS | Activo | 2026-11-02 · OpenCode |
| `simulacion3D/AGENTS.md` | Documento | Contrato local completo: secuencia de 15 planos, producción, pipeline y R0 | Activo; I0 registrada | 2026-11-02 · OpenCode |
| `simulacion3D/README.md` | Documento | Build, render y medición de I0 | Activo | 2026-11-02 · OpenCode |
| `simulacion3D/build_scene.py` | Python | Escena base y frame de prueba | Activo (I0) | 2026-11-02 · OpenCode |
| `simulacion3D/render.sh` | Script | Envoltorio de build, test y render por plano | Activo | 2026-11-02 · OpenCode |
| `simulacion3D/modules/` | Python | `cameras`, `materials`, `render`; faltan terrain/lander/rover/tasks | Parcial | 2026-11-02 · OpenCode |
| `simulacion3D/blender/pathfinder_failure.blend` | Blender | Proyecto editable (escena base) | Activo (I0) | 2026-11-02 · OpenCode |
| `simulacion3D/assets/code/` | Imágenes/Script | Texturas reales de código/terminal y generador | Activo | 2026-11-02 · OpenCode |
| `simulacion3D/assets/fonts/` | Fuentes | DejaVu Sans Mono | Activo | 2026-11-02 · OpenCode |
| `simulacion3D/out/spike/` | PNG | Frames de prueba (ignorados por git) | Activo | 2026-11-02 · OpenCode |
| `slides/` | Presentación | Slides de la exposición | Pendiente (exposición) | — |
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

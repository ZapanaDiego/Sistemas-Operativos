# Plan de trabajo por iteraciones — RTOS y fallos temporales

Alcance autorizado: búsqueda de fuentes, descarga de PDFs y preparación de los datos de investigación en `fuentes/`. No se redactó el artículo del curso.

## Iteración 1 — Organización de fuentes — completada

- Los diez PDFs seleccionados quedaron directamente en `fuentes/`, sin carpeta de artículos.
- Se conservó el ZIP original obtenido desde Scopus en `analisis_bibliografico/` y se creó un segundo ZIP con el corpus final de diez PDFs.
- El documento Word histórico sobre Mars Pathfinder permanece en la raíz de `fuentes/` como contexto del problema.

## Iteración 2 — Selección y descarga — completada

Corpus de artículos arbitrados publicados entre 2020 y 2025. El cuartil corresponde a la revista/fuente, no a cada artículo; la matriz registra la clasificación disponible para 2025 por categoría.

1. ReTiF: A declarative real-time scheduling framework for POSIX systems (2021).
2. Real-time scheduling for parallel tasks with resource reclamation (2024).
3. A comprehensive survey of industry practice in real-time systems (2022).
4. Multi-processor scheduling of elastic applications in compositional real-time systems (2022).
5. Enabling memory access isolation in real-time cloud systems using Intel's detection/regulation capabilities (2023).
6. Survey on Periodic Scheduling for Time-Triggered Hard Real-Time Systems (2022).
7. Build real-time communication for hybrid dual-OS system (2020).
8. Timerlat: Real-Time Linux Scheduling Latency Measurements, Tracing, and Analysis (2025).
9. A framework for static analysis and verification of low-level RTOS code (2024).
10. Schedulability analysis of dynamic priority real-time systems with contention (2022).

Se eligieron copias abiertas o disponibles mediante la descarga institucional autorizada. Dos registros de la búsqueda inicial (RT-AIDE y el enfoque weakly-hard de Choi et al.) se dejaron fuera del ZIP final al no completar su descarga de texto completo en esta sesión; se incorporaron dos artículos abiertos sobre verificación de RTOS y prioridades dinámicas. Sus EID se recuperaron después desde metadatos públicos y se añadieron a la matriz; todavía falta incorporarlos a una nueva exportación institucional de Scopus.

## Iteración 3 — Datos y matriz — completada

- Se preservó la exportación original de Scopus de diez resultados como CSV y como ZIP de descarga de artículos.
- Se creó una matriz XLSX con autores, año, países, objetivo, método, resultados, DOI, PDF, cuartil y estado/EID de Scopus; el libro conserva el CSV original en una hoja aparte.
- También se creó una versión CSV de la matriz para lectura e intercambio. Los DOI y los identificadores de fuente Scopus aparecen en las filas.
- Los ocho artículos seleccionados presentes en la exportación original retienen su EID. Los dos artículos añadidos tienen EID identificados en metadatos públicos y fichas Scopus enlazadas en la matriz; el CSV original sigue sin esos registros.

## Iteración 4 — VOSviewer y Mendeley — preparada

- Se generaron los archivos `VOSviewer_Scopus_keywords.map`, `.net` y `VOSviewer_Scopus_keywords_thesaurus.txt` a partir de las palabras clave de los diez resultados originales de Scopus (umbral: dos apariciones). La red contiene once términos y 42 enlaces.
- Se generaron vistas previas SVG de la red y la densidad. Son vistas de preparación para inspección; no se presentan como capturas de la aplicación VOSviewer. Los `.map` y `.net` se pueden abrir en VOSviewer y cambiar a *Density Visualization*.
- Se prepararon referencias RIS y BibTeX para importar el corpus final en Mendeley. La importación en una cuenta personal no se ejecutó desde esta sesión.

## Iteración 5 — Cierre y límites — completada

- Se comprobó que los diez PDFs seleccionados están completos y se empaquetaron en `RTOS_10_articulos_2020-2025.zip`.
- El ranking de cuartiles es el ranking de fuente disponible para 2025 y puede variar por categoría. Debe volverse a validar en Scopus si cambia el año de evaluación.
- La consulta original devolvió solo diez registros; la frase de búsqueda no quedó guardada en el CSV. Para dejar una exportación Scopus única que corresponda exactamente a los diez PDFs, conviene ejecutar una búsqueda nueva por DOI/rango 2020–2026 e incluir los dos artículos añadidos.

# Corpus de investigación: RTOS y fallos de planificación

Este paquete reúne diez artículos de revista publicados entre 2020 y 2025 para el tema de sistemas operativos de tiempo real y el análisis de fallos temporales como el caso de Mars Pathfinder. Los PDFs de los artículos están en la raíz de `fuentes/`; los archivos de análisis están aquí.

La raíz contiene los diez PDFs seleccionados y una copia adicional de ReTiF extraída del ZIP original de Scopus. El ZIP final incluye una sola copia de cada uno de los diez artículos seleccionados.

## Archivos

- `Matriz_Bibliografica_RTOS.xlsx`: resumen, matriz analítica y exportación original de Scopus en hojas separadas.
- `Matriz_Rtos_10.csv`: matriz en formato abierto.
- `scopus_10_original.csv`: exportación original de Scopus con los diez resultados iniciales, resúmenes, afiliaciones, palabras clave, EID y DOI.
- `Scopus_01Nov2026_02-32-36.4be4d241.zip`: ZIP descargado desde Scopus; se conserva como registro de la descarga.
- `RTOS_10_articulos_2020-2025.zip`: ZIP con una copia de cada uno de los diez PDFs seleccionados.
- `Referencias_Mendeley.ris` y `Referencias_Rtos.bib`: datos bibliográficos listos para importar en Mendeley.
- `VOSviewer_Scopus_keywords.map`, `VOSviewer_Scopus_keywords.net` y `VOSviewer_Scopus_keywords_thesaurus.txt`: mapa, enlaces y tesauro derivados de las palabras clave de la exportación original de Scopus.
- `VOSviewer_previsualizacion_red.svg` y `VOSviewer_previsualizacion_densidad.svg`: vistas previas para revisar los términos y su densidad.
- `PLAN_TRABAJO.md`: registro de las iteraciones y límites.

## Cuartiles y registro Scopus

Q1/Q2 describen la posición de la **revista/fuente** dentro de una categoría y un año; no son una calificación intrínseca del artículo. La columna de cuartil indica el mejor cuartil disponible en la clasificación Scopus de 2025 y muestra la categoría cuando importa. La categoría puede cambiar el cuartil, como en *The Journal of Supercomputing* (Q1 en Computer Science: Theoretical Computer Science; Q2 en Hardware and Architecture). Para JSA, la página de la fuente informa CiteScore 2025 y Q1; Real-Time Systems aparece Q2 en la clasificación actual; ACM Computing Surveys aparece Q1. [JSA](https://journalindexes.com/journal-of-systems-architecture-13837621/) · [Real-Time Systems](https://researchjournalrank.com/journal/real-time-systems) · [ACM Computing Surveys](https://library.wur.nl/WebQuery/uvabrowser/132) · [The Journal of Supercomputing](https://journalindexes.com/journal-of-supercomputing-09208542/).

La exportación institucional inicial contiene ocho de los artículos finales y conserva sus EID; los otros dos resultados de esa búsqueda no están en el corpus final. Los EID de los dos artículos incorporados posteriormente ya se identificaron en metadatos públicos: `2-s2.0-85198027358` para Manjunath y Baunach, y `2-s2.0-85127724315` para Guasque et al. Se añadieron a la matriz y se enlazaron sus fichas Scopus, pero esos registros aún no forman parte del CSV original: para obtener un único CSV institucional coherente con los diez PDFs hay que repetir en Scopus la búsqueda por DOI y exportar los diez registros seleccionados. El primer identificador aparece en la ficha de [TU Graz/ElsevierPure](https://tugraz.elsevierpure.com/en/publications/a-framework-for-static-analysis-and-verification-of-low-level-rto/); el segundo figura en el [perfil ORCID de un coautor con datos de Scopus](https://orcid.org/0000-0002-6606-7406). Para consultar una fuente ya presente en el CSV original: [IEEE Transactions on Computers, fuente Scopus](https://www.scopus.com/sourceid/25033).

## VOSviewer

La red se construyó con las palabras clave de autor e indexadas en los diez resultados de la exportación original; el umbral fue dos apariciones. Se conservaron once términos y 42 enlaces. Para inspeccionarla, abre VOSviewer, selecciona **Open** e indica `VOSviewer_Scopus_keywords.map` y `VOSviewer_Scopus_keywords.net`. Cambia a **Density Visualization** para ver la superficie de densidad. Puedes importar además el archivo de tesauro. Las vistas SVG son previas para revisión; el mapa final de VOSviewer debe guardarse desde la aplicación tras ajustar sus opciones.

La vista de VOSviewer representa los diez resultados de la búsqueda inicial, dos de los cuales no quedaron en el ZIP final por falta de un PDF completo disponible en esta sesión. No mezclar esa red exploratoria con las estadísticas del corpus final sin actualizar la exportación.

## Mendeley

En Mendeley Reference Manager usa **Add new → Import library → RIS** y selecciona `Referencias_Mendeley.ris`. No se inició sesión ni se importó en la biblioteca personal desde esta sesión. El archivo BibTeX se conserva como alternativa.

## Alcance de la búsqueda

El archivo de Scopus conserva los diez resultados originales. No incluye la cadena literal de consulta usada en esa sesión; por ello, se debe repetir la consulta en Scopus para generar una exportación institucional definitiva de los diez artículos seleccionados, ya con los dos DOI/EID añadidos. No se usó Web of Science en esta recopilación. El contenido no se cargó fuera del espacio de investigación local.

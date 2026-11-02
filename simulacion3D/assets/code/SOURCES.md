# Fuentes de las texturas de código y terminal

Las tres imágenes de `assets/code/` se generan con `make_textures.py` a partir
de archivos reales de `../entornoRTOS/`. No se inventan líneas ni salidas.

## `code_panel.png`

| Archivo | Líneas | Contenido |
| :--- | :--- | :--- |
| `entornoRTOS/src/pipe.c` | 65–67, 72–74, 76–77, 95 | `rtos_select()`, toma y libera el mutex interno |
| `entornoRTOS/src/scenario.c` | 43–50 | creación del mutex compartido con `cfg->pip` |
| `entornoRTOS/include/vxworks_like.h` | 15–17 | `semMCreate()` y `SEM_INVERSION_SAFE` |

Los renglones `...` marcan omisiones deliberadas; los números de línea
corresponden al archivo original. Los resaltados ámbar, rojo y verde son
recursos visuales, no texto añadido.

## `terminal_off.png`

- Comando: `make run-pip-off` (objetivo real de `entornoRTOS/Makefile`).
- Salida de consola: ejecución real de `./entornoRTOS --scenario s1`.
- Traza: líneas exactas de `entornoRTOS/out/s1_pip_off.txt` en la ventana
  0,499–0,625 s, más la línea `# SUMMARY`.

## `terminal_on.png`

- Comando: `make run-pip-on`.
- Salida de consola: ejecución real de `./entornoRTOS --scenario s2`.
- Traza: líneas exactas de `entornoRTOS/out/s2_pip_on.txt` en la ventana
  0,499–0,506 s, más la línea `# SUMMARY`.

## Regeneración

```bash
python3 assets/code/make_textures.py
```

Requiere que `entornoRTOS` esté compilado (`make` en ese directorio) y que las
trazas `out/s1_pip_off.txt` y `out/s2_pip_on.txt` existan.

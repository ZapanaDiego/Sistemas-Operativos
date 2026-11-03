#ifndef TRACE_H
#define TRACE_H

#include <stdio.h>
#include "rtos.h"

void trace_init(FILE *out, const char *scenario, int pip, int shared);
void trace_event_at(const char *file, int line, const char *func,
                    const char *event, const task_t *t, const char *fmt, ...);
void trace_snapshot(void);
void trace_summary(int resets, uint64_t max_block_us, int deadline_misses);
void trace_close(void);

/*
 * La macro captura el punto de origen para que el visualizador pueda
 * resaltar la línea C que produjo cada evento.
 */
#define trace_event(event, t, ...) \
    trace_event_at(__FILE__, __LINE__, __func__, (event), (t), __VA_ARGS__)

#endif

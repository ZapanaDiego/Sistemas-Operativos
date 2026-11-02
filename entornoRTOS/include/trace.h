#ifndef TRACE_H
#define TRACE_H

#include <stdio.h>
#include "rtos.h"

void trace_init(FILE *out, const char *scenario, int pip, int shared);
void trace_event(const char *event, const task_t *t, const char *fmt, ...);
void trace_summary(int resets, uint64_t max_block_us, int deadline_misses);
void trace_close(void);

#endif

#include "trace.h"
#include "config.h"
#include "rtos.h"

#include <stdarg.h>
#include <stdio.h>

static FILE *trace_out;
static int trace_owned;

void trace_init(FILE *out, const char *scenario, int pip, int shared) {
    if (out) {
        trace_out = out;
        trace_owned = 0;
    } else {
        trace_out = fopen("/dev/null", "w");
        trace_owned = 1;
    }
    if (!trace_out) {
        return;
    }
    fprintf(trace_out, "# Pathfinder RTOS model - scenario %s\n", scenario);
    fprintf(trace_out, "# pip=%d shared=%d duration=%.6fs\n",
            pip, shared, (double)SIM_DURATION_US / 1000000.0);
}

void trace_event(const char *event, const task_t *t, const char *fmt, ...) {
    if (!trace_out) {
        return;
    }
    double sec = (double)rtos_now_us() / 1000000.0;
    fprintf(trace_out, "[%9.6f] %-7s", sec, event);
    if (t) {
        fprintf(trace_out, " %-8s prio=%d", t->name, t->effective_priority);
    } else {
        fprintf(trace_out, " %-8s        ", "-");
    }
    if (fmt && *fmt) {
        va_list ap;
        va_start(ap, fmt);
        fputc(' ', trace_out);
        vfprintf(trace_out, fmt, ap);
        va_end(ap);
    }
    fputc('\n', trace_out);
}

void trace_summary(int resets, uint64_t max_block_us, int deadline_misses) {
    if (!trace_out) {
        return;
    }
    fprintf(trace_out,
            "# SUMMARY resets=%d max_block_ms=%.3f deadline_misses=%d\n",
            resets, (double)max_block_us / 1000.0, deadline_misses);
    fflush(trace_out);
}

void trace_close(void) {
    if (trace_out && trace_owned) {
        fclose(trace_out);
    }
    trace_out = NULL;
    trace_owned = 0;
}

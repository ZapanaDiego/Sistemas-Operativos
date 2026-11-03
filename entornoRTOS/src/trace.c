#include "trace.h"
#include "config.h"
#include "rtos.h"
#include "sem.h"
#include "bus1553.h"
#include "flight_sw.h"

#include <ctype.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define MAX_TRACE_EVENTS 2048
#define MAX_DETAIL 256
#define MAX_NAME 32

typedef struct {
    char name[MAX_NAME];
    char state[16];
    int base_priority;
    int effective_priority;
    char waiting[MAX_NAME];
} task_snap_t;

typedef struct {
    char name[MAX_NAME];
    char owner[MAX_NAME];
    int pip;
    int nwaiters;
    char waiters[MAX_TASKS][MAX_NAME];
} sem_snap_t;

typedef struct {
    uint64_t t;
    char type[16];
    char task[MAX_NAME];
    int prio;
    char file[64];
    int line;
    char func[64];
    char detail[MAX_DETAIL];
    char current[MAX_NAME];
    int bus_cycle;
    int resets;
    int misses;
    int n_tasks;
    task_snap_t tasks[MAX_TASKS];
    int n_sems;
    sem_snap_t sems[MAX_SEMS];
} trace_record_t;

static FILE *trace_out;
static int trace_owned;
static int data_active;
static char scenario_name[16];
static int scenario_pip;
static int scenario_shared;
static int record_count;
static trace_record_t records[MAX_TRACE_EVENTS];
static uint64_t last_snapshot_us;

static int summary_resets;
static int summary_misses;
static uint64_t summary_max_block_us;

static const char *state_name(task_state_t state) {
    switch (state) {
        case TASK_READY:   return "READY";
        case TASK_RUNNING: return "RUNNING";
        case TASK_BLOCKED: return "BLOCKED";
        case TASK_SLEEPING:return "SLEEPING";
        case TASK_DEAD:    return "DEAD";
        default:           return "?";
    }
}

static void capture_snapshot(trace_record_t *r) {
    task_t *cur = rtos_current();
    snprintf(r->current, sizeof(r->current), "%s", cur ? cur->name : "");
    r->bus_cycle = bus1553_cycle_count();
    r->resets = rtos_reset_count();
    r->misses = flight_deadline_misses;
    r->n_tasks = rtos_task_count();
    if (r->n_tasks > MAX_TASKS) {
        r->n_tasks = MAX_TASKS;
    }
    for (int i = 0; i < r->n_tasks; i++) {
        task_t *t = rtos_task_at(i);
        task_snap_t *dst = &r->tasks[i];
        if (!t) {
            memset(dst, 0, sizeof(*dst));
            continue;
        }
        snprintf(dst->name, sizeof(dst->name), "%s", t->name ? t->name : "");
        snprintf(dst->state, sizeof(dst->state), "%s", state_name(t->state));
        dst->base_priority = t->base_priority;
        dst->effective_priority = t->effective_priority;
        snprintf(dst->waiting, sizeof(dst->waiting), "%s",
                 t->waiting_on ? t->waiting_on->name : "");
    }

    r->n_sems = sem_total();
    if (r->n_sems > MAX_SEMS) {
        r->n_sems = MAX_SEMS;
    }
    for (int i = 0; i < r->n_sems; i++) {
        sem_t *s = sem_at(i);
        sem_snap_t *dst = &r->sems[i];
        if (!s) {
            memset(dst, 0, sizeof(*dst));
            continue;
        }
        snprintf(dst->name, sizeof(dst->name), "%s", s->name ? s->name : "");
        snprintf(dst->owner, sizeof(dst->owner), "%s",
                 s->owner ? s->owner->name : "");
        dst->pip = s->pip;
        dst->nwaiters = s->nwaiters;
        if (dst->nwaiters > MAX_TASKS) {
            dst->nwaiters = MAX_TASKS;
        }
        for (int j = 0; j < dst->nwaiters; j++) {
            snprintf(dst->waiters[j], sizeof(dst->waiters[j]), "%s",
                     s->waiters[j]->name ? s->waiters[j]->name : "");
        }
    }
}

static trace_record_t *next_record(void) {
    if (record_count >= MAX_TRACE_EVENTS) {
        return NULL;
    }
    trace_record_t *r = &records[record_count++];
    memset(r, 0, sizeof(*r));
    return r;
}

void trace_init(FILE *out, const char *scenario, int pip, int shared) {
    if (out) {
        trace_out = out;
        trace_owned = 0;
    } else {
        trace_out = fopen("/dev/null", "w");
        trace_owned = 1;
    }
    snprintf(scenario_name, sizeof(scenario_name), "%s", scenario ? scenario : "?");
    scenario_pip = pip;
    scenario_shared = shared;
    data_active = 1;
    record_count = 0;
    last_snapshot_us = 0;
    summary_resets = 0;
    summary_misses = 0;
    summary_max_block_us = 0;
    if (!trace_out) {
        return;
    }
    fprintf(trace_out, "# Pathfinder RTOS model - scenario %s\n", scenario_name);
    fprintf(trace_out, "# pip=%d shared=%d duration=%.6fs\n",
            pip, shared, (double)SIM_DURATION_US / 1000000.0);
}

void trace_event_at(const char *file, int line, const char *func,
                    const char *event, const task_t *t, const char *fmt, ...) {
    if (!trace_out && !data_active) {
        return;
    }

    char detail[MAX_DETAIL];
    detail[0] = '\0';
    if (fmt && *fmt) {
        va_list ap;
        va_start(ap, fmt);
        vsnprintf(detail, sizeof(detail), fmt, ap);
        va_end(ap);
    }

    const char *ev = event ? event : "";
    int text_visible = strcmp(ev, "SWITCH") != 0 && strcmp(ev, "BUS") != 0;
    if (trace_out && text_visible) {
        double sec = (double)rtos_now_us() / 1000000.0;
        fprintf(trace_out, "[%9.6f] %-7s", sec, ev);
        if (t) {
            fprintf(trace_out, " %-8s prio=%d", t->name, t->effective_priority);
        } else {
            fprintf(trace_out, " %-8s        ", "-");
        }
        if (detail[0]) {
            fprintf(trace_out, " %s", detail);
        }
        fputc('\n', trace_out);
    }

    if (!data_active) {
        return;
    }
    trace_record_t *r = next_record();
    if (!r) {
        return;
    }
    r->t = rtos_now_us();
    snprintf(r->type, sizeof(r->type), "%s", event ? event : "");
    snprintf(r->task, sizeof(r->task), "%s", t ? t->name : "");
    r->prio = t ? t->effective_priority : 0;
    snprintf(r->file, sizeof(r->file), "%s", file ? file : "");
    r->line = line;
    snprintf(r->func, sizeof(r->func), "%s", func ? func : "");
    snprintf(r->detail, sizeof(r->detail), "%s", detail);
    capture_snapshot(r);
}

void trace_snapshot(void) {
    if (!data_active) {
        return;
    }
    uint64_t now = rtos_now_us();
    if (now - last_snapshot_us < 10000) {
        return;
    }
    last_snapshot_us = now;
    trace_record_t *r = next_record();
    if (!r) {
        return;
    }
    r->t = now;
    snprintf(r->type, sizeof(r->type), "SNAP");
    capture_snapshot(r);
}

void trace_summary(int resets, uint64_t max_block_us, int deadline_misses) {
    summary_resets = resets;
    summary_max_block_us = max_block_us;
    summary_misses = deadline_misses;
    if (!trace_out) {
        return;
    }
    fprintf(trace_out,
            "# SUMMARY resets=%d max_block_ms=%.3f deadline_misses=%d\n",
            resets, (double)max_block_us / 1000.0, deadline_misses);
    fflush(trace_out);
}

static void json_string(FILE *f, const char *s) {
    fputc('"', f);
    if (!s) {
        s = "";
    }
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        switch (*p) {
            case '"':  fputs("\\\"", f); break;
            case '\\': fputs("\\\\", f); break;
            case '\n': fputs("\\n", f); break;
            case '\r': fputs("\\r", f); break;
            case '\t': fputs("\\t", f); break;
            default:
                if (*p < 0x20) {
                    fprintf(f, "\\u%04x", *p);
                } else {
                    fputc(*p, f);
                }
                break;
        }
    }
    fputc('"', f);
}

static char *read_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) {
        char *empty = malloc(1);
        if (empty) {
            empty[0] = '\0';
        }
        return empty;
    }
    if (fseek(f, 0, SEEK_END) != 0) {
        fclose(f);
        return NULL;
    }
    long n = ftell(f);
    if (n < 0) {
        n = 0;
    }
    if (fseek(f, 0, SEEK_SET) != 0) {
        fclose(f);
        return NULL;
    }
    char *buf = malloc((size_t)n + 1);
    if (!buf) {
        fclose(f);
        return NULL;
    }
    size_t got = fread(buf, 1, (size_t)n, f);
    buf[got] = '\0';
    fclose(f);
    return buf;
}

static void write_sources(FILE *f) {
    static const char *files[] = {
        "src/rtos.c",
        "src/sem.c",
        "src/pipe.c",
        "src/bus1553.c",
        "src/flight_sw.c",
        "src/scenario.c",
        "src/trace.c",
        "src/main.c",
        "src/switch.S",
        "include/config.h",
        "include/rtos.h",
        "include/sem.h",
        "include/pipe.h",
        "include/bus1553.h",
        "include/flight_sw.h",
        "include/scenario.h",
        "include/trace.h",
        "include/vxworks_like.h"
    };
    fputs("\"sources\":{", f);
    size_t n = sizeof(files) / sizeof(files[0]);
    for (size_t i = 0; i < n; i++) {
        if (i > 0) {
            fputc(',', f);
        }
        json_string(f, files[i]);
        fputc(':', f);
        char *text = read_file(files[i]);
        if (!text) {
            json_string(f, "");
        } else {
            json_string(f, text);
            free(text);
        }
    }
    fputc('}', f);
}

static void write_text_file_field(FILE *f, const char *key, const char *path) {
    json_string(f, key);
    fputc(':', f);
    char *text = read_file(path);
    if (!text) {
        json_string(f, "");
    } else {
        json_string(f, text);
        free(text);
    }
}

static void write_data_file(void) {
    if (!data_active) {
        return;
    }
    mkdir("out", 0755);

    char lower[16];
    size_t i = 0;
    for (; scenario_name[i] && i < sizeof(lower) - 1; i++) {
        lower[i] = (char)tolower((unsigned char)scenario_name[i]);
    }
    lower[i] = '\0';

    char path[128];
    snprintf(path, sizeof(path), "out/%s_data.js", lower);
    FILE *f = fopen(path, "w");
    if (!f) {
        return;
    }

    fputs("window.SCENARIOS = window.SCENARIOS || {};\n", f);
    fprintf(f, "window.SCENARIOS[\"%s\"] = {\n", scenario_name);
    fputs("\"scenario\":", f);
    json_string(f, scenario_name);
    fprintf(f, ",\n\"pip\":%d,\n\"shared\":%d,\n\"duration_us\":%llu,\n",
            scenario_pip, scenario_shared, (unsigned long long)SIM_DURATION_US);
    fprintf(f,
            "\"summary\":{\"resets\":%d,\"max_block_ms\":%.3f,"
            "\"deadline_misses\":%d},\n",
            summary_resets, (double)summary_max_block_us / 1000.0,
            summary_misses);

    fputs("\"events\":[\n", f);
    for (int e = 0; e < record_count; e++) {
        trace_record_t *r = &records[e];
        if (e > 0) {
            fputc(',', f);
        }
        fprintf(f, "{\"t\":%llu,\"type\":", (unsigned long long)r->t);
        json_string(f, r->type);
        fputs(",\"task\":", f);
        json_string(f, r->task);
        fprintf(f, ",\"prio\":%d,\"file\":", r->prio);
        json_string(f, r->file);
        fprintf(f, ",\"line\":%d,\"func\":", r->line);
        json_string(f, r->func);
        fputs(",\"detail\":", f);
        json_string(f, r->detail);
        fputs(",\"snap\":{\"current\":", f);
        json_string(f, r->current);
        fprintf(f, ",\"bus_cycle\":%d,\"resets\":%d,\"misses\":%d,\"tasks\":[",
                r->bus_cycle, r->resets, r->misses);
        for (int t = 0; t < r->n_tasks; t++) {
            task_snap_t *ts = &r->tasks[t];
            if (t > 0) {
                fputc(',', f);
            }
            fputs("{\"name\":", f);
            json_string(f, ts->name);
            fputs(",\"state\":", f);
            json_string(f, ts->state);
            fprintf(f, ",\"base\":%d,\"eff\":%d,\"waiting\":",
                    ts->base_priority, ts->effective_priority);
            json_string(f, ts->waiting);
            fputc('}', f);
        }
        fputs("],\"sems\":[", f);
        for (int s = 0; s < r->n_sems; s++) {
            sem_snap_t *ss = &r->sems[s];
            if (s > 0) {
                fputc(',', f);
            }
            fputs("{\"name\":", f);
            json_string(f, ss->name);
            fputs(",\"owner\":", f);
            json_string(f, ss->owner);
            fprintf(f, ",\"pip\":%d,\"waiters\":[", ss->pip);
            for (int w = 0; w < ss->nwaiters; w++) {
                if (w > 0) {
                    fputc(',', f);
                }
                json_string(f, ss->waiters[w]);
            }
            fputs("]}", f);
        }
        fputs("]}}", f);
    }
    fputs("\n],\n", f);

    write_sources(f);
    fputs(",\n", f);
    write_text_file_field(f, "asm", "src/switch.S");
    fputs(",\n", f);
    write_text_file_field(f, "disasm", "out/disasm.txt");
    fputs("\n};\n", f);
    fclose(f);
}

void trace_close(void) {
    write_data_file();
    if (trace_out && trace_owned) {
        fclose(trace_out);
    }
    trace_out = NULL;
    trace_owned = 0;
    data_active = 0;
}

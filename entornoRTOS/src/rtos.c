#include "rtos.h"
#include "sem.h"
#include "pipe.h"
#include "trace.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Cambio de contexto definido en src/switch.S. */
extern void rtos_switch(void **old_sp, void *new_sp);

#define STACK_CANARY 0x5A5A5A5A5A5A5A5AULL

static task_t task_pool[MAX_TASKS];
static _Alignas(16) char task_stacks[MAX_TASKS][STACK_SIZE];
static int task_count;
static task_t *current;
static uint64_t sim_time_us;
static int stop_flag;
static int reset_count;
static void *sched_sp;

static void task_trampoline(void);

static task_t *pick_next(void) {
    task_t *best = NULL;
    for (int i = 0; i < task_count; i++) {
        task_t *t = &task_pool[i];
        if (t->state != TASK_READY) {
            continue;
        }
        if (best == NULL ||
            t->effective_priority < best->effective_priority ||
            (t->effective_priority == best->effective_priority && t->id < best->id)) {
            best = t;
        }
    }
    return best;
}

static void wake_sleepers(void) {
    for (int i = 0; i < task_count; i++) {
        task_t *t = &task_pool[i];
        if ((t->state == TASK_SLEEPING || t->state == TASK_BLOCKED) &&
            t->wake_time_us != 0 && t->wake_time_us <= sim_time_us) {
            int was_blocked = (t->state == TASK_BLOCKED);
            t->wake_time_us = 0;
            t->state = TASK_READY;
            t->wake_reason = was_blocked ? 1 : 0;
        }
    }
}

static int advance_to_next_event(void) {
    uint64_t next = UINT64_MAX;
    for (int i = 0; i < task_count; i++) {
        task_t *t = &task_pool[i];
        if ((t->state == TASK_SLEEPING || t->state == TASK_BLOCKED) &&
            t->wake_time_us != 0 && t->wake_time_us < next) {
            next = t->wake_time_us;
        }
    }
    if (next == UINT64_MAX) {
        return 0;
    }
    if (next > sim_time_us) {
        sim_time_us = next;
    }
    wake_sleepers();
    return 1;
}

/*
 * Prepara la pila inicial de una tarea.
 *
 * El layout, desde sp hacia arriba, es:
 *   [r15][r14][r13][r12][rbx][rbp][return address][padding]
 *
 * rtos_switch hace pop de los seis registros y luego `ret`, que salta a
 * task_trampoline. sp queda alineado a 16 bytes y la entrada a la función
 * cumple la alineación de System V (rsp % 16 == 8).
 */
static void task_stack_init(task_t *t) {
    uintptr_t top = (uintptr_t)(task_stacks[t->id] + STACK_SIZE);
    top &= ~(uintptr_t)0xF;
    uint64_t *frame = (uint64_t *)(top - 64);
    for (int i = 0; i < 6; i++) {
        frame[i] = 0;
    }
    frame[6] = (uint64_t)(uintptr_t)task_trampoline;
    frame[7] = 0;
    t->sp = (void *)frame;
}

static void task_trampoline(void) {
    task_t *t = current;
    if (t) {
        t->entry();
        t->state = TASK_DEAD;
    }
    rtos_schedule();
}

static void scheduler(void) {
    for (;;) {
        if (stop_flag) {
            return;
        }
        task_t *next = pick_next();
        if (next == NULL) {
            if (!advance_to_next_event()) {
                return;
            }
            continue;
        }
        task_t *prev = current;
        if (prev && prev->state == TASK_RUNNING) {
            prev->state = TASK_READY;
        }
        current = next;
        next->state = TASK_RUNNING;
        trace_event("SWITCH", next, "from=%s", prev ? prev->name : "-");
        rtos_switch(&sched_sp, next->sp);
    }
}

void rtos_init(void) {
    memset(task_pool, 0, sizeof(task_pool));
    memset(task_stacks, 0, sizeof(task_stacks));
    task_count = 0;
    current = NULL;
    sim_time_us = 0;
    stop_flag = 0;
    reset_count = 0;
    sched_sp = NULL;
    sem_global_reset();
    pipe_global_reset();
}

task_t *task_spawn(const char *name, int priority, void (*entry)(void)) {
    if (task_count >= MAX_TASKS) {
        return NULL;
    }
    int id = task_count;
    task_t *t = &task_pool[id];
    memset(t, 0, sizeof(*t));
    t->id = id;
    t->name = name;
    t->base_priority = priority;
    t->effective_priority = priority;
    t->state = TASK_READY;
    t->entry = entry;
    t->wake_reason = 0;
    t->started = 0;
    *(uint64_t *)task_stacks[id] = STACK_CANARY;
    task_stack_init(t);
    task_count++;
    trace_event("SPAWN", t, "%s", name);
    return t;
}

void task_delay(uint64_t us) {
    if (!current) {
        return;
    }
    current->wake_time_us = sim_time_us + us;
    current->wake_reason = 0;
    current->state = TASK_SLEEPING;
    rtos_schedule();
}

void task_yield(void) {
    if (!current) {
        return;
    }
    current->state = TASK_READY;
    rtos_schedule();
}

void cpu_work(uint64_t us) {
    uint64_t remaining = us;
    while (remaining > 0) {
        uint64_t step = remaining > 50 ? 50 : remaining;
        sim_time_us += step;
        remaining -= step;
        wake_sleepers();
        trace_snapshot();
        task_t *next = pick_next();
        if (next && current && next->effective_priority < current->effective_priority) {
            if (strcmp(current->name, "asi_met") == 0) {
                trace_event("PREEMPT", current, "%s", next->name);
            }
            current->state = TASK_READY;
            rtos_schedule();
        }
    }
}

void rtos_run(void) {
    scheduler();
}

void rtos_stop(void) {
    stop_flag = 1;
    if (current) {
        current->state = TASK_READY;
        rtos_schedule();
    }
}

void rtos_reset(void) {
    reset_count++;
    sem_reset_all();
    for (int i = 0; i < task_count; i++) {
        task_pool[i].effective_priority = task_pool[i].base_priority;
    }
    for (int i = 0; i < task_count; i++) {
        task_t *t = &task_pool[i];
        if (t->state == TASK_BLOCKED) {
            t->state = TASK_READY;
            t->waiting_on = NULL;
            t->wake_time_us = 0;
            t->wake_reason = 2;
        }
    }
    trace_event("RESET", current, "watchdog");
}

void rtos_schedule(void) {
    if (current && sched_sp) {
        rtos_switch(&current->sp, sched_sp);
    }
}

uint64_t rtos_now_us(void) {
    return sim_time_us;
}

int rtos_reset_count(void) {
    return reset_count;
}

task_t *rtos_current(void) {
    return current;
}

int rtos_task_count(void) {
    return task_count;
}

task_t *rtos_task_at(int index) {
    if (index < 0 || index >= task_count) {
        return NULL;
    }
    return &task_pool[index];
}

int rtos_check_stacks(void) {
    int bad = 0;
    for (int i = 0; i < task_count; i++) {
        if (*(uint64_t *)task_stacks[i] != STACK_CANARY) {
            bad++;
        }
    }
    return bad;
}

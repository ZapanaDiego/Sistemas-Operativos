#include "rtos.h"
#include "sem.h"
#include "pipe.h"
#include "trace.h"

#include <stdio.h>
#include <string.h>

static task_t task_pool[MAX_TASKS];
static char task_stacks[MAX_TASKS][STACK_SIZE];
static int task_count;
static task_t *current;
static uint64_t sim_time_us;
static int stop_flag;
static int reset_count;
static ucontext_t sched_ctx;
static task_t *spawn_task;

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

static void task_trampoline(void) {
    task_t *t = spawn_task;
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
        if (next != current) {
            if (current && current->state == TASK_RUNNING) {
                current->state = TASK_READY;
            }
            current = next;
        }
        next->state = TASK_RUNNING;
        if (!next->started) {
            next->started = 1;
            spawn_task = next;
        }
        swapcontext(&sched_ctx, &next->ctx);
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
    spawn_task = NULL;
    memset(&sched_ctx, 0, sizeof(sched_ctx));
    sem_global_reset();
    pipe_global_reset();
}

task_t *task_spawn(const char *name, int priority, void (*entry)(void)) {
    if (task_count >= MAX_TASKS) {
        return NULL;
    }
    memset(&task_pool[task_count], 0, sizeof(task_pool[task_count]));
    task_pool[task_count].id = task_count;
    task_pool[task_count].name = name;
    task_pool[task_count].base_priority = priority;
    task_pool[task_count].effective_priority = priority;
    task_pool[task_count].state = TASK_READY;
    task_pool[task_count].entry = entry;
    task_pool[task_count].wake_reason = 0;
    task_pool[task_count].started = 0;
    if (getcontext(&task_pool[task_count].ctx) != 0) {
        perror("getcontext");
        return NULL;
    }
    task_pool[task_count].ctx.uc_stack.ss_sp = task_stacks[task_count];
    task_pool[task_count].ctx.uc_stack.ss_size = STACK_SIZE;
    task_pool[task_count].ctx.uc_link = NULL;
    makecontext(&task_pool[task_count].ctx, task_trampoline, 0);
    task_t *spawned = &task_pool[task_count];
    task_count++;
    trace_event("SPAWN", spawned, "%s", name);
    return spawned;
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
    uint64_t end = sim_time_us + us;
    while (sim_time_us < end) {
        uint64_t step = end - sim_time_us;
        if (step > 50) {
            step = 50;
        }
        sim_time_us += step;
        wake_sleepers();
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
    if (current) {
        swapcontext(&current->ctx, &sched_ctx);
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

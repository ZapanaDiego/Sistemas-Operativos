#include "sem.h"
#include "rtos.h"
#include "trace.h"

#include <string.h>

static sem_t sem_pool[MAX_SEMS];
static int sem_count;

static sem_t *sem_create(const char *name, sem_type_t type, int pip) {
    if (sem_count >= MAX_SEMS) {
        return NULL;
    }
    sem_t *s = &sem_pool[sem_count];
    memset(s, 0, sizeof(*s));
    s->id = sem_count++;
    s->name = name;
    s->type = type;
    s->pip = pip;
    s->owner = NULL;
    s->count = 0;
    s->nwaiters = 0;
    return s;
}

sem_t *sem_mcreate(const char *name, int pip) {
    return sem_create(name, SEM_TYPE_MUTEX, pip);
}

sem_t *sem_bcreate(const char *name) {
    return sem_create(name, SEM_TYPE_BINARY, 0);
}

static void remove_waiter(sem_t *sem, task_t *t) {
    for (int i = 0; i < sem->nwaiters; i++) {
        if (sem->waiters[i] == t) {
            for (int j = i; j < sem->nwaiters - 1; j++) {
                sem->waiters[j] = sem->waiters[j + 1];
            }
            sem->nwaiters--;
            return;
        }
    }
}

static task_t *highest_waiter(sem_t *sem) {
    task_t *best = NULL;
    for (int i = 0; i < sem->nwaiters; i++) {
        task_t *t = sem->waiters[i];
        if (best == NULL ||
            t->effective_priority < best->effective_priority ||
            (t->effective_priority == best->effective_priority && t->id < best->id)) {
            best = t;
        }
    }
    return best;
}

void sem_update_priority(task_t *t) {
    if (!t) {
        return;
    }
    int p = t->base_priority;
    for (int i = 0; i < sem_count; i++) {
        sem_t *s = &sem_pool[i];
        if (s->type != SEM_TYPE_MUTEX || s->owner != t) {
            continue;
        }
        for (int j = 0; j < s->nwaiters; j++) {
            if (s->waiters[j]->effective_priority < p) {
                p = s->waiters[j]->effective_priority;
            }
        }
    }
    t->effective_priority = p;
}

static int block_current(sem_t *sem, uint64_t timeout_us) {
    task_t *cur = rtos_current();
    if (!cur || sem->nwaiters >= MAX_TASKS) {
        return -1;
    }
    cur->state = TASK_BLOCKED;
    cur->waiting_on = sem;
    cur->wake_reason = 0;
    cur->wake_time_us = (timeout_us == WAIT_FOREVER) ? 0 : rtos_now_us() + timeout_us;
    sem->waiters[sem->nwaiters++] = cur;
    trace_event("WAIT", cur, "%s", sem->name);
    return 0;
}

int sem_take(sem_t *sem, uint64_t timeout_us) {
    task_t *cur = rtos_current();
    if (!sem || !cur) {
        return -1;
    }

    if (sem->type == SEM_TYPE_BINARY) {
        if (sem->count > 0) {
            sem->count = 0;
            return 0;
        }
        if (block_current(sem, timeout_us) != 0) {
            return -1;
        }
        rtos_schedule();
        if (cur->wake_reason == 1) {
            remove_waiter(sem, cur);
            cur->waiting_on = NULL;
            return -1;
        }
        if (cur->wake_reason == 2) {
            cur->waiting_on = NULL;
            return -1;
        }
        cur->waiting_on = NULL;
        return 0;
    }

    if (sem->owner == NULL) {
        sem->owner = cur;
        sem->count = 1;
        trace_event("LOCK", cur, "%s", sem->name);
        return 0;
    }
    if (sem->owner == cur) {
        sem->count++;
        return 0;
    }

    if (block_current(sem, timeout_us) != 0) {
        return -1;
    }
    if (sem->pip) {
        sem_update_priority(sem->owner);
        trace_event("INHERIT", sem->owner, "%s", sem->name);
    }
    rtos_schedule();
    if (cur->wake_reason == 1) {
        remove_waiter(sem, cur);
        cur->waiting_on = NULL;
        if (sem->pip) {
            sem_update_priority(sem->owner);
        }
        return -1;
    }
    if (cur->wake_reason == 2) {
        cur->waiting_on = NULL;
        return -1;
    }
    cur->waiting_on = NULL;
    return 0;
}

int sem_give(sem_t *sem) {
    task_t *cur = rtos_current();
    if (!sem || !cur) {
        return -1;
    }

    if (sem->type == SEM_TYPE_BINARY) {
        if (sem->nwaiters > 0) {
            task_t *next = highest_waiter(sem);
            remove_waiter(sem, next);
            next->state = TASK_READY;
            next->waiting_on = NULL;
            next->wake_reason = 0;
            trace_event("WAKE", next, "%s", sem->name);
            if (next->effective_priority < cur->effective_priority) {
                cur->state = TASK_READY;
                rtos_schedule();
            }
        } else {
            sem->count = 1;
        }
        return 0;
    }

    if (sem->owner != cur) {
        if (cur->lost_mutex) {
            cur->lost_mutex = 0;
            trace_event("UNWIND", cur, "%s", sem->name);
            return 0;
        }
        trace_event("GIVE_ERR", cur, "%s", sem->name);
        return -1;
    }
    if (sem->count > 1) {
        sem->count--;
        return 0;
    }

    trace_event("UNLOCK", cur, "%s", sem->name);
    if (sem->nwaiters > 0) {
        task_t *next = highest_waiter(sem);
        remove_waiter(sem, next);
        sem->owner = next;
        sem->count = 1;
        next->state = TASK_READY;
        next->waiting_on = NULL;
        next->wake_reason = 0;
        trace_event("WAKE", next, "%s", sem->name);
        if (sem->pip) {
            sem_update_priority(next);
        }
        sem_update_priority(cur);
        if (next->effective_priority < cur->effective_priority) {
            cur->state = TASK_READY;
            rtos_schedule();
        }
    } else {
        sem->owner = NULL;
        sem->count = 0;
        sem_update_priority(cur);
    }
    return 0;
}

void sem_reset_all(void) {
    for (int i = 0; i < sem_count; i++) {
        if (sem_pool[i].owner) {
            sem_pool[i].owner->lost_mutex = 1;
        }
        sem_pool[i].owner = NULL;
        sem_pool[i].count = 0;
        sem_pool[i].nwaiters = 0;
    }
}

void sem_global_reset(void) {
    memset(sem_pool, 0, sizeof(sem_pool));
    sem_count = 0;
}

int sem_total(void) {
    return sem_count;
}

sem_t *sem_at(int index) {
    if (index < 0 || index >= sem_count) {
        return NULL;
    }
    return &sem_pool[index];
}

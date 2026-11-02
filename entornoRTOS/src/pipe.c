#include "pipe.h"
#include "rtos.h"
#include "trace.h"

#include <string.h>

static pipe_t pipe_pool[MAX_PIPES];
static int pipe_count;

pipe_t *pipe_create(void) {
    if (pipe_count >= MAX_PIPES) {
        return NULL;
    }
    pipe_t *p = &pipe_pool[pipe_count];
    memset(p, 0, sizeof(*p));
    p->id = pipe_count++;
    p->head = 0;
    p->tail = 0;
    p->count = 0;
    return p;
}

int pipe_has_data(const pipe_t *p) {
    return p && p->count > 0;
}

int pipe_has_space(const pipe_t *p) {
    return p && p->count < PIPE_SIZE;
}

int pipe_write(pipe_t *p, const void *data, int len) {
    if (!p || !data || len <= 0) {
        return 0;
    }
    const uint8_t *src = (const uint8_t *)data;
    int n = len;
    if (n > PIPE_SIZE - p->count) {
        n = PIPE_SIZE - p->count;
    }
    for (int i = 0; i < n; i++) {
        p->buf[p->tail] = src[i];
        p->tail = (p->tail + 1) % PIPE_SIZE;
        p->count++;
    }
    return n;
}

int pipe_read(pipe_t *p, void *data, int len) {
    if (!p || !data || len <= 0) {
        return 0;
    }
    uint8_t *dst = (uint8_t *)data;
    int n = len;
    if (n > p->count) {
        n = p->count;
    }
    for (int i = 0; i < n; i++) {
        dst[i] = p->buf[p->head];
        p->head = (p->head + 1) % PIPE_SIZE;
        p->count--;
    }
    return n;
}

int rtos_select(sem_t *mutex, pipe_t *p, int nfds,
                rtos_fd_set *readfds, rtos_fd_set *writefds,
                uint64_t timeout_us) {
    (void)nfds;
    if (!mutex || !p) {
        return -1;
    }
    if (sem_take(mutex, WAIT_FOREVER) != 0) {
        return -1;
    }

    /* Sección crítica que modela el mutex interno de select(). */
    cpu_work(SELECT_WCET_US);

    int ready = 0;
    if (readfds) {
        RTOS_FD_ZERO(readfds);
        if (pipe_has_data(p)) {
            RTOS_FD_SET(p->id, readfds);
            ready = 1;
        }
    }
    if (writefds) {
        RTOS_FD_ZERO(writefds);
        if (pipe_has_space(p)) {
            RTOS_FD_SET(p->id, writefds);
            ready = 1;
        }
    }

    sem_give(mutex);

    if (!ready && timeout_us != 0 && timeout_us != WAIT_FOREVER) {
        task_delay(timeout_us);
    }
    return ready;
}

void pipe_global_reset(void) {
    memset(pipe_pool, 0, sizeof(pipe_pool));
    pipe_count = 0;
}

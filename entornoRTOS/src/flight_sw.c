#include "flight_sw.h"
#include "vxworks_like.h"
#include "trace.h"

volatile int bc_dist_done = 1;
int flight_deadline_misses = 0;

static sem_t *g_asi_mutex;
static sem_t *g_dist_mutex;
static pipe_t *g_pipe;
static sem_t *g_bus_sem;
static uint64_t g_med3_wcet_us;
static uint64_t g_max_block_us;

static rtos_fd_set g_rfds;
static rtos_fd_set g_wfds;
static uint8_t g_packet[64];
static uint8_t g_data[64];

static void wait_until(uint64_t t) {
    uint64_t now = rtos_now_us();
    if (t > now) {
        task_delay(t - now);
    }
}

void flight_sw_init(sem_t *asi_mutex, sem_t *dist_mutex, pipe_t *pipe,
                    sem_t *bus_sem, uint64_t med3_wcet_us) {
    g_asi_mutex = asi_mutex;
    g_dist_mutex = dist_mutex;
    g_pipe = pipe;
    g_bus_sem = bus_sem;
    g_med3_wcet_us = med3_wcet_us;
    g_max_block_us = 0;
    bc_dist_done = 1;
    flight_deadline_misses = 0;
}

uint64_t flight_max_block_us(void) {
    return g_max_block_us;
}

void bc_sched(void) {
    uint64_t next = CYCLE_US;
    for (;;) {
        wait_until(next);
        next += CYCLE_US;

        if (!bc_dist_done) {
            flight_deadline_misses++;
            trace_event("MISS", rtos_current(), "bc_dist");
            rtos_reset();
            bc_dist_done = 1;
        }

        bc_dist_done = 0;
        semGive(g_bus_sem);
        cpu_work(BC_SCHED_WCET_US);
    }
}

void bc_dist(void) {
    for (;;) {
        if (semTake(g_bus_sem, WAIT_FOREVER) != 0) {
            bc_dist_done = 1;
            continue;
        }

        RTOS_FD_ZERO(&g_wfds);
        uint64_t t0 = rtos_now_us();
        int rc = rtos_select(g_dist_mutex, g_pipe, g_pipe->id + 1,
                             NULL, &g_wfds, WAIT_FOREVER);
        uint64_t dt = rtos_now_us() - t0;
        if (dt > g_max_block_us) {
            g_max_block_us = dt;
        }

        if (rc < 0) {
            bc_dist_done = 1;
            continue;
        }

        pipe_write(g_pipe, g_packet, (int)sizeof(g_packet));
        cpu_work(BC_DIST_WCET_US);
        bc_dist_done = 1;
    }
}

void asi_met(void) {
    uint64_t next = ASI_PHASE_US;
    for (;;) {
        wait_until(next);
        next += ASI_PERIOD_US;

        RTOS_FD_ZERO(&g_rfds);
        (void)rtos_select(g_asi_mutex, g_pipe, g_pipe->id + 1,
                          &g_rfds, NULL, WAIT_FOREVER);
        (void)pipe_read(g_pipe, g_data, (int)sizeof(g_data));
    }
}

static void med_task(uint64_t period_us, uint64_t wcet_us) {
    uint64_t next = 0;
    for (;;) {
        wait_until(next);
        next += period_us;
        cpu_work(wcet_us);
    }
}

void med_1(void) {
    med_task(MED1_PERIOD_US, MED1_WCET_US);
}

void med_2(void) {
    med_task(MED2_PERIOD_US, MED2_WCET_US);
}

void med_3(void) {
    uint64_t next = 0;
    for (;;) {
        wait_until(next);
        next += MED3_PERIOD_US;
        trace_event("BURST", rtos_current(), "compression");
        cpu_work(g_med3_wcet_us);
    }
}

void t_exec(void) {
    for (;;) {
        task_delay(1000000ULL);
    }
}

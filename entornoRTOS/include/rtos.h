#ifndef RTOS_H
#define RTOS_H

#include <stdint.h>
#include "config.h"

typedef enum {
    TASK_READY = 0,
    TASK_RUNNING,
    TASK_BLOCKED,
    TASK_SLEEPING,
    TASK_DEAD
} task_state_t;

typedef struct sem sem_t;

typedef struct task {
    int id;
    const char *name;
    int base_priority;
    int effective_priority;
    task_state_t state;
    void *sp;                    /* stack pointer guardado por switch.S */
    void (*entry)(void);
    uint64_t wake_time_us;
    int wake_reason;             /* 0 normal, 1 timeout, 2 reset */
    sem_t *waiting_on;
    int started;
    int lost_mutex;              /* el reset invalidó un mutex que tenía tomado */
} task_t;

void rtos_init(void);
task_t *task_spawn(const char *name, int priority, void (*entry)(void));
void task_delay(uint64_t us);
void task_yield(void);
void cpu_work(uint64_t us);
void rtos_run(void);
void rtos_stop(void);
void rtos_reset(void);
void rtos_schedule(void);

uint64_t rtos_now_us(void);
int rtos_reset_count(void);
task_t *rtos_current(void);
int rtos_task_count(void);
task_t *rtos_task_at(int index);
int rtos_check_stacks(void);

#endif

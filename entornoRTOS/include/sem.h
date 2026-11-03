#ifndef SEM_H
#define SEM_H

#include "rtos.h"

typedef enum {
    SEM_TYPE_MUTEX = 0,
    SEM_TYPE_BINARY
} sem_type_t;

struct sem {
    int id;
    const char *name;
    sem_type_t type;
    int pip;
    task_t *owner;
    int count;
    task_t *waiters[MAX_TASKS];
    int nwaiters;
};

sem_t *sem_mcreate(const char *name, int pip);
sem_t *sem_bcreate(const char *name);
int sem_take(sem_t *sem, uint64_t timeout_us);
int sem_give(sem_t *sem);
void sem_update_priority(task_t *t);
void sem_reset_all(void);
void sem_global_reset(void);
int sem_total(void);
sem_t *sem_at(int index);

#endif

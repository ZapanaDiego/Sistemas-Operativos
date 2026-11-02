#ifndef VXWORKS_LIKE_H
#define VXWORKS_LIKE_H

#include "rtos.h"
#include "sem.h"
#include "pipe.h"

#define SEM_Q_PRIORITY 0x1
#define SEM_INVERSION_SAFE 0x2

#ifndef WAIT_FOREVER
#define WAIT_FOREVER UINT64_MAX
#endif

static inline sem_t *semMCreate(const char *name, int options) {
    return sem_mcreate(name, (options & SEM_INVERSION_SAFE) != 0);
}

static inline sem_t *semBCreate(const char *name) {
    return sem_bcreate(name);
}

static inline int semTake(sem_t *sem, uint64_t timeout_us) {
    return sem_take(sem, timeout_us);
}

static inline int semGive(sem_t *sem) {
    return sem_give(sem);
}

static inline void taskDelay(uint64_t us) {
    task_delay(us);
}

static inline void taskSpawn(const char *name, int prio, void (*entry)(void)) {
    (void)task_spawn(name, prio, entry);
}

#endif

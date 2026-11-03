#include "bus1553.h"
#include "sem.h"
#include "rtos.h"
#include "trace.h"

static sem_t *bus_sem;
static int cycle_count;

void bus1553_init(void) {
    bus_sem = sem_bcreate("bus_sem");
    cycle_count = 0;
}

void bus1553_cycle(void) {
    cycle_count++;
    if (bus_sem) {
        sem_give(bus_sem);
    }
    trace_event("BUS", rtos_current(), "cycle=%d", cycle_count);
}

int bus1553_wait(void) {
    if (!bus_sem) {
        return -1;
    }
    return sem_take(bus_sem, WAIT_FOREVER);
}

int bus1553_cycle_count(void) {
    return cycle_count;
}

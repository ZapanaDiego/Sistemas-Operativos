#ifndef CONFIG_H
#define CONFIG_H

#include <stdint.h>

#define MAX_TASKS 10
#define MAX_SEMS 8
#define MAX_PIPES 4
#define STACK_SIZE (64 * 1024)

#define WAIT_FOREVER UINT64_MAX

/* Tiempo simulado en microsegundos. */
#define SIM_DURATION_US 2000000ULL
#define CYCLE_US 125000ULL

/* ASI/MET: despierta justo antes del ciclo de 500 ms para tomar el mutex. */
#define ASI_PHASE_US 499000ULL
#define ASI_PERIOD_US 500000ULL

/* Sección crítica de select(): ventana donde ASI/MET puede ser expropiada. */
#define SELECT_WCET_US 3000ULL

#define BC_DIST_WCET_US 2000ULL
#define BC_SCHED_WCET_US 100ULL

#define MED1_PERIOD_US 20000ULL
#define MED1_WCET_US 3000ULL
#define MED2_PERIOD_US 25000ULL
#define MED2_WCET_US 4000ULL
#define MED3_PERIOD_US 500000ULL
#define MED3_WCET_HIGH_US 150000ULL
#define MED3_WCET_LOW_US 5000ULL

typedef enum {
    SCENARIO_S0 = 0,
    SCENARIO_S1,
    SCENARIO_S2,
    SCENARIO_S3
} scenario_id_t;

typedef struct {
    scenario_id_t id;
    const char *name;
    int pip;
    int shared_mutex;
    uint64_t med3_wcet_us;
} scenario_config_t;

#endif

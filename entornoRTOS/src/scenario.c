#include "scenario.h"
#include "rtos.h"
#include "sem.h"
#include "pipe.h"
#include "bus1553.h"
#include "flight_sw.h"
#include "trace.h"

static void sim_stop(void) {
    task_delay(SIM_DURATION_US);
    rtos_stop();
}

static const scenario_config_t configs[] = {
    { SCENARIO_S0, "S0", 0, 1, MED3_WCET_LOW_US },
    { SCENARIO_S1, "S1", 0, 1, MED3_WCET_HIGH_US },
    { SCENARIO_S2, "S2", 1, 1, MED3_WCET_HIGH_US },
    { SCENARIO_S3, "S3", 0, 0, MED3_WCET_HIGH_US }
};

const scenario_config_t *scenario_get(scenario_id_t id) {
    size_t n = sizeof(configs) / sizeof(configs[0]);
    for (size_t i = 0; i < n; i++) {
        if (configs[i].id == id) {
            return &configs[i];
        }
    }
    return NULL;
}

scenario_result_t scenario_run(const scenario_config_t *cfg, FILE *out) {
    scenario_result_t result = { 0, 0, 0 };
    if (!cfg) {
        return result;
    }

    rtos_init();
    trace_init(out, cfg->name, cfg->pip, cfg->shared_mutex);

    pipe_t *pipe = pipe_create();
    sem_t *asi_mutex;
    sem_t *dist_mutex;

    if (cfg->shared_mutex) {
        sem_t *shared = sem_mcreate("select_mutex", cfg->pip);
        asi_mutex = shared;
        dist_mutex = shared;
    } else {
        asi_mutex = sem_mcreate("asi_select_mutex", 0);
        dist_mutex = sem_mcreate("dist_select_mutex", 0);
    }

    bus1553_init();
    flight_sw_init(asi_mutex, dist_mutex, pipe, cfg->med3_wcet_us);

    trace_event("START", NULL, "scenario=%s pip=%d shared=%d",
                cfg->name, cfg->pip, cfg->shared_mutex);

    task_spawn("sim_stop", 0, sim_stop);
    task_spawn("bc_sched", 1, bc_sched);
    task_spawn("bc_dist", 3, bc_dist);
    task_spawn("med_1", 4, med_1);
    task_spawn("med_2", 5, med_2);
    task_spawn("med_3", 6, med_3);
    task_spawn("asi_met", 7, asi_met);
    task_spawn("t_exec", 99, t_exec);

    rtos_run();

    result.resets = rtos_reset_count();
    result.max_block_us = flight_max_block_us();
    result.deadline_misses = flight_deadline_misses;

    trace_event("END", NULL, "resets=%d", result.resets);
    trace_summary(result.resets, result.max_block_us, result.deadline_misses);
    trace_close();
    return result;
}

#ifndef SCENARIO_H
#define SCENARIO_H

#include <stdio.h>
#include "config.h"

typedef struct {
    int resets;
    uint64_t max_block_us;
    int deadline_misses;
} scenario_result_t;

const scenario_config_t *scenario_get(scenario_id_t id);
scenario_result_t scenario_run(const scenario_config_t *cfg, FILE *out);

#endif

#include "scenario.h"

#include <stdio.h>
#include <string.h>

static void usage(const char *prog) {
    fprintf(stderr, "usage: %s --scenario s0|s1|s2|s3 [--out file]\n", prog);
}

int main(int argc, char **argv) {
    const char *scenario = NULL;
    const char *out_path = NULL;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--scenario") == 0 && i + 1 < argc) {
            scenario = argv[++i];
        } else if (strcmp(argv[i], "--out") == 0 && i + 1 < argc) {
            out_path = argv[++i];
        } else {
            usage(argv[0]);
            return 2;
        }
    }

    if (!scenario) {
        usage(argv[0]);
        return 2;
    }

    scenario_id_t id;
    if (strcmp(scenario, "s0") == 0) {
        id = SCENARIO_S0;
    } else if (strcmp(scenario, "s1") == 0) {
        id = SCENARIO_S1;
    } else if (strcmp(scenario, "s2") == 0) {
        id = SCENARIO_S2;
    } else if (strcmp(scenario, "s3") == 0) {
        id = SCENARIO_S3;
    } else {
        usage(argv[0]);
        return 2;
    }

    const scenario_config_t *cfg = scenario_get(id);
    if (!cfg) {
        fprintf(stderr, "unknown scenario\n");
        return 2;
    }

    FILE *out = NULL;
    if (out_path) {
        out = fopen(out_path, "w");
        if (!out) {
            perror(out_path);
            return 1;
        }
    }

    scenario_result_t r = scenario_run(cfg, out);
    if (out) {
        fclose(out);
    }

    printf("scenario=%s pip=%d shared=%d\n",
           cfg->name, cfg->pip, cfg->shared_mutex);
    printf("resets=%d deadline_misses=%d max_block_ms=%.3f\n",
           r.resets, r.deadline_misses, (double)r.max_block_us / 1000.0);
    if (r.resets > 0) {
        printf("WATCHDOG: RESET\n");
    } else {
        printf("OK\n");
    }
    return 0;
}

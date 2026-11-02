#include "scenario.h"

#include <stdio.h>

int main(void) {
    scenario_result_t r0 = scenario_run(scenario_get(SCENARIO_S0), NULL);
    scenario_result_t r1 = scenario_run(scenario_get(SCENARIO_S1), NULL);
    scenario_result_t r2 = scenario_run(scenario_get(SCENARIO_S2), NULL);
    scenario_result_t r3 = scenario_run(scenario_get(SCENARIO_S3), NULL);

    printf("S0: resets=%d max_block_ms=%.3f misses=%d\n",
           r0.resets, (double)r0.max_block_us / 1000.0, r0.deadline_misses);
    printf("S1: resets=%d max_block_ms=%.3f misses=%d\n",
           r1.resets, (double)r1.max_block_us / 1000.0, r1.deadline_misses);
    printf("S2: resets=%d max_block_ms=%.3f misses=%d\n",
           r2.resets, (double)r2.max_block_us / 1000.0, r2.deadline_misses);
    printf("S3: resets=%d max_block_ms=%.3f misses=%d\n",
           r3.resets, (double)r3.max_block_us / 1000.0, r3.deadline_misses);

    int ok = (r0.resets == 0) &&
             (r1.resets >= 1) &&
             (r2.resets == 0) &&
             (r3.resets == 0);

    printf("%s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}

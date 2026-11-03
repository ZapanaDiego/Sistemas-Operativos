#include "bus1553.h"
#include "scenario.h"

#include <stdio.h>

int main(void) {
    scenario_run(scenario_get(SCENARIO_S1), NULL);
    int cycles = bus1553_cycle_count();
    int ok = (cycles == 15);
    printf("bus: cycles=%d (esperado 15)\n", cycles);
    printf("%s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}

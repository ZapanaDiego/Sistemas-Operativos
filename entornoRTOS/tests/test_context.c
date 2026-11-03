#include "rtos.h"

#include <stdio.h>

static volatile int runs_a;
static volatile int runs_b;

static void task_a(void) {
    for (int i = 0; i < 5; i++) {
        runs_a++;
        task_delay(1000);
    }
}

static void task_b(void) {
    for (int i = 0; i < 5; i++) {
        runs_b++;
        task_delay(1500);
    }
}

int main(void) {
    rtos_init();
    task_spawn("a", 1, task_a);
    task_spawn("b", 2, task_b);
    rtos_run();

    int bad_stacks = rtos_check_stacks();
    int ok = (runs_a == 5) && (runs_b == 5) && (bad_stacks == 0);

    printf("context: a=%d b=%d bad_stacks=%d\n", runs_a, runs_b, bad_stacks);
    printf("%s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}

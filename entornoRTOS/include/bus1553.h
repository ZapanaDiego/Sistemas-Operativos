#ifndef BUS1553_H
#define BUS1553_H

/*
 * Modelo del ciclo de bus 1553 a 8 Hz (125 ms).
 *
 * El bus se representa con un semáforo binario: bc_sched lo libera al
 * inicio de cada ciclo y bc_dist lo toma para distribuir los datos.
 */

void bus1553_init(void);
void bus1553_cycle(void);
int bus1553_wait(void);
int bus1553_cycle_count(void);

#endif

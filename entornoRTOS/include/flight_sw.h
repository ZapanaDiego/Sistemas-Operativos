#ifndef FLIGHT_SW_H
#define FLIGHT_SW_H

#include "rtos.h"
#include "sem.h"
#include "pipe.h"

extern volatile int bc_dist_done;
extern int flight_deadline_misses;

void flight_sw_init(sem_t *asi_mutex, sem_t *dist_mutex, pipe_t *pipe,
                    sem_t *bus_sem, uint64_t med3_wcet_us);
uint64_t flight_max_block_us(void);

void bc_sched(void);
void bc_dist(void);
void asi_met(void);
void med_1(void);
void med_2(void);
void med_3(void);
void t_exec(void);

#endif

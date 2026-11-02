#ifndef PIPE_H
#define PIPE_H

#include <stdint.h>
#include "sem.h"

#define PIPE_SIZE 4096

typedef struct {
    uint32_t bits;
} rtos_fd_set;

#define RTOS_FD_ZERO(s) ((s)->bits = 0u)
#define RTOS_FD_SET(fd, s) ((s)->bits |= (1u << (fd)))
#define RTOS_FD_ISSET(fd, s) (((s)->bits >> (fd)) & 1u)

typedef struct {
    int id;
    uint8_t buf[PIPE_SIZE];
    int head;
    int tail;
    int count;
} pipe_t;

pipe_t *pipe_create(void);
int pipe_write(pipe_t *p, const void *data, int len);
int pipe_read(pipe_t *p, void *data, int len);
int pipe_has_data(const pipe_t *p);
int pipe_has_space(const pipe_t *p);
int rtos_select(sem_t *mutex, pipe_t *p, int nfds,
                rtos_fd_set *readfds, rtos_fd_set *writefds,
                uint64_t timeout_us);
void pipe_global_reset(void);

#endif

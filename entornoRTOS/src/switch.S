/*
 * Cambio de contexto para x86-64 System V AMD64.
 *
 * void rtos_switch(void **old_sp, void *new_sp);
 *
 * Guarda los registros callee-saved de la tarea actual, almacena su
 * stack pointer en *old_sp y carga el stack pointer de la tarea destino.
 * Al final, `ret` continúa en la función donde la tarea destino quedó
 * suspendida, o en task_trampoline si es su primera ejecución.
 */

    .text
    .globl rtos_switch
    .type rtos_switch, @function
rtos_switch:
    pushq %rbp
    pushq %rbx
    pushq %r12
    pushq %r13
    pushq %r14
    pushq %r15

    movq %rsp, (%rdi)
    movq %rsi, %rsp

    popq %r15
    popq %r14
    popq %r13
    popq %r12
    popq %rbx
    popq %rbp
    ret

    .size rtos_switch, .-rtos_switch

    .section .note.GNU-stack,"",@progbits

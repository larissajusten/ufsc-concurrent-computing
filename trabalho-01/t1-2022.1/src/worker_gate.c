#include <stdlib.h>
#include <pthread.h>

#include "worker_gate.h"
#include "globals.h"
#include "config.h"
#include "queue.h"
#include "buffet.h"

worker_gate_t self_thread;
student_t *buffet_student = NULL;

void worker_gate_look_queue()
{
    /* Olha para a fila de estudantes e seleciona o primeiro estudante da fila */
    if(globals_get_queue()->_length > 0) {
        if(globals_get_queue()->_first)
            buffet_student = globals_get_queue()->_first->_student;
    }
}

void worker_gate_remove_queue_student()
{
    /* Remove o estudante selecionado da fila se ele tem buffet */
    if(buffet_student != NULL && buffet_student->_id_buffet != -1) {
        queue_remove(globals_get_queue());
        buffet_student = NULL;
    }
}

void worker_gate_look_buffet()
{
    buffet_t *buffets = globals_get_buffets();

    if(buffets != NULL && buffet_student != NULL) {
        /* Itera em cima do array de buffets tentando adicionar o estudante no buffet da iteração */
        for (size_t buffet_iter = 0; buffet_iter < globals_get_buffets_number(); buffet_iter++) {
            buffet_student->_id_buffet = buffets[buffet_iter]._id;
            buffet_student->left_or_right = 'R';

            /* Se não conseguiu adicionar o estudante na direita, tenta na esquerda */
            if (!buffet_queue_insert(buffets, buffet_student)) {
                buffet_student->left_or_right = 'L';

                if (buffet_queue_insert(buffets, buffet_student)) {
                    break;
                } else {
                    buffet_student->_id_buffet = -1;
                    continue;
                }
            } else {
                break;
            }
        };
    };
}

void *worker_gate_run(void *arg)
{
    int all_students_entered;
    int number_students;

    number_students = *((int *)arg);
    all_students_entered = number_students > 0 ? FALSE : TRUE;

    while (all_students_entered == FALSE)
    {
        worker_gate_look_queue();
        worker_gate_look_buffet();
        worker_gate_remove_queue_student();
    }

    pthread_exit(NULL);
}

void worker_gate_init(worker_gate_t *self)
{
    int number_students = globals_get_students();
    self_thread = *self;
    pthread_create(&self->thread, NULL, worker_gate_run, &number_students);
}

void worker_gate_finalize(worker_gate_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}

void worker_gate_insert_queue_buffet(student_t *student)
{
    queue_t *queue = globals_get_queue();
    queue_insert(queue, student);
}
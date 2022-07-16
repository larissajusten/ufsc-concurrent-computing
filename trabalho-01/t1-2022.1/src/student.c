#include <time.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>
#include <pthread.h>

#include "student.h"
#include "config.h"
#include "worker_gate.h"
#include "globals.h"
#include "table.h"

pthread_mutex_t lock;

void* student_run(void *arg)
{
    student_t *self = (student_t*) arg;
    table_t *tables  = globals_get_table();
    self->_id_table = -1;

    pthread_mutex_init(&lock, NULL);

    worker_gate_insert_queue_buffet(self);
    student_serve(self);
    student_seat(self, tables);
    student_leave(self, tables);

    pthread_mutex_destroy(&lock);

    pthread_exit(NULL);
};

void student_seat(student_t *self, table_t *table)
{
    table_t *tables = globals_get_table();
    /*Verifica se tem mesa livre*/
    while(self->_id_table == -1) {
        for (size_t table_iter = 0; table_iter < globals_get_number_of_tables(); table_iter++) {
            if(tables[table_iter]._empty_seats > 0) {
                tables[table_iter]._empty_seats -= 1;
                self->_id_table = table_iter;
            }
        }
    }
}


/* Função privada que verifica se o estudante pode andar na fila de buffets */
bool _can_walk_to_next_step(student_t *self, buffet_t buffet) {
    pthread_mutex_lock(&lock);
    int next_position = self->_buffet_position+1;
    bool can_walk_right = self->left_or_right == 'R' && buffet.queue_right[next_position] == 0;
    bool can_walk_left = self->left_or_right == 'L' && buffet.queue_left[next_position] == 0;
    pthread_mutex_unlock(&lock);
    return can_walk_right || can_walk_left;
}

/* Função privada que se o estudante ja passou por todas as bacias, pode sair do buffet */
void _student_leave_buffet(student_t *self, buffet_t *buffets) {
    if(self->left_or_right == 'R'){
        buffets[self->_id_buffet].queue_right[4] = 0;
    } else {
        buffets[self->_id_buffet].queue_left[4] = 0;
    }

    self->_id_buffet = -1;
    self->_buffet_position = -1;
    self->left_or_right = ' ';
}

void student_serve(student_t *self)
{
    buffet_t *buffets = globals_get_buffets();   
    /*Enquanto o estudante estiver no buffet*/
    while(TRUE) {
        /*Verifica se já engressou no buffet*/
        if(buffets != NULL && self->_buffet_position > -1) {
            /*Verifica se ele quer comer o que esta na bacia*/
            if(self->_wishes[self->_buffet_position]) {
                sem_wait(&buffets[self->_id_buffet]._sem_meal[self->_buffet_position]);
                buffets[self->_id_buffet]._meal[self->_buffet_position] -= 1;
            }

            msleep(500);

            /* Se o estudante esta na ultima posição do buffet, sai do for */
            if(self->_buffet_position == 4) {
                break;
            /* Se não, verifica se pode andar */
            } else if(_can_walk_to_next_step(self, buffets[self->_id_buffet])) {
                pthread_mutex_lock(&lock); //next_step faz as mudanças nos students
                buffet_next_step(buffets, self);//precisa proteger os dados da região crítica
                pthread_mutex_unlock(&lock);
            }
        }
    }

    _student_leave_buffet(self, buffets);
}

void student_leave(student_t *self, table_t *table)
{
    table_t *tables = globals_get_table();
    tables[self->_id_table]._empty_seats += 1;
    self->_id_table = -1;
    /* Mutex para adicionar um valor na variavel global que controla o numero de estudantes que sairam do buffet */
    pthread_mutex_lock(&lock);
    globals_add_finished_students();
    pthread_mutex_unlock(&lock);
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

student_t *student_init()
{
    student_t *student = malloc(sizeof(student_t));
    student->_id = rand() % 1000;
    student->_buffet_position = -1;
    int none = TRUE;
    for (int j = 0; j <= 4; j++)
    {
        student->_wishes[j] = _student_choice();
        if(student->_wishes[j] == 1) none = FALSE;
    }

    if(none == FALSE){
        /* O estudante só deseja proteína */
        student->_wishes[3] = 1;
    }

    return student;
};

void student_finalize(student_t *self){
    free(self);
};


pthread_t students_come_to_lunch(int number_students)
{
    pthread_t lets_go;
    pthread_create(&lets_go, NULL, _all_they_come, &number_students);
    return lets_go;
}

/**
 * @brief Função (privada) que inicializa as threads dos alunos.
 * 
 * @param arg 
 * @return void* 
 */
void* _all_they_come(void *arg)
{
    int number_students = *((int *)arg);
    
    student_t *students[number_students];

    for (int i = 0; i < number_students; i++)
    {
        students[i] = student_init();                                               /* Estudante é iniciado, recebe um ID e escolhe o que vai comer*/
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_create(&students[i]->thread, NULL, student_run, students[i]);       /*  Cria as threads  */
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_join(students[i]->thread, NULL);                                    /*  Aguarda o término das threads   */
    }

    for (int i = 0; i < number_students; i++)
    {
        student_finalize(students[i]);                                              /*  Libera a memória de cada estudante  */
    }

    pthread_exit(NULL);
}

/**
 * @brief Função que retorna as escolhas dos alunos, aleatoriamente (50% para cada opção)
 *        retornando 1 (escolhido) 0 (não escolhido). É possível que um aluno não goste de nenhuma opção
 *         de comida. Nesse caso, considere que ele ainda passa pela fila, como todos aqueles que vão comer.
 * @return int 
 */
int _student_choice()
{
    float prob = (float)rand() / RAND_MAX;
    return prob > 0.51 ? 1 : 0;
}
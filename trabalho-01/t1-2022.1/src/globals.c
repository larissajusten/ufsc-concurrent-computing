#include <stdlib.h>
#include "globals.h"

#define TOTAL_MEALS 5

queue_t *students_queue = NULL;
table_t *table = NULL;
buffet_t *buffets_ref = NULL;

int buffets_number = 0;
int students_number = 0;
int number_of_tables = 0;
int finished_students = 0;

void globals_set_queue(queue_t *queue)
{
    students_queue = queue;
}

queue_t *globals_get_queue()
{
    return students_queue;
}

void globals_set_table(table_t *t)
{
    table = t;
}

table_t *globals_get_table()
{
    return table;
}

void globals_set_number_of_tables(int number) {
    number_of_tables = number;
}

int globals_get_number_of_tables() {
    return number_of_tables;
}

void globals_set_students(int number)
{
    students_number = number;
}

int globals_get_students()
{
    return students_number;
}

void globals_set_buffets(buffet_t *buffets)
{
    buffets_ref = buffets;
}

buffet_t *globals_get_buffets()
{
    return buffets_ref;
}

void globals_set_buffets_number(int number)
{
    buffets_number = number;
}

int globals_get_buffets_number()
{
    return buffets_number;
}

void globals_add_finished_students()
{
    finished_students++;
}

int globals_get_finished_students()
{
    return finished_students;
}

/**
 * @brief Finaliza todas as variáveis globais que ainda não foram liberadas.
 *  Se criar alguma variável global que faça uso de mallocs, lembre-se sempre de usar o free dentro
 * dessa função.
 */
void globals_finalize()
{
    free(table);
    free(students_queue);
    free(buffets_ref);
}
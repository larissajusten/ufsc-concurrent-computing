#include <stdlib.h>
#include <stdbool.h>

#include "chef.h"
#include "config.h"
#include "globals.h"

void *chef_run()
{
    while (TRUE) {
        chef_check_food();
    }    
    pthread_exit(NULL);
}


void chef_put_food(buffet_t *buffet, int meal_iter)
{
    buffet->_meal[meal_iter] = 40;
    msleep(5000);
    for (size_t i = 0; i < 40; i++) 
        sem_post(&buffet->_sem_meal[meal_iter]);
}

void chef_check_food()
{
    buffet_t *buffets = globals_get_buffets();

    if(buffets != NULL) {
        for (size_t buffet_iter = 0; buffet_iter < globals_get_buffets_number(); buffet_iter++) {
            for (size_t meal_iter = 0; meal_iter < TOTAL_MEALS; meal_iter++) {
                /* Se ainda existe comida, vai pra próxima iteração */
                if(buffets[buffet_iter]._meal[meal_iter] > 0 ) continue;
                /* Se não, da post nos semaforos da comida e  enche a comida */
                chef_put_food(&buffets[buffet_iter], meal_iter);      
            }
        }
    }
    
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

void chef_init(chef_t *self)
{
    pthread_create(&self->thread, NULL, chef_run, NULL);
}

void chef_finalize(chef_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}
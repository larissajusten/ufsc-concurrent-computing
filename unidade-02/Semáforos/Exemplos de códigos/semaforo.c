#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

// Semáforos usados para controlar o acesso as licenças de software
sem_t licencas;

int n_threads;
int num_licencas;

// Código da thread
void *sw_user(void *arg)
{
    int my_id = *((int *)arg);
    printf("Thread %d iniciada.\n", my_id);
    sem_wait(&licencas);
    printf("Thread %d obteve a licença.\n", my_id);
    sleep(5);
    printf("Thread %d liberando a licença.\n", my_id);
    sem_post(&licencas);
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        printf("Uso: %s n_threads num_licencas\n", argv[0]);
        return 0;
    }

    n_threads = atoi(argv[1]);
    num_licencas = atoi(argv[2]);

    pthread_t threads[n_threads];
    int thread_id[n_threads];

    // Inicializa semáforo sem permissões
    sem_init(&licencas, 0, 0);

    // Cria threads para produtor_func e consumidor_func
    for (int i = 0; i < n_threads; i++)
    {
        thread_id[i] = i;
        pthread_create(&threads[i], NULL, sw_user, (void *)&thread_id[i]);
    }

    sleep(5); // Aguarda um tempo antes de liberar as licenças para uso

    // Libera algumas licenças para uso
    printf("Thread principal liberando %d licenças para uso.\n", num_licencas);
    for (int i = 0; i < num_licencas; i++)
        sem_post(&licencas);

    // Espera threads para produtor_func e consumidor_func
    for (int i = 0; i < n_threads; i++)
        pthread_join(threads[i], NULL);

    // Destrói semáforos
    sem_destroy(&licencas);

    return 0;
}

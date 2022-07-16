#include <semaphore.h>

sem_t semaphore;

void *thread(void *arg)
{
    sem_wait(&semaphore);
    // Seção crítica
    sem_post(&semaphore);
    pthread_exit(NULL);
}

int main(int argc, char **argv)
{
    sem_init(&semaphore, 0, 1);
    // Criação das threads + joins
    sem_destroy(&semaphore);
    return 0;
}

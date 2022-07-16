#include <pthread.h>
#include <stdio.h>

unsigned int contador = 0;

void *thread(void *arg)
{
    printf("Thread % d criada\n", pthread_self());
    for (int i = 0; i < 500; i++) // Região crítica no for e incremento no contador juntos
        contador++; // Região crítica só no incremento do contador
    pthread_exit(NULL);
}

int main()
{
    pthread_t th[10];
    for (int i = 0; i < 10; i++)
        pthread_create(&th[i], NULL, thread, NULL);
    for (int i = 0; i < 10; i++)
        pthread_join(th[i], NULL);
    return 0;
}

#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>

pthread_mutex_t mutex;

void *thread(void *arg)
{
    pthread_mutex_lock(&mutex);
    // região crítica
    pthread_mutex_unlock(&mutex);
    return 0;
}

int main()
{
    pthread_mutex_init(&mutex, NULL);
    pthread_create(...);
    pthread_join(...);
    pthread_mutex_destroy(&mutex);
    return 0;
}
#include <pthread.h>
#include <stdio.h>

void *print_hello(void *arg)
{
    pthread_t tid = pthread_self();
    printf("Thread %u: Hello World!\n", (unsigned int)tid);
    pthread_exit(NULL);
}

int main(int argc, char **argv)
{
    pthread_t thread;
    pthread_create(&thread, NULL, print_hello, NULL);
    pthread_join(thread, NULL);
    return 0;
}

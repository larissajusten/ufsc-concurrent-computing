void *produtor(void *arg)
{
    while (1)
    {
        sem_wait(&vazio);
        sem_wait(&lock_prod);
        f = (f + 1) % N;
        buffer[f] = produz();
        sem_post(&lock_prod);
        sem_post(&cheio);
    }
    pthread_exit(NULL);
}

void *consumidor(void *arg)
{
    while (1)
    {
        sem_wait(&cheio);
        sem_wait(&lock_cons);
        i = (i + 1) % N;
        consome(buffer[i]);
        sem_post(&lock_cons);
        sem_post(&vazio);
    }
    pthread_exit(NULL);
}

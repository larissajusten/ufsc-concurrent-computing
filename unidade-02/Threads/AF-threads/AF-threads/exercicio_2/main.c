#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>
#include <sys/time.h>

// Lê o conteúdo do arquivo filename e retorna um vetor E o tamanho dele
// Se filename for da forma "gen:%d", gera um vetor aleatório com %d elementos
//
// +-------> retorno da função, ponteiro para vetor malloc()ado e preenchido
// |
// |         tamanho do vetor (usado <-----+
// |         como 2o retorno)              |
// v                                       v
double *load_vector(const char *filename, int *out_size);

// Avalia o resultado no vetor c. Assume-se que todos os ponteiros (a, b, e c)
// tenham tamanho size.
void avaliar(double *a, double *b, double *c, int size);

typedef struct
{
    double *vetor_a;
    double *vetor_b;
    double *vetor_c;
    int loop_size_min;
    int loop_size_max;
} Strct_elementos;

void *worker_thread(void *strct_elementos)
{
    Strct_elementos *elementos = (Strct_elementos *)strct_elementos;
    for (int i = elementos->loop_size_min; i < elementos->loop_size_max; i++)
        elementos->vetor_c[i] = elementos->vetor_a[i] + elementos->vetor_b[i];

    pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
    struct timeval begin, end;
    // Gera um resultado diferente a cada execução do programa
    // Se **para fins de teste** quiser gerar sempre o mesmo valor
    // descomente o srand(0)
    srand(time(NULL)); // valores diferentes
    // srand(0);        //sempre mesmo valor

    // Temos argumentos suficientes?
    if (argc < 4)
    {
        printf("Uso: %s n_threads a_file b_file\n"
               "    n_threads    número de threads a serem usadas na computação\n"
               "    *_file       caminho de arquivo ou uma expressão com a forma gen:N,\n"
               "                 representando um vetor aleatório de tamanho N\n",
               argv[0]);
        return 1;
    }

    // Quantas threads?
    int n_threads = atoi(argv[1]);
    if (!n_threads)
    {
        printf("Número de threads deve ser > 0\n");
        return 1;
    }

    // Lê números de arquivos para vetores alocados com malloc
    int a_size = 0, b_size = 0;
    double *a = load_vector(argv[2], &a_size);
    if (!a)
    {
        // load_vector não conseguiu abrir o arquivo
        printf("Erro ao ler arquivo %s\n", argv[2]);
        return 1;
    }

    double *b = load_vector(argv[3], &b_size);
    if (!b)
    {
        printf("Erro ao ler arquivo %s\n", argv[3]);
        return 1;
    }

    // Garante que entradas são compatíveis
    if (a_size != b_size)
    {
        printf("Vetores a e b tem tamanhos diferentes! (%d != %d)\n", a_size, b_size);
        return 1;
    }

    // Cria vetor do resultado
    double *c = malloc(a_size * sizeof(double));

    // Calcula com uma thread só. Programador original só deixou a leitura
    // do argumento e fugiu pro caribe. É essa computação que você precisa
    // paralelizar

    if (n_threads > a_size)
        n_threads = a_size;
    int size_per_thread = a_size / n_threads;

    Strct_elementos elementos[n_threads];
    pthread_t threads[n_threads];

    for (size_t i = 0; i < n_threads; i++)
    {
        elementos[i].vetor_a = a;
        elementos[i].vetor_b = b;
        elementos[i].vetor_c = c;
        elementos[i].loop_size_min = i * size_per_thread;
        elementos[i].loop_size_max = i * size_per_thread + size_per_thread;

        if (i == n_threads - 1)
            elementos[i].loop_size_max = a_size;
    }

    gettimeofday(&begin, NULL);
    for (int i = 0; i < n_threads; i++)
        pthread_create(&threads[i], NULL, worker_thread, (void *)&elementos[i]);

    for (int i = 0; i < n_threads; i++)
        pthread_join(threads[i], NULL);

    gettimeofday(&end, NULL);

    // long double elapsed = (end.tv_sec - begin.tv_sec) +
    //                       ((end.tv_usec - begin.tv_usec) / 1000000.0);

    //    +---------------------------------+
    // ** | IMPORTANTE: avalia o resultado! | **
    //    +---------------------------------+
    avaliar(a, b, c, a_size);

    // Importante: libera memória
    free(a);
    free(b);
    free(c);

    // printf("time = %LF\n", elapsed);

    return 0;
}

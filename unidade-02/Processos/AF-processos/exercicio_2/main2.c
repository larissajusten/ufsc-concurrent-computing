#include <stdio.h>
#include <unistd.h>

//                          (principal)
//                               |
//              +----------------+--------------+
//              |                               |
//           filho_1                         filho_2
//              |                               |
//    +---------+-----------+          +--------+--------+
//    |         |           |          |        |        |
// neto_1_1  neto_1_2  neto_1_3     neto_2_1 neto_2_2 neto_2_3

// ~~~ printfs  ~~~
//      principal (ao finalizar): "Processo principal %d finalizado\n"
// filhos e netos (ao finalizar): "Processo %d finalizado\n"
//    filhos e netos (ao inciar): "Processo %d, filho de %d\n"

// Obs:
// - netos devem esperar 5 segundos antes de imprmir a mensagem de finalizado (e terminar)
// - pais devem esperar pelos seu descendentes diretos antes de terminar

int main(int argc, char **argv)
{
  pid_t pid_filho_1, pid_filho_2;
  pid_t pid_neto_1_1, pid_neto_1_2, pid_neto_1_3, pid_neto_2_1, pid_neto_2_2, pid_neto_2_3;

  pid_filho_1 = fork();

  if (pid_filho_1 == 0)
  {
    printf("Processo filho (%d) criado\n", getpid());
    pid_neto_1_1 = fork();

    if (pid_neto_1_1 == 0)
    {
      printf("Processo neto %d, filho de (%d)\n", getpid(), getppid());
      sleep(5);
    }
    else
    {
      pid_neto_1_2 = fork();
      if (pid_neto_1_2 == 0)
      {
        printf("Processo neto %d, filho de (%d)\n", getpid(), getppid());
        sleep(5);
      }
      else
      {
        pid_neto_1_3 = fork();
        if (pid_neto_1_3 == 0)
        {
          printf("Processo neto %d, filho de (%d)\n", getpid(), getppid());
          sleep(5);
        }
      }
    }
  }
  else
  {
    pid_filho_2 = fork();

    if (pid_filho_2 == 0)
    {
      printf("Processo filho [%d] criado\n", getpid());
      pid_neto_2_1 = fork();

      if (pid_neto_2_1 == 0)
      {
        printf("Processo neto %d, filho de [%d]\n", getpid(), getppid());
      }
      else
      {
        pid_neto_2_2 = fork();

        if (pid_neto_2_2 == 0)
        {
          printf("Processo neto %d, filho de [%d]\n", getpid(), getppid());
        }
        else
        {
          pid_neto_2_3 = fork();

          if (pid_neto_2_3 == 0)
          {
            printf("Processo neto %d, filho de [%d]\n", getpid(), getppid());
          }
        }
      }
    }
  }

  while (wait(NULL) >= 0)
  {
    printf("Processo %d finalizado\n", getpid());
  };

  return 0;
}

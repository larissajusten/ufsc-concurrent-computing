#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

/** no exercicio 1 o pai tem que printar o fork() pra mostrar os pids dos filhos **/

//       (pai)
//         |
//    +----+----+
//    |         |
// filho_1   filho_2

// ~~~ printfs  ~~~
// pai (ao criar filho): "Processo pai criou %d\n"
//    pai (ao terminar): "Processo pai finalizado!\n"
//  filhos (ao iniciar): "Processo filho %d criado\n"

// Obs:
// - pai deve esperar pelos filhos antes de terminar!

int main(int argc, char **argv)
{
  pid_t pid_filho_a, pid_filho_b;

  pid_filho_a = fork();

  if (pid_filho_a == 0)
  {
    printf("Processo filho %d criado\n", getpid());
  }
  else
  {
    pid_filho_b = fork();

    if (pid_filho_b == 0)
    {
      printf("Processo filho %d criado\n", getpid());
    }
    else
    {
      printf("Processo pai criou %d\n", getpid());
      printf("Processo pai finalizado!\n");
    }
  }

  while (wait(NULL) >= 0);
  return 0;
}

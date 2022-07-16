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
  for (size_t i = 0; i < 2; i++)
  {
    pid_t pid_filho;

    pid_filho = fork();

    if(pid_filho != 0) {
      printf("Processo pai criou %d\n", pid_filho);
    } else {
      printf("Processo filho %d criado\n", getpid());
      break;
    }
  }

  while(wait(NULL) >= 0) {
    printf("Processo pai finalizado!\n");
  }
  return 0;
}

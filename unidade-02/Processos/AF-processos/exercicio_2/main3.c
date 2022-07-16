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
  int status;

  pid_t pid_filho;

  pid_filho = fork();

  if (pid_filho == 0){
    for (int i = 0; i < 3; i++) {
      pid_t pid_neto;

      pid_neto = fork();

      if(pid_neto != 0) {
        printf("Processo %d, filho de [%d]\n", pid_neto, getpid());
        sleep(5);
      } else {
        break;
      }
    }
  } else {
    for (int j = 0; j < 3; j++) {
      pid_t pid_neto;

      pid_neto = fork();

      if(pid_neto != 0) {
        printf("Processo %d, filho de [%d]\n", pid_neto, getpid());
        sleep(5);
      } else {
        break;
      }
    }
  }

  while (wait(NULL) >= 0)
  {
    printf("Processo %d finalizado\n", getpid());
  };

  return 0;
}

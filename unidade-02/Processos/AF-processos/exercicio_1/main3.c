#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char const *argv[])
{
  pid_t pid_filho;

  pid_filho = fork();
  pid_filho = fork();
    
  if (pid_filho == 0)
  {
    printf("Processo filho %d criado\n", getpid());
    sleep(1);
  } 
  else {
    printf("Processo pai criou %d\n", fork());
    while(wait(NULL) >= 0);
    return 0;
  }
  return 0;
}

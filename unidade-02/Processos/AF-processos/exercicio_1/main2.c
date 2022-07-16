#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>


/// Pai -> filho 
/// |-> filho 
/// |-> filho
int main(int argc, char const *argv[])
{
  for (size_t i = 0; i < 2; i++)
  {
    pid_t pid_filho;

    pid_filho = fork();
    
    if (pid_filho != 0)
    {
      printf("Processo pai criou %d\n", pid_filho);
    } else {
      break;
    }
  }

  while (wait(NULL) >= 0);
  
  return 0;
}

/// Pai -> filho -> filho -> filho
int main(int argc, char const *argv[])
{
  for (size_t i = 0; i < 2; i++)
  {
    pid_t pid_filho;

    pid_filho = fork();
    
    if (pid_filho == 0)
    {
      printf("Processo pai %d criou %d\n", getpid(), pid_filho);
    } else {
      break;
    }
  }
  return 0;
}
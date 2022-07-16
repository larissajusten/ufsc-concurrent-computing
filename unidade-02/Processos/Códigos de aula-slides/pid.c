#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char const *argv[])
{
    printf("PID retornando ao processo %d eh %d\n", getpid(), fork());
    printf("\n");
    return 0;
}

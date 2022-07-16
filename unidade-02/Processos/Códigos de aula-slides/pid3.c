#include <stdio.h>
#include <unistd.h>

int var_global = 0;

int main(int argc, char **argv)
{
    int var_local = 0;
    pid_t pid;
    pid = fork();
    if (pid == 0)
    { // filho
        var_global = 1;
        var_local = 2;
    }
    else
    { // pai
        var_global = 50;
        var_local = 100;
    }
    return 0;
}

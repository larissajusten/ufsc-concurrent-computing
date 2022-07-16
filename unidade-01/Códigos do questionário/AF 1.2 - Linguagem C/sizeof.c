#include <stdlib.h>
#include <stdio.h>

int main(void)
{
    printf("\n%ld\n", sizeof(int));
    printf("\n%ld\n", sizeof(int *));
    printf("\n%ld\n", sizeof(int **));
    printf("\n%ld\n", sizeof(int ***));
}

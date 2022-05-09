#include <stdlib.h>
#include <stdio.h>

int* g(int* a) {
    printf("\n2 - %ls\n", a);
    printf("\n3 - %d\n", *a);
    return a++;
}

int f(int a) {
    return *g(&a);
}

int main(void) {
    printf("\n1 - %d \n", f(7));
}
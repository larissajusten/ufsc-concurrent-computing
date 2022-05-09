#include <stdlib.h>
#include <stdio.h>

int f(int a) {
    printf("%ls\n", &a);
    if (a % 2 != 0 && a < 20) {
        return a;
    } else if (&a) {
        if (a < 0) return 2*a;
    } else {
        return 27;
    }
    return 31;
}

int main(void) {
    printf("%d\n", f(0));
    printf("%d\n", f(2));
    printf("%d\n", f(-2));
    printf("%d\n", f(-3));
}
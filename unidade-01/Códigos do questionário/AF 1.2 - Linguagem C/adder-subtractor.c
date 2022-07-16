#include <stdio.h>

void adder(int *x, int n, int max)
{
    while (*x < max)
    {
        *x += n;
    }
    printf("%d", *x);
    max *= 2;
}

void subtractor(int *x, int n, int max)
{
    while (*x >= max)
    {
        *x -= n;
    }
}

int main()
{
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    b = 2;
    adder(&a, b, c);
    subtractor(&a, b, c);
    printf("%d %d %d\n", a, b, c);
}

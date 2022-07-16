#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0

typedef struct
{
    int on;
} Lampada;

Lampada *NewLampada()
{
    printf("%ld\n", sizeof(Lampada));
    printf("%ld\n", sizeof(Lampada *));
    Lampada *lamp = malloc(sizeof(Lampada));
    lamp->on = FALSE;
    return lamp;
}

void Click(Lampada *lamp)
{
    if (lamp->on == FALSE)
    {
        lamp->on = TRUE;
    }
    else
    {
        lamp->on = FALSE;
    }
}

int main()
{
    Lampada *lamp = NewLampada();
    if (TRUE)
    {
        Click(lamp);
    }
    printf("%d\n", lamp->on);
    return 0;
}

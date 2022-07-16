#include <stdio.h>
#include <string.h>

int main()
{
    char *str = "A";
    if (strlen(str) == sizeof(str))
    {
        printf("B");
    }
    else if (printf("C"))
    {
        printf("D");
    }
    else
    {
        printf("E");
    }
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char s1[] = "HELLO";
    printf("%s\n", s1);
    char* s2 = "WORLD";
    printf("%s\n", s2);
    char* s3 = s2;
    printf("%s\n", s3);
    // errado = char *s4;
    char *s4 = malloc(sizeof(char));
    printf("%s\n", s4);
    strcpy(s4, s3);
    printf("%s\n", s3);
}
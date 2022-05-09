#include<stdio.h>
#include <sys/time.h>

int main (void) {
    struct timeval begin, end;
    
    gettimeofday(&begin, NULL);
    long int f = 0;
    for(int i=0; i<2000000000000; i++){
        f += i;
    }
    gettimeofday(&end, NULL);
    
    long double elapsed = (end.tv_sec - begin.tv_sec) +
    ((end.tv_usec - begin.tv_usec)/1000000.0);
    printf("time = %LF\n", elapsed);
}
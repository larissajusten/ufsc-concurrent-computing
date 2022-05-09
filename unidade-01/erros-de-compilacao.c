#include <stdio.h>

typedef struct {
    float x, y;
} ponto_t;

int main(void) {
    ponto_t q = {23.0, 27.0};
    ponto_t* p = &q;

    // errado = q->x++;
    // certo = q.x++;

    // errado = q.x = p
    // certo = q.x = p->x;
    
    q.x = q.y = p->x *= 2;
    
    // errado = p->++x;
    // certo = ++p->x;
    // certo = p->x++;
    // certo?? = p->x = ++p->x;
}
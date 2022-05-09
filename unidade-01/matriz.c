#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main(void) {
    int ROW = 5;
    int COL = 5;
    int data[5][5] = {0};


    // errada
    // for (int i = 0; i <= ROW; i++) {
    //     for (int j = i; j <= COL; j++) {
    //         data[i][j] = rand() % 100 + 1;
    //     }
    // }

    // certa
    // for (int i = 0; i < COL; i++) {
    //     for (int j = i; j < ROW; j++) {
    //         data[i][j] = rand() % 100 + 1;
    //     }
    // }

    // certa
    // for (int i = 0; i < ROW; i++) {
    //     for (int j = i; j >= 0; j--) {
    //         data[j][i] = rand() % 100 + 1;
    //     }
    // }

    // ERRADA
    // for (int i = 0; i < ROW; i++) {
    //     for (int j = i; j < COL; j++) {
    //         data[j][i] = rand() % 100 + 1;
    //     }
    // }

    // certa
    // for (int i = 0; i < ROW; i++) {
    //     for (int j = i; j < COL; j++) {
    //         data[i][j] = rand() % 100 + 1;
    //     }
    // }

    // ERRADA
    // for (int i = 0; i < ROW; i++) {
    //     for (int j = i; j >= 0; j--) {
    //         data[i][j] = rand() % 100 + 1;
    //     }
    // }    


    for (int i = 0; i < ROW; i++) {
        for (int j = 0; j < COL; j++) {
            printf("[%d][%d]%d ", i, j, data[i][j]);
        }
        printf("\n");
    }

}

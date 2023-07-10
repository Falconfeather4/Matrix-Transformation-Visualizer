#include <stdio.h>

void map_pixels(void *coordxv, void *coordyv, void *imgv, void *bgv, int rows, int cols);

// main is purely for testing purposes
int main() {
    int coordx[] = {2, 1, 0, 2, 1, 0};
    int coordy[] = {1, 1, 1, 0, 0, 0};
    u_int8_t img[] = { 11, 12, 13, 21, 22, 23,31, 32, 33, 41, 42,
                       43,51, 52, 53, 61, 62, 63};
    u_int8_t bg[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0};
    for (int i = 0; i < 18; i++) {
        printf("%d,", bg[i]);
    }
    printf("\n");

    map_pixels(coordx, coordy, img, bg, 2, 3);

    for (int i = 0; i < 18; i++) {
        printf("%d,", bg[i]);
    }
    printf("\n");

    return 0;
}

// map each pixel in layer of img to background img corresponding to transformed_coords
void map_pixels(void *coordxv, void *coordyv, void *imgv, void *bgv, int rows, int cols) {
    int * coordx = (int *) coordxv;
    int * coordy = (int *) coordyv;
    u_int8_t * img = (u_int8_t *) imgv;
    u_int8_t * bg = (u_int8_t *) bgv;

    for (int i = 0; i < rows * cols; i++) {
        int y_val = coordy[i];
        int x_val = coordx[i];
        if ((x_val >= 0 && x_val < cols) && (y_val >= 0 && y_val < rows)) {
            int position = (y_val * cols) + x_val;
            bg[3*position] = img[3*i];
            bg[3*position + 1] = img[3*i + 1];
            bg[3*position + 2] = img[3*i + 2];
        }
    }

    
}
#include <stdio.h>

typedef struct Image {
    u_int8_t * pointer;
    int rows;
    int cols;
} image;

typedef struct Colour {
    int r;
    int g;
    int b;
} colour;

typedef struct Point {
    int x;
    int y;
} point;

void map_pixels(void *coordxv, void *coordyv, void *imgv, void *bgv, int rows, int cols);

void draw_line(image img, point start, int length, int thickness, char direction, colour c);
void draw_point(image img, point p, colour c);
void draw_axis(void *imgv, int rows, int cols);
void draw_x_ticks(image img, point center, int tick_spacing, colour colour);
void draw_y_ticks(image img, point center, int tick_spacing, colour colour);



// main is purely for testing purposes
int main() {
//    // test map_pixels()
//    int coordx[] = {2, 1, 0, 2, 1, 0};
//    int coordy[] = {1, 1, 1, 0, 0, 0};
//    u_int8_t img[] = { 11, 12, 13, 21, 22, 23,31, 32, 33, 41, 42,
//                       43,51, 52, 53, 61, 62, 63};
//    u_int8_t bg[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
//                     0, 0, 0, 0, 0, 0};
//    for (int i = 0; i < 18; i++) {
//        printf("%d,", bg[i]);
//    }
//    printf("\n");
//
//    map_pixels(coordx, coordy, img, bg, 2, 3);
//
//    for (int i = 0; i < 18; i++) {
//        printf("%d,", bg[i]);
//    }
//    printf("\n");
//

    // test draw_axis()

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


// given an image, start point, length of line in pixels, thickness in pixels, direction, and c in rgb, draws
// a straight line onto given image
void draw_line(image img, point start, int length, int thickness, char direction, colour c) {
    int start_index = (start.y * img.cols) + start.x;
    switch (direction) {
        case 'n':
            for (int i = 0; i < length; i ++) {
                for (int j = 0; j < thickness; j++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point p;
                        p.x = start.x + offset;
                        p.y = start.y - i;
                        draw_point(img, p, c);
                    }else {
                        int offset = j - j / 2;
                        point p;
                        p.x = start.x - offset;
                        p.y = start.y - i;
                        draw_point(img, p, c);
                    }
                }
            }
            break;
        case 's':
            for (int i = 0; i < length; i ++) {
                for (int j = 0; j < thickness; j++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point p;
                        p.x = start.x + offset;
                        p.y = start.y + i;
                        draw_point(img, p, c);
                    } else {
                        int offset = j - j / 2;
                        point p;
                        p.x = start.x - offset;
                        p.y = start.y + i;
                        draw_point(img, p, c);
                    }
                }
            }
            break;
        case 'e':
            for (int i = 0; i < length; i ++) {
                for (int j = 0; j < thickness; j++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point p;
                        p.x = start.x + i;
                        p.y = start.y - offset;
                        draw_point(img, p, c);
                    } else {
                        int offset = j - j / 2;
                        point p;
                        p.x = start.x + i;
                        p.y = start.y + offset;
                        draw_point(img, p, c);
                    }
                }
            }
            break;
        case 'w':
            for (int i = 0; i < length; i ++) {
                for (int j = 0; j < thickness; j++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point p;
                        p.x = start.x - i;
                        p.y = start.y - offset;
                        draw_point(img, p, c);
                    } else {
                        int offset = j - j / 2;
                        point p;
                        p.x = start.x - i;
                        p.y = start.y + offset;
                        draw_point(img, p, c);
                    }
                }
            }
            break;
    }
}

// given an image, a point, and a colour, draw the point onto the image
void draw_point(image img, point p, colour c) {
    int point_index = (3 * p.y * img.cols) + (3 * p.x);
    img.pointer[point_index] = c.r;
    img.pointer[point_index + 1] = c.g;
    img.pointer[point_index + 2] = c.b;
}

// draws the axis
void draw_axis(void *imgv, int rows, int cols) {
    image img;
    img.pointer = (u_int8_t *) imgv;
    img.rows = rows;
    img.cols = cols;

    int middle_row = (int) img.rows / 2;
    int middle_col = (int) img.cols / 2;

    // center of image
    point center;
    center.x = middle_col;
    center.y = middle_row;

    // leftmost point on drawn x-axis
    point middle_row_west;
    middle_row_west.x = 0;
    middle_row_west.y = middle_row;

    // highest point on drawn y-axis
    point middle_col_up;
    middle_col_up.x = middle_col;
    middle_col_up.y = 0;

    colour black;
    black.r = 0;
    black.g = 0;
    black.b = 0;

    // draw x-axis
    draw_line(img, middle_row_west, cols, 3, 'e', black);

    // draw y-axis
    draw_line(img, middle_col_up, rows, 3, 's', black);

    draw_x_ticks(img, center, 100, black);
    draw_y_ticks(img, center, 100, black);
}


// draws x-axis ticks
void draw_x_ticks(image img, point center, int tick_spacing, colour colour) {

    for (int i = tick_spacing; i < img.cols/2; i += tick_spacing) {
        point tick_center_index_pos;
        tick_center_index_pos.x = center.x + i;
        tick_center_index_pos.y = center.y;

        point tick_center_index_neg;
        tick_center_index_neg.x = center.x - i;
        tick_center_index_neg.y = center.y;

        // draw right side ticks
        draw_line(img, tick_center_index_pos, 9, 4, 'n', colour);
        draw_line(img, tick_center_index_pos, 9, 4, 's', colour);

        // draw left side ticks
        draw_line(img, tick_center_index_neg, 9, 4, 'n', colour);
        draw_line(img, tick_center_index_neg, 9, 4, 's', colour);
    }
}

// draws y-axis ticks
void draw_y_ticks(image img, point center, int tick_spacing, colour colour) {
    int center_index = (center.y * img.cols) + center.x;
    for (int i = tick_spacing; i < img.rows/2; i += tick_spacing) {
        point tick_center_index_pos;
        tick_center_index_pos.x = center.x;
        tick_center_index_pos.y = center.y + i;

        point tick_center_index_neg;
        tick_center_index_neg.x = center.x;
        tick_center_index_neg.y = center.y - i;

        // draw upper ticks (above y-axis)
        draw_line(img, tick_center_index_pos, 9, 4, 'e', colour);
        draw_line(img, tick_center_index_pos, 9, 4, 'w', colour);

        // draw lower ticks (below y-axis)
        draw_line(img, tick_center_index_neg, 9, 4, 'e', colour);
        draw_line(img, tick_center_index_neg, 9, 4, 'w', colour);
    }
}


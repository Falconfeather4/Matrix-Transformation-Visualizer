#include <stdio.h>
#include <math.h>
#include <stdlib.h>

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

void draw_axis(void *imgv, int rows, int cols, int unit_len);
void draw_x_ticks(image img, point center, int tick_spacing, int tick_length, int tick_thickness, colour colour);
void draw_y_ticks(image img, point center, int tick_spacing, int tick_length, int tick_thickness, colour colour);

void draw_i_j_hat(void *imgv, int rows, int cols, int unit_len);
void draw_arrow(image img, point p, char direction, colour c, int length, int thickness);

void draw_grid_lines(void *imgv, int rows, int cols, int unit_len);

void draw_eigenvectors(void *imgv, int rows, int cols, float slope, int undefined);

void overlay_image(void *bgv, void *overlayv, int rows, int cols);
int has_same_colour(image img, point p, colour c);
colour * get_colour_at_point(image img, point p);



// main is purely for testing purposes
int main() {
//    // test map_pixels()
//    int coordx[] = {2, 1, 0, 2, 1, 0};
//    int coordy[] = {1, 1, 1, 0, 0, 0};
    u_int8_t img[] = { 11, 12, 13, 21, 22, 23,31, 32, 33, 41, 42,
                       43,51, 52, 53, 61, 62, 63};
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

    draw_eigenvectors(img, 2, 3, 1, 1);



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
void draw_axis(void *imgv, int rows, int cols, int unit_len) {
    image img;
    img.pointer = (u_int8_t *) imgv;
    img.rows = rows;
    img.cols = cols;

    int middle_row = round(img.rows / 2);
    int middle_col = round(img.cols / 2);

    // center of image
    point center;
    center.x = middle_col;
    center.y = middle_row;

    // leftmost point on drawn x-axis
    point middle_row_west;
    middle_row_west.x = 0;
    middle_row_west.y = middle_row;

    // highest point on drawn y-axis
    point middle_col_north;
    middle_col_north.x = middle_col;
    middle_col_north.y = 0;

    colour black;
    black.r = 0;
    black.g = 0;
    black.b = 0;

    // draw x-axis
    draw_line(img, middle_row_west, cols, 4, 'e', black);

    // draw y-axis
    draw_line(img, middle_col_north, rows, 4, 's', black);

    // draw ticks
    draw_x_ticks(img, center, unit_len, 10, 5, black);
    draw_y_ticks(img, center, unit_len, 10, 5, black);

    // draw arrows
    point middle_row_east;
    middle_row_east.x = cols;
    middle_row_east.y = middle_row;

    draw_arrow(img, middle_row_east, 'e', black, 10, 6);
    draw_arrow(img, middle_col_north, 'n', black, 10, 6);
}


// draws x-axis ticks
void draw_x_ticks(image img, point center, int tick_spacing, int tick_length, int tick_thickness, colour colour) {
    for (int i = tick_spacing; i < img.cols/2; i += tick_spacing) {
        point tick_center_index_pos;
        tick_center_index_pos.x = center.x + i;
        tick_center_index_pos.y = center.y;

        point tick_center_index_neg;
        tick_center_index_neg.x = center.x - i;
        tick_center_index_neg.y = center.y;

        // draw right side ticks
        draw_line(img, tick_center_index_pos, tick_length / 2, tick_thickness, 'n', colour);
        draw_line(img, tick_center_index_pos, tick_length / 2, tick_thickness, 's', colour);

        // draw left side ticks
        draw_line(img, tick_center_index_neg, tick_length / 2, tick_thickness, 'n', colour);
        draw_line(img, tick_center_index_neg, tick_length / 2, tick_thickness, 's', colour);
    }
}

// draws y-axis ticks
void draw_y_ticks(image img, point center, int tick_spacing, int tick_length, int tick_thickness, colour colour) {
    int center_index = (center.y * img.cols) + center.x;
    for (int i = tick_spacing; i < img.rows/2; i += tick_spacing) {
        point tick_center_index_pos;
        tick_center_index_pos.x = center.x;
        tick_center_index_pos.y = center.y + i;

        point tick_center_index_neg;
        tick_center_index_neg.x = center.x;
        tick_center_index_neg.y = center.y - i;

        // draw upper ticks (above y-axis)
        draw_line(img, tick_center_index_pos, tick_length / 2, tick_thickness, 'e', colour);
        draw_line(img, tick_center_index_pos, tick_length / 2, tick_thickness, 'w', colour);

        // draw lower ticks (below y-axis)
        draw_line(img, tick_center_index_neg, tick_length / 2, tick_thickness, 'e', colour);
        draw_line(img, tick_center_index_neg, tick_length / 2, tick_thickness, 'w', colour);
    }
}


void draw_i_j_hat(void *imgv, int rows, int cols, int unit_len) {
    image img;
    img.pointer = (u_int8_t *) imgv;
    img.rows = rows;
    img.cols = cols;

    point center;
    center.x = round(cols / 2);
    center.y = round(rows / 2);

    colour green;
    green.r = 0;
    green.g = 255;
    green.b = 0;

    colour red;
    red.r = 255;
    red.g = 0;
    red.b = 0;

    // draw i hat
    draw_line(img, center, unit_len, 4, 'e', green);
    point arrow_center_i;
    arrow_center_i.x = center.x + unit_len;
    arrow_center_i.y = center.y;
    draw_arrow(img, arrow_center_i, 'e', green, 7, 4);

    // draw j hat
    draw_line(img, center, unit_len, 4, 'n', red);
    point arrow_center_j;
    arrow_center_j.x = center.x;
    arrow_center_j.y = center.y - unit_len;
    draw_arrow(img, arrow_center_j, 'n', red, 7, 4);
}


void draw_arrow(image img, point p, char direction, colour c, int length, int thickness) {
    switch (direction) {
        case 'n':
            for (int i = 0; i < length; i++) {
                for (int j = 0; j < thickness; j ++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point left;
                        left.x = p.x - i - offset;
                        left.y = p.y + i;

                        point right;
                        right.x = p.x + i + offset;
                        right.y = p.y + i;

                        draw_point(img, left, c);
                        draw_point(img, right, c);
                    } else {
                        int offset = j - j / 2;
                        point left;
                        left.x = p.x - i - offset;
                        left.y = p.y + i;

                        point right;
                        right.x = p.x + i + offset;
                        right.y = p.y + i;

                        draw_point(img, left, c);
                        draw_point(img, right, c);
                    }
                }
            }
            break;
        case 's':
            for (int i = 0; i < length; i++) {
                for (int j = 0; j < thickness; j ++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point left;
                        left.x = p.x - i - offset;
                        left.y = p.y - i;

                        point right;
                        right.x = p.x + i + offset;
                        right.y = p.y - i;

                        draw_point(img, left, c);
                        draw_point(img, right, c);
                    } else {
                        int offset = j - j / 2;
                        point left;
                        left.x = p.x - i - offset;
                        left.y = p.y - i;

                        point right;
                        right.x = p.x + i + offset;
                        right.y = p.y - i;

                        draw_point(img, left, c);
                        draw_point(img, right, c);
                    }
                }
            }
            break;
        case 'e':
            for (int i = 0; i < length; i++) {
                for (int j = 0; j < thickness; j ++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point top;
                        top.x = p.x - i;
                        top.y = p.y - i - offset;

                        point bottom;
                        bottom.x = p.x - i;
                        bottom.y = p.y + i + offset;

                        draw_point(img, top, c);
                        draw_point(img, bottom, c);
                    } else {
                        int offset = j - j / 2;
                        point top;
                        top.x = p.x - i;
                        top.y = p.y - i - offset;

                        point bottom;
                        bottom.x = p.x - i;
                        bottom.y = p.y + i + offset;

                        draw_point(img, top, c);
                        draw_point(img, bottom, c);
                    }
                }
            }
            break;
        case 'w':
            for (int i = 0; i < length; i++) {
                for (int j = 0; j < thickness; j ++) {
                    if (j % 2) {
                        int offset = j - (j - 1)/2;
                        point top;
                        top.x = p.x + i;
                        top.y = p.y - i - offset;

                        point bottom;
                        bottom.x = p.x + i;
                        bottom.y = p.y + i + offset;

                        draw_point(img, top, c);
                        draw_point(img, bottom, c);
                    } else {
                        int offset = j - j / 2;
                        point top;
                        top.x = p.x + i;
                        top.y = p.y - i - offset;

                        point bottom;
                        bottom.x = p.x + i;
                        bottom.y = p.y + i + offset;

                        draw_point(img, top, c);
                        draw_point(img, bottom, c);
                    }
                }
            }
            break;
    }
}


void draw_grid_lines(void *imgv, int rows, int cols, int unit_len) {
    image img;
    img.pointer = (u_int8_t *) imgv;
    img.rows = rows;
    img.cols = cols;

    int middle_row = round(img.rows / 2);
    int middle_col = round(img.cols / 2);

    // center of image
    point center;
    center.x = middle_col;
    center.y = middle_row;

    colour cyan;
    cyan.r = 0;
    cyan.g = 255;
    cyan.b = 255;

    // use tick function to draw grid; one grid line is just very long tick
    draw_x_ticks(img, center, unit_len, img.rows, 2, cyan);
    draw_y_ticks(img, center, unit_len, img.cols, 2, cyan);

    // leftmost point on drawn x-axis
    point middle_row_west;
    middle_row_west.x = 0;
    middle_row_west.y = middle_row;

    // highest point on drawn y-axis
    point middle_col_north;
    middle_col_north.x = middle_col;
    middle_col_north.y = 0;

    // draw along xy-axis since tick function avoids the axis
    draw_line(img, middle_row_west, img.cols, 2, 'e', cyan);
    draw_line(img, middle_col_north, img.rows, 2, 's', cyan);

}

// given an image and a slope, draws the eigenvectors. If the slope is undefined, undefined will be set to 1,
// and a vertical line will be drawn
void draw_eigenvectors(void *imgv, int rows, int cols, float slope, int undefined) {
    image img;
    img.pointer = (u_int8_t *) imgv;
    img.rows = rows;
    img.cols = cols;

    colour purple;
    purple.r = 140;
    purple.g = 15;
    purple.b = 255;

    int middle_row = round(img.rows / 2);
    int middle_col = round(img.cols / 2);

    point center;
    center.x = middle_col;
    center.y = middle_row;

    if (undefined) {
        point top_center;
        top_center.x = middle_col;
        top_center.y = 0;
        draw_line(img, top_center, rows, 1, 's', purple);
    } else{
        // point for drawing in the positive x direction
        point current_pos;
        current_pos.x = center.x;
        current_pos.y = center.y;

        // nest positive point
        point prev_pos;
        prev_pos.x = current_pos.x;
        prev_pos.y = current_pos.y;

        // point for drawing in the negative x direction
        point current_neg;
        current_neg.x = center.x;
        current_neg.y = center.y;

        // next negative point
        point prev_neg;
        prev_neg.x = current_neg.x;
        prev_neg.y = current_neg.y;

        while ((0 <= current_pos.x && current_pos.x < img.cols) && (0 <= current_pos.y && current_pos.y < img.rows)) {
            int gap_length = abs(current_pos.y - prev_pos.y);
            if (slope > 0) {
                // draws a line from current pos position vertically downwards until the y value of the prev point
                draw_line(img, current_pos, gap_length + 1, 1, 's', purple);

                // draws a line from current neg position vertically upwards until the y value of the prev point.
                draw_line(img, current_neg, gap_length + 1, 1, 'n', purple);
            } else {
            // draws a line from current pos position vertically upwards until the y value of the prev point
            draw_line(img, current_pos, gap_length + 1, 1, 'n', purple);

            // draws a line from current neg position vertically downwards until the y value of the prev point.
             draw_line(img, current_neg, gap_length + 1, 1, 's', purple);
            }

            // set the next point as the current point
            prev_pos.x = current_pos.x;
            prev_pos.y = current_pos.y;
            prev_neg.x = current_neg.x;
            prev_neg.y = current_neg.y;

            // calculate the next point
            // Formula used: (curr_y - prev_y)/(curr_x - prev_x) = -slope
            // negative sign on slope is because the y-axis is flipped
            current_pos.x++;
            current_pos.y = round(center.y - slope * (current_pos.x - center.x));

            current_neg.x--;
            current_neg.y = round(center.y - slope * (current_neg.x - center.x));
        }
    }
}

// overlays overlay img on top of bg img, ignoring white pixels
void overlay_image(void *bgv, void *overlayv, int rows, int cols) {
    image bg;
    bg.pointer = (u_int8_t *) bgv;
    bg.rows = rows;
    bg.cols = cols;

    image overlay;
    overlay.pointer = (u_int8_t *) overlayv;
    overlay.rows = rows;
    overlay.cols = cols;

    colour white;
    white.r = 255;
    white.g = 255;
    white.b = 255;

    for (int x = 0; x < cols; x++) {
        for (int y = 0; y < rows; y++) {
            point position;
            position.x = x;
            position.y = y;
            if (!has_same_colour(overlay, position, white)) {
                colour * point_colour = get_colour_at_point(overlay, position);
                draw_point(bg, position, *point_colour);
                free(point_colour);
            }
        }
    }
}


// determines if the point on an image is a given colour
int has_same_colour(image img, point p, colour c) {
    colour * point_colour = get_colour_at_point(img, p);
    int same_colour = point_colour->r == c.r && point_colour->g == c.g && point_colour->b == c.b;
    free(point_colour);

    return same_colour;
}

// returns a pointer to the colour at a given point on an image
colour * get_colour_at_point(image img, point p) {
    int point_index = (3 * p.y * img.cols) + (3 * p.x);

    colour * point_colour;
    point_colour = (colour *) malloc(sizeof(colour));

    point_colour->r = img.pointer[point_index];
    point_colour->g = img.pointer[point_index + 1];
    point_colour->b = img.pointer[point_index + 2];

    return point_colour;
}

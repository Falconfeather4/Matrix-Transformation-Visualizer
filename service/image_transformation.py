import ctypes
import cv2
import numpy as np
from numpy import linalg as LA
import config


# linking function from c
lib = ctypes.cdll.LoadLibrary('c_funcs/imageTranformation.so')
map_pixels = lib.map_pixels
draw_axis_c = lib.draw_axis
draw_i_j_hat_c = lib.draw_i_j_hat
draw_grid_lines_c = lib.draw_grid_lines
draw_eigenvectors_c = lib.draw_eigenvectors
overlay_image_c = lib.overlay_image


# takes in an image and a 2x2 transformation matrix, applies the
# transformation, and returns the transformed image
def transform_image(img, matrix):
    rows, cols, layers = img.shape
    # creates white background image
    background_img = np.full((rows, cols, layers), 255).astype('uint8')

    # make the matrix of coordinates
    col_base = np.arange(cols)
    x_coords = np.tile(col_base, rows)
    row_base = np.arange(rows)
    y_coords = np.repeat(row_base, cols)
    coord_matrix = np.vstack((x_coords, y_coords))

    # make transformation vector to move center of coordinates to origin
    translation_vector = np.array([[-cols / 2], [-rows / 2]])
    translated_coord_matrix = coord_matrix + translation_vector
    # flip y-axis
    translated_coord_matrix = (np.array([[1, 0], [0, -1]]) @ translated_coord_matrix)
    # do linear algebra to transform each vector
    transformed_coords = (matrix @ translated_coord_matrix)
    # flip y-axis back
    transformed_coords = (np.array([[1, 0], [0, -1]]) @ transformed_coords)
    # move back to original position
    translation_vector_inverse = np.array([[cols / 2], [rows / 2]])
    transformed_coords = transformed_coords + translation_vector_inverse
    transformed_coords = transformed_coords.astype('int32')

    # fn transformed_coords, img, rows, cols, background_img --> background_img
    # map each pixel in layer of img to background img corresponding to transformed_coords
    map_pixels(ctypes.c_void_p(transformed_coords[0].ctypes.data), ctypes.c_void_p(transformed_coords[1].ctypes.data),
               ctypes.c_void_p(img.ctypes.data), ctypes.c_void_p(background_img.ctypes.data),
               ctypes.c_int(rows), ctypes.c_int(cols))

    return background_img;


# given image, adds advanced features based on settings in config.py
def do_transformations(img, matrix):
    image = np.copy(img)
    rows, cols, layers = image.shape

    if config.grid_lines:
        draw_grid_lines_c(ctypes.c_void_p(image.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                          ctypes.c_int(config.unit_length))
    if config.determinant:
        image = draw_determinant(image, rows, cols)
    if config.eigenvectors:
        draw_eigenvectors(image, rows, cols)

    # if axis are off but i_j_hats are on:
    if (not config.axis) and config.i_j_hat:
        draw_i_j_hat_c(ctypes.c_void_p(image.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                       ctypes.c_int(config.unit_length))

    image = transform_image(image, matrix)

    # if axis are on, draw them after transformation. If i_j_hats are also on, then they must be
    # separately transformed and then overlayed onto original image, since ij hats must appear
    # in front of the axis
    if config.axis:
        draw_axis_c(ctypes.c_void_p(image.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                    ctypes.c_int(config.unit_length))
        if config.i_j_hat:
            blank = np.full((rows, cols, layers), 255).astype('uint8')
            draw_i_j_hat_c(ctypes.c_void_p(blank.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                           ctypes.c_int(config.unit_length))
            blank = transform_image(blank, matrix)
            overlay_image_c(ctypes.c_void_p(image.ctypes.data), ctypes.c_void_p(blank.ctypes.data),
                            ctypes.c_int(rows), ctypes.c_int(cols))

    return image





# draws the determinant onto the image
def draw_determinant(img, rows, cols):
    overlay = img.copy()

    # Rectangle parameters
    x, y, width, height = int(cols/2), int(rows/2), config.unit_length, config.unit_length
    # A filled rectangle
    cv2.rectangle(overlay, (x, y), (x + config.unit_length, y - config.unit_length), (255, 255, 0), -1)

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle
    # over the image
    image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    return image_new


# draws the eigenvectors onto the image
def draw_eigenvectors(img, rows, cols):
    matrix = config.transformation_matrix
    value, vector = LA.eig(matrix);

    value1_x = vector[0][0]
    value1_y = vector[1][0]

    value2_x = vector[0][1]
    value2_y = vector[1][1]

    # making sure slope exists for first vector
    if not(isinstance(value1_x, complex) or isinstance(value1_y, complex)):
        if value1_x != 0:
            slope = value1_y / value1_x
            draw_eigenvectors_c(ctypes.c_void_p(img.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
            ctypes.c_float(float(slope)), 0)
        else:
            # 0.1 is just a random float
            draw_eigenvectors_c(ctypes.c_void_p(img.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                                ctypes.c_float(0.1), 1)

    # now for second vector
    if not(isinstance(value2_x, complex) or isinstance(value2_y, complex)):
        if value2_x != 0:
            slope = value2_y / value2_x
            draw_eigenvectors_c(ctypes.c_void_p(img.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                                ctypes.c_float(float(slope)), 0)
        else:
            # 0.1 is just a random float
            draw_eigenvectors_c(ctypes.c_void_p(img.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                                ctypes.c_float(0.1), 1)



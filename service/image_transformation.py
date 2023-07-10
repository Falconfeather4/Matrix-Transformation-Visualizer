import numpy as np
import ctypes

# linking map_pixels function from c
lib = ctypes.cdll.LoadLibrary('c_funcs/imageTranformation.so')
map_pixels = lib.map_pixels


# takes in an image and a 2x2 transformation matrix, applies the
#transformation, and returns the transformed image
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
    translation_vector = np.array([[-cols/2], [-rows/2]])
    translated_coord_matrix = coord_matrix + translation_vector
    # flip y axis
    translated_coord_matrix = (np.array([[1, 0], [0, -1]]) @ translated_coord_matrix)
    # do linear algebra to transform each vector
    transformed_coords = (matrix @ translated_coord_matrix)
    # flip y axis back
    transformed_coords = (np.array([[1, 0], [0, -1]]) @ transformed_coords)
    # move back to original position
    translationVectorInverse = np.array([[cols/2], [rows/2]])
    transformed_coords = transformed_coords + translationVectorInverse
    transformed_coords = transformed_coords.astype('int32')

    # fn transformed_coords, img, rows, cols, background_img --> background_img
    # map each pixel in layer of img to background img corresponding to transformed_coords
    map_pixels(ctypes.c_void_p(transformed_coords[0].ctypes.data), ctypes.c_void_p(transformed_coords[1].ctypes.data),
                ctypes.c_void_p(img.ctypes.data), ctypes.c_void_p(background_img.ctypes.data),
                ctypes.c_int(rows), ctypes.c_int(cols))

    return background_img;


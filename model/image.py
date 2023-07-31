import ctypes
import cv2
import numpy as np
from numpy import linalg


# linking function from c
lib = ctypes.cdll.LoadLibrary('c_funcs/imageTranformation.so')
map_pixels = lib.map_pixels
draw_axis_c = lib.draw_axis
draw_i_j_hat_c = lib.draw_i_j_hat
draw_grid_lines_c = lib.draw_grid_lines
draw_eigenvectors_c = lib.draw_eigenvectors
overlay_image_c = lib.overlay_image


# And Image that contains an 3d np array representing rgb pixels
class Image:
    img_root_path = "./images/"

    def __init__(self, name=None, image_array=None):
        if image_array is None:
            self.name = name
            bgr_img = cv2.imread(self.img_root_path + name)
            self.image_array = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            self.resize(600)
        else:
            self.image_array = image_array
            self.resize(600)

    def clone(self):
        clone = Image("", np.copy(self.image_array))
        return clone

    def resize(self, max_size):
        rows, cols, layers = self.image_array.shape
        if rows > max_size or cols > max_size:
            if rows > cols:
                height = max_size
                width = int(height * (cols / rows))
            else:
                width = max_size
                height = int(width * (cols / rows))
            self.image_array = cv2.resize(self.image_array, (width, height))

    # takes in an image and a 2x2 transformation matrix, and applies the transformation
    def transform(self, matrix):
        rows, cols, layers = self.image_array.shape
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
        map_pixels(ctypes.c_void_p(transformed_coords[0].ctypes.data),
                   ctypes.c_void_p(transformed_coords[1].ctypes.data),
                   ctypes.c_void_p(self.image_array.ctypes.data), ctypes.c_void_p(background_img.ctypes.data),
                   ctypes.c_int(rows), ctypes.c_int(cols))

        self.image_array = background_img

    def do_transformations(self, matrix, options):
        image_copy = self.clone()
        rows, cols, layers = image_copy.image_array.shape

        if options.grid_lines:
            draw_grid_lines_c(ctypes.c_void_p(image_copy.image_array.ctypes.data), ctypes.c_int(rows),
                              ctypes.c_int(cols), ctypes.c_int(options.unit_length))
        if options.determinant:
            image_copy.draw_determinant(rows, cols, options)
        if options.eigenvectors:
            image_copy.draw_eigenvectors(rows, cols, options)

        # if axis are off but i_j_hats are on:
        if (not options.axis) and options.i_j_hat:
            draw_i_j_hat_c(ctypes.c_void_p(image_copy.image_array.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                           ctypes.c_int(options.unit_length))

        image_copy.transform(matrix)

        # if axis are on, draw them after transformation. If i_j_hats are also on, then they must be
        # separately transformed and then overlayed onto original image, since ij hats must appear in front of the axis
        if options.axis:
            draw_axis_c(ctypes.c_void_p(image_copy.image_array.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                        ctypes.c_int(options.unit_length))
            if options.i_j_hat:
                blank = Image("", np.full((rows, cols, layers), 255).astype('uint8'))
                draw_i_j_hat_c(ctypes.c_void_p(blank.image_array.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                               ctypes.c_int(options.unit_length))
                blank.transform(matrix)
                overlay_image_c(ctypes.c_void_p(image_copy.image_array.ctypes.data),
                                ctypes.c_void_p(blank.image_array.ctypes.data),
                                ctypes.c_int(rows), ctypes.c_int(cols))
        self.image_array = image_copy.image_array

    # draws the determinant onto the image
    def draw_determinant(self, rows, cols, options):
        overlay = self.clone()
        x, y, width, height = int(cols / 2), int(rows / 2), options.unit_length, options.unit_length
        cv2.rectangle(overlay.image_array, (x, y), (x + options.unit_length, y - options.unit_length),
                      (255, 255, 0), -1)

        alpha = 0.4
        image_new = Image("", cv2.addWeighted(overlay.image_array, alpha, self.image_array, 1 - alpha, 0))
        self.image_array = image_new.image_array

    # draws eigenvectors onto image
    def draw_eigenvectors(self, rows, cols, options):
        matrix = options.transformation_matrix
        value, vector = linalg.eig(matrix)

        value1_x = vector[0][0]
        value1_y = vector[1][0]
        value2_x = vector[0][1]
        value2_y = vector[1][1]

        if not (isinstance(value1_x, complex) or isinstance(value2_y, complex)):
            self.draw_eigenvector(value1_x, value1_y, rows, cols)
            self.draw_eigenvector(value2_x, value2_y, rows, cols)

    def draw_eigenvector(self, val_x, val_y, rows, cols):
        if val_x != 0:
            slope = val_y / val_x
            draw_eigenvectors_c(ctypes.c_void_p(self.image_array.ctypes.data),
                                ctypes.c_int(rows), ctypes.c_int(cols), ctypes.c_float(float(slope)), 0)
        else:
            # 0.1 is just a random float
            draw_eigenvectors_c(ctypes.c_void_p(self.image_array.ctypes.data),
                                ctypes.c_int(rows), ctypes.c_int(cols), ctypes.c_float(0.1), 1)

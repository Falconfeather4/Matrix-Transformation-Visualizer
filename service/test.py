import image_transformation
import cv2
import config
import numpy as np
from numpy import linalg as LA
import image_transformation
import ctypes

# matrix:
# | 1 2 |
# | 0 3 |

#eigens: <1, 0> --> 1
#        <1, 1> --> 3

# matrix = np.array([[1, 2], [0, 3]])
# value, vector = LA.eig(matrix);

# print(vector)

# print(value)






# linking function from c
lib = ctypes.cdll.LoadLibrary('c_funcs/imageTranformation.so')
map_pixels = lib.map_pixels
draw_axis_c = lib.draw_axis
draw_i_j_hat_c = lib.draw_i_j_hat
draw_grid_lines_c = lib.draw_grid_lines
draw_eigenvectors_c = lib.draw_eigenvectors
overlay_image_c = lib.overlay_image

img = cv2.imread('images/ubc_logo.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rows, cols, layers = np.shape(img)
blank = np.full((rows, cols, layers), 255).astype('uint8')

draw_i_j_hat_c(ctypes.c_void_p(blank.ctypes.data), ctypes.c_int(rows), ctypes.c_int(cols),
                       ctypes.c_int(config.unit_length))

def draw():
    overlay_image_c(ctypes.c_void_p(img.ctypes.data), ctypes.c_void_p(blank.ctypes.data), ctypes.c_int(rows),
                    ctypes.c_int(cols))
draw()








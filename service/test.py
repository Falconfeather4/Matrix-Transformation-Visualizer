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

# draws the determinant onto the image
def draw_determinant(img, rows, cols):
    overlay = img.copy()

    # Rectangle parameters
    x, y, width, height = int(cols/2), int(rows/2) + config.unit_length, config.unit_length, config.unit_length
    # A filled rectangle
    cv2.rectangle(overlay, (x, y), (2, 2), (0, 255, 255), -1)

    #
    # alpha = 0.4  # Transparency factor.
    #
    # # Following line overlays transparent rectangle
    # # over the image
    # image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

img = cv2.imread('images/ubc_logo.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rows, cols, layers = np.shape(img)
blank = np.full((rows, cols, layers), 255).astype('uint8')

draw_determinant(blank, rows, cols)


# cv2.imshow('image', img)
# cv2.imshow('image', blank)
# cv2.waitKey(0)



def test():
    image = cv2.imread('images/ubc_logo.jpg')
    overlay = image.copy()

    # Rectangle parameters
    x, y, w, h = 10, 10, 300, 300
    # A filled rectangle
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 200, 0), -1)

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle
    # over the image
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    # cv2.imshow("some", image_new)
    # cv2.waitKey(0)
    #
    # cv2.destroyAllWindows()

test()






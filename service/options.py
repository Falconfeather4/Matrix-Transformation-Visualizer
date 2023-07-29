import numpy as np
from os import listdir


# options data structure
class Options:
    axis = True
    eigenvectors = True
    grid_lines = True
    i_j_hat = True
    determinant = True
    unit_length = 80
    transformation_matrix = np.array([[1, 0.5], [-0.5, -1]])
    fps = 30

    # all images in ./images folder except hidden files
    image_names = [f for f in listdir("./images") if not f.startswith('.')]
    image = image_names[0]
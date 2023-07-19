# stores and initializes global variables
import numpy as np

# set the below values to True to turn on of False to turn off
axis = True
eigenvectors = True
grid_lines = True
i_j_hat = True
determinant = True

# this determins the spacing between the tick marks / grid lines / size of the
# determinant. It is measured in pixels.
unit_length = 80

transformation_matrix = np.array([[1, 0.5], [-0.5, 1]])
image_names = ["ubc_logo.jpg", "bunny.jpg"]
image_root_path = "images/"




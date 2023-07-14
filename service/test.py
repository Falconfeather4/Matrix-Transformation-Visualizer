import image_transformation
import cv2
import config
import numpy as np
from numpy import linalg as LA

# matrix:
# | 1 2 |
# | 0 3 |

#eigens: <1, 0> --> 1
#        <1, 1> --> 3


matrix = np.array([[1, 2], [0, 3]])
value, vector = LA.eig(matrix);



# print(vector)
# print(value)

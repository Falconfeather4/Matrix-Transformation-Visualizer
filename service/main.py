import matplotlib.pyplot as plt
import numpy as np
import math
import ctypes


from ctypes import *
array = np.array([[[1,1,1],[2,2,2],[3,3,3]], [[4,4,4],[5,5,5],[6,6,6]]])
print(np.shape(array))
print(array[1])




matrix = np.array([[0, -1], [1, 0]])

values = np.array([[-3, -2, -1, 0, 1, 2, 3], [-3, -2, -1, 0, 1, 2, 3]])


transformedValue = (matrix @ values)

xValues = transformedValue[0]
yValues = transformedValue[1]












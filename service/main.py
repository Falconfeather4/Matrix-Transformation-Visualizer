import matplotlib.pyplot as plt
import numpy as np
import math
import ctypes


from ctypes import *
array = np.array([[[1,1,1],[2,2,2],[3,3,3]], [[4,4,4],[5,5,5],[6,6,6]]])
print(np.shape(array))
print(array[1])


# indata = np.ones((5,6), dtype=np.double)
# outdata = np.zeros((5,6), dtype=np.double)
# lib = ctypes.cdll.LoadLibrary('./test.so')
# fun = lib.cfun
# # Here comes the fool part.
# fun(ctypes.c_void_p(indata.ctypes.data), ctypes.c_int(5), ctypes.c_int(6), ctypes.c_void_p(outdata.ctypes.data))
#
# print('indata: %s' % indata)
# print('outdata: %s' % outdata)




matrix = np.array([[0, -1], [1, 0]])

values = np.array([[-3, -2, -1, 0, 1, 2, 3], [-3, -2, -1, 0, 1, 2, 3]])


transformedValue = (matrix @ values)

xValues = transformedValue[0]
yValues = transformedValue[1]

#print (xValues, ":", yValues)
#
# # Drawing the plot:
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
#
# # move axis to center
# ax.spines['left'].set_position('center')
# ax.spines['bottom'].set_position('center')
#
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
#
# # Show ticks in the left and lower axes only
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
#
# plt.xlim(-5, 5)
# plt.ylim(-5, 5)
#
# plt.plot(xValues, yValues, 'o:r')
# plt.show()


# centers image on graph
# plt.imshow(img,  extent=[-cols/2., cols/2., -rows/2., rows/2. ])
#
# plt.show()











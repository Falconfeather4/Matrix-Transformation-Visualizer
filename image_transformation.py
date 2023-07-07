import ctypes
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2

img = cv2.imread('ubc_logo.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rows, cols, layers = img.shape


# linking map_pixels function from c
lib = ctypes.cdll.LoadLibrary('imageTranformation.so')
map_pixels = lib.map_pixels


# takes in an image and a 2x2 transformation matrix, applies the
#transformation, and returns the transformed image

def transform_image(img, matrix):
    rows, cols, layers = img.shape
    # creates white background image
    background_img = np.ndarray.tolist(np.full((rows, cols), 255))
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
    transformed_coords = transformed_coords.astype(int)

    # map each pixel in original image to background img according
    # to the positions in transformed_coords
    fullImg = np.array([])
    for i in range(layers):
        # fn transformed_coords, np.dsplit(img, 3)[i], rows, cols, background_img --> background_img
        # map each pixel in layer of img to background img corresponding to transformed_coords
        for j in range(rows * cols):
            x_val = transformed_coords[0, j]
            y_val = transformed_coords[1, j]
            if ((x_val >= 0) and (x_val < cols)) and ((y_val >= 0) and (y_val < rows)):
                background_img[y_val][x_val] = img[math.floor(j/cols), j%cols, i]
        # fn ends here
        if (i == 0):
            fullImg = np.array(background_img)
        else:
            fullImg = np.dstack((fullImg, background_img))

    return fullImg

idMatrix = np.array([[1, -2], [0,1]])
img2 = transform_image(img, idMatrix).astype('uint8')



plt.imshow(img2,  extent=[-cols/2., cols/2., -rows/2., rows/2. ])
plt.show()
print("done")

# cv2.imshow('image',img)
# cv2.waitKey(0)





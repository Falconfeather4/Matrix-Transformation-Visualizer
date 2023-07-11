import image_transformation
import cv2
import config

img = cv2.imread(config.image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = image_transformation.draw_axis()


# resizing img

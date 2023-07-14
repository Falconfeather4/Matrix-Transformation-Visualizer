import numpy as np
import image_transformation
import cv2
import pygame
from ui import *
import config

# starts the program
config.sync_global_vars()
start()

# loads img from path stored in config
img = cv2.imread(config.image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# resizing img
rows, cols, layers = img.shape
if (rows > 600 or cols > 600):
    if (rows > cols):
        height = 600;
        width = int(height * (cols / rows))
    else:
        width = 600;
        height = int(width * (cols / rows))
    img = cv2.resize(img, (width, height))
rows, cols, layers = img.shape


# creating matrices used in transformation
matrix = config.transformation_matrix
identity_matrix = np.array([[1, 0], [0, 1]])
delta_matrix = matrix - identity_matrix
step_matrix = 0.01 * delta_matrix;


# creating frames used in animation
frames = []
for i in range(100):
    transf_matrix = identity_matrix + i * step_matrix
    transformed_img = image_transformation.transform_image(img, transf_matrix)
    frames.append(transformed_img)


# initializing pygame
pygame.init()
window = pygame.display.set_mode((cols + cols / 50, rows + rows / 50))
clock = pygame.time.Clock()
index = 0
running = True


# display animation
while running:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if index >= len(frames):
        index = len(frames)
        continue
    display_img = cv2.transpose(frames[index])
    pygame_surface = pygame.surfarray.make_surface(display_img)
    x = 0
    y = 0
    window.blit(pygame_surface, (x, y))
    pygame.display.update()

    index += 1

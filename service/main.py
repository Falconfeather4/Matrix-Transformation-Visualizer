import numpy as np
import image_transformation
import cv2
import pygame

img = cv2.imread('ubc_logo.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rows, cols, layers = img.shape

# creating matricies used in transformation
matrix = np.array([[-1, 0.5], [-1, -1]])
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

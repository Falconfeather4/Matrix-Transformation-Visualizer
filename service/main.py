import numpy as np
import image_transformation
import cv2
import pygame
import pygame_gui
import config
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextEntryLine


# resizes img
def resize_image(img, size):
    rows, cols, layers = img.shape
    if (rows > size or cols > size):
        if (rows > cols):
            height = size;
            width = int(height * (cols / rows))
        else:
            width = size;
            height = int(width * (cols / rows))
        img = cv2.resize(img, (width, height))
    return img


identity_matrix = np.array([[1, 0], [0, 1]])
frame_num = 70
# calculates step matrix (which is used in transformation)
def calculate_step_matrix():
    matrix = config.transformation_matrix
    delta_matrix = matrix - identity_matrix
    step_matrix = 1 / frame_num * delta_matrix;
    return step_matrix


# initializing pygame
pygame.init()
pygame.display.set_caption('Linear Transformations')
window = pygame.display.set_mode((1100, 800))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1100, 800))

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 700), (100, 50)),
                                           text='Play', manager=manager)
image_dropdown = UIDropDownMenu(options_list=config.image_names, starting_option=config.image_names[0],
                                relative_rect=pygame.Rect(50, 50, 400, 50),
                                manager=manager, expansion_height_limit=100)

matrix_label = UILabel(text="Transformation Matrix:", relative_rect=pygame.Rect((50, 220), (200, 50), manager=manager))
top_left_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(300, 210, 50, 40),
                                        initial_text=str(config.transformation_matrix[0][0]))
top_right_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(355, 210, 50, 40),
                                         initial_text=str(config.transformation_matrix[0][1]))
bottom_left_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(300, 255, 50, 40),
                                           initial_text=str(config.transformation_matrix[1][0]))
bottom_right_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(355, 255, 50, 40),
                                            initial_text=str(config.transformation_matrix[1][1]))

unit_length_lable = UILabel(text="Unit Length:", relative_rect=pygame.Rect((50, 350), (100, 40)), manager=manager)
unit_length_input = UITextEntryLine(relative_rect=pygame.Rect(170, 350, 50, 40), initial_text=str(config.unit_length))

axis_label = UILabel(text="Axis:", relative_rect=pygame.Rect((50, 460), (100, 40)), manager=manager)
eigenvector_label = UILabel(text="Eigenvectors:", relative_rect=pygame.Rect((50, 520), (110, 40)), manager=manager)
grid_lines_label = UILabel(text="Grid Lines:", relative_rect=pygame.Rect((50, 580), (100, 40)), manager=manager)
i_j_hat_label = UILabel(text="i-j hat:", relative_rect=pygame.Rect((50, 640), (100, 40)), manager=manager)
determinant_label = UILabel(text="Determinant:", relative_rect=pygame.Rect((50, 700), (100, 40)), manager=manager)

yes_no_options = ["yes", "no"]
axis_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                               relative_rect=pygame.Rect(170, 460, 280, 40),
                               manager=manager, expansion_height_limit=100)
eigenvector_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                      relative_rect=pygame.Rect(170, 520, 280, 40),
                                      manager=manager, expansion_height_limit=100)
grid_lines_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                     relative_rect=pygame.Rect(170, 580, 280, 40),
                                     manager=manager, expansion_height_limit=100)
i_j_hat_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                  relative_rect=pygame.Rect(170, 640, 280, 40),
                                  manager=manager, expansion_height_limit=100)
determinant_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                      relative_rect=pygame.Rect(170, 700, 280, 40),
                                      manager=manager, expansion_height_limit=100)

index = 0
running = True
playing = False
preview = True

last_display_surface = None
# display animation
while running:
    window.fill(pygame.Color(128, 128, 128, 255))
    time_delta = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            preview = True
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                playing = True
                preview = False

                img = cv2.imread(config.image_root_path + image_dropdown.selected_option)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = resize_image(img, 600)

                config.transformation_matrix = np.array([[float(top_left_matrix_input.get_text()),
                                                          float(top_right_matrix_input.get_text())],
                                                         [float(bottom_left_matrix_input.get_text()),
                                                          float(bottom_right_matrix_input.get_text())]])

                config.unit_length = int(unit_length_input.get_text())

                config.axis = True if axis_dropdown.selected_option == "yes" else False
                config.eigenvectors = True if eigenvector_dropdown.selected_option == "yes" else False
                config.grid_lines = True if grid_lines_dropdown.selected_option == "yes" else False
                config.i_j_hat = True if i_j_hat_dropdown.selected_option == "yes" else False
                config.determinant = True if determinant_dropdown.selected_option == "yes" else False

        manager.process_events(event)

    if preview:
        tl = top_left_matrix_input.get_text()
        tr = top_right_matrix_input.get_text()
        bl = bottom_left_matrix_input.get_text()
        br = bottom_right_matrix_input.get_text()
        config.transformation_matrix = np.array([[float(tl) if not (tl == "" or tl == "-") else 1.0,
                                                  float(tr) if not (tr == "" or tr == "-") else 1.0],
                                                 [float(bl) if not (bl == "" or bl == "-") else 1.0,
                                                  float(br) if not (br == "" or br == "-") else 1.0]])

        config.unit_length = int(unit_length_input.get_text()) \
            if not (unit_length_input.get_text() == "" or int(unit_length_input.get_text()) < 10) else 10

        config.axis = True if axis_dropdown.selected_option == "yes" else False
        config.eigenvectors = True if eigenvector_dropdown.selected_option == "yes" else False
        config.grid_lines = True if grid_lines_dropdown.selected_option == "yes" else False
        config.i_j_hat = True if i_j_hat_dropdown.selected_option == "yes" else False
        config.determinant = True if determinant_dropdown.selected_option == "yes" else False

        preview_img = img = cv2.imread(config.image_root_path + image_dropdown.selected_option)
        preview_img = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
        preview_img = resize_image(preview_img, 600)
        preview_img = image_transformation.do_transformations(preview_img, identity_matrix)

        if config.eigenvectors:
            rows, cols, layers = preview_img.shape
            image_transformation.draw_eigenvectors(preview_img, rows, cols)
        preview_img = cv2.transpose(preview_img)
        pygame_surface = pygame.surfarray.make_surface(preview_img)

        x = 600
        y = 50
        window.blit(pygame_surface, (x, y))

    if playing:
        if index >= frame_num:
            index = 0
            playing = False
            continue

        transf_matrix = identity_matrix + index * calculate_step_matrix()
        transformed_img = image_transformation.do_transformations(img, transf_matrix)

        display_img = cv2.transpose(transformed_img)
        pygame_surface = pygame.surfarray.make_surface(display_img)
        last_display_surface = pygame_surface
        x = 600
        y = 50
        window.blit(pygame_surface, (x, y))

        index += 1
    elif not (last_display_surface is None):
        x = 600
        y = 50
        window.blit(pygame_surface, (x, y))

    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.update()

pygame.quit()

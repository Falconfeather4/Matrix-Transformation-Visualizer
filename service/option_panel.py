import numpy as np
import pygame
from os import listdir
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextEntryLine



class Options:
    # default options
    axis = True
    eigenvectors = True
    grid_lines = True
    i_j_hat = True
    determinant = True
    unit_length = 80
    transformation_matrix = np.array([[1, 0.5], [-0.5, -1]])

    # all images in ./images folder except hidden files
    path = "./images"
    image_names = [f for f in listdir(path) if not f.startswith('.')]
    image = image_names[0]



class OptionController:
    options = Options()

    def __init__(self, manager):
        path = "./images"
        image_names = [f for f in listdir(path) if not f.startswith('.')]
        self.image_dropdown = UIDropDownMenu(options_list=image_names, starting_option=image_names[0],
                                             relative_rect=pygame.Rect(50, 50, 400, 50),
                                             manager=manager, expansion_height_limit=100)

        self.matrix_label = UILabel(text="Transformation Matrix:",
                                    relative_rect=pygame.Rect((50, 220), (200, 50)), manager=manager)
        self. top_left_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(300, 210, 50, 40),
                                                      initial_text=str(self.options.transformation_matrix[0][0]))
        self.top_right_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(355, 210, 50, 40),
                                                      initial_text=str(self.options.transformation_matrix[0][1]))
        self.bottom_left_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(300, 255, 50, 40),
                                                        initial_text=str(self.options.transformation_matrix[1][0]))
        self.bottom_right_matrix_input = UITextEntryLine(relative_rect=pygame.Rect(355, 255, 50, 40),
                                                         initial_text=str(self.options.transformation_matrix[1][1]))

        self.unit_length_lable = UILabel(text="Unit Length:", relative_rect=pygame.Rect((50, 350), (100, 40)),
                                         manager=manager)
        self.unit_length_input = UITextEntryLine(relative_rect=pygame.Rect(170, 350, 50, 40),
                                                 initial_text=str(self.options.unit_length))

        self.axis_label = UILabel(text="Axis:", relative_rect=pygame.Rect((50, 460), (100, 40)), manager=manager)
        self.eigenvector_label = UILabel(text="Eigenvectors:", relative_rect=pygame.Rect((50, 520), (110, 40)),
                                         manager=manager)
        self.grid_lines_label = UILabel(text="Grid Lines:", relative_rect=pygame.Rect((50, 580), (100, 40)), manager=manager)
        self.i_j_hat_label = UILabel(text="i-j hat:", relative_rect=pygame.Rect((50, 640), (100, 40)), manager=manager)
        self.determinant_label = UILabel(text="Determinant:", relative_rect=pygame.Rect((50, 700), (100, 40)),
                                         manager=manager)

        yes_no_options = ["yes", "no"]
        self.axis_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                            relative_rect=pygame.Rect(170, 460, 280, 40),
                                            manager=manager, expansion_height_limit=100)
        self.eigenvector_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                                   relative_rect=pygame.Rect(170, 520, 280, 40),
                                                   manager=manager, expansion_height_limit=100)
        self.grid_lines_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                                  relative_rect=pygame.Rect(170, 580, 280, 40),
                                                  manager=manager, expansion_height_limit=100)
        self.i_j_hat_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                               relative_rect=pygame.Rect(170, 640, 280, 40),
                                               manager=manager, expansion_height_limit=100)
        self.determinant_dropdown = UIDropDownMenu(options_list=yes_no_options, starting_option="yes",
                                                   relative_rect=pygame.Rect(170, 700, 280, 40),
                                                   manager=manager, expansion_height_limit=100)

    # updates self.options to the current selected options
    def update_options(self):
        tl = self.top_left_matrix_input.get_text()
        tr = self.top_right_matrix_input.get_text()
        bl = self.bottom_left_matrix_input.get_text()
        br = self.bottom_right_matrix_input.get_text()
        self.options.transformation_matrix = np.array([[float(tl) if not (tl == "" or tl == "-") else 1.0,
                                                       float(tr) if not (tr == "" or tr == "-") else 1.0],
                                                      [float(bl) if not (bl == "" or bl == "-") else 1.0,
                                                       float(br) if not (br == "" or br == "-") else 1.0]])

        self.options.unit_length = int(self.unit_length_input.get_text()) \
            if not (self.unit_length_input.get_text() == "" or int(self.unit_length_input.get_text()) < 10) else 10

        self.options.axis = True if self.axis_dropdown.selected_option == "yes" else False
        self.options.eigenvectors = True if self.eigenvector_dropdown.selected_option == "yes" else False
        self.options.grid_lines = True if self.grid_lines_dropdown.selected_option == "yes" else False
        self.options.i_j_hat = True if self.i_j_hat_dropdown.selected_option == "yes" else False
        self.options.determinant = True if self.determinant_dropdown.selected_option == "yes" else False
        self.options.image = self.image_dropdown.selected_option

    # updates options and returns the options
    def get_options(self):
        self.update_options()
        return self.options


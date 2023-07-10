import cv2
import numpy as np
import config
import re


def start():
    # instructions for submitting image
    print("Welcome to the Linear Transformation visualizer. To begin, please add your image files "
          "to the images folder, or use the provided image by typing \'ubc_logo.jpg\'.")

    # get image path from user
    while True:
        try:
            filepath = "images/" + input("Please enter the name of the image file: ")
            # validation
            img = cv2.imread(filepath)
            img_test = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except (cv2.error, FileNotFoundError, UnicodeError):
            print("The path you entered is not valid.")
        else:
            config.image_path = filepath
            break

    # gets matrix from user
    while True:
        matrix = input("Please enter a 2x2 transformation matrix. Enter numbers by column vectors from left to right, "
                       "seperated by commas. "
                       "For example, \n |1 2| \n |3 4| \n should be entered as: 1,3,2,4. ")
        if re.match(r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?$", matrix):
            tl, bl, tr, br = matrix.split(",")
            config.transformation_matrix = np.array([[float(tl), float(tr)], [float(bl), float(br)]])
            break
        else:
            print("Invalid input, please try again.")

    # set display
    text = "The display settings are currently:\nAxis: {ax}\nGrid lines: {gl}\nEigenvectors: {ev}"
    print(text.format(
          ax="On" if config.axis else "Off",
          gl="On" if config.grid_lines else "Off",
          ev="On" if config.eigenvectors else "Off"))
    print("Please enter your display settings or \"s\" to skip. 1 is on and 0 is off. Enter the three settings without "
          "spaces. For examples, on, on, off, will be 110.")
    while True:
        usr_input = input("New display setting: ")
        if usr_input == "s":
            break
        elif re.match("^[01][01][01]$", usr_input):
            config.axis = True if usr_input == "1" else False
            config.grid_lines = True if usr_input == "1" else False
            config.eigenvectors = True if usr_input == "1" else False
            break
        else:
            print("Invalid input, please try again.")





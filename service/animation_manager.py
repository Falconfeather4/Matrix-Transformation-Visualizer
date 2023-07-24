import numpy as np
from image import Image
from option_panel import Options
import copy


class AnimationManager:
    options = Options()

    # the image that serves as a basis for doing transformations
    base_img = Image(options.image)

    frame_num = 80
    frame_index = 0

    playing = False
    last_display_img = None

    options_changed = False
    image_changed = False
    first_image = True

    # compares new options to self.options and sets options_changed and image_changed flags. Then replaces self.options
    # with new options.
    def update_status(self, new_options):
        self.options_changed = not np.array_equal(self.options.transformation_matrix, new_options.transformation_matrix) \
            or self.options.unit_length != new_options.unit_length \
            or self.options.i_j_hat != new_options.i_j_hat \
            or self.options.axis != new_options.axis \
            or self.options.eigenvectors != new_options.eigenvectors \
            or self.options.determinant != new_options.determinant \
            or self.options.grid_lines != new_options.grid_lines

        self.image_changed = self.options.image != new_options.image

        self.options = copy.copy(new_options)
        self.options.transformation_matrix = np.copy(new_options.transformation_matrix)

    # resets frame index to 0 and starts playing
    def start_playing(self):
        self.playing = True
        self.frame_index = 0

    # returns an Image object depending on the current state of the application
    def get_picture(self, new_options):
        self.update_status(new_options)
        identity_matrix = np.array([[1, 0], [0, 1]])

        # if first image or image is changed, reset index, stop playing, and return the new image
        if self.image_changed or self.first_image:
            self.base_img = Image(new_options.image)
            self.playing = False
            self.first_image = False
            self.frame_index = 0
            img_copy = self.base_img.clone()
            img_copy.do_transformations(identity_matrix, self.options)
            if self.options.eigenvectors:
                rows, cols, layers = np.shape(img_copy.image_array)
                img_copy.draw_eigenvectors(rows, cols, self.options)
            self.last_display_img = img_copy
            return img_copy

        # if playing, return correct image based on current index. If teh animation is finished, (index >= frame num)
        # then stop playing.
        if self.playing:
            if self.frame_index == self.frame_num:
                self.playing = False
            else:
                img_copy = self.base_img.clone()
                transformation_matrix = identity_matrix + self.frame_index * self.calculate_step_matrix()
                img_copy.do_transformations(transformation_matrix, self.options)

                self.last_display_img = img_copy
                self.frame_index += 1

        # if any options are changed, redraw image with new options
        elif self.options_changed:
            img_copy = self.base_img.clone()

            if self.frame_index == 0:
                img_copy.do_transformations(identity_matrix, self.options)
                if self.options.eigenvectors:
                    rows, cols, layers = np.shape(img_copy.image_array)
                    img_copy.draw_eigenvectors(rows, cols, self.options)
            elif self.frame_index == self.frame_num:
                last_frame_index = self.frame_index - 1
                transformation_matrix = identity_matrix + last_frame_index * self.calculate_step_matrix()
                img_copy.do_transformations(transformation_matrix, self.options)
            else:
                transformation_matrix = identity_matrix + self.frame_index * self.calculate_step_matrix()
                img_copy.do_transformations(transformation_matrix, self.options)

            self.last_display_img = img_copy

        return self.last_display_img

    # When the animation is playing, each frame is individually drawn with a different matrix. The first frame with be
    # drawn with the identity matrix, and the last frame with the transformation_matrix. The step_matrix is this
    # "incrementing matrix" for each new frame
    def calculate_step_matrix(self):
        identity_matrix = np.array([[1, 0], [0, 1]])
        delta_matrix = self.options.transformation_matrix - identity_matrix
        return (1 / self.frame_num) * delta_matrix

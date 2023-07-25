from option_panel import OptionController
from animation_manager import AnimationManager
import cv2
import pygame
import pygame_gui


# initializing pygame
pygame.init()
pygame.display.set_caption('Linear Transformations')
window = pygame.display.set_mode((1100, 800))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1100, 800))

option_panel = OptionController(manager)
animation_manager = AnimationManager()

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 700), (100, 50)),
                                           text='Play', manager=manager)

# display animation
running = True
while running:
    window.fill(pygame.Color(128, 128, 128, 255))
    new_options = option_panel.get_options()
    time_delta = clock.tick(new_options.fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                animation_manager.start_playing()

        manager.process_events(event)

    img = animation_manager.get_picture(new_options)
    display_img = cv2.transpose(img.image_array)
    pygame_surface = pygame.surfarray.make_surface(display_img)

    x = 600
    y = 50
    window.blit(pygame_surface, (x, y))

    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.update()

pygame.quit()

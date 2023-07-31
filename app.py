from option_controller import OptionController
from animation_manager import AnimationManager
import cv2
import pygame
import pygame_gui


class App:
    running = True

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Linear Transformations')
        self.window = pygame.display.set_mode((1100, 800))
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1100, 800))

        self.option_panel = OptionController(self.manager)
        self.animation_manager = AnimationManager()

        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 700), (100, 50)),
                                                        text='Play', manager=self.manager)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.animation_manager.start_playing()

        self.manager.process_events(event)

    def on_loop(self):
        self.window.fill(pygame.Color(128, 128, 128, 255))
        new_options = self.option_panel.get_options()
        time_delta = self.clock.tick(new_options.fps) / 1000.0

        img = self.animation_manager.get_picture(new_options)
        display_img = cv2.transpose(img.image_array)
        pygame_surface = pygame.surfarray.make_surface(display_img)

        x = 600
        y = 50
        self.window.blit(pygame_surface, (x, y))

        self.manager.update(time_delta)
        self.manager.draw_ui(self.window)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

import pygame

from window import Window


class Description(Window):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        pygame.display.set_caption('Описание игры')

        self.rects = {
            'exit': pygame.Rect(30, 30, 107, 107),
            'bg': pygame.Rect(0, 0, 1920, 1080)
        }

        self.image_1 = pygame.image.load('../assets/images/description_ru.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('bg').width, self.rects.get('bg').height))

        self.image_2 = pygame.image.load('../assets/images/x_exit.png')
        pygame.transform.scale(self.image_2, (
            self.rects.get('exit').width, self.rects.get('exit').height))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rects.get('exit').collidepoint(event.pos):
                self.window_man.set_window('menu')
                self.window_man.run()

    def draw(self):
        self.screen.blit(self.image_1, self.rects.get('bg').topleft)
        self.screen.blit(self.image_2, self.rects.get('exit').topleft)

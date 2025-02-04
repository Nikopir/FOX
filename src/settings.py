import pygame

from window import Window


class Settings(Window):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        pygame.display.set_caption('Настройки')

        self.rects = {
            'line': pygame.Rect(725, 500, 450, 15),
            'circle': pygame.Rect(725, 491, 30, 30),
            'surf': pygame.Rect(0, 0, 1920, 1080),
            'exit': pygame.Rect(215, 125, 107, 107)
        }

        self.moving = False
        self.x = self.rects.get('circle').topleft[0]
        self.x_n = 0

        self.image_1 = pygame.image.load('../assets/images/line_pg1.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('line').width, self.rects.get('line').height))

        self.image_2 = pygame.image.load('../assets/images/circle_pg.png')
        pygame.transform.scale(self.image_2, (
            self.rects.get('circle').width, self.rects.get('circle').height))

        self.image_3 = pygame.image.load('../assets/images/bg.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('surf').width, self.rects.get('surf').height))

        self.image_4 = pygame.image.load('../assets/images/x_exit.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('exit').width, self.rects.get('exit').height))

        self.font = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 42)
        self.font_1 = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 120)

        self.text_music = self.font.render('Музыка', True,
                                           pygame.Color('white'))
        self.text_settings = self.font_1.render('Настройки', True,
                                                pygame.Color(
                                                    'white'))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rects.get('circle').collidepoint(event.pos):
                self.moving = True
            if self.rects.get('exit').collidepoint(event.pos):
                self.window_man.set_window('menu')
                self.window_man.run()
        if event.type == pygame.MOUSEMOTION:
            if self.moving:
                self.x_n = event.rel[0]
                if 710 <= self.x + self.x_n <= 1160:
                    self.x = self.x + self.x_n
                    self.rects['circle'] = pygame.Rect(self.x, 491, 30, 30)
        if event.type == pygame.MOUSEBUTTONUP:
            self.moving = False

    def draw(self):
        self.screen.blit(self.image_3, self.rects.get('surf').topleft)
        self.screen.blit(self.image_1, self.rects.get('line').topleft)
        self.screen.blit(self.image_2, self.rects.get('circle').topleft)
        self.screen.blit(self.image_4, self.rects.get('exit').topleft)
        self.screen.blit(self.text_music, (880, 400))
        self.screen.blit(self.text_settings, (643, 170))

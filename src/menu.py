import pygame
import os
import sys
from design import Design
from window import Window
from game import PlayGame


class StandaloneMenu(Window):
    def __init__(self, screen, manager, db_manager):
        super().__init__(screen, manager)
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.db_manager = db_manager
        pygame.display.set_caption("Standalone Menu")
        self.design = Design()
        self.buttons = {
            'Play': self.design.play_button,
            'Settings': self.design.side_buttons['SETTINGS']['rect'],
            'Book': self.design.side_buttons['BOOK']['rect'],
            'Game Description': self.design.side_buttons['GAME DESCRIPTION']['rect']
        }

        self.all_sprites = pygame.sprite.Group()
        self.dragon = AnimatedSprite(self.load_image("fox_animation.png"), 3,
                                     1,
                                     1200,
                                     750, self.all_sprites)

    def draw(self):
        self.design.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    self.perform_action(action)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.show_exit_dialog(self.screen)

    def perform_action(self, action):
        if action == 'Play':
            self.window_man.add_window('play', PlayGame(self.screen, self.window_man, self.db_manager))
            self.window_man.set_window('play')
            self.window_man.run()
        elif action == 'Settings':
            self.window_man.set_window('settings')
            self.window_man.run()
        elif action == 'Book':
            self.window_man.set_window('book')
            self.window_man.run()
        elif action == 'Game Description':
            self.window_man.set_window('description')
            self.window_man.run()

    def load_image(self, name, colorkey=-1):
        fullname = os.path.join('../assets/images/', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.handle_events(event)
            self.draw()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, grp):
        super().__init__(grp)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

import pygame
import os


class Design:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "../assets/images")
        self.bg_image = pygame.image.load(os.path.join(data_path, "background.png"))
        self.fox_image = pygame.image.load(os.path.join(data_path, "fox.png"))
        self.text_bg = pygame.image.load(os.path.join(data_path, "bg_fox_text.png"))
        self.play_button_img = pygame.image.load(os.path.join(data_path, "btn_play.png"))
        self.settings_button_img = pygame.image.load(os.path.join(data_path, "btn_settings.png"))
        self.book_button_img = pygame.image.load(os.path.join(data_path, "btn_book.png"))
        self.creators_button_img = pygame.image.load(os.path.join(data_path, "btn_creators.png"))
        self.fox_rect = pygame.Rect(50, 50, 281, 283)
        self.text_rect = pygame.Rect(480, 216, 100, 500)
        self.play_button = pygame.Rect(598, 816, 750, 235)
        self.side_buttons = {
            "SETTINGS": {"rect": pygame.Rect(1510, 248, 400, 113), "image": self.settings_button_img},
            "BOOK": {"rect": pygame.Rect(1510, 375, 400, 113), "image": self.book_button_img},
            "GAME DESCRIPTION": {"rect": pygame.Rect(1510, 500, 400, 113), "image": self.creators_button_img}
        }
        self.font = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 384)
        self.text_1 = self.font.render('FOX', True, pygame.Color('white'))
        self.font_min = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 64)
        self.font_min_mm = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 128)
        self.font_min_m = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 36)
        self.text_2 = self.font_min.render('Settings', True, pygame.Color('white'))
        self.text_3 = self.font_min.render('BOOK', True, pygame.Color('white'))
        self.text_4 = self.font_min_m.render('GAME DESCRIPTION', True, pygame.Color('white'))
        self.text_5 = self.font_min_mm.render('Play', True, pygame.Color('white'))

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.fox_image, self.fox_rect.topleft)
        screen.blit(self.text_bg, self.text_rect.topleft)
        screen.blit(self.play_button_img, self.play_button.topleft)
        for button in self.side_buttons.values():
            screen.blit(button["image"], button["rect"].topleft)
        screen.blit(self.text_1, pygame.Rect(625, 300, 100, 500))
        screen.blit(self.text_2, pygame.Rect(1600, 275, 400, 113))
        screen.blit(self.text_3, pygame.Rect(1600, 400, 400, 113))
        screen.blit(self.text_4, pygame.Rect(1550, 540, 400, 113))
        screen.blit(self.text_5, pygame.Rect(825, 870, 400, 113))

import pygame


class Window:
    def __init__(self, screen, manager):
        self.screen = screen
        self.window_man = manager
        self.clock = None
        self.running = True

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                self.handle_events(event)

            self.update()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    @staticmethod
    def show_exit_dialog(screen):
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 50)

        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        screen.blit(surface, (0, 0))

        dialog_rect = pygame.Rect(screen.get_width() // 2 - 200, screen.get_height() // 2 - 100, 400, 200)
        pygame.draw.rect(screen, (50, 50, 50), dialog_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3, border_radius=10)

        text = font.render("Выйти?", True, (255, 255, 255))
        screen.blit(text, (dialog_rect.x + dialog_rect.width // 2 - text.get_width() // 2, dialog_rect.y + 20))

        button_ok = pygame.Rect(dialog_rect.x + 40, dialog_rect.y + 120, 130, 50)
        button_cancel = pygame.Rect(dialog_rect.x + 230, dialog_rect.y + 120, 130, 50)

        selected = 0

        def draw_buttons():
            screen.fill((0, 0, 0, 150), dialog_rect)
            pygame.draw.rect(screen, (50, 50, 50), dialog_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3, border_radius=10)
            screen.blit(text, (dialog_rect.x + dialog_rect.width // 2 - text.get_width() // 2, dialog_rect.y + 20))

            color_ok = (150, 150, 150) if selected == 0 else (100, 100, 100)
            color_cancel = (150, 150, 150) if selected == 1 else (100, 100, 100)

            pygame.draw.rect(screen, color_ok, button_ok, border_radius=5)
            pygame.draw.rect(screen, color_cancel, button_cancel, border_radius=5)

            text_ok = small_font.render("ОК", True, (255, 255, 255))
            text_cancel = small_font.render("Отмена", True, (255, 255, 255))

            screen.blit(text_ok, (button_ok.x + button_ok.width // 2 - text_ok.get_width() // 2,
                                  button_ok.y + button_ok.height // 2 - text_ok.get_height() // 2))
            screen.blit(text_cancel, (button_cancel.x + button_cancel.width // 2 - text_cancel.get_width() // 2,
                                      button_cancel.y + button_cancel.height // 2 - text_cancel.get_height() // 2))

            pygame.display.flip()

        draw_buttons()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_TAB, pygame.K_LEFT, pygame.K_RIGHT):
                        selected = 1 - selected
                        draw_buttons()
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            pygame.quit()
                            exit()
                        else:
                            waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_ok.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    if button_cancel.collidepoint(event.pos):
                        waiting = False

import pygame
from database_manager import DatabaseManager

from window import Window


class LoginError(Exception):
    pass


class PasswordError(Exception):
    pass


class Registration(Window):
    def __init__(self, screen, manager, db_manager):
        super().__init__(screen, manager)
        pygame.display.set_caption('Регистрация')
        self.db_manager = db_manager

        self.flag_input_login = False
        self.flag_input_passw = False
        self.status_in_or_up = False
        self.status_passw = True

        self.validator = '\
        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.password = ''
        self.login = ''

        self.login_x1, self.login_x2 = 500, 500
        self.passw_x1, self.passw_x2 = 500, 500

        self.rects = {'surf': pygame.Rect(0, 0, 1920, 1080),
                      'fox': pygame.Rect(240, 140, 256, 285),
                      'text_surf_login': pygame.Rect(480, 420, 312, 67),
                      'text_surf_passw': pygame.Rect(480, 620, 312, 67),
                      'text_input_login': pygame.Rect(480, 520, 993, 66),
                      'text_input_passw': pygame.Rect(480, 720, 993, 66),
                      'button_next': pygame.Rect(715, 805, 500, 150),
                      'type_sign_in': pygame.Rect(1030, 135, 312, 67),
                      'type_sign_up': pygame.Rect(1380, 135, 312, 67),
                      'show_passw': pygame.Rect(830, 620, 312, 67)
                      }

        self.image_1 = pygame.image.load('../assets/images/window_login.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('surf').width, self.rects.get('surf').height))

        self.image_2 = pygame.image.load('../assets/images/fox.png')
        pygame.transform.scale(self.image_1, (
            self.rects.get('surf').width, self.rects.get('surf').height))

        self.image_3 = pygame.image.load('../assets/images/surf_for_text.png')
        pygame.transform.scale(self.image_3, (
            self.rects.get('text_surf_login').width,
            self.rects.get('text_surf_login').height))

        self.image_4 = pygame.image.load('../assets/images/surf_for_text.png')
        pygame.transform.scale(self.image_4, (
            self.rects.get('text_surf_passw').width,
            self.rects.get('text_surf_passw').height))

        self.image_5 = pygame.image.load('../assets/images/input.png')
        pygame.transform.scale(self.image_5, (
            self.rects.get('text_input_login').width,
            self.rects.get('text_input_login').height))

        self.image_6 = pygame.image.load('../assets/images/input.png')
        pygame.transform.scale(self.image_6, (
            self.rects.get('text_input_passw').width,
            self.rects.get('text_input_passw').height))

        self.image_7 = pygame.image.load('../assets/images/button.png')
        pygame.transform.scale(self.image_7, (
            self.rects.get('button_next').width,
            self.rects.get('button_next').height))

        self.image_8 = pygame.image.load('../assets/images/surf_for_text.png')
        pygame.transform.scale(self.image_8, (
            self.rects.get('type_sign_in').width,
            self.rects.get('type_sign_in').height))

        self.image_9 = pygame.image.load('../assets/images/surf_for_text.png')
        pygame.transform.scale(self.image_9, (
            self.rects.get('type_sign_up').width,
            self.rects.get('type_sign_up').height))

        self.image_10 = pygame.image.load('../assets/images/surf_for_text.png')
        pygame.transform.scale(self.image_10, (
            self.rects.get('show_passw').width,
            self.rects.get('show_passw').height))

        self.font = pygame.font.Font('../assets/font/HomeVideo-Regular.otf', 36)
        self.font_button = pygame.font.Font('../assets/font/HomeVideo-Regular.otf',
                                            70)

        self.text_surface_login = self.font.render('Логин', True,
                                                   pygame.Color('white'))
        self.text_surface_passw = self.font.render('Пароль', True,
                                                   pygame.Color('white'))
        self.text_surface_next = self.font_button.render('Вход', True,
                                                         pygame.Color('white'))
        self.text_type_in = self.font.render('Вход', True,
                                             pygame.Color('white'))
        self.text_type_up = self.font.render('Регистрация',
                                             True,
                                             pygame.Color('white'))
        self.text_login = self.font.render('', True,
                                           pygame.Color('white'))
        self.text_passw = self.font.render('', True,
                                           pygame.Color('white'))
        self.text_show_passw = self.font.render('Показать', True,
                                                pygame.Color('white'))
        self.text_error = self.font.render('', True,
                                           pygame.Color('red'))

        self.text_position_login = (575, 435)
        self.text_position_passw = (570, 635)
        self.text_position_next = (885, 850)
        self.text_type_in_position = (1145, 150)
        self.text_type_up_position = (1417, 150)
        self.text_login_inp = (506, 534)
        self.text_passw_inp = (500, 729)
        self.text_show = (895, 635)
        self.text_error_pos = (0, 0)

    def handle_events(self, event):
        PADDING_LEFT = 15
        CURSOR_OFFSET = 13

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rects.get('button_next').collidepoint(event.pos):
                try:
                    if self.login.strip() == '' or not self.validator_check(self.login):
                        raise LoginError

                    if self.password.strip() == '' or len(self.password) < 5:
                        raise PasswordError

                    if self.status_in_or_up:
                        success = self.db_manager.add_user(self.login, self.password)
                        if not success:
                            raise LoginError

                        self.text_error = self.font.render("Регистрация успешна!", True, pygame.Color('green'))
                    else:
                        if not self.db_manager.check_password(self.login, self.password):
                            raise PasswordError("Неверный логин или пароль!")
                        self.text_error = self.font.render("Вход выполнен!", True, pygame.Color('green'))
                        self.window_man.set_window('menu')
                        self.window_man.run()

                except LoginError:
                    self.text_error = self.font.render(
                        'Логин уже занят или содержит недопустимые символы!',
                        True, pygame.Color('red')
                    )
                    self.text_error_pos = (485, 370)

                except PasswordError:
                    self.text_error = self.font.render(
                        'Неверный логин или пароль!',
                        True, pygame.Color('red')
                    )
                    self.text_error_pos = (485, 370)

            if self.rects.get('text_input_login').collidepoint(event.pos):
                self.flag_input_login = True
                self.flag_input_passw = False
            else:
                self.flag_input_login = False

            if self.rects.get('text_input_passw').collidepoint(event.pos):
                self.flag_input_passw = True
                self.flag_input_login = False
            else:
                self.flag_input_passw = False

            if self.rects.get('type_sign_in').collidepoint(event.pos):
                self.text_surface_next = self.font_button.render('Вход', True, pygame.Color('white'))
                self.text_position_next = (885, 850)
                self.status_in_or_up = False

            if self.rects.get('type_sign_up').collidepoint(event.pos):
                self.text_surface_next = self.font_button.render('Регистрация', True, pygame.Color('white'))
                self.text_position_next = (735, 850)
                self.status_in_or_up = True

            if self.rects.get('show_passw').collidepoint(event.pos):
                self.status_passw = not self.status_passw

        if event.type == pygame.KEYDOWN:
            if self.flag_input_login:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.login) > 0:
                        self.login = self.login[:-1]
                elif len(self.login) < 40:
                    self.login += event.unicode

                self.text_login = self.font.render(self.login, True, pygame.Color('white'))


                text_width, _ = self.font.size(self.login)
                self.login_x1 = self.rects['text_input_login'].x + PADDING_LEFT + text_width + CURSOR_OFFSET
                self.login_x2 = self.login_x1

            if self.flag_input_passw:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.password) > 0:
                        self.password = self.password[:-1]
                elif len(self.password) < 40:
                    self.password += event.unicode

                masked_password = '*' * len(self.password)
                self.text_passw = self.font.render(masked_password, True, pygame.Color('white'))

                text_width, _ = self.font.size(masked_password)
                self.passw_x1 = self.rects['text_input_passw'].x + PADDING_LEFT + text_width + CURSOR_OFFSET
                self.passw_x2 = self.passw_x1

            if event.key == pygame.K_ESCAPE:
                self.show_exit_dialog(self.screen)

    def draw(self):
        self.screen.blit(self.image_1, self.rects.get('surf').topleft)
        self.screen.blit(self.image_2, self.rects.get('fox').topleft)
        self.screen.blit(self.image_3,
                         self.rects.get('text_surf_login').topleft)
        self.screen.blit(self.image_4,
                         self.rects.get('text_surf_passw').topleft)
        self.screen.blit(self.image_5,
                         self.rects.get('text_input_login').topleft)
        self.screen.blit(self.image_6,
                         self.rects.get('text_input_passw').topleft)
        self.screen.blit(self.image_7,
                         self.rects.get('button_next').topleft)
        self.screen.blit(self.image_8,
                         self.rects.get('type_sign_in').topleft)
        self.screen.blit(self.image_9,
                         self.rects.get('type_sign_up').topleft)
        self.screen.blit(self.image_10,
                         self.rects.get('show_passw').topleft)

        self.screen.blit(self.text_surface_login, self.text_position_login)
        self.screen.blit(self.text_surface_passw, self.text_position_passw)
        self.screen.blit(self.text_surface_next, self.text_position_next)
        self.screen.blit(self.text_type_in, self.text_type_in_position)
        self.screen.blit(self.text_type_up, self.text_type_up_position)
        self.screen.blit(self.text_login, self.text_login_inp)
        self.screen.blit(self.text_passw, self.text_passw_inp)
        self.screen.blit(self.text_show_passw, self.text_show)
        self.screen.blit(self.text_error, self.text_error_pos)

        if self.flag_input_login:
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (self.login_x1, 529),
                             (self.login_x2, 575), 5)
        if self.flag_input_passw:
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (self.passw_x1, 729),
                             (self.passw_x2, 775), 5)

        if self.status_passw:
            self.text_show_passw = self.font.render('Показать', True,
                                                    pygame.Color('white'))
            self.text_show = (895, 635)
            self.text_passw = self.font.render('*' * len(self.password),
                                               True,
                                               pygame.Color('white'))
        if not self.status_passw:
            self.text_show_passw = self.font.render('Скрыть', True,
                                                    pygame.Color('white'))
            self.text_show = (920, 635)
            self.text_passw = self.font.render(self.password, True,
                                               pygame.Color('white'))

    def validator_check(self, login):
        """ Проверяет, содержит ли логин только латинские буквы и цифры, и имеет ли корректную длину """
        if not (4 <= len(login) <= 15):
            return False
        return all(c.isalnum() and c.isascii() for c in login)
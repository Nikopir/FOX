import pygame

from registration import Registration
from settings import Settings
from window_manager import WindowManager
from menu import StandaloneMenu
from book import BookScreen
from game import PlayGame
from description import Description
from database_manager import DatabaseManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    manager = WindowManager(screen)
    db_manager = DatabaseManager()
    manager.add_window('registration', Registration(screen, manager, db_manager))
    manager.add_window('menu', StandaloneMenu(screen, manager, db_manager))
    manager.add_window('settings', Settings(screen, manager))
    manager.add_window('book', BookScreen(screen, manager))
    manager.add_window('description', Description(screen, manager))
    manager.add_window('play', PlayGame(screen, manager, db_manager))
    manager.set_window('registration')
    manager.run()


if __name__ == "__main__":
    main()

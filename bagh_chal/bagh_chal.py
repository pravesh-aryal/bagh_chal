import sys, pygame
from pygame import Rect
from board import Board
from settings import Settings
import game_mechanics as gm
from circle import Circle


def start_game():
    pygame.init()

    # Create an instance of the class Settings
    game_settings = Settings()

    window = pygame.display.set_mode(
        (game_settings.WINDOW_WIDTH, game_settings.WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Bagh-Chal")
    # create window rect to access its attribute
    window_rect = window.get_rect()
    window.fill(game_settings.WINDOW_BG_COLOR)

    # Create an instance of the class Board
    board = Board(game_settings, window_rect)
    coordinates = board.generate_coordinates(game_settings)
    gm.initialize_board(window, game_settings, board, coordinates)
    # Create an instance of the class Circle
    circle = Circle(window, game_settings, coordinates)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
        pygame.display.flip()


start_game()

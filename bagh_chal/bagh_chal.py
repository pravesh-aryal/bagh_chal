# this file will be main.py
import sys, pygame
from pygame import Rect
from board import Board
from settings import Settings
import game_mechanics as gm
from circle import Circle
from tiger import Tiger

goat_group = pygame.sprite.Group()


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

    # Create an instance of the class Tiger
    tiger1 = Tiger(*board.rect.topleft)
    tiger2 = Tiger(*board.rect.topright)
    tiger3 = Tiger(*board.rect.bottomright)
    tiger4 = Tiger(*board.rect.bottomleft)
    tiger_group = pygame.sprite.Group()
    tiger_group.add(tiger1, tiger2, tiger3, tiger4)
    circles = gm.generate_circles(
        window, game_settings, coordinates, tiger_group, goat_group
    )
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # On left-click
                if event.button == 1:
                    # print("left")
                    board.handle_click(
                        mx, my, circles, window, game_settings, goat_group
                    )
                    for circle in circles:
                        print(circle.occupying_piece)
                # handling click

        tiger_group.draw(window)
        pygame.display.flip()


start_game()

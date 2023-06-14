# this file will be main.py
import sys, pygame
from pygame import Rect
from board import Board
from settings import Settings
import game_mechanics as gm


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
    board = Board(window, game_settings, window_rect, gm)

    #
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # On left-click
                if event.button == 1:
                    board.handle_click(
                        mx,
                        my,
                        window,
                    )
                    print(board.turn)

                if len(board.trapped_tigers) == 4:
                    print("goat wins")
                    pygame.quit()
                if board.goats_killed == 8:
                    print(len(board.trapped_tigers), board.goats_killed)
                    print("tiger wins")
                    pygame.quit()

        pygame.display.flip()


start_game()

import sys, pygame
from pygame import Rect
from board import Board
from settings import Settings
import game_mechanics as gm
from circle import Circle
from tiger import Tiger


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
    circles = gm.generate_circles(window, game_settings, coordinates)
    circle2 = circles[1]
    circle2.color = (255, 0, 0)
    print(circle2.color)
    pygame.display.flip()

    # Create an instance of the class Circle
    # circle = Circle(window, game_settings, coordinates)

    # Create an instance of the class Tiger
    tiger1 = Tiger(*board.rect.topleft)
    tiger2 = Tiger(*board.rect.topright)
    tiger3 = Tiger(*board.rect.bottomright)
    tiger4 = Tiger(*board.rect.bottomleft)
    tiger_group = pygame.sprite.Group()
    tiger_group.add(tiger1, tiger2, tiger3, tiger4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # print(pygame.mouse.get_pos())
                if tiger1.rect.collidepoint(pygame.mouse.get_pos()):
                    print("the tiger is clicked")
                    tiger1.is_selected = True
                    if tiger1.is_selected:
                        if event.type == pygame.MOUSEBUTTONUP:
                            tiger1.rect.center = pygame.mouse.get_pos()
                elif circle2.rect.collidepoint(pygame.mouse.get_pos()):
                    print("the circle is clicked")
                    circle2.clicked = True
                    circle2.color = (0, 255, 0)

                # gm.generate_circles(window, game_settings, coordinates)
                # circle2.clicked = True
                # if circle2.clicked:
        tiger_group.draw(window)
        for circle in circles:
            circle.draw(window)
        tiger1.rect.center = pygame.mouse.get_pos()
        pygame.display.flip()


start_game()

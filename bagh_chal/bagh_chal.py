import sys, pygame
from pygame import Rect
from board import Board
from settings import Settings

# The call to pygame.init() initializes each of these modules.
pygame.init()

# Create an instance of the class Settings
game_settings = Settings()

window = pygame.display.set_mode(
    (game_settings.WINDOW_WIDTH, game_settings.WINDOW_HEIGHT)
)
pygame.display.set_caption("Bagh-Chal")
# create window rect to access its attribute
window_rect = window.get_rect()

# Create an instance of the class Board
board = Board(game_settings, window_rect)
window.fill(game_settings.WINDOW_BG_COLOR)
CFL, CFLF = board.generate_points(game_settings)
# print(CFLF)
# for each in CFLF:
#     print(each)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw the main rectangle for the game board.

    pygame.draw.rect(window, game_settings.BOARD_COLOR, board.rect)
    # pygame.draw.line(window, game_settings.LINE_COLOR, (0, 0), (100, 100), 10)
    for each_CFL in CFL:
        pygame.draw.line(window, game_settings.LINE_COLOR, each_CFL[0], each_CFL[1], 3)
    # for each_CFLF in CFLF:
    #     print("this issfdsadfsf \n \n \n", each_CFLF)
    #     pygame.draw.lines(window, game_settings.LINE_COLOR, each_CFLF, 3)
    for each_CFLF in CFLF:
        pygame.draw.line(
            window,
            game_settings.LINE_COLOR,
            each_CFLF[0],
            each_CFLF[len(each_CFLF) - 1],
            3,
        )

    pygame.display.flip()

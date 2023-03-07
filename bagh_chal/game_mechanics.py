import sys
import pygame

# from board import Board


def check_events():
    pass


def initialize_board(window, game_settings, board, coordinates) -> None:
    # Draw the main rectangle for the game board.
    pygame.draw.rect(window, game_settings.BOARD_COLOR, board.rect)
    vertical_coordinates, horizontal_coordinates = board.points_for_lines(coordinates)
    for vertical_coordinate in vertical_coordinates:
        pygame.draw.line(
            window,
            game_settings.LINE_COLOR,
            vertical_coordinate[0],
            vertical_coordinate[1],
            2,
        )

    for horizontal_coordinate in horizontal_coordinates:
        pygame.draw.line(
            window,
            game_settings.LINE_COLOR,
            horizontal_coordinate[0],
            horizontal_coordinate[len(horizontal_coordinate) - 1],
            2,
        )
    # pygame.draw.line(window, game_settings.LINE_COLOR, (0, 0), (800, 800), 3)
    # pygame.draw.line(window, game_settings.LINE_COLOR, (0, 800), (800, 0), 3)
    create_diagnols(window, game_settings, coordinates, board.rect)


def update_board():
    pass


def create_diagnols(window, game_settings, coordinates, board_rect):
    # board_top_left_point = board_rect.topleft
    # board_top_right_point = board_rect.topright
    # board_bottom_left_point = board_rect.bottomleft
    # board_bottom_right_point = board_rect.bottomright
    pygame.draw.line(
        window,
        game_settings.LINE_COLOR,
        board_rect.topleft,
        board_rect.bottomright,
        3,
    )
    pygame.draw.line(
        window,
        game_settings.LINE_COLOR,
        board_rect.bottomleft,
        board_rect.topright,
        3,
    )
    pygame.draw.polygon(
        window,
        game_settings.LINE_COLOR,
        (
            board_rect.midtop,
            board_rect.midright,
            board_rect.midbottom,
            board_rect.midleft,
        ),
        3,
    )

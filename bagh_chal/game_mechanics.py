import sys
import pygame
from circle import Circle
from itertools import chain
from position import Position

# from typing import Dict

# from board import Board
# This has some "complex" implementation to abstract from the important code


def check_events():
    pass


def initialize_board(window, game_settings, board, coordinates) -> None:
    # Draw the main rectangle for the game board.
    pygame.draw.rect(window, game_settings.BOARD_COLOR, board.rect)
    vertical_coordinates, horizontal_coordinates = points_for_lines(coordinates)
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

    create_diagnols(window, game_settings, coordinates, board.rect)


def points_for_lines(coordinates) -> tuple:
    vertical_coordinates, horizontal_coordinates = [], []
    index = 0
    for each_row in coordinates:
        vertical_coordinates.append((each_row[0], each_row[len(each_row) - 1]))
    for i in range(0, 5):
        _ = []
        for each_row in coordinates:
            _.append(each_row[index])

        horizontal_coordinates.append(_)
        index += 1

    return vertical_coordinates, horizontal_coordinates


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


def generate_circles(
    window,
    game_settings,
    coordinates,
    tiger_group,
    goat_group,
) -> list:
    circles = []

    for row_coordinates, pos_x in zip(coordinates, range(5)):
        for each_coordinate, pos_y in zip(row_coordinates, range(5)):
            # each_coordinate = center_of_each_cricle
            circles.append(
                Circle(
                    window,
                    game_settings,
                    each_coordinate,
                    tiger_group,
                    goat_group,
                    pos_x,
                    pos_y,
                )
            )
    return circles


def generate_coordinates(board, game_settings) -> list:
    # Coordinate of top left corner of the board in (x, y)
    starting_point = (board.rect.left, board.rect.top)
    length = game_settings.BOARD_WIDTH

    coordinates = []
    JUMP_VALUE = int(length / 4)
    x, y = starting_point
    # Creating 5 * 5 matrix
    for i in range(0, 5):
        row = []
        for j in range(0, 5):
            row.append((x, y))
            y += JUMP_VALUE

        coordinates.append(row)
        x += JUMP_VALUE
        y = starting_point[1]

    return coordinates


def board_config(coordinates, circles):
    # create Position object for each position
    config = []
    for x, circle in zip(range(5), circles):
        _ = []
        for y in range(5):
            _.append(
                Position(
                    x,
                    y,
                    *coordinates[x][y],
                    circle,
                )
            )

        config.append(_)

    return config


def initialize_tigers(board, Tiger, board_config):
    # new
    for row in board_config:
        for position in row:
            if position.abs_position in [
                board.rect.topleft,
                board.rect.topright,
                board.rect.bottomleft,
                board.rect.bottomright,
            ]:
                position.piece = Tiger(
                    *position.abs_position,
                    *position.position,
                )


def classify_coordinates(board_config):
    # new
    restricted_positions = []
    unrestricted_positions = []

    for row in board_config:
        for position in row:
            # position is an obj
            x, y = position.coordinate
            if (x + y) % 2 == 0:
                unrestricted_positions.append(position)
            else:
                restricted_positions.append(position)

    # now defining neighbours for each of the two positions
    for restricted_position in restricted_positions:
        valid_neighbours = []
        base_x, base_y = restricted_position.position
        for position in chain(*board_config):
            if position.position in [
                (base_x + 1, base_y),
                (base_x, base_y + 1),
                (base_x - 1, base_y),
                (base_x, base_y - 1),
            ]:
                valid_neighbours.append(position)

        restricted_position.valid_neighbours = valid_neighbours

    for unrestricted_position in unrestricted_positions:
        valid_neighbours = []
        base_x, base_y = unrestricted_position.position

        for position in chain(*board_config):
            if position.position in [
                (base_x + 1, base_y),
                (base_x, base_y + 1),
                (base_x - 1, base_y),
                (base_x, base_y - 1),
                (base_x + 1, base_y + 1),
                (base_x + 1, base_y - 1),
                (base_x - 1, base_y + 1),
                (base_x - 1, base_y - 1),
            ]:
                valid_neighbours.append(position)

        unrestricted_position.valid_neighbours = valid_neighbours

    return restricted_positions, unrestricted_positions

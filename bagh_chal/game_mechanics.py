import sys
import pygame
from circle import Circle
from collections import OrderedDict

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
) -> None:
    circles = []

    for row_coordinates, x in zip(coordinates, range(5)):
        for each_coordinate, y in zip(row_coordinates, range(5)):
            # each_coordinate = center_of_each_cricle
            circles.append(
                Circle(
                    window,
                    game_settings,
                    each_coordinate,
                    tiger_group,
                    goat_group,
                    x,
                    y,
                )
            )

    return circles


def remove():
    pass


# def update_circles(circles):
#     for circle in circles:


def create_tigers():
    pass


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
    config = []
    for x, circle in zip(range(5), circles):
        _ = []
        for y in range(5):
            _.append(
                {
                    "position": (x, y),
                    "abs_position": coordinates[x][y],
                    "circle": circle,
                    "piece": None,
                }
            )
        config.append(_)

    return config


def initialize_tigers(board, Tiger, board_config):
    for row in board_config:
        for position in row:
            if (
                position.__getitem__("abs_position") == board.rect.topleft
                or position.__getitem__("abs_position") == board.rect.topright
                or position.__getitem__("abs_position") == board.rect.bottomright
                or position.__getitem__("abs_position") == board.rect.bottomleft
            ):
                position["piece"] = Tiger(
                    *position.__getitem__("abs_position"),
                    *(position.__getitem__("position")),
                )


def classify_coordinates(board_config):
    restricted_coordinates = []
    non_restricted_coordinates = []

    for row in board_config:
        for coordinate in row:
            # coordinate is a dict
            x, y = coordinate["position"]
            # if x and y both are even or both are odd, it is a non_restricted coordinate
            # sum of two even numbers or odd numbers is always even
            if (x + y) % 2 == 0:
                non_restricted_coordinates.append(coordinate)
            else:
                restricted_coordinates.append(coordinate)

    # now defining neighbours for each restricted or non restricted coordinate/position
    print(restricted_coordinates)
    for coordinate in restricted_coordinates:
        valid_neighbours = []
        base_x, base_y = coordinate["position"]
        for coordinate in board_config:
            if (
                coordinate["position"] == (base_x + 1, base_y)
                or coordinate["position"] == (base_x, base_y + 1)
                or coordinate["position"] == (base_x - 1, base_y)
                or coordinate["position"] == (base_x, base_y - 1)
            ):
                valid_neighbours.append(coordinate)
        coordinate["valid_neighbours"] = valid_neighbours

    print("these are", restricted_coordinates)

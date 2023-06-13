"""This file includes implementation for creating board and generating required values"""
import sys
import pygame
from circle import Circle
from itertools import chain
from settings import Settings

game_settings = Settings()


def initialize_board(window, board, coordinates) -> None:
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

    create_diagnols(window, board.rect)


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


def create_diagnols(window, board_rect):
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
    coordinates,
    tiger_group,
    goat_group,
) -> list[list]:
    circles = []

    for row_coordinates, pos_y in zip(coordinates, range(5)):
        circle_row = []
        for coordinate, pos_x in zip(row_coordinates, range(5)):
            circle_row.append(
                Circle(
                    window,
                    game_settings,
                    coordinate,
                    pos_x,
                    pos_y,
                )
            )
        circles.append(circle_row)

    return circles


def generate_coordinates(board) -> list[list]:
    # Coordinate of top left corner of the board in (x, y) (0,0)
    x, y = (board.rect.left, board.rect.top)
    length = game_settings.BOARD_WIDTH

    coordinates = []
    JUMP_VALUE = int(length / 4)
    # Creating 5 * 5 matrix
    for i in range(0, 5):
        row = []
        for j in range(0, 5):
            row.append((x, y))
            x += JUMP_VALUE

        coordinates.append(row)
        x = 0  # reinitializing value of x to 0 since x for each row should be same
        y += JUMP_VALUE

    return coordinates


def initialize_tigers(board, Tiger, board_config):
    for row in board_config:
        for position in row:
            # each position is a cirlce obj
            if position.abs_pos in [
                board.rect.topleft,
                board.rect.topright,
                board.rect.bottomleft,
                board.rect.bottomright,
            ]:
                position.occupying_piece = Tiger(
                    *position.pos,
                    *position.abs_pos,
                )


def classify_coordinates(board_config):
    # new
    restricted_positions = []
    unrestricted_positions = []

    for row in board_config:
        for circle in row:
            x, y = circle.pos
            if (x + y) % 2 == 0:
                unrestricted_positions.append(circle)
            else:
                restricted_positions.append(circle)

    get_neighbour_pos(restricted_positions, unrestricted_positions, board_config)
    return restricted_positions, unrestricted_positions


def get_neighbour_pos(restricted_positions, unrestricted_positions, board_config):
    for restricted_position in restricted_positions:
        valid_neighbours = []
        base_x, base_y = restricted_position.pos
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


def get_valid_neighbours(circle, board_config):
    for each_cirlce in chain(*board_config):
        base_x, base_y = each_cirlce.pos_x, each_cirlce.pos_y
        if circle.is_restricted:
            if circle.pos in [
                (base_x + 1, base_y),
                (base_x, base_y + 1),
                (base_x - 1, base_y),
                (base_x, base_y - 1),
            ]:
                pass
        elif not circle.is_restricted:
            pass

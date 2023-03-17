import pygame
import os
from circle import Circle

"""Class to handle board coordinates and design"""


class Board:
    def __init__(self, game_settings, window_rect) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            game_settings.BOARD_WIDTH,
            game_settings.BOARD_HEIGHT,
        )

        # Place the Board at the center (as same as the window)
        self.rect.center = window_rect.center

    def generate_coordinates(self, game_settings) -> list:
        # Coordinate of top left corner of the board in (x, y)
        starting_point = (self.rect.left, self.rect.top)
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

    def points_for_lines(self, coordinates) -> tuple:

        vertical_coordinates = []
        horizontal_coordinates = []
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

    def draw_lines(self) -> None:
        pygame.draw.lines()

    def generate_circles(self, coordinates) -> None:
        circles = []

        for row_coordinates in coordinates:
            for each_coordinate in row_coordinates:
                # each_coordinate = center_of_each_cricle
                circles.append(Circle(window, game_settings, each_coordinate))

import pygame
import os
from circle import Circle
from goats import Goat

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
        self.selected_piece = None
        self.turn = "g"  # goat always has the first turn
        self.board_config = [
            ["t", "", "", "", "t"],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["t", "", "", "", "t"],
        ]

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

    def draw_lines(self) -> None:
        pygame.draw.lines()

    def setup_boad(self) -> None:
        pass

    def handle_click(self, mx, my, circles, window, game_settings, goat_group) -> None:
        for circle in circles:
            if circle.rect.collidepoint(mx, my):
                print("the circle is clicked")
                if not circle.clicked and not circle.occupying_piece:
                    circle.color = game_settings.CIRCLE_COLOR_CLICKED
                    circle.clicked = True
                    circle.occupying_piece = "g"
                    goat_group.add(Goat(*circle.center))
                elif not circle.clicked and circle.occupying_piece:
                    if circle.occupying_piece == "t":
                        pass
                    else:
                        pass
                    pass
                else:
                    circle.color = game_settings.CIRCLE_COLOR_DEFAULT
                    circle.clicked = False
                circle.draw(window)
                goat_group.draw(window)
                print(goat_group)
                # multiple circles cannot be highlighted at a time so we need to implement a logic for that

    def draw(self):
        pass

    def update_board(self):
        pass

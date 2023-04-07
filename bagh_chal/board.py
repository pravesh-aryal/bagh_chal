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
        self.is_piece_selected = False
        self.selected_circle = None
        # self.circles = self.generate_circles()
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
        valid_move = True  # for testing purpose
        for circle in circles:
            if circle.rect.collidepoint(mx, my):
                # check which piece the circle contains or is it empty?
                # dont forget circle.draw(window)

                self.set_default_color(circles, game_settings, window)
                # circle.color = (
                #     game_settings.CIRCLE_COLOR_CLICKED
                #     if circle.clicked == False
                #     else game_settings.CIRCLE_COLOR_DEFAULT
                # )
                if circle.clicked == False:
                    circle.color = game_settings.CIRCLE_COLOR_CLICKED
                    self.set_bool(circles)
                    circle.clicked = True
                else:
                    circle.color = game_settings.CIRCLE_COLOR_DEFAULT
                    circle.clicked = False
                circle.draw(window)

    def set_default_color(self, circles, game_settings, window):
        for circle in circles:
            circle.color = game_settings.CIRCLE_COLOR_DEFAULT
            # if circle.clicked == True:
            #     circle.clicked = False

            # else:
            #     circle.clicked = True
            circle.draw(window)

    def set_bool(self, circles):
        for circle in circles:
            circle.clicked = False

    def draw(self):
        pass

    def update_board(self):
        pass

    def generate_circles(
        window, game_settings, coordinates, tiger_group, goat_group
    ) -> None:
        circles = []

        for row_coordinates in coordinates:
            for each_coordinate in row_coordinates:
                # each_coordinate = center_of_each_cricle
                circles.append(
                    Circle(
                        window,
                        game_settings,
                        each_coordinate,
                        tiger_group,
                        goat_group,
                    )
                )

        return circles

    def get_circle_from_pos(self):
        pass

    def get_piece_from_pos(self):
        pass

    def setup_board(self):
        pass

    def draw(self):
        pass

    def tiger_clicked(self):
        pass

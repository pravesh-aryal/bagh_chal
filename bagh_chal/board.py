import pygame
import os
from circle import Circle
from goats import Goat
from tiger import Tiger

"""Class to handle board coordinates and design"""


class Board:
    def __init__(self, window, game_settings, window_rect, gm) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            game_settings.BOARD_WIDTH,
            game_settings.BOARD_HEIGHT,
        )
        self.goats = 20
        # Place the Board at the center (as same as the window)
        self.rect.center = window_rect.center
        self.is_piece_selected = False
        self.selected_circle = None
        self.turn = "g"  # goat always has the first turn
        self.coordinates = gm.generate_coordinates(self, game_settings)
        gm.initialize_board(window, game_settings, self, self.coordinates)
        self.circles = gm.generate_circles(
            window,
            game_settings,
            self.coordinates,
        )
        self.board_config = gm.board_config(self.coordinates, self.circles)
        gm.initialize_tigers(self, Tiger, self.board_config)
        self.update_board(self.board_config, window)

    def draw_lines(self) -> None:
        pygame.draw.lines()

    def handle_click(
        self, mx, my, circles, window, game_settings, goat_group, tiger_group
    ) -> None:
        valid_move = True  # for testing purpose
        # self.turn = self.get_turn()
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
                if self.turn == "g" and self.goats:
                    self.place_goat(circle, goat_group, window)
                    print(circle.occupying_piece)
                    # change the turn only if a valid move/placement is done.
                    self.turn = self.get_turn()
                    self.goats -= 1
                elif self.turn == "t":
                    # and the circle should also contain a tiger i.e contains_tiger = True || has_tiger = True
                    # self.move_tiger(circle, tiger_group, window)
                    print(circle.occupying_piece)
                    # if the cirlce has a tiger,
                    if circle.occupying_piece:
                        global prev_circle
                        prev_circle = circle
                        # donot change the turn
                    if not circle.occupying_piece:
                        # after a valid move is done
                        # print(
                        #     circle.occupying_piece.rect.center,
                        #     prev_circle.occupying_piece.rect.center,
                        # )
                        circle.occupying_piece = prev_circle.occupying_piece
                        # circle.occupying_piece.rect.center = (
                        #     prev_circle.occupying_piece.rect.center
                        # )
                        prev_circle.occupying_piece.rect.center = circle.rect.center

                        prev_circle.occupying_piece = None
                        tiger_group.draw(window)
                        for tiger in tiger_group:
                            print(tiger.rect.center)
                    # change the turn only if a valid move/placement is done.
                    # else:
                    #     self.turn = self.get_turn()

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

    def place_goat(self, circle, goat_group, window):
        goat_group.add(
            Goat(
                *circle.center,
            )
        )

    def get_turn(self):
        self.turn = "t" if self.turn == "g" else "g"
        return self.turn

    def update_board(self, config, window):
        tiger_group = pygame.sprite.Group()
        goat_group = pygame.sprite.Group()
        for each_row in config:
            for each_piece in each_row:
                if each_piece["piece"]:
                    if each_piece["piece"].notation == "t":
                        tiger_group.add(each_piece["piece"])
                    elif each_piece["piece"].notation == "g":
                        goat_group.add(each_piece["piece"])

        tiger_group.draw(window)
        goat_group.draw(window)

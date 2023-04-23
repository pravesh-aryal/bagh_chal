import pygame
import os
from circle import Circle
from goats import Goat
from tiger import Tiger

"""Class to handle board coordinates and design"""


class Board:
    def __init__(self, window, game_settings, window_rect, gm) -> None:
        self.tiger_group = pygame.sprite.Group()
        self.goat_group = pygame.sprite.Group()
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
        self.selected_piece = None
        self.turn = "g"  # goat always has the first turn
        self.coordinates = gm.generate_coordinates(self, game_settings)
        gm.initialize_board(window, game_settings, self, self.coordinates)
        self.circles = gm.generate_circles(
            window,
            game_settings,
            self.coordinates,
            self.tiger_group,
            self.goat_group,
        )
        self.board_config = gm.board_config(self.coordinates, self.circles)
        gm.initialize_tigers(self, Tiger, self.board_config)
        self.update_board(self.board_config, window)

    def handle_click(self, mx, my, window, game_settings) -> None:
        for circle in self.circles:
            if circle.rect.collidepoint(mx, my):
                self.set_default_color(self.circles, game_settings, window)

                # if circle.clicked == False:
                #     circle.color = game_settings.CIRCLE_COLOR_CLICKED
                #     self.set_bool(self.circles)
                #     circle.clicked = True
                # else:
                #     circle.color = game_settings.CIRCLE_COLOR_DEFAULT
                #     circle.clicked = False
                # circle.draw(window)
                if self.turn == "g" and self.goats:
                    self.place_goat(circle, self.goat_group, window, circle.x, circle.y)
                    # change the turn only if a valid move/placement is done.
                    self.turn = self.get_turn()
                    self.goats -= 1
                elif self.turn == "t":
                    # and the circle should also contain a tiger i.e contains_tiger = True || has_tiger = True
                    if self.selected_piece is None:
                        circle.occupying_piece = self.board_config[circle.x][circle.y][
                            "piece"
                        ]
                        # prev_circle = circle
                        self.selected_piece = circle.occupying_piece
                    elif self.move_tiger(circle, window, circle.x, circle.y):
                        self.turn = self.get_turn()
                    elif self.selected_piece is not None:
                        print("not none")
                        pass

                    # if the cirlce has a tiger,
                    # if circle.occupying_piece:
                    #     global prev_circle
                    #     prev_circle = circle
                    #     # donot change the turn
                    # if not circle.occupying_piece:
                    #     pass

                # circle.occupying_piece = prev_circle.occupying_piece
                # circle.occupying_piece.rect.center = (
                #     prev_circle.occupying_piece.rect.center
                # )
                # prev_circle.occupying_piece.rect.center = circle.rect.center

                # clicked_circle = circle

                # clicked_circle.check_for_occupancy(self.tiger_group, self.goat_group)
                # print("hey")
                # if self.selected_piece is None:
                #     if clicked_circle.occupying_piece is not None:
                #         self.selected_piece = clicked_circle.occupying_piece
                #         piece = self.get_piece(circle)
                #         self.update_board(self.board_config, window)
                # elif self.selected_piece is not None:
                #     self.selected_piece = clicked_circle.occupying_piece
                #     self.update_board(self.board_config, window)
        # self.tiger_group.draw(window)
        # self.goat_group.draw(window)
        self.update_board(self.board_config, window)

    def move_tiger(self, circle, window, x, y):
        # the piece in the new circle is now changed
        # self.board_config[circle.x][circle.y]["piece"] = self.selected_piece
        # """                {
        #             "position": (x, y),
        #             "abs_position": coordinates[x][y],
        #             "circle": circle,
        #             "piece": None,
        #         }"""
        # self.update_board(self.board_config, window)
        # return True
        tiger = Tiger(*circle.center, x, y)
        self.tiger_group.add(tiger)
        self.board_config[x][y]["position"] = (x, y)
        self.board_config[x][y]["abs_position"] = circle.center
        self.board_config[x][y]["circle"] = circle
        self.board_config[x][y]["piece"] = tiger
        circle.occupying_piece = tiger
        self.update_board(self.board_config, window)
        return True

    def get_piece(self, circle):
        for _ in self.board_config:
            for position in _:
                if position["abs_position"] == circle.rect.center:
                    return position["piece"]

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

    def place_goat(self, circle, goat_group, window, x, y):
        goat = Goat(*circle.center, x, y)
        goat_group.add(goat)
        self.board_config[x][y]["position"] = (x, y)
        self.board_config[x][y]["abs_position"] = circle.center
        self.board_config[x][y]["circle"] = circle
        self.board_config[x][y]["piece"] = goat
        circle.occupying_piece = goat
        self.update_board(self.board_config, window)

    def get_turn(self):
        self.turn = "t" if self.turn == "g" else "g"
        return self.turn

    def update_board(self, config, window):
        t_count = 0
        for each_row in self.board_config:
            for each_piece in each_row:
                if each_piece["piece"]:
                    if each_piece["piece"].notation == "t":
                        self.tiger_group.add(each_piece["piece"])
                        print(each_piece["piece"])
                        t_count += 1
                    elif each_piece["piece"].notation == "g":
                        self.goat_group.add(each_piece["piece"])
        print(len(self.tiger_group), "t count is", t_count)
        print(len(self.goat_group))
        self.tiger_group.draw(window)
        self.goat_group.draw(window)

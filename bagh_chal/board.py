import pygame
import os
from circle import Circle
from goats import Goat
from tiger import Tiger
from itertools import chain


class Board:
    """Class to handle board coordinates and design"""

    def __init__(self, window, game_settings, window_rect, gm) -> None:
        self.tiger_group = pygame.sprite.Group()
        self.goat_group = pygame.sprite.Group()
        self.tigers_trapped = 0
        self.goats = 20
        self.rect = pygame.Rect(
            0,
            0,
            game_settings.BOARD_WIDTH,
            game_settings.BOARD_HEIGHT,
        )
        # Place the Board at the center (as same as the window)
        self.rect.center = window_rect.center
        self.is_piece_selected = False
        self.selected_circle: Circle = None
        self.selected_piece: object = None
        self.turn = "g"  # goat always has the first turn
        self.coordinates: list[list] = gm.generate_coordinates(self, game_settings)
        gm.initialize_board(window, game_settings, self, self.coordinates)
        self.circles: list = gm.generate_circles(
            window,
            game_settings,
            self.coordinates,
            self.tiger_group,
            self.goat_group,
        )
        self.board_config: list[list] = gm.board_config(self.coordinates, self.circles)

        # self.check_for_occupancy(self.board_config, self.circles)
        gm.initialize_tigers(self, Tiger, self.board_config)
        (
            self.restricted_positions,
            self.unrestricted_positions,
        ) = gm.classify_coordinates(self.board_config)
        self.update_board(self.board_config, window)

    def handle_click(self, mx, my, window, game_settings) -> None:
        for circle in self.circles:
            if circle.rect.collidepoint(mx, my):
                """LEAVE OUT THE HIGHLIGHT COLOR LOGIC FOR SOME TIME"""
                self.set_default_color(self.circles, game_settings, window)

                if self.turn == "g" and self.goats:
                    self.place_goat(circle, self.goat_group, window, circle.x, circle.y)
                    # change the turn only if a valid move/placement is done.

                elif self.turn == "g" and not self.goats:
                    """MOVE EM GOATS baby"""
                    pass
                elif self.turn == "t":
                    # and the circle should also contain a tiger i.e contains_tiger = True || has_tiger = True
                    if self.selected_piece is None:
                        circle.occupying_piece = self.board_config[circle.x][
                            circle.y
                        ].piece
                        global previous_circle
                        previous_circle = circle
                        self.selected_piece = circle.occupying_piece
                    elif self.move_tiger(circle, window, circle.x, circle.y):
                        self.turn = self.get_turn()
                    elif self.selected_piece is not None:
                        pass

        self.update_board(self.board_config, window)

    def move_tiger(self, circle, window, x, y):
        for position in self.restricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours

        for position in self.unrestricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours

        # self.eat_goats(
        #     circle,
        #     previous_circle,
        #     window,
        #     x,
        #     y,
        #     valid_moves,
        # )
        if (circle.x, circle.y) in [
            valid_move.position for valid_move in valid_moves
        ] and circle.occupying_piece == None:
            for each_tiger in self.tiger_group:
                if (each_tiger.x, each_tiger.y) == (
                    previous_circle.x,
                    previous_circle.y,
                ):
                    self.tiger_group.remove(each_tiger)
                    self.board_config[previous_circle.x][previous_circle.y].piece = None
                    previous_circle.occupying_piece = None
            tiger = Tiger(*circle.center, x, y)
            self.tiger_group.add(tiger)
            self.board_config[x][y].position = (x, y)
            self.board_config[x][y].abs_position = circle.center
            self.board_config[x][y].circle = circle
            self.board_config[x][y].piece = tiger
            circle.occupying_piece = tiger
            self.update_board(self.board_config, window)
            self.selected_piece = None
            return True

    def get_piece(self, circle):
        for _ in self.board_config:
            for position in _:
                if position.abs_position == circle.rect.center:
                    return position.piece

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
        if circle.occupying_piece == None:
            goat = Goat(*circle.center, x, y)
            goat_group.add(goat)
            self.board_config[x][y].position = (x, y)
            self.board_config[x][y].abs_position = circle.center
            self.board_config[x][y].circle = circle
            self.board_config[x][y].piece = goat
            circle.occupying_piece = goat
            self.turn = self.get_turn()
            self.goats -= 1
            self.update_board(self.board_config, window)

    def get_turn(self):
        self.turn = "t" if self.turn == "g" else "g"
        return self.turn

    def update_board(self, board_config, window):
        # new
        t_count = 0
        for each_row in self.board_config:
            for position in each_row:
                if position.piece and position.piece.notation == "t":
                    self.tiger_group.add(position.piece)
                    t_count += 1
                elif position.piece and position.piece.notation == "g":
                    self.goat_group.add(position.piece)

        self.tiger_group.draw(window)
        self.goat_group.draw(window)

    # def check_for_occupancy(self, board_config, circles):
    #     for circle, position in zip(circles, chain(*board_config)):
    #         circle.occupying_piece = position["piece"]

    def eat_goats(
        self,
        circle,
        previous_circle,
        window,
        x,
        y,
        valid_moves,
    ):
        print("can i eat goats")
        # check if goat is located in any of the valid moves
        for goat in self.goat_group:
            print("guiye")
            if (goat.x, goat.y) in [
                valid_move["position"] for valid_move in valid_moves
            ]:
                print("uigete")
                # now get valid positions for the goat
                for position in self.restricted_positions:
                    if (goat.x, goat.y) == position["position"]:
                        print(position["valid_neighbours"])
                        goat.valid_moves_for_goat = position["valid_neighbours"]
                for position in self.unrestricted_positions:
                    if (goat.x, goat.y) == position["position"]:
                        print(position["valid_neighbours"])
                        goat.valid_moves_for_goat = position["valid_neighbours"]
        circle = previous_circle

        # here circle is the tiger containing circle
        for goat in self.goat_group:
            print(goat.valid_moves_for_goat)
            empty_pos = [
                valid_move
                for valid_move in goat.valid_moves_for_goat
                if valid_move["piece"] == None
            ]
            for pos in empty_pos:
                pos = pos["position"]
                pos.x, pos.y = pos["position"]
                if circle.x == goat.x == pos.x:
                    valid_moves.append(pos)
                elif circle.y == goat.y == pos.y:
                    valid_moves.append(pos)
                elif (circle.x + 1, circle.y + 1) == (goat.x, goat.y) and (
                    goat.x + 1,
                    goat.y + 1,
                ) == pos:
                    valid_moves.append(pos)
                elif (circle.x - 1, circle.y - 1) == (goat.x, goat.y) and (
                    goat.x - 1,
                    goat.y - 1,
                ) == pos:
                    valid_moves.append(pos)
                elif (circle.x + 1, circle.y - 1) == (goat.x, goat.y) and (
                    goat.x + 1,
                    goat.y - 1,
                ) == pos:
                    valid_moves.append(pos)
                elif (circle.x - 1, circle.y + 1) == (goat.x, goat.y) and (
                    goat.x - 1,
                    goat.y + 1,
                ) == pos:
                    valid_moves.append(pos)
        """
        if turn == tiger:
            get valid positions from the tigers position
                if goat is in any valid positions
                    get the valid positions from the goat position
                        if the valid positons from the goat are empty
                            get ..eatable_positions like this
                                if tiger.x = goat.x = empty.x
                                    then the tiger can move to empty by eating goat
                                elif tiger.y = goat.y = empty.y
                                    then ....
                                if tiger.x-1, tiger.y+1 ==
                                goat.x-1, goat.y -1 and goat.x-1, goat.y -1 = empty.x, empty.y
                                    then can move if clicked

        """

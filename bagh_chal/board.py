import pygame
import os
from circle import Circle
from goats import Goat
from tiger import Tiger
from itertools import chain


class Board:
    """Class to handle board coordinates and design"""

    def __init__(self, window, game_settings, window_rect, gm) -> None:
        self.tiger_group: pygame.sprite.Group = pygame.sprite.Group()
        self.goat_group: pygame.sprite.Group = pygame.sprite.Group()
        # to get number of trapped tigers we ll read length of the array
        self.trapped_tigers = []
        # remaining goats
        self.goats = 20
        self.goats_killed = 0
        self.rect = pygame.Rect(
            0,
            0,
            game_settings.BOARD_WIDTH,
            game_settings.BOARD_HEIGHT,
        )
        # Place the Board at the center (as same as the window)
        self.rect.center = window_rect.center
        # No piece, circle is selected at first
        self.is_piece_selected = False
        self.selected_circle: Circle = None
        self.selected_piece: object = None
        self.turn = "g"  # goat always has the first turn
        self.coordinates: list[list] = gm.generate_coordinates(self)
        gm.initialize_board(window, self, self.coordinates)
        self.circles: list[list] = gm.generate_circles(window, self.coordinates)
        self.board_config: list[list] = self.circles
        # board config shold be the self.circles with updated pieces at each instance of the game
        gm.initialize_tigers(self, Tiger, self.board_config)
        (
            self.restricted_positions,
            self.unrestricted_positions,
        ) = gm.classify_coordinates(self.board_config)
        self.restricted_positions: list = [
            position for position in chain(self.board_config) if position.is_restricted
        ]
        self.unrestricted_positions: list = [
            position
            for position in chain(self.board_config)
            if not position.is_restricted
        ]
        # self.check_for_occupancy(self.board_config, self.circles)
        self.update_board(self.board_config, window)

    def handle_second_click(self, previous_circle, next_circle, selected_piece) -> None:
        # this will handle second click
        if next_circle in previous_circle.valid_neighbours and self.turn == "g":
            # move the selected goat
            selected_piece.move(previous_circle, next_circle)
        elif self.turn == "t" and next_circle in [
            *previous_circle.valid_neighbours,
            *selected_piece.additional_valid_moves,
        ]:
            # we need to get more valid positions for this one
            selected_piece.get_all_valid_moves(
                previous_circle, next_circle, self.board_config
            )
            selected_piece.move(
                selected_piece, previous_circle, next_circle, self.board_config
            )

    def get_circle_from_pos(self, pos_x, pos_y):
        for circle in chain(*self.circles):
            if (pos_x, pos_y) == (circle.pos_x, circle.pos_y):
                return circle

    def handle_click(self, mx, my, window, game_settings) -> None:
        """this will handle the first click only"""
        for circle in chain(*self.circles):
            if circle.rect.collidepoint(mx, my):
                """LEAVE OUT THE HIGHLIGHT COLOR LOGIC FOR SOME TIME"""
                # self.set_default_color(self.circles, game_settings, window)

                # if any of the goat is remaining, the player must place the goat before moving any of the goat
                if self.turn == "g" and self.goats and circle.occuyping_piece is None:
                    self.place_goat(circle, window)
                    # change the turn after placing
                    self.get_turn()

                    # change the turn only if a valid move/placement is done.
                # if all 20 goats have already been placed the user should move one of the goats

                elif (
                    circle.occupying_piece.notation == self.turn
                    and self.selected_piece is None
                ):
                    # this executes on the first click
                    self.selected_piece = circle.occupying_piece

                elif self.selected_piece is not None:
                    # this executes on the second click
                    # this means a piece is now selected and now we need to handle the second click
                    previous_circle = self.get_circle_from_pos(
                        self.selected_piece.pos_x, self.selected_piece.pos_y
                    )
                    if self.selected_piece.notation == "t":
                        self.selected_piece.get_all_valid_moves()
                    self.handle_second_click(
                        previous_circle, circle, self.selected_piece
                    )

        self.update_board(self.board_config, window)

    def get_piece(self, circle):
        for _ in self.board_config:
            for position in _:
                if position.abs_position == circle.rect.center:
                    return position.piece

    def set_default_color(self, circles, game_settings, window):
        for circle in circles:
            circle.color = (220, 220, 220)
            circle.draw(window, game_settings)

    def set_bool(self, circles):
        for circle in circles:
            circle.clicked = False

    def place_goat(self, circle, window):
        goat = Goat(circle.pos_x, circle.pos_y, *circle.center)
        self.goat_group.add(goat)
        circle.occupying_piece = goat
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

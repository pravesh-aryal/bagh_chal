import pygame
import os
from circle import Circle
from goats import Goat
from tiger import Tiger
from itertools import chain


class Board:
    """Class to handle board coordinates and design"""

    def __init__(self, window, game_settings, window_rect, gm) -> None:
        # to get number of trapped tigers we ll read length of the array

        self.tiger_group: pygame.sprite.Group = pygame.sprite.Group()
        self.goat_group: pygame.sprite.Group = pygame.sprite.Group()
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
        self.circle_group = pygame.sprite.Group()
        self.circle_group.add(chain(*self.circles))
        self.board_config: list[list] = self.circles
        # board config shold be the self.circles with updated pieces at each instance of the game
        gm.initialize_tigers(self, Tiger, self.board_config, self.tiger_group)

        self.restricted_positions: list = [
            position for position in chain(*self.board_config) if position.is_restricted
        ]
        self.unrestricted_positions: list = [
            position
            for position in chain(*self.board_config)
            if not position.is_restricted
        ]
        gm.classify_coordinates(self.board_config)
        self.window = window
        # self.check_for_occupancy(self.board_config, self.circles)
        self.update_board(window)

    def handle_second_click(self, previous_circle, next_circle, selected_piece) -> None:
        # this will handle second click

        if next_circle in previous_circle.valid_neighbours and self.turn == "g":
            # move the selected goati
            selected_piece.move(previous_circle, next_circle)

        elif self.turn == "t" and next_circle in [
            *previous_circle.valid_neighbours,
            *selected_piece.additional_moves,
        ]:
            selected_piece.move(
                selected_piece,
                previous_circle,
                next_circle,
                self.board_config,
                Tiger,
                self.tiger_group,
                self.goat_group,
            )
            self.get_turn()
        self.update_board(self.window)
        # pygame.display.flip()

    def get_circle_from_pos(self, pos_x, pos_y):
        for circle in chain(*self.circles):
            if (pos_x, pos_y) == (circle.pos_x, circle.pos_y):
                return circle

    def handle_click(self, mx, my, window) -> None:
        """this will handle the first click only"""
        for circle in chain(*self.circles):
            if circle.rect.collidepoint(mx, my):
                """LEAVE OUT THE HIGHLIGHT COLOR LOGIC FOR SOME TIME"""
                if self.turn == "g" and self.goats and circle.occupying_piece is None:
                    pass  # place the goat
                elif (
                    self.turn == "g"
                    and not self.goats
                    and circle.occupying_piece == "g"
                ):
                    pass  # Move the goat
                elif self.turn == "t" and circle.occupying_piece.notation == "t":
                    pass  # move the tiger
                # self.set_default_color(self.circles, game_settings, window)
                # if any of the goat is remaining, the player must place the goat before moving any of the goat
                if self.turn == "g" and self.goats and circle.occupying_piece is None:
                    self.place_goat(circle, window)
                    # change the turn after placing
                    self.get_turn()

                    # change the turn only if a valid move/placement is done.
                # if all 20 goats have already been placed the user should move one of the goats

                elif (
                    circle.occupying_piece
                    and circle.occupying_piece.notation == self.turn
                    and self.selected_piece is None
                ):
                    # this executes on the first click
                    self.selected_piece = circle.occupying_piece
                    global previous_circle
                    previous_circle = self.get_circle_from_pos(
                        self.selected_piece.pos_x, self.selected_piece.pos_y
                    )
                    if self.selected_piece.notation == "t":
                        self.selected_piece.get_all_valid_moves(previous_circle)

                elif circle.occupying_piece is self.selected_piece:
                    self.selected_piece = None

                elif self.selected_piece is not None:
                    # this executes on the second click
                    # this means a piece is now selected and now we need to handle the second click

                    self.handle_second_click(
                        previous_circle, circle, self.selected_piece
                    )
        self.update_board(window)

    def set_default_color(self, circles, game_settings, window):
        for circle in circles:
            circle.color = (220, 220, 220)
            circle.draw(window, game_settings)

    def place_goat(self, circle, window):
        goat = Goat(circle.pos_x, circle.pos_y, *circle.center)
        self.goat_group.add(goat)
        circle.occupying_piece = goat
        self.goats -= 1
        self.update_board(window)

    def get_turn(self):
        self.turn = "t" if self.turn == "g" else "g"
        return self.turn

    def update_board(self, window):
        # for circle in chain(*self.board_config):
        #     if circle.occupying_piece and circle.occupying_piece.notation == "t":
        #         self.tiger_group.add(circle.occupying_piece)
        #     elif circle.occupying_piece and circle.occupying_piece.notation == "g":
        #         self.goat_group.add(circle.occupying_piece)
        print("ONE ITER", len(self.circle_group))
        for tiger in self.tiger_group:
            print(tiger.pos_x, tiger.pos_y)
        # self.circle_group.draw(window)
        for circle in chain(*self.circles):
            circle.draw(self.window)
        self.tiger_group.draw(window)

        self.goat_group.draw(window)
        # pygame.display.flip()

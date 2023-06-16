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
        # self.goat_group: pygame.sprite.Group = pygame.sprite.Group()
        self.goat_group = []
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
        self.update_board(window)

    def get_circle_from_pos(self, pos_x, pos_y):
        for circle in chain(*self.circles):
            if (pos_x, pos_y) == (circle.pos_x, circle.pos_y):
                return circle

    def highlight_circles(self, circles, killable_goats, current_circle):
        current_circle.highlight = True
        current_circle.draw(self.window)
        for circle in circles:
            circle.highlight = True
            circle.draw(self.window)
        for killable_goat in killable_goats.keys():
            killable_goat.highlight = True
            circle.draw(self.window)

    def handle_click(self, mx, my, window) -> None:
        for circle in chain(*self.circles):
            if circle.rect.collidepoint(mx, my):
                # Player must  place 20 goats at first
                if self.turn == "g" and self.goats and circle.occupying_piece is None:
                    self.place_goat(circle, window)
                    # change the turn after placement
                    self.get_turn()

                # if all 20 goats have already been placed the user should move one of the goats or another player should move the tiger
                elif self.turn == "g" and self.goats != 0:
                    pass
                elif (
                    circle.occupying_piece
                    and circle.occupying_piece.notation == self.turn
                    and self.selected_piece is None
                ):
                    # On first click
                    self.selected_piece = circle.occupying_piece
                    global previous_circle
                    previous_circle = self.get_circle_from_pos(
                        self.selected_piece.pos_x, self.selected_piece.pos_y
                    )

                    valid_moves, killable_goats = self.selected_piece.get_valid_moves(
                        previous_circle
                    )
                    self.highlight_circles(valid_moves, killable_goats, circle)

                elif circle.occupying_piece is self.selected_piece:
                    # If same piece is clicked for the second time we unselect it
                    self.selected_piece = None
                    self.set_default_color()

                elif self.selected_piece is not None:
                    # On second click
                    if self.selected_piece.move(
                        previous_circle, circle, self.goat_group, self.tiger_group, self
                    ):
                        self.get_turn()
                        self.selected_piece = None
                        self.set_default_color()
        self.update_board(window)

    def set_default_color(self):
        for circle in chain(*self.circles):
            circle.highlight = False
            circle.draw(self.window)

    def place_goat(self, circle, window):
        goat = Goat(circle.pos_x, circle.pos_y, *circle.center)
        # self.goat_group.add(goat)
        self.goat_group.append(goat)
        circle.occupying_piece = goat
        print(circle.occupying_piece, circle.position)
        self.goats -= 1
        self.update_board(window)

    def get_turn(self):
        self.turn = "t" if self.turn == "g" else "g"
        return self.turn

    def update_board(self, window):
        for circle in chain(*self.circles):
            circle.draw(self.window)
        self.tiger_group.draw(window)
        for goat in self.goat_group:
            window.blit(goat.image, goat.rect)


    def check_for_trapped_tigers(self):
        self.trapped_tigers = []
        for tiger in self.tiger_group:
            valid_moves = tiger.get_valid_moves(
                self.get_circle_from_pos(tiger.pos_x, tiger.pos_y)
            )
            if len(valid_moves) == 0:
                self.trapped_tigers.append(tiger)

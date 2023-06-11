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
        self.restricted_positions = [
            position for position in chain(self.board_config) if position.is_restricted
        ]
        self.unrestricted_positions = [
            position
            for position in chain(self.board_config)
            if not position.is_restricted
        ]
        # self.check_for_occupancy(self.board_config, self.circles)
        self.update_board(self.board_config, window)

    def check_for_occupancy(self, board_config, circles):
        #     #     for circle, position in zip(circles, chain(*board_config)):
        # for circle, position in zip(circles, chain(*board_config)):
        #     circle.occupying_piece = position.piece
        pass

    def highlight_circles(
        self, correct_moves, extra_correct_moves, correct_intermediate_moves
    ):
        if self.selected_piece is not None:
            self.set_default_color(self.circles, 1, 1)
            if correct_moves:
                for correct_move in correct_moves:
                    if correct_move.piece == None:
                        correct_move.circle.color = (144, 238, 144)
                        correct_move.circle.draw(1, 2)
            if extra_correct_moves:
                for extra_correct_move in extra_correct_moves:
                    extra_correct_move.circle.color = (144, 238, 144)
                    extra_correct_move.circle.draw(1, 2)
            if correct_intermediate_moves:
                for correct_intermediate_move in correct_intermediate_moves:
                    if correct_intermediate_move.piece.notation == "g":
                        correct_intermediate_move.circle.color = (255, 0, 0)
                        correct_intermediate_move.circle.draw(1, 2)

    def handle_second_click() -> None:
        pass

    def handle_click(self, mx, my, window, game_settings) -> None:
        """this will handle the first click only"""
        for circle in chain(*self.circles):
            if circle.rect.collidepoint(mx, my):
                """LEAVE OUT THE HIGHLIGHT COLOR LOGIC FOR SOME TIME"""
                # self.set_default_color(self.circles, game_settings, window)

                if self.turn == "g" and self.goats and circle.occuyping_piece is None:
                    self.place_goat(circle, window)

                    # change the turn only if a valid move/placement is done.

                else:
                    if self.selected_piece is None:
                        piece = circle.occupying_piece
                        if piece and (piece.notation == self.turn):
                            self.selected_circle = circle
                            global previous_circle
                            previous_circle = circle
                            previous_circle.clicked = True
                            self.selected_piece = piece
                            (
                                self.correct_moves,
                                self.extra_correct_moves,
                                self.correct_intermediate_moves,
                            ) = self.selected_piece.get_all_valid_moves(
                                self, previous_circle, circle
                            )

                            self.highlight_circles(
                                self.correct_moves,
                                self.extra_correct_moves,
                                self.correct_intermediate_moves,
                            )

                    elif self.selected_piece.move(
                        self,
                        circle,
                        window,
                        circle.x,
                        circle.y,
                        game_settings,
                        previous_circle,
                        self.selected_piece,
                        Goat,
                        Tiger,
                    ):
                        self.set_default_color(self.circles, game_settings, window)
                        self.turn = self.get_turn()

                    elif self.selected_piece is not None:
                        self.set_default_color(self.circles, 1, 1)
                        previous_circle.occupying_piece == circle.occupying_piece
                        self.selected_piece = None

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


"""
# logic to draw and highlight
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        for square in self.squares:
            square.draw(display)
# this is square.draw()
    def draw(self, display):
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
"""

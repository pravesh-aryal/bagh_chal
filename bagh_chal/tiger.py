import pygame, os
from pygame.sprite import Sprite

from pathlib import Path
import game_mechanics as gm

"""Tiger class to manage behaviour of tigers"""


class Tiger(Sprite):
    def __init__(self, pos_x, pos_y, abs_x, abs_y):
        """Initialize the tiger pieces and set their starting position"""
        super(Tiger, self).__init__()
        self.image = pygame.image.load(Path("./images/tiger.png"))
        self.rect = self.image.get_rect()
        self.rect.center = abs_x, abs_y
        self.is_selected = False
        self.notation = "t"
        self.pos_x, self.pos_y = pos_x, pos_y
        self.isinwhatposition = None
        self.trapped = False
        self.additional_moves = []

    def get_valid_moves(self, previous_circle):
        additional_valid_moves = []  # moves that can kill goats
        previous_circle_neighbours = previous_circle.valid_neighbours
        goat_neighbours = []
        goat_neighbour_and_extra_valid_move = {}
        for neighbour in previous_circle_neighbours:
            if neighbour.occupying_piece and neighbour.occupying_piece.notation == "g":
                goat_neighbours.append(neighbour)

        for goat_neighbour in goat_neighbours:
            for valid_for_goat_position in goat_neighbour.valid_neighbours:
                # previous circle == clicked circle
                if valid_for_goat_position.occupying_piece == None:
                    if (
                        previous_circle.x
                        == valid_for_goat_position.x
                        == goat_neighbour.x
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

                    elif (
                        previous_circle.y
                        == valid_for_goat_position.y
                        == goat_neighbour.y
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

                    elif (previous_circle.x + 1, previous_circle.y + 1) == (
                        goat_neighbour.x,
                        goat_neighbour.y,
                    ) and (goat_neighbour.x + 1, goat_neighbour.y + 1) == (
                        valid_for_goat_position.x,
                        valid_for_goat_position.y,
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

                    elif (previous_circle.x - 1, previous_circle.y - 1) == (
                        goat_neighbour.x,
                        goat_neighbour.y,
                    ) and (goat_neighbour.x - 1, goat_neighbour.y - 1) == (
                        valid_for_goat_position.x,
                        valid_for_goat_position.y,
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

                    elif (previous_circle.x + 1, previous_circle.y - 1) == (
                        goat_neighbour.x,
                        goat_neighbour.y,
                    ) and (goat_neighbour.x + 1, goat_neighbour.y - 1) == (
                        valid_for_goat_position.x,
                        valid_for_goat_position.y,
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

                    elif (previous_circle.x - 1, previous_circle.y + 1) == (
                        goat_neighbour.x,
                        goat_neighbour.y,
                    ) and (goat_neighbour.x - 1, goat_neighbour.y + 1) == (
                        valid_for_goat_position.x,
                        valid_for_goat_position.y,
                    ):
                        additional_valid_moves.append(valid_for_goat_position)
                        goat_neighbour_and_extra_valid_move[
                            goat_neighbour
                        ] = valid_for_goat_position

        self.additional_moves = additional_valid_moves
        self.goat_and_moves = goat_neighbour_and_extra_valid_move
        self.valid_moves = [
            *additional_valid_moves,
            *[
                valid_move
                for valid_move in previous_circle.valid_neighbours
                if valid_move.occupying_piece is None
            ],
        ]
        return (
            [
                *additional_valid_moves,
                *[
                    valid_move
                    for valid_move in previous_circle.valid_neighbours
                    if valid_move.occupying_piece is None
                ],
            ],
            self.goat_and_moves,
        )

    def check_and_kill(self, previous_circle, next_circle, goat_group, board):
        for goat_circle, empty_circle in self.goat_and_moves.items():
            if next_circle == empty_circle:
                goat_group.remove(goat_circle.occupying_piece)
                goat_circle.occupying_piece = None
                board.goats_killed += 1

    def move(self, previous_circle, next_circle, goat_group, tiger_group, board):
        if next_circle in self.valid_moves:
            self.check_and_kill(previous_circle, next_circle, goat_group, board)
            tiger_group.remove(previous_circle.occupying_piece)
            previous_circle.occupying_piece = None
            next_tiger = Tiger(*next_circle.position, *next_circle.center)
            tiger_group.add(next_tiger)
            next_circle.occupying_piece = next_tiger
            return True

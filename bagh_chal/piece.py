import pygame


class Piece:
    def __init__(self):
        pass

    def move(
        self,
        selected_piece,
        previous_circle,
        next_circle,
        board_config,
        Tiger,
        tiger_group,
        goat_group,
    ):
        # now update the board
        if selected_piece.notation == "t":
            # if next_circle in selected_piece.goat_neighbour_and_extra_valid_move
            selected_piece.check_and_kill(previous_circle, next_circle, goat_group)
            tiger_group.remove(previous_circle.occupying_piece)
            previous_circle.occupying_piece = None
            next_tiger = Tiger(*next_circle.position, *next_circle.center)
            tiger_group.add(next_tiger)
            print(next_tiger.additional_moves, "HEY CHECK THIS")
            next_circle.occupying_piece = next_tiger

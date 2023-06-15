import pygame, os
from pygame.sprite import Sprite
from pathlib import Path


class Goat(Sprite):
    def __init__(self, pos_x, pos_y, abs_pos_x, abs_pos_y):
        # super(Goat, self).__init__()
        Sprite.__init__(Goat)
        self.image = pygame.image.load(Path("./images/goat.png"))
        self.rect = self.image.get_rect()
        self.rect.center = abs_pos_x, abs_pos_y
        self.is_selected = False
        self.notation = "g"
        # self.x, self.y = (x, y)
        self.valid_moves_for_goat = None
        self.pos_x, self.pos_y = pos_x, pos_y

    def move(self, previous_circle, next_circle, goat_group, tiger_group, board):
        if next_circle in self.valid_moves:
            goat_group.remove(previous_circle.occupying_piece)
            previous_circle.occupying_piece = None
            next_goat = Goat(*next_circle.position, *next_circle.center)
            goat_group.add(next_goat)
            next_circle.occupying_piece = next_goat
            return True

    def get_valid_moves(self, previous_circle):
        self.valid_moves = [
            valid_move
            for valid_move in previous_circle.valid_neighbours
            if valid_move.occupying_piece is None
        ]

        return (
            [
                valid_move
                for valid_move in previous_circle.valid_neighbours
                if valid_move.occupying_piece is None
            ],
            {},
        )

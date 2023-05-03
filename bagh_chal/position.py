import pygame, os
from pygame.sprite import Sprite


class Position:
    """Piece class to manage behaviour of goats, tigers and empty positions; also works as a Piece position in board.config"""

    def __init__(self, x: int, y: int, abs_x: int, abs_y: int, circle: object):
        # super(Position, self).__init__()
        self.x, self.y = x, y
        self.position = self.x, self.y
        self.coordinate = self.x, self.y
        self.abs_x, self.abs_y = abs_x, abs_y
        self.abs_position = self.abs_x, self.abs_y
        self.circle: object = circle
        self.piece: object = None
        self.valid_neighbours: list[object] = None

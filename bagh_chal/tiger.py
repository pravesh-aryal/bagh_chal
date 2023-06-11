import pygame, os
from pygame.sprite import Sprite
from piece import Piece
from pathlib import Path

"""Tiger class to manage behaviour of tigers"""


class Tiger(Sprite, Piece):
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

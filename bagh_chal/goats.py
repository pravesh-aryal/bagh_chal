import pygame, os
from pygame.sprite import Sprite

from piece import Piece


class Goat(Sprite, Piece):
    def __init__(self, pos_x, pos_y, x, y):
        # super(Goat, self).__init__()
        Sprite.__init__(Goat)
        self.image = pygame.image.load("./images/goat.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.is_selected = False
        self.notation = "g"
        self.x, self.y = (x, y)
        self.valid_moves_for_goat = None

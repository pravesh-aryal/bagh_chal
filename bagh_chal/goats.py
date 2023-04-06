import pygame, os
from pygame.sprite import Sprite


class Goat(Sprite):
    def __init__(self, pos_x, pos_y):
        super(Goat, self).__init__()
        self.image = pygame.image.load("./images/goat.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.is_selected = False

    def get_possible_moves(self):
        pass

    def get_valid_moves(self):
        pass

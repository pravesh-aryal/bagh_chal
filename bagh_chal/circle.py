import pygame
from pygame.sprite import Sprite
from settings import Settings
import game_mechanics as gm

game_settings = Settings()


# every circle is a rect object modified to visualize as a circle
class Circle(Sprite):
    """Circle class that works as a container for position, tiger or goats."""

    def __init__(self, window, center, pos_x, pos_y):
        super(Circle, self).__init__()
        self.pos_x, self.pos_y = self.pos = pos_x, pos_y
        self.center = self.abs_pos = center  # abs_x, abs_y
        self.clicked = False
        self.highlight = False
        self.rect = pygame.Rect(
            *center, game_settings.CIRCLE_WIDTH, game_settings.CIRCLE_HEIGHT
        )
        self.is_restricted = False if (sum(self.pos)) % 2 == 0 else True
        self.rect.center = center
        self.color = (
            game_settings.CIRCLE_COLOR_DEFAULT
            if not self.highlight
            else game_settings.CIRCLE_COLOR_HIGHLIGHT
        )
        self.draw(window)
        self.occupying_piece = None
        self.highlight = False
        self.valid_neighbours = []
        # self.valid_neighbours = gm.get_valid_neighbours(self)

    def draw(self, window):
        pygame.draw.rect(
            window,
            self.color,
            self.rect,
            0,
            game_settings.CIRCLE_RADIUS,
        )

    def get_coordinate(self):
        pass

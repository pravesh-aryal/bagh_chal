import pygame
from pygame.sprite import Sprite

# from bagh_chal import tiger_group
# from board import goat_group


# every circle is a rect object modified to visualize as a circle
class Circle(Sprite):
    """Circle class that works as a container for position, tiger or goats."""

    def __init__(self, window, game_settings, center, tiger_group, goat_group, x, y):
        super(Circle, self).__init__()
        self.x, self.pos_x = x, x
        self.y, self.pos_y = y, y
        self.center = center  # abs_x, abs_y
        self.clicked = False
        self.highlight = False
        self.rect = pygame.Rect(*center, 80, 80)
        self.rect.center = center
        self.draw(window, game_settings)
        self.occupying_piece = None
        self.highlight = False
        # implementing position in circle class
        # self.position = self.x, self.y
        # self.coordinate = self.x, self.y
        # self.abs_x, self.abs_y = self.center
        # self.circle = self
        # self.piece: object = None
        # self.valid_neighbours: list[object] = None

    def draw(self, window, game_settings):
        pygame.draw.rect(
            window,
            game_settings.CIRCLE_COLOR_DEFAULT
            if self.highlight == False
            else game_settings.CIRCLE_COLOR_CLICKED,
            self.rect,
            0,
            75,
        )

    def get_coordinate(self):
        pass

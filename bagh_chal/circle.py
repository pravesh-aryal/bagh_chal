import pygame
from pygame.sprite import Sprite
from settings import Settings

game_settings = Settings()


class Circle(Sprite):
    """Circle class that works as a container for position, tiger or goat."""

    def __init__(self, window, center, pos_x, pos_y):
        super(Circle, self).__init__()
        self.pos_x, self.pos_y = self.pos = pos_x, pos_y
        self.x, self.y = self.pos_x, self.pos_y
        self.position = self.pos
        self.center = self.abs_pos = center  # abs_x, abs_y
        self.highlight = False
        self.rect = pygame.Rect(
            *center, game_settings.CIRCLE_WIDTH, game_settings.CIRCLE_HEIGHT
        )
        self.is_restricted = False if (sum(self.pos)) % 2 == 0 else True
        self.rect.center = center
        self.draw(window)
        self.occupying_piece = None
        self.highlight = False
        self.valid_neighbours = []

    def draw(self, window):
        if self.highlight:
            self.color = game_settings.CIRCLE_COLOR_HIGHLIGHT
        if (
            self.highlight
            and self.occupying_piece
            and self.occupying_piece.notation == "g"
        ):
            self.color = game_settings.CIRCLE_COLOR_RED
        if not self.highlight:
            self.color = game_settings.CIRCLE_COLOR_DEFAULT
        pygame.draw.rect(
            window,
            self.color,
            self.rect,
            0,
            game_settings.CIRCLE_RADIUS,
        )

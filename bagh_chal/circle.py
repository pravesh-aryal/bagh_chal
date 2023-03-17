import pygame


class Circle:
    def __init__(self, window, game_settings, center):
        self.center = center
        pygame.draw.circle(
            window,
            game_settings.CIRCLE_COLOR_DEFAULT,
            center,
            game_settings.CIRCLE_RADIUS,
        )

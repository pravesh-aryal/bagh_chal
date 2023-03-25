
import pygame

# every circle is a rect object modified to visualize as a circle
class Circle:
    def __init__(self, window, game_settings, center):
        print(*center)
        self.center = center
        self.clicked = False
        self.rect = pygame.Rect(*center, 80, 80)
        self.rect.center = center
        self.color = (
            game_settings.CIRCLE_COLOR_DEFAULT
            if not self.clicked
            else game_settings.CIRCLE_COLOR_CLICKED
        )
        pygame.draw.rect(
            window,
            self.color,
            self.rect,
            0,
            75,
        )

    def draw(self, window):
        pygame.draw.rect(
            window,
            self.color,
            self.rect,
            0,
            75,
        )

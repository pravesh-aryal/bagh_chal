import pygame
from pygame.sprite import Sprite

# from bagh_chal import tiger_group
# from board import goat_group


# every circle is a rect object modified to visualize as a circle
class Circle(Sprite):
    def __init__(
        self, window, game_settings, center, tiger_group, goat_group, x, y, board_config
    ):
        super(Circle, self).__init__()
        self.x = x
        self.y = y
        self.center = center  # abs_x, abs_y
        self.clicked = False
        self.rect = pygame.Rect(*center, 80, 80)
        self.rect.center = center
        # self.color = (
        #     game_settings.CIRCLE_COLOR_DEFAULT
        #     if not self.clicked
        #     else game_settings.CIRCLE_COLOR_CLICKED
        # )
        self.color = game_settings.CIRCLE_COLOR_DEFAULT
        self.image = ""
        # self.highlight_color = game_settings.CIRCLE_COLOR_CLICKED
        self.draw(window)

        self.occupying_piece = None
        self.highlight = False
        self.coordinate = self.get_coordinate()
        # self.check_for_occupancy()

    def draw(self, window):
        pygame.draw.rect(
            window,
            self.color,
            self.rect,
            0,
            75,
        )

    def get_coordinate(self):
        pass

    # def check_for_occupancy(self, board_config):
    #     for each_row in board_config:
    #         for each_position in each_row:
    #             self.occupying_piece = board_config["piece"]

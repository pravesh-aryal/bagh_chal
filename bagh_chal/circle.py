import pygame


class Circle:
    def __init__(self, window, game_settings, coordinates):
        # self.radius = game_settings.CIRCLE_RADIUS
        for row_coordinates in coordinates:
            for each_coordinate in row_coordinates:
                print(each_coordinate)
                pygame.draw.circle(
                    window,
                    game_settings.CIRCLE_COLOR_DEFAULT,
                    each_coordinate,
                    game_settings.CIRCLE_RADIUS,
                )

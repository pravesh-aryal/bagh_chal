import pygame
import os


class Board:
    def __init__(self, game_settings, window_rect) -> None:
        self.rect = pygame.Rect(
            0,
            0,
            game_settings.BOARD_WIDTH,
            game_settings.BOARD_HEIGHT,
        )

        # Place the Board at the center (as same as the window)
        self.rect.center = window_rect.center

    def draw_lines(self) -> None:
        pygame.draw.lines()

    def generate_points(self, game_settings) -> None:
        # Coordinate of top left corner of the game board in (x, y)
        starting_point = (self.rect.left, self.rect.top)
        length = game_settings.BOARD_WIDTH

        coordinates = []
        JUMP_VALUE = int(length / 4)
        x, y = starting_point

        for i in range(0, 5):
            row = []
            for j in range(0, 5):
                row.append((x, y))
                y += JUMP_VALUE

            coordinates.append(row)
            x += JUMP_VALUE
            y = starting_point[1]

        # print(coordinates)
        # coordinate for lines
        CFL = []
        for each_row in coordinates:
            CFL.append((each_row[0], each_row[len(each_row) - 1]))
        CFLF = []
        index = 0
        for i in range(0, 5):
            CFL2 = []
            for each_row in coordinates:
                print(each_row[index])
                CFL2.append(each_row[index])

            CFLF.append(CFL2)
            index += 1

        print(CFLF)
        return CFL, CFLF

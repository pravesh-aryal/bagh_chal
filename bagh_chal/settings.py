"""A class to store all the settings and values for the game."""


class Settings:
    def __init__(self) -> None:
        # Initialize settings for the game.
        # screen settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.WINDOW_BG_COLOR = (255, 255, 255)
        # board settings
        self.BOARD_WIDTH = 600
        self.BOARD_HEIGHT = 600
        self.BOARD_COLOR = (255, 255, 255)

        # lines settings
        self.LINE_COLOR = (0, 0, 0)

        # Circle settings
        self.CIRCLE_RADIUS = 32
        self.CIRCLE_COLOR_DEFAULT = (220, 220, 220)

import pyagme, os
from pygame.sprite import Sprite


class Piece(object):
    """Piece class to manage behaviour of goats and tigers; also works as a Piece position in board.config"""

    def __init__(self, x, y, abs_x, abs_y, circle):
        super(ClassName, self).__init__()
        self.x, sel.y = x, y
        self.abs_x, self.abs_y = abs_x, abs_y
        self.circle = circle
        self.piece = self

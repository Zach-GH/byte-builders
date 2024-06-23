"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import pg, FIELD_W, FIELD_H, TILE_SIZE

"""
Add class docstring here.
"""
class GameBoard:
    def __init__(self, app):
        self.app = app
        self.win = self.app.screen
        self.win_x, self.win_y = self.win.get_size()
        self.center_x = (self.win_x - (FIELD_W * TILE_SIZE)) / 2
        self.center_y = (self.win_y - (FIELD_H * TILE_SIZE)) / 2

    def draw_grid(self):
        """
        Add function docstring here.
        """
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (self.center_x + x * TILE_SIZE,
                              self.center_y + y * TILE_SIZE,
                              TILE_SIZE, TILE_SIZE), 2)

    def update(self):
        """
        Add function docstring here.
        """
        pass

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_grid()

"""
Zachary Meisner
player.py

Add module docstring here
"""

from settings import pg, CELL_SIZE, GRID_COLS, GRID_ROWS

class Player:
    def __init__(self, start_pos, color):
        self.pos = start_pos
        self.color = color
        self.size = CELL_SIZE

    def move(self, direction):
        if direction == 'LEFT':
            self.pos = (self.pos[0], max(self.pos[1] - 1, 0))
        elif direction == 'RIGHT':
            self.pos = (self.pos[0], min(self.pos[1] + 1, GRID_COLS - 1))
        elif direction == 'UP':
            self.pos = (max(self.pos[0] - 1, 0), self.pos[1])
        elif direction == 'DOWN':
            self.pos = (min(self.pos[0] + 1, GRID_ROWS - 1), self.pos[1])

    def draw(self, screen, center_x, center_y):
        x = self.pos[1] * self.size + center_x
        y = self.pos[0] * self.size + center_y
        pg.draw.rect(screen, self.color, (x, y, self.size, self.size))
        pg.draw.rect(screen, (0, 0, 0), (x, y, self.size, self.size), 5)

    def get_position(self):
        return self.pos

"""
Zachary Meisner
grid.py

Intended file for just the grid so make gameboard easier to read.
"""

from settings import (pg, GRID_ROWS, GRID_COLS, GRID_COLOR, CELL_SIZE)
from components import Text

class Grid:
    """
    Grid class to handle the grid.
    """
    def __init__(self, app):
        self.app = app
        self.screen = self.app.screen
        self.x, self.y = (self.app.x, self.app.y)
        self.center_x = (self.x - (GRID_COLS * CELL_SIZE)) / 2
        self.center_y = (self.y - (GRID_ROWS * CELL_SIZE)) / 2
        self.text_list = [("t1", 25, "Game", "white", "title"),
                          ("t2", 25, "Roll\nAgain", "white", "ra1"),
                          ("t3", 25, "Roll\nAgain", "white", "ra2"),
                          ("t4", 25, "Roll\nAgain", "white", "ra3"),
                          ("t5", 25, "Roll\nAgain", "white", "ra4"),
                          ("t6", 25, "HQ", "white", "hq1"),
                          ("t7", 25, "HQ", "white", "hq2"),
                          ("t8", 25, "HQ", "black", "hq3"),
                          ("t9", 25, "HQ", "black", "hq4"),
                          ("t10", 25, "Trivial Compute", "white", "tc")]
        self.grid = []
        self.init_grid()

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def render_text_to_rect(self, text, font_size, text_color, rect):
        font = pg.font.Font(None, font_size)
        lines = text.split("\n")
        y_offset = 0

        for line in lines:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(rect.centerx,
                                                      rect.y + y_offset +
                                                      text_surface.get_height()
                                                      / 2 + 20))
            self.screen.blit(text_surface, text_rect.topleft)
            y_offset += text_surface.get_height()

    def move_action(self):
        pass

    def roll_again_action(self):
        print("Roll Again!")

    def hq_action(self):
        print("HQ!")

    def trivial_compute_action(self):
        print("Trivial Compute!")

    def init_grid(self):
        for row in range(GRID_ROWS):
            row_list = []
            for col in range(GRID_COLS):
                cell = {
                    'id': f'{row}-{col}',
                    'color': GRID_COLOR,
                    'action': self.move_action,
                    'rect': pg.Rect(col * CELL_SIZE + self.center_x,
                                    row * CELL_SIZE + self.center_y,
                                    CELL_SIZE, CELL_SIZE),
                    'special': False
                }
                if ((row == 0 and col == 0) or (row == 0 and col == 8)
                    or (row == 8 and col == 0) or (row == 8 and col == 8)):
                    cell['color'] = (255, 255, 255) # White
                    cell['text'] = "Roll\nAgain"
                    cell['text_color'] = "Black"
                    cell['action'] = self.roll_again_action
                    cell['special'] = True
                elif (row == 4 and col == 4):
                    cell['color'] = (255, 255, 255) # White
                    cell['text'] = "Trivial\nCompute"
                    cell['text_color'] = "Black"
                    cell['action'] = self.trivial_compute_action
                    cell['special'] = True
                elif ((row == 0 and col == 1) or (row == 0 and col == 5)
                      or (row == 1 and col == 4) or (row == 2 and col == 8)
                      or (row == 4 and col == 6) or (row == 5 and col == 4)
                      or (row == 6 and col == 8) or (row == 8 and col == 1)
                      or (row == 8 and col == 5)):
                    cell['color'] = (255, 255, 0) # Yellow
                elif (row == 4 and col == 0):
                    cell['color'] = (255, 255, 0) # Yellow
                    cell['text'] = "HQ"
                    cell['text_color'] = "Black"
                    cell['action'] = self.hq_action
                    cell['special'] = True
                elif ((row == 0 and col == 3) or (row == 0 and col == 7)
                      or (row == 2 and col == 0) or (row == 3 and col == 4)
                      or (row == 4 and col == 2) or (row == 6 and col == 0)
                      or (row == 7 and col == 4) or (row == 8 and col == 3)
                      or (row == 8 and col == 7)):
                    cell['color'] = (0, 255, 0) # Green
                elif (row == 4 and col == 8):
                    cell['color'] = (0, 255, 0) # Green
                    cell['text'] = "HQ"
                    cell['text_color'] = "Black"
                    cell['action'] = self.hq_action
                    cell['special'] = True
                elif ((row == 1 and col == 0) or (row == 1 and col == 8)
                      or (row == 4 and col == 3) or (row == 4 and col == 7)
                      or (row == 5 and col == 0) or (row == 5 and col == 8)
                      or (row == 6 and col == 4) or (row == 8 and col == 2)
                      or (row == 8 and col == 6)):
                    cell['color'] = (255, 0, 0) # Red
                elif (row == 0 and col == 4):
                    cell['color'] = (255, 0, 0) # Red
                    cell['text'] = "HQ"
                    cell['text_color'] = "White"
                    cell['action'] = self.hq_action
                    cell['special'] = True
                elif ((row == 0 and col == 2) or (row == 0 and col == 6)
                      or (row == 2 and col == 4) or (row == 3 and col == 0)
                      or (row == 3 and col == 8) or (row == 4 and col == 1)
                      or (row == 4 and col == 5) or (row == 7 and col == 0)
                      or (row == 7 and col == 8)):
                    cell['color'] = (0, 0, 255) # Blue
                elif (row == 8 and col == 4):
                    cell['color'] = (0, 0, 255) # Blue
                    cell['text'] = "HQ"
                    cell['text_color'] = "White"
                    cell['action'] = self.hq_action
                    cell['special'] = True
                else:
                    pass
                row_list.append(cell)
            self.grid.append(row_list)

    def draw_grid(self, p1, p2, p3, p4):
        """
        Draw the game grid.
        """
        for row in self.grid:
            for cell in row:
                pg.draw.rect(self.screen, cell['color'], cell['rect'])
                if ( # top left and top right
                    cell['id'] == "1-1" or cell['id'] == "1-2"
                    or cell['id'] == "1-3" or cell['id'] == "1-5"
                    or cell['id'] == "1-6" or cell['id'] == "1-7"
                    or cell['id'] == "2-1" or cell['id'] == "2-2"
                    or cell['id'] == "2-3" or cell['id'] == "2-5"
                    or cell['id'] == "2-6" or cell['id'] == "2-7"
                    or cell['id'] == "3-1" or cell['id'] == "3-2"
                    or cell['id'] == "3-3" or cell['id'] == "3-5"
                    or cell['id'] == "3-6" or cell['id'] == "3-7"
                    # bottom left or bottom right
                    or cell['id'] == "5-1" or cell['id'] == "5-2"
                    or cell['id'] == "5-3" or cell['id'] == "5-5"
                    or cell['id'] == "5-6" or cell['id'] == "5-7"
                    or cell['id'] == "6-1" or cell['id'] == "6-2"
                    or cell['id'] == "6-3" or cell['id'] == "6-5"
                    or cell['id'] == "6-6" or cell['id'] == "6-7"
                    or cell['id'] == "7-1" or cell['id'] == "7-2"
                    or cell['id'] == "7-3" or cell['id'] == "7-5"
                    or cell['id'] == "7-6"
                    or cell['id'] == "7-7"):
                    pass
                else:
                    pass
                
                # Render text if available
                if 'text' in cell:
                    self.render_text_to_rect(cell['text'], 30,
                                             cell['text_color'], cell['rect'])

        p1.draw(self.screen, self.center_x, self.center_y)
        p2.draw(self.screen, self.center_x, self.center_y)
        p3.draw(self.screen, self.center_x, self.center_y)
        p4.draw(self.screen, self.center_x, self.center_y)

    def get_left(self):
        return self.center_x

    def get_right(self):
        return self.center_x + (GRID_COLS * CELL_SIZE)

    def get_top(self):
        return self.center_y

    def get_bottom(self):
        return self.center_y + (GRID_ROWS * CELL_SIZE)

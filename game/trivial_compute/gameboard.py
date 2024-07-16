"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import (pg, GRID_ROWS, GRID_COLS, GRID_COLOR, CELL_SIZE,
                          BTN_W_LOC, BTN_W, BTN_H)
from components import Button, Text

class GameBoard:
    """
    GameBoard class to handle the gameboard UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.screen = self.app.screen
        self.x, self.y = (self.app.x, self.app.y)
        self.center_x = (self.x - (GRID_COLS * CELL_SIZE)) / 2
        self.center_y = (self.y - (GRID_ROWS * CELL_SIZE)) / 2
        self.text_list = [("t1", 150, "Game", "white", "title")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Question')]
        self.grid = []
    
        self.init_grid()

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def move_action(self):
        print("Move action executed")

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
                                    CELL_SIZE, CELL_SIZE)
                }
                row_list.append(cell)
            self.grid.append(row_list)

    def draw_grid(self):
        """
        Draw the game grid.
        """
        for row in self.grid:
            for cell in row:
                pg.draw.rect(self.screen, cell['color'], cell['rect'], 1)

    def handle_player_move(self, player_num, player_pos):
        """
        Handle player movement within the grid.
        """
        player_num.pos = player_pos

        row, col = player_pos
        cell = self.grid[row][col]
        cell['action']()

    def move_player(self, p1, p2, p3, p4, direction):
        p1.move(direction)
        p2.move(direction)
        p3.move(direction)
        p4.move(direction)

        self.handle_player_move(p1, p1.get_position())
        self.handle_player_move(p2, p2.get_position())
        self.handle_player_move(p3, p3.get_position())
        self.handle_player_move(p4, p4.get_position())

        self.draw(p1, p2, p3, p4)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_gameboard_ui(self, p1, p2, p3, p4):
        """
        Draw the gameboard UI, including text and buttons.
        """

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("b1", 60, 50)

        self.draw_grid()
        p1.draw(self.screen, self.center_x, self.center_y)
        p2.draw(self.screen, self.center_x, self.center_y)
        p3.draw(self.screen, self.center_x, self.center_y)
        p4.draw(self.screen, self.center_x, self.center_y)

    def check_gameboard_events(self):
        """
        Add function docstring here.
        """
        pos = pg.mouse.get_pos()
        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                button.was_clicked()
                if i[0] == "b1":
                    self.app.app.app.run_question_gui()

    def draw(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        self.draw_gameboard_ui(p1, p2, p3, p4)

"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import (pg, GRID_ROWS, GRID_COLS, GRID_COLOR, CELL_SIZE,
                          BTN_W_LOC, BTN_W, BTN_H)
from components import Button, Text
from player import Player

class GameBoard:
    """
    GameBoard class to handle the gameboard UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.win = self.app.app.screen
        self.x, self.y = (self.app.app.x, self.app.app.y)
        self.center_x = (self.x - (GRID_COLS * CELL_SIZE)) / 2
        self.center_y = (self.y - (GRID_ROWS * CELL_SIZE)) / 2
        self.text_list = [("t1", 150, "Game", "white", "title")]
        self.btn_list = [("b1", (54, 57, 63), 150, (255, 255, 255), 'Back')]
        self.grid = []
        self.player = Player(self.win)
        self.init_grid()

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[2]), (BTN_W, BTN_H), i[4]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def init_grid(self):
        for row in range(GRID_ROWS):
            row_list = []
            for col in range(GRID_COLS):
                cell = {
                    'id': f'{row}-{col}',
                    'color': GRID_COLOR,
                    'action': self.default_action,
                    'rect': pg.Rect(col * CELL_SIZE + self.center_x,
                                    row * CELL_SIZE + self.center_y,
                                    CELL_SIZE, CELL_SIZE)
                }
                row_list.append(cell)
            self.grid.append(row_list)

    def default_action(self):
        print("Default action executed")

    def draw_grid(self):
        """
        Draw the game grid.
        """
        for row in self.grid:
            for cell in row:
                pg.draw.rect(self.win, cell['color'], cell['rect'], 1)

    def handle_player_move(self, player_pos):
        """
        Handle player movement within the grid.
        """
        player_pos = self.player.get_position()
        row, col = player_pos
        cell = self.grid[row][col]
        cell['action']()

    def move_player(self, direction):
        self.player.move(direction)
        self.handle_player_move(direction)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_gameboard_ui(self):
        """
        Draw the gameboard UI, including text and buttons.
        """

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.win, i[1], i[3])

        self.set_button_position("b1", 50, 50)

        self.draw_grid()
        self.player.draw(self.center_x, self.center_y)

    def update(self):
        """
        Update the gameboard.
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(mouse_pos) and mouse_click[0]:
                self.handle_button_click(i[4])

    def handle_button_click(self, button_text):
        """
        Handle button click events.
        """
        if button_text == 'Back':
            self.app.display = "menu"

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_gameboard_ui()

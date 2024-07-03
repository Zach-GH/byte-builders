"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import pg, FIELD_W, FIELD_H, TILE_SIZE, BTN_W_LOC, BTN_W, BTN_H
from components import Button, Text

class GameBoard:
    """
    GameBoard class to handle the game board UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.win = self.app.app.screen
        self.x, self.y = (self.app.app.x, self.app.app.y)
        self.text_list = [("t1", 150, "Text 1", "black", "text1")]
        self.btn_list = [("b1", (255, 255, 0), 150, (0, 0, 0), 'Back')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[2]), (BTN_W, BTN_H), i[4]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def draw_grid(self):
        """
        Draw the game grid.
        """
        center_x = (self.x - (FIELD_W * TILE_SIZE)) / 2
        center_y = (self.y - (FIELD_H * TILE_SIZE)) / 2

        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.win, 'black', (center_x + x * TILE_SIZE,
                                                 center_y + y * TILE_SIZE,
                                                 TILE_SIZE, TILE_SIZE), 2)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_gameboard_ui(self):
        """
        Draw the game board UI, including text and buttons.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[4] == "text1":
                text.draw(1, -4)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.win, i[1], i[3])

        self.set_button_position("b1", 50, 50)

        self.draw_grid()

    def update(self):
        """
        Update the game board.
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
            self.app.mode = "menu"

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_gameboard_ui()

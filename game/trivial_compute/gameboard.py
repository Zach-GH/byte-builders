"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import (pg, GRID_ROWS, GRID_COLS, CELL_SIZE,
                          BTN_W_LOC, BTN_W, BTN_H)
from components import Button, Text

from dice import Dice
from grid import Grid

class GameBoard:
    """
    GameBoard class to handle the gameboard UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.screen = self.app.screen
        self.dice = Dice(self)
        self.x, self.y = (self.app.x, self.app.y)
        self.center_x = (self.x - (GRID_COLS * CELL_SIZE)) / 2
        self.center_y = (self.y - (GRID_ROWS * CELL_SIZE)) / 2
        self.grid = Grid(self)
        self.history_configured = False
        self.science_configured = False
        self.history_color = ""
        self.science_color = ""
        self.configured = False
        self.grid_left = self.grid.get_left()
        self.grid_right = self.grid.get_right()
        self.grid_top = self.grid.get_top()
        self.grid_bottom = self.grid.get_bottom()
        self.text_list = [("t1", 150, "History", "white", "His"),
                          ("t2", 150, "Science", "white", "Sci")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Help'),
                         ("b2", 150, (255, 255, 255), 'Q'),
                         ("b3", 150, (255, 255, 255), 'Red'),
                         ("b4", 150, (255, 255, 255), 'Yellow'),
                         ("b5", 150, (255, 255, 255), 'Blue'),
                         ("b6", 150, (255, 255, 255), 'Green')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def handle_player_move(self, player_num, player_pos):
        """
        Handle player movement within the grid.
        """
        player_num.pos = player_pos

        row, col = player_pos
        cell = self.grid.grid[row][col]
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

    def draw_configuration_ui(self):
        """
        Draw the configuration UI, including text and buttons.
        """
        for i in self.btn_list:
            if i[0] != "b1" and i[0] != "b2":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b3", self.grid_left, self.grid_top + 300)
        self.set_button_position("b4", self.grid_left + 185, self.grid_top + 300)
        self.set_button_position("b5", self.grid_left + 385, self.grid_top + 300)
        self.set_button_position("b6", self.grid_left + 585, self.grid_top + 300)

    def draw_gameboard_ui(self, p1, p2, p3, p4):
        """
        Draw the gameboard UI, including text and buttons.
        """

        for i in self.btn_list:
            if i[0] == "b1" or i[0] == "b2":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b1", self.grid_left - 165, self.grid_top)
        self.set_button_position("b2", self.grid_right + 30,
                                 self.grid_top + 150)

        self.grid.draw_grid(p1, p2, p3, p4)

    def check_gameboard_events(self):
        """
        Add function docstring here.
        """
        pos = pg.mouse.get_pos()
        if self.dice.is_clicked(pos):
            self.dice.roll_dice()
            self.dice.was_clicked()
        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                button.was_clicked()
                if i[0] == "b1":
                    print("Add logic to run Help screen")
                elif i[0] == "b2":
                    self.app.app.app.run_question_gui()
                elif i[0] == "b3":
                    if not self.history_configured:
                        print("History is Red")
                        self.history_color = "red"
                        self.history_configured = True
                    elif self.history_configured and not self.configured:
                        print("Science is Red")
                        self.science_color = "red"
                        self.configured = True
                elif i[0] == "b4":
                    if not self.history_configured:
                        print("History is Yellow")
                        self.history_color = "yellow"
                        self.history_configured = True
                    elif self.history_configured and not self.configured:
                        print("Science is Yellow")
                        self.science_color = "yellow"
                        self.configured = True
                elif i[0] == "b5":
                    if not self.history_configured:
                        print("History is Blue")
                        self.history_color = "blue"
                        self.history_configured = True
                    elif self.history_configured and not self.configured:
                        print("Science is Blue")
                        self.science_color = "blue"
                        self.configured = True
                elif i[0] == "b6":
                    if not self.history_configured:
                        print("History is Green")
                        self.history_color = "green"
                        self.history_configured = True
                    elif self.history_configured and not self.configured:
                        print("Science is Green")
                        self.science_color = "green"
                        self.configured = True

    def draw(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        if not self.configured:
            self.draw_configuration_ui()
            if not self.history_configured:
                for i in self.text_list:
                    text = getattr(self, i[0])
                    if i[0] == "t1":
                        text.draw(self.screen, 1, 0)
            elif self.history_configured and not self.configured:
                for i in self.text_list:
                    text = getattr(self, i[0])
                    if i[0] == "t2":
                        text.draw(self.screen, 1, 0)
        else:
            self.draw_gameboard_ui(p1, p2, p3, p4)
            self.dice.draw_dice(self.grid_right + 50, self.grid_top + 5, 100)

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
        """
        self.history_configured = False
        self.science_configured = False
        self.history_color = ""
        self.science_color = ""
        """
        self.all_categories =  ["History", "Science", "Geography", "Math"]
        self.phase = "categories"
        # KEYI: variables for choosing colors for categories======
        self.categories = []
        self.colors = ["red", "yellow", "blue", "green"]
        self.category_colors = {}
        self.current_category_index = 0
        self.configured = False
        # ======
        self.grid_left = self.grid.get_left()
        self.grid_right = self.grid.get_right()
        self.grid_top = self.grid.get_top()
        self.grid_bottom = self.grid.get_bottom()
        self.text_list = []
        self.btn_list = [("b1", 150, (255, 255, 255), 'Help'),
                         ("b2", 150, (255, 255, 255), 'Q'),
                         ("b3", 150, (255, 255, 255), 'Red'),
                         ("b4", 150, (255, 255, 255), 'Yellow'),
                         ("b5", 150, (255, 255, 255), 'Blue'),
                         ("b6", 150, (255, 255, 255), 'Green')]
        # KEYI:  Create a button for submitting selected categories
        self.submit_btn = Button(self, (self.center_x, self.grid_top + 500), (BTN_W, BTN_H), 'Submit')

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))



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
    # KEYI: ===================
    def draw_category_selection_ui(self):
        """
        Draw the UI for selecting categories.
        """
        font = pg.font.Font(None, 50)
        y_offset = self.grid_top + 50

        # Display instruction
        instruction_text = font.render("Select Four Categories:", True, (0, 0, 0))
        self.screen.blit(instruction_text, (self.center_x - instruction_text.get_width() // 2, y_offset))

        y_offset += 70
        # TODO: better UI button
        # Display category options
        for idx, category in enumerate(self.all_categories):

            # Create a button for each category
            category_btn = Button(self, (self.center_x + 200, y_offset + idx * 40), (BTN_W, BTN_H), category)
            setattr(self, f'category_btn_{idx}', category_btn)
            category_btn.draw(self.screen, (255, 255, 255))

    def draw_configuration_ui(self):
        """
        Draw the configuration UI, including text and buttons.
        """
        self.text_list = [("t1", 150, self.categories[0], "white", self.categories[0][:3]),
                          ("t2", 150, self.categories[1], "white", self.categories[1][:3]),
                          ("t3", 150, self.categories[2], "white", self.categories[2][:3]),
                          ("t4", 150, self.categories[3], "white", self.categories[3][:3])]
        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))
        for i in self.btn_list:
            if i[0] != "b1" and i[0] != "b2":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b3", self.grid_left, self.grid_top + 300)
        self.set_button_position("b4", self.grid_left + 185, self.grid_top + 300)
        self.set_button_position("b5", self.grid_left + 385, self.grid_top + 300)
        self.set_button_position("b6", self.grid_left + 585, self.grid_top + 300)
# ================
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
                # Keyi ==========
                # TODO: handle case user select same color
                elif i[0] in ["b3", "b4", "b5", "b6"]:
                    selected_color = i[3].lower()
                    self.category_colors[self.categories[self.current_category_index]] = selected_color
                    self.current_category_index += 1
                    if self.current_category_index >= len(self.categories):
                        self.configured = True
                    print(f"{self.categories[self.current_category_index - 1]} is {selected_color}")
                # ============
        # KEYI: select categories
        if self.phase == "categories":
            for idx, category in enumerate(self.all_categories):
                category_btn = getattr(self, f'category_btn_{idx}')
                if category_btn.is_clicked(pos):
                    # TODO: another click to unselect
                    if category not in self.categories:
                        self.categories.append(category)
                    if len(self.categories) == 4:
                        self.phase = "colors"
                        self.current_category_index = 0
                    print(f"Selected categories: {self.categories}")
    def draw(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        # KEYI: select category ui
        if self.phase == "categories":
            self.draw_category_selection_ui()
        elif not self.configured:
            self.draw_configuration_ui()
            # KEYI: select color ui ==========
            if self.current_category_index < len(self.categories) + 1:
                i = self.text_list[self.current_category_index - 1]
                text = getattr(self, i[0])
                text.draw(self.screen, 1, 0)
            # TODO: Handle later interaction after choose colors.
        else:
            self.draw_gameboard_ui(p1, p2, p3, p4)
            self.dice.draw_dice(self.grid_right + 50, self.grid_top + 5, 100)

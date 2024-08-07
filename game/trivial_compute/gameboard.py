"""
Zachary Meisner
gameboard.py

Add module docstring here
"""

from settings import (pg, GRID_ROWS, GRID_COLS, CELL_SIZE,
                          BTN_W_LOC, BTN_W, BTN_H, MOVE2)
from components import Button, Text
from beats import Sound_Effect

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
        self.history_color = ""
        self.science_color = ""
        self.geography_color = ""
        self.math_color = ""
        self.art_color = ""
        self.lit_color = ""
        self.grid = Grid(self)
        self.direction = ""
        self.all_categories =  ["History", "Science", "Geography",
                                "Math", "Art", "Literature"]
        self.phase = "categories"
        # KEYI: variables for choosing colors for categories
        # ======
        self.categories = []
        self.colors = ["red", "yellow", "blue", "green"]
        self.category_colors = {}
        self.current_category_index = 0
        self.configured = False
        self.help = False
        # ======
        self.grid_left = self.grid.get_left()
        self.grid_right = self.grid.get_right()
        self.grid_top = self.grid.get_top()
        self.grid_bottom = self.grid.get_bottom()
        self.category_list = []
        self.text_list = [("t1", 150, "Help", "white", "H")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Help'),
                         ("b3", 150, (255, 255, 255), 'Red'),
                         ("b4", 150, (255, 255, 255), 'Yellow'),
                         ("b5", 150, (255, 255, 255), 'Blue'),
                         ("b6", 150, (255, 255, 255), 'Green'),
                         ("b7", 150, (255, 255, 255), 'Back')]

        self.move_sound = Sound_Effect(self, MOVE2)
        self.move_btns = [("m1", 150, (255, 255, 255), 'Up'),
                         ("m2", 150, (255, 255, 255), 'Down'),
                         ("m3", 150, (255, 255, 255), 'Left'),
                         ("m4", 150, (255, 255, 255), 'Right')]

        # KEYI:  Create a button for submitting selected categories
        self.submit_btn = Button(self, (self.center_x, self.grid_top + 500),
                                 (BTN_W, BTN_H), 'Submit')

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.move_btns:
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
        self.direction = p1.move(direction)
        if self.direction == 'CHOOSE_UP_DOWN_LEFT_RIGHT':
            print("You must choose up down left or right")
            self.direction = 'UP'
        elif self.direction == 'CHOOSE_UP_DOWN_RIGHT':
            print("You must choose up down or right")
            self.direction = 'RIGHT'
        elif self.direction == 'CHOOSE_UP_DOWN_LEFT':
            print("You must choose up down or left")
            self.direction = 'LEFT'
        elif self.direction == 'CHOOSE_DOWN_LEFT_RIGHT':
            print("You must choose down left or right")
            self.direction = 'DOWN'
        elif self.direction == 'CHOOSE_UP_LEFT_RIGHT':
            print("You must choose up left or right")
            self.direction = 'UP'

        self.handle_player_move(p1, p1.get_position())

        self.draw(p1, p2, p3, p4)
        self.move_sound.play()
        pg.display.flip()
        pg.time.delay(500)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_help_ui(self):
        """
        Draw the help UI, including text and buttons.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[0] == "t1":
                text.draw(self.screen, 1, 0)

        for i in self.btn_list:
            if i[0] == "b7":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b7", self.grid_left - 165, self.grid_top)

    # KEYI: ===================
    def draw_category_selection_ui(self):
        """
        Draw the UI for selecting categories.
        """
        font = pg.font.Font(None, 50)
        y_offset = self.grid_top + 50

        # Display instruction
        instruction_text = font.render("Select Four Categories:", True,
                                       (255, 255, 255))
        self.screen.blit(instruction_text, (self.center_x -
                                            instruction_text.get_width()
                                            // 2, y_offset))

        y_offset += 70
        # TODO: better UI button
        # Display category options
        for idx, category in enumerate(self.all_categories):

            # Create a button for each category
            category_btn = Button(self, (self.center_x + 200, y_offset
                                         + idx * 40), (BTN_W, BTN_H), category)
            setattr(self, f'category_btn_{idx}', category_btn)
            category_btn.draw(self.screen, (255, 255, 255))

    def draw_configuration_ui(self):
        """
        Draw the configuration UI, including text and buttons.
        """
        self.category_list = [("c1", 150, self.categories[0], "white",
                                      self.categories[0][:3]),
                          ("c2", 150, self.categories[1], "white",
                                      self.categories[1][:3]),
                          ("c3", 150, self.categories[2], "white",
                                      self.categories[2][:3]),
                          ("c4", 150, self.categories[3], "white",
                                      self.categories[3][:3])]
        for i in self.category_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

        for i in self.btn_list:
            if i[0] != "b1" and i[0] != "b7":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b3", self.grid_left, self.grid_top + 300)
        self.set_button_position("b4", self.grid_left + 185,
                                 self.grid_top + 300)
        self.set_button_position("b5", self.grid_left + 385,
                                 self.grid_top + 300)
        self.set_button_position("b6", self.grid_left + 585,
                                 self.grid_top + 300)
# ================

    def draw_gameboard_ui(self, p1, p2, p3, p4):
        """
        Draw the gameboard UI, including text and buttons.
        """

        for i in self.btn_list:
            if i[0] == "b1":
                button = getattr(self, i[0])
                button.draw(self.screen, i[2])

        self.set_button_position("b1", self.grid_left - 285, self.grid_top)

        for i in self.move_btns:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("m1", self.grid_right + 30,
                                 self.grid_top + 150)
        self.set_button_position("m2", self.grid_right + 30,
                                 self.grid_top + 200)
        self.set_button_position("m3", self.grid_right + 30,
                                 self.grid_top + 250)
        self.set_button_position("m4", self.grid_right + 30,
                                     self.grid_top + 300)

        self.grid.draw_grid(p1, p2, p3, p4)

    def check_gameboard_events(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        host = p1.get_id()

        pos = pg.mouse.get_pos()
        if self.dice.is_clicked(pos):
            self.dice.roll_dice()
            self.dice.was_clicked()

        for cell_rect in self.grid.special_cells:
            if cell_rect.collidepoint(pos):
                for row in self.grid.grid:
                    for cell in row:
                        if cell['rect'] == cell_rect:
                            cell['action']()
                            break

        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                # # button.was_clicked()
                if i[0] == "b1":
                    self.help = True
                # Keyi ==========
                # TODO: handle case user select same color
                elif i[0] in ["b3", "b4", "b5", "b6"]:
                    selected_color = i[3].lower()
                    if self.current_category_index < len(self.categories):
                        category = self.categories[self.current_category_index]
                        self.category_colors[category] = selected_color
                        if category == "History":
                            self.history_color = selected_color
                            print("history color is", self.history_color)
                        elif category == "Science":
                            self.science_color = selected_color
                            print("science_color is", self.science_color)
                        elif category == "Geography":
                            self.geography_color = selected_color
                            print("geography color is", self.geography_color)
                        elif category == "Math":
                            self.math_color = selected_color
                            print("math color is", self.math_color)
                        elif category == "Art":
                            self.art_color = selected_color
                            print("art color is", self.art_color)
                        elif category == "Literature":
                            self.lit_color = selected_color
                            print("lit color is", self.lit_color)
                        self.current_category_index += 1
                        if self.current_category_index >= len(self.categories):
                            self.configured = True
                            p1.set_configured()
                            p2.set_configured()
                            p3.set_configured()
                            p4.set_configured()
                elif i[0] == "b7":
                    self.help = False

        for i in self.move_btns:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                # # button.was_clicked()
                if i[0] == "m1":
                    move_num = self.dice.get_num()
                    self.direction = 'UP'
                    for _ in range(move_num):
                        self.move_player(p1, p2, p3, p4, self.direction)
                        if (self.direction == 'CHOOSE_UP_DOWN_LEFT_RIGHT'
                            or 'CHOOSE_UP_LEFT_RIGHT'
                            or 'CHOOSE_UP_DOWN_RIGHT'
                            or 'CHOOSE_UP_DOWN_LEFT'):
                            print("Special UP move")
                    print("p1 after", p1.get_position())
                elif i[0] == "m2":
                    move_num = self.dice.get_num()
                    print("move_num is", move_num)
                    print("p1 pos", p1.get_position())
                    self.direction = 'DOWN'
                    for _ in range(move_num):
                        self.move_player(p1, p2, p3, p4, self.direction)
                        if (self.direction == 'CHOOSE_UP_DOWN_LEFT_RIGHT'
                            or 'CHOOSE_UP_DOWN_RIGHT'
                            or 'CHOOSE_UP_DOWN_LEFT'
                            or 'CHOOSE_DOWN_LEFT_RIGHT'):
                            print("Special DOWN move")
                    print("p1 after", p1.get_position())
                elif i[0] == "m3":
                    move_num = self.dice.get_num()
                    print("move_num is", move_num)
                    print("p1 pos", p1.get_position())
                    self.direction = 'LEFT'
                    for _ in range(move_num):
                        self.move_player(p1, p2, p3, p4, self.direction)
                        if (self.direction == 'CHOOSE_UP_DOWN_LEFT_RIGHT'
                            or 'CHOOSE_UP_DOWN_LEFT'
                            or 'CHOOSE_UP_LEFT_RIGHT'
                            or 'CHOOSE_DOWN_LEFT_RIGHT'):
                            print("special LEFT move")
                    print("p1 after", p1.get_position())
                elif i[0] == "m4":
                    move_num = self.dice.get_num()
                    print("move_num is", move_num)
                    print("p1 pos", p1.get_position())
                    self.direction = 'RIGHT'
                    for _ in range(move_num):
                        self.move_player(p1, p2, p3, p4, self.direction)
                        if (self.direction == 'CHOOSE_UP_DOWN_LEFT_RIGHT'
                            or 'CHOOSE_UP_DOWN_RIGHT'
                            or 'CHOOSE_UP_LEFT_RIGHT'
                            or 'CHOOSE_DOWN_LEFT_RIGHT'):
                            print("Special RIGHT move")
                    print("p1 after", p1.get_position())

        if host == 1 and not self.configured:
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
                        button.choose_category()

    def update_player_name(self, player_num, pName):
        """
        Update player name accurately.
        """
        player_num.name = pName

    def set_player_name(self, player_num):
        """
        Add function docstring here.
        """
        player_num.set_name(self.app.user_text)

        self.update_player_name(player_num, player_num.get_name())

    def draw(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        host = p1.get_id()
        if host == 1:
            self.configured = p1.get_configured()

        # KEYI: select category ui
        if not self.configured and host == 1 and self.phase == "categories":
            self.draw_category_selection_ui()
        elif not self.configured and host == 1:
            self.draw_configuration_ui()
            # KEYI: select color ui ==========
            if self.current_category_index < len(self.categories):
                i = self.category_list[self.current_category_index]
                text = getattr(self, i[0])
                text.draw(self.screen, 1, 0)
            # TODO: Handle later interaction after choose colors.
        elif (self.help):
            self.draw_help_ui()
        else:
            self.draw_gameboard_ui(p1, p2, p3, p4)
            self.dice.draw_dice(self.grid_right + 50, self.grid_top + 5, 100)

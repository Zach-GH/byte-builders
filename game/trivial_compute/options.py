"""
Zachary Meisner
options.py

Add module docstring here
"""

from settings import pg, BTN_W_LOC, BTN_W, BTN_H
from components import Button, Text

class Options:
    """
    Options class to handle the options UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.win = self.app.app.screen
        self.x, self.y = (self.app.app.x, self.app.app.y)
        self.text_list = [("t1", 150, "Options", "white", "title")]
        self.btn_list = [("b1", (54, 57, 63), 150, (255, 255, 255), 'Back')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[2]), (BTN_W, BTN_H), i[4]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_options_ui(self):
        """
        Draw the options UI, including text and buttons.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[4] == "title":
                text.draw(1, 0)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.win, i[1], i[3])

        self.set_button_position("b1", 50, 50)


    def update(self):
        """
        Update the Options menu.
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
        self.draw_options_ui()

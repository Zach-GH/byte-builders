"""
Zachary Meisner
trophies.py

Add module docstring here
"""

from settings import pg, BTN_W_LOC, BTN_W, BTN_H
from components import Button, Text

class Trophies:
    """
    Trophies class to handle the trophies UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.screen = self.app.app.screen
        self.x, self.y = (self.app.app.x, self.app.app.y)
        self.text_list = [("t1", 150, "Trophies", "white", "title")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Back')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_trophies_ui(self):
        """
        Draw the trophies UI, including text and buttons.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[4] == "title":
                text.draw(self.screen, 1, 0)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("b1", 50, 50)

    def handle_button_click(self, button_text):
        """
        Handle button click events.
        """
        if button_text == 'Back':
            self.app.display = "menu"

    def update(self):
        """
        Update the Trophies menu.
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(mouse_pos) and mouse_click[0]:
                button.was_clicked()
                self.handle_button_click(i[3])

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_trophies_ui()

"""
Zachary Meisner
menu.py

Add module docstring here
"""

from settings import pg, MENU_BG_PATH, BTN_W_LOC, BTN_W, BTN_H
from components import Button, Text

class Menu:
    """
    Add class docstring here.
    """
    def __init__(self, app):
        self.app = app
        self.res = (self.x, self.y) = (self.app.app.x, self.app.app.y)
        self.bg_img = pg.image.load(MENU_BG_PATH)
        self.text_list = [("t1", 150, "Trivial Compute", "black", "title"),
                          ("t2", 80, "Team Byte-Builders", "black", "team")]
        self.btn_list = [("b1", (255, 255, 0), 350, (0, 0, 0), 'Play'),
                         ("b2", (255, 0, 0), 350, (0, 0, 0), 'Options'),
                         ("b3", (255, 0, 0), 350, (0, 0, 0), 'Mute'),
                         ("b4", (255, 0, 0), 350, (0, 0, 0), 'Achievements'),
                         ("b5", (0, 255, 0), 350, (0, 0, 0), 'Credits'),
                         ("b6", (0, 255, 0), 350, (0, 0, 0), 'Quit')]

        # Create the buttons on the main menu
        j = 0
        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[2] + j), (BTN_W, BTN_H), i[4]))
            j += 75

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def draw_menu(self):
        """
        Add function docstring here.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[4] == "title":
                text.draw(1, 0)
            elif i[4] == "team":
                text.draw(1.9, 1.9)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.app.app.screen, i[1], i[3])

    def update(self):
        """
        Add function docstring here.
        """
        pg.display.update()

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_menu()

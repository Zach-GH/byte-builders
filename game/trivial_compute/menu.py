"""
Zachary Meisner
menu.py

Add module docstring here
"""

from settings import pg, MENU_BG_PATH, BTN_W_LOC, BTN_W, BTN_H, MENU_MUSIC
from components import Button, Text
from beats import Beats

class Menu:
    """
    Add class docstring here.
    """
    def __init__(self, app):
        self.app = app
        self.screen = self.app.app.screen
        self.res = (self.x, self.y) = (self.app.app.x, self.app.app.y)
        self.bg_img = pg.image.load(MENU_BG_PATH)
        self.beats = Beats(self, MENU_MUSIC, 5000)
        self.text_list = [("t1", 150, "Trivial Compute", "white", "title"),
                          ("t2", 80, "Team Byte-Builders", "white", "team")]
        self.btn_list = [("b1", 175, (255, 255, 255), 'Play'),
                         ("b2", 175, (255, 255, 255), 'Options'),
                         ("b3", 175, (255, 255, 255), 'Mute'),
                         ("b4", 175, (255, 255, 255), 'Host'),
                         ("b5", 175, (255, 255, 255), 'Team'),
                         ("b6", 175, (255, 255, 255), 'Quit')]

        if (self.app.mute == False):
            self.beats.start_music()

        # Create the buttons on the main menu
        j = 0
        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1] + j), (BTN_W, BTN_H), i[3]))
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
                text.draw(self.screen, 1, 0)
            elif i[4] == "team":
                text.draw(self.screen, 1.9, 1.9)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.app.app.screen, i[2])

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

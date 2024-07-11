"""
Madeline Gyllenhoff
question_gui.py

Add module docstring here
"""

import sys
from settings import pg, BTN_W_LOC, BTN_W, BTN_H, MENU_MUSIC
from components import Button, Text

res_type = pg.RESIZABLE

# class MenuBeats:
#     """
#     Add class docstring here.
#     """
#     def __init__(self, app):
#         self.app = app
#         self.music = MENU_MUSIC
#         self.fade_in = 5000

#         # Load music during initialization
#         pg.mixer.music.load(MENU_MUSIC)

#     def is_playing(self):
#         """
#         Add function docstring here.
#         """
#         return pg.mixer.music.get_busy()

#     def start_music(self):
#         """
#         Add function docstring here.
#         """
#         pg.mixer.music.play(-1, fade_ms=self.fade_in)

#     def stop_music(self):
#         """
#         Add function docstring here.
#         """
#         pg.mixer.music.stop()


class Question_Gui:
    """
    Question_Gui class to handle the options UI and interactions.
    """
    def __init__(self, app):
        self.app = app
        self.win = self.app.app.screen
        self.x, self.y = (self.app.app.x, self.app.app.y)
        self.text_list = [("t1", 150, "Question_Gui", "white", "title")]
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
            button.draw(self.win, i[2])

        self.set_button_position("b1", 50, 50)

    def handle_button_click(self, button_text):
        """
        Handle button click events.
        """
        pass
        # if button_text == 'Back':
        #     self.app.display = "menu"

    def update(self):
        """
        Update the Question_Gui menu.
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(mouse_pos) and mouse_click[0]:
                self.handle_button_click(i[3])

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_options_ui()

    def check_events(self):
        """
        Add function docstring here.
        """
        for event in pg.event.get():
            if (event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                          and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()

    def run(self):
        """
        Add function docstring here.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()
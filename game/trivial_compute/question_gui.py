"""
Madeline Gyllenhoff
question_gui.py

Add module docstring here
"""

import sys
from settings import (pg, QGUI_RES, FPS, BTN_W_LOC, BTN_W, BTN_H, QGUI_COLOR,
                      CLICK, FUN)
from components import Button, Text
from beats import Beats

resolution = QGUI_RES
res_type = pg.RESIZABLE

class Question_Gui:
    """
    Question_Gui class to handle the question_gui UI and interactions.
    """
    def __init__(self, app):
        pg.init()
        pg.display.set_caption('Byte-Builders Question GUI')
        self.app = app
        # self.beats = Beats(self, CLICK, 0)
        self.beats = Beats(self, FUN, 0)
        self.screen = pg.display.set_mode(resolution, res_type)
        self.res = (self.x, self.y) = self.screen.get_size()
        self.clock = pg.time.Clock()
        self.text_list = [("t1", 150, "Question_Gui", "white", "title")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'The :) Button')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.btn_list:
            button = getattr(self, i[0])
            if i[3] == "The :) Button":
                button.update_size((50, 50))
        
        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def check_question_gui_events(self, pos):
        """
        Add function docstring here.
        """
        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                if i[3] == "The :) Button":
                    if self.beats.is_playing():
                        pass
                    else:
                        self.beats.sound_effect()

    def check_events(self):
        """
        Add function docstring here.
        """
        for event in pg.event.get():
            if (event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                          and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    self.check_question_gui_events(pos)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_question_gui_ui(self):
        """
        Draw the question_gui UI, including text and buttons.
        """
        self.screen.fill(color=QGUI_COLOR)

        for i in self.text_list:
            text = getattr(self, i[0])
            if i[4] == "title":
                text.draw(self.screen, 1, 0)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("b1", 225, 200)
        pg.display.flip()

    def handle_button_click(self, button_text):
        """
        Handle button click events.
        """
        if button_text == 'The :) Button':
            print("Shrek 5 was confirmed the other day!")

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

        self.clock.tick(FPS)

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_question_gui_ui()

    def run(self):
        """
        Add function docstring here.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()

"""
Madeline Gyllenhoff
question_gui.py

Add module docstring here
"""

import sys
from settings import (pg, QGUI_RES, FPS, BTN_W_LOC, BTN_W, BTN_H, QGUI_COLOR)
from components import Button, Text
from run_sql_query import run_sql_query

resolution = QGUI_RES
res_type = pg.RESIZABLE

def run_question_gui_instance(question_type):
    pg.init()
    screen = pg.display.set_mode(resolution, res_type)
    pg.display.set_caption('Byte-Builders Question GUI')
    question_gui = Question_Gui(screen, question_type)
    question_gui.run()

class Question_Gui:
    """
    Question_Gui class to handle the question_gui UI and interactions.
    """
    def __init__(self, screen=None, question=None):
        pg.init()
        pg.display.set_caption('Byte-Builders Question GUI')
        self.screen = screen or pg.display.set_mode(resolution, res_type)
        self.res = (self.x, self.y) = self.screen.get_size()
        self.clock = pg.time.Clock()
        self.current_question = {}
        self.next_id = 1
        self.question_type = question
        self.show_answer = False
        self.text_list = [("t1", 125, "Question_Gui", "white", "title"),
                          ("t2", 60, "?", "white", "question")]
        self.btn_list = [("b1", 0, (255, 255, 255), 'Reveal')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                              i[1]), (BTN_W, BTN_H), i[3]))

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.update_size((35, 35))

        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def check_question_gui_events(self, pos):
        """
        Handles the events triggered by GUI buttons related to questions.

        Parameters:
        - pos: Tuple[int, int]: The position where the mouse click occurred.
        """
        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                # button.was_clicked()
                # Needs to call for an answer instead
                question_id = self.next_id
                result = run_sql_query(self.question_type)
                for question, answer in result:
                    self.current_question[question_id] = (question, answer)
                first_question = 1
                first_question = self.current_question.get(first_question, None)
                for i in self.text_list:
                    text = getattr(self, i[0])
                    if i[0] == "t2":
                        if self.show_answer == False:
                            self.show_answer = True
                        else:
                            self.show_answer = False

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
            elif i[4] == "question":
                text.draw(self.screen, 0, 1.5)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("b1", 265, 150)

        # Call for database question
        question_id = self.next_id
        result = run_sql_query(self.question_type)
        for question, answer in result:
            self.current_question[question_id] = (question, answer)
        first_question = 1
        first_question = self.current_question.get(first_question, None)
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[0] == "t2":
                if self.show_answer == True:
                    text.update_text(f"{first_question[1]}")
                    text.draw(self.screen, 0, 1.5)
                else:
                    text.update_text(f"{first_question[0]}")
                    text.draw(self.screen, 0, 1.5)

        pg.display.flip()

    def update(self):
        """
        Update the Question_Gui menu.
        """
        self.check_events()
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
            self.update()
            self.draw()

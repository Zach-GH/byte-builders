#!/usr/bin/env python3

"""
Zachary Meisner
main.py

Provides a basic interface for players to interact with.
Creates the initial pygame framework in which the screen and main game loop
are established.  This interface will primarily interact with the settings.py
file in addition to the trivial_compute.py file which will house core logic.
"""

import sys
import multiprocessing as mp
from settings import (pg, MAX_WIN_RES, MED_WIN_RES, MIN_WIN_RES, FPS,
                          MENU_COLOR, OPTIONS_COLOR, HOST_COLOR,
                          TEAM_COLOR, QGUI_RES)
from waiting_room import WaitingRoom
from menu import Menu
from options import Options
from host import Host
from team import Team
from question_gui import Question_Gui, run_question_gui_instance
from database import Database
from net.server import Server

resolution = MIN_WIN_RES
res_type = pg.FULLSCREEN
game_display = "menu"
mute = False
server = False
q_gui = False
q_database = False
dev = False

A = 1
n = len(sys.argv)
while A < n:
    if (sys.argv[A] == "-r" and A + 1 < n):
        res = sys.argv[A + 1].lower()
        if res == "max":
            resolution = MAX_WIN_RES
        elif res == "med":
            resolution = MED_WIN_RES
        elif res == "min":
            resolution = MIN_WIN_RES
        A += 1
    elif (sys.argv[A] == "-t" and A + 1 < n):
        type_ = sys.argv[A + 1].lower()
        if type_ == "full":
            res_type = pg.FULLSCREEN
        elif type_ == "sized":
            res_type = pg.RESIZABLE
        elif type_ == "windowed":
            res_type = pg.NOFRAME
        A += 1
    elif (sys.argv[A] == "-d" and A + 1 < n):
        display = sys.argv[A + 1].lower()
        if display in ["menu", "waitingroom", "options", "host", "team"]:
            game_display = display
        A += 1
    elif (sys.argv[A] == "-dev"):
        dev = True
    elif (sys.argv[A] == "-m"):
        mute = True
    elif (sys.argv[A] == "-s"):
        server = True
        A += 1
    elif (sys.argv[A] == "-g"):
        q_gui = True
        A += 1
    elif (sys.argv[A] == "-db"):
        q_database = True
        A += 1
    A += 1


class Game:
    """
    Add class docstring here.
    """
    def __init__(self, app):
        self.app = app
        self.dev = dev
        self.display = game_display
        self.mute = mute
        self.nav = {
            'menu': Menu(self),
            'waitingroom': WaitingRoom(self),
            'options': Options(self),
            'host': Host(self),
            'team': Team(self)
        }
        self.scale = pg.transform.scale(self.nav['menu'].bg_img,
                                        self.app.res)

    def check_action_events(self, pos):
        """
        Add function docstring here.
        """
        if self.display == "menu":
            for i in self.nav['menu'].btn_list:
                button = getattr(self.nav['menu'], i[0])
                if button.is_clicked(pos):
                    button.was_clicked()
                    if i[3] == "Play":
                        self.display = "waitingroom"
                    elif i[3] == "Options":
                        self.display = "options"
                    elif i[3] == "Mute":
                        if self.mute == False:
                            self.mute = True
                        else:
                            self.mute = False
                        if (self.nav['menu'].beats.is_playing()
                            and self.mute == True):
                            self.nav['menu'].beats.stop_music()
                        elif (not self.nav['menu'].beats.is_playing()
                              and self.mute == False):
                            self.nav['menu'].beats.start_music()
                    elif i[3] == "Host":
                        self.display = "host"
                    elif i[3] == "Team":
                        self.display = "team"
                    elif i[3] == "Quit":
                        pg.quit()
                        sys.exit()

    def check_resize(self, event):
        """
        Add function docstring here.
        """
        if self.display == "menu":
            self.nav['scale'] = pg.transform.scale(self.nav['menu'].bg_img,
                                                   (event.w, event.h))


class App:
    """
    Add class docstring here.
    """
    def __init__(self):
        pg.init()
        pg.display.set_caption('Byte-Builders Trivial Compute')
        self.screen = pg.display.set_mode(resolution, res_type)
        self.res = (self.x, self.y) = self.screen.get_size()
        self.clock = pg.time.Clock()
        self.game = Game(self)
        self.server = Server(self)

    def update(self):
        """
        Add function docstring here.
        """
        if self.game.display == "menu":
            self.game.nav['menu'].update()
        elif self.game.display == "waitingroom":
            self.game.nav['waitingroom'].update()
        elif self.game.display == "options":
            self.game.nav['options'].update()
        elif self.game.display == "host":
            self.game.nav['host'].update()
        elif self.game.display == "team":
            self.game.nav['team'].update()
        self.clock.tick(FPS)

    def draw(self):
        """
        Add function docstring here.
        """
        if self.game.display == "menu":
            self.screen.fill(color=MENU_COLOR)
            self.game.nav['menu'].bg_img = self.game.scale
            self.screen.blit(self.game.nav['menu'].bg_img, (0, 0))
            self.game.nav['menu'].draw()
            pg.display.flip()
        elif self.game.display == "waitingroom":
            self.screen.fill(color=MENU_COLOR)
            self.game.nav['waitingroom'].draw()
            pg.display.flip()
        elif self.game.display == "options":
            self.screen.fill(color=OPTIONS_COLOR)
            self.game.nav['options'].draw()
            pg.display.flip()
        elif self.game.display == "host":
            self.screen.fill(color=HOST_COLOR)
            self.game.nav['host'].draw()
            pg.display.flip()
        elif self.game.display == "team":
            self.screen.fill(color=TEAM_COLOR)
            self.game.nav['team'].draw()
            pg.display.flip()

    def check_events(self):
        """
        Add function docstring here.
        """
        for event in pg.event.get():
            if (event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                          and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            elif (event.type == pg.KEYDOWN):
                if self.game.nav['waitingroom'].active:
                    if event.key == pg.K_BACKSPACE:
                        self.game.nav['waitingroom'].user_text = self.game.nav['waitingroom'].user_text[:-1]
                    else:
                        self.game.nav['waitingroom'].user_text += event.unicode
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.game.display == "waitingroom":
                    self.game.nav['waitingroom'].handle_button_click(pos)
                    if self.game.nav['waitingroom'].input_rect.collidepoint(event.pos):
                        self.game.nav['waitingroom'].active = True
                    else:
                        self.game.nav['waitingroom'].active = False
                else:
                    self.game.check_action_events(pos)
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), res_type)
                self.game.check_resize(event)

    def run_external_gui(self, target, process_attribute):
        current_process = getattr(self, process_attribute, None)
        if current_process is None or not current_process.is_alive():
            process = mp.Process(target=target)
            process.start()
            setattr(self, process_attribute, process)
        else:
            print("You can't open two windows!")

    def run_server(self):
        """
        Add function docstring here.
        """
        self.run_external_gui(self.server.run, 'server_process')

    def run_question_gui(self):
        """
        Add function docstring here.
        """
        self.run_external_gui(run_question_gui_instance, 'question_gui_process')

    def run(self):
        """
        Add function docstring here.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()


class RunServer:
    """
    Add class docstring here.
    """
    def __init__(self):
        self.server = Server(self)

    def run(self):
        print("Running Trivial Compute Server")
        self.server.run()

class Run_Question_Gui:
    """
    Add class docstring here.
    """
    def __init__(self):
        screen = pg.display.set_mode(QGUI_RES, pg.RESIZABLE)
        self.question_gui = Question_Gui(screen)

    def run(self):
        print("Running Trivial Compute Quesiton Gui")
        self.question_gui.run()

class Run_Database:
    """
    Add class docstring here.
    """
    def __init__(self):
        self.database = Database(self)

    def run(self):
        print("Running Trivial Compute Database")
        self.database.run()

if __name__ == '__main__':
    if (server == True):
        s = RunServer()
        s.run()
    elif (q_gui == True):
        g = Run_Question_Gui()
        g.run()
    elif (q_database == True):
        d = Run_Database()
        d.run()
    else:
        a = App()
        a.run()

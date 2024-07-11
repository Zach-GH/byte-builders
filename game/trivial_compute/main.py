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
from settings import (pg, MAX_WIN_RES, MED_WIN_RES, MIN_WIN_RES, FPS,
                          MENU_COLOR, OPTIONS_COLOR, TROPHIES_COLOR,
                          TEAM_COLOR)
from waiting_room import WaitingRoom
from menu import Menu
from options import Options
from trophies import Trophies
from team import Team
from question_gui import Question_Gui
from net.server import Server

resolution = MIN_WIN_RES
res_type = pg.FULLSCREEN
game_display = "menu"
mute = False
server = False
q_gui = False

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
        if display in ["menu", "waitingroom", "options", "trophies", "team"]:
            game_display = display
        A += 1
    elif (sys.argv[A] == "-m"):
        mute = True
        A += 1
    elif (sys.argv[A] == "-s"):
        server = True
        A += 1
    elif (sys.argv[A] == "-g"):
        q_gui = True
        A += 1
    A += 1


class Game:
    """
    Add class docstring here.
    """
    def __init__(self, app):
        self.app = app
        self.display = game_display
        self.mute = mute
        self.nav = {
            'menu': Menu(self),
            'waitingroom': WaitingRoom(self),
            'options': Options(self),
            'trophies': Trophies(self),
            'team': Team(self)
        }
        self.scale = pg.transform.scale(self.nav['menu'].bg_img,
                                        self.app.res)

    def check_menu_events(self, pos):
        """
        Add function docstring here.
        """
        if self.display == "menu":
            for i in self.nav['menu'].btn_list:
                button = getattr(self.nav['menu'], i[0])
                if button.area.get_rect(topleft=button.pos).collidepoint(pos):
                    if i[3] == "Play":
                        self.display = "waitingroom"
                    elif i[3] == "Options":
                        self.display = "options"
                    elif i[3] == "Mute":
                        if self.mute == False:
                            self.mute = True
                        else:
                            self.mute = False
                        if self.nav['menu'].beats.is_playing() and self.mute == True:
                            self.nav['menu'].beats.stop_music()
                        elif not self.nav['menu'].beats.is_playing() and self.mute == False:
                            self.nav['menu'].beats.start_music()
                    elif i[3] == "Trophies":
                        self.display = "trophies"
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
        elif self.game.display == "trophies":
            self.game.nav['trophies'].update()
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
        elif self.game.display == "trophies":
            self.screen.fill(color=TROPHIES_COLOR)
            self.game.nav['trophies'].draw()
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
            elif event.type == pg.MOUSEBUTTONUP:
                if self.game.display == "waitingroom":
                    self.game.nav['waitingroom'].allowUpdate()
                else:
                    pos = pg.mouse.get_pos()
                    self.game.check_menu_events(pos)
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), res_type)
                self.game.check_resize(event)

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
        self.question_gui = Question_Gui(self)

    def run(self):
        print("Running Trivial Compute Quesiton Gui")
        self.question_gui.run()

if __name__ == '__main__':
    if (server == True):
        s = RunServer()
        s.run()
    elif (q_gui == True):
        g = Run_Question_Gui()
        g.run()
    else:
        a = App()
        a.run()

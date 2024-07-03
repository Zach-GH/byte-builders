#!/usr/bin/env python

"""
Zachary Meisner
main.py

Provides a basic interface for players to interact with.
Creates the initial pygame framework in which the screen and main game loop
are established.  This interface will primarily interact with the settings.py
file in addition to the trivial_compute.py file which will house core logic.
"""

import sys
from settings import pg, MAX_WIN_RES, MED_WIN_RES, MIN_WIN_RES, FPS, FIELD_COLOR
from gameboard import GameBoard
from menu import Menu

resolution = MIN_WIN_RES
res_mode = pg.FULLSCREEN

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
    elif (sys.argv[A] == "-m" and A + 1 < n):
        mode = sys.argv[A + 1].lower()
        if mode == "full":
            res_mode = pg.FULLSCREEN
        elif mode == "sized":
            res_mode = pg.RESIZABLE
        elif mode == "windowed":
            res_mode = pg.NOFRAME
        A += 1
    A += 1


class Game:
    """
    Add class docstring here.
    """
    def __init__(self, app):
        self.app = app
        self.mode = "menu"
        self.menu = Menu(self)
        self.scale = pg.transform.scale(self.menu.bg_img, self.app.res)
        self.gameboard = GameBoard(self)

    def check_menu_events(self, pos):
        """
        Add function docstring here.
        """
        if self.mode == "menu":
            for i in self.menu.btn_list:
                button = getattr(self.menu, i[0])
                if button.area.get_rect(topleft=button.pos).collidepoint(pos):
                    if i[4] == "Play":
                        self.mode = "play"
                    elif i[4] == "Options":
                        print(f"{i[4]} was clicked!")
                    elif i[4] == "Mute":
                        print(f"{i[4]} was clicked!")
                    elif i[4] == "Achievements":
                        print(f"{i[4]} was clicked!")
                    elif i[4] == "Credits":
                        print(f"{i[4]} was clicked!")
                    elif i[4] == "Quit":
                        pg.quit()
                        sys.exit()

    def check_resize(self, event):
        """
        Add function docstring here.
        """
        if self.mode == "menu":
            self.scale = pg.transform.scale(self.menu.bg_img,
                                            (event.w, event.h))
        elif self.mode == "play":
            # sizable image background
            pass


class App:
    """
    Add class docstring here.
    """
    def __init__(self):
        pg.init()
        pg.display.set_caption('Byte-Builders Trivial Compute')
        self.screen = pg.display.set_mode(resolution, res_mode)
        self.res = (self.x, self.y) = self.screen.get_size()
        self.clock = pg.time.Clock()
        self.game = Game(self)

    def update(self):
        """
        Add function docstring here.
        """
        if self.game.mode == "menu":
            self.game.menu.update()
        elif self.game.mode == "play":
            self.game.gameboard.update()
        self.clock.tick(FPS)

    def draw(self):
        """
        Add function docstring here.
        """
        if self.game.mode == "menu":
            self.screen.fill(color=FIELD_COLOR)
            self.game.menu.bg_img = self.game.scale
            # Menu background goes here image spans entire screen.
            # self.screen.blit(self.menu.bg_img, (0, 0))
            self.game.menu.draw()
            pg.display.flip()
        elif self.game.mode == "play":
            self.screen.fill(color=FIELD_COLOR)
            self.game.gameboard.draw()
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
                pos = pg.mouse.get_pos()
                self.game.check_menu_events(pos)
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), res_mode)
                self.game.check_resize(event)

    def run(self):
        """
        Add function docstring here.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    a = App()
    a.run()

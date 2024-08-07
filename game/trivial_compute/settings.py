"""
Zachary Meisner
settings.py

Provides settings that dictate parameters for different types of screens,
values, resources, events, etc. that are needed by the game during runtime.
"""

import pygame as pg # type: ignore # pylint: disable=unused-import
import pygame.freetype as ft # type: ignore # pylint: disable=unused-import
import os

FPS = 90
MENU_COLOR =     (40, 40, 40)
PLAY_COLOR =     (40, 40, 40)
TEAM_COLOR =     (40, 40, 40)
OPTIONS_COLOR =  (40, 40, 40)
HOST_COLOR = (40, 40, 40)
QGUI_COLOR =     (40, 40, 40)
DGUI_COLOR =     (40, 40, 40)

# Intended for dice.
WHITE =     (255, 255, 255)
BLACK =     (0, 0, 0)

FPATH = os.path.join("assets", "font", "balmoral.ttf")
FONT_PATH = os.path.realpath(FPATH)

BG_PATH = os.path.join("assets", "sprites", "game-show.png")
MENU_BG_PATH = os.path.realpath(BG_PATH)

# https://archive.org/details/AllStar
SPATH = os.path.join("assets", "sounds", "SmashMouth-AllStar.mp3")
FUN= os.path.realpath(SPATH)

# https://www.youtube.com/watch?v=JiS3D0bo-eM
MPATH = os.path.join("assets", "sounds",
                     "Trivial_Pursuit_CD_ROM_Edition_(1997_Soundtrack).mp3")
MENU_MUSIC= os.path.realpath(MPATH)

# https://opengameart.org/content/menu-selection-click
CPATH = os.path.join("assets", "sounds", "Click.wav")
CLICK= os.path.realpath(CPATH)

# https://pixabay.com/sound-effects/dice-142528/
CPATH = os.path.join("assets", "sounds", "Dice.mp3")
DICE= os.path.realpath(CPATH)

# https://pixabay.com/sound-effects/wooden-thud-mono-6244/
MOVE_PATH = os.path.join("assets", "sounds", "wood-thud.mp3")
MOVE= os.path.realpath(MOVE_PATH)

# https://pixabay.com/sound-effects/stone-dropping-6843/
MOVE_PATH2 = os.path.join("assets", "sounds", "stone-drop.mp3")
MOVE2= os.path.realpath(MOVE_PATH2)

# https://pixabay.com/sound-effects/closing-book-88041/
BOOK_PATH = os.path.join("assets", "sounds", "close-book.mp3")
BOOK= os.path.realpath(BOOK_PATH)

CELL_SIZE = 90
GRID_SIZE = GRID_ROWS, GRID_COLS = 9, 9
GRID_RES = GRID_ROWS * CELL_SIZE, GRID_COLS * CELL_SIZE
GRID_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

BTN_H = 50
BTN_W = 150
BTN_W_LOC = BTN_W / 2

GRID_SCALE_W, GRID_SCALE_H = 1.7, 1.0

MAX_WIN_RES = (MAX_WIN_W, MAX_WIN_H) = (3840, 2160)
MED_WIN_RES = (MED_WIN_W, MED_WIN_H) = (2560, 1440)
MIN_WIN_RES = (MIN_WIN_W, MIN_WIN_H) = (1920, 1080)

QGUI_RES = (MIN_WIN_W, MIN_WIN_H) = (600, 400)
DGUI_RES = (MIN_WIN_W, MIN_WIN_H) = (1000, 1000)

WIN_RES = (WIN_W, WIN_H) = (GRID_RES[0] * GRID_SCALE_W,
                            GRID_RES[1] * GRID_SCALE_H)

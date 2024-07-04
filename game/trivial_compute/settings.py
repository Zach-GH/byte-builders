"""
Zachary Meisner
settings.py

Provides settings that dictate parameters for different types of screens,
values, resources, events, etc. that are needed by the game during runtime.
"""

import pygame as pg # type: ignore # pylint: disable=unused-import
import pygame.freetype as ft # type: ignore # pylint: disable=unused-import

FPS = 60
MENU_COLOR =    (40, 40, 40)
PLAY_COLOR =    (40, 40, 40)
OPTIONS_COLOR = (40, 40, 40)
ACHVM_COLOR =   (40, 40, 40)
CREDITS_COLOR = (40, 40, 40)

MENU_BG_PATH = "assets/sprites/game-show.png"

TILE_SIZE = 90
FIELD_SIZE = FIELD_W, FIELD_H = 9, 9
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE
FW_CENTER = FIELD_W * TILE_SIZE / 2
FH_CENTER = FIELD_H * TILE_SIZE / 2

BTN_H = 50
BTN_W = 150
BTN_W_LOC = BTN_W / 2

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0

MAX_WIN_RES = (MAX_WIN_W, MAX_WIN_H) = (3840, 2160)
MED_WIN_RES = (MED_WIN_W, MED_WIN_H) = (2560, 1440)
MIN_WIN_RES = (MIN_WIN_W, MIN_WIN_H) = (1920, 1080)

WIN_RES = (WIN_W, WIN_H) = (FIELD_RES[0] * FIELD_SCALE_W,
                            FIELD_RES[1] * FIELD_SCALE_H)

FONT_PATH = 'assets/font/balmoral.ttf'

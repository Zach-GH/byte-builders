"""
Zachary Meisner
dice.py

Add module docstring here
"""

from settings import pg, WHITE, BLACK, DICE
from beats import Sound_Effect
import random

class Dice:
    """
    Dice class to handle dice things.
    """
    def __init__(self, app):
        self.app = app
        self.win = self.app.screen
        # Dice face positions
        self.dice_faces = {
            1: [(3, 3)],
            2: [(1, 1), (5, 5)],
            3: [(1, 1), (3, 3), (5, 5)],
            4: [(1, 1), (1, 5), (5, 1), (5, 5)],
            5: [(1, 1), (1, 5), (3, 3), (5, 1), (5, 5)],
            6: [(1, 1), (1, 3), (1, 5), (5, 1), (5, 3), (5, 5)]
        }
        self.dice_number = 1
        self.pos = (0, 0)
        self.size = 50
        self.dice_sound = Sound_Effect(self, DICE)

    def draw_dice(self, x, y, size):
        """
        Draw a dice with the given number at position (x,y) with the given size.
        """
        self.pos = (x, y)
        self.size = size
        shadow_offset = size // 10

        # Draw shadow
        pg.draw.polygon(self.win, (50, 50, 50), [
            (x + shadow_offset, y + shadow_offset),
            (x + size + shadow_offset, y + shadow_offset),
            (x + size + shadow_offset, y + size + shadow_offset),
            (x + shadow_offset, y + size + shadow_offset)
        ])

        # Draw dice faces (front, top, side)
        front_face = [(x, y), (x + size, y), (x + size, y + size),
                      (x, y + size)]

        top_face = [(x, y), (x + size, y),
                    (x + size - shadow_offset, y - shadow_offset),
                    (x - shadow_offset, y - shadow_offset)]

        side_face = [(x + size, y), (x + size, y + size),
                     (x + size + shadow_offset, y + size + shadow_offset),
                     (x + size + shadow_offset, y + shadow_offset)]

        pg.draw.polygon(self.win, (200, 200, 200), top_face)  # Light shade
        pg.draw.polygon(self.win, (100, 100, 100), side_face)  # Dark shade
        pg.draw.polygon(self.win, WHITE, front_face)  # Main face

        for pos in self.dice_faces[self.dice_number]:
            dot_x = x + (pos[0] * size) // 6
            dot_y = y + (pos[1] * size) // 6
            pg.draw.circle(self.win, BLACK, (dot_x, dot_y), size // 12)

    def roll_dice(self):
        """
        Roll the dice and update the dice number.
        """
        self.dice_number = random.randint(1, 6)

    def is_clicked(self, mouse_pos):
        """
        Check if the dice button is clicked.
        """
        x, y = self.pos
        return (x <= mouse_pos[0] <= x + self.size
                and y <= mouse_pos[1] <= y + self.size)

    def was_clicked(self):
        """
        If the button was clicked, play the CLICK sound effect.
        """
        self.dice_sound.play()

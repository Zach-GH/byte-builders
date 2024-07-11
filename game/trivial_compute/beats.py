"""
Zachary Meisner
beats.py

Add module docstring here
"""

from settings import pg

class Beats:
    """
    Add class docstring here.
    """
    def __init__(self, app, music, fade):
        self.app = app
        self.music = music
        self.fade_in = fade

        # Load music during initialization
        pg.mixer.music.load(music)

    def is_playing(self):
        """
        Add function docstring here.
        """
        return pg.mixer.music.get_busy()

    def start_music(self):
        """
        Add function docstring here.
        """
        pg.mixer.music.play(-1, fade_ms=self.fade_in)

    def stop_music(self):
        """
        Add function docstring here.
        """
        pg.mixer.music.stop()

    def sound_effect(self):
        """
        Add function docstring here.
        """
        pg.mixer.music.play()

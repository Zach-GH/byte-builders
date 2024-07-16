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

class Sound_Effect:
    """
    Add class docstring here.
    """
    def __init__(self, app, sound_file):
        self.app = app
        self.sound = pg.mixer.Sound(sound_file)

    def play(self):
        """
        Add function docstring here.
        """
        self.sound.play()

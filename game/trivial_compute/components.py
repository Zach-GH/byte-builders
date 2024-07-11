"""
Zachary Meisner
components.py

Add module docstring here
"""

from settings import pg, ft, FONT_PATH

class Text:
    """
    Add class docstring here.
    """
    def __init__(self, app, size, name, color):
        self.app = app
        self.size = size
        self.name = name
        self.color = color
        self.font = ft.Font(FONT_PATH, self.size)
        self.area, self.rect = self.font.render(self.name, fgcolor=self.color)

    def render(self, off_x, off_y):
        """
        Add function docstring here.
        """
        x = (self.app.x - self.rect.width) / 2 * off_x
        y = (self.app.y - self.rect.height) / 2 * off_y
        return x, y

    def draw(self, screen, offset_x, offset_y):
        """
        Add function docstring here.
        """
        x, y = self.render(offset_x, offset_y)
        self.font.render_to(screen, (x, y), text=self.name,
                            fgcolor=self.color, size=self.size)


class Button:
    """
    Button class to handle button creation, rendering, and events.
    """
    def __init__(self, app, pos, size, text=''):
        self.app = app
        self.pos = pos[0], pos[1]
        self.size = size
        self.text = text
        self.font = pg.font.Font(pg.font.get_default_font(), self.size[1])
        self.rect = pg.Rect(self.pos, self.size)
        self.area = pg.Surface(self.rect.size)

    def render(self, text, text_color):
        """
        Render the text for the button.
        """
        text_area = self.font.render(f"{text}", True, text_color)
        return text_area

    def draw(self, win, text_color):
        """
        Draw the button on the screen.
        """
        text_area = self.render(self.text, text_color)
        text_x = self.pos[0] + (self.size[0] - text_area.get_width()) / 2
        text_y = self.pos[1] + (self.size[1] - text_area.get_height()) / 2
        win.blit(text_area, (text_x, text_y))

        # Update rect to encompass the text area
        self.rect.width = text_area.get_width()
        self.rect.height = text_area.get_height()
        self.rect.topleft = (text_x, text_y)

    def is_clicked(self, mouse_pos):
        """
        Check if the button is clicked.
        """
        return self.rect.collidepoint(mouse_pos)

    def update_position(self, new_pos):
        """
        Update the position of the button.
        """
        self.pos = new_pos

    def update_size(self, new_size):
        """
        Update the size of the button.
        """
        self.size = new_size
        self.rect.size = self.size
        self.area = pg.Surface(self.rect.size)
        self.font = pg.font.Font(pg.font.get_default_font(), self.size[1])


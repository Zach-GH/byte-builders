from settings import *
import math

class Text:
    def __init__(self, app, size, name, color):
        self.app = app
        self.size = size
        self.name = name
        self.color = color
        self.font = ft.Font(FONT_PATH, self.size)
        self.area, self.rect = self.font.render(self.name, fgcolor=self.color)
        self.center_x = (self.app.win_x - self.rect.width) / 2
        self.center_y = (self.app.win_y - self.rect.height) / 2

    def render_text(self, x, y):
        self.font.render_to(self.app.win, (x, y),text=self.name,
                            fgcolor=self.color, size=self.size)

class Button:
    def __init__(self, app, color, pos, size, textColor, text=''):
        self.app = app
        self.color = color
        self.pos = pos[0], pos[1]
        self.size = size
        self.text = text
        self.font = pg.font.Font(pg.font.get_default_font(), size[1])
        self.textArea = self.font.render(f"{text}", True, textColor)
        self.area = pg.Surface((self.size[0], self.size[1]))

    def render(self, win):
        win.blit(self.area, (self.pos[0], self.pos[1]))
        win.blit(self.textArea, (self.pos[0]+1, self.pos[1]+5))
        self.area.fill((self.color))

    def draw(self, win):
        self.render(win)


class Menu:
    def __init__(self, app):
        self.app = app
        self.win = self.app.screen
        self.win_x, self.win_y = self.win.get_size()
        self.bg_img = pg.image.load(MENU_BG_PATH)
        self.title = Text(self, 150, "Trivial Compute", "black")
        self.team_name = Text(self, 80, "Team Byte-Builders", "black")
        self.center = (self.app.x / 2)
        self.btn_list = [("b1", (255, 255, 0), 350, (0, 0, 0), 'Play'),
                    ("b2", (255, 0, 0), 350, (0, 0, 0), 'Options'),
                    ("b3", (255, 0, 0), 350, (0, 0, 0), 'Mute'),
                    ("b4", (255, 0, 0), 350, (0, 0, 0), 'Dark'),
                    ("b5", (0, 255, 0), 350, (0, 0, 0), 'Credits'),
                    ("b6", (0, 255, 0), 350, (0, 0, 0), 'Quit')]

        # Create the buttons on the main menu
        j = 0
        for i in self.btn_list:
            setattr(self, i[0], Button(self, i[1], ((self.center - BTN_W_LOC),
                                        i[2] + j), (BTN_W, BTN_H), i[3], i[4]))
            j += 75

    def draw_menu(self):
        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.win)

        self.title.render_text(self.title.center_x, 0)
        self.team_name.render_text(self.title.center_x + 50, WIN_H * 0.14)

    def update(self):
        pg.display.update()

    def draw(self):
        self.draw_menu()
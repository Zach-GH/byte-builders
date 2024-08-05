"""
Zachary Meisner
waiting_room.py

Add module docstring here
"""

import sys
from settings import pg, PLAY_COLOR, BTN_W_LOC, BTN_W, BTN_H
from net.network import Network
from components import Button, Text
from gameboard import GameBoard
from net.server import Server

class WaitingRoom:
    def __init__(self, app):
        self.app = app
        self.dev = self.app.dev
        self.screen = self.app.app.screen
        self.x = self.app.app.x
        self.y = self.app.app.y
        self.center_x = self.x / 2
        self.center_y = self.y / 2
        self.gameboard = GameBoard(self)
        self.s = Server(self)
        self.connected = False
        self.allowUpdate = False
        self.base_font = pg.font.Font(None, 32)
        self.user_text = ''
        self.input_rect = pg.Rect(self.center_x + 200, self.center_y - 390, 140, 32)
        self.color_active = pg.Color('lightskyblue3')
        self.color_passive = pg.Color('chartreuse4')
        self.active = False
        self.serverFail = False
        self.nameFail = False
        self.text_list = [("t1", 100, "Player Name:", "white", "pname"),
                          ("t2", 100, "Please Choose a Player Name!", "white", "pname"),
                          ("t3", 100, "You must run the server to play!", "white", "pname")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Back'),
                         ("b2", 150, (255, 255, 255), 'Connect')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))
        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def check_events(self, p1, p2, p3, p4):
        """
        Add function docstring here.
        """
        for event in pg.event.get():
            if (event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                          and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            elif (event.type == pg.KEYDOWN):
                if self.dev:
                    if event.key == pg.K_LEFT:
                        self.gameboard.move_player(p1, p2, p3, p4, 'LEFT')
                    elif event.key == pg.K_RIGHT:
                        self.gameboard.move_player(p1, p2, p3, p4, 'RIGHT')
                    elif event.key == pg.K_UP:
                        self.gameboard.move_player(p1, p2, p3, p4, 'UP')
                    elif event.key == pg.K_DOWN:
                        self.gameboard.move_player(p1, p2, p3, p4, 'DOWN')
            elif event.type == pg.MOUSEBUTTONUP:
                self.gameboard.check_gameboard_events(p1, p2, p3, p4)

    def draw_window(self, p1, p2, p3, p4):
        self.connected = True
        self.screen.fill(color=PLAY_COLOR)
        self.gameboard.set_player_name(p1)
        self.gameboard.draw(p1, p2, p3, p4)
        pg.display.flip()
        self.check_events(p1, p2, p3, p4)

    def set_button_position(self, button_name, x, y):
        """
        Set the position of a button dynamically.
        """
        button = getattr(self, button_name)
        button.update_position((x, y))

    def draw_waitingroom_ui(self):
        """
        Draw the waitingroom UI, including text and buttons.
        """
        for i in self.text_list:
            text = getattr(self, i[0])
            if i[0] == "t1":
                text.draw(self.screen, 1, 0)
            else:
                if i[0] == "t2" and self.nameFail == True:
                    text.draw(self.screen, 1, 1)
                elif i[0] == "t3" and self.serverFail == True:
                    text.draw(self.screen, 1, 1)
                else:
                    pass

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        if self.active:
            color = self.color_active
        else:
            color = self.color_passive
        
        pg.draw.rect(self.screen, color, self.input_rect)
        self.text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(200, self.text_surface.get_width() + 10)
        
        self.set_button_position("b1", 50, 50)
        self.set_button_position("b2", self.center_x - 50, self.center_y - 200)
        pg.display.flip()

    def network_connection(self):
        if self.user_text == '':
            self.nameFail = True
            self.allowUpdate = False
        else:
            self.nameFail = False
            running = True
            n = Network(self)
            p1 = n.getP()

            if p1 == None:
                running = False
                self.allowUpdate = False
                self.serverFail = True
            else:
                self.serverFail = False
                while running:
                    p2 = n.send(p1)
                    p3 = n.send(p2)
                    p4 = n.send(p3)

                    self.draw_window(p1, p2, p3, p4)

    def update(self):
        if self.allowUpdate == True:
            self.network_connection()
        else:
            pass

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_waitingroom_ui()

    def handle_button_click(self, pos):
        """
        Handle button click events.
        """
        for i in self.btn_list:
            button = getattr(self, i[0])
            if button.is_clicked(pos):
                button.was_clicked()
                if i[0] == 'b1':
                    self.app.display = "menu"
                elif i[0] == 'b2':
                    print("Connecting!")
                    self.allowUpdate = True

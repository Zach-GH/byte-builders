"""
Zachary Meisner
waiting_room.py

Add module docstring here
"""

import sys
import threading as t
from settings import pg, PLAY_COLOR, BTN_W_LOC, BTN_W, BTN_H
from net.network import Network
from components import Button, Text
from gameboard import GameBoard
from net.server import Server

class WaitingRoom:
    def __init__(self, app):
        self.app = app
        self.clock = self.app.app.clock
        self.screen = self.app.app.screen
        self.x = self.app.app.x
        self.y = self.app.app.y
        self.gameboard = GameBoard(self)
        self.s = Server(self)
        self.connected = False
        self.allowUpdate = False
        self.text_list = [
            ("t1", 150, "Click to Play!", "white", "click"),
            ("t2", 150, f"Total Players Connected: {len(self.s.connected_players)}", "white", "tplayers")]
        self.btn_list = [("b1", 150, (255, 255, 255), 'Back'),
                         ("b2", 150, (255, 255, 255), 'Connect'),
                         ("b3", 150, (255, 255, 255), f'Player Count: {self.s.pnum}')]

        for i in self.btn_list:
            setattr(self, i[0], Button(self, ((self.x / 2 - BTN_W_LOC),
                                        i[1]), (BTN_W, BTN_H), i[3]))
        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def check_events(self, player_num):
        """
        Add function docstring here.
        """
        for event in pg.event.get():
            if (event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                          and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            elif (event.type == pg.KEYDOWN):
                if event.key == pg.K_LEFT:
                    self.gameboard.move_player(player_num, 'LEFT')
                elif event.key == pg.K_RIGHT:
                    self.gameboard.move_player(player_num, 'RIGHT')
                elif event.key == pg.K_UP:
                    self.gameboard.move_player(player_num, 'UP')
                elif event.key == pg.K_DOWN:
                    self.gameboard.move_player(player_num, 'DOWN')
            elif event.type == pg.MOUSEBUTTONUP:
                self.gameboard.check_gameboard_events()

    def draw_window(self, game, player_num):
        if not(game.connected()):
            pass
        else:
            self.connected = True
            self.screen.fill(color=PLAY_COLOR)
            self.gameboard.draw()
            pg.display.flip()
            self.check_events(player_num)

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
            if i[4] == "click":
                text.draw(self.screen, 1, 0)
            elif i[4] == "tplayers":
                text.update_text(f"Total Players Connected: {len(self.s.connected_players)}")
                text.draw(self.screen, 1, 1)

        for i in self.btn_list:
            button = getattr(self, i[0])
            button.draw(self.screen, i[2])

        self.set_button_position("b1", 50, 50)
        self.set_button_position("b2", 900, 650)
        self.set_button_position("b3", 900, 300)

    def network_connection(self):
        running = True
        n = Network(self)
        player = int(n.getP())

        while running:
            try:
                game = n.send("get")
            except:
                running = False
                self.connected = False
                print("Couldn't get game")
                break

            if game.bothWent():
                self.draw_window(game, player)
                pg.time.delay(500)
                try:
                    game = n.send("reset")
                except:
                    running = False
                    print("Couldn't get game")
                    break

                pg.display.update()
                pg.time.delay(2000)

            self.draw_window(game, player)

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
                elif i[0] == 'b3':
                    self.s.configure_player_count()
                    button.update_text(f'Player Count: {self.s.pnum}')
                    print(f"Player Count is now: {self.s.pnum}")

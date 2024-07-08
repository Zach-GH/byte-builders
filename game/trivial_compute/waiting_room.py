"""
Zachary Meisner
waiting_room.py

Add module docstring here
"""

import sys
from settings import pg, PLAY_COLOR
from net.network import Network
from components import Text
from gameboard import GameBoard

class WaitingRoom:
    def __init__(self, app):
        self.app = app
        self.clock = self.app.app.clock
        self.win = self.app.app.screen
        self.x = self.app.app.x
        self.y = self.app.app.y
        self.gameboard = GameBoard(self)
        self.updateAllowed = False
        self.connected = False
        self.text_list = [("t1", 150, "Click to Play!", "white", "click"),
                          ("t2", 150, "Waiting for other player", "white", "wait")]


        for i in self.text_list:
            setattr(self, i[0], Text(self, i[1], i[2], i[3]))

    def check_events(self):
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
                    self.gameboard.move_player('LEFT')
                elif event.key == pg.K_RIGHT:
                    self.gameboard.move_player('RIGHT')
                elif event.key == pg.K_UP:
                    self.gameboard.move_player('UP')
                elif event.key == pg.K_DOWN:
                    self.gameboard.move_player('DOWN')

    def draw_window(self, game):
        if not(game.connected()):
            # print("Waiting for other player to connect")
            pass
        else:
            # print("Connected!")
            self.connected = True
            self.gameboard.update()
            self.win.fill(color=PLAY_COLOR)
            self.gameboard.draw()
            pg.display.flip()
            self.check_events()


        # pg.display.update()

    def draw_waitingroom_ui(self):
        """
        Draw the waitingroom UI, including text and buttons.
        """

        for i in self.text_list:
            text = getattr(self, i[0])
            # Figure out a way to switch the text based off of state
            # so when the player clicks it displays one text or the other
            if i[4] == "click":
                text.draw(1, 0)
            elif i[4] == "wait":
                text.draw(1, 1)

        # pg.display.update()

    def update(self):
        if (self.updateAllowed == True):
            running = True
            n = Network(self)
            player = int(n.getP())
            print("You are player", player)

            while running:
                try:
                    game = n.send("get")
                except:
                    running = False
                    self.connected = False
                    print("Couldn't get game")
                    break

                if game.bothWent():
                    self.draw_window(game)
                    pg.time.delay(500)
                    try:
                        game = n.send("reset")
                    except:
                        running = False
                        print("Couldn't get game")
                        break

                    pg.display.update()
                    pg.time.delay(2000)

                self.draw_window(game)
        else:
            pass

    def allowUpdate(self):
        self.updateAllowed = True

    def draw(self):
        """
        Add function docstring here.
        """
        self.draw_waitingroom_ui()

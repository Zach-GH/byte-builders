import pygame as pg
from network import Network
import pickle
pg.font.init()

width, height = 700, 700
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2)
                        - round(text.get_width()/2),
                        self.y + round(self.height/2)
                        - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if (self.x <= x1 <+ self.x + self.width
            and self.y <= y1 <= self.y + self.height):
            return True
        else:
            return False

class Client:
    def __init__(self, app):
        self.app = app
        self.btns = [Button("Rock", 50, 500, (0,0,0)),
                     Button("Scissors", 250, 500, (255, 0, 0)),
                     Button("Paper", 450, 500, (0, 255, 0))]

    def redrawWindow(self, win, game, p):
        win.fill((128, 128, 128))

        if not(game.connected()):
            font = pg.font.SysFont("comicsans", 60)
            text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
            win.blit(text, (width/2 - text.get_width()/2,
                            height/2 - text.get_height()/2))
        else:
            font = pg.font.SysFont("comicsans", 40)
            text = font.render("Your Move", 1, (0, 255, 255))
            win.blit(text, (80, 200))

            text = font.render("Opponents", 1, (0, 255, 255))
            win.blit(text, (380, 200))

            move1 = game.get_player_move(0)
            move2 = game.get_player_move(1)
            if game.bothWent():
                text1 = font.render(move1, 1, (0, 0, 0))
                text2 = font.render(move2, 1, (0, 0, 0))
            else:
                if game.p1Went and p == 0:
                    text1 = font.render(move1, 1, (0, 0, 0))
                elif game.p1Went:
                    text1 = font.render("Locked In", 1, (0, 0, 0))
                else:
                    text1 = font.render("Waiting...", 1, (0, 0, 0))

                if game.p2Went and p == 1:
                    text2 = font.render(move2, 1, (0, 0, 0))
                elif game.p2Went:
                    text2 = font.render("Locked In", 1, (0, 0, 0))
                else:
                    text2 = font.render("Waiting...", 1, (0, 0, 0))

            if p == 1:
                win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))

            for btn in self.btns:
                btn.draw(win)

        pg.display.update()

    def game_loop(self):
        running = True
        clock = pg.time.Clock()
        n = Network(self)
        player = int(n.getP())
        print("You are player", player)

        while running:
            clock.tick(60)
            try:
                game = n.send("get")
            except:
                running = False
                print("Couldn't get game")
                break

            if game.bothWent():
                self.redrawWindow(win, game, player)
                pg.time.delay(500)
                try:
                    game = n.send("reset")
                except:
                    running = False
                    print("Couldn't get game")
                    break

                font = pg.font.SysFont("comicsans", 90)
                if ((game.winner() == 1 and player == 1)
                    or (game.winner() == 0 and player == 0)):
                    text = font.render("You Won!", 1, (255, 0, 0))
                elif game.winner() == -1:
                    text = font.render("Tie Game!", 1, (255, 0, 0))
                else:
                    text = font.render("You Lost...", 1, (255, 0, 0))

                win.blit(text, (width/2 - text.get_width()/2,
                                height/2 - text.get_height()/2))
                pg.display.update()
                pg.time.delay(2000)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    for btn in self.btns:
                        if btn.click(pos) and game.connected():
                            if player == 0:
                                if not game.p1Went:
                                    n.send(btn.text)
                            else:
                                if not game.p2Went:
                                    n.send(btn.text)

            self.redrawWindow(win, game, player)

    def menu_screen(self):
        running = True
        clock = pg.time.Clock()

        while running:
            clock.tick(60)
            win.fill((128, 128, 128))
            font = pg.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255, 0, 0))
            win.blit(text, (100, 200))
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.game_loop()

    def run(self):
        self.menu_screen()

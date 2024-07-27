"""
Zachary Meisner
game.py

Please note that none of this file accurately pertains
to the logic we are going to need to provide.

This is a file written based off of the initial tutorial
I followed and has corresponding logic to the game
Rock Paper Scissors.  Please take into consideration that
when this file is going to be used, we will change it to
have our own game logic, but is meant to be nothing other
than a template waiting to be filled out for the time being.

"""

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False
        self.p4Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        # P1 and P2
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0] # get the first letter of the move
        p2 = self.moves[1].upper()[0]

        # winner is -1 because there could be a tiet
        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

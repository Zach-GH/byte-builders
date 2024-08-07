import sys
import socket
from _thread import *
import pickle
from player import Player

connected = set()
games = {}

players = [Player((0, 0), (255, 0, 0), 'P1', 1),
           Player((8, 8), (0, 255, 0), 'P2', 2),
           Player((0, 8), (0, 0, 255), 'P3', 3),
           Player((8, 0), (255, 255, 0), 'P4', 4)]

class Server:
    def __init__(self, app):
        self.app = app
        self.server = self.get_local_ip()
        self.port = 5555
        self.pnum = 1 # player num change to whatever
        self.connected_players = []

    def get_local_ip(self):
        local_ip = socket.gethostbyname('localhost')
        return local_ip

    def configure_player_count(self):
        if self.pnum < 4:
            self.pnum += 1
            print("pnum is", self.pnum)
        else:
            self.pnum = 1
            print("pnum is", self.pnum)

    def threaded_client(self, conn, player):
        global games

        # send initial message to determine which player we are
        conn.send(pickle.dumps(players[player]))
        reply = ""

        while True:
            # just in case we are sending too much information double num
            try:
                data = pickle.loads(conn.recv(5000))
                players[player] = data

                if not data:
                    break
                else:
                    if self.pnum == 1:
                        reply = players[0]
                        conn.sendall(pickle.dumps(reply))
                    if self.pnum == 2:
                        reply = players[0]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[1]
                        conn.sendall(pickle.dumps(reply))
                    if self.pnum == 3:
                        reply = players[0]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[1]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[2]
                        conn.sendall(pickle.dumps(reply))
                    if self.pnum == 4:
                        reply = players[0]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[1]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[2]
                        conn.sendall(pickle.dumps(reply))
                        reply = players[3]
                        conn.sendall(pickle.dumps(reply))
            except:
                break

        print("Lost connection")
        conn.close()

    def run(self):
        global games

        # initialize the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind server and port to the socket
        try:
            s.bind((self.server, self.port))
        except socket.error as e:
            # print out why there is a connection problem
            str(e)

        s.listen()
        print("Waiting for a connection, Server Started")

        while True:
            # accept any incoming connections
            # and store the connection and ip address
            conn, addr = s.accept()
            player_id = len(self.connected_players) + 1
            print("Player Number: ", player_id, " has connected to: ", addr)
            self.connected_players.append((conn, addr, player_id))

            if len(self.connected_players) == self.pnum:

                for player in self.connected_players:
                    conn, addr, player_id = player
                    start_new_thread(self.threaded_client,
                                     (conn, player_id - 1))

                # clear list for next games
                self.connected_players.clear()

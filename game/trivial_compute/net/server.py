import socket
from _thread import *
import pickle
from game import Game

connected = set()
games = {}

class Server:
    def __init__(self, app):
        self.app = app
        self.server = self.get_local_ip()
        self.port = 5555
        self.pnum = 1 # player num
        self.connected_players = []

    def get_local_ip(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    def configure_player_count(self):
        if self.pnum < 4:
            self.pnum += 1
            print("pnum is", self.pnum)
        else:
            self.pnum = 1
            print("pnum is", self.pnum)

    def threaded_client(self, conn, p, game_id):
        global games

        # send initial message to determine which player we are
        conn.send(str.encode(str(p)))

        while True:
            # just in case we are sending too much information double num
            try:
                data = conn.recv(4096).decode()

                if game_id in games:
                    game = games[game_id]

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.resetWent()
                        elif data != "get":
                            game.play(p, data)

                        conn.sendall(pickle.dumps(game))
                else:
                    break
            except:
                break

        print("Lost connection")
        try:
            del games[game_id]
            print("Closing game", game_id)
        except:
            pass
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
            print("len(self.connected_players)", len(self.connected_players))

            if len(self.connected_players) == self.pnum:
                game_id = len(games)
                games[game_id] = Game(game_id)
                print(f"Starting game {game_id}")

                # Mark game as ready and assign players
                games[game_id].ready = True

                for player in self.connected_players:
                    conn, addr, player_id = player
                    start_new_thread(self.threaded_client,
                                     (conn, player_id, game_id))

                # clear list for next games
                self.connected_players.clear()

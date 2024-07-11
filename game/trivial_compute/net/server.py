import socket
from _thread import *
import pickle
from game import Game

connected = set()
games = {}
connected_players = []
REQUIRED_PLAYERS = 4

class Server:
    def __init__(self, app):
        self.app = app
        # on mac to get local ethernet connection
        # this command also is default for the Wi-Fi network adapter
        # I used ipconfig getifaddr en0
        self.server = "192.168.1.6"
        self.port = 5555

    # a thread is just a process that is running in the background
    # threads are important because we do not want the function to wait
    # for something to happen before the program continues
    # this is how multiplayer works because we want two people
    # to be able to do things at one time
    #
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

        s.listen(4) # 4 for 4 players
        print("Waiting for a connection, Server Started")

        while True:
            # accept any incoming connections
            # and store the connection and ip address
            conn, addr = s.accept()
            player_id = len(connected_players) + 1
            print("Player Number: ", player_id, " has connected to: ", addr)
            connected_players.append((conn, addr, player_id))

            if len(connected_players) == REQUIRED_PLAYERS:
                # All required players are connected
                game_id = len(games)
                games[game_id] = Game(game_id)
                print(f"Starting game {game_id}")

                # Mark game as ready and assign players
                games[game_id].ready = True

                for player in connected_players:
                    conn, addr, player_id = player
                    start_new_thread(self.threaded_client,
                                     (conn, player_id, game_id))

                # clear list for next games
                connected_players.clear()

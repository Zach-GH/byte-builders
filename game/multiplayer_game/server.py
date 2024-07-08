import socket
from _thread import *
import pickle
from game import Game

connected = set()
games = {}
idCount = 0

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
    def threaded_client(self, conn, p, gameId):
        global idCount
        global games

        # send initial message to determine which player we are
        conn.send(str.encode(str(p)))

        while True:
            # just in case we are sending too much information double num
            try:
                data = conn.recv(4096).decode()

                if gameId in games:
                    game = games[gameId]

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
            del games[gameId]
            print("Closing game", gameId)
        except:
            pass
        idCount -= 1
        conn.close()


    def run(self):
        global idCount
        global games

        # initialize the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind server and port to the socket
        try:
            s.bind((self.server, self.port))
        except socket.error as e:
            # print out why there is a connection problem
            str(e)

        s.listen(2) # 2 for 2 players
        print("Waiting for a connection, Server Started")

        while True:
            # accept any incoming connections
            # and store the connection and ip address
            conn, addr = s.accept()
            print("Connected to:", addr)

            # How many people are connected to the server at once
            idCount += 1
            p = 0
            # What Id is our game?
            gameId = (idCount - 1)//2
            # create a new game if the following happens
            # this means 2 people are already playing and create a new game
            if idCount % 2 == 1:
                games[gameId] = Game(gameId)
                print("Creating a new game...")
            else:
                games[gameId].ready = True
                p = 1 # player equals 1

            start_new_thread(self.threaded_client, (conn, p, gameId))

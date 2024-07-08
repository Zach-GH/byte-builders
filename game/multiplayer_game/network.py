import socket
import pickle

class Network:
    def __init__(self, app):
        self.app = app
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.6" # same number as in server.py
        self.port = 5555 # same port as server.py
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # send player number to classify which player is which
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            # send string expect return obj data
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

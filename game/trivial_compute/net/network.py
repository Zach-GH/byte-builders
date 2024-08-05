import socket
import pickle

class Network:
    def __init__(self, app):
        self.app = app
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = self.get_local_ip()
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_local_ip(self):
        local_ip = socket.gethostbyname('localhost')
        return local_ip

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # send player number to classify which player is which
            return pickle.loads(self.client.recv(10000))
        except:
            pass

    def send(self, data):
        try:
            # send string expect return obj data
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(10000))
        except socket.error as e:
            print(e)

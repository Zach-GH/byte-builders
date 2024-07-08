#!/usr/bin/env python3

# tech with tim tutorial
# https://www.youtube.com/watch?v=_fx7FQ3SP0U&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=1&pp=iAQB

import sys
from client import Client
from server import Server

# Accepting an argument at runtime allows us to test multiple components
# separately in different terminals.  This is helpful for testing the client
# and server files without running them at the same time.
arg = "all"

A = 1
n = len(sys.argv)
while A < n:
    if (sys.argv[A] == "-r" and A + 1 < n):
        run_arg = sys.argv[A + 1].lower()
        if run_arg == "s":
            arg = "server"
        elif run_arg == "c":
            arg = "client"
        A += 1
    A += 1

class App:
    def __init__(self):
        self.arg = arg
        if (self.arg == "client"):
            self.client = Client(self)
        elif (self.arg == "server"):
            self.server = Server(self)

    def run(self):
        # server script has to be running before running the client script
        # there can be multiple client scripts running on one server
        if (self.arg == "all"):
            print("Running All")
            self.server.run()
            self.client.run()
        elif (self.arg == "server"):
            print("Running Server")
            self.server.run()
        elif (self.arg == "client"):
            print("Running Client")
            self.client.run()

if __name__ == '__main__':
    a = App()
    a.run()

import socket
import threading
import random
import time

class ClientSide(object):
    def __init__(self):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!DISCONNECT"

        self.all_profil = []

    def create_profil(self,port,ip):
        new_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

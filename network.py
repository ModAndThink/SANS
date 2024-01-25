import socket
import threading
import random
import time

class ClientSide(object):
    def __init__(self):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!DISCONNECT"

        self.all_profil = {}
        print("[PROGRAMME] nouveaux objet client")

    def create_profil(self,ip,port):
        addr = (ip,port)
        new_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(addr)
        new_client.connect(addr)
        print("[CLIENT] profil initialisé, attente du message d'acceptation")
        msg = new_client.recv(self.HEADER).decode(self.FORMAT).strip()
        if msg!="test_lololololool":
            print("[CLIENT] serveur invalide, arrêt du profil")
            new_client.close()
            return False
        print("[CLIENT] serveur valide, envoie du code de vérification")
        self.send_str("salut, coucou, au revoir, 1414424314544",new_client)
        time.sleep(1)
        if new_client.fileno()==-1:
            print("[CLIENT] serveur fermé, arrêt")
            new_client.close()
            return False
        print("[CLIENT] serveur ouvert, profil valide")
        self.all_profil[ip]=new_client
        return True
        
    
    def send_str(self,msg,clientProfil):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        if msg_length<=self.HEADER:
            clientProfil.send(message + b" " * (self.HEADER - msg_length))
            return True
        else:
            print("[SERVER] erreur, message trop long")
            return False
    
    def send_msg_all(self,msg):
        for profil in self.all_profil:
            self.send_str(msg,self.all_profil[profil])

class ServerSide(object):
    def __init__(self,LINK_CLIENT=ClientSide(),PSEUDO="SP"):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!DISCONNECT"
        self.LINK_CLIENT = LINK_CLIENT
        self.PORT = 25000
        self.PSEUDO = PSEUDO

        self.shutdown = False
        self.all_msg_receive = []
        self.GUI = None
        print("[PROGRAMME] nouveaux objet server")

    def initializeServer(self):
        addr = ("0.0.0.0",self.PORT)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        print("[SERVER] prêt à servir")
        self.server.listen()
        print(f"[SERVER] écoute au port {self.PORT}")
        thread = threading.Thread(target=self.routine)
        thread.start()

    def routine(self):
        while not self.shutdown:
            connection,address = self.server.accept()
            thread = threading.Thread(target=self.handling_client,args= (connection,address))
            thread.start()

    def handling_client(self,connection, address):
        print(f"[SERVER] nouvelle connection de {address}\n")
        self.send_str("test_lololololool",connection)
        msg = connection.recv(self.HEADER).decode(self.FORMAT).strip()

        if msg!="salut, coucou, au revoir, 1414424314544":
            print("[SERVER] mauvais mot de passe, déconnection")
            connection.close()
            return False
        print("[SERVER] mot de passe valide")
        time.sleep(1)
        print("[SERVER] lancement du profil")
        isAlreadyDetected = False
        for i in list(self.LINK_CLIENT.all_profil):
            print(i,address[0],i==address[0])
            if i == address[0]:
                isAlreadyDetected = True
        
        if not isAlreadyDetected:
            print(f"[SERVER] profil inconnu, création du profil client {address[0]}")
            self.LINK_CLIENT.create_profil(address[0],self.PORT)

        while not self.shutdown:
            try:
                msg = connection.recv(self.HEADER).decode(self.FORMAT).strip()
                isNew = True
                for i in self.all_msg_receive:
                    if i==msg:
                        isNew = False
                        break
                
                if isNew:
                    print(f"{address} : {msg}")
                    self.all_msg_receive.append(msg)
                    self.LINK_CLIENT.send_msg_all(msg)
                    if self.GUI!=None:
                        self.GUI.addMessage(msg)
            except Exception as e:
                print(e)
        
    def send_str(self,msg,conn):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        if msg_length<=self.HEADER:
            conn.send(message + b" " * (self.HEADER - msg_length))
            return True
        else:
            print("[SERVER] erreur, message trop long")
            return False
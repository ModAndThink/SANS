import tkinter as tk
import tkinter.font as tkFont
import network

class App(object):
    def __init__(self,LINK_SERVER):
        self.LINK_SERVER = LINK_SERVER
        self.LINK_SERVER.GUI = self
        self.window = tk.Tk()

        self.frameMsg = tk.Frame(master=self.window,width=200,height=900)
        self.scrollBarMsg = tk.Scrollbar(master=self.frameMsg)
        self.listMsg = tk.Listbox(master=self.frameMsg,yscrollcommand=self.scrollBarMsg.set,width=100)

        self.scrollBarMsg.config(command=self.listMsg.yview)
        
        self.scrollBarMsg.pack(side = tk.RIGHT, fill = tk.Y)
        self.frameMsg.pack()
        self.listMsg.pack(side=tk.LEFT,fill=tk.BOTH)

        self.frameSend = tk.Frame(master=self.window)
        self.input = tk.Entry(master=self.frameSend,width=95)
        self.buttonSend = tk.Button(master=self.frameSend,text="->",command=self.sendMessage)

        self.frameSend.pack()
        self.input.pack(side=tk.LEFT,fill=tk.BOTH)
        self.buttonSend.pack(side=tk.RIGHT,fill=tk.Y)

    def sendMessage(self):
        msg = self.input.get()
        if msg=="":
            return False
        elif msg[0]=="!":
            command = msg.split(" ")
            if command[0]=="!connect" and len(command)==2:
                self.LINK_SERVER.LINK_CLIENT.create_profil(command[1],25000)
            elif command[0]=="!rename" and len(command)==2:
                self.LINK_SERVER.PSEUDO = command[1]
            elif command[0]=="!initialize" and len(command)==1:
                self.LINK_SERVER.initializeServer()
            else:
                self.addMessage("commande invalide")
        else:
            self.LINK_SERVER.LINK_CLIENT.send_msg_all(self.LINK_SERVER.PSEUDO+" : "+msg)

    def addMessage(self,text):
        self.listMsg.insert(tk.END,text)

s = network.ServerSide()

App(LINK_SERVER=s).window.mainloop()

import tkinter as tk
import tkinter.font as tkFont

class App(object):
    def __init__(self):
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
        pass

    def addMessage(self,pseudo,text):
        self.listMsg.insert(tk.END,pseudo+" : "+text)

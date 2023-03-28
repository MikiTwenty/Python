from os import system
import customtkinter as ctk
from .__stream import *

class ServerGUI():
    def __init__(self):
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')
        self.root = ctk.CTk()
        self.root.geometry('280x280')
        self.root.resizable(False, False)
        self.server = Server()
        self.state = 'Disconnected'

    def start(self):
        self.cls()
        try:
            accepting, self.client = self.server.start(int(self.port.get()))
            print(accepting, self.client)
            self.port.configure(state='readonly')
            if accepting:
                self.button.configure(text='SHUT DOWN', fg_color='red', command=self.stop)
            else:
                self.button.configure(text='STOP LISTENING', fg_color='blue', command=self.stop)
        except Exception as error:
            print(">> Can't start the server!")
            print(error)
            self.button.configure(text='START', fg_color='green', command=self.start)
        self.port.update()

    def stop(self):
        self.cls()
        self.server.stop()
        self.button.configure(text='START', fg_color='green', command=self.start)
        self.port.configure(state='normal')

    def display(self):
        self.cls()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20,  padx=20, fill='both', expand=True)

        title = ctk.CTkLabel(master=frame, text='Streaming Server', font=('Roboto', 24))
        self.host_ip = ctk.CTkLabel(master=frame, text=("Host IP: "+self.server.host_ip))
        self.port = ctk.CTkEntry(master=frame, placeholder_text='Port: 1234')
        self.button = ctk.CTkButton(master=frame, text='START', command=self.start, fg_color='green')

        title.pack(pady=12, padx=10)
        self.host_ip.pack(pady=12, padx=10)
        self.port.pack(pady=12, padx=10)
        self.button.pack(pady=12, padx=10)

    def update(self):
        self.root.update()

    def cls(self):
        system('cls')
        print('[SERVER]')

class ClientGUI():
    def __init__(self):
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')
        self.root = ctk.CTk()
        self.root.geometry('280x280')
        self.root.resizable(False, False)
        self.client = Client()
        self.state = 'Disconnected'

    def connect(self):
        self.cls()
        try:
            self.client.connect(self.host_ip.get(), int(self.port.get()))
            self.host_ip.configure(state='readonly')
            self.port.configure(state='readonly')
            self.button.configure(text='Disconnect', fg_color='red', command=self.disconnect)
            self.button.update()

        except Exception as error:
            print(">> Connection failed!")
            print(error)

    def disconnect(self):
        self.cls()
        self.client.disconnect()
        self.button.configure(text='Connect', fg_color='green', command=self.connect)
        self.host_ip.configure(state='normal')
        self.port.configure(state='normal')
        self.button.update()

    def display(self):
        self.cls()
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20,  padx=20, fill='both', expand=True)

        title = ctk.CTkLabel(master=frame, text='Streaming Client', font=('Roboto', 24))
        self.host_ip = ctk.CTkEntry(master=frame, placeholder_text='Host IP: 127.0.0.1')
        self.port = ctk.CTkEntry(master=frame, placeholder_text='Port: 1234')
        self.button = ctk.CTkButton(master=frame, text='Connect', command=self.connect, fg_color='green')

        title.pack(pady=12, padx=10)
        self.host_ip.pack(pady=12, padx=10)
        self.port.pack(pady=12, padx=10)
        self.button.pack(pady=12, padx=10)

    def update(self):
        self.root.update()

    def cls(self):
        system('cls')
        print('[CLIENT]')
import customtkinter as ctk

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('360x280')
root.resizable(False, False)

def login():
    print(port.get())

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20,  padx=60, fill='both', expand=True)

title = ctk.CTkLabel(master=frame, text='Streaming Server', font=('Roboto', 24))
title.pack(pady=12, padx=10)

host_ip = ctk.CTkEntry(master=frame, placeholder_text='host ip: 127.0.0.1')
host_ip.pack(pady=12, padx=10)

port = ctk.CTkEntry(master=frame, placeholder_text='port: 1234')
port.pack(pady=12, padx=10)

start_button = ctk.CTkButton(master=frame, text='Start', command=login)
start_button.pack(pady=12, padx=10)

root.mainloop()
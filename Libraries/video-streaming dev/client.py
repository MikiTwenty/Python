from modules.socket import *
from modules.utils import *

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

while True:

    # initialize the client socket
    client = Client()

    client.connect("192.168.0.161", 1234)

    # check connection with the client
    while client.is_connected():
        try:
            client.send()
        except:
            break

        client.receive(show_video=True)



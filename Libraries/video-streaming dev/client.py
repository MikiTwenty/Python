from modules.socket import *
from modules.utils import *

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

while True:
    print(0)
    # initialize the client socket
    client = Client()

    client.connect("172.23.128.1", 1234)

    # check connection with the client
    while client.is_connected():
        print(00)
        try:
            client.send()
        except:
            break

        client.receive(show_video=True)



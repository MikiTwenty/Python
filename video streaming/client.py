from videostreaming.socket import Client
from videostreaming.utils import clear_output

# clear terminal output
clear_output()

# create a loop
while True:

    # initialize the client socket
    client = Client()

    # connect to the server socket
    client.connect(port=1234)

    # check connection with the client
    while client.is_connected():

        # send a frame
        client.send()

        # receive a frame
        client.receive(show_video=True)



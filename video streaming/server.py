from videostreaming.socket import Server
from videostreaming.utils import clear_output

# clear terminal output
clear_output()

# create a loop
while True:

    # initialize the server socket
    server = Server(capture_video=True)

    # open server to incoming connections
    server.start(port=1234)

    # check if a client is connected
    while server.is_connected():

        # recevie a frame
        receiving, frame = server.receive(show_video=True)

        # send a frame
        server.send()
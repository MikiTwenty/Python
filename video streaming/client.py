from videostreaming.hosting import *
from videostreaming.utils import *

# clear terminal output
clear_output()

# initialize the client socket
client = Client(verbose='high')

# connect to the server
client.connect(
    host_ip = "192.168.0.161",
    port    = 1234
)

# check connection with the client
while client.connected():

    # senf a frame to the client
    client.send()

    # receive a frame from the client
    client.receive(show_video=True)

# close the client socket
client.close()
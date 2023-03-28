import cv2
from modules.__ui import *
from modules.__utils import *

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

# initialize the client socket
client_gui = ClientGUI()
client = client_gui.client

# capture video
video = cv2.VideoCapture(0)

# display GUI interface
client_gui.display()

# create a loop
while True:
    client_gui.update()

    # check connection with the client
    while client.is_connected():

        client_gui.update()

        capturing, frame = video.read()

        if capturing:

            #print(sys.getsizeof(frame))

            cv2.imshow('Trasmitting video...', frame)

            client_gui.update()

            try:
                client.send(frame, 'low')
            except:
                pass

            receiving, processed_frame = client.receive()

            print(receiving)

            if receiving:
                cv2.imshow('Processed video', processed_frame)


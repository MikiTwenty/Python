from modules.__ui import *
from modules.__utils import *
from modules.__processing import *
from modules.__fps import *
import cv2

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

# initialize the server socket
server_gui = ServerGUI()
server = server_gui.server

# initialize the yolo model
model = Model('models/yolov8x-seg.pt')

# initialize the fps counter
counter = FPS_Counter()

# display GUI interface
server_gui.display()

# create a loop
while True:

    server_gui.update()

    # check connection with the client
    while server.has_client():

        server_gui.update()

        # recevie a frame
        receiving, frame = server.receive()

        if receiving:

            # start the time counter
            counter.start()

            # process the frame
            processed_frame = model.process(frame)

            # stop the time counter
            counter.stop()

            # get the fps
            counter.get_fps(getStats=True, printOutput=True)

            cv2.imshow('Local processed video', processed_frame)

            # send the processed fps
            try:
                server.send(processed_frame, 'low')
            except Exception as error:
                print(error)
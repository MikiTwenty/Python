from modules.socket import Server
from modules.utils import Clock, clear_output, get_cwd
from modules.processing import Model

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

# initialize the yolo model
model = Model("models/yolov8x-seg.pt")

# initialize the fps clock
clock = Clock()

# create a loop
while True:

    # initialize the server socket
    server = Server()

    server.start(1234)

    # check connection with the client
    while server.is_connected():

        # recevie a frame
        receiving, frame = server.receive()

        if receiving:

            # set starting time to get fps
            clock.tick()

            # process the frame
            processed_frame = model.process_image(frame, show_video=True)

            # get the fps
            clock.get_fps(get_stats=False, print_output=True)

            # send the processed frame
            server.send(frame=processed_frame)
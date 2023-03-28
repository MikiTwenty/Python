from modules.socket import Server
from modules.fps import Counter
from modules.utils import clear_output, get_cwd
from modules._processing import Model

# set current working directory
get_cwd(__file__)

# clear terminal output
clear_output()

# initialize the yolo model
model = Model("models/yolov8x-seg.pt")

# initialize the fps counter
counter = Counter()

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

            # start the time counter
            counter.start()

            # process the frame
            processed_frame = model.process_image(frame, show_video=True)

            # stop the time counter
            counter.stop()

            # get the fps
            fps = counter.get_fps(get_stats=True, print_output=True)

            # send the processed fps
            try:
                server.send(frame=processed_frame)
            except:
                break

        else:
            break
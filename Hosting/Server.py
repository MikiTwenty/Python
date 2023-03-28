# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

data = b""
payload_size = struct.calcsize("Q") # Q: unsigned long long integer(8 bytes)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(64000)  # 4K, range(1024 byte to 64KB)
                if not packet:
                    break
                data += packet # append the data packet got from server into data variable
            packed_msg_size = data[:payload_size] #will find the packed message size i.e. 8 byte, we packed on server side.
            data = data[payload_size:] # Actual frame data
            msg_size = struct.unpack("Q", packed_msg_size)[0] # meassage size

            while len(data) < msg_size:
                data += client_socket.recv(64000) # will receive all frame data from client socket
            frame_data = data[:msg_size] #recover actual frame data
            data = data[msg_size:]
            frame = pickle.loads(frame_data) # de-serialize bytes into actual frame type
            #cv2.imshow("RECEIVING VIDEO A", frame) # show video frame at client side
            key = cv2.waitKey(1) & 0xFF

            frame = imutils.resize(frame, width=1366)
            a = pickle.dumps(frame) #serialize frame to bytes
            message = struct.pack("Q", len(a)) + a # pack the serialized data
            # print(message)
            try:
                client_socket.sendall(message) #send message or data frames to client
            except Exception as e:
                print(e)
                raise Exception(e)

            #cv2.imshow('TRANSMITTING VIDEO B', frame) # will show video frame on server side.
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'): # press q to exit video
                break

        client_socket.close()
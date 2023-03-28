import socket, pickle, struct, imutils

class Server():
    def __init__(self):
        '''
        Streaming server socket.\n
        Methods:
        - connect(): open connections for a client socket;
        - send(): send a frame to the client socket;
        - receive(): receive a frame from the client socket;
        - stop(): Interrupt the connection with the client socket.
        '''
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_name  = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)

    def start(self, port):
        '''
        Open connections for a client socket.\n
        Parameters:
        - port (int): the port you open to enstablish a connection (default: 1234)\n
        '''
        self.__init__()
        socket_address = (self.host_ip, port)
        self.server_socket.bind(socket_address)
        self.server_socket.listen(5)
        print(">> Listening at: "+self.host_ip+':'+str(port))
        try:
            self.server_socket.setblocking(True)
            self.client_socket, address = self.server_socket.accept()
            print('>> Got connection from:', address[0])
            return True, self.client_socket
        except:
            return False, False

    def send(self, frame, resolution='high'):
        '''
        Send a frame to the client socket.\n
        Parameters:
        - frame (obj): the frame to send;
        - resolution (str, int): the frame resolution;
        can be 'high' (1920px), 'medium' (1366px), 'low' (1024px)
        or an int (default: 'high').
        '''
        if resolution == 'high':
            resolution = 1920
        elif resolution == 'medium':
            resolution = 1366
        elif resolution == 'low':
            resolution = 1024
        elif type(resolution) == int:
            pass
        frame = imutils.resize(frame, width=resolution)
        serialized_frame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialized_frame)) + serialized_frame
        try:
            self.client_socket.sendall(message)
        except Exception as error:
            print(error)
            raise Exception(error)

    def receive(self, download_speed=2):
        '''
        Receive a frame from the client socket.\n
        Parameters:
        - download_speed (int): max download speed reachable on the network,
        set a value below the effective maximum to avoid errors (default: 2 [MB]).
        '''
        download_speed = download_speed*1000*1024
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(download_speed)
                if not data:
                    break
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            return True, frame
        except:
            return False, None

    def has_client(self):
        try:
            return self.client_socket
        except:
            return False

    def stop(self):
        '''
        Interrupt the connection with the client socket.
        '''
        self.server_socket.close()
        print('>> Server stopped')

class Client():
    def __init__(self):
        '''
        Streaming client socket.\n
        Methods:
        - connect(): connect to the server socket;
        - send(): send a frame to the server socket;
        - receive(): receive a frame from the server socket;
        - disconnect(): disconnect from the server socket.
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host_ip='127.0.0.1', port=1234):
        '''
        Connect to the server socket.
        '''
        self.__init__()
        self.host_ip = host_ip
        self.port = port
        self.client_socket.connect((self.host_ip, self.port))
        print('>> Connected at:', self.host_ip)

    def send(self, frame, resolution='high'):
        '''
        Send a frame to the server socket.\n
        Parameters:
        - frame (obj): the frame to send;
        - resolution (str, int): the frame resolution;
        can be 'high' (1920px), 'medium' (1366px), 'low' (1024px)
        or an int (default: 'high').
        '''
        if resolution == 'high':
            resolution = 1920
        elif resolution == 'medium':
            resolution = 1366
        elif resolution == 'low':
            resolution = 1024
        elif type(resolution) == int:
            pass
        frame = imutils.resize(frame, width=resolution)
        serialized_frame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialized_frame)) + serialized_frame
        try:
            self.client_socket.sendall(message)
        except Exception as error:
            print(error)
            raise Exception(error)

    def receive(self, download_speed=2):
        '''
        Receive a frame from the server socket.\n
        Parameters:
        - download_speed (int): max download speed reachable on the network,
        set a value below the effective maximum to avoid errors (default: 2 [MB]).
        '''
        download_speed = download_speed*1000*1024
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(download_speed)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            return True, frame
        except:
            return False, None

    def is_connected(self):
        try:
            return self.client_socket
        except:
            return False

    def disconnect(self):
        '''
        Interrupt the connection with the client socket.
        '''
        self.client_socket.close()
        print('>> Client disconnected')
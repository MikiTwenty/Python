import socket, pickle, struct, cv2, sys

class Socket(object):
    def __init__(self, socket_type="", show_ip=False, capture_video=False, video_source=0):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_name  = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.socket_type = socket_type
        self.capture_video = capture_video
        self.video_source = video_source
        self.max_download_speed = 10*1000*1024
        if show_ip:
            print(f"{self.socket_type} Host IP: {self.host_ip}")
        if self.capture_video:
            self._get_video()

    def _get_video(self):
        try:
            self.video = cv2.VideoCapture(self.video_source)
            if self.video is None or not self.video.isOpened():
                print(f"Warning: unable to open video source: {self.video_source}")
                exit()
        except Exception as error:
            print(error)

    def _set_port(self):
        while True:
            port = input("{self.socket_type} >> Select port: ")
            if len(port) == 4:
                try:
                    port = int(port)
                    break
                except:
                    print("{self.socket_type} Port not valid!")
            else:
                print("{self.socket_type} Port not valid!")
        return port

    def _get_size(self):
        capturing, frame = self.video.read(self.video_source)
        frame_size = sys.getsizeof(frame) + 100
        self.max_download_speed = frame_size
        frame_size_binary = (bin(frame_size)).encode()
        return frame_size_binary

    def _set_size(self):
        self.client_socket.settimeout(1)
        self.max_download_speed = int(self.client_socket.recv(10*1000*1024), 2)
        self.client_socket.setblocking(True)

    def send(self, frame=None, resolution=(640, 480), show_video=False):
        """
        Send a frame to the connected socket.\n
        Parameters
        ----------
        - ``frame`` (obj) : the frame to send.
        - ``resolution`` (tuple) : the frame resolution,
         must be a tuple (int, int), (default: (640, 480)).
        - ``show_video`` (bool) : show the outgoing video,
         it works with capture_video=True (default=False).
        """
        if self.capture_video:
            capturing, frame = self.video.read()
        else:
            capturing = True
        if capturing:
            try:
                frame = cv2.resize(frame, dsize=resolution)
            except Exception as error:
                print(error)
            serialized_frame = pickle.dumps(frame)
            message = struct.pack("Q", len(serialized_frame)) + serialized_frame
            try:
                if show_video and self.capture_video:
                    cv2.imshow(f"{self.socket_type} Trasmitting video...", frame)
                    if cv2.waitKey(30) == 27:
                        cv2.destroyAllWindows()
                self.client_socket.sendall(message)
            except Exception as error:
                print(error)

    def receive(self, show_video=False):
        """
        Receive a frame from the connected socket.\n
        Parameters
        ----------
        - ``show_video`` (bool) : show the outgoing video,
         it works with capture_video=True (default=False).\n
        Returns
        -------
        - ``True`` , ``frame`` (obj) : while receiving data.
        """
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(self.max_download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(self.max_download_speed)
                if not data:
                    break
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            if show_video and self.capture_video:
                cv2.imshow(f"{self.socket_type} Receiving video...", frame)
                if cv2.waitKey(30) == 27:
                    cv2.destroyAllWindows()
            else:
                return True, frame
        except Exception as error:
            print(error)

    def stop(self):
        """
        Interrupt the connection with the connected socket.
        """
        self.socket.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("{self.socket_type} Stopped")

class Server(Socket):
    def __init__(self, show_ip=True, capture_video=False, video_source=0):
        """
        Streaming server socket.\n
        Parameters
        ----------
        - ``show_ip`` (bool) : print server IP address (default=True).
        - ``capture_video`` (bool) : enable video capturing with cameras (default=False).
        - ``video_source`` (int) : set camera index (default=0).\n
        Methods
        -------
        - ``start()`` : open connections for a client socket.
        - ``send()`` : send a frame to the client socket.
        - ``receive()`` : receive a frame from the client socket.
        - ``is_connected()`` : check if the server is connected with a client.
        - ``stop()`` : interrupt all the connections and shut down the server.
        """
        super().__init__(socket_type="[Server]", show_ip=show_ip, capture_video=capture_video, video_source=video_source)
        self.server_socket = self.socket

    def start(self, port=None):
        """
        Wait for a client socket connection.\n
        Parameters
        ----------
        - ``port`` (int) : set the port to open for connections (default: False)\n
        Returns
        -------
        - ``True`` : if started correctly.
        - ``False`` : if can"t start.
        """
        if not port:
            port = self._set_port()
        socket_address = (self.host_ip, port)
        try:
            self.server_socket.bind(socket_address)
        except Exception as error:
            print(error)
        self.server_socket.listen(5)
        print(f"{self.socket_type} Listening at: {self.host_ip}:{str(port)}")
        try:
            self.client_socket, address = self.server_socket.accept()
            print(f"{self.socket_type} Got connection from: {address[0]}")
            self._set_size()
            return True
        except:
            return False

    def is_connected(self):
        """
        Check if a client is connected with the server.\n
        Returns
        -------
        - ``False`` : if no client connected.
        - ``socket`` (obj) : if client connected.
        """
        try:
            return self.client_socket
        except:
            return False

class Client(Socket):
    def __init__(self, show_ip=False, capture_video=True, video_source=0):
        """
        Streaming client socket.\n
        Parameters
        ----------
        - ``capture_video`` (bool) : enable video capturing with cameras (default=False).
        - ``video_source`` (int) : set camera index (default=0).\n
        Methods
        -------
        - ``connect()`` : connect to the server socket.
        - ``send()`` : send a frame to the server socket.
        - ``receive()`` : receive a frame from the server socket.
        - ``is_connected()`` : check if the client is connected with the server.
        - ``disconnect()`` : disconnect from the server socket.
        """
        super().__init__(socket_type="[Client]", show_ip=show_ip, capture_video=capture_video, video_source=video_source)
        self.client_socket = self.socket
        self.stop = self.connect

    def _set_ip(self):
        return input(f"{self.socket_type} >> Select ip: ")

    def connect(self, host_ip=None, port=None):
        """
        Connect to the server socket.\n
        Parameters
        ----------
        - ``host_ip`` (str) : set the host ip,
         if None, get input (default=None).
         - ``port`` (int) : set the host port,
         if None, get input (default=None).
        """
        if not host_ip:
            host_ip = self._set_ip()
        if not port:
            port = self._set_port()
        try:
            self.client_socket.connect((host_ip, port))
            print(f"{self.socket_type} Connected at: {host_ip}")
            if self.capture_video:
                try:
                    self.client_socket.sendall(self._get_size())
                except Exception as error:
                    print(error)
        except:
            pass

    def is_connected(self):
        """
        [!] Coming soon: always return ``True``
        """
        return True
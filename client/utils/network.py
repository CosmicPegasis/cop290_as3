import socket
import pickle
import struct


class Network:
    def __init__(self, game_mode):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.15.136"
        self.game_mode = game_mode
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print("Reached here")
        self.client_number = int((self.client.getsockname())[1])

    def connect(self):
        self.client.connect(self.addr)
        ans = self.recv_one_message().decode()
        return ans  # this conatins the overall data of the game

    def send(self, data):
        data = pickle.dumps(data)
        self.send_one_message(data)
        ans = pickle.loads(self.recv_one_message())
        return ans  # this sends the overall data of the game

    def send_bin(self, data):
        print(len(data))
        self.send_one_message(data)

    def send_one_message(self, data):
        length = len(data)
        self.client.sendall(struct.pack("!I", length))
        self.client.sendall(data)

    def recv_one_message(self):
        lengthbuf = self.recvall(4)
        (length,) = struct.unpack("!I", lengthbuf)
        return self.recvall(length)

    def recvall(self, count):
        buf = b""
        while count:
            newbuf = self.client.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def getP(self):
        return self.p

import socket
import pickle


class Network:
    def __init__(self, game_mode):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.game_mode = game_mode
        self.port = 5555
        self.addr = (self.server, self.port)
        # self.send(str(self.game_mode))
        self.p = self.connect()
        # self.client.sendall(pickle.dumps(self.game_mode))
        print("Reached here")
        self.client_number = int((self.client.getsockname())[1])

    def connect(self):
        try:
            self.client.connect(self.addr)
            # print('r')
            ans = self.client.recv(2048).decode()
            # print("connected successfully")
            return ans  # this conatins the overall data of the game
        except Exception as e:
            print(e)
            print("error in the connect function in network.py")

    def send(self, data):
        try:
            data = pickle.dumps(data)
            self.client.send(data)
            # print("sent successfully")
            # print("reached-2")
            # if (data == "game_mode"):
            #     self.client.sendall(pickle.dumps((data,self.game_mode)))

            ans = pickle.loads(self.client.recv(2048 * 2))
            # print("reached-3")
            return ans  # this sends the overall data of the game
        except Exception as e:
            print(e)
        # print("error in the send function in network.py")

    def send_bin(self, data):
        # bdata = pickle.dumps(data)
        self.client.send(data)

    def getP(self):
        return self.p
